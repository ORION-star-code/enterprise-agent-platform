from __future__ import annotations

import asyncio
import concurrent.futures
from typing import Any

from app.graph.state import AgentState
from app.mcp_client.mcp_client import MCPClient
from app.mcp_client.server_registry import ServerRegistry

# Map plan step names to (server_name, tool_name)
_STEP_TOOLS: dict[str, tuple[str, str]] = {
    "query_order": ("business", "order_lookup"),
    "query_customer": ("business", "customer_lookup"),
    "query_inventory": ("business", "inventory_check"),
    "query_tickets": ("business", "ticket_lookup"),
    "recent_orders": ("business", "recent_orders"),
    "search_knowledge_base": ("knowledge", "knowledge_search"),
}


def _run_in_new_loop(coro: Any) -> Any:
    """Run async coroutine in a new event loop on a separate thread."""
    def _target() -> Any:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()
            asyncio.set_event_loop(None)

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_target)
        return future.result()


async def _execute_tools(
    user_message: str, plan: list[str] | None
) -> list[dict[str, Any]]:
    registry = ServerRegistry()
    results: list[dict[str, Any]] = []

    tools_to_call: list[tuple[str, str, dict[str, Any]]] = []

    if plan:
        for step in plan:
            if step in _STEP_TOOLS:
                server, tool = _STEP_TOOLS[step]
                args: dict[str, Any] = {}
                if tool == "knowledge_search":
                    args = {"query": user_message}
                elif tool in ("order_lookup", "query_order"):
                    args = {"order_id": user_message}
                elif tool in ("customer_lookup", "query_customer"):
                    args = {"customer_name": user_message}
                elif tool == "inventory_check":
                    args = {"sku": user_message}
                elif tool == "ticket_lookup":
                    args = {"customer_name": user_message}
                elif tool == "recent_orders":
                    args = {"customer_name": user_message}
                tools_to_call.append((server, tool, args))

    if not tools_to_call:
        tools_to_call.append((
            "business",
            "order_lookup",
            {"order_id": user_message},
        ))

    for server_name, tool_name, args in tools_to_call:
        url = registry.get_url(server_name)
        if not url:
            results.append({
                "tool": tool_name,
                "error": f"Server '{server_name}' not configured",
            })
            continue

        try:
            client = MCPClient(url)
            result = await client.call_tool(tool_name, args)
            results.append({
                "server": server_name,
                "tool": tool_name,
                "arguments": args,
                "result": result,
            })
        except Exception as e:
            results.append({
                "server": server_name,
                "tool": tool_name,
                "error": str(e),
            })

    return results


def tool_executor_node(state: AgentState) -> dict:
    user_message = state.get("user_message", "")
    plan = state.get("plan")

    tool_results = _run_in_new_loop(_execute_tools(user_message, plan))

    trace_entry = {
        "node": "tool_executor",
        "action": "execute_tools",
        "details": {"tool_count": len(tool_results)},
    }
    trace = list(state.get("trace", []))
    trace.append(trace_entry)

    return {"tool_results": tool_results, "trace": trace}
