#!/usr/bin/env bash
# install-claude-dir.sh — Windows-friendly copy fallback for .claude/skills/.
#
# Authored by Task 094 ST-2 per the ADR-0011 D.7-compliant integration plan.
# On platforms where Git or Claude Code do not follow symbolic links
# (e.g. some Windows + WSL configurations, Git with `core.symlinks=false`),
# the .claude/skills/ symlink resolves to a plain text file containing the
# string "../skills". This script materialises a copy-tree mirror of
# ../../skills/ into .claude/skills/ so the loader's directory walk succeeds.
#
# Idempotent: safe to re-run. Refuses to clobber an existing real symlink.
#
# PR #124 review fixes:
#   - Sync is prune-delete (rsync --delete; rm-then-cp fallback when rsync
#     missing) so a skill renamed or removed upstream does not leave a
#     stale directory in the mirror (Codex P2 #4).
#   - When the tracked symlink path is replaced with a real directory the
#     working tree appears dirty to `git status`. The script now prints
#     explicit guidance on how to suppress this for Windows operators so
#     the documented recovery path no longer breaks the clean-tree gate
#     (Codex P2 #5).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CLAUDE_SKILLS="${REPO_ROOT}/.claude/skills"
SOURCE_SKILLS="${REPO_ROOT}/skills"

if [[ ! -d "${SOURCE_SKILLS}" ]]; then
    echo "[install-claude-dir] ERROR: source ${SOURCE_SKILLS} not found." >&2
    exit 1
fi

if [[ -L "${CLAUDE_SKILLS}" ]]; then
    target="$(readlink "${CLAUDE_SKILLS}")"
    if [[ "${target}" == "../skills" ]] && [[ -d "${CLAUDE_SKILLS}/" ]]; then
        echo "[install-claude-dir] ok: .claude/skills symlink resolves correctly; no action needed."
        exit 0
    fi
    echo "[install-claude-dir] note: existing symlink at .claude/skills points to '${target}' but does not resolve to a directory."
    echo "[install-claude-dir] note: leave the symlink in place if your platform supports it; otherwise remove and re-run."
    exit 0
fi

dirty_warn=0
if [[ -e "${CLAUDE_SKILLS}" ]] && [[ ! -d "${CLAUDE_SKILLS}" ]]; then
    echo "[install-claude-dir] note: .claude/skills exists as a plain file (probably a symlink that Git checked out as text on a no-symlink-support platform)."
    echo "[install-claude-dir] removing and replacing with a copy-tree mirror."
    rm -f "${CLAUDE_SKILLS}"
    dirty_warn=1
fi

# Prune-delete sync so removals upstream propagate. Prefer rsync (atomic
# add/update/delete pass); fall back to rm-then-cp on hosts without rsync.
mkdir -p "${CLAUDE_SKILLS}"
if command -v rsync >/dev/null 2>&1; then
    rsync --archive --delete --no-perms --exclude '.git' \
        "${SOURCE_SKILLS}/" "${CLAUDE_SKILLS}/"
    sync_method="rsync --delete"
else
    echo "[install-claude-dir] note: rsync not found; falling back to rm-then-cp (slower but still prune-deletes stale entries)."
    rm -rf "${CLAUDE_SKILLS}"
    mkdir -p "${CLAUDE_SKILLS}"
    cp -R "${SOURCE_SKILLS}/." "${CLAUDE_SKILLS}/"
    sync_method="rm + cp -R"
fi

count=$(find "${CLAUDE_SKILLS}" -maxdepth 2 -name SKILL.md | wc -l)
echo "[install-claude-dir] ok: materialised ${count} SKILL.md files into .claude/skills/ (${sync_method})."

if [[ "${dirty_warn}" -eq 1 ]]; then
    cat <<'EOF'
[install-claude-dir] note: on symlink-less platforms the tracked path
[install-claude-dir]       `.claude/skills` (a checked-in symlink) is
[install-claude-dir]       now replaced with a real directory of copied
[install-claude-dir]       files. `git status` will show this as
[install-claude-dir]         deleted:    .claude/skills
[install-claude-dir]         untracked:  .claude/skills/...
[install-claude-dir]       which will fail clean-working-tree gates.
[install-claude-dir]
[install-claude-dir]       To suppress locally (does NOT alter the tracked
[install-claude-dir]       symlink in the index, just hides the diff from
[install-claude-dir]       your working tree):
[install-claude-dir]
[install-claude-dir]         git update-index --skip-worktree .claude/skills
[install-claude-dir]
[install-claude-dir]       Reverse with:  git update-index --no-skip-worktree .claude/skills
[install-claude-dir]
[install-claude-dir]       This is a one-time per-clone fixup; subsequent
[install-claude-dir]       reruns of this script will hit the prune-sync
[install-claude-dir]       path and stay quiet.
EOF
fi
