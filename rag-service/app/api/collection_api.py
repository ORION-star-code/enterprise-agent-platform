from __future__ import annotations

from fastapi import APIRouter

from app.schemas.document_schema import CollectionStatusResponse
from app.vector_store.collection_manager import CollectionManager


router = APIRouter(prefix="/api/rag", tags=["rag-collections"])


@router.get("/collections/status", response_model=CollectionStatusResponse)
def collection_status() -> CollectionStatusResponse:
    return CollectionManager().status()
