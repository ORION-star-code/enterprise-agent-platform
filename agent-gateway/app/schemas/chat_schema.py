from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class Message(BaseModel):
    role: str
    content: str


class SourceItem(BaseModel):
    doc_name: str
    section: str
    score: float


class ChatResponse(BaseModel):
    response: str
    session_id: str
    intent: str | None = None
    sources: list[SourceItem] = Field(default_factory=list)
