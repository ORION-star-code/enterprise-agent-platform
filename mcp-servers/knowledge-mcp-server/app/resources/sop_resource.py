from __future__ import annotations

from app.clients.rag_service_client import RagServiceClient


async def get_sop_resource(topic: str) -> str:
    """Retrieve SOP documents related to a topic.

    URI pattern: kb://sop/{topic}
    """
    client = RagServiceClient()
    data = await client.search(topic, top_k=3, doc_type="sop")

    if not data.get("results"):
        return f"No SOP documents found for topic: {topic}"

    parts = [f"SOP search results for: {topic}\n"]
    for i, r in enumerate(data["results"], 1):
        parts.append(
            f"--- SOP {i} ---\n"
            f"Document: {r['doc_name']}\n"
            f"Section: {r['section']}\n"
            f"Content:\n{r['content']}\n"
        )
    return "\n".join(parts)
