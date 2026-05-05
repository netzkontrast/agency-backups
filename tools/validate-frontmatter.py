#!/usr/bin/env python3
"""Shim: forward to tools/legacy/validate-frontmatter.py.

Task 017 moved the legacy validator into tools/legacy/ so the new
flexible-frontmatter toolchain (tools/fm/) can take over as the
canonical linter. This shim is retained for one release window so
existing callers (CI scripts, contributor muscle memory) keep working.

Migrate callers to: python3 tools/fm/validate.py
"""
from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path

_LEGACY = Path(__file__).resolve().parent / "legacy" / "validate-frontmatter.py"

if os.environ.get("FM_LEGACY_QUIET", "0") != "1":
    print(
        "warning: tools/validate-frontmatter.py is a deprecation shim; "
        "use tools/fm/validate.py (set FM_LEGACY_QUIET=1 to silence).",
        file=sys.stderr,
    )

runpy.run_path(str(_LEGACY), run_name="__main__")
