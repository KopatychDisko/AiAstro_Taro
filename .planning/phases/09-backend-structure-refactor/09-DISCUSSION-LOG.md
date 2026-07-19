# Phase 9: Backend Structure Refactor - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-07-19
**Phase:** 09-backend-structure-refactor
**Areas discussed:** Top-level split

---

## Top-level split

### Q1 — Package layout under `src/backend`

| Option | Description | Selected |
|--------|-------------|----------|
| `server/` + `agents/` | HTTP in server; graph+LLM in agents (no separate graph/) | ✓ |
| `server/` + `graph/` | HTTP in server; keep agent logic under graph/ | |
| You decide | Claude picks | |

**User's choice:** `server/` + `agents/`

### Q2 — Boundary for root modules / shared models

| Option | Description | Selected |
|--------|-------------|----------|
| Strict | server=HTTP only; TaroCard/AgentState under agents | ✓ |
| Shared root | models stay at backend root / shared/ | |
| You decide | Claude picks | |

**User's choice:** Strict separation

### Q3 — Uvicorn entrypoint

| Option | Description | Selected |
|--------|-------------|----------|
| `server.app:app` | Explicit new path; update README | ✓ |
| Root shim | Keep `uvicorn app:app` via re-export | |
| You decide | Claude picks | |

**User's choice:** `server.app:app`

### Q4 — Old module paths

| Option | Description | Selected |
|--------|-------------|----------|
| Hard cut | Delete old modules; rewrite imports/tests | ✓ |
| Deprecation shims | Thin re-exports for one phase | |
| You decide | Claude picks | |

**User's choice:** Hard cut

---

## Claude's Discretion

- Internal layout of `agents/` (per-agent folders vs files)
- Exact placement of stream schemas vs agent types without violating D-02
- Minimal pytest import churn strategy

## Deferred Ideas

- Per-agent graph granularity discussion (user declined further gray areas this session)
