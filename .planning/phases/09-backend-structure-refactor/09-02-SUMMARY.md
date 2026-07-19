---
phase: 09-backend-structure-refactor
plan: 02
subsystem: api
tags: [agents, langgraph, mcp, factories, packaging, refactor]

requires:
  - phase: 09-backend-structure-refactor
    provides: agents.state schemas, agents.config base_url/zep_api
provides:
  - agents.router.factory.create_router_agent
  - agents.taro.factory.create_tarot_agent
  - agents.astro.factory.create_astro_agent
  - MCP ../../../tarotmcp and ../../../astromcp path depth preserved
affects:
  - 09-03 memory tools and create_agents aggregator
  - 09-04 workflow assembly
  - 09-06 legacy deletion

tech-stack:
  added: []
  patterns:
    - "Per-agent packages at agents/<name>/{prompt,factory}.py matching graph/agents depth for MCP paths"
    - "Lazy import of agents.memory.tools from taro/astro factories until Plan 03 lands"

key-files:
  created:
    - src/backend/agents/router/__init__.py
    - src/backend/agents/router/prompt.py
    - src/backend/agents/router/factory.py
    - src/backend/agents/taro/__init__.py
    - src/backend/agents/taro/prompt.py
    - src/backend/agents/taro/factory.py
    - src/backend/agents/astro/__init__.py
    - src/backend/agents/astro/prompt.py
    - src/backend/agents/astro/factory.py
  modified: []

key-decisions:
  - "Lazy-import search_facts/search_nodes from agents.memory.tools inside taro/astro factories so packages import before Plan 03"
  - "Duplicate create_prompt helper per package prompt.py for package isolation"

patterns-established:
  - "agents/<name>/factory.py keeps ../../../ MCP relative paths identical to graph/agents/agent.py"
  - "Legacy graph/agents left untouched until Plan 06"

requirements-completed: [SC-03]

duration: 2min
completed: 2026-07-19
---

# Phase 09 Plan 02: Router/Taro/Astro Packages Summary

**Per-agent router/taro/astro packages under `agents/` with MCP `../../../tarotmcp` and `../../../astromcp` path depth preserved**

## Performance

- **Duration:** 2 min
- **Started:** 2026-07-19T21:05:37Z
- **Completed:** 2026-07-19T21:07:17Z
- **Tasks:** 2
- **Files modified:** 9 created

## Accomplishments

- Extracted router prompt + `create_router_agent` into `agents/router/`
- Extracted tarot prompt + `create_tarot_agent` into `agents/taro/` with `../../../tarotmcp/dist/index.js`
- Extracted astro prompt + `create_astro_agent` into `agents/astro/` with `../../../astromcp/dist/main.js`
- Legacy `graph/agents` unchanged; pytest still green (13 passed)

## Task Commits

Each task was committed atomically:

1. **Task 1: Router and taro packages** - `8bf8120` (feat)
2. **Task 2: Astro package** - `d01ff80` (feat)

**Plan metadata:** (pending docs commit)

## Files Created/Modified

- `src/backend/agents/router/__init__.py` - Package marker
- `src/backend/agents/router/prompt.py` - Router system prompt
- `src/backend/agents/router/factory.py` - `create_router_agent`
- `src/backend/agents/taro/__init__.py` - Package marker
- `src/backend/agents/taro/prompt.py` - Tarot reader prompt
- `src/backend/agents/taro/factory.py` - `create_tarot_agent` + MCP path
- `src/backend/agents/astro/__init__.py` - Package marker
- `src/backend/agents/astro/prompt.py` - Astrologer prompt
- `src/backend/agents/astro/factory.py` - `create_astro_agent` + MCP path

## Decisions Made

- Lazy-import `search_facts`/`search_nodes` from `agents.memory.tools` inside taro/astro factories so factory modules import cleanly before Plan 03 creates memory tools
- Kept a local `create_prompt` helper in each package's `prompt.py` rather than a shared util (package isolation)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Lazy-import memory tools in taro/astro factories**
- **Found during:** Task 1 (Router and taro packages)
- **Issue:** `create_tarot_agent` / `create_astro_agent` need `search_facts`/`search_nodes`, but Plan 03 owns `agents.memory.tools`; module-level import would break Plan 02 verify
- **Fix:** Import memory tools inside the factory functions (deferred binding until Plan 03)
- **Files modified:** `src/backend/agents/taro/factory.py`, `src/backend/agents/astro/factory.py`
- **Verification:** `from agents.taro.factory import create_tarot_agent` and astro equivalent succeed; MCP path asserts pass
- **Committed in:** `8bf8120`, `d01ff80` (task commits)

---

**Total deviations:** 1 auto-fixed (Rule 2)
**Impact on plan:** Minimal; enables SC-03 packages now without pulling Plan 03 scope.

## Issues Encountered

- Used `.venv/bin/python` for verifies (`uv run` / `psycopg2` noted in STATE.md from Plan 01)

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 03 can add `agents.memory.tools` and `agents.factories.create_agents`; taro/astro already expect that import path
- MCP depth locked; do not flatten factories to `agents/*.py`

## Self-Check: PASSED

- FOUND: all 9 planned artifacts
- FOUND: commits `8bf8120`, `d01ff80` (via `git cat-file`)

---
*Phase: 09-backend-structure-refactor*
*Completed: 2026-07-19*
