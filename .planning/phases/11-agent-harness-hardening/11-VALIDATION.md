---
phase: 11
slug: agent-harness-hardening
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-07-20
---

# Phase 11 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest ≥8.3 + pytest-asyncio ≥0.25 (+ deepeval for marked evals) |
| **Config file** | `pyproject.toml` → `[tool.pytest.ini_options]` |
| **Quick run command** | `uv run pytest -q` |
| **Full suite command** | `uv run pytest -q` then `uv run deepeval test run tests/evals` (eval wave) |
| **Estimated runtime** | ~5s unit / eval suite separate |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest -q`
- **After every plan wave:** Run `uv run pytest -q` (+ eval command if eval wave)
- **Before `/gsd-verify-work`:** Unit suite green; eval suite documented runnable offline
- **Max feedback latency:** 60 seconds (unit)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 11-*-* | * | * | SC-11.1 | — | No unlock agent; spread_name rename | unit+grep | `uv run pytest -q tests/test_taro_cards.py tests/test_router.py` | ❌ W0 | ⬜ pending |
| 11-*-* | * | * | SC-11.2 | T-11-budget | Cap + structured log, silent stop | unit | `uv run pytest -q tests/test_routing.py` | ✅ extend | ⬜ pending |
| 11-*-* | * | * | SC-11.3 | T-11-trust | UNTRUSTED_USER_MEMORY wrap always | unit | `uv run pytest -q tests/test_context_trust.py` | ❌ W0 | ⬜ pending |
| 11-*-* | * | * | SC-11.4 | — | Langfuse v4 optional; config prop | unit | `uv run pytest -q tests/test_observability.py tests/test_langfuse_config_prop.py` | partial | ⬜ pending |
| 11-*-* | * | * | SC-11.5 | — | DeepEval offline router+taro | eval | `uv run deepeval test run tests/evals` | ❌ W0 | ⬜ pending |
| 11-*-* | * | * | SC-11.6 | — | Default pytest excludes eval | smoke | `uv run pytest -q` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Land uncommitted Langfuse v4 wiring
- [ ] `tests/test_context_trust.py`
- [ ] Extend `tests/test_routing.py` with caplog
- [ ] `tests/test_langfuse_config_prop.py`
- [ ] `tests/evals/` + goldens + `@pytest.mark.eval` + `addopts = -m "not eval"`
- [ ] `uv add --dev deepeval` after legitimacy checkpoint
- [ ] Update `make_mock_agents` when Agents shape changes

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Frontend card title without unlock_name | D-02/D-03 | UI visual | After API returns `spread_name`, confirm Streamlit title shows MCP-derived name |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s for unit
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
