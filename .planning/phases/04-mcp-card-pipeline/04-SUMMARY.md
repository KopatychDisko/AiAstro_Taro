---
phase: 04-mcp-card-pipeline
status: complete
---

# Phase 4: MCP Card Pipeline — Complete

## ARCH-01 — Cards from MCP ToolMessage

- Added `src/backend/graph/taro_card_mapping.py`
- `extract_cards_from_messages()` reads latest `ToolMessage` content from graph state
- `parse_mcp_reading_text()` parses MCP markdown (`**Card** (upright|reversed)`) deterministically
- `normalize_spread_name()` maps MCP spread titles to frontend layout keys (e.g. `Three Card Spread` → `Three Card`)

## ARCH-02 — img_node without LLM

- `img_node` no longer calls `img_agent` / LLM structured output
- Removed `create_img_agent()` and `img_agent` from `Agents` container
- Removed unused `ImgOutput` schema

## Tests

- `tests/test_taro_cards.py` — markdown parsing + ToolMessage extraction (3 tests)
- Full suite: `pytest -q` → 11 passed

## Artifacts

- `graph.taro_card_mapping.extract_cards_from_messages`
- `graph.taro_card_mapping.parse_mcp_reading_text`
- `graph.taro_card_mapping.parse_mcp_tool_payload`
