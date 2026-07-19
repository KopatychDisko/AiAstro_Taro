---
phase: 09-backend-structure-refactor
plan: 04
subsystem: api
tags: [agents, workflow, langgraph, setup_workflow, AsyncZep, nodes]

requires:
  - phase: 09-backend-structure-refactor
    provides: agents.factories.create_agents, agents.cards.mapping, agents.routing, AgentState
provides:
  - agents.setup_workflow / agents.workflow.setup_workflow
  - per-agent node modules (router/taro/astro/cards)
  - patch sites agents.workflow.create_agents and agents.workflow.AsyncZep
affects:
  - 09-05 server package import
  - 09-06 hard-cut tests and legacy deletion

tech-stack:
  added: []
  patterns:
    - "Agent nodes as create_*_node(agents) factories returning closures"
    - "AsyncZep constructed inside agents.workflow.setup_workflow; take_context/add_memory nested closures"
    - "Thin agents/__init__ exports only setup_workflow"

key-files:
  created:
    - src/backend/agents/router/node.py
    - src/backend/agents/taro/node.py
    - src/backend/agents/astro/node.py
    - src/backend/agents/cards/node.py
    - src/backend/agents/workflow.py
  modified:
    - src/backend/agents/__init__.py

key-decisions:
  - "Per-agent nodes use create_*_node(agents) factories so LangGraph callables close over Agents like legacy nested defs"
  - "img_node stays a plain async function (no Agents dependency); route_from_router exported from router.node"

patterns-established:
  - "from agents import setup_workflow is the public compile entry for server Plan 05"
  - "Plan 06 patches agents.workflow.create_agents and agents.workflow.AsyncZep"

requirements-completed: [SC-02, SC-03]

duration: 1min
completed: 2026-07-19
---

# Phase 09 Plan 04: Workflow and Node Wiring Summary

**Per-agent LangGraph nodes under agents/ plus `setup_workflow` with local AsyncZep construction and thin public export**

## Performance

- **Duration:** 1 min
- **Started:** 2026-07-19T21:11:16Z
- **Completed:** 2026-07-19T21:12:33Z
- **Tasks:** 2
- **Files modified:** 6 (5 created, 1 modified)

## Accomplishments

- Extracted router/taro/astro/img node callables into per-agent `node.py` modules (SC-03)
- Rebuilt `agents.workflow.setup_workflow` with same graph edges/names as legacy `graph/nodes.py`
- Locked AsyncZep construction and take_context/add_memory closures in workflow for Plan 06 patch sites
- Thin `agents/__init__.py` exports only `setup_workflow` (SC-02); legacy `graph/` untouched

## Task Commits

Each task was committed atomically:

1. **Task 1: Per-agent node modules** - `0bc28e0` (feat)
2. **Task 2: workflow setup_workflow and public export** - `c1676e0` (feat)

**Plan metadata:** (pending docs commit)

## Files Created/Modified

- `src/backend/agents/router/node.py` - `create_router_node` + `route_from_router`
- `src/backend/agents/taro/node.py` - `create_taro_node`
- `src/backend/agents/astro/node.py` - `create_astro_node`
- `src/backend/agents/cards/node.py` - `img_node` via `agents.cards.mapping`
- `src/backend/agents/workflow.py` - `setup_workflow` graph compile + AsyncZep
- `src/backend/agents/__init__.py` - public `setup_workflow` re-export

## Decisions Made

- Used `create_*_node(agents)` factories for agent-bound nodes so callables stay LangGraph-compatible closures
- Left `img_node` as a module-level async function (no Agents close-over)
- Kept AsyncZep import/construction in `agents.workflow` per RESEARCH Open Question 1

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- Used `.venv/bin/python` for verifies (same as Plans 01–03)

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 05 can `from agents import setup_workflow` in server.app
- Plan 06 can rewrite patches to `agents.workflow.create_agents` / `agents.workflow.AsyncZep`
- Do not delete legacy `graph/` until Plan 06

## Self-Check: PASSED

- FOUND: all 6 planned artifacts
- FOUND: commits `0bc28e0`, `c1676e0` (via `git cat-file`)

---
*Phase: 09-backend-structure-refactor*
*Completed: 2026-07-19*
