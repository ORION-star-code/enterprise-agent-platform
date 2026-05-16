from __future__ import annotations

from app.prompts.faq_answer_prompt import faq_answer_prompt
from app.prompts.policy_answer_prompt import policy_answer_prompt
from app.prompts.summarize_doc_prompt import summarize_doc_prompt


def test_policy_answer_prompt_contains_question() -> None:
    result = policy_answer_prompt("What is the refund policy?", "Some context")
    assert "What is the refund policy?" in result


def test_policy_answer_prompt_contains_context() -> None:
    result = policy_answer_prompt("question", "Refund within 7 days")
    assert "Refund within 7 days" in result


def test_policy_answer_prompt_has_rules() -> None:
    result = policy_answer_prompt("q", "c")
    assert "Cite the specific document" in result
    assert "Do not speculate" in result


def test_faq_answer_prompt_contains_question() -> None:
    result = faq_answer_prompt("How to reset password?", "FAQ content")
    assert "How to reset password?" in result


def test_faq_answer_prompt_contains_context() -> None:
    result = faq_answer_prompt("q", "Go to settings page")
    assert "Go to settings page" in result


def test_summarize_doc_prompt_contains_doc_name() -> None:
    result = summarize_doc_prompt("manual.pdf", "Some content")
    assert "manual.pdf" in result


def test_summarize_doc_prompt_contains_content() -> None:
    result = summarize_doc_prompt("doc", "Important information here")
    assert "Important information here" in result
