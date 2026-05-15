from __future__ import annotations

from app.schemas.trace_schema import WorkflowTrace

_traces: dict[str, WorkflowTrace] = {}


def save_trace(trace_id: str, trace: WorkflowTrace) -> None:
    _traces[trace_id] = trace


def get_trace(trace_id: str) -> WorkflowTrace | None:
    return _traces.get(trace_id)


def list_traces() -> list[str]:
    return list(_traces.keys())
