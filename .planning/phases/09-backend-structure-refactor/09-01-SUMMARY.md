---
phase: 09-backend-structure-refactor
plan: 01
subsystem: api
tags: [agents, langgraph, pydantic, packaging, refactor]

requires:
  - phase: 05-graph-schema-cleanup
    provides: TaroCard, AgentState, routing, card mapping under flat/graph layout
provides:
  - agents.models.TaroCard
  - agents.state AgentState/Agents/router schemas
  - agents.routing capped_tools_condition
  - agents.config base_url/zep_api
  - agents.cards.mapping extract_cards_from_messages
affects:
  - 09-02 per-agent factories
  - 09-03 workflow assembly
  - 09-05 server package
  - 09-06 legacy deletion

tech-stack:
  added: []
  patterns:
    - "agents/ package mirrors shared graph foundation; legacy graph/ untouched until Plan 06"
    - "PYTHONPATH=src/backend imports as agents.*"

key-files:
  created:
    - src/backend/agents/__init__.py
    - src/backend/agents/models.py
    - src/backend/agents/state.py
    - src/backend/agents/routing.py
    - src/backend/agents/config/__init__.py
    - src/backend/agents/config/config.py
    - src/backend/agents/cards/__init__.py
    - src/backend/agents/cards/mapping.py
  modified: []

key-decisions:
  - "Import TaroCard via agents.models (absolute under pythonpath) in state and cards.mapping"
  - "Empty package __init__.py files for agents/ and agents/cards/ for explicit packages"

patterns-established:
  - "Behavior-identical copy into agents/; do not delete legacy until Plan 06 (D-04 hard cut later)"
  - "No HTTP under agents/ (D-02)"

requirements-completed: [SC-02]

duration: 2min
completed: 2026-07-19
---

# Phase 09 Plan 01: Agents Shared Foundation Summary

**Shared agents foundation under `agents/` — TaroCard, AgentState, routing caps, config, and MCP card mapping — with no HTTP and legacy graph untouched**

## Performance

- **Duration:** 2 min
- **Started:** 2026-07-19T21:01:56Z
- **Completed:** 2026-07-19T21:03:26Z
- **Tasks:** 2
- **Files modified:** 8 created

## Accomplishments

- Created `agents.models.TaroCard` behavior-identical to root `models.TaroCard`
- Relocated graph schemas/routing/config into `agents.state`, `agents.routing`, `agents.config`
- Added `agents.cards.mapping.extract_cards_from_messages` importing from `agents.models`
- Verified foundation imports via `PYTHONPATH=src/backend`; legacy `pytest -q` still green (13 passed)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create agents models, state, routing, config** - `a93e4c2` (feat)
2. **Task 2: Create cards mapping module** - `008c7cf` (feat)

**Plan metadata:** `7bf6ff5` (docs: complete plan)

## Files Created/Modified

- `src/backend/agents/__init__.py` - Package marker
- `src/backend/agents/models.py` - TaroCard domain model
- `src/backend/agents/state.py` - AgentState, Agents, RouterOutput, UnlockCard, Summarize
- `src/backend/agents/routing.py` - MAX_TOOL_ITERATIONS, capped_tools_condition
- `src/backend/agents/config/config.py` - base_url, zep_api, env wiring
- `src/backend/agents/config/__init__.py` - Exports base_url, zep_api
- `src/backend/agents/cards/__init__.py` - Thin package marker
- `src/backend/agents/cards/mapping.py` - MCP ToolMessage → TaroCard mapping

## Decisions Made

- Used `from agents.models import TaroCard` (absolute under pythonpath) in state and cards.mapping for consistency with plan contract
- Added empty `agents/__init__.py` and `cards/__init__.py` so packages are explicit (plan listed cards/__init__; agents/__init__ added for the same reason)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Added `agents/__init__.py`**
- **Found during:** Task 1 (Create agents models, state, routing, config)
- **Issue:** Plan file list omitted package `__init__.py` at `agents/` root; without it some import modes are fragile
- **Fix:** Created empty `src/backend/agents/__init__.py`
- **Files modified:** `src/backend/agents/__init__.py`
- **Verification:** `from agents.models import TaroCard` succeeds
- **Committed in:** `a93e4c2` (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (Rule 2)
**Impact on plan:** Minimal; enables clean package imports without scope creep.

## Issues Encountered

- `uv run python` fails building `psycopg2` without `pg_config` — used existing `.venv/bin/python` for verifies (noted in STATE.md)

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 02 can build per-agent factories on `agents.state` / `agents.config`
- Legacy `graph/` and flat `models.py` remain until Plan 06

## Self-Check: PASSED

- FOUND: all 7 planned artifacts (+ agents/__init__.py)
- FOUND: commits `a93e4c2`, `008c7cf`

---
*Phase: 09-backend-structure-refactor*
*Completed: 2026-07-19*
