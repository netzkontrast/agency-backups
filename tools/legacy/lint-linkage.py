#!/usr/bin/env python3
"""DEPRECATED — thin shim around fm-validate --type-check (Task 019 ST-6).

The cross-reference graph rules from TASK.md §7 and FOLDERS.md §6
(`task_uses_prompts` / `task_spawns_research` / `prompt_relates_to_task`
reciprocity, dangling-reference detection) now live in
`tools/fm/validate.py` under the F.T.* code family. This file
preserves the legacy CLI surface so `tools/check-governance.sh` and
older invocations continue to work; behaviour is sourced from
`fm-validate --type-check`.

Original rule semantics preserved by F.T.* codes:
  F.T.1  — every list/scalar slug-or-task_id reference resolves to a file
  F.T.2  — task_uses_prompts ↔ prompt_relates_to_task reciprocity

Pending fm-* feature (Task 020 candidate):
  - "When task_status is 'done', every Todo checkbox MUST be checked."
  - "When task_status is 'done', friction-log.md MUST exist." (currently
    enforced by tools/check-trust.py).

Usage: python3 tools/legacy/lint-linkage.py
Exits 0 on success, 1 on any ERROR-level diagnostic.
"""
from __future__ import annotations

import sys
from pathlib import Path

_FM_DIR = Path(__file__).resolve().parent.parent / "fm"
sys.path.insert(0, str(_FM_DIR))

import validate as fm_validate  # type: ignore


def main() -> int:
    rc = fm_validate.main(["--type-check", "--format=text"])
    print("lint-linkage: shim → fm-validate --type-check", file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
