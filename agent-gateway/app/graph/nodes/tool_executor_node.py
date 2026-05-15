from __future__ import annotations

from typing import Any

from app.graph.state import AgentState


def tool_executor_node(state: AgentState) -> dict:
    # MVP stub — MCP tool execution not yet implemented
    tool_results: list[dict[str, Any]] = []

    trace_entry = {
        "node": "tool_executor",
        "action": "execute_tools",
        "details": {"tool_count": 0, "note": "MCP not implemented"},
    }
    trace = list(state.get("trace", []))
    trace.append(trace_entry)

    return {"tool_results": tool_results, "trace": trace}
