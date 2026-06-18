---
phase: 03-test-foundation
status: complete
---

# Phase 3: Test Foundation — Complete

## Delivered (TEST-01 through TEST-06)

| Req | Test file | Coverage |
|-----|-----------|----------|
| TEST-01 | `pyproject.toml` `[tool.pytest.ini_options]` | `pythonpath = ["src/backend"]`, `tests/` layout |
| TEST-02 | `tests/test_router.py` | Mocked router → taro/astro/add_memory `next_node` |
| TEST-03 | `tests/test_memory_tools.py` | Mocked Zep `search_facts` / `search_nodes` with limit |
| TEST-04 | `tests/test_taro_cards.py` | MCP payload → `List[TaroCard]` mapping |
| TEST-05 | `tests/test_add_memory_resilience.py` | Zep write failure → graph still returns `END` |
| TEST-06 | `tests/test_stream_endpoint.py` | `/stream` 200 + `ExtractData` JSON; 401 without key |

## Supporting change

- `add_memory` in `nodes.py` wraps Zep `add_messages` in try/except (best-effort persistence)

## Run

```bash
uv pip install pytest pytest-asyncio httpx fastapi langgraph langchain-core zep-cloud python-dotenv pydantic langchain-openai langchain-mcp-adapters langgraph-prebuilt
python -m pytest -q
```
