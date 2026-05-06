"""Append a record to ``maintenance/run-log.md`` after each synthesis run.

Spec anchor ADR.A.3.7. The record honours the coherence-check schema
enforced by ``tools/lint-runlog.py`` (every record MUST carry
``start_commit``, ``end_commit``, ``baseline_commit``, file-delta
counters, fix counters, and ``notes``); ADR-synthesis-specific values
land in ``notes``.
"""
from __future__ import annotations

import datetime as dt
import subprocess
import sys
from pathlib import Path

_TOOLS = str(Path(__file__).resolve().parent.parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
_FM = str(Path(__file__).resolve().parent.parent / "fm")
if _FM not in sys.path:
    sys.path.insert(0, _FM)
import _core  # type: ignore  # noqa: E402


def _git_head(repo_root: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short=7", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        sha = out.stdout.strip().split()[0] if out.stdout.strip() else ""
        return sha or "n/a"
    except (OSError, subprocess.SubprocessError):
        return "n/a"


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
    sha = _git_head(run_log.parent.parent)
    contributing = ", ".join(contributing_adr_ids) or "none"
    notes = (
        f">\n  adr-synthesize {mode}; "
        f"contributing_adr_ids=[{contributing}]; "
        f"token_count={token_count}; "
        f"fidelity={fidelity:.4f} ({fidelity_mode})."
    )
    record = [
        f"### Run {today.isoformat()} — adr-synthesize",
        "- agent: tools/adr/cli.py",
        f"- start_commit: {sha}",
        f"- end_commit: {sha}",
        f"- baseline_commit: {sha}",
        "- files_in_delta: 0",
        "- files_scanned: 0",
        "- t1_fixes: 0",
        "- t2_fixes: 0",
        "- t3_tasks_created: 0",
        "- t4_skipped: 0",
        "- issues_skipped: 0",
        f"- notes: {notes}",
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
