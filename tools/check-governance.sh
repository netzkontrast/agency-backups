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
FM_TOOLCHAIN="${FM_TOOLCHAIN:-0}"

echo "=== agency check-governance ==="

echo ""
echo "--- [1/3] Frontmatter linter ---"
# Task 016: dual-run during the migration window. The legacy validator
# decides the exit code by default; fm-validate runs in advisory mode.
# Set FM_TOOLCHAIN=1 to flip the gate (Task 017 makes that the default).
if [ "$FM_TOOLCHAIN" = "1" ]; then
  echo "(FM_TOOLCHAIN=1 — fm-validate is the gate; legacy runs advisory)"
  if ! "$PYTHON" tools/fm/validate.py; then
    FAIL=1
  fi
  echo "--- legacy validate-frontmatter.py (advisory) ---"
  "$PYTHON" tools/validate-frontmatter.py || true
else
  if ! "$PYTHON" tools/validate-frontmatter.py; then
    FAIL=1
  fi
  if [ -f "tools/fm/validate.py" ]; then
    echo "--- fm-validate (advisory; set FM_TOOLCHAIN=1 to gate) ---"
    "$PYTHON" tools/fm/validate.py >/dev/null 2>&1 || true
  fi
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

# Optional: narrative-ontology validator (gated on the ontology file existing,
# so the rest of the repo doesn't break if narrative-ontology is removed).
NARRATIVE_ONTOLOGY="$REPO_ROOT/maintenance/schemas/narrative-ontology/ontology.json"
if [ -f "$NARRATIVE_ONTOLOGY" ]; then
  echo ""
  echo "--- [opt] Narrative-ontology validator ---"
  if ! "$PYTHON" tools/dramatica-nav/validate.py; then
    FAIL=1
  fi
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
