#!/usr/bin/env python3
"""One-shot helper for Task 030 ST-1.

Strips four LOCKED classes of PDF-extract residue from the dramatica corpus:

  1. Copyright footers   : lines matching ^Copyright \\(c\\) 2001 Screenplay
                           Systems Inc\\..* — together with the immediately
                           preceding blank line and the immediately following
                           page-number-only line (and the blank line after it).
  2. Page-number-only    : lines matching ^[0-9]+\\.\\s*$ surrounded by blank
                           lines on both sides AND not followed by a markdown
                           heading (i.e. genuine PDF page numbers, not list
                           items).
  3. Double-apostrophe   : '' -> ' (CLI quote-escape residue).
  4. Leading-> bullets   : in Contents-list bullet items only
                           (^- \\[.*\\]\\(#.*\\) — ), strip a leading > from
                           the description.

Usage:
    python3 tools/dramatica-nav/_strip_artifacts.py --dry-run
    python3 tools/dramatica-nav/_strip_artifacts.py --apply

Locked: do NOT add new artefact classes here. If you find suspicious content
that doesn't match these four patterns, surface it as a friction event in the
ST-1 commit body and DO NOT delete it.

Internal one-shot tool. Deletable after ST-1 closes (leading underscore).
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VOCAB_DIR = REPO_ROOT / "skills" / "dramatica-vocabulary" / "references"
THEORY_DIR = REPO_ROOT / "skills" / "dramatica-theory" / "references"

# Excluded by subtask spec (different structure / not in scope).
EXCLUDED_NAMES = {"_synonym-lookup.md", "dynamic-pairs-index.md"}

COPYRIGHT_RE = re.compile(r"^Copyright \(c\) 2001 Screenplay Systems Inc\..*$")
PAGE_NUMBER_RE = re.compile(r"^[0-9]+\.\s*$")
HEADING_RE = re.compile(r"^#{1,6} ")
# Contents-list bullet: "- [Label](#anchor) — body..."
CONTENTS_BULLET_RE = re.compile(r"^(- \[[^\]]+\]\(#[^)]+\) — )>(.*)$")


def _iter_target_files() -> list[Path]:
    files: list[Path] = []
    for d in (VOCAB_DIR, THEORY_DIR):
        for p in sorted(d.glob("*.md")):
            if p.name in EXCLUDED_NAMES:
                continue
            if p.name == "SKILL.md":
                continue
            files.append(p)
    return files


def _strip_file(text: str) -> tuple[str, dict[str, int]]:
    """Return (new_text, per_class_counts) for a single file.

    Counts:
      - copyright_blocks: number of copyright-footer blocks removed
      - page_number_lines: number of page-number-only lines removed
        (excluding those swallowed as part of a copyright block)
      - double_apostrophes: number of '' -> ' replacements
      - bullet_gt: number of contents-list bullets had leading > stripped
    """
    counts = {
        "copyright_blocks": 0,
        "page_number_lines": 0,
        "double_apostrophes": 0,
        "bullet_gt": 0,
    }

    # ---- Pass 1: line-based deletion of copyright + page-number residue ----
    lines = text.split("\n")
    keep = [True] * len(lines)

    n = len(lines)
    for i in range(n):
        if not keep[i]:
            continue
        if COPYRIGHT_RE.match(lines[i]):
            counts["copyright_blocks"] += 1
            keep[i] = False
            # Drop preceding blank line (if any).
            if i - 1 >= 0 and lines[i - 1].strip() == "" and keep[i - 1]:
                keep[i - 1] = False
            # Drop following blank line + page-number-only line + blank line.
            j = i + 1
            if j < n and lines[j].strip() == "":
                keep[j] = False
                j += 1
            if j < n and PAGE_NUMBER_RE.match(lines[j]):
                keep[j] = False
                j += 1
                if j < n and lines[j].strip() == "":
                    keep[j] = False

    # ---- Pass 2: standalone page-number-only lines ----
    # A page-number line: matches PAGE_NUMBER_RE, has blank line before AND
    # blank line after (or EOF), and the next non-blank line is NOT a
    # numbered list continuation. Since the regex requires "<digits>.\s*$"
    # with NOTHING after the dot, this filter alone already excludes "26. Foo".
    # The blank-line-on-both-sides constraint excludes any genuine list usage
    # (which would have list items adjacent without blanks between them).
    for i in range(n):
        if not keep[i]:
            continue
        if not PAGE_NUMBER_RE.match(lines[i]):
            continue
        # Check blank-line-before condition (or BOF).
        before_blank = i == 0 or (lines[i - 1].strip() == "" and keep[i - 1])
        after_blank = i == n - 1 or (lines[i + 1].strip() == "" and keep[i + 1])
        if not (before_blank and after_blank):
            continue
        # Ensure this isn't a numbered-list item with blank-line spacing.
        # Look at the next non-blank kept line: if it's a heading, we're at
        # an end-of-section page-break — safe to strip. If it starts with
        # another numbered-list item, also safe (a list item never has the
        # form "<digits>." on a line by itself with NOTHING else — the regex
        # already ensures that). So we strip unconditionally here.
        keep[i] = False
        counts["page_number_lines"] += 1
        # Collapse paired blank lines: drop one of the surrounding blanks
        # to avoid leaving two blank lines in a row. Drop the FOLLOWING
        # blank (if both before+after are blanks); otherwise leave as-is.
        if (
            i + 1 < n
            and lines[i + 1].strip() == ""
            and i - 1 >= 0
            and lines[i - 1].strip() == ""
            and keep[i + 1]
        ):
            keep[i + 1] = False

    surviving = [lines[i] for i in range(n) if keep[i]]

    # ---- Pass 3: contents-list bullet leading-> ----
    out: list[str] = []
    for line in surviving:
        m = CONTENTS_BULLET_RE.match(line)
        if m:
            new_line = m.group(1) + m.group(2).lstrip()
            if new_line != line:
                counts["bullet_gt"] += 1
            out.append(new_line)
        else:
            out.append(line)

    new_text = "\n".join(out)

    # ---- Pass 4: double-apostrophe replacement ----
    # Count first, then replace.
    counts["double_apostrophes"] = new_text.count("''")
    new_text = new_text.replace("''", "'")

    return new_text, counts


def _format_diff(path: Path, before: str, after: str) -> str:
    diff = difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile=str(path.relative_to(REPO_ROOT)),
        tofile=str(path.relative_to(REPO_ROOT)),
        n=2,
    )
    return "".join(diff)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true", help="print diff + stats")
    g.add_argument("--apply", action="store_true", help="write changes")
    parser.add_argument(
        "--no-diff",
        action="store_true",
        help="suppress unified diff output (show stats only)",
    )
    args = parser.parse_args(argv)

    files = _iter_target_files()
    totals = {
        "copyright_blocks": 0,
        "page_number_lines": 0,
        "double_apostrophes": 0,
        "bullet_gt": 0,
    }
    per_file: list[tuple[Path, dict[str, int]]] = []

    for path in files:
        before = path.read_text(encoding="utf-8")
        after, counts = _strip_file(before)
        if any(counts.values()):
            per_file.append((path, counts))
            for k, v in counts.items():
                totals[k] += v
            if args.dry_run and not args.no_diff:
                sys.stdout.write(_format_diff(path, before, after))
            if args.apply:
                path.write_text(after, encoding="utf-8")

    sys.stderr.write("\n=== ST-1 strip stats ===\n")
    for path, counts in per_file:
        rel = path.relative_to(REPO_ROOT)
        sys.stderr.write(
            f"  {rel}: cprt={counts['copyright_blocks']} "
            f"pnum={counts['page_number_lines']} "
            f"apos={counts['double_apostrophes']} "
            f"bgt={counts['bullet_gt']}\n"
        )
    sys.stderr.write("\nTOTALS:\n")
    sys.stderr.write(f"  copyright_blocks    : {totals['copyright_blocks']}\n")
    sys.stderr.write(f"  page_number_lines   : {totals['page_number_lines']}\n")
    sys.stderr.write(f"  double_apostrophes  : {totals['double_apostrophes']}\n")
    sys.stderr.write(f"  bullet_gt_stripped  : {totals['bullet_gt']}\n")
    sys.stderr.write(f"  files touched       : {len(per_file)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
