from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.graph.nodes.human_review_node import human_review_node
from app.graph.nodes.intent_router_node import intent_router_node
from app.graph.nodes.planner_node import planner_node
from app.graph.nodes.rag_node import rag_node
from app.graph.nodes.synthesizer_node import synthesizer_node
from app.graph.nodes.tool_executor_node import tool_executor_node
from app.graph.state import AgentState


def _route_intent(state: AgentState) -> str:
    intent = state.get("intent", "general_chat")
    if intent == "knowledge_search":
        return "rag"
    if intent == "business_operation":
        return "tool_executor"
    return "synthesizer"


def build_workflow() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("intent_router", intent_router_node)
    graph.add_node("planner", planner_node)
    graph.add_node("rag", rag_node)
    graph.add_node("tool_executor", tool_executor_node)
    graph.add_node("human_review", human_review_node)
    graph.add_node("synthesizer", synthesizer_node)

    graph.add_edge(START, "intent_router")
    graph.add_conditional_edges(
        "intent_router",
        _route_intent,
        {
            "rag": "planner",
            "tool_executor": "planner",
            "synthesizer": "planner",
        },
    )
    graph.add_conditional_edges(
        "planner",
        lambda state: (
            "rag"
            if state.get("intent") == "knowledge_search"
            else "tool_executor"
            if state.get("intent") == "business_operation"
            else "synthesizer"
        ),
        {
            "rag": "rag",
            "tool_executor": "tool_executor",
            "synthesizer": "synthesizer",
        },
    )
    graph.add_edge("rag", "synthesizer")
    graph.add_edge("tool_executor", "human_review")
    graph.add_edge("human_review", "synthesizer")
    graph.add_edge("synthesizer", END)

    return graph


def compile_workflow():
    graph = build_workflow()
    return graph.compile()
