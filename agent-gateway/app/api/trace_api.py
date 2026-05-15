from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.memory.message_store import get_trace

router = APIRouter()


@router.get("/traces/{trace_id}")
async def get_trace_detail(trace_id: str) -> dict:
    trace = get_trace(trace_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Trace not found.")
    return trace.model_dump()
