---
phase: 11-agent-harness-hardening
plan: 04
subsystem: testing
tags: [deepeval, pytest, eval, router, taro, offline]

requires:
  - phase: 11-agent-harness-hardening
    provides: Router/taro harness stable after unlock strip + trust/cap (11-02, 11-03)
provides:
  - Offline DeepEval+pytest eval harness for router + taro (D-12, D-13)
  - pytest marker eval + addopts -m "not eval" (SC-11.6)
  - Hand-curated goldens under tests/evals/
affects: [phase-11-verification, future-eval-expansion]

tech-stack:
  added: [deepeval>=4.1.1]
  patterns:
    - "ExactMatchMetric BaseMetric for offline assert_test (no LLM judge / no Confident AI)"
    - "@pytest.mark.eval + addopts exclusion keeps default pytest green/fast"

key-files:
  created:
    - tests/evals/metrics.py
    - tests/evals/goldens_router.json
    - tests/evals/goldens_taro.json
    - tests/evals/test_router_eval.py
    - tests/evals/test_taro_eval.py
  modified:
    - pyproject.toml
    - uv.lock
    - README.md
    - .gitignore

key-decisions:
  - "Deterministic ExactMatchMetric instead of GEval — offline, no judge key required for suite pass"
  - "Router evals drive mocked next_node through real router_node path; taro evals use parse_mcp_reading_text"
  - "Ignore .deepeval/ local telemetry after suite runs"

patterns-established:
  - "Pattern: hand-curated JSON goldens + metrics.py + @pytest.mark.eval assert_test"
  - "Pattern: default uv run pytest -q excludes eval; opt-in via -m eval or deepeval test run"

requirements-completed: [SC-11.5, SC-11.6]

duration: 3min
completed: 2026-07-20
---

# Phase 11 Plan 04: Offline DeepEval Suite Summary

**DeepEval+pytest offline eval harness for router + taro behind an eval marker so default pytest stays green and fast**

## Performance

- **Duration:** 3 min
- **Started:** 2026-07-19T23:37:57Z
- **Completed:** 2026-07-19T23:40:28Z
- **Tasks:** 2
- **Files modified:** 9

## Accomplishments

- Installed `deepeval==4.1.1` via `uv add --dev` after human PyPI↔GitHub legitimacy approval (D-12 / T-11-SC)
- Hand-curated router (6) + taro (4) goldens with `ExactMatchMetric` + `assert_test` (no Confident AI login)
- Registered `eval` marker and `addopts = -m 'not eval'`; default `uv run pytest -q` → 67 passed, 10 deselected
- README documents `uv run pytest -m eval` and `uv run deepeval test run tests/evals`

## Task Commits

Each task was committed atomically:

1. **Task 1: Verify deepeval package legitimacy** — checkpoint (human replied `approved`; no code commit)
2. **Task 2: Install deepeval and scaffold marked offline evals** (TDD)
   - `8f7e474` (test) — failing eval suite imports before deepeval install
   - `1405b5a` (feat) — uv add deepeval, metrics/markers/addopts, README
   - `7574f66` (chore) — ignore `.deepeval/` runtime telemetry

**Plan metadata:** `3ff74c4` (docs: complete plan)

## Files Created/Modified

- `tests/evals/metrics.py` — `ExactMatchMetric` + ROUTER/TARO metric lists
- `tests/evals/goldens_router.json` — hand-curated router intent goldens
- `tests/evals/goldens_taro.json` — hand-curated MCP spread-name goldens
- `tests/evals/test_router_eval.py` — `@pytest.mark.eval` mocked router path
- `tests/evals/test_taro_eval.py` — `@pytest.mark.eval` mapping path
- `pyproject.toml` — deepeval dev dep, markers, addopts
- `uv.lock` — locked deepeval 4.1.1
- `README.md` — offline eval run instructions
- `.gitignore` — `.deepeval/`

## Decisions Made

- Used deterministic `ExactMatchMetric` (Claude discretion) so explicit `-m eval` stays offline and does not require an LLM judge key for green runs
- Coverage limited to router + taro (D-13); no astro eval file
- No Confident AI login / tracing skill wiring (D-12)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Closed router astream after early break**
- **Found during:** Task 2 (GREEN verification)
- **Issue:** Breaking out of `compiled.astream` raised `PytestUnraisableExceptionWarning` / `GeneratorExit`
- **Fix:** Assign stream, `break` on router update, `await stream.aclose()` in `finally`
- **Files modified:** `tests/evals/test_router_eval.py`
- **Verification:** `uv run pytest -q -m eval` → 10 passed without GeneratorExit warnings
- **Committed in:** `1405b5a`

**2. [Rule 2 - Critical] Ignore DeepEval local telemetry dir**
- **Found during:** Task 2 (post-run `git status`)
- **Issue:** Running evals created untracked `.deepeval/` telemetry
- **Fix:** Added `.deepeval/` to `.gitignore`
- **Files modified:** `.gitignore`
- **Verification:** `.deepeval/` no longer listed as untracked
- **Committed in:** `7574f66`

## Auth Gates

Task 1 human-verify for deepeval PyPI↔GitHub legitimacy — user replied `approved`; install proceeded.

## TDD Gate Compliance

- RED: `8f7e474` — `ModuleNotFoundError: deepeval` on collection
- GREEN: `1405b5a` — package + markers + suite green
- Optional chore after GREEN: `7574f66`

## Threat Flags

None — no new network endpoints; evals offline; Confident AI login not introduced; default pytest path excludes evals (T-11-07, T-11-08).

## Known Stubs

None.

## Verification Results

- `uv run pytest -q` → 67 passed, 10 deselected (evals excluded)
- `uv run pytest -q -m eval --collect-only` → 10 tests (`test_router_eval` ×6, `test_taro_eval` ×4)
- `uv run pytest -q -m eval` → 10 passed

## Next Phase Readiness

- SC-11.5 / SC-11.6 satisfied for Phase 11 eval harness
- Ready for phase verification / UAT

## Self-Check: PASSED

- FOUND: tests/evals/metrics.py, goldens_router.json, goldens_taro.json, test_router_eval.py, test_taro_eval.py, 11-04-SUMMARY.md
- FOUND: commits 8f7e474, 1405b5a, 7574f66
