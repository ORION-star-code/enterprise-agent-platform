from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True, slots=True)
class EmbeddingConfig:
    provider: str = "hash"
    dimension: int = 128


def get_embedding_config() -> EmbeddingConfig:
    provider = os.getenv("RAG_EMBEDDING_PROVIDER", "hash")
    dimension = int(os.getenv("RAG_EMBEDDING_DIMENSION", "128"))
    return EmbeddingConfig(provider=provider, dimension=dimension)
