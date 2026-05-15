from __future__ import annotations

from app.graph.state import AgentState
from app.llm.model_client import get_llm_client
from app.llm.prompts import INTENT_ROUTER_PROMPT


def intent_router_node(state: AgentState) -> dict:
    llm = get_llm_client()
    messages = [
        {"role": "system", "content": INTENT_ROUTER_PROMPT},
        {"role": "user", "content": state["user_message"]},
    ]
    intent = llm.chat(messages).strip().lower()

    valid = {"knowledge_search", "business_operation", "general_chat"}
    if intent not in valid:
        intent = "general_chat"

    trace_entry = {
        "node": "intent_router",
        "action": "classify",
        "details": {"intent": intent},
    }
    trace = list(state.get("trace", []))
    trace.append(trace_entry)

    return {"intent": intent, "trace": trace}
