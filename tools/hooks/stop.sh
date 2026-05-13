#!/usr/bin/env bash
# Task 094 ST-3 HK.14.4 — Stop hook (Closing Run Procedure enforcer).
# Thin shim; testable logic lives in tools/hooks/_stop.py.
set -euo pipefail
HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${PYTHON:-python3}" "${HOOK_DIR}/_stop.py"
