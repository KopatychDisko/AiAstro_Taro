---
phase: 09-backend-structure-refactor
verified: 2026-07-19T21:47:11Z
status: passed
score: 7/7 must-haves verified
overrides_applied: 0
re_verification: false
---

# Phase 9: Backend Structure Refactor Verification Report

**Phase Goal:** Restructure `src/backend` so HTTP/server concerns are separated from agent orchestration, and the LangGraph workflow is split into clear per-agent (and subagent) modules instead of monolithic files.

**Verified:** 2026-07-19T21:47:11Z
**Status:** passed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
| --- | ------- | ---------- | -------------- |
| 1 | SC-01: Clear `server` package (FastAPI app, auth, stream schemas, observability) separate from agent code | ✓ VERIFIED | `src/backend/server/{app,auth,schemas,observability}.py` exist; only `agents/` + `server/` under `src/backend/` |
| 2 | SC-02: Agent/graph code under `agents/`; no HTTP entrypoints in agents | ✓ VERIFIED | `agents/` has workflow, factories, per-agent packages; `rg` for fastapi/HTTPException/Depends in `agents/` = 0; agents never imports `server` |
| 3 | SC-03: Graph split by agent/subagent (router, taro, astro, memory, cards, routing) | ✓ VERIFIED | Packages `agents/{router,taro,astro,memory,cards}/` with factory/node/prompt (as applicable); `agents/routing.py`, `agents/cards/mapping.py`; no monolithic `nodes.py`/`agent.py` |
| 4 | SC-04: Public imports + `pytest -q` green; behavior unchanged | ✓ VERIFIED | `.venv/bin/python -m pytest -q` → **13 passed** in 0.46s; tests import `server.*` / `agents.*` only |
| 5 | D-01/D-04: No top-level `graph/`; hard cut of flat root modules; no re-export shims | ✓ VERIFIED | `test ! -e src/backend/graph`; no `app.py`/`auth.py`/`models.py`/`schemas.py`/`observability.py` at backend root; grep gate empty under `src/backend` `tests` `README.md` |
| 6 | D-03: README documents `uvicorn server.app:app` | ✓ VERIFIED | `README.md` lines 82 & 88 use `uvicorn server.app:app`; no `uvicorn app:app` |
| 7 | Auth still on `/stream` (`test_stream_endpoint`, compare_digest, fail-closed) | ✓ VERIFIED | `server/app.py` `Depends(verify_stream_api_key)`; `server/auth.py` uses `secrets.compare_digest` + 500 if key unset; `tests/test_stream_endpoint.py` 200 + 401 cases pass |

**Score:** 7/7 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | -------- | ------ | ------- |
| `src/backend/server/app.py` | FastAPI + `/stream` + lifespan | ✓ VERIFIED | WIRED: `from agents import setup_workflow`, `Depends(verify_stream_api_key)` |
| `src/backend/server/auth.py` | `verify_stream_api_key` + compare_digest | ✓ VERIFIED | Substantive fail-closed auth |
| `src/backend/server/schemas.py` | `ExtractData`/`UserData`; `TaroCard` from agents | ✓ VERIFIED | `from agents.models import TaroCard` |
| `src/backend/server/observability.py` | Langfuse callbacks | ✓ VERIFIED | Optional when keys absent |
| `src/backend/agents/__init__.py` | Exports `setup_workflow` | ✓ VERIFIED | `__all__ = ["setup_workflow"]` |
| `src/backend/agents/workflow.py` | `setup_workflow` graph compile | ✓ VERIFIED | Wires router/taro/astro/cards nodes + memory |
| `src/backend/agents/factories.py` | `create_agents` aggregator | ✓ VERIFIED | Imports router/taro/astro/memory/cards factories |
| `src/backend/agents/models.py` | `TaroCard` | ✓ VERIFIED | Domain model |
| `src/backend/agents/routing.py` | `capped_tools_condition` | ✓ VERIFIED | Used by workflow |
| `src/backend/agents/cards/mapping.py` | MCP card extraction | ✓ VERIFIED | Used by `cards/node.py` |
| `src/backend/agents/{router,taro,astro,memory,cards}/` | Per-agent modules | ✓ VERIFIED | factory/node/prompt/tools as designed |
| `README.md` | `uvicorn server.app:app` | ✓ VERIFIED | Entrypoint updated |
| `src/backend/graph/` | Must NOT exist | ✓ VERIFIED | Absent |
| Flat `src/backend/{app,auth,models,schemas,observability}.py` | Must NOT exist | ✓ VERIFIED | Absent |

### Key Link Verification

| From | To | Via | Status | Details |
| ---- | -- | --- | ------ | ------- |
| `server/app.py` | `agents.setup_workflow` | `from agents import setup_workflow` | ✓ WIRED | Lifespan assigns `workflow = await setup_workflow()` |
| `server/app.py` | `server.auth` | `Depends(verify_stream_api_key)` | ✓ WIRED | On `/stream` |
| `server/schemas.py` | `agents.models.TaroCard` | import | ✓ WIRED | One-way server→agents |
| `agents/workflow.py` | per-agent nodes | `create_*_node` / `img_node` | ✓ WIRED | Graph edges registered |
| `agents/factories.py` | per-agent factories | `create_*_agent` | ✓ WIRED | Aggregator returns `Agents` |
| `tests/test_router.py` | `agents.workflow` | patch `agents.workflow.create_agents` | ✓ WIRED | Also patches `AsyncZep` |
| `tests/test_stream_endpoint.py` | `server.auth` / `server.schemas` | imports | ✓ WIRED | Auth dependency on test app |
| `agents/*` → `server/*` | — | must be absent | ✓ WIRED (boundary) | No `from server` / `import server` in agents |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| -------- | ------------- | ------ | ------------------ | ------ |
| `server/app.py` `/stream` | `workflow` / stream chunks | `setup_workflow()` → LangGraph `astream` | Real graph when env available; tests mock stream | ✓ FLOWING |
| `agents/cards/node.py` | `taro_cards` | `extract_cards_from_messages(state["messages"])` | Parses ToolMessage content (not hardcoded empty) | ✓ FLOWING |
| `server/schemas.ExtractData` | response schema | Validated from graph chunk | Real pydantic model | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| Full suite green (SC-04) | `.venv/bin/python -m pytest -q` | 13 passed, 1 warning, 0.46s | ✓ PASS |
| Stream auth tests | `.venv/bin/python -m pytest tests/test_stream_endpoint.py -q` | 2 passed | ✓ PASS |
| Legacy import grep gate | `rg -n "from graph\\.|import graph|from auth import|from schemas import|from models import|from observability import|uvicorn app:app" src/backend tests README.md` | 0 matches | ✓ PASS |
| No `graph/` / flat roots | `test ! -e src/backend/graph`; flat files absent | Confirmed | ✓ PASS |
| README entrypoint | `rg "uvicorn server.app:app" README.md` | 2 hits | ✓ PASS |

### Probe Execution

| Probe | Command | Result | Status |
| ----- | ------- | ------ | ------ |
| — | — | No phase-declared `scripts/*/tests/probe-*.sh` | SKIPPED |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ---------- | ----------- | ------ | -------- |
| SC-01 | 09-05, 09-06 | Clear `server` package | ✓ SATISFIED | `server/` package complete |
| SC-02 | 09-01, 09-04, 09-06 | Agents package, no HTTP mix | ✓ SATISFIED | `agents/` + boundary greps |
| SC-03 | 09-02, 09-03, 09-04 | Per-agent module split | ✓ SATISFIED | router/taro/astro/memory/cards |
| SC-04 | 09-06 | pytest green after move | ✓ SATISFIED | 13 passed |
| D-01 | CONTEXT | `server/` + `agents/`, no top-level `graph/` | ✓ SATISFIED | Layout confirmed |
| D-02 | CONTEXT | Strict HTTP vs agents boundary | ✓ SATISFIED | One-way imports; no HTTP in agents |
| D-03 | CONTEXT | `uvicorn server.app:app` in README | ✓ SATISFIED | README updated |
| D-04 | CONTEXT | Hard cut; no shims | ✓ SATISFIED | Legacy paths deleted; grep gate clean |

No `.planning/REQUIREMENTS.md` — requirements are SC/D IDs from ROADMAP + CONTEXT.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| `agents/*/prompt.py` | — | `MessagesPlaceholder` | ℹ️ Info | LangChain API name, not a stub marker |
| `server/schemas.py` | Config | Pydantic v1 `class Config` | ℹ️ Info | Deprecation warning in pytest; pre-existing style, not a phase gap |

No `TBD`/`FIXME`/`XXX` debt markers in phase-modified backend code.

### Human Verification Required

None required for phase goal. Roadmap SCs and D-01–D-04 are satisfied by code structure, import gates, and pytest.

Optional ops smoke (out of band; needs env + MCP build): `cd src/backend && PYTHONPATH=. uvicorn server.app:app --port 8000` — not a must-have truth for this refactor phase.

### Gaps Summary

No gaps. Phase goal achieved: backend is split into `server/` + `agents/`, graph is per-agent modular, legacy flat/`graph/` paths removed, README entrypoint updated, stream auth preserved, full pytest suite green.

---

_Verified: 2026-07-19T21:47:11Z_
_Verifier: Claude (gsd-verifier)_
