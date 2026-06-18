"""LangGraph routing helpers."""

from __future__ import annotations

from langgraph.prebuilt import tools_condition

MAX_TOOL_ITERATIONS = 3


def capped_tools_condition(state: dict) -> str:
    if state.get("tool_iterations", 0) >= MAX_TOOL_ITERATIONS:
        return "__end__"
    return tools_condition(state)
