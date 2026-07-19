---
phase: 10-simple-startup
plan: 02
subsystem: infra
tags: [npm, subprocess, aitaro-setup, tarotmcp, streamlit, fail-fast]

requires:
  - phase: 10-simple-startup
    provides: aitaro-setup/aitaro-api packaging stubs and server.required_env
provides:
  - aitaro_setup.build_tarot_mcp fixed-argv npm install/build under src/tarotmcp
  - aitaro_setup.main env-before-npm + stdout checklist (login_menu.py, Postgres reminder)
  - tarot factory FileNotFoundError primary hint uv run aitaro-setup
affects: [10-03-api-lifespan, README-quick-start]

tech-stack:
  added: []
  patterns:
    - "subprocess.run fixed argv lists only; cwd = repo_root/src/tarotmcp"
    - "env fail-fast before npm; checklist prints key names never values"
    - "factory missing-dist primary remediation matches aitaro-setup"

key-files:
  created:
    - tests/test_tarot_factory_message.py
  modified:
    - scripts/aitaro_setup.py
    - src/backend/agents/taro/factory.py
    - tests/test_aitaro_scripts.py

key-decisions:
  - "Checklist wording matches RESEARCH: Tarot MCP OK, required keys, aitaro-api next, UI optional with POSTGRESQL_* reminder"
  - "Factory keeps legacy npm one-liner as secondary hint after uv run aitaro-setup"
  - "require_env_or_exit stays lazy-imported inside main after ensure_backend_on_path"

patterns-established:
  - "Pattern: build_tarot_mcp(repo_root) raises FileNotFoundError if src/tarotmcp missing"
  - "Pattern: unit tests monkeypatch subprocess.run — no real npm in CI unit path"

requirements-completed: [SC-10.1, SC-10.4]

duration: 2min
completed: 2026-07-20
---

# Phase 10 Plan 02: Setup npm & factory message Summary

**aitaro-setup runs env fail-fast then fixed-argv npm install/build in src/tarotmcp and prints Streamlit/Postgres checklist; tarot factory missing-dist points at `uv run aitaro-setup`**

## Performance

- **Duration:** 2 min
- **Started:** 2026-07-19T22:22:42Z
- **Completed:** 2026-07-19T22:24:29Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Completed `aitaro-setup` end-to-end: path ensure → `require_env_or_exit` → `build_tarot_mcp` → checklist (D-02, D-10–D-15)
- Fixed argv `["npm","install"]` / `["npm","run","build"]` with cwd only under `repo_root/src/tarotmcp` (T-10-03/T-10-04); no `uv sync`, no `shell=True`
- Aligned `create_tarot_agent` FileNotFoundError with primary `uv run aitaro-setup` remediation (SC-10.4)
- Unit tests cover monkeypatched npm argv/cwd/order and factory message; full suite 39 passed

## Task Commits

Each task was committed atomically:

1. **Task 1 (RED): aitaro-setup npm/checklist tests** - `6917ac0` (test)
2. **Task 1 (GREEN): implement aitaro-setup** - `5a596a1` (feat)
3. **Task 2 (RED): factory aitaro-setup message test** - `0762893` (test)
4. **Task 2 (GREEN): factory message alignment** - `8ad6d87` (feat)

**Plan metadata:** `87b404a` (docs: complete plan)

## Files Created/Modified

- `scripts/aitaro_setup.py` — `build_tarot_mcp`, full `main` with checklist
- `tests/test_aitaro_scripts.py` — env-before-npm, argv/cwd, checklist, no uv sync assertions
- `src/backend/agents/taro/factory.py` — FileNotFoundError mentions `uv run aitaro-setup`
- `tests/test_tarot_factory_message.py` — SC-10.4 assertion via monkeypatched `isfile`

## Decisions Made

- Checklist stdout copied from RESEARCH discretionary wording (MCP OK, three keys, `aitaro-api`, UI with `login_menu.py` + POSTGRESQL_* reminder)
- Kept legacy `cd src/tarotmcp && npm …` as secondary parenthetical in factory error
- Left `require_env_or_exit` as import-inside-`main` so path is set before `server` import (same pattern as Plan 01 stub)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## User Setup Required

None - no external service configuration required. Developers still need Node/npm available when running real `uv run aitaro-setup` (unit tests mock subprocess).

## Next Phase Readiness

- Plan 03 can wire `uvicorn.run` into `aitaro_api.main` and lifespan `require_env_or_raise` before `setup_workflow`
- README Quick start can document `uv run aitaro-setup` as the MCP build step

## Self-Check: PASSED

- FOUND: `scripts/aitaro_setup.py`, `src/backend/agents/taro/factory.py`, `tests/test_aitaro_scripts.py`, `tests/test_tarot_factory_message.py`
- FOUND: commits `6917ac0`, `5a596a1`, `0762893`, `8ad6d87`
