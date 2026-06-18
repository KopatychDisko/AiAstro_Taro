---
phase: 05-graph-schema-cleanup
status: complete
---

# Phase 5: Graph & Schema Cleanup — Complete

## ARCH-03 — Unified routing

- Removed duplicate `astro_node → add_memory` unconditional edge
- Agent nodes route via `tools_condition` only; router uses `route_from_router`
- `next_node` on agent outputs kept for frontend status display only

## ARCH-04 — AgentState next_node

- `next_node` made `Optional` in `AgentState` (display + router routing)

## ARCH-05 — Dataclass Agents

- `Agents` converted from Pydantic `BaseModel` to `@dataclass`

## ARCH-06 — Shared TaroCard

- `src/backend/models.py` — single `TaroCard` definition
- Imported by `schemas.py`, `graph/agents/schemas.py`, `taro_card_mapping.py`

## Tests

`pytest -q` → 11 passed (pre phase 6 additions)
