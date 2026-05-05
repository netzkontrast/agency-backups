#!/usr/bin/env python3
"""Shim: forward to tools/legacy/lint-linkage.py (Task 017)."""
from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path

_LEGACY = Path(__file__).resolve().parent / "legacy" / "lint-linkage.py"

if os.environ.get("FM_LEGACY_QUIET", "0") != "1":
    print(
        "warning: tools/lint-linkage.py is a deprecation shim; "
        "graph queries fold into fm-query (set FM_LEGACY_QUIET=1 to silence).",
        file=sys.stderr,
    )

runpy.run_path(str(_LEGACY), run_name="__main__")
