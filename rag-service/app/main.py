from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.collection_api import router as collection_router
from app.api.document_api import router as document_router
from app.api.search_api import router as search_router
from app.vector_store.collection_manager import CollectionManager


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    CollectionManager().initialize()
    yield


app = FastAPI(
    title="Enterprise RAG Service",
    version="0.1.0",
    description="Local MVP RAG service for document ingestion and retrieval.",
    lifespan=lifespan,
)

app.include_router(document_router)
app.include_router(search_router)
app.include_router(collection_router)


@app.get("/api/rag/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "storage_type": "local-json-qdrant-compatible",
    }


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "rag-service", "status": "ok"}
