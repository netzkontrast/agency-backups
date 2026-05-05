"""Subprocess tests for extract.py (CLI exit codes + output shape)."""
from __future__ import annotations

import subprocess

import pytest


def _run(nav_dir, *args):
    return subprocess.run(
        ["python3", str(nav_dir / "extract.py"), *args],
        capture_output=True,
        text=True,
    )


def test_extract_by_id_strips_yaml(nav_dir):
    """Default mode strips the embedded nav-ontology block from prose output."""
    r = _run(nav_dir, "el.trust")
    assert r.returncode == 0
    # YAML block marker must NOT appear in output
    assert "nav-ontology" not in r.stdout
    assert "```yaml" not in r.stdout
    # But the term heading should
    assert "## Trust" in r.stdout


def test_extract_no_strip_yaml(nav_dir):
    """`--no-strip-yaml` preserves the embedded block."""
    r = _run(nav_dir, "el.trust", "--no-strip-yaml")
    assert r.returncode == 0
    assert "nav-ontology" in r.stdout


def test_extract_bad_id_exits_4(nav_dir):
    r = _run(nav_dir, "el.nonexistent")
    assert r.returncode == 4
    assert "unknown" in r.stderr.lower() or "not found" in r.stderr.lower()


def test_extract_prose_under_5kb(nav_dir):
    """Per the navigator's token-economy invariant, a typical Element entry's
    extracted prose is small. el.trust is a representative term."""
    r = _run(nav_dir, "el.trust")
    assert r.returncode == 0
    assert len(r.stdout.encode("utf-8")) < 5000, (
        f"prose extract exceeded 5 KB: got {len(r.stdout.encode())}"
    )
