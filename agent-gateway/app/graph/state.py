from __future__ import annotations

from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    messages: list[dict[str, str]]
    user_message: str
    intent: str | None
    plan: list[str] | None
    rag_results: list[dict[str, Any]] | None
    tool_results: list[dict[str, Any]] | None
    response: str | None
    trace: list[dict[str, Any]]
