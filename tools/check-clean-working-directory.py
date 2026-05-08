#!/usr/bin/env python3
"""check-clean-working-directory — repo-wide PC.1.1 enforcement.

Spec anchors:
    PRE_COMMIT.md PC.1.1 — "no temporary files, .py or .sh script
                           scratchpads, or loose log dumps".
    FOLDERS.md §8        — exemption table for non-operational storage
                           folders (`/tools/`, `/skills/`, `/templates/`,
                           `/maintenance/`, `/decisions/`, `/Agency-System/`).

Why a second linter?
--------------------

`tools/check-workspace-cleanliness.py` (Task 035 ST-2) already enforces
R.4.4 inside `research/<slug>/workspace/` only. PC.1.1 is broader: it
guards the *entire* working tree at commit time. The two linters share
a similar diagnostic shape but cover disjoint scopes.

Scope
-----

Default (no paths): walk the repo root and flag any `.py`/`.sh`/`.log`
file that is not inside an exempt directory and is not on the
`tools/.script-allowlist` allowlist.

Exempt directory prefixes (PRE_COMMIT.md PC.1.1 + FOLDERS.md §8):
    tools/         — repository tooling lives here by design.
    skills/        — versioned skill mirror; `.py` helpers permitted.
    templates/     — skeletons may carry placeholder scripts.
    maintenance/   — governance annex; opaque to the cleanliness scan.
    decisions/     — ADR ledger; `.py` files not expected but the dir
                     is exempt per FOLDERS.md §8 either way (no false
                     positives).
    Agency-System/ — frontend prototype; opaque per §8.
    .githooks/     — pre-commit hook scripts.
    .git/          — VCS internals.
    .agent_cache/  — agent-only cache (FOLDERS.md L3).

Always-allowed filenames (anywhere):
    session.log    — RESEARCH.md §4.5 mandates this file.

Allowlist (per-repo override):
    tools/.script-allowlist (one path per line, glob, `#` for comments)
    Use this for legitimate `.py` files kept under e.g.
    `tasks/<NNN>-<slug>/scripts/` for audit reasons (see Task 041).

Diagnostic format
-----------------

    <relpath>::ERROR:PC.1.1:script-scratchpad

Matches the ADR / Trust / FL-declaration linter shape so a single
MAINTENANCE.md aggregator can ingest the diagnostics.

Exit codes
----------

    0 — every scanned path is clean (or covered by an allowlist line).
    1 — at least one diagnostic emitted.
"""
from __future__ import annotations

import argparse
import fnmatch
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

_FORBIDDEN_SUFFIXES: frozenset[str] = frozenset({".py", ".sh", ".log"})

_ALWAYS_ALLOWED_NAMES: frozenset[str] = frozenset({"session.log"})

_EXEMPT_DIR_PREFIXES: tuple[str, ...] = (
    "tools/",
    "tests/",
    "skills/",
    "templates/",
    "maintenance/",
    "decisions/",
    "Agency-System/",
    ".githooks/",
    ".git/",
    ".agent_cache/",
)

_DIAG = "{rel}::ERROR:PC.1.1:script-scratchpad"

_ALLOWLIST_FILE = REPO_ROOT / "tools" / ".script-allowlist"


def _load_allowlist() -> list[str]:
    if not _ALLOWLIST_FILE.exists():
        return []
    patterns: list[str] = []
    for line in _ALLOWLIST_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def _is_exempt_dir(rel_posix: str) -> bool:
    return any(rel_posix.startswith(p) for p in _EXEMPT_DIR_PREFIXES)


def _is_allowlisted(rel_posix: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(rel_posix, pat) for pat in patterns)


def _iter_files(roots: list[Path]) -> list[Path]:
    out: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        if root.is_file():
            out.append(root)
            continue
        for f in root.rglob("*"):
            if f.is_file():
                out.append(f)
    return out


def scan(paths: list[Path], allowlist: list[str]) -> list[str]:
    diagnostics: list[str] = []
    for f in _iter_files(paths):
        suffix = f.suffix.lower()
        if suffix not in _FORBIDDEN_SUFFIXES:
            continue
        if f.name in _ALWAYS_ALLOWED_NAMES:
            continue
        try:
            rel = f.resolve().relative_to(REPO_ROOT).as_posix()
        except ValueError:
            # Path outside repo (shouldn't happen via default scan).
            rel = str(f)
        if _is_exempt_dir(rel):
            continue
        if _is_allowlisted(rel, allowlist):
            continue
        diagnostics.append(_DIAG.format(rel=rel))
    return sorted(diagnostics)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="PRE_COMMIT.md PC.1.1 — repo-wide script-scratchpad scan.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Files or directories to scan (default: repo root).",
    )
    args = parser.parse_args(argv)

    roots = args.paths if args.paths else [REPO_ROOT]
    allowlist = _load_allowlist()
    diagnostics = scan(roots, allowlist)

    for d in diagnostics:
        print(d, file=sys.stderr)
    return 0 if not diagnostics else 1


if __name__ == "__main__":
    raise SystemExit(main())
