#!/usr/bin/env bash
# Install SuperClaude from netzkontrast/SuperClaude_Framework into this environment.
# Also wires up the agency governance pre-commit hook.
#
# Usage:
#   tools/install-superclaude.sh [--yes] [--clone-dir <path>]
#
# Options:
#   --yes              Non-interactive; accept all prompts automatically.
#   --clone-dir <path> Where to clone SuperClaude_Framework if not found locally.
#                      Default: ~/SuperClaude_Framework

set -euo pipefail

REPO_URL="https://github.com/netzkontrast/SuperClaude_Framework.git"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENCY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
AUTO_YES=false
CLONE_DIR=""
# Default clone location: $HOME/SuperClaude_Framework (avoids relative-path issues)
DEFAULT_CLONE_TARGET="$HOME/SuperClaude_Framework"

# ── arg parsing ───────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case $1 in
    --yes|-y)       AUTO_YES=true; shift ;;
    --clone-dir)    CLONE_DIR="$2"; shift 2 ;;
    --help|-h)
      sed -n '2,12p' "$0"   # print the usage block at the top
      exit 0
      ;;
    *) echo "Unknown option: $1 (run with --help for usage)"; exit 1 ;;
  esac
done

# ── helpers ───────────────────────────────────────────────────────────────────
info()    { printf '\033[0;34m[info]\033[0m  %s\n' "$*"; }
ok()      { printf '\033[0;32m[ok]\033[0m    %s\n' "$*"; }
warn()    { printf '\033[1;33m[warn]\033[0m  %s\n' "$*"; }
die()     { printf '\033[0;31m[error]\033[0m %s\n' "$*" >&2; exit 1; }

confirm() {
  [[ "$AUTO_YES" == true ]] && return 0
  local prompt="$1 [Y/n] "
  read -rp "$prompt" ans
  [[ -z "$ans" || "$ans" =~ ^[Yy] ]]
}

# ── 1. locate / clone SuperClaude_Framework ───────────────────────────────────
echo ""
info "=== SuperClaude installer (netzkontrast fork) ==="
echo ""

# Search order: explicit --clone-dir, then sibling dir, then ~/SuperClaude_Framework
if [[ -n "$CLONE_DIR" ]]; then
  SC_DIR="$CLONE_DIR"
elif [[ -d "$AGENCY_ROOT/../SuperClaude_Framework/.git" ]]; then
  SC_DIR="$(cd "$AGENCY_ROOT/../SuperClaude_Framework" && pwd)"
  info "Found existing clone at $SC_DIR"
elif [[ -d "$HOME/SuperClaude_Framework/.git" ]]; then
  SC_DIR="$HOME/SuperClaude_Framework"
  info "Found existing clone at $SC_DIR"
else
  SC_DIR="$DEFAULT_CLONE_TARGET"
  info "SuperClaude_Framework not found locally."
  confirm "Clone from $REPO_URL into $SC_DIR?" || die "Aborted."
  git clone "$REPO_URL" "$SC_DIR"
  ok "Cloned to $SC_DIR"
fi

# Validate the clone looks correct
[[ -f "$SC_DIR/pyproject.toml" ]] || die "$SC_DIR/pyproject.toml not found — clone may be corrupt."

# ── 2. check / install UV ─────────────────────────────────────────────────────
if ! command -v uv &>/dev/null; then
  warn "UV package manager not found."
  confirm "Install UV now via the official installer?" || die "UV is required. Install it manually: https://docs.astral.sh/uv/"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # add to PATH for this session
  export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"
  command -v uv &>/dev/null || die "UV installed but not in PATH. Restart your shell and re-run."
fi
ok "UV $(uv --version)"

# ── 3. install SuperClaude Python package ─────────────────────────────────────
info "Installing SuperClaude package in editable mode from $SC_DIR …"
cd "$SC_DIR"
# --system: install into the system Python when no virtualenv is active
uv pip install --system -e ".[dev]"
ok "Package installed"

# ── 4. deploy Claude Code artifacts ──────────────────────────────────────────
if ! command -v superclaude &>/dev/null; then
  # uv editable installs may put the script in the venv; try uv run
  SC_CMD="uv run superclaude"
else
  SC_CMD="superclaude"
fi

info "Deploying commands/agents/skills to ~/.claude/ …"
$SC_CMD install
ok "superclaude install complete"

# ── 5. wire up agency governance hook ─────────────────────────────────────────
cd "$AGENCY_ROOT"
info "Installing agency governance pre-commit hook …"
if [[ -f "$AGENCY_ROOT/tools/install-hooks.sh" ]]; then
  bash "$AGENCY_ROOT/tools/install-hooks.sh"
  ok "Governance hook installed (core.hooksPath = .githooks)"
else
  warn "tools/install-hooks.sh not found; skipping governance hook."
fi

# ── 6. summary ────────────────────────────────────────────────────────────────
echo ""
ok "=== Installation complete ==="
echo ""
printf '  SuperClaude source : %s\n' "$SC_DIR"
printf '  Commands           : ~/.claude/commands/sc/\n'
printf '  Agents             : ~/.claude/agents/\n'
printf '  Skills             : ~/.claude/skills/\n'
printf '  Agency hook        : %s/.githooks/pre-commit\n' "$AGENCY_ROOT"
echo ""
info "Run 'superclaude doctor' to verify the installation."
info "Try '/sc:help' inside a Claude Code session to get started."
echo ""
