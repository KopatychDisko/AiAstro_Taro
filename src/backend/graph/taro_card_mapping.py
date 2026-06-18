"""Map tarot MCP ToolMessage output to TaroCard models without LLM involvement."""

from __future__ import annotations

import json
import re
from typing import List

from langchain_core.messages import BaseMessage, ToolMessage

from models import TaroCard

CARD_LINE_PATTERN = re.compile(
    r"\*\*(.+?)\*\*\s*\((upright|reversed)\)",
    re.IGNORECASE,
)
SPREAD_HEADER_PATTERN = re.compile(
    r"^#\s+(.+?)\s+Reading\s*$",
    re.MULTILINE,
)

MCP_SPREAD_TO_FRONTEND: dict[str, str] = {
    "Single Card": "Single Card",
    "Three Card Spread": "Three Card",
    "Celtic Cross": "Celtic Cross",
    "Horseshoe Spread": "Horseshoe",
    "Relationship Cross": "Relationship Cross",
    "Career Path Spread": "Career Path",
    "Decision Making Spread": "Decision Making",
    "Year Ahead Spread": "Year Ahead",
    "Spiritual Guidance Spread": "Spiritual Guidance",
    "Chakra Alignment Spread": "Chakra Alignment",
    "Shadow Work Spread": "Shadow Work",
}

FRONTEND_SPREAD_NAMES: frozenset[str] = frozenset(MCP_SPREAD_TO_FRONTEND.values())


def normalize_card_name(name: str) -> str:
    return "".join(character.lower() for character in name if character.isalnum())


def normalize_spread_name(mcp_spread_name: str) -> str:
    trimmed = mcp_spread_name.strip()
    if trimmed in MCP_SPREAD_TO_FRONTEND:
        return MCP_SPREAD_TO_FRONTEND[trimmed]
    if trimmed in FRONTEND_SPREAD_NAMES:
        return trimmed
    raise ValueError(
        f"Unsupported tarot spread for frontend layout: {trimmed!r}. "
        f"Known MCP spreads: {sorted(MCP_SPREAD_TO_FRONTEND.keys())}"
    )


def _tool_message_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return str(content)


def parse_mcp_reading_text(text: str) -> tuple[List[TaroCard], str]:
    spread_header = SPREAD_HEADER_PATTERN.search(text)
    if spread_header is None:
        raise ValueError("MCP reading text missing spread header (# <Name> Reading)")

    spread_name = normalize_spread_name(spread_header.group(1))

    cards: List[TaroCard] = []
    for match in CARD_LINE_PATTERN.finditer(text):
        cards.append(
            TaroCard(
                name=normalize_card_name(match.group(1)),
                reversed=match.group(2).lower() == "reversed",
            )
        )

    if not cards:
        raise ValueError("MCP reading text contains no card lines (**Name** (upright|reversed))")

    return cards, spread_name


def parse_mcp_tool_payload(payload: list[dict[str, object]]) -> List[TaroCard]:
    return [
        TaroCard(name=str(item["name"]), reversed=bool(item["reversed"]))
        for item in payload
    ]


def extract_cards_from_messages(messages: list[BaseMessage]) -> tuple[List[TaroCard], str]:
    tool_texts: list[str] = []
    for message in reversed(messages):
        if isinstance(message, ToolMessage):
            tool_texts.append(_tool_message_text(message.content))

    for text in tool_texts:
        lower = text.lower()
        if "**" in text and ("(upright)" in lower or "(reversed)" in lower):
            return parse_mcp_reading_text(text)

    for text in tool_texts:
        stripped = text.strip()
        if not stripped.startswith("["):
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, list) and payload:
            cards = parse_mcp_tool_payload(payload)
            return cards, "Three Card"

    raise ValueError("No tarot MCP ToolMessage with card data found in message history")
