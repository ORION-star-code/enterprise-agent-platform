from __future__ import annotations

from app.graph.workflow import compile_workflow


def test_knowledge_search_workflow() -> None:
    workflow = compile_workflow()
    result = workflow.invoke({
        "messages": [],
        "user_message": "What is the refund policy?",
        "intent": None,
        "plan": None,
        "rag_results": None,
        "tool_results": None,
        "response": None,
        "trace": [],
    })

    assert result["intent"] == "knowledge_search"
    assert result["response"] is not None
    assert len(result["trace"]) >= 2


def test_general_chat_workflow() -> None:
    workflow = compile_workflow()
    result = workflow.invoke({
        "messages": [],
        "user_message": "Hello!",
        "intent": None,
        "plan": None,
        "rag_results": None,
        "tool_results": None,
        "response": None,
        "trace": [],
    })

    assert result["intent"] == "general_chat"
    assert result["response"] is not None


def test_business_operation_workflow() -> None:
    workflow = compile_workflow()
    result = workflow.invoke({
        "messages": [],
        "user_message": "Check order status for customer #123",
        "intent": None,
        "plan": None,
        "rag_results": None,
        "tool_results": None,
        "response": None,
        "trace": [],
    })

    assert result["intent"] == "business_operation"
    assert result["response"] is not None
