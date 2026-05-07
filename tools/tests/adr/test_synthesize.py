"""Synthesis orchestrator — anchors ADR.A.3.5, ADR.A.3.6, ADR.A.3.7."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO / "tools") not in sys.path:
    sys.path.insert(0, str(REPO / "tools"))

from adr import synthesize as adr_synth  # noqa: E402


_AGENTS_TEMPLATE = (
    "# AGENTS\n"
    "\n"
    "Some preface that MUST NOT be modified by synthesis.\n"
    "\n"
    "## Synthesised ADR Constraints\n"
    "\n"
    "<!-- BEGIN AGENCY-ADR SYNTHESIS -->\n"
    "<!-- AGENT-WRITTEN. DO NOT EDIT BY HAND. Edits will be overwritten by tools/adr/cli.py synthesize. -->\n"
    "_(empty placeholder)_\n"
    "<!-- END AGENCY-ADR SYNTHESIS -->\n"
    "\n"
    "## Trailer\n"
    "Bytes after the markers MUST also survive.\n"
)


def _seed_runlog(repo_root: Path) -> Path:
    maint = repo_root / "maintenance"
    maint.mkdir(parents=True, exist_ok=True)
    log = maint / "run-log.md"
    log.write_text("# log\n\n", encoding="utf-8")
    return log


def test_adr_a_3_5_missing_markers_aborts(tmp_path, make_adr, tmp_decisions_root):
    make_adr("ADR-0001", slug="0001-a")
    agents = tmp_path / "AGENTS.md"
    agents.write_text("# AGENTS\nno markers here.\n", encoding="utf-8")
    _seed_runlog(tmp_path)
    result = adr_synth.synthesize(
        agents_md=agents,
        decisions_root=tmp_decisions_root,
        repo_root=tmp_path,
    )
    assert result.exit_code == 1
    assert any(d.code == "ADR.A.3.5" for d in result.diagnostics)
    # AGENTS.md byte-for-byte unchanged.
    assert agents.read_text(encoding="utf-8") == "# AGENTS\nno markers here.\n"


def test_adr_a_3_5_writes_only_inside_markers(tmp_path, make_adr, tmp_decisions_root):
    make_adr("ADR-0001", slug="0001-a")
    agents = tmp_path / "AGENTS.md"
    agents.write_text(_AGENTS_TEMPLATE, encoding="utf-8")
    _seed_runlog(tmp_path)
    result = adr_synth.synthesize(
        agents_md=agents,
        decisions_root=tmp_decisions_root,
        repo_root=tmp_path,
    )
    assert result.exit_code == 0
    new_text = agents.read_text(encoding="utf-8")
    # Bytes before BEGIN marker are preserved.
    pre_orig = _AGENTS_TEMPLATE.split("<!-- BEGIN AGENCY-ADR SYNTHESIS -->", 1)[0]
    pre_new = new_text.split("<!-- BEGIN AGENCY-ADR SYNTHESIS -->", 1)[0]
    assert pre_orig == pre_new
    # Trailer survives.
    assert "## Trailer" in new_text
    assert "Bytes after the markers MUST also survive." in new_text
    assert "ADR-0001" in new_text


def test_adr_a_3_6_idempotent(tmp_path, make_adr, tmp_decisions_root):
    make_adr("ADR-0001", slug="0001-a")
    agents = tmp_path / "AGENTS.md"
    agents.write_text(_AGENTS_TEMPLATE, encoding="utf-8")
    log = _seed_runlog(tmp_path)
    r1 = adr_synth.synthesize(
        agents_md=agents,
        decisions_root=tmp_decisions_root,
        repo_root=tmp_path,
    )
    bytes1 = agents.read_text(encoding="utf-8")
    r2 = adr_synth.synthesize(
        agents_md=agents,
        decisions_root=tmp_decisions_root,
        repo_root=tmp_path,
    )
    bytes2 = agents.read_text(encoding="utf-8")
    assert r1.exit_code == 0 and r2.exit_code == 0
    assert bytes1 == bytes2
    # ADR.A.3.7: both runs recorded in the log.
    log_contents = log.read_text(encoding="utf-8")
    assert log_contents.count("### Run") == 2


def test_adr_a_3_3_token_limit_overflow_aborts(tmp_path, make_adr, tmp_decisions_root):
    body = (
        "## Context and Problem Statement\nx\n\n"
        "## Decision Drivers\n- d\n\n"
        "## Considered Options\n- a\n- b\n\n"
        "## Decision Outcome\nThe pipeline MUST do " + " ".join(["x"] * 100) + ".\n\n"
        "## Consequences\n- Positive: y MUST be true.\n"
    )
    for i in range(1, 6):
        make_adr(f"ADR-{i:04d}", slug=f"{i:04d}-x", body=body)
    agents = tmp_path / "AGENTS.md"
    agents.write_text(_AGENTS_TEMPLATE, encoding="utf-8")
    _seed_runlog(tmp_path)
    result = adr_synth.synthesize(
        agents_md=agents,
        decisions_root=tmp_decisions_root,
        repo_root=tmp_path,
        token_limit=50,
    )
    assert result.exit_code == 1
    assert any(d.code == "ADR.A.3.3" for d in result.diagnostics)


def test_dry_run_does_not_write(tmp_path, make_adr, tmp_decisions_root):
    make_adr("ADR-0001", slug="0001-a")
    agents = tmp_path / "AGENTS.md"
    agents.write_text(_AGENTS_TEMPLATE, encoding="utf-8")
    log = _seed_runlog(tmp_path)
    pre = agents.read_text(encoding="utf-8")
    result = adr_synth.synthesize(
        agents_md=agents,
        decisions_root=tmp_decisions_root,
        repo_root=tmp_path,
        dry_run=True,
    )
    assert result.exit_code == 0
    assert agents.read_text(encoding="utf-8") == pre
    # Dry run does not append to the log.
    assert "### Run" not in log.read_text(encoding="utf-8")
