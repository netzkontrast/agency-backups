#!/bin/bash
# package_skill.sh — Wrapper for skill-creator/scripts/package_skill.py
#
# Packs novel-architect into a .skill file via the skill-creator tooling.
#
# Usage:
#   bash package_skill.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

# Find skill-creator (either in agency repo or claude.ai mount)
SKILL_CREATOR=""
for candidate in \
    "$(dirname "$SKILL_ROOT")/skill-creator/scripts/package_skill.py" \
    "/mnt/skills/examples/skill-creator/scripts/package_skill.py" \
    "/home/claude/novel-architect-workspace/tmp/skills-ref/skill-creator/scripts/package_skill.py" \
; do
    if [ -f "$candidate" ]; then
        SKILL_CREATOR="$candidate"
        break
    fi
done

if [ -z "$SKILL_CREATOR" ]; then
    echo "ERROR: package_skill.py not found." >&2
    echo "Tried:" >&2
    echo "  - $(dirname "$SKILL_ROOT")/skill-creator/scripts/package_skill.py" >&2
    echo "  - /mnt/skills/examples/skill-creator/scripts/package_skill.py" >&2
    echo "  - /home/claude/novel-architect-workspace/tmp/skills-ref/skill-creator/scripts/package_skill.py" >&2
    exit 1
fi

echo "Using packager: $SKILL_CREATOR"
echo "Packaging skill at: $SKILL_ROOT"
python3 "$SKILL_CREATOR" "$SKILL_ROOT"

echo "Skill packaged successfully."
