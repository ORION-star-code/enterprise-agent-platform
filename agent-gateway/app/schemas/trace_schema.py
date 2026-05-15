from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class TraceStep(BaseModel):
    node: str
    action: str
    details: dict[str, Any] = {}


class WorkflowTrace(BaseModel):
    trace_id: str
    session_id: str
    steps: list[TraceStep] = []
    final_response: str | None = None
