#!/usr/bin/env python3
"""bundle-size-snapshot — emit a one-line measurement of the root-spec boot bundle.

Spec anchor:
    decisions/0009-root-spec-no-consolidation.md §"Falsifier triggers" F1
        — "Bundle-token cost exceeds 100,000 tokens" mandates a successor ADR.
        Without a repeatable measurement, F1 is theoretical. This script makes
        it mechanical.

Surface:
    python3 tools/maintenance/bundle-size-snapshot.py [--format text|json|runlog]
                                                      [--repo-root PATH]

Behaviour:
    Reads each root spec listed in BUNDLE_SPECS, sums their byte size,
    estimates token count at 4 chars/token (the canonical estimator used in
    ADR-0009 and the AGENTS.md narrative-section measurements). Emits a
    single line suitable for appending to `maintenance/run-log.md` or
    consumption by humans.

Exit codes:
    0 — measurement succeeded.
    1 — usage error or a bundle spec is missing.
    2 — bundle exceeds F1 threshold (>= 100_000 tokens). Advisory only;
        a maintainer triages whether to file the ADR-0009 successor.

The set of bundle specs is intentionally hard-coded here rather than
discovered, so adding a new root spec to the bundle is an explicit edit
to this file (and a re-measurement of the baseline). That is the same
discipline ADR-0009 itself relied on.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Iterable

# Suffix set considered when counting inbound references for a spec.
DEPENDENT_SCAN_SUFFIXES: tuple[str, ...] = (".md", ".py", ".sh")

# Top-level directories excluded from the dependent scan (large binary trees,
# vendored assets, agent caches). Cross-references that matter live in code
# and prose.
DEPENDENT_SCAN_SKIP_DIRS: frozenset[str] = frozenset({
    ".git",
    ".agent_cache",
    "node_modules",
    "Agency-System",
})

# The 11 root specs that make up the session-boot bundle per ADR-0009 §"Context".
# Adding or removing an entry is a deliberate amendment to the baseline.
BUNDLE_SPECS: tuple[str, ...] = (
    "AGENTS.md",
    "TASK.md",
    "PROMPT.md",
    "RESEARCH.md",
    "FOLDERS.md",
    "PRE_COMMIT.md",
    "FRUSTRATED.md",
    "MAINTENANCE.md",
    "SKILLS.md",
    "README.md",
    "maintenance/language-spec.md",
)

# The threshold ADR-0009 F1 trigger fires at.
F1_THRESHOLD_TOKENS = 100_000

# 4 chars per token — the canonical estimator used across ADR-0009,
# the AGENTS.md narrative-section measurement, and the Task 056 notes.
CHARS_PER_TOKEN = 4


def count_dependents(repo_root: Path, spec_rel: str) -> int:
    """Count files under repo_root that reference spec_rel by basename.

    ADR-0009 F2 ("either spec < 1000 tokens AND < 50 dependents") requires a
    cheap, deterministic inbound-reference count. We scan files with one of
    DEPENDENT_SCAN_SUFFIXES below repo_root, skipping top-level directories
    in DEPENDENT_SCAN_SKIP_DIRS, and count files whose contents contain the
    spec's basename (e.g. "PRE_COMMIT.md"). The spec file itself is excluded.
    """
    basename = Path(spec_rel).name
    target_abs = (repo_root / spec_rel).resolve()
    needle = basename.encode("utf-8")
    count = 0
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in DEPENDENT_SCAN_SUFFIXES:
            continue
        try:
            rel_parts = path.resolve().relative_to(repo_root.resolve()).parts
        except ValueError:
            continue
        if rel_parts and rel_parts[0] in DEPENDENT_SCAN_SKIP_DIRS:
            continue
        if path.resolve() == target_abs:
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if needle in data:
            count += 1
    return count


def measure_bundle(
    repo_root: Path,
    specs: Iterable[str] = BUNDLE_SPECS,
    *,
    include_dependents: bool = False,
) -> dict:
    """Return per-spec sizes and aggregate measurements.

    The return shape is the canonical record this tool emits in --format json
    and (with a one-line projection) in --format text / --format runlog.

    When include_dependents is True, each per-spec record additionally carries
    a `dependents` field (count of files referencing the spec by basename).
    Composed by tools/maintenance/adr-trigger-audit.py for ADR-0009 F2.
    """
    per_spec: list[dict] = []
    missing: list[str] = []
    total_bytes = 0
    total_lines = 0
    for rel in specs:
        path = repo_root / rel
        if not path.is_file():
            missing.append(rel)
            continue
        text = path.read_text(encoding="utf-8")
        nbytes = len(text.encode("utf-8"))
        nlines = text.count("\n") + (0 if text.endswith("\n") else 1)
        rec = {
            "path": rel,
            "lines": nlines,
            "bytes": nbytes,
            "tokens": nbytes // CHARS_PER_TOKEN,
        }
        if include_dependents:
            rec["dependents"] = count_dependents(repo_root, rel)
        per_spec.append(rec)
        total_bytes += nbytes
        total_lines += nlines
    return {
        "date": dt.date.today().isoformat(),
        "specs_measured": len(per_spec),
        "specs_missing": missing,
        "total_lines": total_lines,
        "total_bytes": total_bytes,
        "total_tokens": total_bytes // CHARS_PER_TOKEN,
        "f1_threshold_tokens": F1_THRESHOLD_TOKENS,
        "f1_triggered": (total_bytes // CHARS_PER_TOKEN) >= F1_THRESHOLD_TOKENS,
        "per_spec": per_spec,
    }


def format_text(snapshot: dict) -> str:
    lines = [
        f"# bundle-size snapshot ({snapshot['date']})",
        f"# specs measured: {snapshot['specs_measured']}; missing: {len(snapshot['specs_missing'])}",
    ]
    if snapshot["specs_missing"]:
        lines.append(f"# missing: {', '.join(snapshot['specs_missing'])}")
    lines.append("")
    for rec in snapshot["per_spec"]:
        lines.append(f"  {rec['path']:40s} {rec['lines']:>5} lines  {rec['bytes']:>7} bytes  ~{rec['tokens']:>6} tokens")
    lines.append("")
    f1_marker = " [F1-TRIGGERED]" if snapshot["f1_triggered"] else ""
    lines.append(
        f"  TOTAL{' ' * 35} {snapshot['total_lines']:>5} lines  "
        f"{snapshot['total_bytes']:>7} bytes  ~{snapshot['total_tokens']:>6} tokens"
        f"{f1_marker}"
    )
    lines.append("")
    lines.append(
        f"# ADR-0009 F1 threshold: {F1_THRESHOLD_TOKENS} tokens; "
        f"current: {snapshot['total_tokens']} "
        f"({'OVER' if snapshot['f1_triggered'] else 'under'})"
    )
    return "\n".join(lines)


def format_runlog(snapshot: dict) -> str:
    """One-line projection appendable to maintenance/run-log.md."""
    f1 = "F1-TRIGGERED" if snapshot["f1_triggered"] else "ok"
    return (
        f"{snapshot['date']} | bundle-size | "
        f"{snapshot['specs_measured']} specs / "
        f"{snapshot['total_lines']} lines / "
        f"{snapshot['total_bytes']} bytes / "
        f"~{snapshot['total_tokens']} tokens | "
        f"ADR-0009-F1={f1}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Measure the root-spec bundle size; back ADR-0009 F1.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json", "runlog"),
        default="text",
        help="Output format (default: text).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repo root (defaults to git toplevel discovery from CWD).",
    )
    parser.add_argument(
        "--include-dependents",
        action="store_true",
        help="Augment per-spec records with `dependents` count (ADR-0009 F2 input).",
    )
    args = parser.parse_args(argv)

    if args.repo_root is None:
        # Walk up looking for the AGENTS.md marker — same discipline as
        # tools/fm/_core.py.repo_root_from().
        cur = Path.cwd().resolve()
        while cur != cur.parent:
            if (cur / "AGENTS.md").is_file():
                args.repo_root = cur
                break
            cur = cur.parent
        if args.repo_root is None:
            print(
                "bundle-size-snapshot: ERROR: could not locate repo root (no AGENTS.md found in ancestors)",
                file=sys.stderr,
            )
            return 1

    snapshot = measure_bundle(args.repo_root, include_dependents=args.include_dependents)

    if snapshot["specs_missing"]:
        print(
            f"bundle-size-snapshot: ERROR: {len(snapshot['specs_missing'])} "
            f"bundle spec(s) missing from disk: {', '.join(snapshot['specs_missing'])}",
            file=sys.stderr,
        )
        return 1

    if args.format == "json":
        print(json.dumps(snapshot, indent=2, sort_keys=True))
    elif args.format == "runlog":
        print(format_runlog(snapshot))
    else:
        print(format_text(snapshot))

    return 2 if snapshot["f1_triggered"] else 0


if __name__ == "__main__":
    sys.exit(main())
