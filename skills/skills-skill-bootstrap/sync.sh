#!/usr/bin/env bash
# sync.sh — pull skill bodies from origin/main:/skills/ into ~/.claude/skills/
#
# Usage: sync.sh [--clean] [--target DIR] [--dry-run] [--list] [--help]
#
# --clean     also remove local skills absent from origin/main:/skills/
# --target    override destination (default: ~/.claude/skills/)
# --dry-run   print what would happen; make no changes
# --list      list skills available in origin/main without syncing
# --help      show usage
#
# Exit codes:
#   0  success (including no-op when everything is already in sync)
#   1  unexpected error (git failure, permission denied, SKILL.md missing, etc.)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"

TARGET_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
CLEAN_MODE=false
DRY_RUN=false
LIST_ONLY=false

# ---------- argument parsing ----------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --clean)    CLEAN_MODE=true;      shift ;;
    --dry-run)  DRY_RUN=true;         shift ;;
    --list)     LIST_ONLY=true;       shift ;;
    --target)   TARGET_DIR="$2";      shift 2 ;;
    --help)
      echo "Usage: sync.sh [--clean] [--target DIR] [--dry-run] [--list] [--help]"
      echo ""
      echo "  --clean     remove local skills absent from origin/main:/skills/"
      echo "  --target    override destination (default: ~/.claude/skills/)"
      echo "  --dry-run   print what would change; make no changes"
      echo "  --list      list skills in origin/main and exit (no changes)"
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
MAIN_SHA="$(git -C "$REPO_ROOT" rev-parse origin/main)"

# ---------- discover skill directories in repo ----------
# -d --name-only: lists only tree objects (directories), names only.
# This naturally skips non-directory entries like readme.md.
REPO_SKILLS=()
while IFS= read -r name; do
  [[ "$name" == "skills-skill-bootstrap" ]] && continue
  [[ "$name" == "skills-skill" ]]           && continue
  REPO_SKILLS+=("$name")
done < <(
  git -C "$REPO_ROOT" ls-tree -d --name-only origin/main:skills/ 2>/dev/null || true
)

if [[ ${#REPO_SKILLS[@]} -eq 0 ]]; then
  warn "origin/main:skills/ contains no skill directories (pre-Stage-A or empty)."
  log "Nothing to sync. Exiting cleanly."
  exit 0
fi

# ---------- --list mode ----------
if [[ "$LIST_ONLY" == "true" ]]; then
  log "Skills available in origin/main @ ${MAIN_SHA:0:7}:"
  for skill_name in "${REPO_SKILLS[@]}"; do
    echo "  - $skill_name"
  done
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

  # Write directly from git to avoid command-substitution stripping on large files
  remote_tmp="$(mktemp)"
  if ! git -C "$REPO_ROOT" show "origin/main:skills/$skill_name/SKILL.md" > "$remote_tmp" 2>/dev/null; then
    warn "$skill_name: SKILL.md not found in origin/main:skills/$skill_name/ — skipping"
    rm -f "$remote_tmp"
    (( ERRORS++ )) || true
    continue
  fi

  # Check if already in sync
  if [[ -f "$dest_file" ]] && cmp -s "$remote_tmp" "$dest_file"; then
    log "ok (already in sync): $skill_name"
    rm -f "$remote_tmp"
    (( SKIPPED++ )) || true
    continue
  fi

  if [[ "$DRY_RUN" == "true" ]]; then
    dry "would sync: $skill_name → $dest_file"
    rm -f "$remote_tmp"
    (( SYNCED++ )) || true
    continue
  fi

  mkdir -p "$dest"
  mv "$remote_tmp" "$dest_file"
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
        dry "would remove (absent from repo, --clean): $local_name"
      else
        log "removing (absent from repo, --clean): $local_name"
        rm -rf "$local_dir"
      fi
    fi
  done
fi

# ---------- summary ----------
echo ""
log "Sync complete: $SYNCED synced, $SKIPPED already-in-sync, $ERRORS errors"
log "Source: origin/main @ ${MAIN_SHA:0:7}"
log "Target: $TARGET_DIR"

if [[ $ERRORS -gt 0 ]]; then
  exit 1
fi
exit 0
