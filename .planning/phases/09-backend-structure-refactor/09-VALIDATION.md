---
phase: 9
slug: backend-structure-refactor
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-07-19
---

# Phase 9 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.x + pytest-asyncio |
| **Config file** | `pyproject.toml` → `[tool.pytest.ini_options]` |
| **Quick run command** | `python -m pytest -q` |
| **Full suite command** | `python -m pytest -q` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest -q`
- **After every plan wave:** Run `python -m pytest -q`
- **Before `/gsd-verify-work`:** Full suite must be green + grep gates
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 09-*-* | * | * | SC-01 | T-09-01 | Auth stays on `/stream` | unit | `python -m pytest tests/test_stream_endpoint.py tests/test_observability.py -q` | ✅ rewrite | ⬜ pending |
| 09-*-* | * | * | SC-02 | — | setup_workflow from agents | unit | `python -m pytest tests/test_router.py tests/test_add_memory_resilience.py -q` | ✅ rewrite | ⬜ pending |
| 09-*-* | * | * | SC-03 | — | Split packages importable | unit | `python -m pytest tests/test_routing.py tests/test_taro_cards.py tests/test_memory_tools.py -q` | ✅ rewrite | ⬜ pending |
| 09-*-* | * | * | SC-04 | — | Full suite green | suite | `python -m pytest -q` | ✅ | ⬜ pending |
| 09-*-* | * | * | D-03 | — | README entrypoint | grep | `rg "uvicorn server.app:app" README.md` | ❌ Wave 0 | ⬜ pending |
| 09-*-* | * | * | D-04 | T-09-02 | No graph/ shims left | grep | `rg -n "from graph\\.|import graph" tests src/backend` must be empty | ❌ Wave 0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Rewrite test imports/patches to `server.*` / `agents.*` (files exist; contents stale)
- [ ] README entrypoint + layout update (`uvicorn server.app:app`)
- [ ] Post-move grep gate for leftover `graph.` / flat imports

*Existing pytest infrastructure covers behavioral SC-04 once imports/patches are updated. No new test framework install.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Live uvicorn starts | D-03 | Needs env + MCP build | `cd src/backend && uvicorn server.app:app --port 8000` |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
