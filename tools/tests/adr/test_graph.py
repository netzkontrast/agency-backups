"""Supersession graph — anchors ADR.A.4.2/4.3/4.5/4.6, ADR.A.5.7."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO / "tools") not in sys.path:
    sys.path.insert(0, str(REPO / "tools"))

from adr import corpus as adr_corpus  # noqa: E402
from adr import graph as adr_graph  # noqa: E402


def test_adr_a_4_5_three_node_cycle(make_adr, tmp_decisions_root):
    # 0001 -> 0002 -> 0003 -> 0001 — pure cycle.
    make_adr("ADR-0001", slug="0001-a", supersedes=["ADR-0002"], superseded_by=["ADR-0003"])
    make_adr("ADR-0002", slug="0002-b", supersedes=["ADR-0003"], superseded_by=["ADR-0001"])
    make_adr("ADR-0003", slug="0003-c", supersedes=["ADR-0001"], superseded_by=["ADR-0002"])
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    g = adr_graph.build_graph(corpus)
    cycles = adr_graph.detect_cycles(g)
    assert cycles, "expected at least one cycle"
    diags = adr_graph.check_cycles(g)
    assert any(d.code == "ADR.A.4.5" for d in diags)


def test_acyclic_graph_passes(make_adr, tmp_decisions_root):
    make_adr("ADR-0001", slug="0001-a", status="Superseded",
             superseded_by=["ADR-0002"])
    make_adr("ADR-0002", slug="0002-b", supersedes=["ADR-0001"])
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    g = adr_graph.build_graph(corpus)
    assert adr_graph.detect_cycles(g) == []
    assert adr_graph.check_cycles(g) == []


def test_adr_a_4_6_missing_reciprocal(make_adr, tmp_decisions_root):
    make_adr("ADR-0017", slug="0017-old", status="Accepted")
    make_adr("ADR-0042", slug="0042-new", supersedes=["ADR-0017"])
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    g = adr_graph.build_graph(corpus)
    diags = adr_graph.check_reciprocity(g)
    assert any(d.code == "ADR.A.4.6" and "ADR-0017" in d.path or "0017-old" in d.path
               for d in diags)


def test_adr_a_4_6_clean_when_reciprocal(make_adr, tmp_decisions_root):
    make_adr("ADR-0017", slug="0017-old", status="Superseded",
             superseded_by=["ADR-0042"])
    make_adr("ADR-0042", slug="0042-new", supersedes=["ADR-0017"])
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    g = adr_graph.build_graph(corpus)
    assert adr_graph.check_reciprocity(g) == []


def test_adr_a_5_7_orphan_reference(make_adr, tmp_decisions_root):
    make_adr("ADR-0042", slug="0042-new", supersedes=["ADR-9999"])
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    g = adr_graph.build_graph(corpus)
    diags = adr_graph.check_orphans(g)
    assert any(d.code == "ADR.A.5.7" for d in diags)


def test_live_ids_filter(make_adr, tmp_decisions_root):
    make_adr("ADR-0001", slug="0001-a", status="Superseded",
             superseded_by=["ADR-0002"])
    make_adr("ADR-0002", slug="0002-b", supersedes=["ADR-0001"])
    make_adr("ADR-0003", slug="0003-c", status="Proposed")
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    g = adr_graph.build_graph(corpus)
    assert g.live_ids == frozenset({"ADR-0002"})
