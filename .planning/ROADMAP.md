# Roadmap: AI-Taro Brownfield Hardening

## Overview

Harden the existing AI-Taro tarot assistant for portfolio and interview presentation.

## Phases

- [x] **Phase 1: Security** - Purge secrets, ship `.env.example`, protect `/stream`
- [x] **Phase 2: Bug Fixes** - Country field, bare except, star imports, draw_mermaid
- [x] **Phase 3: Test Foundation** - pytest suite locks router/memory/stream before refactor
- [x] **Phase 4: MCP Card Pipeline** - Cards from MCP ToolMessage; remove img_node LLM path
- [x] **Phase 5: Graph & Schema Cleanup** - Unified routing, dataclass Agents, single TaroCard
- [x] **Phase 6: Reliability** - Best-effort memory, LLM errors, retries, tool-loop caps
- [x] **Phase 7: Langfuse Observability** - SDK tracing, optional when keys absent
- [x] **Phase 8: README & Documentation** - Architecture diagram, stack, run instructions
- [x] **Phase 9: Backend Structure Refactor** - Split backend into agents + server; split graph by agent/subagent (completed 2026-07-19)
- [x] **Phase 10: Simple Startup** - One-command local run: deps, MCP build, env checks, backend + frontend (completed 2026-07-19)
- [ ] **Phase 11: Agent Harness Hardening** - Dead unlock agent, budgets, trust-labeled context, Langfuse v4, lightweight evals

## Progress

| Phase | Status | Completed |
|-------|--------|-----------|
| 1. Security | Complete | 2026-06-17 |
| 2. Bug Fixes | Complete | 2026-06-17 |
| 3. Test Foundation | Complete | 2026-06-17 |
| 4. MCP Card Pipeline | Complete | 2026-06-17 |
| 5. Graph & Schema Cleanup | Complete | 2026-06-17 |
| 6. Reliability | Complete | 2026-06-17 |
| 7. Langfuse Observability | Complete | 2026-06-17 |
| 8. README & Documentation | Complete | 2026-06-17 |
| 9. Backend Structure Refactor | Complete | 2026-07-19 |
| 10. Simple Startup | Complete — ready for verification | 2026-07-20 |
| 11. Agent Harness Hardening | In Progress — 2/4 plans | - |

### Phase 9: Backend Structure Refactor

**Goal:** Restructure `src/backend` so HTTP/server concerns are separated from agent orchestration, and the LangGraph workflow is split into clear per-agent (and subagent) modules instead of monolithic files.

**Requirements:** SC-01, SC-02, SC-03, SC-04

**Depends on:** Phase 8

**Success Criteria** (what must be TRUE):

  1. Backend has a clear `server` package (FastAPI app, auth, stream schemas, observability) separate from agent/graph code
  2. Agent/graph code lives under an `agents` (or equivalent) package, not mixed with HTTP entrypoints
  3. Graph is split into modules/folders by agent and subagent (router, taro, astro, memory, card mapping, routing) — not one large `nodes.py` / `agent.py`
  4. Public imports and `pytest -q` stay green after the move; behavior unchanged

**Plans:** 6/6 plans complete

Plans:

- [x] 09-01-PLAN.md — Agents foundation (models, state, routing, config, cards mapping)
- [x] 09-02-PLAN.md — Per-agent router/taro/astro factories (MCP ../../../)
- [x] 09-03-PLAN.md — Memory/cards factories + create_agents aggregator
- [x] 09-04-PLAN.md — Workflow nodes + setup_workflow public export
- [x] 09-05-PLAN.md — Server package + README uvicorn server.app:app
- [x] 09-06-PLAN.md — Hard-cut tests, delete legacy graph/flat modules, grep gates

### Phase 10: Simple Startup

**Goal:** Make local development start with a single documented path — install deps, build tarot MCP, validate required env vars, run backend and frontend without `PYTHONPATH` gymnastics or opaque startup failures.

**Requirements:** SC-10.1, SC-10.2, SC-10.3, SC-10.4, SC-10.5, SC-10.6

**Depends on:** Phase 9

**Success Criteria** (what must be TRUE):

  1. A root script or documented one-liner installs Python deps (`uv sync`), builds tarot MCP (`npm run build` including card-data), and prints clear next steps
  2. Backend starts with `uv run` / script from repo root without manual `PYTHONPATH=src/backend` (packaging or wrapper handles it)
  3. Missing required env (`OPENAI_API_KEY`, `ZEP_API`, `STREAM_API_KEY`, …) fails fast with actionable messages before MCP/LLM init
  4. Missing tarot MCP dist fails with the exact build command (already partial — keep/improve)
  5. README Quick start is ≤5 steps and matches the scripts that actually work
  6. `pytest -q` still green

**Plans:** 3/3 plans complete

Plans:

**Wave 1**

- [x] 10-01-PLAN.md — Wave 0: setuptools scripts packaging, required_env helper, Nyquist tests

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 10-02-PLAN.md — aitaro-setup npm + checklist; factory aitaro-setup message
- [x] 10-03-PLAN.md — aitaro-api uvicorn wrapper, lifespan fail-fast, README 4 steps

**Cross-cutting constraints:**

- Required env (`STREAM_API_KEY`, `OPENAI_API_KEY`, `ZEP_API`) fail-fast in setup and lifespan before MCP/LLM init
- No manual `PYTHONPATH`; canonical path is `uv run aitaro-api`
- `pytest -q` stays green; pytest pythonpath unchanged

### Phase 11: Agent Harness Hardening

**Goal:** Harden the AiTaro agent harness per provider-neutral best practices: remove dead agent surface, make tool/step budgets explicit, label untrusted memory context, verify Langfuse v4 tracing reaches agents, and add a small eval/regression harness beyond unit mocks.

**Requirements:** SC-11.1, SC-11.2, SC-11.3, SC-11.4, SC-11.5, SC-11.6

**Depends on:** Phase 10

**Success Criteria** (what must be TRUE):

  1. Dead `unlock_card_agent` is removed from factories/state (or wired with a clear use path — prefer remove if unused after Phase 4)
  2. Tool/step budgets are explicit, documented, and enforceable (beyond silent `MAX_TOOL_ITERATIONS`)
  3. Zep/user memory context is trust-labeled as untrusted data in agent prompts/context assembly
  4. Langfuse v4 CallbackHandler + config propagation to router/taro/astro/summarize is verified by tests; optional when keys absent
  5. A lightweight eval harness exists (fixture scenarios + pass/fail criteria) for at least router + one domain agent path
  6. `pytest -q` stays green; no new required env keys beyond existing optional Langfuse

**Plans:** 2/4 plans executed

Plans:

**Wave 1**

- [x] 11-01-PLAN.md — Land Langfuse v4 wiring + config-prop tests (D-10, D-11)

**Wave 2** *(blocked on Wave 1)*

- [x] 11-02-PLAN.md — Hard-delete unlock agent; rename unlock_name → spread_name E2E (D-01–D-03)

**Wave 3** *(blocked on Waves 1–2)*

- [ ] 11-03-PLAN.md — Tool-cap structured logging + trust-label take_context (D-04–D-09)

**Wave 4** *(blocked on Waves 2–3; human deepeval legitimacy gate)*

- [ ] 11-04-PLAN.md — Offline DeepEval router+taro suite behind eval marker (D-12, D-13)

**Cross-cutting constraints:**

- Langfuse keys remain optional; no Confident AI; no live Langfuse gate
- Default `pytest -q` excludes `@pytest.mark.eval`
- Astro removal / token budgets deferred
