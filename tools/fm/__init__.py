"""Flexible frontmatter toolchain — fm-validate, fm-extract, fm-edit, fm-query.

Spec: /research/flexible-frontmatter-toolchain/output/SPEC.md
Task: /tasks/016-flexible-frontmatter-toolchain/

This package is intentionally small and stateless. Each CLI tool is a single
file; shared logic lives in `_core.py`. No runtime dependencies outside the
Python 3.11 standard library.
"""
from __future__ import annotations
