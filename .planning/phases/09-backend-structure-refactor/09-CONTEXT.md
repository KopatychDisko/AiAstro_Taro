# Phase 9: Backend Structure Refactor - Context

**Gathered:** 2026-07-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Restructure `src/backend` into two top-level packages — `server/` (HTTP/FastAPI) and `agents/` (LangGraph + LLM agents) — and split the graph into per-agent modules. Behavior must stay unchanged; `pytest -q` stays green. No new product features.

</domain>

<decisions>
## Implementation Decisions

### Top-level package split
- **D-01:** Use `src/backend/server/` and `src/backend/agents/` — do **not** keep a separate top-level `graph/` package (current `graph/` content moves under `agents/`).
- **D-02:** Strict boundary: `server/` = HTTP only (`app`, `auth`, observability, stream request/response schemas like `ExtractData`/`UserData`). Agent orchestration, LLM factories, prompts, routing, card mapping, and shared domain models used by the graph (`TaroCard`, `AgentState`, etc.) live under `agents/`. Server may import from `agents` for types needed by the API; agent code must not own HTTP entrypoints.
- **D-03:** Entrypoint after move is `uvicorn server.app:app` (run from `src/backend` with existing `pythonpath`). Update README accordingly. No root `app.py` compatibility shim.
- **D-04:** Hard cut in this phase — delete old flat modules (`app.py`, `auth.py`, `graph/`, etc.) after the move; rewrite tests and imports to `server.*` / `agents.*`. No deprecation re-export layer.

### Claude's Discretion
- Exact folder layout **inside** `agents/` (per-agent folders vs files) — not discussed; planner/researcher may propose a clear split by router/taro/astro/memory/card mapping as long as D-01–D-04 hold.
- Whether `ExtractData` stays in `server/schemas.py` vs a thin re-export of card types from `agents` — implement the strict boundary without unnecessary duplication.
- How to update `pytest` `pythonpath` / import paths with minimal churn.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase / roadmap
- `.planning/ROADMAP.md` — Phase 9 goal and success criteria
- `.planning/STATE.md` — current milestone state

### Current backend (pre-refactor)
- `src/backend/app.py` — FastAPI lifespan + `/stream`
- `src/backend/auth.py` — stream API key dependency
- `src/backend/observability.py` — Langfuse callbacks
- `src/backend/schemas.py` — `ExtractData`, `UserData`
- `src/backend/models.py` — shared `TaroCard`
- `src/backend/graph/nodes.py` — `setup_workflow` (monolithic nodes)
- `src/backend/graph/routing.py` — tool-loop caps
- `src/backend/graph/taro_card_mapping.py` — MCP card parsing
- `src/backend/graph/agents/agent.py` — agent factories
- `src/backend/graph/agents/prompt.py` — prompts (monolithic)
- `src/backend/graph/agents/schemas.py` — `AgentState`, `Agents`, router outputs

### Docs / tests
- `README.md` — run instructions (must update entrypoint)
- `tests/` — import from `graph.*`, `auth`, `schemas`, `models`, `observability`
- `pyproject.toml` — `pythonpath = ["src/backend"]`

No external ADRs — requirements fully captured in decisions above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `setup_workflow()` in `graph/nodes.py` — public compile entry; must remain reachable from `server.app` after move
- `create_agents()` / `Agents` dataclass — factory container for all chains
- `build_langfuse_callbacks()` — stays in server observability module
- `verify_stream_api_key` — stays in server auth

### Established Patterns
- Flat imports under `src/backend` via pytest `pythonpath` (no installable package name)
- Graph package exports only `setup_workflow` from `__init__.py`
- Agents nested today as `graph.agents.*` — target is top-level `agents.*`

### Integration Points
- Frontend calls `http://127.0.0.1:8000/stream` — unchanged if uvicorn still binds same app
- Tests patch `graph.nodes.create_agents` / `AsyncZep` — paths must be updated after move
- MCP paths in `agent.py` are relative to file location — verify after relocating factories

</code_context>

<specifics>
## Specific Ideas

- User wants the backend split to match the mental model: **agents** vs **server**, not “graph under agents under graph”.
- Explicit `server.app:app` is preferred over keeping legacy `uvicorn app:app`.

</specifics>

<deferred>
## Deferred Ideas

- Fine-grained per-agent folder layout inside `agents/` was not discussed in this session — left to Claude's discretion / planning.
- Frontend `TaroCard` dedup (v2 FE-02) stays out of scope.

None other — discussion stayed within phase scope.

</deferred>

---

*Phase: 09-backend-structure-refactor*
*Context gathered: 2026-07-19*
