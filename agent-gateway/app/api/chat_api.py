from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter

from app.graph.workflow import compile_workflow
from app.memory.session_memory import add_message, get_session
from app.memory.message_store import save_trace
from app.schemas.chat_schema import ChatRequest, ChatResponse, Message, SourceItem
from app.schemas.trace_schema import TraceStep, WorkflowTrace

router = APIRouter()

_workflow = None


def _get_workflow():
    global _workflow
    if _workflow is None:
        _workflow = compile_workflow()
    return _workflow


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    session = get_session(request.session_id)

    initial_state = {
        "messages": [{"role": m.role, "content": m.content} for m in session],
        "user_message": request.message,
        "intent": None,
        "plan": None,
        "rag_results": None,
        "tool_results": None,
        "response": None,
        "trace": [],
    }

    workflow = _get_workflow()
    result = workflow.invoke(initial_state)

    response_text = result.get("response", "I could not generate a response.")
    intent = result.get("intent")
    rag_results = result.get("rag_results") or []

    add_message(request.session_id, Message(role="user", content=request.message))
    add_message(request.session_id, Message(role="assistant", content=response_text))

    trace_id = uuid4().hex
    trace_steps = [
        TraceStep(**step) for step in result.get("trace", [])
    ]
    save_trace(
        trace_id,
        WorkflowTrace(
            trace_id=trace_id,
            session_id=request.session_id,
            steps=trace_steps,
            final_response=response_text,
        ),
    )

    sources = [
        SourceItem(
            doc_name=r["doc_name"],
            section=r["section"],
            score=r["score"],
        )
        for r in rag_results
    ]

    return ChatResponse(
        response=response_text,
        session_id=request.session_id,
        intent=intent,
        sources=sources,
    )
