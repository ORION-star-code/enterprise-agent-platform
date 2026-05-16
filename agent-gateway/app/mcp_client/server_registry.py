from __future__ import annotations

from app.core.config import get_settings


class ServerRegistry:
    """Registry of MCP server endpoints."""

    def __init__(self) -> None:
        settings = get_settings()
        self._servers: dict[str, str] = {
            "knowledge": settings.mcp_knowledge_url,
            "business": settings.mcp_business_url,
        }

    def get_url(self, name: str) -> str | None:
        return self._servers.get(name)

    def list_servers(self) -> list[str]:
        return list(self._servers.keys())
