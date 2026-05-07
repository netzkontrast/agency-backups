"""Tests for tools/check-prompt-framework-declaration.py (Task 034 ST-3).

Mechanizes PROMPT.md §5.2 (Framework Declaration) — verifies the WARN-tier
linter detects every documented violation and exits cleanly on conformant
prompts.
"""
from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "tools" / "check-prompt-framework-declaration.py"


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


# --- Fixtures: well-formed prompts -------------------------------------------

_VALID_BODY = """\
---
type: prompt
status: active
slug: demo
prompt_kind: task-spec
prompt_framework: RISEN
---

# Demo Prompt

## Framework

RISEN. Selected because the deliverable is a structured one-shot output and
the agent does not need iterative reflection beyond the prescribed steps.

## R - Role

You are an agent.
"""


def test_valid_prompt_passes(tmp_path: Path) -> None:
    p = _write(tmp_path, "prompt.md", _VALID_BODY)
    result = _run(p)
    assert result.returncode == 0, result.stderr


def test_compound_framework_passes(tmp_path: Path) -> None:
    body = _VALID_BODY.replace(
        "prompt_framework: RISEN", "prompt_framework: RISEN+ReAct"
    ).replace(
        "RISEN. Selected", "RISEN+ReAct. Selected"
    )
    p = _write(tmp_path, "prompt.md", body)
    result = _run(p)
    assert result.returncode == 0, result.stderr


def test_compound_framework_with_spacing_passes(tmp_path: Path) -> None:
    """`RISEN+ReAct` frontmatter MUST also accept `RISEN + ReAct` body text."""
    body = _VALID_BODY.replace(
        "prompt_framework: RISEN", "prompt_framework: RISEN+ReAct"
    ).replace(
        "RISEN. Selected because the deliverable",
        "RISEN + ReAct. Selected because the deliverable",
    )
    p = _write(tmp_path, "prompt.md", body)
    result = _run(p)
    assert result.returncode == 0, result.stderr


# --- Fixtures: each violation in isolation -----------------------------------


def test_missing_frontmatter_key(tmp_path: Path) -> None:
    body = _VALID_BODY.replace("prompt_framework: RISEN\n", "")
    p = _write(tmp_path, "prompt.md", body)
    result = _run(p)
    assert result.returncode == 2
    assert "framework-missing-frontmatter" in result.stderr


def test_non_canonical_framework(tmp_path: Path) -> None:
    body = _VALID_BODY.replace("prompt_framework: RISEN", "prompt_framework: XYZ")
    p = _write(tmp_path, "prompt.md", body)
    result = _run(p)
    assert result.returncode == 2
    assert "framework-non-canonical" in result.stderr


def test_missing_framework_section(tmp_path: Path) -> None:
    body = _VALID_BODY.replace(
        "## Framework\n\nRISEN. Selected because the deliverable is a structured "
        "one-shot output and\nthe agent does not need iterative reflection beyond "
        "the prescribed steps.\n\n",
        "",
    )
    p = _write(tmp_path, "prompt.md", body)
    result = _run(p)
    assert result.returncode == 2
    assert "framework-missing-section" in result.stderr


def test_framework_mismatch(tmp_path: Path) -> None:
    """Frontmatter says RISEN but the body section claims ReAct."""
    body = _VALID_BODY.replace(
        "RISEN. Selected because the deliverable is a structured one-shot output and\n"
        "the agent does not need iterative reflection beyond the prescribed steps.",
        "ReAct. Selected because the agent must iteratively reason and act on "
        "tool feedback before producing the final answer.",
    )
    p = _write(tmp_path, "prompt.md", body)
    result = _run(p)
    assert result.returncode == 2
    assert "framework-mismatch" in result.stderr


def test_no_rationale(tmp_path: Path) -> None:
    """Section heading present but body is too short."""
    body = _VALID_BODY.replace(
        "RISEN. Selected because the deliverable is a structured one-shot output and\n"
        "the agent does not need iterative reflection beyond the prescribed steps.",
        "RISEN only here.",
    )
    p = _write(tmp_path, "prompt.md", body)
    result = _run(p)
    assert result.returncode == 2
    assert "framework-no-rationale" in result.stderr


# --- Multi-file dispatch -----------------------------------------------------


def test_multi_file_one_violator_exits_two(tmp_path: Path) -> None:
    good = _write(tmp_path, "good.md", _VALID_BODY)
    bad_body = _VALID_BODY.replace("prompt_framework: RISEN", "prompt_framework: XYZ")
    bad = _write(tmp_path, "bad.md", bad_body)
    result = _run(good, bad)
    assert result.returncode == 2
    assert str(bad) in result.stderr
    assert str(good) not in result.stderr


# --- Sanity -------------------------------------------------------------------


def test_no_args_exits_two(tmp_path: Path) -> None:
    result = _run()  # no paths
    assert result.returncode == 2
    assert "usage" in result.stderr.lower()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(pytest.main([__file__, "-v"]))
