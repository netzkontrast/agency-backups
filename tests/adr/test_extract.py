"""Normative extraction — anchor ADR.A.3.1."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools") not in sys.path:
    sys.path.insert(0, str(REPO / "tools"))

from adr import corpus as adr_corpus  # noqa: E402
from adr import extract as adr_extract  # noqa: E402
from adr import graph as adr_graph  # noqa: E402


def test_adr_a_3_1_only_accepted_contributes(make_adr, tmp_decisions_root):
    make_adr("ADR-0001", slug="0001-accepted", status="Accepted")
    make_adr("ADR-0002", slug="0002-proposed", status="Proposed")
    make_adr("ADR-0003", slug="0003-superseded", status="Superseded",
             superseded_by=["ADR-0001"])
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    g = adr_graph.build_graph(corpus)
    norms = adr_extract.extract_normatives(corpus, graph=g)
    sources = {n.adr_id for n in norms}
    assert sources == {"ADR-0001"}


def test_adr_a_3_1_picks_up_decision_outcome_and_consequences(make_adr, tmp_decisions_root):
    make_adr("ADR-0001", slug="0001-x")
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    g = adr_graph.build_graph(corpus)
    norms = adr_extract.extract_normatives(corpus, graph=g)
    keywords = {n.keyword for n in norms}
    # Default body uses MUST in Decision Outcome and MUST/SHOULD in Consequences.
    assert "MUST" in keywords
    assert any(n.consequence_kind == "positive" for n in norms)
    assert any(n.consequence_kind == "negative" for n in norms)


def test_supersession_chain_excludes_predecessor(make_adr, tmp_decisions_root):
    body_old = (
        "## Context and Problem Statement\nold\n\n"
        "## Decision Drivers\n- d\n\n"
        "## Considered Options\n- a\n- b\n\n"
        "## Decision Outcome\nThe pipeline MUST honour OLD-RULE.\n\n"
        "## Consequences\n- Negative: agents MAY drift.\n"
    )
    body_new = (
        "## Context and Problem Statement\nnew\n\n"
        "## Decision Drivers\n- d\n\n"
        "## Considered Options\n- a\n- b\n\n"
        "## Decision Outcome\nThe pipeline MUST honour NEW-RULE.\n\n"
        "## Consequences\n- Positive: behaviour MUST be uniform.\n"
    )
    make_adr("ADR-0001", slug="0001-old", status="Superseded",
             superseded_by=["ADR-0002"], body=body_old)
    make_adr("ADR-0002", slug="0002-new", status="Accepted",
             supersedes=["ADR-0001"], body=body_new)
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    g = adr_graph.build_graph(corpus)
    norms = adr_extract.extract_normatives(corpus, graph=g)
    sentences = " ".join(n.sentence for n in norms)
    assert "NEW-RULE" in sentences
    assert "OLD-RULE" not in sentences
