from __future__ import annotations

from typing import Any, Protocol


class LLMClient(Protocol):
    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str: ...


class MockLLMClient:
    """Rule-based mock LLM for MVP. No external API needed."""

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        if not messages:
            return ""
        last = messages[-1]["content"]
        system = next(
            (m["content"] for m in messages if m["role"] == "system"), ""
        )

        if "intent" in system.lower() or "classify" in system.lower():
            return self._classify_intent(last)
        if "plan" in system.lower():
            return self._make_plan(last)
        return self._synthesize(last)

    def _classify_intent(self, text: str) -> str:
        keywords_search = ["what", "how", "why", "when", "where", "who",
                           "policy", "document", "search", "find", "tell",
                           "explain", "?", "refund", "return", "rule"]
        keywords_biz = ["order", "customer", "inventory", "ticket",
                        "create", "update", "delete", "status", "check"]
        lower = text.lower()
        biz_score = sum(1 for k in keywords_biz if k in lower)
        search_score = sum(1 for k in keywords_search if k in lower)
        if biz_score > search_score and biz_score > 0:
            return "business_operation"
        if search_score > 0:
            return "knowledge_search"
        return "general_chat"

    def _make_plan(self, text: str) -> str:
        return '["search_knowledge_base", "synthesize_response"]'

    def _synthesize(self, text: str) -> str:
        return (
            "Based on the retrieved context, here is what I found:\n\n"
            + text
        )


def get_llm_client(provider: str = "mock") -> LLMClient:
    if provider == "mock":
        return MockLLMClient()
    raise ValueError(f"Unsupported LLM provider: {provider}")
