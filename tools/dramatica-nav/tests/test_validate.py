"""Subprocess tests for validate.py — 5 PASS on canonical + 5 FAIL on broken fixtures.

Covers Gherkin acceptance scenarios NO.1.4 + NO.1.5.
"""
from __future__ import annotations

import json
import subprocess

import pytest


def _run(nav_dir, *args):
    return subprocess.run(
        ["python3", str(nav_dir / "validate.py"), *args],
        capture_output=True,
        text=True,
    )


# ---------- 5 PASS tests on canonical tree ----------


def test_canonical_schema_passes(nav_dir):
    """validate.py exits 0 on the canonical ontology (no schema errors)."""
    r = _run(nav_dir, "--json")
    data = json.loads(r.stdout)
    assert data["summary"]["by_check"]["schema"] == 0


def test_canonical_reciprocity_passes(nav_dir):
    r = _run(nav_dir, "--json")
    data = json.loads(r.stdout)
    assert data["summary"]["by_check"]["reciprocity"] == 0


def test_canonical_pair_member_resolves(nav_dir):
    r = _run(nav_dir, "--json")
    data = json.loads(r.stdout)
    assert data["summary"]["by_check"]["pair_member"] == 0


def test_canonical_alias_uniqueness(nav_dir):
    r = _run(nav_dir, "--json")
    data = json.loads(r.stdout)
    assert data["summary"]["by_check"]["alias-uniqueness"] == 0


def test_canonical_ncp_enum_closure(nav_dir):
    """All ncp_appreciation values resolve to a known NCP enum surface."""
    r = _run(nav_dir, "--json")
    data = json.loads(r.stdout)
    assert data["summary"]["by_check"]["ncp-enum"] == 0


def test_canonical_exit_zero(nav_dir):
    """Default mode exits 0 on the canonical tree (warnings don't block)."""
    r = _run(nav_dir)
    assert r.returncode == 0


# ---------- 5 FAIL tests on broken fixtures ----------


def test_schema_failure_exits_nonzero(nav_dir, fixtures_dir):
    r = _run(nav_dir, "--ontology", str(fixtures_dir / "ontology_schema_fail.json"))
    assert r.returncode != 0


@pytest.mark.gherkin("NO.1.5")
def test_reciprocity_violation_exits_nonzero(nav_dir, fixtures_dir):
    """NO.1.5 — pre-commit gate catches reciprocity drift."""
    r = _run(
        nav_dir,
        "--json",
        "--ontology",
        str(fixtures_dir / "ontology_reciprocity_fail.json"),
    )
    assert r.returncode != 0
    data = json.loads(r.stdout)
    assert data["summary"]["by_check"]["reciprocity"] >= 1


def test_pair_member_unresolved_exits_nonzero(nav_dir, fixtures_dir):
    r = _run(
        nav_dir,
        "--json",
        "--ontology",
        str(fixtures_dir / "ontology_pair_member_fail.json"),
    )
    assert r.returncode != 0
    data = json.loads(r.stdout)
    assert data["summary"]["by_check"]["pair_member"] >= 1


def test_alias_dup_exits_nonzero(nav_dir, fixtures_dir):
    r = _run(
        nav_dir,
        "--json",
        "--ontology",
        str(fixtures_dir / "ontology_alias_dup.json"),
    )
    assert r.returncode != 0
    data = json.loads(r.stdout)
    assert data["summary"]["by_check"]["alias-uniqueness"] >= 1


@pytest.mark.gherkin("NO.1.4")
def test_ncp_enum_failure_exits_nonzero(nav_dir, fixtures_dir):
    """NO.1.4 — validate.py exits non-zero when ontology has bad ncp_appreciation."""
    r = _run(
        nav_dir,
        "--json",
        "--ontology",
        str(fixtures_dir / "ontology_ncp_bad.json"),
    )
    assert r.returncode != 0
    data = json.loads(r.stdout)
    assert data["summary"]["by_check"]["ncp-enum"] >= 1
