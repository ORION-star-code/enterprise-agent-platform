from __future__ import annotations


def faq_answer_prompt(question: str, context: str) -> str:
    """Generate a prompt for answering FAQ questions."""
    return (
        "You are a helpful FAQ assistant. Answer the user's question\n"
        "concisely based on the provided FAQ entries. Match the tone and "
        "style of the FAQ documentation.\n\n"
        "Rules:\n"
        "1. Keep answers brief and direct.\n"
        "2. Reference the specific FAQ entry when possible.\n"
        "3. If no FAQ matches, provide a general helpful response and note "
        "that the answer is not from the FAQ database.\n\n"
        f"FAQ Entries:\n{context}\n\n"
        f"User Question: {question}\n\n"
        "Answer:"
    )
