"""Re-export shim for the legacy frontmatter helper API.

The implementation moved to `tools/fm/_core.py` per
SPEC.md §5.5 (anchor F.5.5). This shim is kept for one release window
so the existing linters (`validate-frontmatter.py`, `lint-structure.py`,
`lint-linkage.py`, `check-trust.py`, `check-maintenance-bypass.py`) keep
working. Task 017 is responsible for re-pointing those imports and
removing this file.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Make `tools/fm/` importable when invoked by scripts in `tools/`
# (which add their own dir, not `tools/fm/`, to sys.path).
sys.path.insert(0, str(Path(__file__).resolve().parent / "fm"))

from _core import (  # noqa: E402,F401
    FRONTMATTER_RE,
    Diag,
    parse_frontmatter,
    read_fm,
    str_val,
    str_list,
)
