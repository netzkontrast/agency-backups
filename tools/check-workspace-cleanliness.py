#!/usr/bin/env python3
"""Workspace-cleanliness linter — Task 035 ST-2 / RESEARCH.md R.4.4.

Mechanises the R.4.4 enforcement gap: ``Execution scripts (.py, .sh) MUST
be deleted before final commit``. Until this linter shipped, R.4.4 was
human-review only, so stragglers leaked into closed research workspaces.

Surface
-------

    python3 tools/check-workspace-cleanliness.py [<paths> ...]

With no arguments the linter scans ``research/`` recursively. With one or
more paths it scans the union of those paths, restricted to subtrees that
sit under a ``research/<slug>/workspace/`` ancestor.

Heuristic
---------

Flag any file whose path matches ``research/<slug>/workspace/**/*.{py,sh,log}``
(modulo the legacy single-script ``.log`` exception below). The R.4.4 rule
explicitly names ``.py`` and ``.sh``; ``.log`` is included because trace
logs that are *not* ``session.log`` are typically tool-generated leftovers
that bloat the closed workspace.

Exemptions
----------

  * ``session.log`` — RESEARCH.md §4.5 mandates this file. Always allowed.
  * Any path listed line-by-line in a ``.cleanignore`` file at the
    workspace root (one path per line, glob-relative to the workspace).
  * Lines starting with ``#`` in ``.cleanignore`` are comments.

Diagnostic format
-----------------

    <relpath>::WARN:R.4.4:execution-script-not-cleaned

This matches the ``<relpath>::<TIER>:<code>:<message>`` shape used by the
ADR validator (``tools/adr/runlog.py``) so MAINTENANCE.md aggregation can
ingest the diagnostics through a single parser.

Exit codes
----------

  0 — every scanned workspace is clean (or has a covering ``.cleanignore``).
  1 — at least one straggler emitted a WARN diagnostic.
"""
from __future__ import annotations

import argparse
import fnmatch
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# File suffixes that constitute "execution scripts" per R.4.4 plus the
# `.log` extension (trace logs are leftovers when they aren't session.log).
_FORBIDDEN_SUFFIXES: frozenset[str] = frozenset({".py", ".sh", ".log"})

# Files that are always allowed regardless of suffix.
_ALWAYS_ALLOWED: frozenset[str] = frozenset({"session.log"})

_DIAG = "{rel}::WARN:R.4.4:execution-script-not-cleaned"


def _workspace_root(path: Path) -> Path | None:
    """Return the closest ``research/<slug>/workspace`` ancestor, or None."""
    parts = path.parts
    for i in range(len(parts) - 1):
        if parts[i] == "research" and i + 2 < len(parts) and parts[i + 2] == "workspace":
            # research/<slug>/workspace/...
            return Path(*parts[: i + 3])
    return None


def _load_cleanignore(workspace: Path) -> list[str]:
    f = workspace / ".cleanignore"
    if not f.exists():
        return []
    patterns: list[str] = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def _is_ignored(rel_to_workspace: Path, patterns: list[str]) -> bool:
    s = rel_to_workspace.as_posix()
    for pat in patterns:
        if fnmatch.fnmatch(s, pat):
            return True
        # Also match path-prefix style "subdir/" or "subdir".
        if pat.endswith("/") and (s + "/").startswith(pat):
            return True
    return False


def _iter_targets(paths: list[Path]) -> list[Path]:
    """Expand input paths into individual files under workspace dirs."""
    targets: list[Path] = []
    for p in paths:
        if not p.exists():
            continue
        if p.is_file():
            targets.append(p)
            continue
        # Directory: walk; only recurse when within (or above) a research/ tree.
        for f in p.rglob("*"):
            if f.is_file():
                targets.append(f)
    return targets


def scan(paths: list[Path]) -> list[str]:
    """Return diagnostic strings for any forbidden stragglers."""
    diagnostics: list[str] = []
    seen_workspaces: dict[Path, list[str]] = {}
    for f in _iter_targets(paths):
        try:
            rel = f.resolve().relative_to(REPO_ROOT)
        except ValueError:
            rel = f
        ws = _workspace_root(rel)
        if ws is None:
            continue
        if f.name in _ALWAYS_ALLOWED:
            continue
        if f.suffix not in _FORBIDDEN_SUFFIXES:
            continue
        if ws not in seen_workspaces:
            seen_workspaces[ws] = _load_cleanignore(REPO_ROOT / ws)
        rel_to_ws = Path(*rel.parts[len(ws.parts):])
        if _is_ignored(rel_to_ws, seen_workspaces[ws]):
            continue
        diagnostics.append(_DIAG.format(rel=rel))
    return sorted(diagnostics)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Scan research/<slug>/workspace/ paths for execution-script "
            "stragglers (.py/.sh/.log) per RESEARCH.md R.4.4."
        ),
    )
    ap.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Files or directories to scan. Defaults to research/.",
    )
    args = ap.parse_args(argv)

    paths = args.paths or [REPO_ROOT / "research"]
    diagnostics = scan(paths)
    for line in diagnostics:
        print(line, file=sys.stderr)
    return 1 if diagnostics else 0


if __name__ == "__main__":
    sys.exit(main())
