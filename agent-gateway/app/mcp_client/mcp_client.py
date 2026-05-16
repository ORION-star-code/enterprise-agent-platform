from __future__ import annotations

from typing import Any

from mcp import ClientSession
from mcp.client.sse import sse_client


class MCPClient:
    """MCP protocol client using SSE transport."""

    def __init__(self, server_url: str) -> None:
        self.server_url = server_url

    async def list_tools(self) -> list[dict[str, Any]]:
        """Connect to the MCP server and list available tools."""
        async with sse_client(self.server_url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                return [t.model_dump() for t in tools.tools]

    async def call_tool(
        self, tool_name: str, arguments: dict[str, Any]
    ) -> dict[str, Any]:
        """Connect to the MCP server and invoke a tool."""
        async with sse_client(self.server_url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return {
                    "content": [c.model_dump() for c in result.content]
                }
