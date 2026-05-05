#!/usr/bin/env bash
# install.sh — bootstrap all tooling dependencies for netzkontrast/agency
#
# Usage:
#   ./install.sh            # install into the active Python environment
#   ./install.sh --check    # verify installed versions without installing
#
# Requirements are defined in tools/requirements.txt.
# After installing, run tools/check-governance.sh to verify the full
# tooling stack is operational.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUIREMENTS="$REPO_ROOT/tools/requirements.txt"
PYTHON="${PYTHON:-python3}"
PIP="$PYTHON -m pip"

# ── helpers ──────────────────────────────────────────────────────────────────

info()  { printf '\033[0;34m[install]\033[0m %s\n' "$*"; }
ok()    { printf '\033[0;32m[  ok  ]\033[0m %s\n' "$*"; }
fail()  { printf '\033[0;31m[ FAIL ]\033[0m %s\n' "$*" >&2; exit 1; }

# ── pre-flight ────────────────────────────────────────────────────────────────

info "Python: $($PYTHON --version 2>&1)"
info "Requirements: $REQUIREMENTS"

[[ -f "$REQUIREMENTS" ]] || fail "requirements file not found: $REQUIREMENTS"

# ── check-only mode ───────────────────────────────────────────────────────────

if [[ "${1:-}" == "--check" ]]; then
  info "Running in --check mode (no installation)."
  $PIP install --dry-run --quiet -r "$REQUIREMENTS" 2>&1 \
    | grep -E "Would install|already satisfied|Requirement already" \
    || true
  ok "Dependency check complete."
  exit 0
fi

# ── install ───────────────────────────────────────────────────────────────────

info "Installing from $REQUIREMENTS ..."
# Install without --upgrade so system-managed packages (e.g. debian PyYAML)
# that already satisfy the version constraint are not touched.
# If pip refuses due to PEP 668 (externally-managed environment), retry with
# --break-system-packages so CI / container environments work out of the box.
if ! $PIP install -r "$REQUIREMENTS" 2>&1; then
  info "pip rejected install; retrying with --break-system-packages ..."
  $PIP install --break-system-packages -r "$REQUIREMENTS"
fi

# ── verify ────────────────────────────────────────────────────────────────────

info "Verifying installed packages..."

verify_package() {
  local pkg="$1"
  local import_name="${2:-$1}"
  if $PYTHON -c "import $import_name" 2>/dev/null; then
    local version
    version=$($PYTHON -c "import $import_name; print(getattr($import_name, '__version__', 'n/a'))" 2>/dev/null || echo "n/a")
    ok "$pkg ($version)"
  else
    fail "$pkg could not be imported after installation"
  fi
}

verify_package "PyYAML"      "yaml"
verify_package "jsonschema"  "jsonschema"
verify_package "pytest"      "pytest"

# ── post-install hint ─────────────────────────────────────────────────────────

printf '\n'
ok "All dependencies installed."
info "Run \`tools/check-governance.sh\` to verify the full tooling stack."
info "Run \`python -m pytest tools/dramatica-nav/tests/\` to execute the test suite."
