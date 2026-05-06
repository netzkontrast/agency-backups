"""Compression — anchors ADR.A.3.2, ADR.A.3.3."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools") not in sys.path:
    sys.path.insert(0, str(REPO / "tools"))

from adr import compress as adr_compress  # noqa: E402
from adr.extract import Normative  # noqa: E402


def _norm(adr_id: str, keyword: str, sentence: str, kind: str | None = None) -> Normative:
    return Normative(adr_id=adr_id, keyword=keyword, sentence=sentence,
                     consequence_kind=kind, line=1)


def test_adr_a_3_2_dedupes_identical_sentences():
    norms = [
        _norm("ADR-0001", "MUST", "Agents MUST cite their source"),
        _norm("ADR-0002", "MUST", "agents must cite their source."),
        _norm("ADR-0003", "SHOULD", "Tooling SHOULD log every run"),
    ]
    out = adr_compress.compress(norms, token_limit=2000)
    # Only one MUST line, plus one SHOULD line.
    must_lines = [l for l in out.body.splitlines() if l.startswith("- ") and "MUST" in l]
    should_lines = [l for l in out.body.splitlines() if l.startswith("- ") and "SHOULD" in l]
    assert len(must_lines) == 1
    assert len(should_lines) == 1
    assert "Contributing ADRs" in out.body


def test_adr_a_3_2_groups_by_keyword():
    norms = [
        _norm("ADR-0001", "MUST", "A MUST be true"),
        _norm("ADR-0002", "SHOULD", "B SHOULD be true"),
        _norm("ADR-0003", "MUST", "C MUST be true"),
    ]
    out = adr_compress.compress(norms, token_limit=2000)
    # Group order: MUST first (encountered first), then SHOULD.
    must_idx = out.body.find("### MUST")
    should_idx = out.body.find("### SHOULD")
    assert 0 <= must_idx < should_idx


def test_adr_a_3_3_token_limit_overflow_raises():
    sentence = "Tooling MUST " + " ".join(["foo"] * 50)
    norms = [
        _norm(f"ADR-{i:04d}", "MUST", sentence + f" rule {i}")
        for i in range(50)
    ]
    with pytest.raises(adr_compress.TokenLimitExceeded) as exc:
        adr_compress.compress(norms, token_limit=200)
    assert exc.value.tokens > 200
    assert exc.value.contributing  # at least some candidates listed


def test_count_tokens_basic():
    assert adr_compress.count_tokens("hello world") == 2
    assert adr_compress.count_tokens("") == 0
