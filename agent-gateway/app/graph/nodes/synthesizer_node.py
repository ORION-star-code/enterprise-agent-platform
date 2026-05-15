from __future__ import annotations

from app.graph.state import AgentState
from app.llm.model_client import get_llm_client
from app.llm.prompts import SYNTHESIZER_PROMPT


def synthesizer_node(state: AgentState) -> dict:
    llm = get_llm_client()

    context_parts: list[str] = []

    rag_results = state.get("rag_results") or []
    if rag_results:
        context_parts.append("Retrieved context:")
        for r in rag_results:
            context_parts.append(
                f"- [{r['doc_name']}] {r['section']}: {r['content']}"
            )

    tool_results = state.get("tool_results") or []
    if tool_results:
        context_parts.append("Tool results:")
        for t in tool_results:
            context_parts.append(f"- {t}")

    context = "\n".join(context_parts) if context_parts else "No context available."

    messages = [
        {"role": "system", "content": SYNTHESIZER_PROMPT},
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nUser: {state['user_message']}",
        },
    ]
    response = llm.chat(messages)

    trace_entry = {
        "node": "synthesizer",
        "action": "generate_response",
        "details": {"response_length": len(response)},
    }
    trace = list(state.get("trace", []))
    trace.append(trace_entry)

    return {"response": response, "trace": trace}
