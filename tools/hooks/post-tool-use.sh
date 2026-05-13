#!/usr/bin/env bash
# Task 094 ST-3 HK.14.3 — PostToolUse hook (matcher Skill|Agent).
# Thin shim; testable logic lives in tools/hooks/_post_tool_use.py.
set -euo pipefail
HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${PYTHON:-python3}" "${HOOK_DIR}/_post_tool_use.py"
