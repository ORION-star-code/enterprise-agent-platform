from __future__ import annotations

from pathlib import Path

from app.retrievers.hybrid_retriever import HybridRetriever
from app.tasks.document_ingest_task import DocumentIngestTask, IngestDocumentCommand
from app.vector_store.qdrant_store import LocalQdrantStore


def test_store_and_hybrid_retriever_support_metadata_filter(tmp_path: Path) -> None:
    storage = tmp_path / "storage"
    source = tmp_path / "refund.md"
    source.write_text("# Refund Policy\n\nRefund requests are allowed within 7 days.", encoding="utf-8")
    store = LocalQdrantStore(storage)

    response = DocumentIngestTask(store=store).run(
        IngestDocumentCommand(
            file_path=source,
            doc_name="refund.md",
            doc_type="policy",
            department="after_sales",
            permission="internal",
        )
    )

    results = HybridRetriever(store).search(
        "refund conditions",
        top_k=3,
        filters={"doc_type": "policy", "permission": "internal"},
    )

    assert response.chunk_count >= 1
    assert store.document_count() == 1
    assert results
    assert results[0].chunk.doc_name == "refund.md"
    assert "Refund" in results[0].chunk.content
