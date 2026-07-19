---
phase: 11
slug: agent-harness-hardening
status: verified
threats_open: 0
asvs_level: 1
created: 2026-07-20
---

# Phase 11 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| Client → FastAPI stream | Authenticated user requests into agent graph | User message, profile fields, session id |
| Env → Langfuse (optional) | Outbound telemetry only when keys present | Trace metadata (session/user tags); never required for startup |
| Zep → `take_context` | Untrusted user memory into LLM context | Memory strings / name-only fallback — always trust-labeled |
| MCP → cards mapping | Spread/card parse for UI | `spread_name` + card HTML metadata (display/layout only) |
| Dev → DeepEval offline | Opt-in eval suite excluded from default pytest | Hand-curated goldens; no Confident AI / live cloud gate |

---

## Threat Register

| Threat ID | Category | Component | Disposition | Mitigation | Status |
|-----------|----------|-----------|-------------|------------|--------|
| T-11-01 | Information Disclosure | observability/app | mitigate | Optional Langfuse keys; empty callbacks when absent; never log secrets; mock-only verification | closed |
| T-11-02 | Tampering | CallbackHandler metadata | accept | Server-composed session/user tags; Phase 7 posture | closed |
| T-11-03 | Tampering | spread_name from MCP | accept | Display/layout metadata only; not executed as code | closed |
| T-11-04 | Elevation of Privilege | deleted unlock LLM | mitigate | Unlock agent removed — reduced surface | closed |
| T-11-05 | Tampering/Elevation | take_context + context_trust | mitigate | Always wrap with UNTRUSTED_USER_MEMORY | closed |
| T-11-06 | Denial of Service | capped_tools_condition | mitigate | Cap 3 + structured log + silent stop (`__end__`) | closed |
| T-11-07 | Information Disclosure | tests/evals + deepeval | mitigate | Offline only; no Confident AI; eval mark excluded from default pytest | closed |
| T-11-08 | Denial of Service | LLM-judge evals | mitigate | Marker + addopts keep default suite fast; ExactMatch offline metrics | closed |
| T-11-SC | Tampering | uv add deepeval | mitigate | Human PyPI↔GitHub legitimacy gate before install (approved in execute) | closed |

*Status: open · closed*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Verification Evidence

| Threat ID | Evidence |
|-----------|----------|
| T-11-01 | `src/backend/server/observability.py:9–31` — `_langfuse_keys_present` / empty `[]` without keys; secret used only for presence check, never logged. `src/backend/server/app.py:24–60` wires callbacks/metadata/flush. `src/backend/server/required_env.py` — Langfuse not in `REQUIRED_ENV_KEYS`. `tests/test_observability.py` — mocked `CallbackHandler` / `get_client` only. |
| T-11-02 | Accepted risk (below). `langfuse_run_metadata` in `observability.py:34–41` composes tags from server `session_id`/`user_name`; `app.py:30` applies metadata — not client-controlled CallbackHandler ctor args. |
| T-11-03 | Accepted risk (below). `cards/mapping.py` / `cards/node.py` emit `spread_name`; frontend `create_html_taro(cards, spread_name)` selects known layout renderers — string not executed as code. |
| T-11-04 | `rg unlock_card_agent\|UnlockCard\|unlock_name` under `src/` empty. `factories.py:13–20` — six Agents fields only; no unlock factory. `state.py` Agents dataclass has no unlock agent. |
| T-11-05 | `context_trust.py:5–12` — `UNTRUSTED_USER_MEMORY_PREFIX` + `wrap_untrusted_user_memory`. `workflow.py:36–43` — both Zep success and exception/name-only paths return wrapped context (single return after try/except). |
| T-11-06 | `routing.py:10` `MAX_TOOL_ITERATIONS = 3`; `15–25` logs `tool_iteration_cap_reached` with structured `extra`, returns `"__end__"` (no user-facing limit copy). Covered by `tests/test_routing.py`. |
| T-11-07 | `tests/evals/metrics.py` — offline `ExactMatchMetric`, docstring “no Confident AI”. Eval modules use `@pytest.mark.eval`; no Confident login APIs. `pyproject.toml:68` `addopts = "-m 'not eval'"`. |
| T-11-08 | Same marker/addopts gate; metrics are deterministic ExactMatch (no LLM judge in default or eval path for this suite). Default `pytest -q` deselects evals (67 passed / 10 deselected per VERIFICATION). |
| T-11-SC | `11-04-SUMMARY.md` — human replied `approved` on PyPI↔GitHub legitimacy checkpoint before `uv add --dev deepeval`. `pyproject.toml:61` `deepeval>=4.1.1` in dev group. |

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-11-02 | T-11-02 | Langfuse CallbackHandler metadata is server-composed session/user tags. If keys are stolen, impact matches Phase 7 optional-telemetry posture; no client-controlled constructor session binding. | Phase 11 plan (11-01 threat_model) / security audit | 2026-07-20 |
| AR-11-03 | T-11-03 | `spread_name` from MCP is display/layout metadata (known spread title → renderer map). Same trust boundary as existing card HTML parsing; string is not executed as code. | Phase 11 plan (11-02 threat_model) / security audit | 2026-07-20 |

*Accepted risks do not resurface in future audit runs.*

---

## Unregistered Flags

None. All SUMMARY `## Threat Flags` sections map to register IDs (T-11-01…08 / T-11-SC) or explicitly report no new surface.

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-07-20 | 9 | 9 | 0 | gsd-security-auditor |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-07-20
