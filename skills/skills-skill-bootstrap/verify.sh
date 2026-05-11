#!/usr/bin/env bash
# verify.sh — compare ~/.claude/skills/ against origin/main:/skills/
#
# Usage: verify.sh [--target DIR] [--help]
#
# Per-skill status: OK | MISSING | DIVERGED | MISSING-SUB | BUNDLE-MISSING |
#                   BUNDLE-DRIFT | ERROR.
# Also lists LOCAL-only skills (present locally but absent from repo).
#
# Authority: decisions/0007-skill-bundles-tools-frontmatter.md (ADR-0007).
#
# Exit codes:
#   0  all canonical skills + declared bundles in sync
#   1  any skill or bundle missing / diverged (run sync.sh to fix)
#   2  unexpected error (git show / archive failure)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
TARGET_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET_DIR="$2"; shift 2 ;;
    --help)
      sed -n '2,15p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
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

read_bundles_local() {
  local skill_md="$1"
  [[ -f "$skill_md" ]] || return 0
  python3 "$REPO_ROOT/tools/fm/extract.py" \
    "$skill_md" --frontmatter skill_bundles_tools 2>/dev/null \
    | sed -e '/^$/d' -e 's/^- *//' -e 's/^"//' -e 's/"$//' || true
}

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
SUB_MISSING=0
BUNDLE_OK=0
BUNDLE_BAD=0
FETCH_ERR=0

for skill_name in "${REPO_SKILLS[@]}"; do
  local_file="$TARGET_DIR/$skill_name/SKILL.md"

  if [[ ! -f "$local_file" ]]; then
    echo "MISSING:  $skill_name"
    (( MISSING++ )) || true
    continue
  fi

  remote_tmp="$(mktemp)"
  if ! git -C "$REPO_ROOT" show "origin/main:skills/$skill_name/SKILL.md" > "$remote_tmp" 2>/dev/null; then
    echo "ERROR:    $skill_name  (git show failed for origin/main:skills/$skill_name/SKILL.md)"
    rm -f "$remote_tmp"
    (( FETCH_ERR++ )) || true
    continue
  fi

  if cmp -s "$remote_tmp" "$local_file"; then
    echo "OK:       $skill_name"
    (( IN_SYNC++ )) || true
  else
    echo "DIVERGED: $skill_name  (local SKILL.md differs from origin/main)"
    (( DIVERGED++ )) || true
  fi
  rm -f "$remote_tmp"

  # ----- subtree presence (scripts/, references/, assets/) -----
  for sub in scripts references assets; do
    if git -C "$REPO_ROOT" ls-tree origin/main "skills/$skill_name/$sub" \
         --name-only 2>/dev/null | grep -q .; then
      if [[ ! -d "$TARGET_DIR/$skill_name/$sub" ]]; then
        echo "MISSING-SUB: $skill_name/$sub"
        (( SUB_MISSING++ )) || true
      fi
    fi
  done

  # ----- bundle parity -----
  bundles=()
  while IFS= read -r entry; do
    [[ -z "$entry" ]] || bundles+=("$entry")
  done < <(read_bundles_local "$local_file")

  bundle_root="$TARGET_DIR/$skill_name/scripts/_bundled"
  for slug_path in "${bundles[@]}"; do
    base="$(basename "$slug_path")"
    dst="$bundle_root/$base"
    src="$REPO_ROOT/$slug_path"
    if [[ ! -d "$dst" ]]; then
      echo "BUNDLE-MISSING: $skill_name → $slug_path"
      (( BUNDLE_BAD++ )) || true
      continue
    fi
    expected="$( ( cd "$src" && find . -type f ! -name '.bundle.sha256' \
                  -exec sha256sum {} \; | LC_ALL=C sort ) )"
    actual="$( [[ -f "$dst/.bundle.sha256" ]] && cat "$dst/.bundle.sha256" || echo "" )"
    if [[ "$expected" == "$actual" ]]; then
      (( BUNDLE_OK++ )) || true
    else
      echo "BUNDLE-DRIFT: $skill_name → $slug_path"
      (( BUNDLE_BAD++ )) || true
    fi
  done
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
log "SKILL.md: $IN_SYNC in-sync, $MISSING missing, $DIVERGED diverged"
log "Subtrees: $SUB_MISSING missing-sub"
log "Bundles:  $BUNDLE_OK in-sync, $BUNDLE_BAD missing-or-drifted"
log "Target:   $TARGET_DIR"

if [[ $FETCH_ERR -gt 0 ]]; then
  log "git show failed for one or more skills; check origin/main and network."
  exit 2
fi

if (( MISSING + DIVERGED + SUB_MISSING + BUNDLE_BAD > 0 )); then
  log "Run skills/skills-skill-bootstrap/sync.sh to fix."
  exit 1
fi

log "All canonical skills + bundles in sync."
exit 0
