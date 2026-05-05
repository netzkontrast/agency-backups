"""Tests for ontology-build.py (covers Gherkin NO.1.6)."""
from __future__ import annotations

import shutil
import subprocess


def _run(nav_dir, *args):
    return subprocess.run(
        ["python3", str(nav_dir / "ontology-build.py"), *args],
        capture_output=True,
        text=True,
    )


import pytest


@pytest.mark.gherkin("NO.1.6")
def test_check_only_canonical_no_drift(nav_dir):
    """NO.1.6 — skill prose stays human-readable.

    ontology-build.py --check-only verifies that the merge of per-term
    frontmatter blocks produces a byte-identical ontology.json. Drift here
    would mean the per-term blocks were accidentally mutated (e.g., prose
    edits that touched the YAML, or a script regression).
    """
    r = _run(nav_dir, "--check-only")
    assert r.returncode == 0, f"drift detected on canonical tree: {r.stdout}\n{r.stderr}"


def test_drift_detection(nav_dir, repo_root, tmp_path):
    """When the ontology file diverges from a fresh build, --check-only exits 1."""
    canonical = repo_root / "maintenance" / "schemas" / "narrative-ontology" / "ontology.json"
    drifted = tmp_path / "ontology.json"
    # Write a deliberately empty stub
    drifted.write_text(
        '{"schema_version": "1.0", "ontology_version": "0.0", "created": "2026-01-01", "entries": []}'
    )
    r = _run(nav_dir, "--check-only", "--output", str(drifted))
    # Non-zero because the drifted file is empty but the merge would re-fill it
    assert r.returncode != 0


def test_help_text_mentions_check_only(nav_dir):
    r = _run(nav_dir, "--help")
    assert r.returncode == 0
    assert "--check-only" in r.stdout
    assert "--from-scratch" in r.stdout
