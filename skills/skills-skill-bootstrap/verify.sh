#!/usr/bin/env bash
# verify.sh — compare ~/.claude/skills/ against origin/main:/skills/
#
# Usage: verify.sh [--target DIR] [--help]
#
# Prints per-skill status: OK | MISSING | DIVERGED
# Also lists LOCAL-ONLY skills (present locally but absent from repo).
# Exit codes:
#   0  all canonical skills present and in sync
#   1  one or more skills missing or diverged (run sync.sh to fix)
#   2  unexpected error

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
TARGET_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET_DIR="$2"; shift 2 ;;
    --help)
      echo "Usage: verify.sh [--target DIR]"
      echo "  Exit 0 = all canonical skills in sync."
      echo "  Exit 1 = missing or diverged skills. Exit 2 = error."
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

log()  { echo "[verify] $*"; }
warn() { echo "[verify] WARN: $*" >&2; }

log "Fetching origin/main..."
git -C "$REPO_ROOT" fetch origin main --quiet
MAIN_SHA="$(git -C "$REPO_ROOT" rev-parse origin/main)"

# Collect canonical skill dirs (-d --name-only: tree objects only, names only)
REPO_SKILLS=()
while IFS= read -r name; do
  [[ "$name" == "skills-skill-bootstrap" ]] && continue
  [[ "$name" == "skills-skill" ]]           && continue
  REPO_SKILLS+=("$name")
done < <(
  git -C "$REPO_ROOT" ls-tree -d --name-only origin/main:skills/ 2>/dev/null || true
)

if [[ ${#REPO_SKILLS[@]} -eq 0 ]]; then
  warn "origin/main:skills/ contains no skill directories."
  log "Nothing to verify. Treating as in-sync."
  exit 0
fi

IN_SYNC=0
MISSING=0
DIVERGED=0

for skill_name in "${REPO_SKILLS[@]}"; do
  local_file="$TARGET_DIR/$skill_name/SKILL.md"

  if [[ ! -f "$local_file" ]]; then
    echo "MISSING:  $skill_name"
    (( MISSING++ )) || true
    continue
  fi

  remote_tmp="$(mktemp)"
  git -C "$REPO_ROOT" show "origin/main:skills/$skill_name/SKILL.md" > "$remote_tmp" 2>/dev/null || true

  if cmp -s "$remote_tmp" "$local_file"; then
    echo "OK:       $skill_name"
    (( IN_SYNC++ )) || true
  else
    echo "DIVERGED: $skill_name  (local differs from origin/main)"
    (( DIVERGED++ )) || true
  fi
  rm -f "$remote_tmp"
done

# Report local-only skills (informational — not a failure)
if [[ -d "$TARGET_DIR" ]]; then
  REPO_SET=" ${REPO_SKILLS[*]} "
  for local_dir in "$TARGET_DIR"/*/; do
    [[ -d "$local_dir" ]] || continue
    local_name="$(basename "$local_dir")"
    if [[ "$REPO_SET" != *" $local_name "* ]]; then
      echo "LOCAL:    $local_name  (not in repo — managed outside skills-skill-bootstrap)"
    fi
  done
fi

echo ""
log "Source: origin/main @ ${MAIN_SHA:0:7}"
log "Result: $IN_SYNC in-sync, $MISSING missing, $DIVERGED diverged"
log "Target: $TARGET_DIR"

if [[ $MISSING -gt 0 || $DIVERGED -gt 0 ]]; then
  log "Run skills/skills-skill-bootstrap/sync.sh to fix."
  exit 1
fi

log "All canonical skills in sync."
exit 0
