# Phase 10: Simple Startup - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-07-20
**Phase:** 10-simple-startup
**Areas discussed:** Launch surface, PYTHONPATH / packaging, Env fail-fast, Frontend in setup

---

## Launch surface

| Question | Selected |
|----------|----------|
| Day-to-day mechanism | uv `[project.scripts]` (`aitaro-setup`, `aitaro-api`) |
| Setup scope | MCP build + env checklist (no `uv sync`) |
| Runtime commands | API only (`aitaro-api`) |
| Port/reload | Defaults `--reload --port 8000` |

## PYTHONPATH / packaging

| Question | Selected |
|----------|----------|
| How to drop PYTHONPATH | Wrapper only (no editable package) |
| Entrypoint location | `scripts/` |
| pytest pythonpath | Leave unchanged |
| Document raw uvicorn | No — canonical `uv run aitaro-api` only |

## Env fail-fast

| Question | Selected |
|----------|----------|
| Required keys | `STREAM_API_KEY`, `OPENAI_API_KEY`, `ZEP_API` |
| When to check | Both setup and lifespan |
| Error format | Compact missing list + `.env.example` hint |
| Optional keys | Do not check/warn (Langfuse etc.) |

## Frontend in setup

| Question | Selected |
|----------|----------|
| Setup vs UI | Print checklist + Streamlit command; do not start UI |
| Postgres | Do not validate |
| Streamlit entry | `login_menu.py` |
| README steps | 4 steps + one UI line |

## Claude's Discretion

- Minimal packaging metadata for console scripts
- Shared env-check helper
- Setup stdout wording

## Deferred Ideas

- `aitaro-ui` entrypoint
- Editable package layout
- Uvicorn argv pass-through
