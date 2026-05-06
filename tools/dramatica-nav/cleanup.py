#!/usr/bin/env python3
"""cleanup.py — Dramatica corpus cleanup linter (Task 030 ST-6).

The linter prevents the four corruption classes Task 030 ST-1..ST-4 stripped
from re-entering the corpus. The v0.1 lint catalogue is LOCKED at exactly
four rules; growing it requires an `agency-adr` ADR (Task 027 spec, Task 028
CLI). The `RULES` module variable is asserted ``len(RULES) == 4`` by the test
suite to enforce the cap.

Rules
-----

DR-CLEAN-001  copyright-footer
    Block any line matching the Screenplay Systems copyright footer regex
    (``^Copyright \\(c\\) 2001 Screenplay Systems Inc\\..*$``). Auto-fix:
    delete the line, the immediately-preceding blank, and the immediately-
    following page-number-only line (mirrors the ST-1 pattern).

DR-CLEAN-002  page-number-only
    Block orphan page-number-only lines (``^[0-9]+\\.\\s*$``) surrounded by
    blanks. The "surrounded by blanks" predicate distinguishes a page-break
    artefact from a numbered-list item. Auto-fix: delete the line and
    collapse the surrounding blanks.

DR-CLEAN-003  double-apostrophe
    Block any ``''`` escape in body text. Auto-fix: ``''`` -> ``'``.

DR-CLEAN-004  see-x-empty-redirect
    Block any ``## `` heading whose body resolves to ``See <Other>`` with
    <= 2 lines of substantive text before the next heading / EOF.
    NON-AUTO-FIX (manual decision required: alias-on-canonical or reify
    body).

CLI surface
-----------

::

    cleanup.py --check               # exit 1 on any hit; print diagnostic table
    cleanup.py --apply               # auto-fix mechanically safe rules; non-zero on remaining
    cleanup.py --apply --dry-run     # preview unified diff without writing
    cleanup.py --explain <rule-id>   # rationale + cite-anchor for one rule
    cleanup.py --baseline            # emit JSON baseline file (per-rule counts)

agency-adr integration
----------------------

If ``agency-adr`` is on PATH, ``--explain`` will surface the ratified ADR ID
for any rule whose normative source has been recorded in the ADR registry.
If ``agency-adr`` is NOT on PATH, rule violations are also emitted to stderr
in JSON-line format (one object per violation) so a downstream ADR ingestor
can consume them later.

# TODO(after-028): replace the JSON-line stderr fallback with a direct
# ``agency-adr`` API call once Task 028's CLI lands.
"""

from __future__ import annotations

import argparse
import dataclasses
import difflib
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Callable, Iterable

# -------------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------------

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parents[1]  # tools/dramatica-nav -> tools -> repo root
VOCAB_DIR = _REPO_ROOT / "skills" / "dramatica-vocabulary" / "references"
THEORY_DIR = _REPO_ROOT / "skills" / "dramatica-theory" / "references"
BASELINE_PATH = _HERE / "cleanup-baseline.json"

# Files excluded from the linter scan (different structure / not in scope).
EXCLUDED_NAMES = frozenset({
    "_synonym-lookup.md",
    "dynamic-pairs-index.md",
    "SKILL.md",
})

# -------------------------------------------------------------------------
# Regexes
# -------------------------------------------------------------------------

COPYRIGHT_RE = re.compile(r"^Copyright \(c\) 2001 Screenplay Systems Inc\..*$")
PAGE_NUMBER_RE = re.compile(r"^[0-9]+\.\s*$")
DOUBLE_APOSTROPHE_RE = re.compile(r"''")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SEE_BODY_RE = re.compile(r"^\s*See\s+\S+", re.IGNORECASE)


# -------------------------------------------------------------------------
# Diagnostics
# -------------------------------------------------------------------------

@dataclasses.dataclass(frozen=True)
class Diagnostic:
    """One rule hit. ``line`` is 1-indexed for human consumption."""

    rule_id: str
    path: Path
    line: int
    excerpt: str

    def to_json_dict(self, repo_root: Path) -> dict:
        try:
            rel = str(self.path.relative_to(repo_root))
        except ValueError:
            rel = str(self.path)
        return {
            "rule_id": self.rule_id,
            "path": rel,
            "line": self.line,
            "excerpt": self.excerpt,
        }

    def format_row(self, repo_root: Path) -> str:
        try:
            rel = str(self.path.relative_to(repo_root))
        except ValueError:
            rel = str(self.path)
        excerpt = self.excerpt
        if len(excerpt) > 80:
            excerpt = excerpt[:77] + "..."
        return f"{self.rule_id}\t{rel}:{self.line}\t{excerpt}"


# -------------------------------------------------------------------------
# Rule definitions
# -------------------------------------------------------------------------

CheckFn = Callable[[list[str], Path], list[Diagnostic]]
ApplyFn = Callable[[list[str]], tuple[list[str], int]]


@dataclasses.dataclass(frozen=True)
class Rule:
    """A single lint rule. Keep the catalogue at exactly four entries."""

    rule_id: str
    short_name: str
    summary: str
    rationale: str
    cite_anchor: str
    auto_fix: bool
    check: CheckFn
    apply: ApplyFn  # noqa: A003 — `apply` is a method name, not the builtin


# ---- DR-CLEAN-001 -------------------------------------------------------

def _check_copyright(lines: list[str], path: Path) -> list[Diagnostic]:
    out: list[Diagnostic] = []
    for i, line in enumerate(lines):
        if COPYRIGHT_RE.match(line):
            out.append(Diagnostic("DR-CLEAN-001", path, i + 1, line))
    return out


def _apply_copyright(lines: list[str]) -> tuple[list[str], int]:
    n = len(lines)
    keep = [True] * n
    fixes = 0
    for i in range(n):
        if not keep[i]:
            continue
        if COPYRIGHT_RE.match(lines[i]):
            fixes += 1
            keep[i] = False
            # Drop preceding blank.
            if i - 1 >= 0 and lines[i - 1].strip() == "" and keep[i - 1]:
                keep[i - 1] = False
            # Drop trailing blank + page-number + blank (mirrors ST-1).
            j = i + 1
            if j < n and lines[j].strip() == "":
                keep[j] = False
                j += 1
            if j < n and PAGE_NUMBER_RE.match(lines[j]):
                keep[j] = False
                j += 1
                if j < n and lines[j].strip() == "":
                    keep[j] = False
    return [lines[i] for i in range(n) if keep[i]], fixes


# ---- DR-CLEAN-002 -------------------------------------------------------

def _is_orphan_page_number(lines: list[str], i: int) -> bool:
    """A page-number-only line surrounded by blanks (or BOF/EOF)."""

    if not PAGE_NUMBER_RE.match(lines[i]):
        return False
    n = len(lines)
    before_blank = i == 0 or lines[i - 1].strip() == ""
    after_blank = i == n - 1 or lines[i + 1].strip() == ""
    return before_blank and after_blank


def _check_page_number(lines: list[str], path: Path) -> list[Diagnostic]:
    out: list[Diagnostic] = []
    for i in range(len(lines)):
        if _is_orphan_page_number(lines, i):
            out.append(Diagnostic("DR-CLEAN-002", path, i + 1, lines[i]))
    return out


def _apply_page_number(lines: list[str]) -> tuple[list[str], int]:
    n = len(lines)
    keep = [True] * n
    fixes = 0
    for i in range(n):
        if not keep[i]:
            continue
        if not PAGE_NUMBER_RE.match(lines[i]):
            continue
        before_blank = i == 0 or (lines[i - 1].strip() == "" and keep[i - 1])
        after_blank = i == n - 1 or (lines[i + 1].strip() == "" and keep[i + 1])
        if not (before_blank and after_blank):
            continue
        keep[i] = False
        fixes += 1
        # Collapse paired blanks: drop the trailing blank if both surround.
        if (
            0 < i < n - 1
            and lines[i - 1].strip() == ""
            and lines[i + 1].strip() == ""
            and keep[i + 1]
        ):
            keep[i + 1] = False
    return [lines[i] for i in range(n) if keep[i]], fixes


# ---- DR-CLEAN-003 -------------------------------------------------------

def _check_double_apostrophe(lines: list[str], path: Path) -> list[Diagnostic]:
    out: list[Diagnostic] = []
    for i, line in enumerate(lines):
        if DOUBLE_APOSTROPHE_RE.search(line):
            out.append(Diagnostic("DR-CLEAN-003", path, i + 1, line))
    return out


def _apply_double_apostrophe(lines: list[str]) -> tuple[list[str], int]:
    fixes = 0
    out: list[str] = []
    for line in lines:
        count = line.count("''")
        if count:
            fixes += count
            line = line.replace("''", "'")
        out.append(line)
    return out, fixes


# ---- DR-CLEAN-004 -------------------------------------------------------

def _iter_h2_blocks(lines: list[str]) -> Iterable[tuple[int, str, list[str]]]:
    """Yield ``(heading_index, heading_text, body_lines)`` for each ``## `` block.

    ``body_lines`` runs from the line after the heading up to (but not
    including) the next ``# {1,6}`` heading or EOF.
    """

    n = len(lines)
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if not m or len(m.group(1)) != 2:
            continue
        body: list[str] = []
        j = i + 1
        while j < n:
            if HEADING_RE.match(lines[j]):
                break
            body.append(lines[j])
            j += 1
        yield i, m.group(2), body


def _check_see_redirect(lines: list[str], path: Path) -> list[Diagnostic]:
    out: list[Diagnostic] = []
    for idx, heading_text, body in _iter_h2_blocks(lines):
        substantive = [b for b in body if b.strip()]
        if not substantive:
            continue
        if len(substantive) > 2:
            continue
        if SEE_BODY_RE.match(substantive[0]):
            excerpt = f"## {heading_text} -> {substantive[0].strip()}"
            out.append(Diagnostic("DR-CLEAN-004", path, idx + 1, excerpt))
    return out


def _apply_see_redirect(lines: list[str]) -> tuple[list[str], int]:
    """DR-CLEAN-004 is NON-AUTO-FIX. Always returns the input untouched.

    The check still runs in ``--apply`` mode and remaining diagnostics
    cause a non-zero exit. The caller surfaces a manual-decision-required
    warning when a hit is present.
    """

    return lines, 0


# -------------------------------------------------------------------------
# Catalogue (LOCKED at 4 rules — see module docstring + tests)
# -------------------------------------------------------------------------

RULES: tuple[Rule, ...] = (
    Rule(
        rule_id="DR-CLEAN-001",
        short_name="copyright-footer",
        summary="Block Screenplay Systems copyright footer line.",
        rationale=(
            "PDF-extract residue. The Phillips/Huntley dictionary embeds a "
            "Screenplay Systems copyright footer at every page break; the "
            "line is layout chrome, not source content. ST-1 stripped 38 "
            "occurrences from the vocabulary references and this rule "
            "prevents regression. Auto-fix removes the line plus the "
            "preceding blank and any trailing page-number residue, mirroring "
            "the ST-1 algorithm."
        ),
        cite_anchor=(
            "tasks/030-cleanup-dramatica-skills-corpus/notes.md#21-pdf-page-break-footers"
        ),
        auto_fix=True,
        check=_check_copyright,
        apply=_apply_copyright,
    ),
    Rule(
        rule_id="DR-CLEAN-002",
        short_name="page-number-only",
        summary="Block orphan page-number-only line surrounded by blanks.",
        rationale=(
            "PDF-extract residue. A line of the form '<digits>.' surrounded "
            "by blank lines is a page-break footer remnant — never a "
            "numbered-list item, since list items never sit alone in a "
            "stand-alone paragraph. ST-1 stripped 324 occurrences from the "
            "theory references. Auto-fix deletes the line and collapses the "
            "paired blanks."
        ),
        cite_anchor=(
            "tasks/030-cleanup-dramatica-skills-corpus/notes.md#22-page-number-only-lines--09s"
        ),
        auto_fix=True,
        check=_check_page_number,
        apply=_apply_page_number,
    ),
    Rule(
        rule_id="DR-CLEAN-003",
        short_name="double-apostrophe",
        summary="Block '' escape; suggest single ' replacement.",
        rationale=(
            "CLI quote-escape residue. '' originates from shell-escaped "
            "single quotes that survived the OCR-to-markdown conversion. "
            "Auto-fix replaces every occurrence with a single apostrophe."
        ),
        cite_anchor=(
            "tasks/030-cleanup-dramatica-skills-corpus/subtasks/06-build-cleanup-linter.md#rules"
        ),
        auto_fix=True,
        check=_check_double_apostrophe,
        apply=_apply_double_apostrophe,
    ),
    Rule(
        rule_id="DR-CLEAN-004",
        short_name="see-x-empty-redirect",
        summary="Block ## heading whose body is 'See <Other>' with <=2 lines.",
        rationale=(
            "An empty redirect ('## Female Mental Sex' -> 'See Intuitive') "
            "is a navigator dead end: the heading mints an anchor that the "
            "ontology cannot resolve. NON-AUTO-FIX: the right resolution "
            "depends on intent (reify the entry with substantive prose, or "
            "delete the heading and add the alias to the canonical entry's "
            "deprecated_aliases list). ST-4 hand-resolved the v0.1 hits."
        ),
        cite_anchor=(
            "tasks/030-cleanup-dramatica-skills-corpus/task.md#anti-patterns-to-avoid"
        ),
        auto_fix=False,
        check=_check_see_redirect,
        apply=_apply_see_redirect,
    ),
)


# -------------------------------------------------------------------------
# Walking the corpus
# -------------------------------------------------------------------------

def iter_target_files(roots: Iterable[Path] | None = None) -> list[Path]:
    """Return the markdown files under the dramatica references trees.

    ``roots`` defaults to the canonical theory + vocabulary references
    directories. Tests can pass synthetic roots.
    """

    roots = list(roots) if roots is not None else [VOCAB_DIR, THEORY_DIR]
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.glob("*.md")):
            if path.name in EXCLUDED_NAMES:
                continue
            files.append(path)
    return files


def run_check(
    files: Iterable[Path] | None = None,
    rules: Iterable[Rule] = RULES,
) -> list[Diagnostic]:
    """Run every rule's ``check`` against every target file."""

    files = list(files) if files is not None else iter_target_files()
    diagnostics: list[Diagnostic] = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:  # pragma: no cover — defensive
            print(f"WARN: could not read {path}: {exc}", file=sys.stderr)
            continue
        lines = text.split("\n")
        for rule in rules:
            diagnostics.extend(rule.check(lines, path))
    return diagnostics


def run_apply(
    files: Iterable[Path] | None = None,
    rules: Iterable[Rule] = RULES,
    dry_run: bool = False,
) -> tuple[dict[Path, str], dict[str, int]]:
    """Run every auto-fixable rule's ``apply`` against every target file.

    Returns ``(diffs, fix_counts)`` where ``diffs`` maps file path -> the
    rewritten text (only for files that changed) and ``fix_counts`` maps
    rule id -> total fixes applied.
    """

    rules = list(rules)
    files = list(files) if files is not None else iter_target_files()
    diffs: dict[Path, str] = {}
    fix_counts: dict[str, int] = {r.rule_id: 0 for r in rules}
    for path in files:
        try:
            before = path.read_text(encoding="utf-8")
        except OSError as exc:  # pragma: no cover
            print(f"WARN: could not read {path}: {exc}", file=sys.stderr)
            continue
        lines = before.split("\n")
        changed = False
        for rule in rules:
            if not rule.auto_fix:
                continue
            new_lines, fixes = rule.apply(lines)
            if fixes:
                fix_counts[rule.rule_id] += fixes
                lines = new_lines
                changed = True
        if not changed:
            continue
        after = "\n".join(lines)
        diffs[path] = after
        if not dry_run:
            path.write_text(after, encoding="utf-8")
    return diffs, fix_counts


# -------------------------------------------------------------------------
# agency-adr integration
# -------------------------------------------------------------------------

def _agency_adr_on_path() -> bool:
    return shutil.which("agency-adr") is not None


def _emit_adr_jsonlines(diagnostics: Iterable[Diagnostic]) -> None:
    """Emit one JSON object per violation to stderr (ingestible by future
    agency-adr tooling — schema TBD by Task 028).
    """

    for d in diagnostics:
        sys.stderr.write(
            json.dumps(
                {
                    "kind": "lint-violation",
                    "tool": "tools/dramatica-nav/cleanup.py",
                    **d.to_json_dict(_REPO_ROOT),
                }
            )
            + "\n"
        )


# -------------------------------------------------------------------------
# CLI handlers
# -------------------------------------------------------------------------

def _format_diff(path: Path, before: str, after: str, repo_root: Path) -> str:
    try:
        rel = str(path.relative_to(repo_root))
    except ValueError:
        rel = str(path)
    diff = difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile=rel,
        tofile=rel,
        n=2,
    )
    return "".join(diff)


def _print_diagnostic_table(
    diagnostics: list[Diagnostic],
    repo_root: Path,
    stream=sys.stdout,
) -> None:
    if not diagnostics:
        stream.write("cleanup.py: 0 diagnostics\n")
        return
    stream.write(f"cleanup.py: {len(diagnostics)} diagnostic(s)\n")
    stream.write("rule\tlocation\texcerpt\n")
    for d in diagnostics:
        stream.write(d.format_row(repo_root) + "\n")
    # Per-rule summary.
    counts: dict[str, int] = {}
    for d in diagnostics:
        counts[d.rule_id] = counts.get(d.rule_id, 0) + 1
    stream.write("\nsummary:\n")
    for rule in RULES:
        stream.write(f"  {rule.rule_id}\t{counts.get(rule.rule_id, 0)}\n")


def cmd_check(args: argparse.Namespace) -> int:
    diagnostics = run_check()
    _print_diagnostic_table(diagnostics, _REPO_ROOT)
    if diagnostics and not _agency_adr_on_path():
        _emit_adr_jsonlines(diagnostics)
    return 1 if diagnostics else 0


def cmd_apply(args: argparse.Namespace) -> int:
    files = iter_target_files()
    if args.dry_run:
        # Read each file, apply, emit diff.
        for path in files:
            before = path.read_text(encoding="utf-8")
            lines = before.split("\n")
            changed = False
            for rule in RULES:
                if not rule.auto_fix:
                    continue
                new_lines, fixes = rule.apply(lines)
                if fixes:
                    lines = new_lines
                    changed = True
            if changed:
                after = "\n".join(lines)
                sys.stdout.write(_format_diff(path, before, after, _REPO_ROOT))
        # Re-run check post-(simulated)-fix on freshly-read content +
        # NON-AUTO-FIX rules to surface remaining diagnostics.
        diagnostics = run_check()
        non_auto = [d for d in diagnostics if d.rule_id == "DR-CLEAN-004"]
        if non_auto:
            sys.stderr.write(
                "\nNON-AUTO-FIX (manual decision required):\n"
            )
            for d in non_auto:
                sys.stderr.write("  " + d.format_row(_REPO_ROOT) + "\n")
        return 1 if non_auto else 0

    diffs, fix_counts = run_apply(files=files, dry_run=False)
    sys.stderr.write("cleanup.py --apply summary:\n")
    for rule in RULES:
        sys.stderr.write(
            f"  {rule.rule_id}\t{fix_counts.get(rule.rule_id, 0)} fix(es)\n"
        )
    sys.stderr.write(f"  files rewritten\t{len(diffs)}\n")

    # Re-run check to see remaining (NON-AUTO-FIX) diagnostics.
    remaining = run_check()
    if remaining:
        sys.stderr.write("\ncleanup.py --apply: remaining diagnostics:\n")
        for d in remaining:
            sys.stderr.write("  " + d.format_row(_REPO_ROOT) + "\n")
        non_auto = [d for d in remaining if d.rule_id == "DR-CLEAN-004"]
        if non_auto:
            sys.stderr.write(
                "manual-decision-required: alias-on-canonical or reify body "
                "for each DR-CLEAN-004 hit listed above.\n"
            )
        return 1
    return 0


def cmd_explain(args: argparse.Namespace) -> int:
    rule_id = args.rule_id
    for rule in RULES:
        if rule.rule_id == rule_id:
            print(f"{rule.rule_id} — {rule.short_name}")
            print(f"summary  : {rule.summary}")
            print(f"auto-fix : {rule.auto_fix}")
            print()
            print("rationale:")
            print(f"  {rule.rationale}")
            print()
            print(f"cite-anchor: {rule.cite_anchor}")
            if not _agency_adr_on_path():
                print()
                print(
                    "# TODO(after-028): once agency-adr CLI lands, this output "
                    "should surface the ratified ADR ID for this rule. The "
                    "current path emits one JSON-line per violation to stderr "
                    "in --check mode."
                )
            return 0
    valid = ", ".join(r.rule_id for r in RULES)
    print(f"ERROR: unknown rule {rule_id!r}. Valid: {valid}", file=sys.stderr)
    return 2


def cmd_baseline(args: argparse.Namespace) -> int:
    diagnostics = run_check()
    counts: dict[str, int] = {r.rule_id: 0 for r in RULES}
    for d in diagnostics:
        counts[d.rule_id] = counts.get(d.rule_id, 0) + 1
    payload = {
        "version": 1,
        "tool": "tools/dramatica-nav/cleanup.py",
        "total": len(diagnostics),
        "per_rule": counts,
    }
    out_path = Path(args.output) if args.output else BASELINE_PATH
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    try:
        rel = out_path.relative_to(_REPO_ROOT)
    except ValueError:
        rel = out_path
    print(f"cleanup.py: baseline written to {rel}", file=sys.stderr)
    print(json.dumps(payload, indent=2))
    return 0


# -------------------------------------------------------------------------
# Argparse entrypoint
# -------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cleanup.py",
        description="Dramatica corpus cleanup linter (Task 030 ST-6).",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--check",
        action="store_true",
        help="Lint and exit 1 on any hit; print diagnostic table.",
    )
    mode.add_argument(
        "--apply",
        action="store_true",
        help="Auto-fix mechanically-safe rules; non-zero exit on remaining.",
    )
    mode.add_argument(
        "--explain",
        metavar="RULE_ID",
        dest="explain_rule",
        help="Print rationale + cite-anchor for one rule.",
    )
    mode.add_argument(
        "--baseline",
        action="store_true",
        help="Emit per-rule diagnostic counts as a JSON baseline file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="(with --apply) preview unified diff without writing.",
    )
    parser.add_argument(
        "--output",
        metavar="PATH",
        help="(with --baseline) override the baseline output path.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.dry_run and not args.apply:
        parser.error("--dry-run requires --apply")
    if args.check:
        return cmd_check(args)
    if args.apply:
        return cmd_apply(args)
    if args.explain_rule is not None:
        args.rule_id = args.explain_rule
        return cmd_explain(args)
    if args.baseline:
        return cmd_baseline(args)
    parser.error("no mode selected")  # pragma: no cover
    return 2  # pragma: no cover


if __name__ == "__main__":
    sys.exit(main())
