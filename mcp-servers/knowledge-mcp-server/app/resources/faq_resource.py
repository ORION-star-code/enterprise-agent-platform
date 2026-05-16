from __future__ import annotations

from app.clients.rag_service_client import RagServiceClient


async def get_faq_resource(topic: str) -> str:
    """Retrieve FAQ entries related to a topic.

    URI pattern: kb://faq/{topic}
    """
    client = RagServiceClient()
    data = await client.search(topic, top_k=3, doc_type="faq")

    if not data.get("results"):
        return f"No FAQ entries found for topic: {topic}"

    parts = [f"FAQ search results for: {topic}\n"]
    for i, r in enumerate(data["results"], 1):
        parts.append(
            f"--- FAQ {i} ---\n"
            f"Document: {r['doc_name']}\n"
            f"Section: {r['section']}\n"
            f"Content:\n{r['content']}\n"
        )
    return "\n".join(parts)
