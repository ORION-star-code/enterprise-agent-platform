from __future__ import annotations

from typing import Any

import pytest

from app.clients.rag_service_client import RagServiceClient


@pytest.fixture
def rag_client() -> RagServiceClient:
    return RagServiceClient(base_url="http://test-rag:8000")


MOCK_SEARCH_RESPONSE: dict[str, Any] = {
    "query": "refund",
    "total": 1,
    "results": [
        {
            "chunk_id": "chunk_001",
            "doc_id": "doc_001",
            "doc_name": "refund_policy.md",
            "section": "Chapter 3",
            "content": "Refund within 7 days of purchase.",
            "score": 0.86,
            "metadata": {"doc_type": "policy"},
        }
    ],
}

MOCK_DOCUMENTS_RESPONSE: dict[str, Any] = {
    "documents": [
        {
            "doc_id": "doc_001",
            "doc_name": "refund_policy.md",
            "doc_type": "policy",
            "department": "after_sales",
            "permission": "internal",
            "source_path": "/storage/uploads/doc_001",
            "chunk_count": 3,
            "status": "indexed",
            "created_at": "2026-05-01T00:00:00",
            "updated_at": "2026-05-01T00:00:00",
        },
        {
            "doc_id": "doc_002",
            "doc_name": "faq_orders.md",
            "doc_type": "faq",
            "department": "support",
            "permission": "public",
            "source_path": "/storage/uploads/doc_002",
            "chunk_count": 5,
            "status": "indexed",
            "created_at": "2026-05-02T00:00:00",
            "updated_at": "2026-05-02T00:00:00",
        },
    ],
    "total": 2,
}

MOCK_CHUNK_RESPONSE: dict[str, Any] = {
    "chunk_id": "chunk_001",
    "doc_id": "doc_001",
    "doc_name": "refund_policy.md",
    "section": "Chapter 3",
    "content": "Refund within 7 days of purchase.",
    "metadata": {"doc_type": "policy"},
}
