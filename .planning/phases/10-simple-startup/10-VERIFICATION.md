---
phase: 10-simple-startup
verified: 2026-07-19T22:31:02Z
status: human_needed
score: 6/6 must-haves verified
overrides_applied: 0
re_verification: false
human_verification:
  - test: "Live aitaro-setup then aitaro-api smoke"
    expected: "Setup builds MCP and prints checklist; API binds 127.0.0.1:8000; /stream accepts X-API-Key"
    why_human: "Needs real .env secrets, npm build, and a bound port — unit tests mock subprocess/uvicorn/lifespan"
  - test: "Setup stdout checklist copy"
    expected: "MCP OK, required-env OK for three keys, uv run aitaro-api next step, Streamlit login_menu.py hint, Postgres reminder without hard-fail"
    why_human: "Human-readable copy quality beyond unit string asserts"
next_action: human_uat
next_command: "/gsd-verify-work 10"
---

# Phase 10: Simple Startup Verification Report

**Phase Goal:** Make local development start with a single documented path — install deps, build tarot MCP, validate required env vars, run backend and frontend without `PYTHONPATH` gymnastics or opaque startup failures.

**Verified:** 2026-07-19T22:31:02Z  
**Status:** human_needed  
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths (Roadmap SC-10.1..SC-10.6)

| # | Truth | Status | Evidence |
| --- | ------- | ---------- | -------------- |
| 1 | SC-10.1: Documented path installs deps (`uv sync`), builds tarot MCP, prints clear next steps | ✓ VERIFIED | README steps 2–3: `uv sync` then `uv run aitaro-setup`. Setup runs fixed `npm install` + `npm run build` in `src/tarotmcp`, then prints checklist (`uv run aitaro-api`, Streamlit). Per D-02, setup does **not** own `uv sync` — documented path covers both. |
| 2 | SC-10.2: Backend starts via `uv run` without manual `PYTHONPATH=src/backend` | ✓ VERIFIED | `[project.scripts] aitaro-api`; `scripts/aitaro_api.py` `ensure_backend_on_path()` + `uvicorn.run("server.app:app", host="127.0.0.1", port=8000, reload=True)`. Consoles present at `.venv/bin/aitaro-api`. Unit test asserts uvicorn kwargs. |
| 3 | SC-10.3: Missing required env fails fast with actionable messages before MCP/LLM init | ✓ VERIFIED | `REQUIRED_ENV_KEYS = (STREAM_API_KEY, OPENAI_API_KEY, ZEP_API)`; setup calls `require_env_or_exit()` before npm; lifespan calls `require_env_or_raise()` before `await setup_workflow()`. Message lists keys + `.env.example` hint. Tests prove ordering and empty-string handling. |
| 4 | SC-10.4: Missing tarot MCP dist fails with exact build command | ✓ VERIFIED | `factory.py` FileNotFoundError: `Run: uv run aitaro-setup` (+ legacy npm one-liner). `tests/test_tarot_factory_message.py` asserts `uv run aitaro-setup`. |
| 5 | SC-10.5: README Quick start ≤5 steps matching working scripts | ✓ VERIFIED | Four numbered steps (`.env` → `uv sync` → `aitaro-setup` → `aitaro-api`) + optional UI `login_menu.py`. No `PYTHONPATH=` / uvicorn docs (`rg` + `test_readme_quickstart.py`). |
| 6 | SC-10.6: `pytest -q` still green | ✓ VERIFIED | `uv run pytest -q` → **45 passed**, 1 warning, exit 0. `pythonpath = ["src/backend", "."]` unchanged (D-07). |

**Score:** 6/6 truths verified (automated). Live smoke deferred to human verification below.

### Locked Decisions (D-01..D-16)

| Decision | Status | Evidence |
| -------- | ------ | -------- |
| D-01 `[project.scripts]` / `uv run` entrypoints | ✓ | `aitaro-setup`, `aitaro-api` in pyproject; resolve under `.venv/bin` |
| D-02 setup = MCP build + env checklist; no `uv sync` | ✓ | `aitaro_setup.py` has no `uv sync`; source/test assert |
| D-03 API-only runtime; no `aitaro-ui` | ✓ | Only two scripts; Streamlit documented separately |
| D-04 uvicorn `--reload` port 8000 fixed | ✓ | `reload=True`, `port=8000`, host `127.0.0.1`; no argv pass-through |
| D-05 wrapper sets path; no editable `src/` package | ✓ | `ensure_backend_on_path`; setuptools `py-modules` under `scripts/` only |
| D-06 entrypoints under `scripts/` | ✓ | `scripts/aitaro_api.py`, `scripts/aitaro_setup.py` |
| D-07 pytest pythonpath unchanged | ✓ | `["src/backend", "."]` |
| D-08 no raw PYTHONPATH uvicorn in README | ✓ | grep + test gate |
| D-09 required keys STREAM/OPENAI/ZEP | ✓ | `REQUIRED_ENV_KEYS` exact tuple |
| D-10 validate in setup **and** lifespan before MCP | ✓ | `require_env_or_exit` before npm; `require_env_or_raise` before `setup_workflow` |
| D-11 compact missing list + `.env.example` hint | ✓ | `format_missing_env_message` |
| D-12 optional keys not checked | ✓ | no Langfuse/Qdrant/HF/Postgres in `REQUIRED_ENV_KEYS`; tests assert disjoint |
| D-13 setup does not start Streamlit; prints checklist | ✓ | print-only UI section |
| D-14 Postgres reminder text only (no validate) | ✓ | checklist `POSTGRESQL_*`; not in required keys |
| D-15 Streamlit entry `login_menu.py` | ✓ | setup stdout + README |
| D-16 README 4 steps + one UI line | ✓ | Quick start structure matches |

### Plan Must-Haves (merged)

**10-01 truths:** console scripts resolve; missing/empty env → compact list + hint; optional keys never checked; pytest pythonpath stays — all ✓ VERIFIED.

**10-02 truths:** env then npm without `uv sync`; Streamlit + Postgres reminder without validating POSTGRESQL_*; factory mentions `aitaro-setup` — all ✓ VERIFIED.

**10-03 truths:** uvicorn wrapper defaults; lifespan fail-fast before workflow; README four steps + UI, no PYTHONPATH uvicorn — all ✓ VERIFIED.

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | -------- | ------ | ------- |
| `pyproject.toml` | scripts + setuptools | ✓ VERIFIED | `[project.scripts]`, build-system, `py-modules`, package-dir `scripts` |
| `scripts/aitaro_api.py` | path wrapper + uvicorn | ✓ VERIFIED | `find_repo_root`, `ensure_backend_on_path`, `main` → uvicorn |
| `scripts/aitaro_setup.py` | env + npm + checklist | ✓ VERIFIED | `build_tarot_mcp`, `require_env_or_exit`, checklist |
| `src/backend/server/required_env.py` | shared D-09 helper | ✓ VERIFIED | all five exports present; no secret logging |
| `src/backend/server/app.py` | lifespan gate | ✓ VERIFIED | `require_env_or_raise` then `setup_workflow` |
| `src/backend/agents/taro/factory.py` | aitaro-setup message | ✓ VERIFIED | FileNotFoundError text |
| `README.md` | D-16 Quick start | ✓ VERIFIED | four steps + UI |
| `tests/test_required_env.py` | Wave 0 env tests | ✓ VERIFIED | exists, substantive, in suite |
| `tests/test_aitaro_scripts.py` | entrypoint + npm mocks | ✓ VERIFIED | exists, substantive |
| `tests/test_tarot_factory_message.py` | SC-10.4 | ✓ VERIFIED | exists |
| `tests/test_lifespan_required_env.py` | lifespan + uvicorn kwargs | ✓ VERIFIED | exists |
| `tests/test_readme_quickstart.py` | D-08/D-16 grep | ✓ VERIFIED | exists |

`gsd-tools query verify.artifacts` on 10-01/02/03: all_passed true for all declared artifacts.

### Key Link Verification

| From | To | Via | Status | Details |
| ---- | -- | --- | ------ | ------- |
| pyproject.toml | aitaro_api:main | `[project.scripts]` | ✓ WIRED | Manual: `aitaro-api = "aitaro_api:main"`; `.venv/bin/aitaro-api` exists (`gsd-tools` false-negative: looks for file path string in TOML) |
| pyproject.toml | aitaro_setup:main | `[project.scripts]` | ✓ WIRED | Same; `aitaro-setup = "aitaro_setup:main"` |
| scripts/aitaro_api.py | server.app:app | uvicorn import string | ✓ WIRED | Line 44 `"server.app:app"` (`gsd-tools` regex false-negative) |
| scripts/aitaro_setup.py | required_env | `require_env_or_exit` | ✓ WIRED | after path ensure, before npm |
| scripts/aitaro_setup.py | src/tarotmcp | subprocess cwd | ✓ WIRED | `repo_root / "src" / "tarotmcp"` |
| factory.py | aitaro-setup | FileNotFoundError | ✓ WIRED | message contains `uv run aitaro-setup` |
| app.py | required_env | `require_env_or_raise` | ✓ WIRED | before `setup_workflow` |
| README.md | aitaro-api / aitaro-setup | Quick start | ✓ WIRED | both commands present |
| tests/test_required_env.py | required_env | import | ✓ WIRED | pattern verified by gsd-tools |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| -------- | ------------- | ------ | ------------------ | ------ |
| `required_env` | `os.getenv(key)` | process env / `.env` via dotenv | Yes (live env) | ✓ FLOWING |
| `aitaro_setup` checklist | stdout strings | hardcoded post-success | Static checklist (by design) | ✓ FLOWING (intentional) |
| `aitaro_api` | uvicorn app string | fixed `"server.app:app"` | Import-string launch | ✓ FLOWING |
| lifespan | `workflow` | `setup_workflow()` after env gate | Real workflow when env OK | ✓ FLOWING |

No hollow/static stubs on user-facing startup paths.

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| Full suite green (SC-10.6) | `uv run pytest -q` | 45 passed, exit 0 | ✓ PASS |
| Console scripts importable | `uv run python -c "import aitaro_api, aitaro_setup; …"` | `scripts_ok` | ✓ PASS |
| Entry points installed | `uv run which aitaro-api aitaro-setup` | `.venv/bin/…` | ✓ PASS |
| README no PYTHONPATH uvicorn | `rg PYTHONPATH= README.md` | 0 matches | ✓ PASS |
| Live aitaro-api bind | — | not run (no server start in verifier) | ? SKIP → human |

### Probe Execution

| Probe | Command | Result | Status |
| ----- | ------- | ------ | ------ |
| — | — | No phase-declared or conventional `scripts/*/tests/probe-*.sh` | SKIPPED |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ---------- | ----------- | ------ | -------- |
| SC-10.1 | 10-01, 10-02 | Setup path + MCP build + next steps | ✓ SATISFIED | setup + README |
| SC-10.2 | 10-01, 10-03 | No manual PYTHONPATH | ✓ SATISFIED | wrapper + packaging |
| SC-10.3 | 10-01, 10-03 | Env fail-fast before MCP/LLM | ✓ SATISFIED | required_env + lifespan |
| SC-10.4 | 10-02 | Missing dist → aitaro-setup | ✓ SATISFIED | factory + test |
| SC-10.5 | 10-03 | README ≤5 steps | ✓ SATISFIED | Quick start + test |
| SC-10.6 | 10-01, 10-03 | pytest green | ✓ SATISFIED | 45 passed |

No REQUIREMENTS.md in repo; roadmap SC IDs used as the contract. No orphaned phase requirements found.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| — | — | No TBD/FIXME/XXX/TODO/HACK/PLACEHOLDER in phase key files | — | None |
| `tests/test_aitaro_scripts.py` | 59 | Test name `test_aitaro_api_main_only_ensures_path` slightly stale (main now also calls uvicorn; mock covers it) | ℹ️ Info | Does not affect goal |

### Human Verification Required

### 1. Live `uv run aitaro-api` smoke

**Test:** With a filled `.env`, run `uv run aitaro-setup` then `uv run aitaro-api`; hit `POST /stream` with `X-API-Key`.  
**Expected:** Setup succeeds; API listens on `http://127.0.0.1:8000`; stream responds (or auth-fails closed on bad key).  
**Why human:** Needs real secrets, npm, and a live server — verifier must not start services.

### 2. Setup stdout checklist

**Test:** Run `uv run aitaro-setup` and read stdout.  
**Expected:** Tarot MCP OK; Required env OK naming three keys; Next `uv run aitaro-api`; UI line with `login_menu.py`; Postgres reminder; no hard-fail on POSTGRESQL_*.  
**Why human:** Copy/UX confirmation beyond unit asserts (unit already checks key substrings with mocked npm).

### Gaps Summary

**No automated gaps.** All roadmap success criteria and plan must-haves are verified in code and tests. Status is `human_needed` solely for live smoke / checklist UX per VALIDATION.md Manual-Only Verifications.

**Note on SC-10.1 wording:** Roadmap mentions a script that “installs Python deps (`uv sync`)”; locked D-02 splits `uv sync` (user) from `aitaro-setup` (MCP + env). Documented four-step path satisfies the intent — not treated as a gap.

**Deferred:** None (no later milestone phases after Phase 10).

---

_Verified: 2026-07-19T22:31:02Z_  
_Verifier: Claude (gsd-verifier)_
