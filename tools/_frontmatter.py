"""Shared frontmatter helpers for the agency governance linters.

Hand-rolled YAML parser with deliberate constraints (TASK.md §3):

  - YAML MUST NOT nest deeper than one level.
  - Lists MUST contain only scalars or short strings.

Two parse modes:

  parse_frontmatter(text, strict=True)   raises Diag on malformed input.
  parse_frontmatter(text, strict=False)  returns {} on malformed input.

The validator (`validate-frontmatter.py`) uses strict=True to surface every
malformation as an error. The downstream linters (`lint-linkage.py`,
`check-trust.py`, `lint-structure.py`) use strict=False because the
validator already gates malformed files; they only care about reading
well-formed values.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)


class Diag(Exception):
    """Raised by parse_frontmatter(strict=True) on malformed input."""


def parse_frontmatter(text: str, *, strict: bool = True) -> dict[str, Any]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        if strict:
            raise Diag("missing frontmatter block (no leading '---' fenced YAML)")
        return {}

    body = m.group(1)
    mapping: dict[str, Any] = {}
    current_list_key: str | None = None

    for raw in body.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        depth = indent // 2
        stripped = raw.strip()

        if stripped.startswith("- "):
            if current_list_key is None:
                if strict:
                    raise Diag(f"orphan list item: {stripped!r}")
                continue
            mapping.setdefault(current_list_key, []).append(
                stripped[2:].strip().strip('"')
            )
            continue

        if depth >= 2:
            if strict:
                raise Diag(
                    f"YAML nested deeper than 1 level (depth={depth}) at line: {raw!r}"
                )
            continue

        if ":" not in stripped:
            if strict:
                raise Diag(f"unparseable frontmatter line: {raw!r}")
            continue

        key, _, val = stripped.partition(":")
        key = key.strip()
        val = val.strip()
        current_list_key = None
        if val == "":
            mapping[key] = []
            current_list_key = key
        elif val == "[]":
            mapping[key] = []
        else:
            mapping[key] = val.strip('"')

    return mapping


def read_fm(path: Path, *, strict: bool = False) -> dict[str, Any]:
    try:
        return parse_frontmatter(path.read_text(encoding="utf-8"), strict=strict)
    except (OSError, Diag):
        return {}


def str_val(fm: dict, key: str) -> str:
    v = fm.get(key, "")
    return v if isinstance(v, str) else ""


def str_list(fm: dict, key: str) -> list[str]:
    v = fm.get(key, [])
    if isinstance(v, list):
        return [s for s in v if s]
    if isinstance(v, str) and v:
        return [v]
    return []
