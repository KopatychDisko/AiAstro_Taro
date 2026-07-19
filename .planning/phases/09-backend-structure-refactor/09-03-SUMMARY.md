---
phase: 09-backend-structure-refactor
plan: 03
subsystem: api
tags: [agents, memory, zep, factories, create_agents, cards]

requires:
  - phase: 09-backend-structure-refactor
    provides: agents.router/taro/astro factories, agents.state.Agents, agents.config zep_api
provides:
  - agents.memory.tools search_facts/search_nodes
  - agents.memory.factory.create_summarize_agent
  - agents.cards.factory.create_card_unlock_agent
  - agents.factories.create_agents aggregator
affects:
  - 09-04 workflow assembly
  - 09-06 legacy deletion

tech-stack:
  added: []
  patterns:
    - "Thin create_agents aggregator calls per-agent factories and returns Agents"
    - "Module-level AsyncZep client in agents.memory.tools (not workflow AsyncZep)"

key-files:
  created:
    - src/backend/agents/memory/__init__.py
    - src/backend/agents/memory/tools.py
    - src/backend/agents/memory/prompt.py
    - src/backend/agents/memory/factory.py
    - src/backend/agents/cards/prompt.py
    - src/backend/agents/cards/factory.py
    - src/backend/agents/factories.py
  modified:
    - src/backend/agents/taro/factory.py
    - src/backend/agents/astro/factory.py

key-decisions:
  - "Promote taro/astro memory-tool imports to module level once agents.memory.tools exists"
  - "Keep unlock_card_agent in create_agents for Agents shape / mocks"

patterns-established:
  - "agents.factories.create_agents is the single aggregator for workflow Plan 04"
  - "Memory Zep tools live under agents.memory; workflow AsyncZep stays for Plan 04"

requirements-completed: [SC-03]

duration: 1min
completed: 2026-07-19
---

# Phase 09 Plan 03: Memory Tools and create_agents Summary

**Memory Zep tools + summarize/card-unlock factories under agents/, with thin `create_agents` aggregator preserving Agents dataclass shape**

## Performance

- **Duration:** 1 min
- **Started:** 2026-07-19T21:09:28Z
- **Completed:** 2026-07-19T21:10:13Z
- **Tasks:** 2
- **Files modified:** 9 (7 created, 2 modified)

## Accomplishments

- Moved Zep `search_facts`/`search_nodes` and module-level `zep` into `agents.memory.tools`
- Added summarize prompt + `create_summarize_agent` under `agents.memory`
- Added unlock-card prompt + `create_card_unlock_agent` under `agents.cards` (keeps Agents shape)
- Added `agents.factories.create_agents` thin async aggregator for Plan 04
- Legacy `graph/agents` left untouched; pytest green (13 passed)

## Task Commits

Each task was committed atomically:

1. **Task 1: Memory tools and summarize factory** - `5d366a0` (feat)
2. **Task 2: Cards unlock factory and create_agents aggregator** - `ec92e91` (feat)

**Plan metadata:** (pending docs commit)

## Files Created/Modified

- `src/backend/agents/memory/__init__.py` - Package marker
- `src/backend/agents/memory/tools.py` - Zep search tools + module-level client
- `src/backend/agents/memory/prompt.py` - Summarize prompt
- `src/backend/agents/memory/factory.py` - `create_summarize_agent`
- `src/backend/agents/cards/prompt.py` - Unlock-card prompt
- `src/backend/agents/cards/factory.py` - `create_card_unlock_agent`
- `src/backend/agents/factories.py` - Thin `create_agents` aggregator
- `src/backend/agents/taro/factory.py` - Module-level memory tools import
- `src/backend/agents/astro/factory.py` - Module-level memory tools import

## Decisions Made

- Promoted Plan 02 lazy imports of `search_facts`/`search_nodes` to module-level once `agents.memory.tools` landed
- Kept `unlock_card_agent` in aggregator even if unused in graph (Agents field + mocks)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Promote taro/astro memory-tool imports to module level**
- **Found during:** Task 1 (Memory tools and summarize factory)
- **Issue:** Plan 02 used lazy imports so factories imported before memory tools existed; leaving them lazy after tools land hides the dependency
- **Fix:** Module-level `from agents.memory.tools import search_facts, search_nodes` in taro/astro factories
- **Files modified:** `src/backend/agents/taro/factory.py`, `src/backend/agents/astro/factory.py`
- **Verification:** Memory + factory imports succeed; pytest 13 passed after Task 2
- **Committed in:** `5d366a0` (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (Rule 2)
**Impact on plan:** Minimal; completes Plan 02 follow-up once memory.tools exists. No scope creep.

## Issues Encountered

- Used `.venv/bin/python` for verifies (same as Plan 01/02 note on `uv sync` / `psycopg2`)

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 04 can wire workflow against `agents.factories.create_agents`
- Do not delete legacy `graph/agents` until Plan 06; no server package yet

## Self-Check: PASSED

- FOUND: all 7 planned artifacts
- FOUND: commits `5d366a0`, `ec92e91` (via `git cat-file`)

---
*Phase: 09-backend-structure-refactor*
*Completed: 2026-07-19*
