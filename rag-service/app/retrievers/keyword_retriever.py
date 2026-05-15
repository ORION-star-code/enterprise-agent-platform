from __future__ import annotations

from collections import Counter

from app.embeddings.embedding_client import extract_text_features
from app.retrievers.reranker import RankedChunk
from app.vector_store.qdrant_store import LocalQdrantStore


class KeywordRetriever:
    def __init__(self, store: LocalQdrantStore | None = None) -> None:
        self.store = store or LocalQdrantStore()

    def search(
        self,
        query: str,
        top_k: int,
        filters: dict[str, str] | None = None,
    ) -> list[RankedChunk]:
        query_features = Counter(extract_text_features(query))
        if not query_features:
            return []

        results: list[RankedChunk] = []
        for chunk in self.store.list_chunks(filters):
            content_features = Counter(extract_text_features(chunk.content))
            overlap = sum(
                min(count, content_features.get(feature, 0))
                for feature, count in query_features.items()
            )
            score = overlap / max(1, sum(query_features.values()))
            if score > 0:
                results.append(RankedChunk(chunk=chunk, score=score))

        results.sort(key=lambda item: item.score, reverse=True)
        return results[:top_k]
