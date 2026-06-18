"""Card mapping tests — MCP ToolMessage output to TaroCard models."""

from __future__ import annotations

from langchain_core.messages import ToolMessage

from models import TaroCard
from graph.taro_card_mapping import (
    extract_cards_from_messages,
    parse_mcp_reading_text,
    parse_mcp_tool_payload,
)

SAMPLE_MCP_READING = """# Three Card Spread Reading

**Question:** Will this work?
**Date:** 6/17/2026, 12:00:00 PM
**Reading ID:** reading_123

*A versatile three-card spread*

## Your Cards

### 1. Past/Situation
*What has led to this situation*

**The Fool** (upright)

*Keywords: beginnings, innocence*

### 2. Present/Action
*The current state*

**The Magician** (reversed)

*Keywords: trickery*

### 3. Future/Outcome
*What may come*

**Death** (upright)

## Interpretation

Sample interpretation text.
"""


def test_maps_mcp_tool_result_to_taro_cards() -> None:
    mcp_payload = [
        {"name": "thefool", "reversed": False},
        {"name": "themagician", "reversed": True},
    ]

    cards = parse_mcp_tool_payload(mcp_payload)

    assert len(cards) == 2
    assert all(isinstance(card, TaroCard) for card in cards)
    assert cards[0].name == "thefool"
    assert cards[0].reversed is False
    assert cards[1].name == "themagician"
    assert cards[1].reversed is True


def test_parse_mcp_reading_markdown_without_llm() -> None:
    cards, spread_name = parse_mcp_reading_text(SAMPLE_MCP_READING)

    assert spread_name == "Three Card"
    assert len(cards) == 3
    assert cards[0].name == "thefool"
    assert cards[0].reversed is False
    assert cards[1].name == "themagician"
    assert cards[1].reversed is True
    assert cards[2].name == "death"
    assert cards[2].reversed is False


def test_extract_cards_from_tool_message_history() -> None:
    messages = [
        ToolMessage(content=SAMPLE_MCP_READING, tool_call_id="call-1"),
    ]

    cards, spread_name = extract_cards_from_messages(messages)

    assert spread_name == "Three Card"
    assert len(cards) == 3
    assert cards[1].reversed is True
