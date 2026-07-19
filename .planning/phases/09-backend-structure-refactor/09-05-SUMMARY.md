---
phase: 09-backend-structure-refactor
plan: 05
subsystem: api
tags: [fastapi, server, uvicorn, auth, pydantic, langfuse]

requires:
  - phase: 09-backend-structure-refactor
    provides: agents.setup_workflow and agents.models.TaroCard (Plan 04)
provides:
  - server.app:app ASGI entrypoint
  - server.auth.verify_stream_api_key with compare_digest
  - server.schemas.ExtractData and UserData
  - server.observability.build_langfuse_callbacks
  - README documents uvicorn server.app:app
affects:
  - 09-06-legacy-deletion
  - frontend STREAM client docs

tech-stack:
  added: []
  patterns:
    - "server/ is HTTP-only; imports agents one-way"
    - "ExtractData/UserData live in server.schemas; TaroCard from agents.models"

key-files:
  created:
    - src/backend/server/__init__.py
    - src/backend/server/app.py
    - src/backend/server/auth.py
    - src/backend/server/observability.py
    - src/backend/server/schemas.py
  modified:
    - README.md

key-decisions:
  - "No root app.py shim — dual tree until Plan 06 (D-03/D-04)"
  - "Absolute server.* and agents.* imports under PYTHONPATH=src/backend"

patterns-established:
  - "Pattern: HTTP package under server/; domain under agents/; one-way import only"
  - "Pattern: Stream auth relocated without weakening compare_digest / fail-closed"

requirements-completed: [SC-01]

duration: 1min
completed: 2026-07-19
---

# Phase 09 Plan 05: Server Package Summary

**FastAPI HTTP package at `server/` with `server.app:app`, auth preserved via `secrets.compare_digest`, and README entrypoint `uvicorn server.app:app`**

## Performance

- **Duration:** 1 min
- **Started:** 2026-07-19T21:14:46Z
- **Completed:** 2026-07-19T21:15:52Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments
- Created `src/backend/server/` with app, auth, observability, and schemas
- Wired `/stream` to `agents.setup_workflow`; schemas import `TaroCard` from `agents.models`
- Updated README to document `uvicorn server.app:app` and server/ + agents/ layout
- Left legacy root modules intact for Plan 06 deletion

## Task Commits

Each task was committed atomically:

1. **Task 1: Create server package with one-way agents imports** - `aea3f79` (feat)
2. **Task 2: Update README entrypoint and layout docs** - `e6e283c` (docs)

**Plan metadata:** (pending docs commit)

## Files Created/Modified
- `src/backend/server/__init__.py` - Minimal server package marker
- `src/backend/server/app.py` - FastAPI app + `/stream` lifespan using `setup_workflow`
- `src/backend/server/auth.py` - Stream API key verification (compare_digest, fail-closed)
- `src/backend/server/observability.py` - Langfuse callback builder
- `src/backend/server/schemas.py` - ExtractData / UserData; TaroCard from agents.models
- `README.md` - Entrypoint and layout docs for server/ + agents/

## Decisions Made
- No root compatibility shim for `app:app` — dual tree only until Plan 06 deletes legacy roots (D-03/D-04, T-09-02)
- Used absolute imports (`server.*`, `agents.*`) matching `pythonpath = ["src/backend"]`
- Auth logic copied without change to preserve T-09-01 mitigations

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- `uv run python` failed to resolve env due to `psycopg2` build (missing `pg_config`); verification used existing `.venv/bin/python` with `PYTHONPATH=src/backend` instead

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- `server.app:app` is the documented ASGI entrypoint; Plan 06 can delete legacy root `app.py`, `auth.py`, `observability.py`, `schemas.py`
- Agents package has zero imports of server; one-way boundary holds

## Self-Check: PASSED

- Created files present: `src/backend/server/{__init__,app,auth,observability,schemas}.py`, SUMMARY
- Commits present: `aea3f79`, `e6e283c`

---
*Phase: 09-backend-structure-refactor*
*Completed: 2026-07-19*
