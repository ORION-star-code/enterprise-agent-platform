from __future__ import annotations

from pydantic import BaseModel, Field


class Citation(BaseModel):
    chunk_id: str
    doc_id: str
    doc_name: str
    section: str
    content_snippet: str
    score: float


class CitationList(BaseModel):
    query: str
    citations: list[Citation] = Field(default_factory=list)
    total: int = 0
