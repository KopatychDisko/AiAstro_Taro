---
phase: 11-agent-harness-hardening
plan: 03
subsystem: agents
tags: [tool-budget, trust-label, zep, routing, logging, pytest]

requires:
  - phase: 11-agent-harness-hardening
    provides: Langfuse v4 (11-01); unlock→spread_name (11-02)
provides:
  - Structured tool_iteration_cap_reached warning on MAX_TOOL_ITERATIONS
  - Documented MAX_TOOL_ITERATIONS=3 (code + README; not env-configurable)
  - Pure wrap_untrusted_user_memory at take_context assembly (always)
affects: [11-04-deepeval]

tech-stack:
  added: []
  patterns:
    - "Stable log message + structured extras (no dynamics in message string)"
    - "Trust label once at take_context; never in per-agent prompts"

key-files:
  created:
    - src/backend/agents/context_trust.py
    - tests/test_context_trust.py
  modified:
    - src/backend/agents/routing.py
    - src/backend/agents/workflow.py
    - tests/test_routing.py
    - README.md

key-decisions:
  - "Pattern 2 English UNTRUSTED_USER_MEMORY prefix with treat-as-data line (D-08)"
  - "Single wrap after success/fallback assign — both paths labeled once (D-09)"
  - "Cap log extras: tool_iterations + max_tool_iterations (D-04)"

patterns-established:
  - "Pattern: capped_tools_condition logs then returns __end__ silently"
  - "Pattern: wrap_untrusted_user_memory is pure and assembly-only"

requirements-completed: [SC-11.2, SC-11.3]

duration: 1min
completed: 2026-07-20
---

# Phase 11 Plan 03: Tool Cap Logging + Trust Label Summary

**Structured log on tool-iteration cap and always-wrap Zep/user memory at take_context assembly**

## Performance

- **Duration:** 1 min
- **Started:** 2026-07-19T23:34:26Z
- **Completed:** 2026-07-19T23:35:20Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments

- Cap path logs `tool_iteration_cap_reached` with `tool_iterations` / `max_tool_iterations` extras, then `__end__` with no user-facing limit copy
- `MAX_TOOL_ITERATIONS = 3` documented in code comment and README (not env-configurable)
- Pure `wrap_untrusted_user_memory` applied once for both Zep success and name-only fallback in `take_context`

## Task Commits

Each task was committed atomically (TDD RED → GREEN):

1. **Task 1: Cap logging on MAX_TOOL_ITERATIONS**
   - `c18e9dd` (test) — failing caplog / constant / below-cap tests
   - `baf3ff3` (feat) — structured cap warning + README budget note
2. **Task 2: Pure trust wrap in take_context**
   - `cea1eab` (test) — failing wrapper purity tests
   - `c72e71c` (feat) — `context_trust.py` + wire `take_context`

**Plan metadata:** `a95a693` (docs: complete plan)

## Files Created/Modified

- `src/backend/agents/routing.py` — comment + `logger.warning` on cap
- `src/backend/agents/context_trust.py` — prefix + pure wrap helper
- `src/backend/agents/workflow.py` — always wrap context before return
- `tests/test_routing.py` — caplog extras + below-cap delegation
- `tests/test_context_trust.py` — Wave 0 wrapper purity
- `README.md` — tool-loop budget of 3

## Decisions Made

- Used RESEARCH Pattern 2 wording for the English trust prefix
- Wrap once after both branches assign `context` (equivalent to wrapping each path; single call site)
- No token/cost/step budgets; cap remains named constant only (D-05/D-06)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## User Setup Required

None

## Next Phase Readiness

- SC-11.2 / SC-11.3 complete; Wave 4 (11-04 DeepEval) unblocked
- Prompt packages have no `UNTRUSTED_USER_MEMORY` (assembly-only)
- Full `uv run pytest -q` green (67 passed)

## Known Stubs

None

## Threat Flags

None — T-11-05 / T-11-06 mitigations implemented as specified; no new network/auth surface

## Self-Check: PASSED

- Artifacts present: `context_trust.py`, cap log in `routing.py`, wrap in `workflow.py`, `11-03-SUMMARY.md`
- Commits present: `c18e9dd`, `baf3ff3`, `cea1eab`, `c72e71c`
- pytest: 67 passed

---
*Phase: 11-agent-harness-hardening*
*Completed: 2026-07-20*
