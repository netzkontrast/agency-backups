#!/usr/bin/env bash
# sync.sh — pull skill bodies from origin/main:/skills/ into ~/.claude/skills/
#
# Usage: sync.sh [--clean] [--target DIR] [--dry-run] [--help]
#
# --clean     also remove local skills absent from origin/main:/skills/
# --target    override destination (default: ~/.claude/skills/)
# --dry-run   print what would happen; make no changes
# --help      show usage
#
# Exit codes:
#   0  success (even if origin/main has no /skills/ yet)
#   1  unexpected error (git failure, permission denied, etc.)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"

TARGET_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
CLEAN_MODE=false
DRY_RUN=false

# ---------- argument parsing ----------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --clean)    CLEAN_MODE=true;      shift ;;
    --dry-run)  DRY_RUN=true;         shift ;;
    --target)   TARGET_DIR="$2";      shift 2 ;;
    --help)
      echo "Usage: sync.sh [--clean] [--target DIR] [--dry-run] [--help]"
      echo ""
      echo "  --clean     remove local skills absent from origin/main:/skills/"
      echo "  --target    override destination (default: ~/.claude/skills/)"
      echo "  --dry-run   print what would change; make no changes"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

# ---------- helpers ----------
log()  { echo "[sync] $*"; }
warn() { echo "[sync] WARN: $*" >&2; }
dry()  { echo "[sync] DRY-RUN: $*"; }

# ---------- fetch origin/main ----------
log "Fetching origin/main..."
git -C "$REPO_ROOT" fetch origin main --quiet

# ---------- discover skills in repo ----------
# ls-tree returns empty if the path doesn't exist in the tree yet (pre-Stage-A).
REPO_SKILLS=()
while IFS= read -r name; do
  # Skip management/reserved folders
  [[ "$name" == "skills-skill-bootstrap" ]] && continue
  [[ "$name" == "skills-skill" ]]           && continue
  REPO_SKILLS+=("$name")
done < <(
  git -C "$REPO_ROOT" ls-tree --name-only origin/main:skills/ 2>/dev/null || true
)

if [[ ${#REPO_SKILLS[@]} -eq 0 ]]; then
  warn "origin/main:skills/ is empty or does not exist yet (expected before Stage A merges)."
  log "Nothing to sync. Exiting cleanly."
  exit 0
fi

# ---------- sync each skill ----------
SYNCED=0
SKIPPED=0
ERRORS=0

mkdir -p "$TARGET_DIR"

for skill_name in "${REPO_SKILLS[@]}"; do
  dest="$TARGET_DIR/$skill_name"
  dest_file="$dest/SKILL.md"

  # Fetch remote content
  remote_content=""
  if ! remote_content="$(git -C "$REPO_ROOT" show "origin/main:skills/$skill_name/SKILL.md" 2>/dev/null)"; then
    warn "$skill_name: SKILL.md not found in origin/main:skills/$skill_name/ — skipping"
    (( ERRORS++ )) || true
    continue
  fi

  # Check if already in sync
  if [[ -f "$dest_file" ]]; then
    local_content="$(cat "$dest_file")"
    if [[ "$remote_content" == "$local_content" ]]; then
      log "ok (already in sync): $skill_name"
      (( SKIPPED++ )) || true
      continue
    fi
  fi

  if [[ "$DRY_RUN" == "true" ]]; then
    dry "would sync: $skill_name → $dest_file"
    (( SYNCED++ )) || true
    continue
  fi

  mkdir -p "$dest"
  printf '%s\n' "$remote_content" > "$dest_file"
  log "synced: $skill_name"
  (( SYNCED++ )) || true
done

# ---------- clean mode: remove local skills absent from repo ----------
if [[ "$CLEAN_MODE" == "true" && -d "$TARGET_DIR" ]]; then
  REPO_SET=" ${REPO_SKILLS[*]} "
  for local_dir in "$TARGET_DIR"/*/; do
    [[ -d "$local_dir" ]] || continue
    local_name="$(basename "$local_dir")"
    if [[ "$REPO_SET" != *" $local_name "* ]]; then
      if [[ "$DRY_RUN" == "true" ]]; then
        dry "would remove (--clean): $local_name"
      else
        log "removing (--clean): $local_name"
        rm -rf "$local_dir"
      fi
    fi
  done
fi

# ---------- summary ----------
echo ""
log "Sync complete: $SYNCED synced, $SKIPPED already-in-sync, $ERRORS errors"
log "Target: $TARGET_DIR"

if [[ $ERRORS -gt 0 ]]; then
  exit 1
fi
exit 0
