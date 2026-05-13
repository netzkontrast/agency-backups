#!/usr/bin/env bash
# Task 094 ST-3 HK.14.5 — SubagentStop hook (matcher code-reviewer|deep-research).
# Thin shim; testable logic lives in tools/hooks/_subagent_stop.py.
set -euo pipefail
HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${PYTHON:-python3}" "${HOOK_DIR}/_subagent_stop.py"
