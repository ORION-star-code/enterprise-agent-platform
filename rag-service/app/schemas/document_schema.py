from __future__ import annotations

from pydantic import BaseModel, Field


class DocumentRecord(BaseModel):
    doc_id: str
    doc_name: str
    doc_type: str = "policy"
    department: str = "general"
    permission: str = "internal"
    source_path: str
    chunk_count: int = 0
    status: str = "indexed"
    created_at: str
    updated_at: str


class DocumentUploadResponse(BaseModel):
    doc_id: str
    doc_name: str
    chunk_count: int
    status: str


class DocumentListResponse(BaseModel):
    documents: list[DocumentRecord] = Field(default_factory=list)
    total: int


class ReindexDocumentRequest(BaseModel):
    doc_id: str


class CollectionStatusResponse(BaseModel):
    storage_type: str
    document_count: int
    chunk_count: int
    storage_path: str
