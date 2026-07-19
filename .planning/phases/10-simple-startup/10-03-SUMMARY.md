---
phase: 10-simple-startup
plan: 03
subsystem: infra
tags: [uvicorn, fastapi, lifespan, aitaro-api, README, fail-fast]

requires:
  - phase: 10-simple-startup
    provides: aitaro-api path wrapper stub and server.required_env
provides:
  - aitaro_api.main uvicorn.run server.app:app host 127.0.0.1 port 8000 reload True
  - FastAPI lifespan require_env_or_raise before setup_workflow
  - README four-step Quick start plus login_menu.py UI line (no PYTHONPATH uvicorn)
affects: [phase-10-complete, developer-onboarding]

tech-stack:
  added: []
  patterns:
    - "uvicorn import-string + reload=True after ensure_backend_on_path sets PYTHONPATH"
    - "lifespan fail-closed: require_env_or_raise then await setup_workflow"
    - "README D-16 four backend steps + optional UI; never PYTHONPATH uvicorn"

key-files:
  created:
    - tests/test_lifespan_required_env.py
    - tests/test_readme_quickstart.py
  modified:
    - scripts/aitaro_api.py
    - src/backend/server/app.py
    - README.md
    - tests/test_aitaro_scripts.py

key-decisions:
  - "Bind host 127.0.0.1 (not 0.0.0.0) for local API (T-10-05)"
  - "uvicorn kwargs asserted only in test_lifespan_required_env.py"
  - "Legacy test_aitaro_api_main_only_ensures_path mocks uvicorn.run to avoid hang"

patterns-established:
  - "Pattern: aitaro-api is the only documented backend start path"
  - "Pattern: missing required env aborts lifespan before MCP/LLM init"

requirements-completed: [SC-10.2, SC-10.3, SC-10.5, SC-10.6]

duration: 3min
completed: 2026-07-20
---

# Phase 10 Plan 03: API Launch & README Summary

**`aitaro-api` runs uvicorn on 127.0.0.1:8000 with reload, lifespan fails closed on missing env before MCP, and README Quick start is four steps plus UI**

## Performance

- **Duration:** 3 min
- **Started:** 2026-07-19T22:25:57Z
- **Completed:** 2026-07-19T22:28:30Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments

- Completed `aitaro_api.main` with `uvicorn.run("server.app:app", host="127.0.0.1", port=8000, reload=True)` after path/PYTHONPATH setup (SC-10.2, D-03–D-05)
- FastAPI lifespan calls `require_env_or_raise()` before `await setup_workflow()` so missing env never initializes MCP/LLM (SC-10.3, D-10, T-10-01/T-10-02)
- README Quick start is `.env` → `uv sync` → `aitaro-setup` → `aitaro-api` plus `login_menu.py` UI; all `PYTHONPATH=… uvicorn` snippets removed (SC-10.5, D-08/D-16)
- Full suite green: 45 passed (SC-10.6)

## Task Commits

Each task was committed atomically:

1. **Task 1 (RED): lifespan/uvicorn failing tests** - `eaa2107` (test)
2. **Task 1 (GREEN): aitaro-api uvicorn + lifespan env** - `28b95a3` (feat)
3. **Task 2 (RED): README quickstart gates** - `68410ff` (test)
4. **Task 2 (GREEN): README four-step Quick start** - `8ac7426` (feat)

**Plan metadata:** (pending docs commit)

## Files Created/Modified

- `scripts/aitaro_api.py` — uvicorn.run with fixed host/port/reload after `ensure_backend_on_path`
- `src/backend/server/app.py` — `require_env_or_raise` before `setup_workflow` in lifespan
- `tests/test_lifespan_required_env.py` — ordering + uvicorn kwargs unit tests
- `tests/test_aitaro_scripts.py` — mock uvicorn.run in legacy path test (Rule 3)
- `README.md` — D-16 Quick start; no PYTHONPATH uvicorn
- `tests/test_readme_quickstart.py` — D-08/D-16 grep-style assertions

## Decisions Made

- Host `127.0.0.1` per RESEARCH/threat T-10-05 (local bind only)
- Kept uvicorn kwargs assertions out of Plan 02's `test_aitaro_scripts.py` as planned; only patched that file to mock `uvicorn.run` so `main()` no longer hangs CI
- README UI remains a separate optional line (D-03/D-15), not an `aitaro-ui` entrypoint

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Legacy entrypoint test hung after uvicorn wiring**
- **Found during:** Task 1 GREEN (post-verify of full entrypoint suite)
- **Issue:** `test_aitaro_api_main_only_ensures_path` called `aitaro_api.main()` without mocking uvicorn; after GREEN it bound a real server and hung pytest
- **Fix:** Monkeypatch `aitaro_api.uvicorn.run` to a no-op in that test only (kwargs still asserted in `test_lifespan_required_env.py`)
- **Files modified:** `tests/test_aitaro_scripts.py`
- **Verification:** `uv run pytest -q` — 45 passed
- **Committed in:** `28b95a3` (Task 1 GREEN)

---

**Total deviations:** 1 auto-fixed (Rule 3)
**Impact on plan:** Required for SC-10.6; no scope creep; plan ownership of uvicorn assertions preserved.

## Issues Encountered

None beyond the hanging stub test above.

## User Setup Required

None - no external service configuration required. Developers still copy `.env.example` → `.env` and run the four Quick start commands.

## Next Phase Readiness

- Phase 10 success criteria SC-10.1–SC-10.6 covered across plans 01–03
- Ready for phase verification / milestone audit

## Self-Check: PASSED

- FOUND: `scripts/aitaro_api.py`, `src/backend/server/app.py`, `tests/test_lifespan_required_env.py`, `tests/test_readme_quickstart.py`, `README.md`
- FOUND: commits `eaa2107`, `28b95a3`, `68410ff`, `8ac7426`

---
*Phase: 10-simple-startup*
*Completed: 2026-07-20*
