from __future__ import annotations

from typing import Any

import httpx

from app.config import get_settings


class RagServiceClient:
    """Async HTTP client for the rag-service API."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or get_settings().rag_service_url

    async def search(
        self,
        query: str,
        top_k: int = 5,
        doc_type: str | None = None,
        permission: str | None = None,
    ) -> dict[str, Any]:
        """POST /api/rag/search"""
        payload: dict[str, Any] = {"query": query, "top_k": top_k}
        if doc_type:
            payload["doc_type"] = doc_type
        if permission:
            payload["permission"] = permission
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/api/rag/search", json=payload
            )
            resp.raise_for_status()
            result: dict[str, Any] = resp.json()
            return result

    async def list_documents(self) -> dict[str, Any]:
        """GET /api/rag/documents"""
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/api/rag/documents")
            resp.raise_for_status()
            result: dict[str, Any] = resp.json()
            return result

    async def get_chunk(self, chunk_id: str) -> dict[str, Any]:
        """GET /api/rag/chunks/{chunk_id}"""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/api/rag/chunks/{chunk_id}"
            )
            resp.raise_for_status()
            result: dict[str, Any] = resp.json()
            return result

    async def collection_status(self) -> dict[str, Any]:
        """GET /api/rag/collections/status"""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/api/rag/collections/status"
            )
            resp.raise_for_status()
            result: dict[str, Any] = resp.json()
            return result
