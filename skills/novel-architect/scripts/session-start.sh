#!/bin/bash
# session-start.sh — Lean SessionStart-Hook für novel-architect (v1.1.0)
#
# Aufgabe: nach Bootstrap des Roman-Workspaces eine token-cheap Roll-Up der
# learnings.md (MIF Level 3) und der unresolved canon-meta entries auf STDOUT
# emittieren. Kein Body-Load der Einträge — nur Card-Blöcke pro Entry.
#
# Per AGENTS.md Bootstrap-Protocol: dieser Hook läuft NACH ./install.sh und
# NACH der Workspace-Detection, aber VOR der Phase-Routing-Entscheidung.
#
# Usage:
#   bash skills/novel-architect/scripts/session-start.sh <project-slug>
#
# Env:
#   NOVEL_ARCHITECT_PROJECTS_ROOT  — projects root override (default: /home/claude/novel-projects)

set -euo pipefail

SLUG="${1:-}"
if [ -z "$SLUG" ]; then
    echo "Usage: bash session-start.sh <project-slug>" >&2
    exit 1
fi

if ! [[ "$SLUG" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo "ERROR: slug must be kebab-case: $SLUG" >&2
    exit 1
fi

PROJECTS_ROOT="${NOVEL_ARCHITECT_PROJECTS_ROOT:-/home/claude/novel-projects}"
WORKSPACE="$PROJECTS_ROOT/$SLUG"

if [ ! -d "$WORKSPACE" ]; then
    echo "WARN: workspace not found at $WORKSPACE — skipping session-start roll-up" >&2
    exit 0
fi

LEARNINGS="$WORKSPACE/learnings.md"
CANON_META="$WORKSPACE/canon-meta.md"

echo "=== novel-architect session-start roll-up for '$SLUG' ==="
echo ""

# ─── learnings.md (MIF Level 3) ──────────────────────────────────────────────
if [ -f "$LEARNINGS" ]; then
    # Count H2-headers that match the canonical L-YYYY-MM-DD-NNN pattern.
    # The pattern '## L-' is conservative — matches Level 3 only, ignores legacy.
    TOTAL=$(grep -c '^## L-' "$LEARNINGS" 2>/dev/null || echo 0)
    # Unresolved = entries whose card block contains "learning_resolved: false"
    UNRESOLVED=$(grep -c 'learning_resolved: false' "$LEARNINGS" 2>/dev/null || echo 0)
    echo "learnings.md (MIF Level 3): $TOTAL total / $UNRESOLVED unresolved"
    if [ "$UNRESOLVED" -gt 0 ]; then
        echo ""
        echo "Unresolved entries (severity-ordered scan; first 5):"
        # Scan card blocks; report id + phase + severity for unresolved.
        # We intentionally don't load body prose — token budget.
        awk '
            /^## L-/ {
                inside = 1; id = $2; phase = ""; sev = ""; resolved = "true"
            }
            inside && /learning_phase:/ { phase = $NF }
            inside && /learning_severity:/ { sev = $NF }
            inside && /learning_resolved: false/ { resolved = "false" }
            inside && /^$/ && id != "" {
                if (resolved == "false") {
                    printf "  - %s [%s] severity=%s\n", id, phase, sev
                    count++
                    if (count >= 5) exit
                }
                inside = 0
            }
        ' "$LEARNINGS"
    fi
else
    echo "learnings.md: not found — Phase-7 SHOULD write it at first session-end"
fi

echo ""

# ─── canon-meta.md (Canon-Status Schema) ─────────────────────────────────────
if [ -f "$CANON_META" ]; then
    PROPOSED=$(grep -c 'canon_status: proposed' "$CANON_META" 2>/dev/null || echo 0)
    CONTESTED=$(grep -c 'canon_status: contested' "$CANON_META" 2>/dev/null || echo 0)
    ACCEPTED=$(grep -c 'canon_status: accepted' "$CANON_META" 2>/dev/null || echo 0)
    echo "canon-meta.md: $ACCEPTED accepted / $PROPOSED proposed / $CONTESTED contested"
    if [ "$CONTESTED" -gt 0 ]; then
        echo "  ⚠ $CONTESTED contested entr(y/ies) — Phase 7 audit recommended"
    fi
    if [ "$PROPOSED" -gt 0 ]; then
        echo "  ! $PROPOSED proposed entr(y/ies) — askuser approval needed"
    fi
else
    echo "canon-meta.md: not found (ok for early-phase projects)"
fi

echo ""
echo "=== session-start roll-up complete ==="
