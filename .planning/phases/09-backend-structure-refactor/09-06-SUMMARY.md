---
phase: 09-backend-structure-refactor
plan: 06
subsystem: testing
tags: [pytest, hard-cut, server, agents, D-04, D-03]

requires:
  - phase: 09-backend-structure-refactor
    provides: server.* package and agents.setup_workflow (Plans 01–05)
provides:
  - tests import and patch server.* / agents.* only
  - legacy flat modules and graph/ deleted (no shims)
  - pytest -q green (SC-04)
  - README D-03 entrypoint uvicorn server.app:app verified
affects:
  - phase-09-verification
  - future backend imports

tech-stack:
  added:
    - psycopg2-binary (replaces psycopg2 for local sync)
  patterns:
    - "Hard-cut D-04: no re-export shims; patch at agents.workflow / agents.memory.tools lookup sites"
    - "pytest pythonpath = [src/backend, .] for agents.* and tests.conftest"

key-files:
  created: []
  modified:
    - tests/conftest.py
    - tests/test_stream_endpoint.py
    - tests/test_observability.py
    - tests/test_routing.py
    - tests/test_taro_cards.py
    - tests/test_memory_tools.py
    - tests/test_router.py
    - tests/test_add_memory_resilience.py
    - pyproject.toml
    - README.md
    - src/backend/agents/taro/factory.py
    - src/backend/agents/astro/factory.py
    - src/tarotmcp/package.json
    - uv.lock
  deleted:
    - src/backend/app.py
    - src/backend/auth.py
    - src/backend/observability.py
    - src/backend/schemas.py
    - src/backend/models.py
    - src/backend/graph/

key-decisions:
  - "D-04 hard cut: delete legacy flat modules and graph/ with no re-export shims"
  - "Patch agents.workflow.create_agents / AsyncZep (not factories) — lookup-site patching"
  - "pytest pythonpath includes repo root so tests.conftest imports resolve under pytest 9"
  - "Post-checkpoint: psycopg2-binary, tarot MCP build copies card-data.json, astro MCP optional"

patterns-established:
  - "Pattern: single import vocabulary server.* / agents.* in production and tests"
  - "Pattern: no dual tree — legacy graph/ and root app.py gone after Plan 06"

requirements-completed: [SC-04, SC-01, SC-02]

duration: 25min
completed: 2026-07-19
---

# Phase 09 Plan 06: Hard-Cut Legacy Deletion Summary

**D-04 hard cut to `server.*` / `agents.*`: tests rewritten, legacy flat modules and `graph/` deleted, pytest green, human-verified `uvicorn server.app:app`**

## Performance

- **Duration:** ~25 min (tasks 1–2 + post-checkpoint fixes; human verify in between)
- **Started:** 2026-07-19T21:19:00Z
- **Completed:** 2026-07-19T21:45:00Z
- **Tasks:** 3
- **Files modified:** 16 (8 tests + deletes + post-checkpoint startup fixes)

## Accomplishments
- Rewrote all test imports/patches to `server.*` and `agents.*` (D-04 hard cut)
- Deleted legacy root modules (`app.py`, `auth.py`, `observability.py`, `schemas.py`, `models.py`) and entire `src/backend/graph/`
- Confirmed `pytest -q` green (13 passed), grep gates empty, stream auth tests intact
- Human approved D-03 entrypoint docs (`uvicorn server.app:app`)

## Task Commits

Each task was committed atomically:

1. **Task 1: Rewrite all test imports and patch targets** - `efa6307` (test)
2. **Task 2: Delete legacy modules, clear caches, full suite + grep gates** - `5e726a5` (chore)
3. **Task 3: Confirm live entrypoint docs match runnable command** - human-verify **approved** (no code commit)

**Post-checkpoint startup fixes (D-03 runnable):**

4. `7ff9c00` fix(09-06): include repo root on pytest pythonpath
5. `02183c5` fix: switch to psycopg2-binary for local sync
6. `61db95b` fix: require tarot MCP build and copy card-data.json
7. `5bebb36` fix: start without astro MCP when dist is missing
8. `dd04dc7` docs: clarify D-03 uvicorn startup from repo root

**Plan metadata:** (see docs commit after self-check)

## Files Created/Modified
- `tests/*.py` — imports/patches point at `server.*` / `agents.*` only
- `src/backend/{app,auth,observability,schemas,models}.py` — deleted
- `src/backend/graph/` — deleted
- `pyproject.toml` — `pythonpath = ["src/backend", "."]`; `psycopg2-binary`
- `README.md` — `PYTHONPATH=src/backend` + `uvicorn server.app:app`; tarot/astro notes
- `src/backend/agents/taro/factory.py` — fail-fast if tarot MCP dist missing
- `src/backend/agents/astro/factory.py` — optional MCP when dist absent (deferred v2)
- `src/tarotmcp/package.json` — build copies `card-data.json` into `dist/`

## Decisions Made
- Hard-cut only — no deprecation re-export shims (D-03/D-04)
- Patch at `agents.workflow.create_agents` / `AsyncZep` and `agents.memory.tools.zep.graph.search` (lookup sites)
- Add `.` to pytest `pythonpath` so `from tests.conftest` works under pytest 9 importlib collection
- Make D-03 startup practical: binary psycopg2, required tarot MCP build, optional astro MCP

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] pytest could not import `tests.conftest`**
- **Found during:** Post-checkpoint gate re-check (continuation after Task 3 approved)
- **Issue:** `pythonpath = ["src/backend"]` alone left `from tests.conftest` as `ModuleNotFoundError` under pytest 9
- **Fix:** Set `pythonpath = ["src/backend", "."]`
- **Files modified:** `pyproject.toml`
- **Verification:** `uv run pytest -q` → 13 passed
- **Committed in:** `7ff9c00`

**2. [Rule 2 - Missing Critical] Post-checkpoint D-03 startup blockers (user-approved)**
- **Found during:** Task 3 human verification (user fixed locally, then approved)
- **Issue:** `psycopg2` needed `pg_config`; tarot MCP runtime needed `card-data.json` in `dist/`; astro MCP missing blocked startup
- **Fix:** `psycopg2-binary`; tarot build copies JSON + fail-fast; astro factory skips MCP when dist absent
- **Files modified:** `pyproject.toml`, `uv.lock`, `src/tarotmcp/package.json`, `src/backend/agents/taro/factory.py`, `src/backend/agents/astro/factory.py`, `README.md`
- **Verification:** Gates remain green; README documents runnable entrypoint
- **Committed in:** `02183c5`, `61db95b`, `5bebb36`, `dd04dc7`

---

**Total deviations:** 2 auto-fixed (1 blocking, 1 missing-critical / human-driven startup)
**Impact on plan:** Required for SC-04 gate and D-03 runnable entrypoint; no scope creep beyond making the hard-cut tree startable.

## Issues Encountered
- Checkpoint paused for human verify; user approved after local startup fixes (psycopg2-binary, tarotmcp build, astro optional)
- Continuation re-check found pytest red until pythonpath included repo root

## User Setup Required
None beyond existing `.env` / MCP build notes already in README:
- `cd src/tarotmcp && npm install && npm run build` required for live tarot tools
- Astro MCP remains deferred (v2)

## Next Phase Readiness
- Phase 9 plans 01–06 complete — ready for `/gsd-verify-work` / phase verification
- Single import vocabulary (`server.*` / `agents.*`); no legacy dual tree
- SC-04 satisfied: `pytest -q` green against new layout

## Self-Check: PASSED

- SUMMARY exists at `.planning/phases/09-backend-structure-refactor/09-06-SUMMARY.md`
- Task commits present: `efa6307`, `5e726a5`
- Post-checkpoint commits present: `7ff9c00`, `02183c5`, `61db95b`, `5bebb36`, `dd04dc7`
- Gates: no `src/backend/graph`, no `src/backend/app.py`, README has `uvicorn server.app:app`, `pytest -q` → 13 passed

---
*Phase: 09-backend-structure-refactor*
*Completed: 2026-07-19*
