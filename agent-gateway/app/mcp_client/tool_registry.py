from __future__ import annotations

from typing import Any


class ToolRegistry:
    """Registry of available MCP tools. Empty in MVP."""

    def __init__(self) -> None:
        self._tools: dict[str, dict[str, Any]] = {}

    def register(self, name: str, schema: dict[str, Any]) -> None:
        self._tools[name] = schema

    def get(self, name: str) -> dict[str, Any] | None:
        return self._tools.get(name)

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())
