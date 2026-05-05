"""Flexible frontmatter toolchain — fm-validate, fm-extract, fm-edit, fm-query.

Spec: /research/flexible-frontmatter-toolchain/output/SPEC.md
Task: /tasks/016-flexible-frontmatter-toolchain/

This package is intentionally small and stateless. Each CLI tool is a single
file; shared logic lives in `_core.py`. No runtime dependencies outside the
Python 3.11 standard library.

`fm-rename` (Task 019 ST-1) extends the surface with a single audited T3
operation: cross-file slug rename. Per SPEC §7.2, fm-edit is forbidden from
applying T3 changes — `fm-rename` exists so a slug rename can be performed
atomically (pre-scan + per-file FileLock + body-byte invariant) and
audit-ably (refuses to touch any slug referenced from a done-Task's
`task_affects_paths`, exits 4) without hand-editing every cross-reference.
"""
from __future__ import annotations
