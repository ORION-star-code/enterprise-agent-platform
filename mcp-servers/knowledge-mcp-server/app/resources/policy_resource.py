from __future__ import annotations

from app.clients.rag_service_client import RagServiceClient


async def get_policy_resource(topic: str) -> str:
    """Retrieve policy documents related to a topic.

    URI pattern: kb://policy/{topic}
    """
    client = RagServiceClient()
    data = await client.search(topic, top_k=3, doc_type="policy")

    if not data.get("results"):
        return f"No policy documents found for topic: {topic}"

    parts = [f"Policy search results for: {topic}\n"]
    for i, r in enumerate(data["results"], 1):
        parts.append(
            f"--- Result {i} ---\n"
            f"Document: {r['doc_name']}\n"
            f"Section: {r['section']}\n"
            f"Score: {r['score']:.4f}\n"
            f"Content:\n{r['content']}\n"
        )
    return "\n".join(parts)
