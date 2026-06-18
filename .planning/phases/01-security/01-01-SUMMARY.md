---
phase: 01-security
plan: 01
subsystem: infra
tags: [git, secrets, filter-repo, security]

requires: []
provides:
  - .env untracked and purged from git history
  - scripts/purge-env-from-history.sh
  - docs/security-git-history-purge.md
affects: [all-phases]

tech-stack:
  added: [git-filter-repo]
  patterns: [history rewrite via filter-repo]

key-files:
  created: [scripts/purge-env-from-history.sh, docs/security-git-history-purge.md]
  modified: [.gitignore]

key-decisions:
  - "Use git filter-repo --path .env --invert-paths for history purge"
  - "Preserve local .env on disk after untrack"

patterns-established:
  - "Secret purge: untrack index first, then filter-repo history rewrite"

status: complete
---

# Plan 01-01 Summary: Purge .env from Git

## Completed

- `git rm --cached .env` — `.env` no longer in index
- `scripts/purge-env-from-history.sh` created and executed
- `docs/security-git-history-purge.md` documents force-push procedure
- Verification: `git log --all --full-history -- .env` empty; `git rev-list` has no `.env` objects
- Local `.env` preserved on disk

## Human Checkpoint (blocking)

Before continuing autonomous execution:

1. Run verification commands (should all pass):
   - `git log --all --full-history -- .env` — no output
   - `git rev-list --objects --all | grep -E '(^|/)\.env$'` — no output
   - `git ls-files .env` — no output
   - `test -f .env && echo OK`

2. **Rotate secrets** that were ever in committed `.env` (OpenRouter, Zep, Postgres, etc.)

3. Re-add remote and force-push per `docs/security-git-history-purge.md`:
   - `git remote add origin git@github.com:KopatychDisko/AiAstro_Taro.git` (filter-repo removed origin)
   - `git push origin --force --all`

Reply **approved** when verified and optional force-push is done.

## Curl reference

N/A for this plan.
