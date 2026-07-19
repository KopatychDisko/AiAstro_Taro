# Phase 9 Plan Check

**Phase:** 09-backend-structure-refactor — Backend Structure Refactor  
**Checked:** 2026-07-19 (pass 2 — post-revision)  
**Plans verified:** 09-01 … 09-06  
**Status:** PASSED  

## Verdict

All three prior blockers are fixed. Six plans stay under the file-budget cap, automated verifies use real `&&`, RESEARCH Open Questions are marked RESOLVED, and D-01–D-04 / SC-01–SC-04 / hard cut / MCP depth / threat models remain covered. Safe to execute.

## Prior blockers — resolution

| Prior blocker | Resolution |
|---------------|------------|
| Plan 01 had 29 files | Split into 09-01..09-04 (agents) + 09-05 (server) + 09-06 (hard-cut); max files_modified = 14 |
| `&amp;&amp;` in Plan 02 verifies | No HTML entities in any plan; all `<automated>` use real `&&` |
| RESEARCH Open Questions unresolved | `## Open Questions (RESOLVED)` with AsyncZep-in-workflow + `factories.create_agents` aggregator |

## Coverage Summary

| Requirement / Decision | Plans | Status |
|------------------------|-------|--------|
| SC-01 server package | 05, 06 | Covered |
| SC-02 agents package, no HTTP in agents | 01, 04, 06 | Covered |
| SC-03 per-agent split | 02, 03, 04 | Covered |
| SC-04 pytest green + public imports | 06 | Covered |
| D-01 server/ + agents/ (no top-level graph long-term) | 01–06 | Covered |
| D-02 one-way server→agents boundary | 01–05 (grep in 05) | Covered |
| D-03 `uvicorn server.app:app`, no app shim | 05, 06 | Covered |
| D-04 hard cut, delete legacy, rewrite tests | 06 | Covered |
| MCP `../../../` path depth | 02 (taro + astro factories) | Covered |
| Auth not weakened | 05, 06 + threat models | Covered |
| Deferred (FE TaroCard dedup) excluded | — | OK — no creep |

## Plan Summary

| Plan | Tasks | Files (frontmatter) | Wave | depends_on | Structure |
|------|-------|---------------------|------|------------|-----------|
| 01 | 2 | 7 | 1 | [] | Valid |
| 02 | 2 | 9 | 2 | ["09-01"] | Valid; MCP depth locked |
| 03 | 2 | 7 | 3 | ["09-02"] | Valid; create_agents aggregator |
| 04 | 2 | 6 | 4 | ["09-03"] | Valid; setup_workflow smoke + AsyncZep lock |
| 05 | 2 | 6 | 5 | ["09-04"] | Valid; server + README |
| 06 | 3 (2 auto + checkpoint) | 14 | 6 | ["09-05"] | Valid; hard-cut + full suite |

## Confirm checklist (requested)

1. **Each plan `files_modified` &lt; 15** — ✅ 7 / 9 / 7 / 6 / 6 / 14  
2. **No literal `&amp;&amp;` in automated verifies** — ✅ real `&&` only (0 HTML amp entities)  
3. **RESEARCH Open Questions marked RESOLVED** — ✅ both questions resolved inline  
4. **Still covers D-01–D-04, SC-01–SC-04, hard cut, MCP depth, threat models** — ✅  

## Dimension Results

| # | Dimension | Result |
|---|-----------|--------|
| 1 | Requirement coverage | PASS — SC-01..SC-04 each in ≥1 plan `requirements` |
| 2 | Task completeness | PASS — auto tasks have files/action/verify/done; checkpoint structured |
| 3 | Dependency correctness | PASS — acyclic 01→02→03→04→05→06; waves match |
| 4 | Key links planned | PASS — TaroCard, MCP paths, setup_workflow, server→agents, patch sites |
| 5 | Scope sanity | PASS — all plans &lt;15 files; tasks 2–3; Plan 06 at 14 = warning band only |
| 6 | Verification derivation | PASS — Plan 04 Task 2 now mocks `await setup_workflow()` |
| 7 | Context compliance | PASS — D-01..D-04 honored; deferred FE-02 excluded |
| 7b | Scope reduction | PASS — no v1/stub/placeholder dilution |
| 7c | Architectural tier | PASS — auth/HTTP in server (05); orchestration in agents (01–04) |
| 8 | Nyquist compliance | PASS — VALIDATION.md exists; all auto tasks have `<automated>`; no watch mode |
| 9 | Cross-plan data contracts | PASS — AsyncZep / create_agents patch sites consistent 03→04→06 |
| 10 | .cursor/rules/ | SKIPPED (no `.cursor/rules/`) |
| 11 | Research resolution | PASS — Open Questions (RESOLVED) |
| 12 | Pattern compliance | SKIPPED (no PATTERNS.md) |

### Dimension 8: Nyquist detail

| Task | Plan | Wave | Automated Command | Status |
|------|------|------|-------------------|--------|
| T1 foundation | 01 | 1 | PYTHONPATH import models/state/routing/config | ✅ |
| T2 cards mapping | 01 | 1 | import mapping `&&` pytest -q | ✅ |
| T1 router/taro | 02 | 2 | import + assert `../../../tarotmcp` | ✅ |
| T2 astro | 02 | 2 | import + assert `../../../astromcp` `&&` pytest | ✅ |
| T1 memory | 03 | 3 | import memory tools/factory | ✅ |
| T2 aggregator | 03 | 3 | import create_agents `&&` pytest | ✅ |
| T1 nodes | 04 | 4 | import per-agent node modules | ✅ |
| T2 workflow | 04 | 4 | mocked await setup_workflow `&&` pytest | ✅ |
| T1 server | 05 | 5 | import server + reverse-import grep + compare_digest | ✅ |
| T2 README | 05 | 5 | rg uvicorn server.app:app only | ✅ |
| T1 rewrite tests | 06 | 6 | pytest all 8 test modules | ✅ |
| T2 delete + gates | 06 | 6 | pytest -q + path/grep gates | ✅ |
| T3 checkpoint | 06 | 6 | rg entrypoint + legacy paths gone | ✅ |

Sampling: Waves 1–6 each fully verified → ✅  
Wave 0 MISSING refs: none → ✅  
Overall Nyquist: ✅ PASS

---

## Warnings (non-blocking)

**1. [scope_sanity] Plan 06 lists 14 files_modified (warning band ≥10)**  
- Plan: 09-06  
- Acceptable: Task 1 (8 test rewrites) and Task 2 (6 deletes) stay separate; do not merge more work.

---

## Structured Issues

```yaml
issues:
  - plan: "09-06"
    dimension: scope_sanity
    severity: warning
    description: "Plan 06 has 14 files_modified (warning band ≥10, under blocker ≥15)"
    metrics:
      tasks: 3
      files: 14
    fix_hint: "Keep test rewrite and delete gates as separate tasks; do not add more scope"
```

---

## What remains solid (do not regress)

- Locked decisions D-01–D-04 mapped to concrete tasks; no FE-02 / deferred creep  
- Hard cut: delete flat modules + `graph/`, no shim, grep gates, full `pytest -q`  
- MCP: factories at `agents/<name>/factory.py` with `../../../tarotmcp|astromcp` preserved  
- Threat models on all six plans; auth relocate-only + `compare_digest` + stream tests  
- Patch-site discipline (`agents.workflow.create_agents` / `AsyncZep`) locked across 03→04→06  
- One-way import boundary enforced with reverse grep in Plan 05  
- Prior warning fixed: Plan 04 Task 2 exercises mocked `await setup_workflow()`  
- Prior warning fixed: Plan 06 Task 1 runs all eight test modules including router + add_memory  

---

## Recommendation

0 blocker(s). Plans verified. Run `/gsd-execute-phase 9` to proceed.

## VERIFICATION PASSED

## PLAN CHECK PASSED
