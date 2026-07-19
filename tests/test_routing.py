"""Graph routing cap tests."""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage

from agents.routing import MAX_TOOL_ITERATIONS, capped_tools_condition


def test_capped_tools_condition_ends_when_limit_reached() -> None:
    state = {
        "messages": [
            HumanMessage(content="draw cards"),
            AIMessage(
                content="",
                tool_calls=[{"id": "1", "name": "draw", "args": {}}],
            ),
        ],
        "tool_iterations": MAX_TOOL_ITERATIONS,
    }

    assert capped_tools_condition(state) == "__end__"
