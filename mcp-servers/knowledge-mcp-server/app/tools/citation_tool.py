from __future__ import annotations

from app.clients.rag_service_client import RagServiceClient
from app.schemas.citation_schema import Citation, CitationList


async def extract_citations(
    query: str,
    top_k: int = 5,
    doc_type: str | None = None,
) -> CitationList:
    """Search and extract formatted citations for a query.

    Returns citation objects with content snippets suitable for
    inline reference in agent responses.

    Args:
        query: The search query text.
        top_k: Maximum number of citations (1-10).
        doc_type: Optional filter by document type.
    """
    client = RagServiceClient()
    data = await client.search(query, min(top_k, 10), doc_type)

    citations = [
        Citation(
            chunk_id=r["chunk_id"],
            doc_id=r["doc_id"],
            doc_name=r["doc_name"],
            section=r["section"],
            content_snippet=r["content"][:200],
            score=r["score"],
        )
        for r in data.get("results", [])
    ]

    return CitationList(
        query=query,
        citations=citations,
        total=len(citations),
    )
