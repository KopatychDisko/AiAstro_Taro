---
status: testing
phase: 10-simple-startup
source: [10-VERIFICATION.md]
started: 2026-07-19T22:32:02Z
updated: 2026-07-19T22:34:13Z
---

## Current Test

number: 2
name: Setup stdout checklist copy
expected: |
  MCP OK, required-env OK for three keys, uv run aitaro-api next step, Streamlit login_menu.py hint, Postgres reminder without hard-fail
awaiting: user response

## Tests

### 1. Live aitaro-setup then aitaro-api smoke
expected: Setup builds MCP and prints checklist; API binds 127.0.0.1:8000; /stream accepts X-API-Key
why_human: Needs real .env secrets, npm build, and a bound port — unit tests mock subprocess/uvicorn/lifespan
result: blocked
blocked_by: other
reason: "Lifespan RuntimeError: Missing STREAM_API_KEY. .env has OPENAI_API_KEY and ZEP_API but no STREAM_API_KEY. Also started via old PYTHONPATH=src/backend uvicorn from src/backend instead of uv run aitaro-api from repo root."
status: blocked

### 2. Setup stdout checklist copy
expected: MCP OK, required-env OK for three keys, uv run aitaro-api next step, Streamlit login_menu.py hint, Postgres reminder without hard-fail
why_human: Human-readable copy quality beyond unit string asserts
status: pending

## Summary

total: 2
passed: 0
failed: 0
blocked: 1
pending: 1
