# Phase 1: Security - Context

**Gathered:** 2026-06-17
**Status:** Ready for planning
**Mode:** Auto-generated (autonomous smart discuss — recommendations auto-accepted)

<domain>
## Phase Boundary

Harden repository and streaming API for public portfolio use: purge tracked `.env` and git history, ship `.env.example`, eliminate hardcoded secrets, and protect `POST /stream` with API key authentication.

</domain>

<decisions>
## Implementation Decisions

### Git History & Secrets Purge
- Use `git filter-repo --path .env --invert-paths` to purge `.env` from all history
- Keep local `.env` on disk after untracking (do not delete developer copy)
- Document force-push and collaborator re-clone steps in `docs/security-git-history-purge.md`
- Plan 01-01 is `autonomous: false` — checkpoint before force-push

### Environment Variable Contract
- Ship `.env.example` with every required key and empty placeholder values
- Keys must include: `OPENAI_API_KEY`, `HUGGINGFACEHUB_API_TOKEN`, `QDRANT_API_KEY`, `QDRANT_URL`, `ZEP_API`, `POSTGRESQL_*`, `STREAM_API_KEY`, `LANGFUSE_*` (when referenced in code)
- Add `scripts/scan-secrets.sh` for repeatable grep-based secret pattern scan

### Stream API Authentication
- Shared-secret API key via `X-API-Key` header on `POST /stream`
- Backend: FastAPI dependency `verify_stream_api_key` (async) raises HTTP 401 on missing/wrong key
- Frontend: Streamlit `httpx` client sends `X-API-Key` from `STREAM_API_KEY` env on every stream request
- Load `STREAM_API_KEY` via `os.getenv()` on both backend and frontend — no hardcoded values

### Claude's Discretion
- Exact grep patterns for secret scan script
- Whether to also accept `Authorization: Bearer` header as alternate (optional — X-API-Key is primary)

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/backend/app.py` — `/stream` endpoint (currently unauthenticated)
- `src/backend/graph/agents/config/config.py` — env var loading pattern via `os.getenv()`
- `src/frontend/pages/app.py` — httpx stream client to `http://127.0.0.1:8000/stream`

### Established Patterns
- Secrets loaded via `os.getenv()` / `os.environ` in config modules
- `.env` is currently tracked in git index (`git ls-files .env` returns match)

### Integration Points
- Backend FastAPI app mounts `/stream` POST handler
- Frontend Streamlit chat page calls backend stream endpoint

</code_context>

<specifics>
## Specific Ideas

- Match ТЗ: `.env` never in git; only `.env.example` with empty values
- Portfolio-safe: repo must be showable without credential leakage

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>
