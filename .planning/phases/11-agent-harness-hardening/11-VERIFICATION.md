---
phase: 11-agent-harness-hardening
verified: 2026-07-19T23:42:48Z
status: passed
score: 6/6 must-haves verified
overrides_applied: 0
human_verification: []
---

# Phase 11: Agent Harness Hardening Verification Report

**Phase Goal:** Harden the AiTaro agent harness per provider-neutral best practices: remove dead agent surface, make tool/step budgets explicit, label untrusted memory context, verify Langfuse v4 tracing reaches agents, and add a small eval/regression harness beyond unit mocks.

**Verified:** 2026-07-20T02:48:00Z  
**Status:** passed  
**Re-verification:** Human UAT completed — Streamlit spread_name title confirmed

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Dead `unlock_card_agent` removed from factories/state (SC-11.1 / D-01–D-03) | ✓ VERIFIED | `Agents` has no unlock field; `cards/factory.py` and `cards/prompt.py` deleted; `rg unlock_card_agent\|UnlockCard\|unlock_name` under `src/` empty; `AgentState`/`ExtractData`/frontend use `spread_name`; `img_node` emits MCP-derived `spread_name` |
| 2 | Tool/step budgets explicit, documented, enforceable (SC-11.2 / D-04–D-06) | ✓ VERIFIED | `MAX_TOOL_ITERATIONS = 3` with code comment; `capped_tools_condition` returns `__end__` and logs `tool_iteration_cap_reached` with structured extras; README documents silent stop; not env-configurable |
| 3 | Zep/user memory trust-labeled in context assembly (SC-11.3 / D-07–D-09) | ✓ VERIFIED | `wrap_untrusted_user_memory` in `context_trust.py`; `take_context` always wraps success and name-only exception fallback; not duplicated into per-agent prompts |
| 4 | Langfuse v4 CallbackHandler + config prop verified by tests; optional when keys absent (SC-11.4 / D-10–D-11) | ✓ VERIFIED | `CallbackHandler()` with no session ctor args; empty callbacks without keys; `app.py` metadata + `flush_langfuse` in `finally` when callbacks used; router/taro/astro/summarize pass `config=config`; covered by `tests/test_observability.py` + `tests/test_langfuse_config_prop.py` |
| 5 | Lightweight eval harness for router + one domain agent (SC-11.5 / D-12–D-13) | ✓ VERIFIED | `tests/evals/` with hand-curated goldens (6 router + 4 taro), `ExactMatchMetric`, `@pytest.mark.eval`; deepeval in `dependency-groups.dev`; no Confident AI login; astro not covered |
| 6 | `pytest -q` green; no new required env beyond optional Langfuse (SC-11.6) | ✓ VERIFIED | `uv run pytest -q` → **67 passed, 10 deselected**; `REQUIRED_ENV_KEYS` remains STREAM/OPENAI/ZEP only; Langfuse stays optional |

**Score:** 6/6 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | -------- | ------ | ------- |
| `src/backend/server/observability.py` | v4 callbacks/metadata/flush | ✓ VERIFIED | Exists, substantive, used by `app.py` |
| `src/backend/server/app.py` | stream config + flush | ✓ VERIFIED | Wired to observability helpers |
| `tests/test_observability.py` | mocked CallbackHandler tests | ✓ VERIFIED | Present; unit suite green |
| `tests/test_langfuse_config_prop.py` | ainvoke receives config | ✓ VERIFIED | Router/taro/astro/summarize cases |
| `src/backend/agents/state.py` | Agents without unlock; `spread_name` | ✓ VERIFIED | No `UnlockCard` / `unlock_card_agent` |
| `src/backend/agents/factories.py` | `create_agents` without unlock | ✓ VERIFIED | Six Agents fields only |
| `src/backend/agents/cards/node.py` | emits `spread_name` | ✓ VERIFIED | From `extract_cards_from_messages` |
| `src/backend/server/schemas.py` | `ExtractData.spread_name` | ✓ VERIFIED | Field present; no `unlock_name` |
| `src/frontend/pages/app.py` | session/messages use `spread_name` | ✓ VERIFIED | `create_html_taro(..., spread_name)` |
| `src/backend/agents/routing.py` | cap log `tool_iteration_cap_reached` | ✓ VERIFIED | Structured extras + `__end__` |
| `src/backend/agents/context_trust.py` | `wrap_untrusted_user_memory` | ✓ VERIFIED | Prefix + treat-as-data line |
| `src/backend/agents/workflow.py` | `take_context` wraps always | ✓ VERIFIED | Import + wrap on both paths |
| `tests/test_context_trust.py` | trust wrapper unit tests | ✓ VERIFIED | Prefix / empty / purity |
| `tests/test_routing.py` | caplog on cap | ✓ VERIFIED | Asserts message + extras |
| `tests/evals/metrics.py` | DeepEval metrics | ✓ VERIFIED | Offline `ExactMatchMetric` |
| `tests/evals/test_router_eval.py` | marked router evals | ✓ VERIFIED | `@pytest.mark.eval` |
| `tests/evals/test_taro_eval.py` | marked taro evals | ✓ VERIFIED | Mapping path |
| `tests/evals/goldens_*.json` | hand-curated goldens | ✓ VERIFIED | Not generated via deepeval |
| `pyproject.toml` | eval marker + addopts + deepeval | ✓ VERIFIED | `addopts = -m 'not eval'` |

### Key Link Verification

| From | To | Via | Status | Details |
| ---- | -- | --- | ------ | ------- |
| `server/app.py` | `server/observability.py` | build/metadata/flush | ✓ WIRED | Imports + stream config + finally flush |
| `router/taro/astro/node.py` | `RunnableConfig` | `ainvoke(..., config=config)` | ✓ WIRED | All three nodes pass config |
| `workflow.py` | `summarize_agent.ainvoke` | `config=config` | ✓ WIRED | `add_memory` |
| `cards/mapping.py` | `cards/node.py` | `spread_name` | ✓ WIRED | Unpack + state emit |
| `server/schemas.py` | `frontend/schema.py` | `ExtractData.spread_name` | ✓ WIRED | Field parity |
| `frontend/pages/app.py` | `templates.py` | `create_html_taro(cards, spread_name)` | ✓ WIRED | Session key + call site |
| `workflow.py` | `context_trust.py` | `wrap_untrusted_user_memory` | ✓ WIRED | `take_context` return |
| `routing.py` | `logger.warning` | `tool_iteration_cap_reached` | ✓ WIRED | Cap path only |
| `pyproject.toml` | `tests/evals/` | `not eval` addopts | ✓ WIRED | 10 eval tests deselected by default |
| `test_router_eval.py` | `metrics.py` / deepeval | `assert_test` | ✓ WIRED | ExactMatch metrics |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| -------- | ------------- | ------ | ------------------ | ------ |
| `cards/node.py` | `spread_name` | `extract_cards_from_messages` / MCP markdown parse | Yes (parsed header) | ✓ FLOWING |
| `frontend/pages/app.py` | `data.spread_name` → session → `create_html_taro` | Stream `ExtractData` JSON | Yes when cards present | ✓ FLOWING |
| `workflow.take_context` | `context` | Zep `get_user_context` or name-only fallback | Real or fallback string, always wrapped | ✓ FLOWING |
| `app.stream_agent` | Langfuse callbacks/metadata | Env keys → `build_langfuse_callbacks` | Empty list without keys; handler when present | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| Default unit suite green | `uv run pytest -q` | 67 passed, 10 deselected | ✓ PASS |
| No unlock symbols in `src/` | `rg unlock_card_agent\|UnlockCard\|unlock_name src/` | (none) | ✓ PASS |
| Cap + trust + Langfuse + schema tests | `uv run pytest -q tests/test_routing.py tests/test_context_trust.py tests/test_observability.py tests/test_langfuse_config_prop.py tests/test_spread_name_schema.py` | all passed | ✓ PASS |
| Eval suite offline | `uv run pytest -q -m eval` | 10 passed, 67 deselected | ✓ PASS |

### Probe Execution

| Probe | Command | Result | Status |
| ----- | ------- | ------ | ------ |
| — | — | No phase probes declared; not a migration/tooling probe phase | SKIP |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ---------- | ----------- | ------ | -------- |
| SC-11.1 | 11-02 | Dead unlock removed; `spread_name` E2E | ✓ SATISFIED | Code + grep + `test_spread_name_schema.py` |
| SC-11.2 | 11-03 | Explicit tool budget + log | ✓ SATISFIED | `routing.py` + README + `test_routing.py` |
| SC-11.3 | 11-03 | Trust-labeled Zep context | ✓ SATISFIED | `context_trust.py` + `take_context` wrap |
| SC-11.4 | 11-01 | Langfuse v4 + config prop tests | ✓ SATISFIED | observability + config-prop tests |
| SC-11.5 | 11-04 | Offline eval router + domain | ✓ SATISFIED | `tests/evals/` router+taro |
| SC-11.6 | 11-01, 11-04 | pytest green; no new required keys | ✓ SATISFIED | suite green; required_env unchanged |

No `.planning/REQUIREMENTS.md`; coverage mapped from ROADMAP SC-11.1–SC-11.6. No orphaned phase requirements found.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| `tests/evals/test_router_eval.py` | `run_router_with_mocks` | Mock pre-seeded with `expected_next_node` | ℹ️ Info | Harness + goldens + pass/fail criteria exist (SC-11.5); router cases validate plumbing more than live LLM routing quality. Taro evals exercise real MCP mapping. Acceptable for offline D-12 design. |
| — | — | No `TBD`/`FIXME`/`XXX` in phase-touched sources | — | Debt-marker gate clean |

### Human Verification Required

### 1. Frontend card title without unlock_name

**Test:** Complete a tarot reading in Streamlit after API returns cards + `spread_name`.  
**Expected:** Layout title shows the MCP-derived spread name; no leftover unlock naming or blank title from the deleted unlock path.  
**Why human:** Visual Streamlit rendering and session message replay are outside automated unit/eval coverage (`11-VALIDATION.md` manual-only).

### Gaps Summary

No automated gaps. All six roadmap success criteria are verified in the codebase. Phase status is `human_needed` solely for the Streamlit title visual check deferred by validation strategy.

**Confirmation-bias notes (non-blocking):** (1) Router DeepEval cases are mock-driven exact matches — intentional offline shape. (2) Trust wrap is unit-tested on the pure helper; `take_context` always-wrap is verified by code inspection of both try/except paths, not a dedicated integration test.

---

_Verified: 2026-07-19T23:42:48Z_  
_Verifier: Claude (gsd-verifier)_
