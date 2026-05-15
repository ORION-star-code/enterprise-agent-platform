from __future__ import annotations

from fastapi import APIRouter

from app.memory.session_memory import clear_session, list_sessions

router = APIRouter()


@router.get("/sessions")
async def get_sessions() -> dict:
    return {"sessions": list_sessions()}


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str) -> dict:
    clear_session(session_id)
    return {"deleted": session_id}
