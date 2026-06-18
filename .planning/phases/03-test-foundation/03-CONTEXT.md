# Phase 3: Test Foundation - Context

**Gathered:** 2026-06-17
**Status:** Ready for execution
**Mode:** Auto-generated (autonomous — yolo)

<domain>
## Phase Boundary

pytest suite with mocked externals locks router, memory, card mapping, and stream behavior before architectural changes in Phase 4+.

</domain>

<decisions>
## Implementation Decisions

### Test layout
- `tests/` at repo root; `pythonpath` includes `src/backend`
- `pytest-asyncio` with `asyncio_mode = auto`
- Dev deps in `[dependency-groups] dev`

### Mocking strategy
- Patch `create_agents` and `AsyncZep` for graph tests — no live MCP/Zep
- Stream tests use isolated FastAPI app with mocked `stream_agent`
- Card mapping tested via pure `map_mcp_tool_cards` helper (Phase 4 will wire to MCP)

### Claude's Discretion
- Exact mock fixture structure in `tests/conftest.py`

</decisions>
