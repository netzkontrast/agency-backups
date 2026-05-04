#!/usr/bin/env bash
# One-time installer that points this clone's git hooks at .githooks/.
# Idempotent: safe to run multiple times.
#
# Usage:
#   tools/install-hooks.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

if [ ! -d .githooks ]; then
  echo "ERROR: .githooks/ directory missing at $REPO_ROOT" >&2
  exit 1
fi

git config core.hooksPath .githooks
echo "Installed: core.hooksPath = .githooks"
echo "Pre-commit hook now runs tools/check-governance.sh on every commit."
