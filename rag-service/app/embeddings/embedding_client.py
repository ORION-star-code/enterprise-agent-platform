from __future__ import annotations

import hashlib
import math
import re

from app.embeddings.embedding_config import EmbeddingConfig, get_embedding_config


WORD_PATTERN = re.compile(r"[\w]+", re.UNICODE)


def extract_text_features(text: str) -> list[str]:
    normalized = text.lower()
    compact = re.sub(r"\s+", "", normalized)
    features: list[str] = []

    features.extend(token for token in WORD_PATTERN.findall(normalized) if token)

    for size in (2, 3, 4):
        if len(compact) >= size:
            features.extend(
                compact[index : index + size]
                for index in range(len(compact) - size + 1)
            )

    return features or [normalized]


class HashEmbeddingClient:
    def __init__(self, config: EmbeddingConfig | None = None) -> None:
        self.config = config or get_embedding_config()
        if self.config.provider != "hash":
            raise ValueError(
                f"Unsupported embedding provider for MVP: {self.config.provider}"
            )

    def embed_text(self, text: str) -> list[float]:
        vector = [0.0] * self.config.dimension

        for feature in extract_text_features(text):
            digest = hashlib.sha256(feature.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.config.dimension
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector

        return [value / norm for value in vector]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    return sum(a * b for a, b in zip(left, right, strict=True))
