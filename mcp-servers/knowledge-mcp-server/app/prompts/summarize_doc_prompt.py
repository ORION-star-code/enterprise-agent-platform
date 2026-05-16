from __future__ import annotations


def summarize_doc_prompt(doc_name: str, content: str) -> str:
    """Generate a prompt for summarizing a document."""
    return (
        "Summarize the following document. Provide:\n"
        "1. A one-sentence overview.\n"
        "2. Key points (3-5 bullet points).\n"
        "3. The document's primary audience and purpose.\n\n"
        f"Document: {doc_name}\n\n"
        f"Content:\n{content}\n\n"
        "Summary:"
    )
