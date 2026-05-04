#!/usr/bin/env python3
"""
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

import re
import sys
from pathlib import Path
from typing import Iterable

L1_REQUIRED = {"type", "status", "slug", "summary", "created", "updated"}
L2_TASK = {"task_id", "task_status", "task_owner", "task_priority",
           "task_uses_prompts", "task_spawns_research", "task_affects_paths"}
L2_PROMPT = {"prompt_kind", "prompt_framework", "prompt_target_agent",
             "prompt_relates_to_task", "prompt_spawned_from_research"}
L2_RESEARCH = {"research_phase", "research_executes_prompt", "research_friction_level"}

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)


class Diag(Exception):
    pass


def parse_frontmatter(text: str) -> dict[str, object]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise Diag("missing frontmatter block (no leading '---' fenced YAML)")
    body = m.group(1)
    mapping: dict[str, object] = {}
    current_list_key: str | None = None
    for raw in body.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        depth = indent // 2
        stripped = raw.strip()
        if stripped.startswith("- "):
            if current_list_key is None:
                raise Diag(f"orphan list item: {stripped!r}")
            mapping.setdefault(current_list_key, []).append(stripped[2:].strip().strip('"'))
            continue
        if depth >= 2:
            raise Diag(f"YAML nested deeper than 1 level (depth={depth}) at line: {raw!r}")
        if ":" not in stripped:
            raise Diag(f"unparseable frontmatter line: {raw!r}")
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


def classify(path: Path) -> tuple[bool, set[str]]:
    """Return (frontmatter_required, l2_required_keys)."""
    parts = path.parts
    name = path.name
    in_tasks = "tasks" in parts
    in_prompts = "prompts" in parts
    in_research = "research" in parts
    in_templates = "templates" in parts
    in_tools = "tools" in parts

    if in_templates or in_tools:
        return (name == "readme.md", set())

    if in_tasks:
        if name == "task.md":
            return (True, L2_TASK)
        if name == "readme.md":
            return (True, set())
        return (False, set())

    if in_prompts:
        if name == "prompt.md":
            return (True, L2_PROMPT)
        if name == "readme.md":
            return (True, set())
        return (False, set())

    if in_research:
        if name == "readme.md" and len(parts) <= 3:
            return (True, L2_RESEARCH if len(parts) == 3 else set())
        if name == "SPEC.md" and "output" in parts:
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
        fm = parse_frontmatter(text)
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


def load_waivers() -> set[str]:
    waiver_path = Path("tools/.frontmatter-waivers")
    if not waiver_path.exists():
        return set()
    out: set[str] = set()
    for line in waiver_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.add(line)
    return out


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        roots = [Path(a) for a in argv[1:]]
    else:
        candidates = [Path("tasks"), Path("prompts"), Path("research"),
                      Path("templates"), Path("tools")]
        roots = [r for r in candidates if r.exists()]

    waivers = load_waivers()
    all_diags: list[str] = []
    checked = 0
    waived = 0
    for path in iter_targets(roots):
        required, _ = classify(path)
        if not required:
            continue
        if str(path) in waivers:
            waived += 1
            continue
        checked += 1
        all_diags.extend(check_file(path))

    for d in all_diags:
        print(d, file=sys.stderr)
    print(f"Checked {checked} files ({waived} waived); {len(all_diags)} diagnostic(s).")
    return 1 if all_diags else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
