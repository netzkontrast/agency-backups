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

`fm-new` (Task 019 ST-3) scaffolds a new task / prompt / research folder
from the canonical templates with valid frontmatter. The task subcommand
allocates the next zero-padded id by scanning `tasks/`; every variant
refuses to clobber an existing folder.

`fm-graph` (Task 019 ST-2) walks the operational corpus' frontmatter graph
and emits cycles, dangling references, and orphans.

`fm-fix` (Task 019 ST-4) is the T1/T2 auto-repair driver. It runs
`fm-validate`, applies a closed-set recipe table for diagnostic codes that
have an unambiguous mechanical fix, and emits a T3 stub Task for anything
the recipe table can't safely auto-repair.
"""
from __future__ import annotations
