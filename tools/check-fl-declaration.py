#!/usr/bin/env python3
"""FL-declaration linter — Task 038 ST-2 / FRUSTRATED.md FR.B.4.

Validates that the canonical Frustration-Level declaration is present and
parseable for a closed-Task closure surface. Surfaces accepted:

  1. A *task folder* `tasks/<NNN>-<slug>/` whose `task.md` carries
     `task_status: done`. The linter looks for `friction-log.md` first,
     then for a `## Frustration Log` section in any `*.pr-body.md` file
     in the same folder (used in CI surfaces where the PR body is
     materialised next to the task).
  2. A *PR-body file* (any `.md` path that is not a task.md) — the linter
     scans for the `## Frustration Log` section and validates its content.
  3. A *research workspace* `research/<slug>/reflection/friction-log.md` —
     accepted with the same canonical line set as task closures.

The canonical line per FRUSTRATED.md is::

    Highest Frustration Level: FL[0-3]

The linter accepts the bounded variant set documented in
`research/fl0-value-justification/output/SPEC.md` §2.2 (10 forms) so
historical logs are not rejected pedantically.

Diagnostic format (per Task 028/031 prior art)::

    <relpath>::ERROR:FR.B.4:missing:<details>
    <relpath>::ERROR:FR.B.4:malformed:<details>

Exit codes:
  0 — all surfaces have a parseable FL declaration.
  1 — one or more diagnostics emitted.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# 10 accepted variant forms (corpus-derived; see research SPEC §2.2).
# Order matters only for documentation; matching is by alternation.
_FL_LINE_PATTERNS: tuple[re.Pattern[str], ...] = (
    # 1. canonical                           "Highest Frustration Level: FL2"
    re.compile(r"(?im)^\s*\*{0,2}\s*Highest\s+Frustration\s+Level\s*:\s*\*{0,2}\s*FL[0-3]\b"),
    # 2. bold-canonical                      "**Highest Frustration Level: FL2**"
    #    (covered by pattern 1's optional `**`)
    # 3. phrasing variant                    "**Highest friction level experienced: FL0**"
    re.compile(r"(?im)^\s*\*{0,2}\s*Highest\s+friction\s+level\s+experienced\s*:\s*\*{0,2}\s*FL[0-3]\b"),
    # 4. abbreviated phrasing                "**Highest FL experienced: FL0**"
    re.compile(r"(?im)^\s*\*{0,2}\s*Highest\s+FL\s+experienced\s*:\s*\*{0,2}\s*FL[0-3]\b"),
    # 5. bold-bare-prose                     "**FL0** — plan obsolesced cleanly"
    re.compile(r"(?im)^\s*\*\*FL[0-3]\*\*\s*[—\-:]"),
    # 6. list-form                           "- **Friction Level:** FL0 (...)"
    re.compile(r"(?im)^\s*[-*]\s*\*{0,2}\s*Friction\s+Level\s*:?\s*\*{0,2}\s*FL[0-3]\b"),
    # 7. bold-bare                           "**FL0**" (with prose on next line)
    re.compile(r"(?im)^\s*\*\*FL[0-3]\*\*\s*$"),
    # 8. bare-with-em-dash                   "FL0 - <prose>"
    re.compile(r"(?im)^\s*FL[0-3]\s*[—\-:]"),
    # 9. bare-on-own-line                    "FL0"
    re.compile(r"(?im)^\s*FL[0-3]\s*$"),
    # 11. "Highest Friction Level: FL1"      (Friction vs Frustration variant)
    re.compile(r"(?im)^\s*\*{0,2}\s*Highest\s+Friction\s+Level\s*:\s*\*{0,2}\s*FL[0-3]\b"),
    # 12. heading form                       "## Frustration Level: FL2"
    re.compile(r"(?im)^\s*##+\s*Frustration\s+Level\s*:\s*FL[0-3]\b"),
    # 13. bold short form                    "**Frustration Level: FL0**"
    re.compile(r"(?im)^\s*\*{0,2}\s*Frustration\s+Level\s*:\s*\*{0,2}\s*FL[0-3]\b"),
    # 14. "Highest FL reached this run: FL1" (research-side variant)
    re.compile(r"(?im)^\s*\*{0,2}\s*Highest\s+FL\s+reached\b[^.\n]*?:\s*\*{0,2}\s*FL[0-3]\b"),
    # 10. summary-frontmatter (WARN only — see _check_text)
)

# A laxer regex used to detect "log mentions an FL token at all" so we can
# distinguish missing (no FL token anywhere) from malformed (token present
# but not on a recognised declaration line).
_FL_TOKEN_RE = re.compile(r"\bFL[0-3]\b")

_FL_LOG_SECTION_HEAD_RE = re.compile(
    r"(?im)^\s*##+\s*Frustration\s+Log\s*$",
)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text
    return text[end + 5 :]


def _has_canonical_line(text: str) -> bool:
    body = _strip_frontmatter(text)
    return any(p.search(body) for p in _FL_LINE_PATTERNS)


def _frontmatter_only_fl(text: str) -> bool:
    """Detect logs that only declare FL via `summary: FL0` in frontmatter
    (variant 10 in SPEC §2.2). These trigger a `malformed` diagnostic, not
    `missing`, because the agent did make a declaration — just on the wrong
    surface.
    """
    if not text.startswith("---\n"):
        return False
    end = text.find("\n---\n", 4)
    if end == -1:
        return False
    fm = text[4:end]
    body = text[end + 5 :]
    if _FL_TOKEN_RE.search(fm) and not _FL_TOKEN_RE.search(body):
        return True
    return False


def _check_friction_log(path: Path, rel: Path) -> list[str]:
    text = _read_text(path)
    if not text.strip():
        return [f"{rel}::ERROR:FR.B.4:missing:friction-log.md is empty"]
    if _has_canonical_line(text):
        return []
    if _frontmatter_only_fl(text):
        return [
            f"{rel}::ERROR:FR.B.4:malformed:"
            f"FL declared only in frontmatter (`summary:` field); "
            f"body MUST carry a parseable declaration line "
            f"(see FRUSTRATED.md §FL.Log; canonical: "
            f"`Highest Frustration Level: FL[0-3]`)"
        ]
    if _FL_TOKEN_RE.search(_strip_frontmatter(text)):
        return [
            f"{rel}::ERROR:FR.B.4:malformed:"
            f"FL token present but not on a recognised declaration line; "
            f"see research/fl0-value-justification/output/SPEC.md §2.2 "
            f"for the accepted variant set"
        ]
    return [
        f"{rel}::ERROR:FR.B.4:missing:"
        f"no FL declaration found in friction-log.md "
        f"(canonical: `Highest Frustration Level: FL[0-3]`)"
    ]


def _check_pr_body(path: Path, rel: Path) -> list[str]:
    text = _read_text(path)
    if not text.strip():
        return [f"{rel}::ERROR:FR.B.4:missing:PR body is empty"]
    section_head = _FL_LOG_SECTION_HEAD_RE.search(text)
    if not section_head:
        return [
            f"{rel}::ERROR:FR.B.4:missing:"
            f"no `## Frustration Log` section in PR body "
            f"(FRUSTRATED.md §FL.Log.2)"
        ]
    section_body = text[section_head.end() :]
    next_h2 = re.search(r"(?im)^\s*##+\s+\S", section_body)
    if next_h2:
        section_body = section_body[: next_h2.start()]
    if _has_canonical_line(section_body):
        return []
    if _FL_TOKEN_RE.search(section_body):
        return [
            f"{rel}::ERROR:FR.B.4:malformed:"
            f"FL token in `## Frustration Log` but no recognised "
            f"declaration line (see SPEC §2.2 for accepted variants)"
        ]
    return [
        f"{rel}::ERROR:FR.B.4:missing:"
        f"`## Frustration Log` section has no FL[0-3] declaration"
    ]


def _check_task_folder(folder: Path) -> list[str]:
    rel = folder
    fl = folder / "friction-log.md"
    pr_body_candidates = sorted(folder.glob("*.pr-body.md"))
    if fl.exists():
        return _check_friction_log(fl, fl)
    if pr_body_candidates:
        return _check_pr_body(pr_body_candidates[0], pr_body_candidates[0])
    return [
        f"{rel}::ERROR:FR.B.4:missing:"
        f"task folder has neither friction-log.md nor a *.pr-body.md surface "
        f"(FRUSTRATED.md §FL.Log.1 / §FL.Log.2)"
    ]


def check_path(target: Path) -> list[str]:
    """Dispatch by surface type. Returns a list of diagnostic strings."""
    if target.is_dir():
        return _check_task_folder(target)
    name = target.name.lower()
    if name == "friction-log.md":
        return _check_friction_log(target, target)
    return _check_pr_body(target, target)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Validate FL[0-3] declarations on task closure surfaces "
            "(friction-log.md, PR body, research reflection)."
        ),
    )
    ap.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help=(
            "Task folder, friction-log.md, or PR-body file. "
            "Multiple targets supported; failure on any is suite failure."
        ),
    )
    args = ap.parse_args(argv)

    diagnostics: list[str] = []
    for target in args.paths:
        if not target.exists():
            diagnostics.append(
                f"{target}::ERROR:FR.B.4:missing:path does not exist"
            )
            continue
        diagnostics.extend(check_path(target))

    for line in diagnostics:
        print(line, file=sys.stderr)
    return 1 if diagnostics else 0


if __name__ == "__main__":
    sys.exit(main())
