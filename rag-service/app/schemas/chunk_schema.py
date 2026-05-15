from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ChunkMetadata(BaseModel):
    doc_id: str
    doc_name: str
    doc_type: str = "policy"
    department: str = "general"
    permission: str = "internal"
    section: str = "General"
    created_at: str


class DocumentChunk(BaseModel):
    chunk_id: str
    doc_id: str
    doc_name: str
    section: str
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    embedding: list[float] = Field(default_factory=list)


class ChunkResponse(BaseModel):
    chunk_id: str
    doc_id: str
    doc_name: str
    section: str
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)


def chunk_to_response(chunk: DocumentChunk) -> ChunkResponse:
    return ChunkResponse(
        chunk_id=chunk.chunk_id,
        doc_id=chunk.doc_id,
        doc_name=chunk.doc_name,
        section=chunk.section,
        content=chunk.content,
        metadata=chunk.metadata,
    )
