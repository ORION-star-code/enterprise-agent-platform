from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ToolCall(BaseModel):
    tool_name: str
    server: str
    arguments: dict[str, Any] = {}


class ToolResult(BaseModel):
    tool_name: str
    success: bool
    result: Any = None
    error: str | None = None
