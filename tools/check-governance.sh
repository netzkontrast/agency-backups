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
echo "--- [2b/6] Readme L1 frontmatter linter (Task 036 ST-1 — FOLDERS.md F.5) ---"
# Promotes F.5 from SHOULD to MUST; checks L1 Vault Core key presence
# and folder-slug containment for every operational readme.md. Provider
# research sub-trees and /decisions/ are exempt per FOLDERS.md F.1.1 / §8.
if ! "$PYTHON" tools/check-readme-frontmatter.py; then
  FAIL=1
fi

echo ""
echo "--- [2c/6] Clean working directory linter (Task 037 ST-2 — PRE_COMMIT.md PC.1.1) ---"
# Mechanises the PC.1.1 "no .py/.sh script scratchpads, no loose log dumps"
# rule across the whole working tree. Exempts /tools/, /tests/, /skills/,
# /templates/, /maintenance/, /decisions/, /Agency-System/, /.githooks/
# per FOLDERS.md §8. session.log is always allowed (RESEARCH.md §4.5).
# Per-repo carve-outs live in tools/.script-allowlist.
if ! "$PYTHON" tools/check-clean-working-directory.py; then
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
echo "--- [opt] Audit-graph consistency linter (Task 036 ST-2 — FOLDERS.md F.6) ---"
# Detects body-link-without-frontmatter dual-surface drift. WARN-tier;
# never gates. Set FM_AUDIT_GRAPH_STRICT=1 to gate once corpus drift is
# remediated.
AG_OUT="$(mktemp)"
AG_RC=0
"$PYTHON" tools/check-audit-graph-consistency.py \
  > "$AG_OUT" 2>&1 || AG_RC=$?
cat "$AG_OUT"
rm -f "$AG_OUT"
if [ "${FM_AUDIT_GRAPH_STRICT:-0}" = "1" ] && [ "$AG_RC" -ne 0 ]; then
  FAIL=1
fi

echo ""
echo "--- [opt] Assumption-log substance linter (Task 032 ST-4 — advisory) ---"
# AGENTS.md §60-65 / FOLDERS.md F.3 enforcement. WARN-tier only — never gates.
"$PYTHON" tools/check-assumption-log.py tasks/ research/ || true

echo ""
echo "--- [opt] Dynamic-readme partition linter (Task 039 ST-4 — MAINTENANCE.md §3.2) ---"
# repo-maintenance-protocol-spec §3.1 enforcement. WARN-tier only — never gates.
# Falsification mitigation per Task 039 ST-4 brief: readmes lacking the
# `<!-- BEGIN DYNAMIC -->` / `<!-- END DYNAMIC -->` markers emit a one-time
# `missing-marker` advisory rather than an ERROR, so the linter does not
# retroactively break the existing corpus.
"$PYTHON" tools/maintenance/dynamic-readme-partition.py tasks/ research/ prompts/ || true

echo ""
echo ""
echo "--- [opt] Prompt self-containedness linter (Task 034 ST-2, PROMPT.md §6.4 — advisory) ---"
# PROMPT.md §5.1 / P.B.6 anchor. WARN-tier — emits to stderr, never gates.
PROMPT_FILES=$(find prompts -maxdepth 2 -name prompt.md 2>/dev/null)
if [ -n "$PROMPT_FILES" ]; then
  "$PYTHON" tools/check-prompt-self-containedness.py $PROMPT_FILES || true
fi

echo ""
echo "--- [opt] Prompt framework-declaration linter (Task 034 ST-3, PROMPT.md §6.4.b — advisory) ---"
# PROMPT.md §5.2 / P.B.4 anchor. WARN-tier — emits to stderr, never gates.
if [ -n "$PROMPT_FILES" ]; then
  "$PYTHON" tools/check-prompt-framework-declaration.py $PROMPT_FILES || true
fi

echo ""
echo "--- [opt] Duplicate task_id linter (Task 033 ST-3 — TASK.md §8.1) ---"
# Closes the agent-responsibility-only enforcement window acknowledged in
# TASK.md §8.1. Advisory by default during the migration window
# (Task 043 renumbers the existing 006/006, 009/009, 031/031, 032/032
# collisions). Set FM_DUPLICATE_TASK_ID_STRICT=1 to gate the suite once
# Task 043 lands and the collisions are resolved.
DUPLICATE_TASK_ID_OUT="$(mktemp)"
DUPLICATE_TASK_ID_RC=0
"$PYTHON" tools/fm/check-duplicate-task-id.py tasks/ \
  > "$DUPLICATE_TASK_ID_OUT" 2>&1 || DUPLICATE_TASK_ID_RC=$?
cat "$DUPLICATE_TASK_ID_OUT"
rm -f "$DUPLICATE_TASK_ID_OUT"
if [ "${FM_DUPLICATE_TASK_ID_STRICT:-0}" = "1" ] && [ "$DUPLICATE_TASK_ID_RC" -ne 0 ]; then
  FAIL=1
fi

echo ""
echo "--- [opt] Workspace cleanliness linter (Task 035 ST-2 — RESEARCH.md R.4.4) ---"
# Closes the §5.3 enforcement gap. WARN-tier by default during the
# migration window (existing closed workspaces may carry historical
# stragglers); set FM_WORKSPACE_CLEANLINESS_STRICT=1 to gate.
WS_CLEAN_OUT="$(mktemp)"
WS_CLEAN_RC=0
"$PYTHON" tools/check-workspace-cleanliness.py \
  > "$WS_CLEAN_OUT" 2>&1 || WS_CLEAN_RC=$?
cat "$WS_CLEAN_OUT"
rm -f "$WS_CLEAN_OUT"
if [ "${FM_WORKSPACE_CLEANLINESS_STRICT:-0}" = "1" ] && [ "$WS_CLEAN_RC" -ne 0 ]; then
  FAIL=1
fi

echo ""
echo "--- [opt] External-result downstream-Task linter (Task 035 ST-3 — RESEARCH.md R.6.5) ---"
# Closes the §6.5 enforcement gap: every research/<provider>/<slug>/result.md
# MUST have a back-linked Task. Advisory by default; set
# FM_EXTERNAL_RESULT_STRICT=1 to gate once historical results are linked.
EXT_RES_OUT="$(mktemp)"
EXT_RES_RC=0
"$PYTHON" tools/check-external-result-downstream-task.py \
  > "$EXT_RES_OUT" 2>&1 || EXT_RES_RC=$?
cat "$EXT_RES_OUT"
rm -f "$EXT_RES_OUT"
if [ "${FM_EXTERNAL_RESULT_STRICT:-0}" = "1" ] && [ "$EXT_RES_RC" -ne 0 ]; then
  FAIL=1
fi

echo ""
echo "--- [opt] Trust-audit GATE (Task 035 ST-4 — RESEARCH.md §5.7, Spec-J/K/L) ---"
# Per-workspace trust-audit gate. Runs over every research/<slug>/ workspace
# whose readme.md declares research_phase: complete. Advisory by default; set
# FM_TRUST_AUDIT_STRICT=1 to gate. Cross-workspace aggregation is owned by
# Task 039 (MAINTENANCE.md AGGREGATOR), per the C3 partition.
TRUST_OUT="$(mktemp)"
TRUST_RC=0
for ws in research/*/; do
  ws="${ws%/}"
  base="$(basename "$ws")"
  case "$base" in
    gemini|gpt|human|other) continue ;;
  esac
  readme="$ws/readme.md"
  [ -f "$readme" ] || continue
  if grep -q "^research_phase: complete" "$readme" 2>/dev/null; then
    if ! "$PYTHON" tools/check-trust-audit.py "$ws" >> "$TRUST_OUT" 2>&1; then
      TRUST_RC=1
    fi
  fi
done
cat "$TRUST_OUT"
rm -f "$TRUST_OUT"
if [ "${FM_TRUST_AUDIT_STRICT:-0}" = "1" ] && [ "$TRUST_RC" -ne 0 ]; then
  FAIL=1
fi

echo ""
echo "--- [opt] Trust-audit AGGREGATOR (Task 039 ST-5 — MAINTENANCE.md §3.2, C3 partition) ---"
# Cross-research roll-up of the per-workspace GATE above. Imports
# tools/check-trust-audit.py's DIAGNOSTIC_SCHEMA + audit() callable;
# never re-implements per-workspace logic. Advisory by default — set
# FM_TRUST_AUDIT_AGGREGATOR_STRICT=1 to gate. Surfaces FL≥1 trust failures
# as MAINT.TRUST.FRICTION recommendations for §3.3 task-delegation.
TRUST_AGG_OUT="$(mktemp)"
TRUST_AGG_RC=0
TRUST_AGG_MODE="advisory"
if [ "${FM_TRUST_AUDIT_AGGREGATOR_STRICT:-0}" = "1" ]; then
  TRUST_AGG_MODE="strict"
fi
"$PYTHON" tools/maintenance/trust-audit.py --threshold-mode "$TRUST_AGG_MODE" \
  > "$TRUST_AGG_OUT" 2>&1 || TRUST_AGG_RC=$?
cat "$TRUST_AGG_OUT"
rm -f "$TRUST_AGG_OUT"
if [ "${FM_TRUST_AUDIT_AGGREGATOR_STRICT:-0}" = "1" ] && [ "$TRUST_AGG_RC" -ne 0 ]; then
  FAIL=1
fi

echo ""
echo "--- [opt] FL declaration linter (Task 038 ST-2 — FRUSTRATED.md FR.B.4) ---"
# Per FRUSTRATED.md §FL.Log enforcement. Advisory by default; set
# FM_FL_DECLARATION_STRICT=1 to gate. Targets every closed Task's
# friction-log.md and every research workspace reflection log.
FL_DECL_OUT="$(mktemp)"
FL_DECL_RC=0
FL_DECL_TARGETS="$(find tasks -mindepth 2 -maxdepth 2 -name friction-log.md 2>/dev/null) \
$(find research -mindepth 3 -maxdepth 3 -path '*/reflection/friction-log.md' 2>/dev/null)"
if [ -n "$(echo "$FL_DECL_TARGETS" | tr -s ' \n' ' ' | sed 's/^ *//;s/ *$//')" ]; then
  # shellcheck disable=SC2086
  "$PYTHON" tools/check-fl-declaration.py $FL_DECL_TARGETS \
    > "$FL_DECL_OUT" 2>&1 || FL_DECL_RC=$?
  cat "$FL_DECL_OUT"
fi
rm -f "$FL_DECL_OUT"
if [ "${FM_FL_DECLARATION_STRICT:-0}" = "1" ] && [ "$FL_DECL_RC" -ne 0 ]; then
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
