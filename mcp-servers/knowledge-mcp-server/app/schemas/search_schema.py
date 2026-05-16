from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=50)
    doc_type: str | None = None
    permission: str | None = None


class SearchResult(BaseModel):
    chunk_id: str
    doc_id: str
    doc_name: str
    section: str
    content: str
    score: float
    metadata: dict[str, Any] = Field(default_factory=dict)


class SearchResponse(BaseModel):
    query: str
    total: int
    results: list[SearchResult] = Field(default_factory=list)
