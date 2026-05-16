from __future__ import annotations

from app.clients.rag_service_client import RagServiceClient
from app.schemas.search_schema import SearchResponse


async def search_knowledge_base(
    query: str,
    top_k: int = 5,
    doc_type: str | None = None,
    permission: str | None = None,
) -> SearchResponse:
    """Search the enterprise knowledge base using hybrid retrieval.

    Args:
        query: The search query text.
        top_k: Maximum number of results to return (1-50).
        doc_type: Filter by document type (e.g., 'policy', 'faq', 'sop').
        permission: Filter by permission level (e.g., 'internal', 'public').
    """
    client = RagServiceClient()
    data = await client.search(query, top_k, doc_type, permission)
    return SearchResponse(**data)
