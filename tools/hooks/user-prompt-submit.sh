#!/usr/bin/env bash
# Task 094 ST-3 HK.14.1 — UserPromptSubmit hook (D.7-compliant).
# Thin shim; testable logic lives in tools/hooks/_user_prompt_submit.py.
set -euo pipefail
HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${PYTHON:-python3}" "${HOOK_DIR}/_user_prompt_submit.py"
