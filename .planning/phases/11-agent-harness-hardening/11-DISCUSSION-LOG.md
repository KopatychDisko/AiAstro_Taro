# Phase 11: Agent Harness Hardening - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-07-20
**Phase:** 11-agent-harness-hardening
**Areas discussed:** Unlock agent fate, Budget behavior, Trust-labeled context, Langfuse land + verify, Eval harness shape

---

## Unlock agent fate

| Option | Description | Selected |
|--------|-------------|----------|
| Hard-delete | Remove unlock agent surface | ✓ |
| Keep stubs | Leave unused for future | |
| You decide | | |

**User's choice:** Hard-delete

| Option | Description | Selected |
|--------|-------------|----------|
| Delete agent only | Keep unlock_name in state/API/UI | |
| Also strip unlock_name | End-to-end remove | ✓ |
| You decide | | |

**User's choice:** Strip unlock_name end-to-end

| Option | Description | Selected |
|--------|-------------|----------|
| No separate unlock title | Cards only | |
| Derive from MCP spread/card | | ✓ |
| You decide | | |

**User's choice:** Derive title from MCP spread/card name

---

## Budget behavior

| Option | Description | Selected |
|--------|-------------|----------|
| Silent stop | Current UX | |
| Log + silent stop | Observability without user copy | ✓ |
| User-visible notice | Product copy change | |

**User's choice:** Log + silent stop

| Option | Description | Selected |
|--------|-------------|----------|
| Named constant 3 | Document only | ✓ |
| Env-configurable | AITARO_MAX_TOOL_ITERATIONS | |
| You decide | | |

**User's choice:** Keep constant 3

| Option | Description | Selected |
|--------|-------------|----------|
| Tool-loop only | Defer token budgets | ✓ |
| Also soft token/step | | |
| You decide | | |

**User's choice:** Tool-loop only

---

## Trust-labeled context

| Option | Description | Selected |
|--------|-------------|----------|
| Assembly only | take_context wrap | ✓ |
| Prompts only | | |
| Both | | |

**User's choice:** Assembly only

| Option | Description | Selected |
|--------|-------------|----------|
| English harness label | | ✓ |
| Bilingual | | |
| You decide | | |

**User's choice:** English

| Option | Description | Selected |
|--------|-------------|----------|
| Always wrap | Including name-only fallback | ✓ |
| Wrap only when memory present | | |
| You decide | | |

**User's choice:** Always wrap

---

## Langfuse land + verify

| Option | Description | Selected |
|--------|-------------|----------|
| Land + test | Include v4 wiring in phase | ✓ |
| Tests only | Assume already merged | |
| You decide | | |

**User's choice:** Land + test

| Option | Description | Selected |
|--------|-------------|----------|
| Unit/integration mocks only | No live cloud | ✓ |
| Unit + optional manual smoke | | |
| You decide | | |

**User's choice:** Unit/integration only

---

## Eval harness shape

| Option | Description | Selected |
|--------|-------------|----------|
| Pytest + mocked LLM | | |
| DeepEval | | ✓ |
| You decide | | |

**User's choice:** DeepEval

| Option | Description | Selected |
|--------|-------------|----------|
| Offline DeepEval + pytest | No Confident AI | ✓ |
| DeepEval + Confident AI | | |
| You decide | | |

**User's choice:** Offline

| Option | Description | Selected |
|--------|-------------|----------|
| Router + taro | | ✓ |
| Router + astro | | |
| You decide | | |

**User's choice:** Router + taro; also expressed desire to remove astro entirely (deferred)

---

## Claude's Discretion

- Exact trust-wrapper wording/delimiters
- Structured log fields for tool-cap
- DeepEval metrics and dataset layout
- MCP title field naming after unlock_name removal
- Keep astro Langfuse config wiring until remove-astro phase

## Deferred Ideas

- Remove astrology agent entirely (user preference) — future phase
- Token/cost budgets; env-configurable tool iterations; Confident AI; live Langfuse smoke
