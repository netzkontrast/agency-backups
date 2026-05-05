"""End-to-end CLI tests for nav.py (subprocess; covers all 7 subcommands).

Covers Gherkin acceptance scenarios NO.1.1, NO.1.2, NO.1.3, NO.1.7.
"""
from __future__ import annotations

import json
import subprocess

import pytest


def _run(nav_dir, *args):
    return subprocess.run(
        ["python3", str(nav_dir / "nav.py"), *args],
        capture_output=True,
        text=True,
    )


def _parse_json(stdout: str):
    return json.loads(stdout)


def test_by_id_returns_record(nav_dir):
    r = _run(nav_dir, "by-id", "el.trust")
    assert r.returncode == 0
    data = _parse_json(r.stdout)
    assert data["id"] == "el.trust"
    assert data["kind"] == "element"
    assert data["canonical_label"] == "Trust"


@pytest.mark.gherkin("NO.1.1")
def test_by_id_include_pairs_attaches_dp(nav_dir):
    """NO.1.1 — by-id with --include-pairs returns dynamic_pair_id partner + dp.* entry."""
    r = _run(nav_dir, "by-id", "el.trust", "--include-pairs")
    assert r.returncode == 0
    data = _parse_json(r.stdout)
    assert data["id"] == "el.trust"
    assert data.get("dynamic_pair_id") == "el.test"
    # The dp.* entries containing el.trust as a pair_member must be inlined
    assert "dynamic_pairs" in data
    assert len(data["dynamic_pairs"]) >= 1
    for dp in data["dynamic_pairs"]:
        assert dp["kind"] == "dynamic-pair"
        assert "el.trust" in (dp["pair_member_a"], dp["pair_member_b"])


@pytest.mark.gherkin("NO.1.2")
def test_by_alias_locale_en(nav_dir):
    """NO.1.2 — by-alias resolves through a locale alias.

    The canonical v0.1 ontology has aliases_en populated but aliases_de minimal.
    Test the locale flag mechanism with the en alias 'IC' which resolves to
    throughline.influence (per OQ resolution: Impact Character is an alias for
    the canonical NCP label 'Influence Character').
    """
    r = _run(nav_dir, "by-alias", "IC", "--lang", "en")
    assert r.returncode == 0
    data = _parse_json(r.stdout)
    assert data["id"] == "throughline.influence"
    assert data["canonical_label"] == "Influence Character"


@pytest.mark.gherkin("NO.1.3")
def test_by_scenario_kind_filter(nav_dir):
    """NO.1.3 — by-scenario --kind element returns array filtered to kind=element."""
    r = _run(nav_dir, "by-scenario", "novel.crucial-element-audit", "--kind", "element")
    assert r.returncode == 0
    data = _parse_json(r.stdout)
    assert isinstance(data, list)
    assert len(data) >= 5
    for entry in data:
        assert entry["kind"] == "element"
        assert "novel.crucial-element-audit" in entry.get("scenarios", [])


def test_by_quad_returns_4_members(nav_dir):
    r = _run(nav_dir, "by-quad", "quad.logic-feeling-el")
    assert r.returncode == 0
    data = _parse_json(r.stdout)
    assert isinstance(data, list)
    assert len(data) == 4


def test_by_ktad_returns_array(nav_dir):
    r = _run(nav_dir, "by-ktad", "K")
    assert r.returncode == 0
    data = _parse_json(r.stdout)
    assert isinstance(data, list)
    assert len(data) >= 4
    for entry in data:
        assert entry.get("ktad_position") == "K"


def test_by_ncp_throughline(nav_dir):
    r = _run(nav_dir, "by-ncp", "Relationship Story")
    assert r.returncode == 0
    data = _parse_json(r.stdout)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == "throughline.relationship"


def test_by_pair_returns_dp_entries(nav_dir):
    r = _run(nav_dir, "by-pair", "el.trust")
    assert r.returncode == 0
    data = _parse_json(r.stdout)
    assert isinstance(data, list)
    assert len(data) >= 1
    for entry in data:
        assert entry["kind"] == "dynamic-pair"


@pytest.mark.gherkin("NO.1.7")
def test_by_id_output_under_2kb(nav_dir):
    """NO.1.7 — navigator surface size invariant: a single-record query is < 2 KB.

    This is the navigator's token-economy claim in test form. The full
    benchmark across 10 queries is Plan Step 12.
    """
    r = _run(nav_dir, "by-id", "el.trust")
    assert r.returncode == 0
    size = len(r.stdout.encode("utf-8"))
    assert size < 2000, f"single-record output exceeded 2 KB: {size}"
