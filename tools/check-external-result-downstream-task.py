#!/usr/bin/env python3
"""External-result downstream-Task linter — Task 035 ST-3 / RESEARCH.md R.6.5.

Mechanises the R.6.5 enforcement gap: every
``/research/<provider>/<slug>/result.md`` MUST be paired with a
back-linked Task in ``/tasks/``. Until this linter shipped, the rule was
human-review only, so an external result could land without ever
spawning a downstream analysis Task.

Surface
-------

    python3 tools/check-external-result-downstream-task.py [<paths> ...]

With no arguments the linter scans ``research/`` recursively for
``<provider>/<slug>/result.md`` files. With explicit paths it scans only
those targets (each must be a ``result.md`` under a provider folder).

Algorithm
---------

A *back-linked Task* is any ``tasks/<NNN>-<slug>/task.md`` whose
frontmatter satisfies at least one of:

  * ``task_affects_paths`` contains the result.md path or its parent
    directory ``research/<provider>/<slug>/``;
  * ``task_uses_prompts`` contains the result's slug (matches the stub
    prompt created by RESEARCH.md §6.3);
  * ``task_spawns_research`` contains the result's slug or the
    ``<provider>/<slug>`` namespaced form;
  * ``task_spawns_prompts`` contains the result's slug.

A result.md without any back-linked Task emits an ERROR diagnostic.

Diagnostic format
-----------------

    <result.md path>::ERROR:R.6.5:no-downstream-task

This matches the ``<relpath>::<TIER>:<code>:<message>`` shape used by
``tools/check-fl-declaration.py`` and the ADR validator so MAINTENANCE.md
aggregation can ingest the diagnostics through a single parser.

Exit codes
----------

  0 — every external result has a back-linked Task.
  1 — at least one result.md is unlinked.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.fm._core import read_fm, str_list  # noqa: E402

_DIAG = "{rel}::ERROR:R.6.5:no-downstream-task"


def _iter_external_results(paths: list[Path]) -> list[Path]:
    """Return every result.md target under research/<provider>/<slug>/."""
    targets: list[Path] = []
    for p in paths:
        if not p.exists():
            continue
        if p.is_file():
            if p.name == "result.md" and _is_external_path(p):
                targets.append(p)
            continue
        for f in p.rglob("result.md"):
            if _is_external_path(f):
                targets.append(f)
    return targets


def _is_external_path(path: Path) -> bool:
    """True iff path is research/<provider>/<slug>/result.md."""
    try:
        rel = path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        return False
    parts = rel.parts
    return (
        len(parts) == 4
        and parts[0] == "research"
        and parts[3] == "result.md"
    )


def _collect_task_backlinks(tasks_dir: Path) -> list[dict]:
    """Return frontmatter dicts for every task.md under /tasks/."""
    out: list[dict] = []
    if not tasks_dir.is_dir():
        return out
    for tm in tasks_dir.glob("*/task.md"):
        fm = read_fm(tm)
        if not fm:
            continue
        out.append(fm)
    return out


def _result_keys(result: Path) -> tuple[str, str, str, str]:
    """Return identifiers a Task may use to back-link this result."""
    rel = result.resolve().relative_to(REPO_ROOT)
    parts = rel.parts  # research / <provider> / <slug> / result.md
    provider, slug = parts[1], parts[2]
    folder = f"research/{provider}/{slug}/"
    namespaced = f"{provider}/{slug}"
    return rel.as_posix(), folder, slug, namespaced


def _has_backlink(task_fm: dict, keys: tuple[str, str, str, str]) -> bool:
    rel_path, folder, slug, namespaced = keys

    affects = str_list(task_fm, "task_affects_paths")
    for entry in affects:
        if entry == rel_path:
            return True
        if entry == folder or entry.rstrip("/") == folder.rstrip("/"):
            return True
        if entry == f"research/{slug}/" or entry == f"research/{slug}":
            return True

    for key in ("task_uses_prompts", "task_spawns_research", "task_spawns_prompts"):
        for entry in str_list(task_fm, key):
            if entry in (slug, namespaced):
                return True
    return False


def scan(paths: list[Path]) -> list[str]:
    """Return diagnostic strings for unlinked external results."""
    results = _iter_external_results(paths)
    if not results:
        return []
    tasks_fm = _collect_task_backlinks(REPO_ROOT / "tasks")
    diagnostics: list[str] = []
    for r in results:
        keys = _result_keys(r)
        rel = keys[0]
        if not any(_has_backlink(t, keys) for t in tasks_fm):
            diagnostics.append(_DIAG.format(rel=rel))
    return sorted(diagnostics)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Verify every external research result.md is paired with a "
            "back-linked Task per RESEARCH.md R.6.5."
        ),
    )
    ap.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="result.md files or directories to scan. Defaults to research/.",
    )
    args = ap.parse_args(argv)

    paths = args.paths or [REPO_ROOT / "research"]
    diagnostics = scan(paths)
    for line in diagnostics:
        print(line, file=sys.stderr)
    return 1 if diagnostics else 0


if __name__ == "__main__":
    sys.exit(main())
