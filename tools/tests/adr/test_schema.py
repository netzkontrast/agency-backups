"""Schema validation — anchors ADR.A.2.2, ADR.A.5.4."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO / "tools") not in sys.path:
    sys.path.insert(0, str(REPO / "tools"))

from adr import schema as adr_schema  # noqa: E402


def _good_fm() -> dict:
    return {
        "type": "adr",
        "status": "active",
        "slug": "0001-test",
        "summary": "ok",
        "created": "2026-05-06",
        "updated": "2026-05-06",
        "adr_id": "ADR-0001",
        "adr_status": "Accepted",
    }


def test_adr_a_2_2_clean_frontmatter_passes(mini_ontology):
    diags = adr_schema.validate_frontmatter(_good_fm(), ontology=mini_ontology)
    assert diags == []


def test_adr_a_5_4_missing_required_key(mini_ontology):
    fm = _good_fm()
    del fm["adr_id"]
    diags = adr_schema.validate_frontmatter(fm, ontology=mini_ontology)
    assert any(d.code == "ADR.A.5.4" for d in diags)


def test_adr_a_2_2_bad_adr_id_pattern(mini_ontology):
    fm = _good_fm()
    fm["adr_id"] = "ADR-42"
    diags = adr_schema.validate_frontmatter(fm, ontology=mini_ontology)
    assert any(d.code == "ADR.A.2.2" for d in diags)


def test_adr_a_2_2_invalid_adr_status(mini_ontology):
    fm = _good_fm()
    fm["adr_status"] = "Maybe"
    diags = adr_schema.validate_frontmatter(fm, ontology=mini_ontology)
    assert any(d.code == "ADR.A.2.2" for d in diags)


def test_adr_a_2_2_summary_too_long_reports_length(mini_ontology):
    """The maxLength diagnostic MUST surface actual length + cap + trim count.

    Authoring an ADR with an over-cap summary previously required iterative
    trim attempts because the diagnostic only said "is too long" without
    quantifying the gap. See Task 056 friction-log FL1.
    """
    fm = _good_fm()
    # 250-char summary; cap is 240; gap = 10.
    fm["summary"] = "x" * 250
    diags = adr_schema.validate_frontmatter(fm, ontology=mini_ontology)
    summary_diags = [
        d for d in diags
        if d.code == "ADR.A.2.2" and "summary" in d.message
    ]
    assert summary_diags, f"expected ADR.A.2.2 on summary; got {diags!r}"
    msg = summary_diags[0].message
    assert "actual=250" in msg, f"expected actual=250 in {msg!r}"
    assert "max=240" in msg, f"expected max=240 in {msg!r}"
    assert "trim 10 chars" in msg, f"expected trim count in {msg!r}"


def test_adr_a_2_2_summary_at_cap_passes(mini_ontology):
    """Exactly the cap MUST validate clean (off-by-one regression guard)."""
    fm = _good_fm()
    fm["summary"] = "x" * 240
    diags = adr_schema.validate_frontmatter(fm, ontology=mini_ontology)
    assert not any(
        d.code == "ADR.A.2.2" and "summary" in d.message
        for d in diags
    ), f"summary at exactly 240 chars should pass; got {diags!r}"
