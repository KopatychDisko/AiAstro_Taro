"""LangGraph routing helpers."""

from __future__ import annotations

import logging

from langgraph.prebuilt import tools_condition

# Tool-loop budget for taro/astro ToolNode cycles; not env-configurable this phase.
MAX_TOOL_ITERATIONS = 3

logger = logging.getLogger(__name__)


def capped_tools_condition(state: dict) -> str:
    tool_iterations = state.get("tool_iterations", 0)
    if tool_iterations >= MAX_TOOL_ITERATIONS:
        logger.warning(
            "tool_iteration_cap_reached",
            extra={
                "tool_iterations": tool_iterations,
                "max_tool_iterations": MAX_TOOL_ITERATIONS,
            },
        )
        return "__end__"
    return tools_condition(state)
