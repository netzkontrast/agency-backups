"""Run-log append — supports anchor ADR.A.3.7."""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO / "tools") not in sys.path:
    sys.path.insert(0, str(REPO / "tools"))

from adr import runlog  # noqa: E402


def test_append_when_log_missing_is_noop(tmp_path):
    missing = tmp_path / "no-such.md"
    runlog.append_run_record(
        run_log=missing,
        contributing_adr_ids=("ADR-0001",),
        token_count=10,
        fidelity=1.0,
        fidelity_mode="bcp14-keyword",
        written=True,
        dry_run=False,
    )
    assert not missing.exists()


def test_append_records_one_block(tmp_path):
    log = tmp_path / "run-log.md"
    log.write_text("# log\n", encoding="utf-8")
    runlog.append_run_record(
        run_log=log,
        contributing_adr_ids=("ADR-0001", "ADR-0002"),
        token_count=42,
        fidelity=0.9876,
        fidelity_mode="bcp14-keyword",
        written=True,
        dry_run=False,
        today=dt.date(2026, 5, 6),
    )
    text = log.read_text(encoding="utf-8")
    assert "### Run 2026-05-06 — adr-synthesize" in text
    assert "ADR-0001, ADR-0002" in text
    assert "fidelity=0.9876" in text
    # All coherence-check schema fields are present so lint-runlog.py passes.
    for field in (
        "agent", "start_commit", "end_commit", "baseline_commit",
        "files_in_delta", "files_scanned", "t1_fixes", "t2_fixes",
        "t3_tasks_created", "t4_skipped", "issues_skipped", "notes",
    ):
        assert f"- {field}:" in text, f"missing required field {field!r}"
