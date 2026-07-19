---
phase: 11-agent-harness-hardening
plan: 01
subsystem: observability
tags: [langfuse, langchain, runnable-config, pytest, tracing]

requires:
  - phase: 07-langfuse-observability
    provides: Optional Langfuse CallbackHandler path and LANGFUSE_* keys
provides:
  - Langfuse SDK v4 helpers (CallbackHandler no session kwargs, metadata, flush)
  - RunnableConfig propagation to router/taro/astro/summarize ainvoke
  - Wave 0 mocked config-prop integration tests (SC-11.4)
affects: [11-02-unlock-cleanup, 11-03-trust-budgets, 11-04-deepeval]

tech-stack:
  added: []
  patterns:
    - "v4 CallbackHandler() + langfuse_* metadata on RunnableConfig"
    - "flush_langfuse in stream finally when callbacks non-empty"
    - "Optional keys: empty callbacks, no required env"

key-files:
  created:
    - tests/test_langfuse_config_prop.py
  modified:
    - src/backend/server/observability.py
    - src/backend/server/app.py
    - src/backend/agents/router/node.py
    - src/backend/agents/taro/node.py
    - src/backend/agents/astro/node.py
    - src/backend/agents/workflow.py
    - tests/test_observability.py
    - README.md

key-decisions:
  - "Landed existing WIP Langfuse v4 API rather than inventing a second wrapper"
  - "Kept astro config=config while astro remains (Claude discretion / D-10)"
  - "Config-prop summarize assertions accept LangGraph AsyncCallbackManager wrap"

patterns-established:
  - "Pattern: session/user via metadata keys, not CallbackHandler ctor kwargs"
  - "Pattern: thin node ainvoke config tests + one graph-level summarize check"

requirements-completed: [SC-11.4, SC-11.6]

duration: 2min
completed: 2026-07-20
---

# Phase 11 Plan 01: Langfuse v4 Wiring Summary

**Optional Langfuse SDK v4 CallbackHandler + metadata/flush on `/stream`, with mocked unit and config-propagation tests (no live cloud)**

## Performance

- **Duration:** 2 min
- **Started:** 2026-07-19T23:26:20Z
- **Completed:** 2026-07-19T23:28:00Z
- **Tasks:** 2
- **Files modified:** 10 (including orphan `src/new_temp.py` deletion)

## Accomplishments

- Landed v4 observability helpers: empty callbacks without keys; `CallbackHandler()` with zero session kwargs when keys present; `langfuse_run_metadata`; `flush_langfuse`
- Wired `/stream` RunnableConfig callbacks + metadata and `finally` flush when callbacks used
- Propagated `config=config` through router, taro, astro, and summarize `ainvoke`
- Added Wave 0 `tests/test_langfuse_config_prop.py`; full `uv run pytest -q` green (55 passed)

## Task Commits

Each task was committed atomically:

1. **Task 1: Land Langfuse v4 wiring from working tree** - `c425744` (feat)
2. **Task 2: Wave 0 config-propagation integration tests** - `4f9cfe9` (test)

**Plan metadata:** `9ab9441` (docs: complete plan)

## Files Created/Modified

- `src/backend/server/observability.py` — v4 build/metadata/flush helpers
- `src/backend/server/app.py` — stream metadata + flush
- `src/backend/agents/router/node.py` — `ainvoke(..., config=config)`
- `src/backend/agents/taro/node.py` — same
- `src/backend/agents/astro/node.py` — same (kept while astro exists)
- `src/backend/agents/workflow.py` — summarize `ainvoke` config prop
- `tests/test_observability.py` — mocked CallbackHandler / flush / metadata
- `tests/test_langfuse_config_prop.py` — Wave 0 config propagation
- `README.md` — Langfuse propagation sentence
- `src/new_temp.py` — deleted orphan (optional WIP cleanup)

## Decisions Made

- Did not rewrite a second wrapper API; committed the existing WIP (D-10)
- Astro keeps config propagation until a future remove-astro phase
- Summarize integration asserts metadata + non-None callbacks (LangGraph wraps list in AsyncCallbackManager)

## Deviations from Plan

None - plan executed exactly as written.

Optional orphan `src/new_temp.py` deletion included as allowed by Task 1 action.

## Issues Encountered

- Fake `object()` callbacks broke LangGraph `astream` (`run_inline` missing) — fixed tests with a minimal `BaseCallbackHandler` subclass

## User Setup Required

None - no external service configuration required. Langfuse keys remain optional (D-11 / Phase 10 D-12).

## Next Phase Readiness

- SC-11.4 / SC-11.6 observability slice done; Wave 2 (11-02 unlock/spread_name) unblocked for Langfuse-shared tree
- No new required env keys; live Langfuse cloud still out of scope

## Known Stubs

None

## Threat Flags

None — no new trust-boundary surface beyond plan threat model (optional outbound telemetry when keys present)

## Self-Check: PASSED

- Artifacts present: `observability.py`, `test_langfuse_config_prop.py`, `11-01-SUMMARY.md`
- Commits present: `c425744`, `4f9cfe9`
- Config prop call sites: router/taro/astro/workflow summarize

---
*Phase: 11-agent-harness-hardening*
*Completed: 2026-07-20*
