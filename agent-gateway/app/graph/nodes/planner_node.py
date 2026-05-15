from __future__ import annotations

import json

from app.graph.state import AgentState
from app.llm.model_client import get_llm_client
from app.llm.prompts import PLANNER_PROMPT


def planner_node(state: AgentState) -> dict:
    llm = get_llm_client()
    intent = state.get("intent", "general_chat")
    context = f"Intent: {intent}\nUser: {state['user_message']}"

    messages = [
        {"role": "system", "content": PLANNER_PROMPT},
        {"role": "user", "content": context},
    ]
    raw = llm.chat(messages).strip()

    try:
        plan = json.loads(raw)
    except json.JSONDecodeError:
        if intent == "knowledge_search":
            plan = ["search_knowledge_base", "synthesize_response"]
        elif intent == "business_operation":
            plan = ["execute_tool", "human_review", "synthesize_response"]
        else:
            plan = ["synthesize_response"]

    trace_entry = {
        "node": "planner",
        "action": "plan",
        "details": {"plan": plan},
    }
    trace = list(state.get("trace", []))
    trace.append(trace_entry)

    return {"plan": plan, "trace": trace}
