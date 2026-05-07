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
# Task 017 flipped the default: fm-validate is now the gate; the legacy
# validator runs advisory and is silenced by default. Set FM_TOOLCHAIN=0
# to revert (e.g., for the duration of a contested migration step).
FM_TOOLCHAIN="${FM_TOOLCHAIN:-1}"
export FM_LEGACY_QUIET="${FM_LEGACY_QUIET:-1}"

echo "=== agency check-governance ==="

echo ""
echo "--- [1/6] Frontmatter linter ---"
if [ "$FM_TOOLCHAIN" = "1" ]; then
  if ! "$PYTHON" tools/fm/validate.py --type-check; then
    FAIL=1
  fi
  echo "--- legacy validate-frontmatter.py (advisory; one release window) ---"
  "$PYTHON" tools/legacy/validate-frontmatter.py >/dev/null 2>&1 || true
else
  echo "(FM_TOOLCHAIN=0 — legacy validator gates; fm-validate runs advisory)"
  if ! "$PYTHON" tools/legacy/validate-frontmatter.py; then
    FAIL=1
  fi
  echo "--- fm-validate (advisory) ---"
  "$PYTHON" tools/fm/validate.py >/dev/null 2>&1 || true
fi

echo ""
echo "--- [2/6] Directory-structure linter ---"
if ! "$PYTHON" tools/lint-structure.py; then
  FAIL=1
fi

echo ""
echo "--- [3/6] Cross-reference linkage (folded into fm-validate --type-check) ---"
echo "(legacy tools/lint-linkage.py is now a shim around fm-validate --type-check; checked above)"

echo ""
echo "--- [4/6] Run-log record validator ---"
if ! "$PYTHON" tools/lint-runlog.py; then
  FAIL=1
fi

echo ""
echo "--- [5/6] ADR governance validator (Task 028) ---"
if ! "$PYTHON" tools/adr/cli.py validate; then
  FAIL=1
fi

echo ""
echo "--- [adv] RFC 2119 polarity audit (Task 032 ST-3, ASM-001 mitigation) ---"
# Advisory by default — emits WARN diagnostics for human review of candidate
# MUST / MUST NOT polarity inversions. Pass --strict to gate the governance
# suite on a clean polarity scan (any candidate pair becomes blocking). Scope:
# root specs + research/<slug>/output/SPEC.md + decisions/<NNNN>-<slug>.md
# (the corpus that feeds tools/adr/synthesize.py).
POLARITY_STRICT=0
for arg in "$@"; do
  if [ "$arg" = "--strict" ]; then
    POLARITY_STRICT=1
  fi
done
POLARITY_TARGETS=(
  AGENTS.md TASK.md PROMPT.md RESEARCH.md
  FOLDERS.md PRE_COMMIT.md FRUSTRATED.md MAINTENANCE.md
)
# research/*/output/SPEC.md and decisions/*.md are globbed; silently skip
# patterns that don't match (fresh repos may lack either set).
for f in research/*/output/SPEC.md; do
  [ -f "$f" ] && POLARITY_TARGETS+=("$f")
done
for f in decisions/*.md; do
  [ -f "$f" ] && [ "$(basename "$f")" != "readme.md" ] && POLARITY_TARGETS+=("$f")
done
POLARITY_OUT="$(mktemp)"
"$PYTHON" tools/check-rfc2119-polarity.py "${POLARITY_TARGETS[@]}" \
  > "$POLARITY_OUT" 2>&1 || true
cat "$POLARITY_OUT"
if [ "$POLARITY_STRICT" -eq 1 ]; then
  # Any line tagged WARN:RFC2119.POLARITY is a candidate pair — gate.
  if grep -q "WARN:RFC2119.POLARITY" "$POLARITY_OUT"; then
    echo "polarity audit (--strict): candidate pair(s) detected; gating commit."
    FAIL=1
  fi
fi
rm -f "$POLARITY_OUT"

echo ""
echo "--- [6/6] Tasks-index freshness (TASK.md §7.11) ---"
if ! "$PYTHON" tools/fm/index_diff.py; then
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

  echo ""
  echo "--- [opt] Dramatica corpus cleanup linter (Task 030 ST-6) ---"
  if ! "$PYTHON" tools/dramatica-nav/cleanup.py --check; then
    FAIL=1
  fi
fi

echo ""
echo "--- [opt] Assumption-log substance linter (Task 032 ST-4 — advisory) ---"
# AGENTS.md §60-65 / FOLDERS.md F.3 enforcement. WARN-tier only — never gates.
"$PYTHON" tools/check-assumption-log.py tasks/ research/ || true

echo ""
echo "--- [opt] Duplicate task_id linter (Task 033 ST-3 — TASK.md §8.1) ---"
# Closes the agent-responsibility-only enforcement window acknowledged in
# TASK.md §8.1. Advisory by default during the migration window
# (Task 043 renumbers the existing 006/006, 009/009, 031/031, 032/032
# collisions). Set FM_DUPLICATE_TASK_ID_STRICT=1 to gate the suite once
# Task 043 lands and the collisions are resolved.
DUPLICATE_TASK_ID_OUT="$(mktemp)"
"$PYTHON" tools/fm/check-duplicate-task-id.py tasks/ \
  > "$DUPLICATE_TASK_ID_OUT" 2>&1
DUPLICATE_TASK_ID_RC=$?
cat "$DUPLICATE_TASK_ID_OUT"
rm -f "$DUPLICATE_TASK_ID_OUT"
if [ "${FM_DUPLICATE_TASK_ID_STRICT:-0}" = "1" ] && [ "$DUPLICATE_TASK_ID_RC" -ne 0 ]; then
  FAIL=1
fi

# Optional WARN-tier: narrative-ontology load discipline (AGENTS.md NO.5,
# Task 032 ST-2). Advisory only — never sets FAIL=1. Targets the most
# recently-touched task.md when one exists; otherwise no-ops on `tasks/`.
# Exit code 2 is the WARN signal and is intentionally swallowed here.
echo ""
echo "--- [opt] Narrative-ontology load discipline (AGENTS.md NO.5, WARN-tier) ---"
NARRATIVE_LOAD_TARGET=""
if [ -d "tasks" ]; then
  NARRATIVE_LOAD_TARGET="$(find tasks -mindepth 2 -maxdepth 2 -name task.md -printf '%T@ %h\n' 2>/dev/null \
    | sort -nr | head -n1 | awk '{print $2}')"
  if [ -z "$NARRATIVE_LOAD_TARGET" ]; then
    NARRATIVE_LOAD_TARGET="tasks"
  fi
fi
if [ -n "$NARRATIVE_LOAD_TARGET" ]; then
  "$PYTHON" tools/check-narrative-ontology-load.py "$NARRATIVE_LOAD_TARGET" || true
fi

if [ "$SKIP_TRUST" -eq 0 ]; then
  echo ""
  echo "--- [trust] Spec-J/K/L trust audit ---"
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
