"""Body shape validation — anchors ADR.A.2.1, ADR.A.2.3, ADR.A.2.4."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools") not in sys.path:
    sys.path.insert(0, str(REPO / "tools"))

from adr import body as adr_body  # noqa: E402


_FRONTMATTER = (
    "---\n"
    "type: adr\n"
    "status: active\n"
    "slug: 0001-x\n"
    "summary: x\n"
    "created: 2026-05-06\n"
    "updated: 2026-05-06\n"
    "adr_id: ADR-0001\n"
    "adr_status: Accepted\n"
    "---\n\n"
)

_FULL_BODY = (
    "## Context and Problem Statement\nfoo\n\n"
    "## Decision Drivers\n- d1\n\n"
    "## Considered Options\n- a\n- b\n\n"
    "## Decision Outcome\nWe MUST do the thing.\n\n"
    "## Consequences\n- Positive: pros\n- Negative: cons\n"
)


def test_adr_a_2_1_missing_decision_outcome():
    text = _FRONTMATTER + _FULL_BODY.replace("## Decision Outcome\nWe MUST do the thing.\n\n", "")
    diags = adr_body.validate_body(text, "decisions/0001-x.md")
    assert any(d.code == "ADR.A.2.1" and "Decision Outcome" in d.message for d in diags)


def test_adr_a_2_1_missing_consequences():
    text = _FRONTMATTER + _FULL_BODY.replace("## Consequences\n- Positive: pros\n- Negative: cons\n", "")
    diags = adr_body.validate_body(text, "decisions/0001-x.md")
    assert any(d.code == "ADR.A.2.1" and "Consequences" in d.message for d in diags)


def test_adr_a_2_3_empty_decision_outcome():
    body = _FULL_BODY.replace("We MUST do the thing.\n", "")
    text = _FRONTMATTER + body
    diags = adr_body.validate_body(text, "decisions/0001-x.md")
    assert any(d.code == "ADR.A.2.3" for d in diags)


def test_adr_a_2_4_empty_consequences():
    body = _FULL_BODY.replace("- Positive: pros\n- Negative: cons\n", "")
    text = _FRONTMATTER + body
    diags = adr_body.validate_body(text, "decisions/0001-x.md")
    assert any(d.code == "ADR.A.2.4" for d in diags)


def test_clean_body_passes():
    text = _FRONTMATTER + _FULL_BODY
    diags = adr_body.validate_body(text, "decisions/0001-x.md")
    assert diags == []
