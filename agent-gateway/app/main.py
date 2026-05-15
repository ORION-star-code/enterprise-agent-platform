from __future__ import annotations

from fastapi import FastAPI

from app.api.chat_api import router as chat_router
from app.api.session_api import router as session_router
from app.api.trace_api import router as trace_router

app = FastAPI(
    title="Agent Gateway",
    version="0.1.0",
    description="LangGraph-based agent orchestrator",
)

app.include_router(chat_router, tags=["chat"])
app.include_router(session_router, prefix="/api", tags=["sessions"])
app.include_router(trace_router, prefix="/api", tags=["traces"])


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
