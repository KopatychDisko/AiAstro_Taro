---
phase: 06-reliability
status: complete
---

# Phase 6: Reliability — Complete

## REL-01 — Best-effort memory

- Already implemented in Phase 3 (`add_memory` try/except)

## REL-02 — Stream error chunks

- `stream_agent` catches exceptions and yields `ExtractData` with `next_node='END'` and user-facing error message

## REL-03 — LLM retries

- `.with_retry(stop_after_attempt=2)` on router, unlock, and summarize agents

## REL-04 — Tool loop caps

- `graph/routing.py` — `capped_tools_condition` stops after 3 tool iterations
- `tool_iterations` field on `AgentState`
- `tests/test_routing.py`
