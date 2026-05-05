#!/usr/bin/env python3
"""
DEPRECATED — moved to tools/legacy/ by Task 017.

The structural rules this linter enforced now live in MAINTENANCE.md and
the type-classification table at maintenance/schemas/header-ontology.json.
fm-validate enforces the type/path agreement that previously lived here;
the remaining structural rules (presence of task.md / readme.md inside a
slug folder) will be folded into a future fm-validate extension.

Retained for one release window so the side-by-side comparison can
surface disagreements. Will be removed in the Task 017 cleanup commit.

Original docstring follows.

Directory-structure linter for the agency repository.

Enforces the structural rules from TASK.md §2, PROMPT.md §2, RESEARCH.md §2,
FOLDERS.md §3, and Spec-G/H/I (session-continuity):

  /tasks/<NNN>-<slug>/    MUST contain task.md
  /tasks/<NNN>-<slug>/    MUST contain readme.md
  /tasks/<NNN>-<slug>/    MUST contain notes.md when task_status is "blocked"

  /prompts/<slug>/        MUST contain prompt.md
  /prompts/<slug>/        MUST contain brief.md
  /prompts/<slug>/        MUST contain readme.md

  /research/<slug>/       MUST contain readme.md  (non-provider, non-archived)
  /research/<slug>/       SHOULD contain workspace/, synthesis/, reflection/, output/
                          (emitted as warnings, not errors, since some runs are archived)

Provider subfolders under /research/<provider>/<slug>/ are checked separately:
  /research/<provider>/<slug>/  MUST contain result.md

Usage:
    python3 tools/lint-structure.py [--warn-only-research-dirs]

Exits 0 on success, 1 on any error-level diagnostic.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _frontmatter import read_fm, str_val

TASK_DIR_RE = re.compile(r"^\d{3}-.+$")
PROVIDER_NAMES = {"gemini", "gpt", "human", "other"}
RESEARCH_SUBDIRS = {"workspace", "synthesis", "reflection", "output"}


def _read_frontmatter_key(path: Path, key: str) -> str:
    """Return the value for a YAML frontmatter key, or '' if missing/unparseable."""
    return str_val(read_fm(path), key)


def lint_tasks(tasks_root: Path) -> list[str]:
    errors: list[str] = []
    for entry in sorted(tasks_root.iterdir()):
        if entry.name == "readme.md" or not entry.is_dir():
            continue
        if not TASK_DIR_RE.match(entry.name):
            errors.append(
                f"tasks/{entry.name}: folder name does not match <NNN>-<slug> pattern"
            )
            continue
        task_md = entry / "task.md"
        if not task_md.exists():
            errors.append(f"{entry}: missing required task.md (TASK.md §2)")
        if not (entry / "readme.md").exists():
            errors.append(f"{entry}: missing required readme.md (FOLDERS.md §3)")
        # Spec-G/H/I §8.4: blocked tasks MUST have notes.md
        if task_md.exists():
            status = _read_frontmatter_key(task_md, "task_status")
            if status == "blocked" and not (entry / "notes.md").exists():
                errors.append(
                    f"{entry}: task_status is 'blocked' but notes.md is missing "
                    f"(TASK.md §8.4 / Spec-I.3.1)"
                )
    return errors


def lint_prompts(prompts_root: Path) -> list[str]:
    errors: list[str] = []
    for entry in sorted(prompts_root.iterdir()):
        if entry.name == "readme.md" or not entry.is_dir():
            continue
        if not (entry / "prompt.md").exists():
            errors.append(f"{entry}: missing required prompt.md (PROMPT.md §2)")
        if not (entry / "brief.md").exists():
            errors.append(f"{entry}: missing required brief.md (PROMPT.md §2)")
        if not (entry / "readme.md").exists():
            errors.append(f"{entry}: missing required readme.md (FOLDERS.md §3)")
    return errors


def lint_research(research_root: Path) -> tuple[list[str], list[str]]:
    """Returns (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []
    for entry in sorted(research_root.iterdir()):
        if entry.name == "readme.md" or not entry.is_dir():
            continue
        # Provider subfolder: /research/<provider>/<slug>/result.md
        if entry.name in PROVIDER_NAMES:
            for slug_dir in sorted(entry.iterdir()):
                if not slug_dir.is_dir():
                    continue
                if not (slug_dir / "result.md").exists():
                    errors.append(
                        f"{slug_dir}: provider result folder missing result.md "
                        f"(RESEARCH.md §6.1)"
                    )
            continue
        # Normal research workspace
        if not (entry / "readme.md").exists():
            errors.append(f"{entry}: missing required readme.md (FOLDERS.md §3)")
        for subdir in RESEARCH_SUBDIRS:
            if not (entry / subdir).is_dir():
                warnings.append(
                    f"{entry}: missing recommended subdir '{subdir}/' "
                    f"(RESEARCH.md §2, SHOULD)"
                )
    return errors, warnings


def main(argv: list[str]) -> int:
    root = Path(".")
    tasks_root = root / "tasks"
    prompts_root = root / "prompts"
    research_root = root / "research"

    all_errors: list[str] = []
    all_warnings: list[str] = []

    if tasks_root.exists():
        all_errors.extend(lint_tasks(tasks_root))
    if prompts_root.exists():
        all_errors.extend(lint_prompts(prompts_root))
    if research_root.exists():
        errs, warns = lint_research(research_root)
        all_errors.extend(errs)
        all_warnings.extend(warns)

    for w in all_warnings:
        print(f"WARN  {w}", file=sys.stderr)
    for e in all_errors:
        print(f"ERROR {e}", file=sys.stderr)

    total = len(all_errors)
    print(
        f"lint-structure: {total} error(s), {len(all_warnings)} warning(s)."
    )
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
