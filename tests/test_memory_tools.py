"""Zep memory tool tests with mocked graph search."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from langchain_core.runnables import RunnableConfig

from agents.memory.tools import search_facts, search_nodes


@pytest.mark.asyncio
async def test_search_facts_returns_facts_with_limit(runnable_config: dict) -> None:
    mock_edges = [
        SimpleNamespace(fact="User likes tarot"),
        SimpleNamespace(fact="User lives in Paris"),
    ]

    with patch(
        "agents.memory.tools.zep.graph.search",
        AsyncMock(return_value=mock_edges),
    ) as mock_search:
        facts = await search_facts.ainvoke(
            {"query": "tarot", "limit": 2},
            config=RunnableConfig(**runnable_config),
        )

    mock_search.assert_awaited_once()
    call_kwargs = mock_search.await_args.kwargs
    assert call_kwargs["limit"] == 2
    assert call_kwargs["search_scope"] == "edges"
    assert facts == ["User likes tarot", "User lives in Paris"]


@pytest.mark.asyncio
async def test_search_nodes_returns_summaries_with_limit(runnable_config: dict) -> None:
    mock_nodes = [
        SimpleNamespace(summary="Tarot session"),
        SimpleNamespace(summary="Birth chart"),
        SimpleNamespace(summary="Extra node"),
    ]

    with patch(
        "agents.memory.tools.zep.graph.search",
        AsyncMock(return_value=mock_nodes),
    ) as mock_search:
        nodes = await search_nodes.ainvoke(
            {"query": "astrology", "limit": 3},
            config=RunnableConfig(**runnable_config),
        )

    mock_search.assert_awaited_once()
    call_kwargs = mock_search.await_args.kwargs
    assert call_kwargs["limit"] == 3
    assert call_kwargs["search_scope"] == "nodes"
    assert nodes == ["Tarot session", "Birth chart", "Extra node"]
