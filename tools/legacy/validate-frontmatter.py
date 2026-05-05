#!/usr/bin/env python3
"""
DEPRECATED — moved to tools/legacy/ by Task 017.

This validator is retained for one release window so the side-by-side
comparison in tools/check-governance.sh can surface any disagreement
between the legacy schema and tools/fm/validate.py. The flexible
toolchain (Task 016) is now the canonical linter; this file will be
removed in the Task 017 final cleanup commit.

Migrate callers to:
    python3 tools/fm/validate.py [paths ...]

Original docstring follows.

Frontmatter validator for the agency repository.

Enforces the Layered Schema with Namespacing defined in TASK.md §3 by checking
ONLY the files the spec mandates frontmatter on:

  /tasks/<NNN>-<slug>/task.md            -> L1 + task_*
  /prompts/<slug>/prompt.md              -> L1 + prompt_*
  /research/<slug>/output/SPEC.md        -> L1 + research_*
  /research/<slug>/readme.md             -> L1 + research_*
  /tasks/readme.md, /prompts/readme.md,
  /research/readme.md, /tasks/<...>/readme.md, /prompts/<...>/readme.md,
  /templates/, /tools/                   -> L1 only (FOLDERS.md §5)

Workspace scratch files, synthesis logs, methodology notes, brief.md, and
similar operational artifacts are NOT required to carry frontmatter.

Additional checks:
  - YAML nesting MUST NOT exceed depth 1.
  - Templates MUST NOT leave 'REPLACE' tokens in non-template files.
  - Slug field MUST be kebab-case (no spaces).

Usage:
    python3 tools/validate-frontmatter.py [path ...]

If no paths are given, walks /tasks/, /prompts/, /research/, /templates/,
/tools/ from CWD. Exits 0 on success, 1 on any diagnostic.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable

from _frontmatter import FRONTMATTER_RE, Diag, parse_frontmatter

L1_REQUIRED = {"type", "status", "slug", "summary", "created", "updated"}
L2_TASK = {"task_id", "task_status", "task_owner", "task_priority",
           "task_uses_prompts", "task_spawns_research", "task_spawns_prompts", "task_affects_paths"}
# PROMPT.md §3 example shows prompt_relates_to_task / prompt_spawned_from_research
# as "<slug or empty>" — they are conditional linkage fields, not always present.
# Only the kind/framework/target trio is required on every prompt.
L2_PROMPT = {"prompt_kind", "prompt_framework", "prompt_target_agent"}
L2_RESEARCH = {"research_phase", "research_executes_prompt", "research_friction_level"}


KNOWN_ROOTS = ("tasks", "prompts", "research", "templates", "tools")


def _root_index(parts: tuple[str, ...]) -> int | None:
    """Return the index of the first known governance root in parts.

    This lets classify() handle both repo-relative paths
    ("research/foo/output/SPEC.md") and absolute paths
    ("/home/.../agency/research/foo/output/SPEC.md") correctly,
    while still ignoring deeper accidental matches like
    "research/foo/tasks/bar.md" (the first known root wins).
    """
    for i, p in enumerate(parts):
        if p in KNOWN_ROOTS:
            return i
    return None


def classify(path: Path) -> tuple[bool, set[str]]:
    """Return (frontmatter_required, l2_required_keys)."""
    parts = path.parts
    idx = _root_index(parts)
    if idx is None:
        return (False, set())
    top = parts[idx]
    rel_parts = parts[idx:]
    name = path.name

    if top in ("templates", "tools"):
        return (name == "readme.md", set())

    if top == "tasks":
        if name == "task.md":
            return (True, L2_TASK)
        if name == "readme.md":
            return (True, set())
        return (False, set())

    if top == "prompts":
        if name == "prompt.md":
            return (True, L2_PROMPT)
        if name == "readme.md":
            return (True, set())
        return (False, set())

    if top == "research":
        if name == "readme.md" and len(rel_parts) <= 3:
            return (True, L2_RESEARCH if len(rel_parts) == 3 else set())
        if name == "SPEC.md" and "output" in rel_parts:
            return (True, L2_RESEARCH)
        return (False, set())

    return (False, set())


def check_file(path: Path) -> list[str]:
    required, l2_keys = classify(path)
    if not required:
        return []

    diags: list[str] = []
    text = path.read_text(encoding="utf-8")

    fm_match = FRONTMATTER_RE.match(text)
    if (fm_match
            and not path.is_relative_to(Path("templates"))
            and "REPLACE" in fm_match.group(1)):
        diags.append(f"{path}: unresolved 'REPLACE' token in frontmatter")

    try:
        fm = parse_frontmatter(text, strict=True)
    except Diag as e:
        return diags + [f"{path}: {e}"]

    missing_l1 = L1_REQUIRED - fm.keys()
    if missing_l1:
        diags.append(f"{path}: missing L1 keys: {sorted(missing_l1)}")

    if l2_keys:
        missing_l2 = l2_keys - fm.keys()
        if missing_l2:
            diags.append(f"{path}: missing L2 keys: {sorted(missing_l2)}")

    slug = fm.get("slug", "")
    if isinstance(slug, str) and slug and " " in slug:
        diags.append(f"{path}: slug must be kebab-case, got {slug!r}")

    return diags


def iter_targets(roots: Iterable[Path]) -> Iterable[Path]:
    for root in roots:
        if root.is_file() and root.suffix == ".md":
            yield root
        elif root.is_dir():
            yield from root.rglob("*.md")


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        roots = [Path(a) for a in argv[1:]]
    else:
        candidates = [Path("tasks"), Path("prompts"), Path("research"),
                      Path("templates"), Path("tools")]
        roots = [r for r in candidates if r.exists()]

    all_diags: list[str] = []
    checked = 0
    for path in iter_targets(roots):
        required, _ = classify(path)
        if not required:
            continue
        checked += 1
        all_diags.extend(check_file(path))

    for d in all_diags:
        print(d, file=sys.stderr)
    print(f"Checked {checked} files; {len(all_diags)} diagnostic(s).")
    return 1 if all_diags else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
