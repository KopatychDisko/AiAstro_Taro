---
phase: 11-agent-harness-hardening
plan: 02
subsystem: agents
tags: [unlock, spread_name, mcp-mapping, cleanup, pytest]

requires:
  - phase: 11-agent-harness-hardening
    provides: Langfuse v4 wiring landed (11-01); shared tree ready for unlock cleanup
provides:
  - Unlock LLM surface hard-deleted (factory, prompt, UnlockCard, unlock_card_agent)
  - spread_name end-to-end from MCP mapping → AgentState → ExtractData → Streamlit UI
  - Wave 0 schema/node contract tests (SC-11.1)
affects: [11-03-trust-budgets, 11-04-deepeval]

tech-stack:
  added: []
  patterns:
    - "UI title from extract_cards_from_messages spread_name (no unlock LLM)"
    - "Clean cut rename unlock_name → spread_name (no dual-field compat)"

key-files:
  created:
    - tests/test_spread_name_schema.py
  modified:
    - src/backend/agents/state.py
    - src/backend/agents/factories.py
    - src/backend/agents/cards/node.py
    - src/backend/server/schemas.py
    - src/frontend/schema.py
    - src/frontend/pages/app.py
    - src/frontend/templates.py
    - tests/conftest.py
    - README.md
  deleted:
    - src/backend/agents/cards/factory.py
    - src/backend/agents/cards/prompt.py

key-decisions:
  - "Hard-delete unlock agent surface rather than wire it (D-01)"
  - "Rename unlock_name → spread_name end-to-end; no dual-write (D-02/D-03)"
  - "create_html_taro param renamed name → spread_name for clarity"

patterns-established:
  - "Pattern: MCP mapping is sole title source; img_node forwards spread_name"
  - "Pattern: Agents dataclass fields stay aligned with create_agents and make_mock_agents"

requirements-completed: [SC-11.1]

duration: 2min
completed: 2026-07-20
---

# Phase 11 Plan 02: Unlock Delete / spread_name E2E Summary

**Hard-deleted dead unlock LLM surface and renamed unlock_name → spread_name so the UI title comes from MCP spread/card mapping**

## Performance

- **Duration:** 2 min
- **Started:** 2026-07-19T23:30:37Z
- **Completed:** 2026-07-19T23:32:42Z
- **Tasks:** 2
- **Files modified:** 12 (including 2 deletions)

## Accomplishments

- Removed `UnlockCard`, `create_card_unlock_agent`, unlock prompt, and `unlock_card_agent` from `Agents` / factories / mocks
- Renamed state, API, and frontend title field to `spread_name`; `img_node` emits mapping output under that key
- Added Wave 0 `tests/test_spread_name_schema.py`; full `uv run pytest -q` green (62 passed)

## Task Commits

Each task was committed atomically (TDD RED → GREEN):

1. **Task 1: Delete unlock agent surface and rename state/API to spread_name**
   - `f36d2b3` (test) — failing backend unlock/spread_name contract tests
   - `ad55433` (feat) — delete unlock surface; backend/API spread_name
2. **Task 2: Frontend spread_name migration + Wave 0 schema tests**
   - `c3e275a` (test) — failing frontend spread_name / no-unlock_name tests
   - `c0d640a` (feat) — frontend schema/session/templates migration

**Plan metadata:** `495b253` (docs: complete plan)

## Files Created/Modified

- `tests/test_spread_name_schema.py` — Wave 0 unlock-gone + spread_name contract tests
- `src/backend/agents/state.py` — drop UnlockCard / unlock_card_agent; `spread_name` on AgentState
- `src/backend/agents/factories.py` — create_agents without unlock
- `src/backend/agents/cards/node.py` — emit `spread_name` from mapping
- `src/backend/agents/cards/factory.py` — deleted
- `src/backend/agents/cards/prompt.py` — deleted
- `src/backend/server/schemas.py` — ExtractData.spread_name
- `src/frontend/schema.py` — ExtractData.spread_name
- `src/frontend/pages/app.py` — session/message keys use spread_name
- `src/frontend/templates.py` — `create_html_taro(cards, spread_name)`
- `tests/conftest.py` — make_mock_agents aligned with Agents
- `README.md` — remove Unlock-card model row; document MCP title path

## Decisions Made

- Clean cut rename — no unlock_name/spread_name dual-field compat layer
- Kept `cards/mapping.py` behavior unchanged (already returns spread_name)
- Astro left in place (deferred remove-astro)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## User Setup Required

None - no new env keys or services.

## Next Phase Readiness

- SC-11.1 complete; Wave 3 (11-03 trust wrap + tool-cap logging) unblocked
- Grep gates clean under `src/` for unlock_card / UnlockCard / unlock_name

## Known Stubs

None

## Threat Flags

None — unlock LLM removal reduces attack surface (T-11-04 mitigate); spread_name remains display-only MCP metadata (T-11-03 accept)

## Self-Check: PASSED

- Artifacts present: factory/prompt deleted; `spread_name` in state/schemas/frontend; `11-02-SUMMARY.md`
- Commits present: `f36d2b3`, `ad55433`, `c3e275a`, `c0d640a`
- pytest: 62 passed

---
*Phase: 11-agent-harness-hardening*
*Completed: 2026-07-20*
