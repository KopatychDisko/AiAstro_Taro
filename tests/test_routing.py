"""Graph routing cap tests."""

from __future__ import annotations

import logging

from langchain_core.messages import AIMessage, HumanMessage

from agents.routing import MAX_TOOL_ITERATIONS, capped_tools_condition


def test_capped_tools_condition_ends_when_limit_reached(
    caplog: logging.LogCaptureFixture,
) -> None:
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

    with caplog.at_level(logging.WARNING, logger="agents.routing"):
        assert capped_tools_condition(state) == "__end__"

    assert "tool_iteration_cap_reached" in caplog.text
    matching = [
        record
        for record in caplog.records
        if record.getMessage() == "tool_iteration_cap_reached"
    ]
    assert len(matching) == 1
    assert matching[0].tool_iterations == MAX_TOOL_ITERATIONS
    assert matching[0].max_tool_iterations == MAX_TOOL_ITERATIONS


def test_capped_tools_condition_below_cap_delegates_to_tools() -> None:
    state = {
        "messages": [
            HumanMessage(content="draw cards"),
            AIMessage(
                content="",
                tool_calls=[{"id": "1", "name": "draw", "args": {}}],
            ),
        ],
        "tool_iterations": MAX_TOOL_ITERATIONS - 1,
    }

    assert capped_tools_condition(state) == "tools"


def test_max_tool_iterations_is_three() -> None:
    assert MAX_TOOL_ITERATIONS == 3
