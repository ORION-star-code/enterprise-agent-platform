from __future__ import annotations

from app.graph.state import AgentState


def human_review_node(state: AgentState) -> dict:
    # MVP stub — auto-approve all actions
    trace_entry = {
        "node": "human_review",
        "action": "auto_approve",
        "details": {"approved": True},
    }
    trace = list(state.get("trace", []))
    trace.append(trace_entry)

    return {"trace": trace}
