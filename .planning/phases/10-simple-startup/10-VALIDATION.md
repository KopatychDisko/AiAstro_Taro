---
phase: 10
slug: simple-startup
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-07-20
---

# Phase 10 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest ≥8.3.0 + pytest-asyncio ≥0.25.0 |
| **Config file** | `pyproject.toml` → `[tool.pytest.ini_options]` (`pythonpath = ["src/backend", "."]`) |
| **Quick run command** | `uv run pytest -q tests/test_required_env.py tests/test_aitaro_scripts.py -x` |
| **Full suite command** | `uv run pytest -q` |
| **Estimated runtime** | ~10 seconds (quick) / ~30 seconds (full) |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest -q tests/test_required_env.py tests/test_aitaro_scripts.py -x`
- **After every plan wave:** Run `uv run pytest -q`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 10-*-* | * | * | SC-10.1 | — | Setup entrypoint + MCP build path | unit | `uv run pytest -q tests/test_aitaro_scripts.py -x` | ❌ W0 | ⬜ pending |
| 10-*-* | * | * | SC-10.2 | — | Wrapper exposes `server` without manual PYTHONPATH | unit | `uv run pytest -q tests/test_aitaro_scripts.py -x` | ❌ W0 | ⬜ pending |
| 10-*-* | * | * | SC-10.3 | T-10-01 | Missing/empty required env fail-fast; no secret values logged | unit | `uv run pytest -q tests/test_required_env.py -x` | ❌ W0 | ⬜ pending |
| 10-*-* | * | * | SC-10.4 | — | Tarot missing-dist message mentions `aitaro-setup` | unit | assert factory error text | ❌ W0 | ⬜ pending |
| 10-*-* | * | * | SC-10.5 | — | README 4 steps + UI; no `PYTHONPATH=… uvicorn` | grep | `rg -n "PYTHONPATH=.*uvicorn|uv run aitaro-api" README.md` | ❌ | ⬜ pending |
| 10-*-* | * | * | SC-10.6 | — | Full suite green; pytest pythonpath unchanged (D-07) | suite | `uv run pytest -q` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_required_env.py` — missing/empty/present keys + `.env.example` hint in message
- [ ] `tests/test_aitaro_scripts.py` — `aitaro_api` / `aitaro_setup` importable; `main` callables; optional subprocess monkeypatch for npm
- [ ] Do **not** change pytest `pythonpath` (D-07)
- [ ] Avoid TestClient against real lifespan+MCP in unit tests — keep mocked lifespan pattern from `tests/test_stream_endpoint.py`

*Existing pytest infrastructure covers SC-10.6 once Wave 0 tests land. No new framework install.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Live `uv run aitaro-api` starts | SC-10.2 | Needs real `.env` + MCP build | `uv run aitaro-setup` then `uv run aitaro-api`; hit `/stream` with API key |
| Setup stdout checklist | SC-10.1 / D-13 | Human-readable copy | Run `uv run aitaro-setup`; confirm MCP OK, env OK, Streamlit `login_menu.py` hint, no Postgres hard fail |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
