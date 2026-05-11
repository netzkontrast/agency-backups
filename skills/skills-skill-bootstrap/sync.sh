#!/usr/bin/env bash
# sync.sh — materialise repo skills + declared tool bundles into ~/.claude/skills/
#
# Usage: sync.sh [--clean] [--target DIR] [--dry-run] [--list]
#                [--no-bundle] [--bundle-only] [--verify-bundles] [--help]
#
# Phases per skill:
#   1. Tree sync     — full skills/<name>/ tree from origin/main is staged
#                      via `git archive` and atomically swapped in via rsync,
#                      preserving the local scripts/_bundled/ namespace.
#   2. Bundle copy   — `skill_bundles_tools` from the synced SKILL.md is read
#                      via tools/fm/extract.py; each declared tools/<slug> is
#                      mirrored into <target>/scripts/_bundled/<basename>/
#                      with rsync --checksum, plus a .bundle.sha256 sidecar.
#
# Flags:
#   --clean            remove local skills absent from origin/main:/skills/
#   --target DIR       override destination (default: ~/.claude/skills/)
#   --dry-run          print what would happen; make no changes
#   --list             list skills available in origin/main without syncing
#   --no-bundle        skip phase 2 (offline / fast path)
#   --bundle-only      skip phase 1 (re-bundle after a /tools/ change)
#   --verify-bundles   diff sources vs bundled copies; non-zero exit on drift
#   --help             show usage
#
# Authority: decisions/0007-skill-bundles-tools-frontmatter.md (ADR-0007).
#
# Exit codes:
#   0  success (including no-op when everything is already in sync)
#   1  unexpected error (git failure, permission denied, SKILL.md missing,
#      bundle source missing, or --verify-bundles detected drift)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"

TARGET_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
CLEAN_MODE=false
DRY_RUN=false
LIST_ONLY=false
NO_BUNDLE=false
BUNDLE_ONLY=false
VERIFY_BUNDLES=false

# ---------- argument parsing ----------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --clean)           CLEAN_MODE=true;      shift ;;
    --dry-run)         DRY_RUN=true;         shift ;;
    --list)            LIST_ONLY=true;       shift ;;
    --no-bundle)       NO_BUNDLE=true;       shift ;;
    --bundle-only)     BUNDLE_ONLY=true;     shift ;;
    --verify-bundles)  VERIFY_BUNDLES=true;  shift ;;
    --target)          TARGET_DIR="$2";      shift 2 ;;
    --help)
      sed -n '2,32p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ "$NO_BUNDLE" == "true" && "$BUNDLE_ONLY" == "true" ]]; then
  echo "sync.sh: --no-bundle and --bundle-only are mutually exclusive" >&2
  exit 1
fi

# ---------- helpers ----------
log()  { echo "[sync] $*"; }
warn() { echo "[sync] WARN: $*" >&2; }
dry()  { echo "[sync] DRY-RUN: $*"; }

# Read skill_bundles_tools list from a SKILL.md via tools/fm/extract.py.
# Emits one path per line on stdout (empty when key absent).
read_bundles() {
  local skill_md="$1"
  [[ -f "$skill_md" ]] || return 0
  python3 "$REPO_ROOT/tools/fm/extract.py" \
    "$skill_md" --frontmatter skill_bundles_tools 2>/dev/null \
    | sed -e '/^$/d' -e 's/^- *//' -e 's/^"//' -e 's/"$//' || true
}

# Hash every tracked file under a tools/<slug> path at the given git ref.
# Emits "<sha256>  <relative-path>" lines, sorted, with '.bundle.sha256'
# excluded. The set is restricted to git-tracked files so __pycache__,
# *.pyc, .pytest_cache, and similar runtime droppings never enter the
# sidecar.
hash_bundle_source() {
  local slug_path="$1" ref="${2:-HEAD}"
  ( cd "$REPO_ROOT" && \
    git ls-tree -r --name-only "$ref" -- "$slug_path/" \
    | grep -v '/\.bundle\.sha256$' \
    | LC_ALL=C sort \
    | while IFS= read -r tracked; do
        # Hash the working-tree content (which matches HEAD when clean).
        # Strip the slug_path/ prefix so the sidecar entries are slug-local.
        local rel="${tracked#${slug_path}/}"
        sha256sum "$tracked" | awk -v r="$rel" '{print $1"  ./"r}'
      done \
    | LC_ALL=C sort )
}

# Materialise one tools/<slug> source into <dest_root>/<basename>/ via
# `git archive`. This respects .gitignore (no __pycache__ / *.pyc leak)
# and yields the exact file set the sha256 sidecar tracks.
materialise_bundle() {
  local slug_path="$1" dest_root="$2"
  local src="$REPO_ROOT/$slug_path"
  local base; base="$(basename "$slug_path")"
  local dst="$dest_root/$base"
  if [[ ! -d "$src" ]]; then
    warn "bundle source missing: $slug_path"
    return 1
  fi
  if [[ "$DRY_RUN" == "true" ]]; then
    dry "would bundle: $slug_path → $dst"
    return 0
  fi
  mkdir -p "$dest_root"
  rm -rf "$dst"
  mkdir -p "$dst"
  # `git archive HEAD -- <slug_path>` emits a tarball with paths
  # rooted at slug_path/<...>; strip the slug-path components so we
  # land flat inside <dst>/.
  local depth; depth="$(awk -F/ '{print NF}' <<<"$slug_path")"
  if ! ( cd "$REPO_ROOT" \
         && git archive --format=tar HEAD -- "$slug_path/" 2>/dev/null \
         | tar -x --strip-components="$depth" -C "$dst" ) ; then
    warn "git archive failed for $slug_path"
    return 1
  fi
  hash_bundle_source "$slug_path" HEAD > "$dst/.bundle.sha256"
  return 0
}

# Hash every file in a bundled destination dir, excluding .bundle.sha256.
hash_bundle_dest() {
  local dst="$1"
  ( cd "$dst" && \
    find . -type f ! -name '.bundle.sha256' -print0 \
    | LC_ALL=C sort -z \
    | xargs -0 -I{} sha256sum {} \
    | LC_ALL=C sort )
}

# Compare repo source ↔ bundled destination directly. Echoes "OK",
# "DRIFT", or "MISSING"; returns 0 in all cases.
diff_bundle() {
  local slug_path="$1" dest_root="$2"
  local base; base="$(basename "$slug_path")"
  local dst="$dest_root/$base"
  [[ -d "$dst" ]] || { echo MISSING; return 0; }
  local expected actual
  expected="$(hash_bundle_source "$slug_path" HEAD)"
  actual="$(hash_bundle_dest "$dst")"
  if [[ "$expected" == "$actual" ]]; then
    echo OK
  else
    echo DRIFT
  fi
}

# ---------- fetch origin/main ----------
log "Fetching origin/main..."
git -C "$REPO_ROOT" fetch origin main --quiet
MAIN_SHA="$(git -C "$REPO_ROOT" rev-parse origin/main)"

# ---------- discover skill directories in repo ----------
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
BUNDLES_OK=0
BUNDLES_DRIFTED=0

mkdir -p "$TARGET_DIR"

for skill_name in "${REPO_SKILLS[@]}"; do
  dest="$TARGET_DIR/$skill_name"
  bundle_root="$dest/scripts/_bundled"

  # ---------- Phase 1: tree sync ----------
  if [[ "$BUNDLE_ONLY" != "true" ]]; then
    stage="$(mktemp -d)"
    if ! git -C "$REPO_ROOT" archive --format=tar origin/main \
            "skills/$skill_name/" 2>/dev/null \
            | tar -x --strip-components=2 -C "$stage" 2>/dev/null; then
      warn "$skill_name: failed to extract skills/$skill_name/ from origin/main"
      rm -rf "$stage"
      (( ERRORS++ )) || true
      continue
    fi
    if [[ ! -f "$stage/SKILL.md" ]]; then
      warn "$skill_name: SKILL.md not present in origin/main — skipping"
      rm -rf "$stage"
      (( ERRORS++ )) || true
      continue
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
      bundle_count=0
      while IFS= read -r _; do (( bundle_count++ )) || true; done < <(read_bundles "$stage/SKILL.md")
      dry "would sync tree: $skill_name → $dest (+ $bundle_count declared bundle(s))"
      rm -rf "$stage"
      (( SYNCED++ )) || true
      continue
    fi

    # Detect no-op via SKILL.md cmp; if identical AND scripts/references match, skip.
    if [[ -f "$dest/SKILL.md" ]] && cmp -s "$stage/SKILL.md" "$dest/SKILL.md"; then
      # Tree may still differ; rsync with --checksum to skip identical files cheaply.
      rsync -a --checksum --delete --exclude='scripts/_bundled/' \
            "$stage/" "$dest/" >/dev/null
      log "ok (tree in sync): $skill_name"
      (( SKIPPED++ )) || true
    else
      mkdir -p "$dest"
      rsync -a --checksum --delete --exclude='scripts/_bundled/' \
            "$stage/" "$dest/" >/dev/null
      log "synced: $skill_name"
      (( SYNCED++ )) || true
    fi
    rm -rf "$stage"
  fi

  # ---------- Phase 2: bundle materialisation ----------
  if [[ "$NO_BUNDLE" == "true" ]]; then
    continue
  fi
  bundles=()
  if [[ -f "$dest/SKILL.md" ]]; then
    while IFS= read -r entry; do
      [[ -z "$entry" ]] || bundles+=("$entry")
    done < <(read_bundles "$dest/SKILL.md")
  fi
  if [[ ${#bundles[@]} -eq 0 ]]; then
    continue
  fi

  if [[ "$VERIFY_BUNDLES" == "true" ]]; then
    for slug_path in "${bundles[@]}"; do
      status="$(diff_bundle "$slug_path" "$bundle_root")"
      case "$status" in
        OK)      (( BUNDLES_OK++ )) || true ;;
        DRIFT|MISSING)
          echo "BUNDLE-$status: $skill_name → $slug_path"
          (( BUNDLES_DRIFTED++ )) || true
          ;;
      esac
    done
    continue
  fi

  for slug_path in "${bundles[@]}"; do
    if materialise_bundle "$slug_path" "$bundle_root"; then
      (( BUNDLES_OK++ )) || true
    else
      (( ERRORS++ )) || true
    fi
  done
  log "  bundled into $skill_name: ${bundles[*]}"
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
log "Sync complete: $SYNCED synced, $SKIPPED in-sync, $ERRORS errors"
log "Bundles: $BUNDLES_OK ok, $BUNDLES_DRIFTED drifted"
log "Source: origin/main @ ${MAIN_SHA:0:7}"
log "Target: $TARGET_DIR"

if [[ $ERRORS -gt 0 || $BUNDLES_DRIFTED -gt 0 ]]; then
  exit 1
fi
exit 0
