"""Wave 0: unlock surface gone; title field is spread_name from MCP mapping."""

from __future__ import annotations

import importlib
from dataclasses import fields

import pytest
from langchain_core.messages import ToolMessage

from agents.state import Agents
from server.schemas import ExtractData

from tests.test_taro_cards import SAMPLE_MCP_READING


def test_unlock_card_model_removed() -> None:
    state_mod = importlib.import_module("agents.state")
    assert not hasattr(state_mod, "UnlockCard")


def test_agents_dataclass_has_no_unlock_card_agent() -> None:
    field_names = {f.name for f in fields(Agents)}
    assert "unlock_card_agent" not in field_names
    assert field_names == {
        "taro_agent",
        "taro_tool",
        "astro_agent",
        "astro_tool",
        "router_agent",
        "summarize_agent",
    }


def test_card_unlock_factory_module_deleted() -> None:
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("agents.cards.factory")


def test_extract_data_uses_spread_name() -> None:
    model_fields = ExtractData.model_fields
    assert "spread_name" in model_fields
    assert "unlock_name" not in model_fields
    payload = ExtractData(spread_name="Three Card")
    assert payload.model_dump()["spread_name"] == "Three Card"


@pytest.mark.asyncio
async def test_img_node_returns_spread_name() -> None:
    from agents.cards.node import img_node

    result = await img_node(
        {"messages": [ToolMessage(content=SAMPLE_MCP_READING, tool_call_id="call-1")]}
    )
    assert "spread_name" in result
    assert "unlock_name" not in result
    assert result["spread_name"] == "Three Card"
    assert result["next_node"] == "add_memory"
    assert len(result["taro_cards"]) == 3
