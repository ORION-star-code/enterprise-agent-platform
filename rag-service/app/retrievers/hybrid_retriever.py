from __future__ import annotations

from app.retrievers.dense_retriever import DenseRetriever
from app.retrievers.keyword_retriever import KeywordRetriever
from app.retrievers.reranker import RankedChunk, SimpleReranker
from app.vector_store.qdrant_store import LocalQdrantStore


class HybridRetriever:
    def __init__(self, store: LocalQdrantStore | None = None) -> None:
        self.store = store or LocalQdrantStore()
        self.dense_retriever = DenseRetriever(self.store)
        self.keyword_retriever = KeywordRetriever(self.store)
        self.reranker = SimpleReranker()

    def search(
        self,
        query: str,
        top_k: int,
        filters: dict[str, str] | None = None,
    ) -> list[RankedChunk]:
        recall_size = max(top_k * 4, top_k)
        dense_results = self.dense_retriever.search(query, recall_size, filters)
        keyword_results = self.keyword_retriever.search(query, recall_size, filters)
        return self.reranker.merge(dense_results, keyword_results, top_k)
