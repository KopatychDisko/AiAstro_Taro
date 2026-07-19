---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: verifying
last_updated: "2026-07-19T21:45:45.819Z"
last_activity: 2026-07-19
progress:
  total_phases: 1
  completed_phases: 0
  total_plans: 7
  completed_plans: 6
  percent: 0
---

# Project State

**Milestone:** v1.0 — Brownfield Hardening  
**Status:** Phase complete — ready for verification
**Last updated:** 2026-07-19

## Current Position

Phase: 09-backend-structure-refactor
Plan: 6 of 6 in current phase
Status: Phase complete — ready for verification
Last activity: 2026-07-19

## Current Phase

Phase 9: Backend Structure Refactor — all 6 plans complete; ready for verification

## Completed

- Phase 1: Security (SEC-01–04)
- Phase 2: Bug Fixes (BUG-01–04)
- Phase 3: Test Foundation (TEST-01–06)
- Phase 4: MCP Card Pipeline (ARCH-01–02)
- Phase 5: Graph & Schema Cleanup (ARCH-03–06)
- Phase 6: Reliability (REL-01–04)
- Phase 7: Langfuse Observability (OBS-01–03)
- Phase 8: README & Documentation (DOC-01–03)
- Phase 9 Plan 01: Agents shared foundation (models, state, routing, config, cards mapping)
- Phase 9 Plan 02: Per-agent router/taro/astro packages (MCP ../../../ preserved)
- Phase 9 Plan 03: Memory/cards factories + create_agents aggregator
- Phase 9 Plan 04: Workflow nodes + setup_workflow public export
- Phase 9 Plan 05: Server package (app/auth/schemas/observability) + README uvicorn server.app:app
- Phase 9 Plan 06: Hard-cut tests to server.*/agents.*; delete legacy graph/flat modules; SC-04 green

## Blockers

None

## Notes

- Uses `psycopg2-binary` (no system `pg_config` required for `uv sync`).
- Tarot MCP requires `npm run build` in `src/tarotmcp` before live runs (copies `card-data.json` into `dist/`).
- Astro MCP deferred to v2 — backend starts without it.

## Accumulated Context

### Roadmap Evolution

- Phase 9 added: Backend structure refactor — split into agents and server packages; split graph into per-agent and subagent modules

### Decisions

- [Phase 09]: Import TaroCard via agents.models under PYTHONPATH=src/backend
- [Phase 09]: Empty package __init__.py for agents/ and agents/cards/
- [Phase 09]: Lazy-import memory tools in taro/astro factories until Plan 03
- [Phase 09]: Per-package create_prompt helper for router/taro/astro isolation
- [Phase 09]: Promote taro/astro memory-tool imports to module level once agents.memory.tools exists
- [Phase 09]: Keep unlock_card_agent in create_agents for Agents shape / mocks
- [Phase 09]: Per-agent nodes use create_*_node(agents) factories so LangGraph callables close over Agents like legacy nested defs
- [Phase 09]: img_node stays a plain async function (no Agents dependency); route_from_router exported from router.node
- [Phase 09-05]: No root app.py shim — dual tree until Plan 06 (D-03/D-04)
- [Phase 09-05]: Absolute server.* and agents.* imports under PYTHONPATH=src/backend
- [Phase 09-06]: D-04 hard cut: delete legacy flat modules and graph/ with no re-export shims
- [Phase 09-06]: Patch agents.workflow.create_agents / AsyncZep (not factories) — lookup-site patching
- [Phase 09-06]: pytest pythonpath includes repo root so tests.conftest imports resolve under pytest 9
- [Phase 09-06]: Post-checkpoint: psycopg2-binary, tarot MCP build copies card-data.json, astro MCP optional

### Performance Metrics

| Phase | Plan | Duration | Tasks | Files |
|-------|------|----------|-------|-------|
| 09 | 01 | 2min | 2 | 8 |
| 09 | 02 | 2min | 2 | 9 |
| 09 | 03 | 1min | 2 | 9 |
| 09 | 04 | 1min | 2 | 6 |
| Phase 09 P05 | 1min | 2 tasks | 6 files |
| 09 | 06 | 25min | 3 | 16 |

### Session

- Stopped at: Completed 09-06-PLAN.md
- Resume: None
- Last session: 2026-07-19T21:45:00Z
