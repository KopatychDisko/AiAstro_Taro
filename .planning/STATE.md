---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: phase_11_added
last_updated: "2026-07-20T02:02:00.000Z"
last_activity: 2026-07-20 — Added Phase 11 Agent Harness Hardening
progress:
  total_phases: 11
  completed_phases: 9
  total_plans: 0
  completed_plans: 0
  percent: 82
---

# Project State

**Milestone:** v1.0 — Brownfield Hardening  
**Status:** Phase 11 context gathered — ready to plan  
**Last updated:** 2026-07-20

## Current Position

Phase: 11-agent-harness-hardening  
Status: Context gathered — ready for `/gsd-plan-phase 11`  
Last activity: 2026-07-20 — Discussed Phase 11 (D-01–D-13)

## Current Phase

Phase 11: Agent Harness Hardening — not planned

## Completed

- Phase 1: Security (SEC-01–04)
- Phase 2: Bug Fixes (BUG-01–04)
- Phase 3: Test Foundation (TEST-01–06)
- Phase 4: MCP Card Pipeline (ARCH-01–02)
- Phase 5: Graph & Schema Cleanup (ARCH-03–06)
- Phase 6: Reliability (REL-01–04)
- Phase 7: Langfuse Observability (OBS-01–03)
- Phase 8: README & Documentation (DOC-01–03)
- Phase 9: Backend Structure Refactor (SC-01–04) — verified

## Blockers

None

## Notes

- Uses `psycopg2-binary` (no system `pg_config` required for `uv sync`).
- Tarot MCP requires `npm run build` in `src/tarotmcp` before live runs (copies `card-data.json` into `dist/`).
- Astro MCP deferred to v2 — backend starts without it.
- Backend entrypoint: `uv run aitaro-api` (127.0.0.1:8000, reload); setup via `uv run aitaro-setup`.

## Accumulated Context

### Roadmap Evolution

- Phase 9 added: Backend structure refactor — split into agents and server packages; split graph into per-agent and subagent modules
- Phase 10 added: Simple Startup — one-command local run, MCP build, env checks, remove PYTHONPATH friction
- Phase 11 added: Agent Harness Hardening — dead unlock agent, budgets, trust-labeled Zep context, Langfuse v4 verify, lightweight evals

## Performance Metrics

| Phase | Plan | Duration | Notes |
|-------|------|----------|-------|
| Phase 10 P01 | 2min | 2 tasks | 7 files |
| Phase 10 P02 | 2min | 2 tasks | 4 files |
| Phase 10 P03 | 3min | 2 tasks | 6 files |

## Decisions

- [Phase 10]: setuptools py-modules from scripts/ only — never packages=find under src/ (D-05)
- [Phase 10]: required_env loads repo-root .env when present; tests no-op loader for isolation
- [Phase 10]: aitaro_api.main is path-only stub; uvicorn deferred to Plan 03
- [Phase 10]: aitaro_setup.main is path + require_env_or_exit only; npm/checklist deferred to Plan 02
- [Phase 10]: Checklist wording matches RESEARCH discretionary stdout (MCP OK, keys, aitaro-api, login_menu + POSTGRESQL_* reminder)
- [Phase 10]: Factory missing-dist primary hint is uv run aitaro-setup; legacy npm one-liner secondary
- [Phase 10]: Bind aitaro-api to 127.0.0.1:8000 with reload=True (T-10-05)
- [Phase 10]: README Quick start is four steps plus UI; no PYTHONPATH uvicorn (D-08/D-16)
