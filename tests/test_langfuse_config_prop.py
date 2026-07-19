"""Wave 0: Langfuse config propagation into agent ainvoke (mocked, no live cloud)."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from agents.astro.node import create_astro_node
from agents.router.node import create_router_node
from agents.taro.node import create_taro_node
from server.observability import build_langfuse_callbacks, langfuse_run_metadata
from tests.conftest import make_mock_agents, make_mock_zep, make_router_output


class _FakeLangfuseHandler(BaseCallbackHandler):
    """Minimal callback handler so LangGraph astream accepts callbacks."""


def _tracing_config(session_id: str, user_name: str) -> RunnableConfig:
    return RunnableConfig(
        configurable={"thread_id": session_id},
        callbacks=[_FakeLangfuseHandler()],
        metadata=langfuse_run_metadata(session_id, user_name),
    )


def _assert_ainvoke_received_config(agent: AsyncMock, config: RunnableConfig) -> None:
    assert agent.ainvoke.await_count == 1
    call_kwargs = agent.ainvoke.await_args.kwargs
    assert "config" in call_kwargs
    received = call_kwargs["config"]
    assert received is config
    assert received.get("callbacks") == config.get("callbacks")
    metadata = received.get("metadata")
    assert metadata is not None
    assert metadata["langfuse_session_id"] == config["metadata"]["langfuse_session_id"]
    assert metadata["langfuse_user_id"] == config["metadata"]["langfuse_user_id"]
    assert "stream" in metadata["langfuse_tags"]


def test_callbacks_empty_without_langfuse_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)

    assert build_langfuse_callbacks("user-1", "Test") == []


@pytest.mark.asyncio
async def test_router_ainvoke_receives_langfuse_config() -> None:
    agents = make_mock_agents(make_router_output(next_node="taro_node"))
    config = _tracing_config("user-1", "Alice")
    node = create_router_node(agents)

    await node(
        {
            "messages": [HumanMessage(content="hello")],
            "context": "User name: Alice",
        },
        config,
    )

    _assert_ainvoke_received_config(agents.router_agent, config)


@pytest.mark.asyncio
async def test_taro_ainvoke_receives_langfuse_config() -> None:
    agents = make_mock_agents(make_router_output(next_node="taro_node"))
    config = _tracing_config("user-1", "Alice")
    node = create_taro_node(agents)

    await node(
        {
            "messages": [HumanMessage(content="hello")],
            "context": "User name: Alice",
        },
        config,
    )

    _assert_ainvoke_received_config(agents.taro_agent, config)


@pytest.mark.asyncio
async def test_astro_ainvoke_receives_langfuse_config() -> None:
    agents = make_mock_agents(make_router_output(next_node="astro_node"))
    config = _tracing_config("user-1", "Alice")
    node = create_astro_node(agents)

    await node(
        {
            "messages": [HumanMessage(content="hello")],
            "context": "User name: Alice",
            "birth_day": "1990-01-01",
            "time_birth": "12:00",
            "city": "Paris",
            "country": "France",
        },
        config,
    )

    _assert_ainvoke_received_config(agents.astro_agent, config)


@pytest.mark.asyncio
async def test_summarize_ainvoke_receives_config_via_add_memory() -> None:
    router_output = make_router_output(next_node="add_memory", message="direct reply")
    mock_agents = make_mock_agents(router_output)
    mock_zep = make_mock_zep()
    config = _tracing_config("user-1", "Alice")

    with (
        patch("agents.workflow.create_agents", AsyncMock(return_value=mock_agents)),
        patch("agents.workflow.AsyncZep", return_value=mock_zep),
    ):
        from agents.workflow import setup_workflow

        compiled = await setup_workflow()
        graph_input = {
            "messages": [HumanMessage(content="hi")],
            "name": "Alice",
            "birth_day": "1990-01-01",
            "time_birth": "12:00",
            "city": "Paris",
            "country": "France",
            "next_node": "router_node",
        }

        async for _update in compiled.astream(
            graph_input,
            config=config,
            stream_mode="updates",
        ):
            pass

    assert mock_agents.summarize_agent.ainvoke.await_count == 1
    call_kwargs = mock_agents.summarize_agent.ainvoke.await_args.kwargs
    assert "config" in call_kwargs
    received = call_kwargs["config"]
    assert received.get("callbacks") is not None
    metadata = received.get("metadata")
    assert metadata is not None
    assert metadata["langfuse_session_id"] == "user-1"
    assert metadata["langfuse_user_id"] == "user-1"
    assert "stream" in metadata["langfuse_tags"]
    assert metadata["user_name"] == "Alice"
