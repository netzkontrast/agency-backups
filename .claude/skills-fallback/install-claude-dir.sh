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

if [[ -e "${CLAUDE_SKILLS}" ]] && [[ ! -d "${CLAUDE_SKILLS}" ]]; then
    echo "[install-claude-dir] note: .claude/skills exists as a plain file (probably a symlink that Git checked out as text on a no-symlink-support platform)."
    echo "[install-claude-dir] removing and replacing with a copy-tree mirror."
    rm -f "${CLAUDE_SKILLS}"
fi

mkdir -p "${CLAUDE_SKILLS}"
# Copy with -L would dereference the source; we want a faithful mirror of
# regular files only (the source is itself a regular folder, never symlinked).
cp -R "${SOURCE_SKILLS}/." "${CLAUDE_SKILLS}/"

count=$(find "${CLAUDE_SKILLS}" -maxdepth 2 -name SKILL.md | wc -l)
echo "[install-claude-dir] ok: materialised ${count} SKILL.md files into .claude/skills/."
