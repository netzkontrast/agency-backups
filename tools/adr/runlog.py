"""Append a record to ``maintenance/run-log.md`` after each synthesis run.

Spec anchor ADR.A.3.7. The record format mirrors the existing routine-run
record but uses ``adr-synthesize`` as the routine type so a maintainer can
filter for ADR runs.
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

_TOOLS = str(Path(__file__).resolve().parent.parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
_FM = str(Path(__file__).resolve().parent.parent / "fm")
if _FM not in sys.path:
    sys.path.insert(0, _FM)
import _core  # type: ignore  # noqa: E402


def append_run_record(
    *,
    run_log: Path,
    contributing_adr_ids: tuple[str, ...],
    token_count: int,
    fidelity: float,
    fidelity_mode: str,
    written: bool,
    dry_run: bool,
    today: dt.date | None = None,
) -> None:
    """Append a one-line synthesis record to ``run_log``.

    The function is best-effort: if ``run_log`` does not exist it is a
    silent no-op. Concurrent appenders are protected by ``FileLock``.
    """
    if not run_log.exists():
        return
    today = today or dt.date.today()
    mode = "dry-run" if dry_run else ("rewrite" if written else "noop")
    record = [
        f"### Run {today.isoformat()} — adr-synthesize",
        f"- agent: tools/adr/cli.py",
        f"- mode: {mode}",
        f"- contributing_adr_ids: [{', '.join(contributing_adr_ids) or 'none'}]",
        f"- token_count: {token_count}",
        f"- fidelity: {fidelity:.4f}",
        f"- fidelity_mode: {fidelity_mode}",
        "",
    ]
    payload = "\n".join(record)
    with _core.FileLock(run_log):
        existing = run_log.read_text(encoding="utf-8")
        if not existing.endswith("\n"):
            existing += "\n"
        if not existing.endswith("\n\n"):
            existing += "\n"
        run_log.write_text(existing + payload, encoding="utf-8")
