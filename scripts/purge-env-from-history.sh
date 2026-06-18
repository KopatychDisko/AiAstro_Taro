#!/usr/bin/env bash
# Purge .env from entire git history using git-filter-repo.
# Run from repository root. Does NOT read or print .env contents.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

if ! command -v git-filter-repo >/dev/null 2>&1; then
  if [ -x "$ROOT/.venv/bin/git-filter-repo" ]; then
    export PATH="$ROOT/.venv/bin:$PATH"
  fi
fi

if ! command -v git-filter-repo >/dev/null 2>&1; then
  echo "ERROR: git-filter-repo is not installed." >&2
  echo "Install: pip install git-filter-repo  OR  apt install git-filter-repo" >&2
  exit 1
fi

echo "Purging .env from all commits (history rewrite)..."
git filter-repo --path .env --invert-paths --force

echo ""
echo "Post-run verification (expect no output):"
echo "  git log --all --full-history -- .env"
echo "  git rev-list --objects --all | grep -E '(^|/)\\.env\$'"
echo ""
echo "Remote sync: see docs/security-git-history-purge.md"
