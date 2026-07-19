---
phase: 10-simple-startup
plan: 01
subsystem: infra
tags: [uv, setuptools, console-scripts, dotenv, pytest, fail-fast]

requires:
  - phase: 09-backend-structure-refactor
    provides: server package under src/backend with flat imports
provides:
  - setuptools [project.scripts] aitaro-setup and aitaro-api
  - scripts/ path wrappers (sys.path + PYTHONPATH)
  - server.required_env shared D-09/D-11 fail-fast helper
  - Wave 0 tests for env and entrypoints
affects: [10-02-setup-npm, 10-03-api-lifespan]

tech-stack:
  added: [setuptools>=61 (build-system only)]
  patterns:
    - "scripts-only packaging via py-modules + package-dir (no src/ ship)"
    - "path wrapper sets sys.path and PYTHONPATH for uvicorn reload children"
    - "shared required_env for setup CLI and future lifespan"

key-files:
  created:
    - scripts/aitaro_api.py
    - scripts/aitaro_setup.py
    - src/backend/server/required_env.py
    - tests/test_required_env.py
    - tests/test_aitaro_scripts.py
  modified:
    - pyproject.toml
    - uv.lock

key-decisions:
  - "setuptools py-modules from scripts/ only — never packages=find under src/ (D-05)"
  - "required_env loads repo-root .env when present; tests no-op loader for isolation"
  - "aitaro_api.main is path-only stub; uvicorn deferred to Plan 03"
  - "aitaro_setup.main is path + require_env_or_exit only; npm/checklist deferred to Plan 02"

patterns-established:
  - "Pattern: console entrypoints live in scripts/ registered via [project.scripts]"
  - "Pattern: ensure_backend_on_path inserts src/backend on sys.path and PYTHONPATH"
  - "Pattern: REQUIRED_ENV_KEYS exactly STREAM_API_KEY, OPENAI_API_KEY, ZEP_API; optional keys unchecked"

requirements-completed: [SC-10.1, SC-10.2, SC-10.3, SC-10.6]

duration: 2min
completed: 2026-07-20
---

# Phase 10 Plan 01: Packaging & required_env Summary

**setuptools console scripts `aitaro-setup`/`aitaro-api` plus shared `server.required_env` fail-fast (D-09/D-11) with Wave 0 pytest coverage**

## Performance

- **Duration:** 2 min
- **Started:** 2026-07-19T22:18:46Z
- **Completed:** 2026-07-19T22:20:45Z
- **Tasks:** 2
- **Files modified:** 7

## Accomplishments

- Packaged flat `scripts/` modules via setuptools so `uv run aitaro-setup` / `uv run aitaro-api` resolve after `uv sync`
- Shared `server.required_env` implements D-09 keys, empty-as-missing, compact `.env.example` hint (D-11), no optional-key checks (D-12), no secret values in messages (T-10-01)
- Wave 0 tests green; full suite `33 passed`; pytest `pythonpath` unchanged (D-07)

## Task Commits

Each task was committed atomically:

1. **Task 1 (RED): Wave 0 failing tests** - `28f2fba` (test)
2. **Task 1 (GREEN): Packaging, path stubs, required_env** - `9172224` (feat)
3. **Task 2: Expand Wave 0 entrypoint coverage** - `21ffac7` (test)

**Plan metadata:** (pending docs commit)

## Files Created/Modified

- `pyproject.toml` — `[project.scripts]`, `[build-system]` setuptools, `py-modules` + `package-dir` for scripts/
- `uv.lock` — editable project install metadata after packaging
- `scripts/aitaro_api.py` — `find_repo_root`, `ensure_backend_on_path`, path-only `main`
- `scripts/aitaro_setup.py` — path + `require_env_or_exit` stub
- `src/backend/server/required_env.py` — D-09/D-11/D-12 fail-fast helpers
- `tests/test_required_env.py` — missing/empty/present keys; no secret leakage
- `tests/test_aitaro_scripts.py` — importable entrypoints and path helper contracts

## Decisions Made

- Used setuptools `py-modules` + `package-dir = {"" = "scripts"}` per RESEARCH Pattern 1 (smallest change; no hatchling)
- Prefer repo-root `.env` in `_load_dotenv_from_repo` when `pyproject.toml` is found walking parents
- Autouse test fixture no-ops dotenv load so monkeypatch.delenv is not undone by local `.env`
- Stub mains only — uvicorn and npm intentionally deferred

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Dotenv reload undid monkeypatch.delenv in env tests**
- **Found during:** Task 1 GREEN verification
- **Issue:** `missing_required_env_keys` calls `_load_dotenv_from_repo`, which refilled `OPENAI_API_KEY` from the developer's `.env` after tests deleted it
- **Fix:** Autouse fixture patches `_load_dotenv_from_repo` to a no-op in `tests/test_required_env.py`
- **Files modified:** `tests/test_required_env.py`
- **Verification:** `uv run pytest -q tests/test_required_env.py tests/test_aitaro_scripts.py -x` — 20 passed
- **Committed in:** `9172224` (Task 1 GREEN)

---

**Total deviations:** 1 auto-fixed (Rule 1)
**Impact on plan:** Necessary for correct Wave 0 isolation against real `.env`; no scope creep.

## Issues Encountered

None beyond the dotenv/test isolation fix above.

## User Setup Required

None - no external service configuration required. Developers still copy `.env.example` → `.env` as before (validated by the new helper).

## Next Phase Readiness

- Plan 02 can wire npm MCP build + UI checklist into `aitaro_setup.main`
- Plan 03 can add uvicorn.run to `aitaro_api.main` and lifespan `require_env_or_raise` before `setup_workflow`

## Self-Check: PASSED

- FOUND: `scripts/aitaro_api.py`, `scripts/aitaro_setup.py`, `src/backend/server/required_env.py`, `tests/test_required_env.py`, `tests/test_aitaro_scripts.py`
- FOUND: commits `28f2fba`, `9172224`, `21ffac7`

---
*Phase: 10-simple-startup*
*Completed: 2026-07-20*
