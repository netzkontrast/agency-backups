#!/usr/bin/env python3
"""check-spec-runtime-state — flag runtime-state sections in root specs.

Background: README.md §11.6 R.19 forbids runtime state from living in
root governance specs (the entry-point files agents read on every
session). Task 055 lifts an existing `## LOOP_LOG` block out of
AGENTS.md and lands this guard so the pattern cannot drift back.

Scope: the closed list of root specs (AGENTS, TASK, PROMPT, RESEARCH,
FOLDERS, PRE_COMMIT, FRUSTRATED, MAINTENANCE) plus README.md and
CLAUDE.md. Within those files, every `## ` heading is normalised and
compared against a closed vocabulary of forbidden runtime-state names
(case-insensitive, ignoring trailing punctuation).

Severity: WARN by default. With `--strict`, WARN promotes to ERROR
and the script exits non-zero.

Usage:
    python3 tools/check-spec-runtime-state.py [--strict] [--root PATH]

Exit:
    0 — no findings (or only WARN findings without --strict)
    1 — at least one finding under --strict
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT_SPEC_FILES = (
    "AGENTS.md",
    "TASK.md",
    "PROMPT.md",
    "RESEARCH.md",
    "FOLDERS.md",
    "PRE_COMMIT.md",
    "FRUSTRATED.md",
    "MAINTENANCE.md",
    "README.md",
    "CLAUDE.md",
    "SKILLS.md",
)

FORBIDDEN_HEADINGS = (
    "LOOP_LOG",
    "SESSION_LOG",
    "RUN_LOG",
    "ITERATION_LOG",
    "STATE",
)


HEADING_RE = re.compile(r"^##\s+(.*?)\s*$")


def _normalise(name: str) -> str:
    """Strip trailing punctuation so `## STATE:` and `## STATE` collide."""
    s = name.strip()
    while s and s[-1] in ":—–- \t":
        s = s[:-1]
    return s.upper()


def scan_file(path: Path) -> list[tuple[int, str]]:
    """Return (line_number, raw_heading) for every banned heading in `path`.

    Headings inside fenced code blocks are ignored.
    """
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    findings: list[tuple[int, str]] = []
    in_fence = False
    fence_marker: str | None = None
    for idx, raw in enumerate(text.splitlines(), start=1):
        s = raw.lstrip()
        if s.startswith("```") or s.startswith("~~~"):
            marker = s[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif fence_marker == marker:
                in_fence = False
                fence_marker = None
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(raw)
        if not m:
            continue
        heading = m.group(1)
        norm = _normalise(heading)
        if norm in FORBIDDEN_HEADINGS:
            findings.append((idx, heading))
    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="check-spec-runtime-state")
    ap.add_argument("--strict", action="store_true",
                    help="promote WARN to ERROR and exit non-zero on any finding")
    ap.add_argument("--root", default=".",
                    help="repository root (default: current directory)")
    ap.add_argument("paths", nargs="*",
                    help="explicit files to scan (overrides ROOT_SPEC_FILES)")
    args = ap.parse_args(argv)

    repo_root = Path(args.root).resolve()
    if args.paths:
        targets = [Path(p) for p in args.paths]
    else:
        targets = [repo_root / name for name in ROOT_SPEC_FILES]

    severity = "ERROR" if args.strict else "WARN"
    found = 0
    for target in targets:
        for line, heading in scan_file(target):
            try:
                rel = target.resolve().relative_to(repo_root).as_posix()
            except ValueError:
                rel = str(target)
            print(
                f"{rel}:{line}:{severity}:R.19:"
                f"runtime-state heading '## {heading}' in root spec — move "
                f"to maintenance/session-logs/ (Task 055)",
                file=sys.stderr,
            )
            found += 1

    if found == 0:
        return 0
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
