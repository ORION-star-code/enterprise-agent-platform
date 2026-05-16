from __future__ import annotations

from typing import Any

from app.clients.rag_service_client import RagServiceClient


async def get_document_chunk(chunk_id: str) -> dict[str, Any]:
    """Retrieve a specific document chunk by its ID.

    Args:
        chunk_id: The unique identifier of the chunk.
    """
    client = RagServiceClient()
    return await client.get_chunk(chunk_id)


async def list_available_documents(
    doc_type: str | None = None,
) -> dict[str, Any]:
    """List all indexed documents in the knowledge base.

    Args:
        doc_type: Optional filter by document type.
    """
    client = RagServiceClient()
    data = await client.list_documents()
    if doc_type:
        data["documents"] = [
            d for d in data["documents"] if d.get("doc_type") == doc_type
        ]
        data["total"] = len(data["documents"])
    return data


async def get_document_summary(doc_id: str) -> dict[str, Any]:
    """Get a summary view of a document (metadata + chunk count).

    Args:
        doc_id: The unique identifier of the document.
    """
    client = RagServiceClient()
    data = await client.list_documents()
    for doc in data.get("documents", []):
        if doc["doc_id"] == doc_id:
            return {
                "doc_id": doc["doc_id"],
                "doc_name": doc["doc_name"],
                "doc_type": doc["doc_type"],
                "department": doc["department"],
                "chunk_count": doc["chunk_count"],
                "status": doc["status"],
                "created_at": doc["created_at"],
            }
    return {"error": f"Document {doc_id} not found"}
