# Purging `.env` from Git History

## Why

If `.env` was ever committed, removing it from the current tree is not enough — secrets remain recoverable from past commits. `git filter-repo` rewrites history to drop `.env` blobs entirely.

## Procedure

1. Ensure `.env` is untracked: `git ls-files .env` must be empty.
2. Run from repo root: `bash scripts/purge-env-from-history.sh`
3. Verify locally:
   - `git log --all --full-history -- .env` — no output
   - `git rev-list --objects --all | grep -E '(^|/)\.env$'` — no output
4. **Rotate all secrets** that were ever in committed `.env` (API keys, DB passwords, etc.). History purge does not invalidate leaked credentials.

## Force-push (coordinate with collaborators)

After a history rewrite, every clone must be re-synced:

```bash
git push origin --force --all
git push origin --force --tags
```

Warn collaborators before force-pushing. They should re-clone or reset:

```bash
git fetch origin
git reset --hard origin/main
```

## Local `.env`

The working-tree `.env` file is preserved for development. Do not commit it again — `.gitignore` enforces exclusion.
