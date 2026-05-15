from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.vector_store.collection_manager import CollectionManager


def test_document_upload_search_and_status(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        CollectionManager,
        "default_storage_dir",
        staticmethod(lambda: tmp_path / "storage"),
    )
    client = TestClient(app)

    upload_response = client.post(
        "/api/rag/documents/upload",
        files={"file": ("refund.md", b"# Refund Policy\n\nRefund within 7 days.", "text/markdown")},
        data={"doc_type": "policy", "department": "after_sales", "permission": "internal"},
    )
    assert upload_response.status_code == 200
    uploaded = upload_response.json()
    assert uploaded["chunk_count"] == 1

    list_response = client.get("/api/rag/documents")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1

    search_response = client.post(
        "/api/rag/search",
        json={"query": "refund conditions", "top_k": 5, "doc_type": "policy", "permission": "internal"},
    )
    assert search_response.status_code == 200
    results = search_response.json()["results"]
    assert results
    assert results[0]["doc_name"] == "refund.md"

    chunk_response = client.get(f"/api/rag/chunks/{results[0]['chunk_id']}")
    assert chunk_response.status_code == 200
    assert chunk_response.json()["doc_id"] == uploaded["doc_id"]

    status_response = client.get("/api/rag/collections/status")
    assert status_response.status_code == 200
    assert status_response.json()["document_count"] == 1
