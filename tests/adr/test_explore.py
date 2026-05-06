"""Exploration constraints — anchor ADR.A.1.4."""
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


def _body(options_block: str) -> str:
    return _FRONTMATTER + (
        "## Context and Problem Statement\nctx\n\n"
        "## Decision Drivers\n- d\n\n"
        f"## Considered Options\n{options_block}\n\n"
        "## Decision Outcome\nWe MUST do the thing.\n\n"
        "## Consequences\n- Positive: y MUST hold.\n"
    )


def test_adr_a_1_4_single_option_rejected():
    text = _body("- option-a")
    diags = adr_body.validate_body(text, "decisions/0001-x.md")
    assert any(d.code == "ADR.A.1.4" for d in diags)


def test_adr_a_1_4_zero_options_rejected():
    text = _body("(no options listed)")
    diags = adr_body.validate_body(text, "decisions/0001-x.md")
    assert any(d.code == "ADR.A.1.4" for d in diags)


def test_adr_a_1_4_two_options_passes():
    text = _body("- option-a\n- option-b")
    diags = adr_body.validate_body(text, "decisions/0001-x.md")
    assert not any(d.code == "ADR.A.1.4" for d in diags)


def test_adr_a_1_4_three_options_passes():
    text = _body("- option-a\n- option-b\n- option-c")
    diags = adr_body.validate_body(text, "decisions/0001-x.md")
    assert not any(d.code == "ADR.A.1.4" for d in diags)


def test_adr_a_1_4_ordered_list_form_also_counts():
    text = _body("1. option-a\n2. option-b")
    diags = adr_body.validate_body(text, "decisions/0001-x.md")
    assert not any(d.code == "ADR.A.1.4" for d in diags)
