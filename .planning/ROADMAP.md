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
- [ ] **Phase 9: Backend Structure Refactor** - Split backend into agents + server; split graph by agent/subagent

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
| 9. Backend Structure Refactor | In Progress | - |

### Phase 9: Backend Structure Refactor

**Goal:** Restructure `src/backend` so HTTP/server concerns are separated from agent orchestration, and the LangGraph workflow is split into clear per-agent (and subagent) modules instead of monolithic files.

**Requirements:** SC-01, SC-02, SC-03, SC-04

**Depends on:** Phase 8

**Success Criteria** (what must be TRUE):

  1. Backend has a clear `server` package (FastAPI app, auth, stream schemas, observability) separate from agent/graph code
  2. Agent/graph code lives under an `agents` (or equivalent) package, not mixed with HTTP entrypoints
  3. Graph is split into modules/folders by agent and subagent (router, taro, astro, memory, card mapping, routing) — not one large `nodes.py` / `agent.py`
  4. Public imports and `pytest -q` stay green after the move; behavior unchanged

**Plans:** 5/6 plans executed

Plans:

- [x] 09-01-PLAN.md — Agents foundation (models, state, routing, config, cards mapping)
- [x] 09-02-PLAN.md — Per-agent router/taro/astro factories (MCP ../../../)
- [x] 09-03-PLAN.md — Memory/cards factories + create_agents aggregator
- [x] 09-04-PLAN.md — Workflow nodes + setup_workflow public export
- [x] 09-05-PLAN.md — Server package + README uvicorn server.app:app
- [ ] 09-06-PLAN.md — Hard-cut tests, delete legacy graph/flat modules, grep gates
