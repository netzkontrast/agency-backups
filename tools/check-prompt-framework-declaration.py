#!/usr/bin/env python3
"""
Framework Declaration linter (PROMPT.md §5.2 / P.B.4 anchor).

Mechanizes Prompt Engineering Principle #2 ("Framework Declaration"): every
``/prompts/<slug>/prompt.md`` MUST declare its prompt-engineering framework
both in frontmatter (``prompt_framework``) AND in a top-level ``## Framework``
section, with the two declarations naming the same framework and the section
carrying at least one sentence of rationale.

Usage::

    python3 tools/check-prompt-framework-declaration.py <prompt.md> [<prompt.md>...]

Exit codes:
    0 — every input file passes all four checks.
    2 — one or more files emitted at least one WARN finding.
    1 — internal error (e.g., unreadable file).

Diagnostic shape (one line per violation, on stderr)::

    <path>:<line>: WARN: <rule-id>: <message>

Rule IDs: ``framework-missing-frontmatter``, ``framework-non-canonical``,
``framework-missing-section``, ``framework-mismatch``, ``framework-no-rationale``.

Canonical frameworks (PROMPT.md §3 frontmatter schema, §4.3 selection guide):
    RISEN | RISE-DX | ReAct | RISEN+ReAct | CoT
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Allow ``from tools.fm._core import ...`` when invoked from the repo root.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

try:
    from tools.fm._core import (  # noqa: E402  (sys.path manipulation above)
        find_all_section_bodies,
        parse_frontmatter,
        split_frontmatter_and_body,
    )
except ImportError:
    print(
        "check-prompt-framework-declaration: tools/fm/_core.py not importable "
        "(skipping — advisory linter, exit 0). Install/repair the fm "
        "toolchain to re-enable the WARN gate.",
        file=sys.stderr,
    )
    raise SystemExit(0)

CANONICAL_FRAMEWORKS = ("RISEN", "RISE-DX", "ReAct", "RISEN+ReAct", "CoT")
SECTION_HEADING = "Framework"
MIN_RATIONALE_WORDS = 10


def _emit(path: Path, line: int, rule: str, message: str) -> str:
    return f"{path}:{line}: WARN: {rule}: {message}"


def _frontmatter_line(text: str, key: str) -> int:
    """Return the 1-based line number of the `key:` row in the YAML
    frontmatter, or line 1 if the key is absent (best-effort anchor)."""
    pat = re.compile(rf"^\s*{re.escape(key)}\s*:", re.MULTILINE)
    m = pat.search(text)
    if not m:
        return 1
    return text.count("\n", 0, m.start()) + 1


def _heading_line(text: str, heading: str) -> int:
    """Return the 1-based line of the first ``## heading`` match, or 1."""
    fm_block, _ = split_frontmatter_and_body(text)
    fm_lines = fm_block.count("\n")
    pat = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.IGNORECASE | re.MULTILINE)
    m = pat.search(text)
    if not m:
        return max(fm_lines, 1)
    return text.count("\n", 0, m.start()) + 1


def _section_mentions_framework(section_body: str, framework: str) -> bool:
    """True iff `section_body` references the same framework value the
    frontmatter declared. Case-insensitive substring match. The compound
    ``RISEN+ReAct`` also matches when the section spells it ``RISEN + ReAct``
    or names both component frameworks separately."""
    body_lc = section_body.lower()
    if framework.lower() in body_lc:
        return True
    # Accept whitespace around the '+' for the compound form.
    if "+" in framework:
        spaced = re.sub(r"\s*\+\s*", r"\\s*\\+\\s*", re.escape(framework))
        if re.search(spaced, section_body, re.IGNORECASE):
            return True
        # Accept both component names appearing independently.
        parts = [p.strip().lower() for p in framework.split("+") if p.strip()]
        if parts and all(p in body_lc for p in parts):
            return True
    return False


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w\-]+\b", text))


def check_file(path: Path) -> list[str]:
    """Return a list of formatted WARN diagnostics for one prompt.md.

    Raises OSError if `path` is unreadable; the caller turns that into a
    process-level exit code of 1 (internal error), matching the
    ``check-prompt-self-containedness.py`` convention.
    """
    findings: list[str] = []
    text = path.read_text(encoding="utf-8")

    fm = parse_frontmatter(text, strict=False)
    framework = fm.get("prompt_framework", "")
    if not isinstance(framework, str):
        framework = ""
    framework = framework.strip()

    if not framework:
        findings.append(_emit(
            path, _frontmatter_line(text, "prompt_framework"),
            "framework-missing-frontmatter",
            "frontmatter key 'prompt_framework' is missing or empty",
        ))
    elif framework not in CANONICAL_FRAMEWORKS:
        findings.append(_emit(
            path, _frontmatter_line(text, "prompt_framework"),
            "framework-non-canonical",
            f"prompt_framework={framework!r} is not in canonical set "
            f"{list(CANONICAL_FRAMEWORKS)}",
        ))

    section_bodies = find_all_section_bodies(text, SECTION_HEADING)
    if not section_bodies:
        findings.append(_emit(
            path, _heading_line(text, SECTION_HEADING),
            "framework-missing-section",
            f"no top-level '## {SECTION_HEADING}' section found in body",
        ))
        return findings  # downstream checks assume the section exists

    section_body = section_bodies[0]

    if framework and framework in CANONICAL_FRAMEWORKS:
        if not _section_mentions_framework(section_body, framework):
            findings.append(_emit(
                path, _heading_line(text, SECTION_HEADING),
                "framework-mismatch",
                f"'## {SECTION_HEADING}' body does not mention frontmatter "
                f"framework {framework!r}",
            ))

    if _word_count(section_body) < MIN_RATIONALE_WORDS:
        findings.append(_emit(
            path, _heading_line(text, SECTION_HEADING),
            "framework-no-rationale",
            f"'## {SECTION_HEADING}' section has fewer than "
            f"{MIN_RATIONALE_WORDS} words of rationale",
        ))

    return findings


def main(argv: list[str]) -> int:
    if not argv:
        print(
            "usage: check-prompt-framework-declaration.py <prompt.md> [<prompt.md>...]",
            file=sys.stderr,
        )
        return 2

    any_violation = False
    for arg in argv:
        path = Path(arg)
        try:
            diags = check_file(path)
        except OSError as exc:
            print(f"{path}:1: ERROR: cannot read file ({exc})", file=sys.stderr)
            return 1
        for diag in diags:
            print(diag, file=sys.stderr)
            any_violation = True
    return 2 if any_violation else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
