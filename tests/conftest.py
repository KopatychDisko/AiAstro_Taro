"""Shared test fixtures for backend graph and API tests."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from graph.agents.schemas import Agents, RouterOutput, Summarize


def make_mock_zep() -> MagicMock:
    mock_zep = MagicMock()
    mock_zep.thread.get_user_context = AsyncMock(
        return_value=SimpleNamespace(context="prior context"),
    )
    mock_zep.thread.add_messages = AsyncMock()
    mock_zep.graph.search = AsyncMock(return_value=[])
    return mock_zep


@pytest.fixture
def runnable_config() -> dict:
    return {"configurable": {"thread_id": "test-user-1"}}


@pytest.fixture
def base_router_state() -> dict:
    return {
        "messages": [HumanMessage(content="hello")],
        "context": "User name: Test\n Context: none",
        "name": "Test",
    }


def make_router_output(next_node: str, message: str | None = None) -> RouterOutput:
    return RouterOutput(next_node=next_node, message=message)


def make_mock_agents(router_output: RouterOutput) -> Agents:
    router_agent = AsyncMock()
    router_agent.ainvoke.return_value = router_output

    taro_agent = AsyncMock()
    taro_agent.ainvoke.return_value = AIMessage(content="taro reply")

    astro_agent = AsyncMock()
    astro_agent.ainvoke.return_value = AIMessage(content="astro reply")

    summarize_agent = AsyncMock()
    summarize_agent.ainvoke.return_value = Summarize(
        user_message="hello",
        message_to_user="reply",
    )

    return Agents(
        taro_agent=taro_agent,
        taro_tool=MagicMock(),
        astro_agent=astro_agent,
        astro_tool=MagicMock(),
        router_agent=router_agent,
        unlock_card_agent=MagicMock(),
        summarize_agent=summarize_agent,
    )
