"""Fidelity scoring — anchor ADR.A.3.4."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools") not in sys.path:
    sys.path.insert(0, str(REPO / "tools"))

from adr import compress as adr_compress  # noqa: E402
from adr import corpus as adr_corpus  # noqa: E402
from adr import extract as adr_extract  # noqa: E402
from adr import fidelity as adr_fidelity  # noqa: E402
from adr import graph as adr_graph  # noqa: E402


def test_bcp14_score_is_one_on_self_compression(make_adr, tmp_decisions_root):
    make_adr("ADR-0001", slug="0001-a")
    make_adr("ADR-0002", slug="0002-b")
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    g = adr_graph.build_graph(corpus)
    norms = adr_extract.extract_normatives(corpus, graph=g)
    section = adr_compress.compress(norms, token_limit=2000)
    s = adr_fidelity.score(corpus, section, mode="bcp14-keyword", graph=g)
    assert s == pytest.approx(1.0)


def test_anchor_score_is_one_when_all_cited(make_adr, tmp_decisions_root):
    body_a = (
        "## Context and Problem Statement\nctx-a\n\n"
        "## Decision Drivers\n- d\n\n"
        "## Considered Options\n- a\n- b\n\n"
        "## Decision Outcome\nThe pipeline MUST honour rule alpha.\n\n"
        "## Consequences\n- Positive: alpha-rule MUST stay live.\n"
    )
    body_b = (
        "## Context and Problem Statement\nctx-b\n\n"
        "## Decision Drivers\n- d\n\n"
        "## Considered Options\n- a\n- b\n\n"
        "## Decision Outcome\nThe pipeline MUST honour rule beta.\n\n"
        "## Consequences\n- Positive: beta-rule MUST stay live.\n"
    )
    make_adr("ADR-0001", slug="0001-a", body=body_a)
    make_adr("ADR-0002", slug="0002-b", body=body_b)
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    g = adr_graph.build_graph(corpus)
    norms = adr_extract.extract_normatives(corpus, graph=g)
    section = adr_compress.compress(norms, token_limit=2000)
    s = adr_fidelity.score(corpus, section, mode="adr-id-anchor", graph=g)
    assert s == pytest.approx(1.0)


def test_llm_pass_mode_is_deferred(make_adr, tmp_decisions_root):
    make_adr("ADR-0001", slug="0001-a")
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    g = adr_graph.build_graph(corpus)
    norms = adr_extract.extract_normatives(corpus, graph=g)
    section = adr_compress.compress(norms, token_limit=2000)
    with pytest.raises(NotImplementedError):
        adr_fidelity.score(corpus, section, mode="llm-pass", graph=g)


def test_unknown_mode_raises(make_adr, tmp_decisions_root):
    make_adr("ADR-0001", slug="0001-a")
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    g = adr_graph.build_graph(corpus)
    norms = adr_extract.extract_normatives(corpus, graph=g)
    section = adr_compress.compress(norms, token_limit=2000)
    with pytest.raises(ValueError):
        adr_fidelity.score(corpus, section, mode="bogus")
