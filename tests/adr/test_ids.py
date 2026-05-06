"""Duplicate-id detection — anchor ADR.A.5.6."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools") not in sys.path:
    sys.path.insert(0, str(REPO / "tools"))

from adr import corpus as adr_corpus  # noqa: E402
from adr import ids as adr_ids  # noqa: E402


def test_adr_a_5_6_duplicate_id(make_adr, tmp_decisions_root):
    make_adr("ADR-0042", slug="0042-first")
    make_adr("ADR-0042", slug="0042-second")
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    diags = adr_ids.check_unique_ids(corpus)
    assert any(d.code == "ADR.A.5.6" for d in diags)
    # Both files cited.
    msgs = " ".join(d.message for d in diags)
    assert "0042-first" in msgs and "0042-second" in msgs


def test_adr_a_5_6_unique_ids_pass(make_adr, tmp_decisions_root):
    make_adr("ADR-0001", slug="0001-a")
    make_adr("ADR-0002", slug="0002-b")
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    diags = adr_ids.check_unique_ids(corpus)
    assert diags == []
