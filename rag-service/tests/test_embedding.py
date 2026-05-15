from __future__ import annotations

from app.embeddings.embedding_client import HashEmbeddingClient


def test_hash_embedding_is_stable_and_distinguishes_text() -> None:
    client = HashEmbeddingClient()

    refund_a = client.embed_text("refund policy")
    refund_b = client.embed_text("refund policy")
    order = client.embed_text("order status")

    assert refund_a == refund_b
    assert refund_a != order
    assert len(refund_a) == 128
