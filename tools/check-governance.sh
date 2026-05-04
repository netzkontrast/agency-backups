#!/usr/bin/env bash
# Thin shim that invokes the pre-commit governance suite without requiring
# Git to be configured. Use this for CI or manual verification.
#
# Usage: tools/check-governance.sh [--no-trust]
#
# Flags:
#   --no-trust   Skip the Spec-J/K/L trust audit (check-trust.py).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

PYTHON="${PYTHON:-python3}"
SKIP_TRUST=0
for arg in "$@"; do
  if [ "$arg" = "--no-trust" ]; then
    SKIP_TRUST=1
  fi
done

FAIL=0

echo "=== agency check-governance ==="

echo ""
echo "--- [1/3] Frontmatter linter ---"
if ! "$PYTHON" tools/validate-frontmatter.py; then
  FAIL=1
fi

echo ""
echo "--- [2/3] Directory-structure linter ---"
if ! "$PYTHON" tools/lint-structure.py; then
  FAIL=1
fi

echo ""
echo "--- [3/3] Cross-reference linkage linter ---"
if ! "$PYTHON" tools/lint-linkage.py; then
  FAIL=1
fi

echo ""
echo "--- [4/4] Run-log record validator ---"
if ! "$PYTHON" tools/lint-runlog.py; then
  FAIL=1
fi

if [ "$SKIP_TRUST" -eq 0 ]; then
  echo ""
  echo "--- [5/5] Spec-J/K/L trust audit ---"
  if ! "$PYTHON" tools/check-trust.py; then
    FAIL=1
  fi
fi

echo ""
if [ "$FAIL" -eq 1 ]; then
  echo "=== FAIL: one or more checks failed. ==="
  exit 1
else
  echo "=== PASS: all governance checks passed. ==="
fi
