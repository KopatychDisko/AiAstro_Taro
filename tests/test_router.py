"""Router intent tests with mocked LLM structured output."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from tests.conftest import make_mock_agents, make_mock_zep, make_router_output


def _minimal_graph_input() -> dict:
    return {
        "messages": [HumanMessage(content="hello")],
        "name": "Test",
        "birth_day": "1990-01-01",
        "time_birth": "12:00",
        "city": "Paris",
        "country": "France",
        "next_node": "router_node",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("next_node", "message"),
    [
        ("taro_node", None),
        ("astro_node", None),
        ("add_memory", "General chat reply"),
    ],
)
async def test_router_node_next_node_for_intents(
    next_node: str,
    message: str | None,
) -> None:
    router_output = make_router_output(next_node=next_node, message=message)
    mock_agents = make_mock_agents(router_output)
    mock_zep = make_mock_zep()

    with (
        patch("agents.workflow.create_agents", AsyncMock(return_value=mock_agents)),
        patch("agents.workflow.AsyncZep", return_value=mock_zep),
    ):
        from agents.workflow import setup_workflow

        compiled = await setup_workflow()
        config = RunnableConfig(configurable={"thread_id": "test-user-1"})
        router_update: dict | None = None

        async for update in compiled.astream(
            _minimal_graph_input(),
            config=config,
            stream_mode="updates",
        ):
            if "router_node" in update:
                router_update = update["router_node"]
                break

    assert router_update is not None
    assert router_update["next_node"] == next_node
    if next_node == "add_memory":
        assert router_update["message_to_user"] == message
