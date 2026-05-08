#!/usr/bin/env python3
"""dynamic-readme-partition — verify static/dynamic boundary in operational ``readme.md``.

Spec anchors:
    research/repo-maintenance-protocol-spec/output/SPEC.md §3.1
    MAINTENANCE.md §3.2 (Dynamic Readme Updates)
    Task 039 ST-4 (anchor M.B.6)

Usage:
    python3 tools/maintenance/dynamic-readme-partition.py [<paths>]

Each PATH may be either a single ``readme.md`` or a directory under which
operational ``<NNN>-<slug>/readme.md`` (or ``<slug>/readme.md``) folders
live. The linter walks one operational level deep and inspects every
``readme.md``. Provider research sub-trees (``gemini``, ``gpt``, ``human``,
``other``) are exempt per FOLDERS.md F.1.1.

Default scan roots: ``tasks/``, ``research/``, ``prompts/``.

Heuristic
---------
The SPEC §3.1 mandates that every operational ``readme.md`` be partitioned
into a *static* section (Purpose / Linked Navigation / Assumptions Log)
above an HTML-comment boundary marker and a *dynamic* section (Current
State / Latest Synthesised Learnings / Open Blockers) below it. The agreed
markers are:

    <!-- BEGIN DYNAMIC -->
    <!-- END DYNAMIC -->

This linter classifies each ``## H2`` heading and verifies its placement
relative to the BEGIN marker. The rule-set:

* If neither marker is present, emit a single ``missing-marker`` advisory
  ("consider partitioning"). This is the **falsification mitigation** — the
  pre-existing corpus has no markers, so the linter MUST NOT punish that
  state with an ERROR (Task 039 ST-4 brief, Falsification clause).
* If exactly one marker is present, emit ``unbalanced-marker``.
* If a static heading appears below ``BEGIN DYNAMIC``, or a dynamic
  heading appears above it, emit ``misplaced-section``.
* If duplicate ``BEGIN`` or ``END`` markers exist, emit ``multiple-markers``.

Diagnostic format
-----------------
``<relpath>::WARN:M.B.6:<code>:<details>``

Compatible with ``tools/check-maintenance-bypass.py`` consumption and with
the unified ``tools/adr/runlog.py`` diagnostic shape.

Exit codes
----------
``0`` — no diagnostics emitted.
``2`` — at least one WARN diagnostic surfaced (advisory).
``1`` — usage error.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

# Reuse the shared frontmatter / section-finding library.
_TOOLS = Path(__file__).resolve().parent.parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
_FM = _TOOLS / "fm"
if str(_FM) not in sys.path:
    sys.path.insert(0, str(_FM))

try:
    import _core  # type: ignore  # noqa: E402
except ImportError:
    # Graceful degradation per repo's advisory-linter convention: if the
    # frontmatter parser is unavailable, exit clean rather than crash.
    print(
        "dynamic-readme-partition: tools/fm/_core.py not importable — "
        "skipping (advisory linter, exit 0).",
        file=sys.stderr,
    )
    raise SystemExit(0)


DIAG_PREFIX = "M.B.6"

# HTML-comment marker pattern. Tolerant to extra whitespace; strict on the
# token shape so accidental matches (e.g. inside fenced blocks) are rare.
BEGIN_MARKER_RE = re.compile(
    r"<!--\s*BEGIN\s+DYNAMIC\s*-->", re.IGNORECASE
)
END_MARKER_RE = re.compile(
    r"<!--\s*END\s+DYNAMIC\s*-->", re.IGNORECASE
)
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^```")

# Heading taxonomy per repo-maintenance-protocol-spec §3.1 + FOLDERS.md F.3.
# Compared case-insensitively after stripping decorative punctuation.
STATIC_HEADINGS = frozenset(
    {
        "purpose",
        "what",
        "what and why",
        "what",
        "files",
        "navigation",
        "linked navigation",
        "assumptions log",
    }
)
DYNAMIC_HEADINGS = frozenset(
    {
        "current state",
        "latest synthesised learnings",
        "latest synthesized learnings",
        "recent activity",
        "open blockers",
        "blockers",
    }
)

# Provider folders under /research/ — exempt per FOLDERS.md F.1.1.
PROVIDER_NAMES = frozenset({"gemini", "gpt", "human", "other"})

# Default scan roots when no paths are supplied.
DEFAULT_ROOTS = ("tasks", "research", "prompts")


def _normalise_heading(raw: str) -> str:
    """Lowercase + strip decorative trailing punctuation for taxonomy lookup."""
    return raw.strip().rstrip(":").strip().lower()


def _classify(heading: str) -> str:
    """Return ``static`` | ``dynamic`` | ``unknown`` for a heading."""
    n = _normalise_heading(heading)
    if n in STATIC_HEADINGS:
        return "static"
    if n in DYNAMIC_HEADINGS:
        return "dynamic"
    return "unknown"


def _scan_markers_and_h2(text: str) -> tuple[list[int], list[int], list[tuple[int, str]]]:
    """Return (begin_offsets, end_offsets, h2_entries).

    Each offset is a 0-based line index. ``h2_entries`` is a list of
    ``(line_index, heading_text)`` for every level-2 ATX heading found
    OUTSIDE fenced code blocks. Markers found inside fences are also
    ignored.
    """
    begin_offsets: list[int] = []
    end_offsets: list[int] = []
    h2_entries: list[tuple[int, str]] = []
    in_fence = False
    for idx, line in enumerate(text.splitlines()):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # A single line MAY contain both markers; we still want to flag both.
        if BEGIN_MARKER_RE.search(line):
            begin_offsets.append(idx)
        if END_MARKER_RE.search(line):
            end_offsets.append(idx)
        m = H2_RE.match(line)
        if m:
            h2_entries.append((idx, m.group(1)))
    return begin_offsets, end_offsets, h2_entries


def diagnostics_for(readme: Path) -> list[str]:
    """Return WARN diagnostic strings for a single ``readme.md``."""
    diags: list[str] = []
    try:
        text = readme.read_text(encoding="utf-8")
    except OSError as exc:
        diags.append(
            f"{readme}::WARN:{DIAG_PREFIX}:read-error:cannot read file ({exc})"
        )
        return diags

    # Strip frontmatter — markers in the YAML preamble would be a distinct
    # bug; the partition lives in the Markdown body.
    _fm_block, body = _core.split_frontmatter_and_body(text)

    begin_offsets, end_offsets, h2_entries = _scan_markers_and_h2(body)

    # Case 1 — no markers at all. Single advisory, never an error.
    if not begin_offsets and not end_offsets:
        diags.append(
            f"{readme}::WARN:{DIAG_PREFIX}:missing-marker:"
            f"no `<!-- BEGIN DYNAMIC -->` / `<!-- END DYNAMIC -->` markers found; "
            f"consider partitioning per repo-maintenance-protocol-spec §3.1"
        )
        return diags

    # Case 2 — duplicate markers.
    if len(begin_offsets) > 1:
        diags.append(
            f"{readme}::WARN:{DIAG_PREFIX}:multiple-markers:"
            f"`<!-- BEGIN DYNAMIC -->` appears {len(begin_offsets)} times "
            f"(lines {', '.join(str(o + 1) for o in begin_offsets)}); "
            f"exactly one is permitted"
        )
    if len(end_offsets) > 1:
        diags.append(
            f"{readme}::WARN:{DIAG_PREFIX}:multiple-markers:"
            f"`<!-- END DYNAMIC -->` appears {len(end_offsets)} times "
            f"(lines {', '.join(str(o + 1) for o in end_offsets)}); "
            f"exactly one is permitted"
        )

    # Case 3 — unbalanced (only one of the pair).
    if begin_offsets and not end_offsets:
        diags.append(
            f"{readme}::WARN:{DIAG_PREFIX}:unbalanced-marker:"
            f"`<!-- BEGIN DYNAMIC -->` present (line {begin_offsets[0] + 1}) "
            f"but matching `<!-- END DYNAMIC -->` is absent"
        )
    if end_offsets and not begin_offsets:
        diags.append(
            f"{readme}::WARN:{DIAG_PREFIX}:unbalanced-marker:"
            f"`<!-- END DYNAMIC -->` present (line {end_offsets[0] + 1}) "
            f"but matching `<!-- BEGIN DYNAMIC -->` is absent"
        )

    # Case 4 — partition exists; verify section placement.
    if begin_offsets:
        boundary = begin_offsets[0]
        end_boundary = end_offsets[0] if end_offsets else None
        for line_idx, heading in h2_entries:
            klass = _classify(heading)
            if klass == "unknown":
                continue
            if klass == "static" and line_idx > boundary:
                diags.append(
                    f"{readme}::WARN:{DIAG_PREFIX}:misplaced-section:"
                    f"static heading `## {heading.strip()}` at line {line_idx + 1} "
                    f"appears below the `<!-- BEGIN DYNAMIC -->` marker "
                    f"(line {boundary + 1}); move above the marker"
                )
            elif klass == "dynamic" and line_idx < boundary:
                diags.append(
                    f"{readme}::WARN:{DIAG_PREFIX}:misplaced-section:"
                    f"dynamic heading `## {heading.strip()}` at line {line_idx + 1} "
                    f"appears above the `<!-- BEGIN DYNAMIC -->` marker "
                    f"(line {boundary + 1}); move below the marker"
                )
            elif (
                klass == "dynamic"
                and end_boundary is not None
                and line_idx > end_boundary
            ):
                diags.append(
                    f"{readme}::WARN:{DIAG_PREFIX}:misplaced-section:"
                    f"dynamic heading `## {heading.strip()}` at line {line_idx + 1} "
                    f"appears below the `<!-- END DYNAMIC -->` marker "
                    f"(line {end_boundary + 1}); move into the dynamic block"
                )

    return diags


def _is_provider_research(path: Path, root: Path) -> bool:
    """True iff `path` lies under research/<provider>/ where <provider> ∈ PROVIDER_NAMES."""
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    parts = rel.parts
    if len(parts) < 2:
        return False
    if parts[0] != "research":
        return False
    return parts[1] in PROVIDER_NAMES


def _iter_readmes(target: Path, repo_root: Path | None = None) -> Iterable[Path]:
    """Yield every operational ``readme.md`` reachable under ``target``.

    Layout rules mirror ``check-assumption-log.py``: a single ``readme.md``
    target is yielded directly; a directory is walked one level deep and
    only second-level operational readmes are returned. Provider research
    sub-trees are skipped.
    """
    if target.is_file():
        if target.name.lower() == "readme.md":
            yield target
        return
    if not target.is_dir():
        return
    repo_root = repo_root or target
    for path in sorted(target.rglob("readme.md")):
        rel_parts = path.relative_to(target).parts
        if len(rel_parts) <= 1:
            # Top-level index (e.g. tasks/readme.md), not operational.
            continue
        if len(rel_parts) > 2:
            # Sub-artefact (workspace/, output/, subtasks/, …).
            continue
        if _is_provider_research(path, repo_root):
            continue
        yield path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="dynamic-readme-partition",
        description=(
            "Advisory linter for the static/dynamic readme partition "
            "(MAINTENANCE.md §3.2 / repo-maintenance-protocol-spec §3.1)."
        ),
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=list(DEFAULT_ROOTS),
        help=(
            "readme.md files or directories to scan "
            f"(default: {' '.join(DEFAULT_ROOTS)})"
        ),
    )
    args = parser.parse_args(argv)

    targets = [Path(p) for p in args.paths]
    if not targets:
        parser.error("no paths supplied")
        return 1

    repo_root = Path.cwd()
    all_diags: list[str] = []
    scanned = 0
    for target in targets:
        if not target.exists():
            print(
                f"dynamic-readme-partition: warning: path does not exist: {target}",
                file=sys.stderr,
            )
            continue
        for readme in _iter_readmes(target, repo_root):
            scanned += 1
            all_diags.extend(diagnostics_for(readme))

    for d in all_diags:
        print(d)

    print(
        f"dynamic-readme-partition: {len(all_diags)} WARN diagnostic(s) "
        f"across {scanned} readme.md file(s).",
        file=sys.stderr,
    )
    return 2 if all_diags else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
