#!/usr/bin/env bash
# Scan tracked source for hardcoded secrets. Exit 0 if clean, 1 if matches found.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

mapfile -t FILES < <(
  git ls-files \
    | grep -E '\.(py|ts|tsx|js|jsx|toml|yaml|yml|json|md|sh)$' \
    | grep -vE '^(\.env$|uv\.lock$)' \
    | grep -vE '(^|/)(node_modules|dist|\.venv|__pycache__)/' \
    || true
)

if [ "${#FILES[@]}" -eq 0 ]; then
  echo "No files to scan."
  exit 0
fi

FOUND=0
TMP_MATCHES="$(mktemp)"
trap 'rm -f "$TMP_MATCHES"' EXIT

check_pattern() {
  local label="$1"
  local pattern="$2"
  local filtered="$3"
  local raw
  raw=$(grep -nE "$pattern" "${FILES[@]}" 2>/dev/null || true)
  if [ -n "$raw" ]; then
    if [ -n "$filtered" ]; then
      raw=$(echo "$raw" | eval "$filtered" || true)
    fi
    if [ -n "$raw" ]; then
      echo "=== $label ==="
      echo "$raw"
      FOUND=1
    fi
  fi
}

check_pattern "OpenAI-style key" 'sk-[a-zA-Z0-9]{20,}' ""
check_pattern "Bearer token" 'Bearer [a-zA-Z0-9._-]{20,}' ""
check_pattern "Hardcoded assignment" "(api[_-]?key|secret|password|token)[[:space:]]*=[[:space:]]*['\"][^'\"]{8,}['\"]" \
  "grep -v 'os\\.getenv' | grep -v 'your-key' | grep -v 'placeholder'"
check_pattern "Postgres URL with creds" 'postgresql://[^:]+:[^@]+@' ""

if [ "$FOUND" -eq 1 ]; then
  echo ""
  echo "Secret scan FAILED. Remediate findings or use os.getenv()."
  exit 1
fi

echo "Secret scan passed."
exit 0
