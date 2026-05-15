from __future__ import annotations

from dataclasses import dataclass

from app.schemas.chunk_schema import DocumentChunk


@dataclass(frozen=True, slots=True)
class RankedChunk:
    chunk: DocumentChunk
    score: float


class SimpleReranker:
    def merge(
        self,
        dense_results: list[RankedChunk],
        keyword_results: list[RankedChunk],
        top_k: int,
        dense_weight: float = 0.65,
        keyword_weight: float = 0.35,
    ) -> list[RankedChunk]:
        scores: dict[str, float] = {}
        chunks: dict[str, DocumentChunk] = {}

        for result in dense_results:
            chunks[result.chunk.chunk_id] = result.chunk
            scores[result.chunk.chunk_id] = scores.get(result.chunk.chunk_id, 0.0) + (
                self._normalize_dense(result.score) * dense_weight
            )

        for result in keyword_results:
            chunks[result.chunk.chunk_id] = result.chunk
            scores[result.chunk.chunk_id] = scores.get(result.chunk.chunk_id, 0.0) + (
                min(max(result.score, 0.0), 1.0) * keyword_weight
            )

        ranked = [
            RankedChunk(chunk=chunks[chunk_id], score=score)
            for chunk_id, score in scores.items()
        ]
        ranked.sort(key=lambda item: item.score, reverse=True)
        return ranked[:top_k]

    def _normalize_dense(self, score: float) -> float:
        return min(max((score + 1.0) / 2.0, 0.0), 1.0)
