"""Shared fixtures for the agency-adr test suite.

Spec anchors covered: see implementation-plan.md §3.1.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
if str(REPO / "tools") not in sys.path:
    sys.path.insert(0, str(REPO / "tools"))


def _render_adr(
    adr_id: str,
    *,
    status: str = "Accepted",
    supersedes: list[str] | None = None,
    superseded_by: list[str] | None = None,
    slug: str | None = None,
    body: str | None = None,
    summary: str = "Test ADR",
    extra_fm: dict[str, str] | None = None,
) -> tuple[str, str]:
    """Return ``(filename, text)`` for a synthetic ADR."""
    num = adr_id.split("-", 1)[1] if "-" in adr_id else adr_id
    slug = slug or f"{num}-test-decision"
    fm_lines = [
        "---",
        "type: adr",
        "status: active",
        f"slug: {slug}",
        f'summary: "{summary}"',
        "created: 2026-05-06",
        "updated: 2026-05-06",
        f"adr_id: {adr_id}",
        f"adr_status: {status}",
    ]
    if supersedes:
        fm_lines.append("adr_supersedes:")
        for s in supersedes:
            fm_lines.append(f"  - {s}")
    if superseded_by:
        fm_lines.append("adr_superseded_by:")
        for s in superseded_by:
            fm_lines.append(f"  - {s}")
    for k, v in (extra_fm or {}).items():
        fm_lines.append(f"{k}: {v}")
    fm_lines.append("---")
    fm = "\n".join(fm_lines)

    if body is None:
        body = (
            "# {title}\n"
            "\n"
            "## Context and Problem Statement\n"
            "We need to decide the test invariant.\n"
            "\n"
            "## Decision Drivers\n"
            "- determinism\n"
            "- token budget\n"
            "\n"
            "## Considered Options\n"
            "- option-a\n"
            "- option-b\n"
            "\n"
            "## Decision Outcome\n"
            "Tooling MUST honour the synthesised guarded section.\n"
            "\n"
            "## Consequences\n"
            "- Positive: agents MUST treat the section as authoritative.\n"
            "- Negative: maintainers SHOULD review token counts each commit.\n"
        ).format(title=adr_id)
    text = fm + "\n\n" + body
    return f"{slug}.md", text


@pytest.fixture
def tmp_decisions_root(tmp_path):
    """Create a temp ``decisions/`` directory and return its Path."""
    root = tmp_path / "decisions"
    root.mkdir()
    return root


@pytest.fixture
def make_adr(tmp_decisions_root):
    """Return a factory that writes synthetic ADRs into a temp corpus."""

    def _make(adr_id: str, **kwargs) -> Path:
        filename, text = _render_adr(adr_id, **kwargs)
        # Override filename when slug is provided explicitly.
        slug = kwargs.get("slug")
        if slug:
            filename = f"{slug}.md"
        path = tmp_decisions_root / filename
        path.write_text(text, encoding="utf-8")
        return path

    return _make


@pytest.fixture
def mini_ontology():
    """Return the on-disk ontology dict (the validator uses this directly)."""
    fm_path = str(REPO / "tools" / "fm")
    if fm_path not in sys.path:
        sys.path.insert(0, fm_path)
    import _core  # type: ignore
    return _core.load_ontology(REPO)
