from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.retrievers.hybrid_retriever import HybridRetriever
from app.schemas.search_schema import SearchRequest, SearchResponse, SearchResult


router = APIRouter(prefix="/api/rag", tags=["rag-search"])


@router.post("/search", response_model=SearchResponse)
def search_documents(request: SearchRequest) -> SearchResponse:
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Search query must not be empty.")

    filters = {
        key: value
        for key, value in {
            "doc_type": request.doc_type,
            "permission": request.permission,
        }.items()
        if value
    }
    results = HybridRetriever().search(query, request.top_k, filters or None)

    return SearchResponse(
        query=query,
        total=len(results),
        results=[
            SearchResult(
                chunk_id=result.chunk.chunk_id,
                doc_id=result.chunk.doc_id,
                doc_name=result.chunk.doc_name,
                section=result.chunk.section,
                content=result.chunk.content,
                score=round(result.score, 6),
                metadata=result.chunk.metadata,
            )
            for result in results
        ],
    )
