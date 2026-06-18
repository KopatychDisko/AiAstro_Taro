---
phase: 01-security
plan: 03
subsystem: auth
tags: [fastapi, api-key, stream]

requires:
  - phase: 01-02
    provides: STREAM_API_KEY in .env.example
provides:
  - src/backend/auth.py verify_stream_api_key
  - Protected POST /stream
  - Frontend X-API-Key header
affects: [phase-03-test-stream]

tech-stack:
  added: []
  patterns: [FastAPI Depends + secrets.compare_digest]

key-files:
  created: [src/backend/auth.py]
  modified: [src/backend/app.py, src/frontend/pages/app.py, src/backend/graph/agents/config/config.py]

key-decisions:
  - "X-API-Key header primary; Authorization Bearer also accepted"
  - "HTTP 500 if STREAM_API_KEY unset (fail closed)"

patterns-established:
  - "Stream auth: shared secret via env on backend and frontend"

status: complete
---

# Plan 01-03 Summary: Stream API Key Auth

## Completed

- `src/backend/auth.py` — async `verify_stream_api_key` with `secrets.compare_digest`
- `src/backend/app.py` — `Depends(verify_stream_api_key)` on `/stream`
- `src/frontend/pages/app.py` — sends `X-API-Key` from `STREAM_API_KEY` env
- `stream_api_key` added to `config.py`
- Dependency unit test passes (401 missing/wrong, pass correct key)
- `scripts/scan-secrets.sh` passes after auth wiring

## Curl replay (when server running with STREAM_API_KEY set)

```bash
# Expect 401
curl -s -o /dev/null -w '%{http_code}' -X POST http://127.0.0.1:8000/stream \
  -H 'Content-Type: application/json' \
  -d '{"message":"hi","user_id":"1","country":"x","city":"x","birth_day":"1","time_birth":"1","name":"n"}'

# Expect non-401 with valid key
curl -s -o /dev/null -w '%{http_code}' -X POST http://127.0.0.1:8000/stream \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $STREAM_API_KEY" \
  -d '{"message":"hi","user_id":"1","country":"x","city":"x","birth_day":"1","time_birth":"1","name":"n"}'
```

## Note

Add `STREAM_API_KEY=your-local-key` to `.env` for Streamlit ↔ FastAPI local dev.
