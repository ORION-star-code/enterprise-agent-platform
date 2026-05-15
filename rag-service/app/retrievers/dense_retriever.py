from __future__ import annotations

from app.embeddings.embedding_client import HashEmbeddingClient, cosine_similarity
from app.retrievers.reranker import RankedChunk
from app.vector_store.qdrant_store import LocalQdrantStore


class DenseRetriever:
    def __init__(
        self,
        store: LocalQdrantStore | None = None,
        embedding_client: HashEmbeddingClient | None = None,
    ) -> None:
        self.store = store or LocalQdrantStore()
        self.embedding_client = embedding_client or HashEmbeddingClient()

    def search(
        self,
        query: str,
        top_k: int,
        filters: dict[str, str] | None = None,
    ) -> list[RankedChunk]:
        query_vector = self.embedding_client.embed_text(query)
        results = [
            RankedChunk(
                chunk=chunk,
                score=cosine_similarity(query_vector, chunk.embedding),
            )
            for chunk in self.store.list_chunks(filters)
        ]
        results.sort(key=lambda item: item.score, reverse=True)
        return results[:top_k]
