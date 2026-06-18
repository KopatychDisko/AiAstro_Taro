"""add_memory resilience when Zep persistence fails."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from tests.conftest import make_mock_agents, make_mock_zep, make_router_output


@pytest.mark.asyncio
async def test_add_memory_continues_when_zep_write_fails() -> None:
    router_output = make_router_output(next_node="add_memory", message="direct reply")
    mock_agents = make_mock_agents(router_output)
    mock_zep = make_mock_zep()
    mock_zep.thread.add_messages = AsyncMock(side_effect=RuntimeError("zep down"))

    with (
        patch("graph.nodes.create_agents", AsyncMock(return_value=mock_agents)),
        patch("graph.nodes.AsyncZep", return_value=mock_zep),
    ):
        from graph.nodes import setup_workflow

        compiled = await setup_workflow()
        config = RunnableConfig(configurable={"thread_id": "user-1"})

        graph_input = {
            "messages": [HumanMessage(content="hi")],
            "name": "Test",
            "birth_day": "1990-01-01",
            "time_birth": "12:00",
            "city": "Paris",
            "country": "France",
            "next_node": "router_node",
        }

        add_memory_update: dict | None = None
        async for update in compiled.astream(
            graph_input,
            config=config,
            stream_mode="updates",
        ):
            if "add_memory" in update:
                add_memory_update = update["add_memory"]
                break

    assert add_memory_update is not None
    assert add_memory_update["next_node"] == "END"
    mock_zep.thread.add_messages.assert_awaited_once()
