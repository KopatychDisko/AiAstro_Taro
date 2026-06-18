# Project State

**Milestone:** v1.0 — Brownfield Hardening  
**Status:** Complete  
**Last updated:** 2026-06-17

## Current Phase

All 8 phases complete.

## Completed

- Phase 1: Security (SEC-01–04)
- Phase 2: Bug Fixes (BUG-01–04)
- Phase 3: Test Foundation (TEST-01–06)
- Phase 4: MCP Card Pipeline (ARCH-01–02)
- Phase 5: Graph & Schema Cleanup (ARCH-03–06)
- Phase 6: Reliability (REL-01–04)
- Phase 7: Langfuse Observability (OBS-01–03)
- Phase 8: README & Documentation (DOC-01–03)

## Blockers

None.

## Notes

- `uv sync` may fail on `psycopg2` without `pg_config`; use selective `uv pip install` for dev/test.
- Tarot MCP requires `npm run build` in `src/tarotmcp` before live runs.
- Astro MCP deferred to v2.
