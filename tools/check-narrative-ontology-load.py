#!/usr/bin/env python3
"""Narrative-ontology load discipline checker (AGENTS.md NO.5).

AGENTS.md §NO.5 (lines 254, 286-292) forbids loading the 215-entry
`maintenance/schemas/narrative-ontology/ontology.json` from agents whose
active Task has no narrative scope. This linter is a heuristic gate:

  * Surface:
      python3 tools/check-narrative-ontology-load.py <task-folder-or-task.md>
      Exits 0 (clean) or 2 (WARN — narrative ontology loaded in
      non-narrative task).

  * Heuristic:
      WARN iff (a) the active task's `task_affects_paths` does NOT include
      ANY of `skills/dramatica-*`, `skills/ncp-*`, `skills/novel-*` (or
      their `**` subtrees), AND (b) either `task_affects_paths` itself
      OR the staged-files diff references something under
      `maintenance/schemas/narrative-ontology/`.

  * Edge case: missing/unreadable task.md → exit 0 (no context, no claim).

Diagnostic shape: `<file>::<level>:<code>:<message>` (matches the
fm-validate diagnostic shape used elsewhere in this repo).

Run from repo root.
"""
from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path

# Wire in the canonical frontmatter parser so we share semantics with the
# rest of the toolchain (fm/_core.py is the single source of truth).
# Guard: skip duplicate insert when the test suite imports this module
# alongside its own sys.path edits.
_FM_PATH = str(Path(__file__).resolve().parent / "fm")
if _FM_PATH not in sys.path:
    sys.path.insert(0, _FM_PATH)
try:
    import _core  # type: ignore  # noqa: E402
    read_fm = _core.read_fm
    str_list = _core.str_list
except ImportError:
    # Graceful degradation per repo's advisory-linter convention: if the
    # frontmatter parser is unavailable (e.g. mid-toolchain-migration window
    # per MAINTENANCE.md §1), exit clean rather than crash. check-governance.sh
    # invokes this linter advisory-tier (`|| true`), so an unhandled crash
    # would silently no-op and rob the operator of any signal.
    print(
        "check-narrative-ontology-load: tools/fm/_core.py not importable — "
        "skipping (advisory linter, exit 0).",
        file=sys.stderr,
    )
    raise SystemExit(0)

EXIT_OK = 0
EXIT_WARN = 2

NARRATIVE_GLOBS = (
    "skills/dramatica-*",
    "skills/dramatica-*/**",
    "skills/ncp-*",
    "skills/ncp-*/**",
    "skills/novel-*",
    "skills/novel-*/**",
)

NARRATIVE_ONTOLOGY_PREFIX = "maintenance/schemas/narrative-ontology/"

DIAG_CODE = "NO.5"


def _normalise(p: str) -> str:
    """Strip leading `./` and trailing `/` so glob-matching is consistent."""
    return p.strip().lstrip("./").rstrip("/")


def is_narrative_scope(paths: list[str]) -> bool:
    """True iff any entry in `paths` matches a narrative-scope glob."""
    for raw in paths:
        p = _normalise(raw)
        if not p:
            continue
        for pattern in NARRATIVE_GLOBS:
            if fnmatch.fnmatchcase(p, pattern):
                return True
            # Allow a directory entry (e.g. `skills/dramatica-foo/`) to match
            # the bare pattern even when the user did not append `/**`.
            if fnmatch.fnmatchcase(p + "/x", pattern):
                return True
    return False


def references_narrative_ontology(paths: list[str]) -> bool:
    """True iff any entry sits under `maintenance/schemas/narrative-ontology/`."""
    for raw in paths:
        p = _normalise(raw)
        if not p:
            continue
        if p.startswith(NARRATIVE_ONTOLOGY_PREFIX):
            return True
        if p == NARRATIVE_ONTOLOGY_PREFIX.rstrip("/"):
            return True
    return False


def staged_paths() -> list[str]:
    """Best-effort list of staged file paths (empty when git is unavailable)."""
    try:
        result = subprocess.run(
            ["git", "diff", "--staged", "--name-only"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return []
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def resolve_task_md(arg: Path) -> Path | None:
    """Accept either a task folder or a task.md file; return the .md or None."""
    if arg.is_file() and arg.name == "task.md":
        return arg
    if arg.is_dir():
        candidate = arg / "task.md"
        if candidate.is_file():
            return candidate
    return None


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect narrative-ontology loads in non-narrative tasks (AGENTS.md NO.5).",
    )
    parser.add_argument(
        "target",
        type=Path,
        help="Path to a task folder (e.g. tasks/032-foo/) or a task.md file.",
    )
    parser.add_argument(
        "--paths-from-frontmatter-only",
        action="store_true",
        help=(
            "Skip `git diff --staged` and consult only `task_affects_paths` "
            "when deciding whether the narrative ontology was loaded. "
            "Used by the test suite for determinism."
        ),
    )
    args = parser.parse_args(argv)

    task_md = resolve_task_md(args.target)
    if task_md is None:
        # Edge case: no task context. NO.5 is silent by design.
        return EXIT_OK

    fm = read_fm(task_md)
    affects = str_list(fm, "task_affects_paths")

    if is_narrative_scope(affects):
        # Narrative task — loading the ontology is fully permitted.
        return EXIT_OK

    references = list(affects)
    if not args.paths_from_frontmatter_only:
        references.extend(staged_paths())

    if not references_narrative_ontology(references):
        return EXIT_OK

    diag_path = task_md.as_posix()
    print(
        f"{diag_path}::WARN:{DIAG_CODE}:"
        "narrative-ontology load detected in a non-narrative task — "
        "task_affects_paths does not include skills/dramatica-* / "
        "skills/ncp-* / skills/novel-*, but reads against "
        "maintenance/schemas/narrative-ontology/ are present "
        "(AGENTS.md NO.5).",
        file=sys.stderr,
    )
    return EXIT_WARN


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
