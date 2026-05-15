from __future__ import annotations

from typing import Any

from app.graph.state import AgentState


def rag_node(state: AgentState) -> dict:
    query = state["user_message"]
    results: list[dict[str, Any]] = []

    try:
        from app.retrievers.hybrid_retriever import HybridRetriever
        from app.vector_store.qdrant_store import LocalQdrantStore

        store = LocalQdrantStore()
        retriever = HybridRetriever(store)
        hits = retriever.search(query, top_k=5)

        results = [
            {
                "chunk_id": hit.chunk.chunk_id,
                "doc_name": hit.chunk.doc_name,
                "section": hit.chunk.section,
                "content": hit.chunk.content,
                "score": round(hit.score, 6),
                "metadata": hit.chunk.metadata,
            }
            for hit in hits
        ]
    except Exception:
        results = []

    trace_entry = {
        "node": "rag",
        "action": "search",
        "details": {"query": query, "result_count": len(results)},
    }
    trace = list(state.get("trace", []))
    trace.append(trace_entry)

    return {"rag_results": results, "trace": trace}
