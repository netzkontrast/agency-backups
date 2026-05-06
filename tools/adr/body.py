"""MADR body validation for ADR files.

Spec anchors:
  - ADR.A.1.4 — "Considered Options" MUST hold at least two options.
  - ADR.A.2.1 — required MADR headings.
  - ADR.A.2.3 — "Decision Outcome" must declare the chosen option.
  - ADR.A.2.4 — "Consequences" must enumerate impacts.
"""
from __future__ import annotations

import sys
from pathlib import Path

_TOOLS = str(Path(__file__).resolve().parent.parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
_FM = str(Path(__file__).resolve().parent.parent / "fm")
if _FM not in sys.path:
    sys.path.insert(0, _FM)
import _core  # type: ignore  # noqa: E402

Diagnostic = _core.Diagnostic

REQUIRED_HEADINGS = (
    "Context and Problem Statement",
    "Decision Drivers",
    "Considered Options",
    "Decision Outcome",
    "Consequences",
)


def validate_body(text: str, rel: str) -> list[Diagnostic]:
    """Return diagnostics for any MADR-shape violation in ``text``."""
    diags: list[Diagnostic] = []
    _, body = _core.split_frontmatter_and_body(text)
    actual = {_core.normalise_heading(h) for _, h in _core.iter_h2(body)}

    for heading in REQUIRED_HEADINGS:
        if _core.normalise_heading(heading) not in actual:
            diags.append(Diagnostic(
                rel, None, "ERROR", "ADR.A.2.1",
                f"missing required MADR heading '## {heading}'",
            ))

    decision = _core.find_section_body(text, "Decision Outcome")
    if decision is not None:
        stripped = decision.strip()
        if not stripped:
            diags.append(Diagnostic(
                rel, None, "ERROR", "ADR.A.2.3",
                "section '## Decision Outcome' is empty; "
                "it MUST declare the chosen option in a single sentence",
            ))

    consequences = _core.find_section_body(text, "Consequences")
    if consequences is not None and not consequences.strip():
        diags.append(Diagnostic(
            rel, None, "ERROR", "ADR.A.2.4",
            "section '## Consequences' is empty; "
            "it MUST enumerate positive, negative, and neutral impacts",
        ))

    options = _core.find_section_body(text, "Considered Options")
    if options is not None:
        items = _core._list_items(options)
        if len(items) < 2:
            diags.append(Diagnostic(
                rel, None, "ERROR", "ADR.A.1.4",
                "section '## Considered Options' lists "
                f"{len(items)} option(s); exploration requires at least two "
                "mutually exclusive options",
            ))

    return diags
