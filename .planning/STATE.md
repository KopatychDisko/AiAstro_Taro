---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: human_verification_needed
last_updated: "2026-07-19T23:42:48Z"
last_activity: 2026-07-20 — Phase 11 verification human_needed (6/6 SC)
progress:
  total_phases: 3
  completed_phases: 2
  total_plans: 14
  completed_plans: 14
  percent: 100
---

# Project State

**Milestone:** v1.0 — Brownfield Hardening  
**Status:** Phase 11 verified (human_needed) — Streamlit spread_name title check  
**Last updated:** 2026-07-20

## Current Position

Phase: 11 (agent-harness-hardening) — COMPLETE  
Plan: 4 of 4
Status: Verified — UAT passed (spread_name title)
Last activity: 2026-07-20 — Phase 11 UAT complete

## Current Phase

Phase 11: Agent Harness Hardening — VERIFICATION.md written; status human_needed (UI title)

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
- Phase 10: Simple Startup — verified
- Phase 11: Agent Harness Hardening (SC-11.1–11.6) — verified

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
| Phase 11 P01 | 2min | 2 tasks | 10 files |
| Phase 11 P02 | 2min | 2 tasks | 12 files |
| Phase 11 P03 | 1min | 2 tasks | 6 files |
| Phase 11 P04 | 3min | 2 tasks | 9 files |

## Decisions

- [Phase 10]: setuptools py-modules from scripts/ only — never packages=find under src/ (D-05)
- [Phase 10]: required_env loads repo-root .env when present; tests no-op loader for isolation
- [Phase 10]: aitaro_api.main is path-only stub; uvicorn deferred to Plan 03
- [Phase 10]: aitaro_setup.main is path + require_env_or_exit only; npm/checklist deferred to Plan 02
- [Phase 10]: Checklist wording matches RESEARCH discretionary stdout (MCP OK, keys, aitaro-api, login_menu + POSTGRESQL_* reminder)
- [Phase 10]: Factory missing-dist primary hint is uv run aitaro-setup; legacy npm one-liner secondary
- [Phase 10]: Bind aitaro-api to 127.0.0.1:8000 with reload=True (T-10-05)
- [Phase 10]: README Quick start is four steps plus UI; no PYTHONPATH uvicorn (D-08/D-16)
- [Phase 11]: Landed existing WIP Langfuse v4 API rather than inventing a second wrapper
- [Phase 11]: Kept astro config=config while astro remains (Claude discretion / D-10)
- [Phase 11]: Config-prop summarize assertions accept LangGraph AsyncCallbackManager wrap
- [Phase 11]: Hard-delete unlock agent surface rather than wire it (D-01)
- [Phase 11]: Rename unlock_name → spread_name end-to-end; no dual-write (D-02/D-03)
- [Phase 11]: create_html_taro param renamed name → spread_name for clarity
- [Phase 11]: Pattern 2 English UNTRUSTED_USER_MEMORY prefix with treat-as-data line (D-08)
- [Phase 11]: Single wrap after success/fallback assign — both paths labeled once (D-09)
- [Phase 11]: Cap log extras: tool_iterations + max_tool_iterations (D-04)
- [Phase 11]: Deterministic ExactMatchMetric for offline router/taro DeepEval (no GEval/Confident AI)
- [Phase 11]: Eval coverage router+taro only; pytest mark eval excluded by default addopts
