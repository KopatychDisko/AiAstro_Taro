# Phase 10: Simple Startup - Context

**Gathered:** 2026-07-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Make local development start with a single documented path: required env validated early, tarot MCP built via a setup entrypoint, backend started via `uv run aitaro-api` without manual `PYTHONPATH`. Frontend remains documented separately (Streamlit `login_menu.py`). No new product features; `pytest -q` stays green.

</domain>

<decisions>
## Implementation Decisions

### Launch surface
- **D-01:** Use `[project.scripts]` / `uv run` entrypoints — at least `aitaro-setup` and `aitaro-api` (not ad-hoc shell-only as the primary path).
- **D-02:** `aitaro-setup` does MCP build (`npm install`/`npm run build` in `src/tarotmcp`) + env checklist only — does **not** run `uv sync`.
- **D-03:** Runtime entrypoint is **API only** (`aitaro-api`). No `aitaro-ui` entrypoint in this phase; Streamlit stays as a documented separate command.
- **D-04:** `aitaro-api` uses fixed defaults: uvicorn `--reload --port 8000` (no argv pass-through required).

### PYTHONPATH / packaging
- **D-05:** Remove manual `PYTHONPATH=src/backend` via a **wrapper only** — entrypoint sets path/`sys.path` to `src/backend`. Do **not** convert to an editable installable package layout in this phase.
- **D-06:** Entrypoint modules live under repo-root `scripts/` (e.g. `scripts/aitaro_api.py`, `scripts/aitaro_setup.py`) registered in `pyproject.toml` `[project.scripts]`.
- **D-07:** Leave pytest `[tool.pytest.ini_options] pythonpath` unchanged (keep working `src/backend` / repo-root config as-is).
- **D-08:** README Quick start must **not** document raw `PYTHONPATH=… uvicorn …` — canonical path is `uv run aitaro-api` only.

### Env fail-fast
- **D-09:** Required backend env: `STREAM_API_KEY`, `OPENAI_API_KEY`, `ZEP_API`.
- **D-10:** Validate in **both** places: `aitaro-setup` checklist and FastAPI lifespan (before `setup_workflow()` / MCP init). Missing vars → non-zero exit / startup failure.
- **D-11:** Error format: compact list of missing keys + hint to copy `.env.example` → `.env`.
- **D-12:** Langfuse / Qdrant / HuggingFace / other optional keys are **not** checked and not warned in fail-fast.

### Frontend in setup
- **D-13:** Setup does not start Streamlit; it prints a short checklist including the Streamlit command.
- **D-14:** Do **not** validate `POSTGRESQL_*` in setup — only a text reminder that UI needs them.
- **D-15:** Canonical Streamlit entry remains `login_menu.py` (from `src/frontend`).
- **D-16:** README Quick start is **4 steps**: `.env` → `uv sync` → `uv run aitaro-setup` → `uv run aitaro-api`, plus one line for UI.

### Claude's Discretion
- Exact Python packaging metadata to expose `scripts/` as console scripts under uv (setuptools vs hatchling) — pick the smallest change that makes `uv run aitaro-api` work.
- Whether env check is a shared helper module imported by both setup and lifespan.
- Wording of setup stdout checklist.
- Keeping existing tarot MCP missing-dist `FileNotFoundError` message aligned with `aitaro-setup`.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase / roadmap
- `.planning/ROADMAP.md` — Phase 10 goal and success criteria
- `.planning/STATE.md` — current state / notes on PYTHONPATH friction

### Startup-related code & docs
- `README.md` — Quick start (must shrink to 4 steps + UI line)
- `.env.example` — required vs optional keys
- `pyproject.toml` — add `[project.scripts]`; pytest pythonpath stays
- `src/backend/server/app.py` — lifespan; inject env fail-fast before `setup_workflow`
- `src/backend/agents/taro/factory.py` — existing MCP missing-build error
- `src/tarotmcp/package.json` — build copies `card-data.json`
- `src/frontend/login_menu.py` — Streamlit entry for checklist/README

No external ADRs — decisions fully captured above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `server.app:app` — FastAPI application to target from `aitaro-api`
- Tarot MCP build script already copies `card-data.json`
- Astro MCP optional at factory (deferred v2)
- `psycopg2-binary` already allows `uv sync` without `pg_config`

### Established Patterns
- Flat imports under `PYTHONPATH=src/backend` (`server.*`, `agents.*`)
- pytest uses `pythonpath = ["src/backend"]` (and possibly repo root) — do not break
- Auth already fails closed when `STREAM_API_KEY` unset (may return 500 today) — unify with D-09/D-10 messaging

### Integration Points
- Frontend calls `http://127.0.0.1:8000/stream` with `X-API-Key`
- Streamlit needs Postgres separately — out of hard fail for backend setup

</code_context>

<specifics>
## Specific Ideas

- User wants `uv run aitaro-api` as the daily command, not PYTHONPATH one-liners.
- Setup must not own `uv sync` (user runs that once).
- Backend must start without Postgres; UI is optional reminder only.

</specifics>

<deferred>
## Deferred Ideas

- `aitaro-ui` Streamlit entrypoint — explicitly out for this phase (D-03).
- Editable installable package layout for `server`/`agents` — deferred (D-05).
- Pass-through uvicorn CLI flags — deferred (D-04).

None other — discussion stayed within phase scope.

</deferred>

---

*Phase: 10-simple-startup*
*Context gathered: 2026-07-20*
