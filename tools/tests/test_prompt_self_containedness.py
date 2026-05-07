"""Tests for tools/check-prompt-self-containedness.py (Task 034 ST-2).

Mechanizes PROMPT.md §5.1 (Self-Containedness) — verifies the WARN-tier
linter flags every canonical external-context phrase, suppresses
frontmatter / fenced-code / blockquote occurrences, and exits cleanly
on conformant prompts.
"""
from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "tools" / "check-prompt-self-containedness.py"

CANONICAL_PHRASES = (
    "this conversation",
    "as discussed above",
    "the user mentioned",
    "see the previous message",
    "as we discussed",
    "in our previous",
    "you mentioned",
    "earlier you said",
)


def _run(*paths: Path) -> subprocess.CompletedProcess[str]:
    """Invoke the linter with the supplied prompt paths."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), *(str(p) for p in paths)],
        capture_output=True,
        text=True,
        cwd=REPO,
    )


def _write(tmp_path: Path, name: str, body: str) -> Path:
    """Write a synthetic prompt.md fixture under tmp_path."""
    p = tmp_path / name
    p.write_text(textwrap.dedent(body).lstrip(), encoding="utf-8")
    return p


# --- Fixtures ----------------------------------------------------------------

_CLEAN_BODY = """\
---
type: prompt
status: active
slug: demo
prompt_kind: task-spec
prompt_framework: RISEN
---

# Demo Prompt

## Framework

RISEN. Selected because the deliverable is a structured one-shot output.

## R - Role

You are an agent that produces well-formed Markdown.
"""


# --- Clean / pass cases ------------------------------------------------------


def test_clean_prompt_passes(tmp_path: Path) -> None:
    p = _write(tmp_path, "prompt.md", _CLEAN_BODY)
    result = _run(p)
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


# --- One test per canonical phrase ------------------------------------------


@pytest.mark.parametrize("phrase", CANONICAL_PHRASES)
def test_each_canonical_phrase_is_flagged(tmp_path: Path, phrase: str) -> None:
    body = _CLEAN_BODY.replace(
        "You are an agent that produces well-formed Markdown.",
        f"You are an agent that produces well-formed Markdown {phrase} here.",
    )
    p = _write(tmp_path, "prompt.md", body)
    result = _run(p)
    assert result.returncode == 2, result.stderr
    assert f"external-context phrase '{phrase}'" in result.stderr
    # Verify the line/col triple shape is `<path>:<line>:<col>:`.
    first_diag = result.stderr.splitlines()[0]
    head, _, _ = first_diag.partition(": WARN[self-containedness]")
    parts = head.rsplit(":", 2)
    assert len(parts) == 3
    line_no, col_no = int(parts[1]), int(parts[2])
    assert line_no >= 1 and col_no >= 1


# --- Suppression rules -------------------------------------------------------


def test_phrase_in_frontmatter_is_suppressed(tmp_path: Path) -> None:
    body = """\
    ---
    type: prompt
    status: active
    slug: demo
    summary: this conversation should not be flagged here
    prompt_kind: task-spec
    prompt_framework: RISEN
    ---

    # Demo Prompt

    ## Framework

    RISEN. Selected because the deliverable is a structured one-shot output.
    """
    p = _write(tmp_path, "prompt.md", body)
    result = _run(p)
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_phrase_in_fenced_code_block_is_suppressed(tmp_path: Path) -> None:
    body = _CLEAN_BODY + textwrap.dedent("""
        ## Example

        ```text
        the user mentioned this conversation earlier you said hi
        ```
        """)
    p = _write(tmp_path, "prompt.md", body)
    result = _run(p)
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_phrase_on_blockquote_line_is_suppressed(tmp_path: Path) -> None:
    body = _CLEAN_BODY + textwrap.dedent("""
        ## Anti-Pattern

        > the user mentioned the requirement earlier (this is a quoted bad example)

        Inline rationale follows.
        """)
    p = _write(tmp_path, "prompt.md", body)
    result = _run(p)
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


# --- Case-insensitivity ------------------------------------------------------


def test_uppercase_phrase_is_flagged(tmp_path: Path) -> None:
    body = _CLEAN_BODY.replace(
        "You are an agent that produces well-formed Markdown.",
        "You are an agent. AS DISCUSSED ABOVE, the schema is fixed.",
    )
    p = _write(tmp_path, "prompt.md", body)
    result = _run(p)
    assert result.returncode == 2, result.stderr
    assert "external-context phrase 'as discussed above'" in result.stderr


# --- Multi-file dispatch -----------------------------------------------------


def test_multi_file_one_violator_exits_two(tmp_path: Path) -> None:
    good = _write(tmp_path, "good.md", _CLEAN_BODY)
    bad_body = _CLEAN_BODY.replace(
        "You are an agent that produces well-formed Markdown.",
        "You are an agent. As we discussed, the schema is fixed.",
    )
    bad = _write(tmp_path, "bad.md", bad_body)
    result = _run(good, bad)
    assert result.returncode == 2, result.stderr
    assert str(bad) in result.stderr
    assert str(good) not in result.stderr


def test_summary_line_emitted_on_warn(tmp_path: Path) -> None:
    bad_body = _CLEAN_BODY.replace(
        "You are an agent that produces well-formed Markdown.",
        "You are an agent. As we discussed, this conversation matters.",
    )
    p = _write(tmp_path, "prompt.md", bad_body)
    result = _run(p)
    assert result.returncode == 2, result.stderr
    # Two phrases on one line → two warnings across one file.
    summary_lines = [
        ln for ln in result.stderr.splitlines() if ln.startswith("total:")
    ]
    assert len(summary_lines) == 1
    assert "warning(s) across" in summary_lines[0]
    assert "1 file(s)" in summary_lines[0]


# --- Sanity ------------------------------------------------------------------


def test_no_args_exits_two(tmp_path: Path) -> None:
    result = _run()  # no paths
    assert result.returncode == 2
    assert "usage" in result.stderr.lower()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(pytest.main([__file__, "-v"]))
