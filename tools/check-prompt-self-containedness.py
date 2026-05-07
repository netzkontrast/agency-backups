#!/usr/bin/env python3
"""
Self-Containedness linter (PROMPT.md §5.1 / §6.4 anchor).

Mechanizes Prompt Engineering Principle #1 ("Self-Containedness"): every
``/prompts/<slug>/prompt.md`` MUST be readable in isolation, with no
dependence on prior conversation history or out-of-band context. This
linter is the regex-tier compression of the LLM-mediated reader-test
audit specified in
``skills/research-prompt-optimizer/phases/phase4-reader-test.md``;
that Phase-4 audit remains the canonical deeper check.

Detection: any case-insensitive, word-boundary-anchored occurrence of
the eight canonical external-context phrases listed in
``EXTERNAL_CONTEXT_PHRASES`` (SPEC §3.1.2) is flagged.

False-positive suppression (SPEC §3.1.4):
  - Phrases inside the YAML frontmatter block are NOT diagnosed.
  - Phrases inside fenced code blocks (triple-backtick or triple-tilde
    fences) are NOT diagnosed.
  - Lines whose stripped content begins with ``>`` (Markdown blockquote,
    typically used for quoting bad examples in anti-pattern tables) are
    skipped (MAY-suppression rule).

Rewrite hint: when a phrase is flagged, rewrite the surrounding clause to
inline whatever context the prompt was implicitly referencing. See
``skills/research-prompt-optimizer/phases/phase4-reader-test.md`` Step 3
(Assumption sweep + Ambiguity sweep) for the canonical rewrite pattern.

Usage::

    python3 tools/check-prompt-self-containedness.py <prompt.md> [<prompt.md>...]

Exit codes:
    0 — every input file is free of external-context phrases.
    2 — one or more files emitted at least one WARN finding.
    1 — internal error (e.g., unreadable file).

Diagnostic shape (one line per violation, on stderr)::

    <path>:<line>:<col>: WARN[self-containedness]: external-context phrase '<phrase>'
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Allow ``from tools.fm._core import ...`` when invoked from any CWD.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.fm._core import split_frontmatter_and_body  # noqa: E402

EXTERNAL_CONTEXT_PHRASES: tuple[str, ...] = (
    "this conversation",
    "as discussed above",
    "the user mentioned",
    "see the previous message",
    "as we discussed",
    "in our previous",
    "you mentioned",
    "earlier you said",
)

_PHRASE_RE = re.compile(
    "|".join(rf"\b{re.escape(p)}\b" for p in EXTERNAL_CONTEXT_PHRASES),
    re.IGNORECASE,
)

_FENCE_RE = re.compile(r"^(\s*)(```|~~~)")


def _emit(path: Path, line: int, col: int, phrase: str) -> str:
    return (
        f"{path}:{line}:{col}: WARN[self-containedness]: "
        f"external-context phrase '{phrase}'"
    )


def _body_offset(text: str) -> tuple[str, int]:
    """Return (body, body_start_line_1based) — the body and the 1-indexed
    line number on which the body begins in the original `text`."""
    fm_block, body = split_frontmatter_and_body(text)
    if not fm_block:
        return body, 1
    # The body starts the line *after* the closing `---` fence.
    fm_lines = fm_block.count("\n")
    return body, fm_lines + 1


def _iter_scannable_lines(body: str) -> list[tuple[int, str]]:
    """Yield (1-based-body-line, line-text) for every body line that is
    NOT inside a fenced code block AND not a blockquote line. Fence lines
    themselves are also skipped."""
    out: list[tuple[int, str]] = []
    in_fence = False
    fence_marker: str | None = None
    for idx, line in enumerate(body.splitlines(), start=1):
        m = _FENCE_RE.match(line)
        if m:
            marker = m.group(2)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif fence_marker == marker:
                in_fence = False
                fence_marker = None
            continue
        if in_fence:
            continue
        if line.lstrip().startswith(">"):
            continue
        out.append((idx, line))
    return out


def check_file(path: Path) -> list[str]:
    """Return a list of formatted WARN diagnostics for one prompt.md.

    Raises OSError if `path` is unreadable; the caller turns that into a
    process-level exit code of 1.
    """
    text = path.read_text(encoding="utf-8")
    body, body_start_line = _body_offset(text)

    findings: list[str] = []
    for body_line_no, line in _iter_scannable_lines(body):
        for m in _PHRASE_RE.finditer(line):
            abs_line = body_start_line + body_line_no - 1
            col = m.start() + 1  # 1-indexed column
            findings.append(_emit(path, abs_line, col, m.group(0).lower()))
    return findings


def main(argv: list[str]) -> int:
    if not argv:
        print(
            "usage: check-prompt-self-containedness.py <prompt.md> [<prompt.md>...]",
            file=sys.stderr,
        )
        return 2

    total_warnings = 0
    files_with_warnings = 0
    for arg in argv:
        path = Path(arg)
        try:
            diags = check_file(path)
        except OSError as exc:
            print(f"{path}:1:1: ERROR: cannot read file ({exc})", file=sys.stderr)
            return 1
        if diags:
            files_with_warnings += 1
            total_warnings += len(diags)
            for d in diags:
                print(d, file=sys.stderr)

    if total_warnings:
        print(
            f"total: {total_warnings} warning(s) across "
            f"{files_with_warnings} file(s)",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
