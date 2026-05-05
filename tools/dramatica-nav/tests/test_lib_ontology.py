"""Unit tests for lib/ontology.OntologyIndex (one per lookup method)."""
from __future__ import annotations

import pytest

from lib import LookupNotFoundError


def test_by_id_resolves(canonical_index):
    e = canonical_index.by_id("el.trust")
    assert e["kind"] == "element"
    assert e["canonical_label"] == "Trust"
    assert e["dynamic_pair_id"] == "el.test"


def test_by_id_raises_on_missing(canonical_index):
    with pytest.raises(LookupNotFoundError):
        canonical_index.by_id("el.nonexistent")


def test_by_alias_en(canonical_index):
    # "IC" is a registered en alias for throughline.influence
    e = canonical_index.by_alias("IC", locale="en")
    assert e["id"] == "throughline.influence"


def test_by_scenario_with_kind_filter(canonical_index):
    elements = canonical_index.by_scenario("novel.crucial-element-audit", kind="element")
    assert len(elements) >= 5
    assert all(e["kind"] == "element" for e in elements)
    assert all("novel.crucial-element-audit" in e.get("scenarios", []) for e in elements)


def test_by_quad(canonical_index):
    members = canonical_index.by_quad("quad.logic-feeling-el")
    assert len(members) == 4, f"a clean Element Quad MUST have 4 members; got {len(members)}"
    positions = sorted(m.get("ktad_position") for m in members if m.get("ktad_position"))
    assert positions == ["A", "D", "K", "T"]


def test_by_ktad(canonical_index):
    k_entries = canonical_index.by_ktad("K")
    assert len(k_entries) >= 4
    assert all(e["ktad_position"] == "K" for e in k_entries)


def test_by_ncp_for_throughline(canonical_index):
    rs = canonical_index.by_ncp("Relationship Story")
    assert len(rs) == 1
    assert rs[0]["id"] == "throughline.relationship"


def test_by_pair_returns_dp_entries(canonical_index):
    pairs = canonical_index.by_pair("el.trust")
    assert len(pairs) >= 1
    assert all(e["kind"] == "dynamic-pair" for e in pairs)
    assert all("el.trust" in (e["pair_member_a"], e["pair_member_b"]) for e in pairs)


def test_pair_partner(canonical_index):
    partner = canonical_index.pair_partner("el.trust")
    assert partner is not None
    assert partner["id"] == "el.test"
    # Symmetry
    back = canonical_index.pair_partner("el.test")
    assert back is not None
    assert back["id"] == "el.trust"
