from __future__ import annotations

import re
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.metadata.metadata_extractor import generate_doc_id
from app.schemas.chunk_schema import ChunkResponse, chunk_to_response
from app.schemas.document_schema import (
    DocumentListResponse,
    DocumentUploadResponse,
    ReindexDocumentRequest,
)
from app.tasks.document_ingest_task import DocumentIngestTask, IngestDocumentCommand
from app.vector_store.collection_manager import CollectionManager
from app.vector_store.qdrant_store import LocalQdrantStore


router = APIRouter(prefix="/api/rag", tags=["rag-documents"])


@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    doc_type: str = Form("policy"),
    department: str = Form("general"),
    permission: str = Form("internal"),
) -> DocumentUploadResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a filename.")

    doc_id = generate_doc_id()
    manager = CollectionManager()
    manager.initialize()
    target_path = manager.uploads_dir / f"{doc_id}_{_safe_filename(file.filename)}"
    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    target_path.write_bytes(content)

    try:
        return DocumentIngestTask().run(
            IngestDocumentCommand(
                file_path=target_path,
                doc_name=file.filename,
                doc_type=doc_type,
                department=department,
                permission=permission,
                doc_id=doc_id,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/documents", response_model=DocumentListResponse)
def list_documents() -> DocumentListResponse:
    documents = LocalQdrantStore().list_documents()
    return DocumentListResponse(documents=documents, total=len(documents))


@router.post("/documents/reindex", response_model=DocumentUploadResponse)
def reindex_document(request: ReindexDocumentRequest) -> DocumentUploadResponse:
    store = LocalQdrantStore()
    document = store.get_document(request.doc_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    source_path = Path(document.source_path)
    if not source_path.exists():
        raise HTTPException(status_code=404, detail="Document source file not found.")

    try:
        return DocumentIngestTask(store=store).run(
            IngestDocumentCommand(
                file_path=source_path,
                doc_name=document.doc_name,
                doc_type=document.doc_type,
                department=document.department,
                permission=document.permission,
                doc_id=document.doc_id,
                created_at=document.created_at,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/chunks/{chunk_id}", response_model=ChunkResponse)
def get_chunk(chunk_id: str) -> ChunkResponse:
    chunk = LocalQdrantStore().get_chunk(chunk_id)
    if not chunk:
        raise HTTPException(status_code=404, detail="Chunk not found.")
    return chunk_to_response(chunk)


def _safe_filename(filename: str) -> str:
    name = Path(filename).name
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
    return safe or "document"
