"""Filename ↔ frontmatter coupling — anchor ADR.A.2.7."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO / "tools") not in sys.path:
    sys.path.insert(0, str(REPO / "tools"))

from adr import corpus as adr_corpus  # noqa: E402
from adr import ids as adr_ids  # noqa: E402


def test_adr_a_2_7_passes_when_filename_matches(make_adr, tmp_decisions_root):
    make_adr("ADR-0042", slug="0042-test-decision")
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    diags = adr_ids.check_filename_coupling(corpus)
    assert diags == []


def test_adr_a_2_7_disagreeing_adr_id(make_adr, tmp_decisions_root):
    p = make_adr("ADR-0099", slug="0042-record-architecture")
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    diags = adr_ids.check_filename_coupling(corpus)
    codes = [d.code for d in diags]
    assert "ADR.A.2.7" in codes
    assert any("ADR-0042" in d.message for d in diags)


def test_adr_a_2_7_unparseable_filename(tmp_decisions_root):
    p = tmp_decisions_root / "garbage.md"
    p.write_text("---\ntype: adr\nstatus: active\nslug: 0001-x\nsummary: x\n"
                  "created: 2026-05-06\nupdated: 2026-05-06\nadr_id: ADR-0001\n"
                  "adr_status: Accepted\n---\n")
    corpus = adr_corpus.load_corpus(tmp_decisions_root)
    diags = adr_ids.check_filename_coupling(corpus)
    assert any(d.code == "ADR.A.2.7" for d in diags)
