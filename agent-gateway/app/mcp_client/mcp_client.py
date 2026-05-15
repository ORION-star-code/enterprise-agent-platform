from __future__ import annotations

from typing import Any


class MCPClient:
    """MCP protocol client stub. Not implemented in MVP."""

    def __init__(self, server_url: str) -> None:
        self.server_url = server_url

    async def list_tools(self) -> list[dict[str, Any]]:
        return []

    async def call_tool(
        self, tool_name: str, arguments: dict[str, Any]
    ) -> dict[str, Any]:
        return {"error": "MCP client not implemented"}
