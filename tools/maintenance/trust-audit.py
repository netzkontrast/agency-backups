#!/usr/bin/env python3
"""Trust-audit AGGREGATOR — Task 039 ST-5 / MAINTENANCE.md §3.2.

Cross-research roll-up of the per-workspace trust-audit GATE
(``tools/check-trust-audit.py``, Task 035 ST-4 / RESEARCH.md §5.7).

C3 partition (per spec-panel review)
------------------------------------

* GATE   = ``tools/check-trust-audit.py`` — operates on **one** workspace.
* AGG    = this module — iterates **all** ``research/<slug>/`` workspaces
           whose ``readme.md`` declares ``research_phase: complete`` and rolls
           per-workspace findings into a single nightly-maintenance report.

The AGGREGATOR MUST NOT re-implement the Spec-J/K/L checks. It IMPORTS:

* ``DIAGNOSTIC_SCHEMA`` — the public schema contract (thresholds, codes,
  format) — schema-locked to the GATE so a regression test catches drift.
* ``audit(workspace) -> TrustResult`` — the linter callable.
* ``_is_research_workspace(path) -> bool`` — the in-house workspace shape.

The per-workspace ``TrustResult`` (schema/behavioral/governance scores +
diagnostic tuple) is the unit of aggregation. The aggregator never opens
files inside a workspace; that work is delegated to the GATE.

Surface
-------

    python3 tools/maintenance/trust-audit.py [options]

Options:

    --threshold-mode {strict,advisory}
        ``strict``   — exit 1 if any workspace fails any threshold.
        ``advisory`` (default) — always exit 0; failures are reported but
                       do not gate. Matches the migration-window stance
                       the per-workspace GATE adopts in
                       ``tools/check-governance.sh`` (FM_TRUST_AUDIT_STRICT).

    --format {text,json}
        ``text`` (default) — Markdown-friendly per-workspace summary lines
                              + a final rolled-up tally block.
        ``json``           — Single JSON object suitable for downstream
                              ingestion (e.g. ``maintenance/run-log.md``
                              record bodies, or a programmatic friction
                              aggregator per MAINTENANCE.md §3.2).

    --root PATH
        Override the repository root (default: this file's grandparent).
        Primarily for tests that point the aggregator at a temp tree.

    --write-runlog
        Append a one-record summary to ``maintenance/run-log.md`` (using
        the schema enforced by ``tools/lint-runlog.py``). The record's
        ``routine_type`` is ``nightly-maintenance``. Best-effort: silently
        no-ops if the run-log file is absent.

FL classification (per MAINTENANCE.md §3.3 friction-aggregation contract)
-------------------------------------------------------------------------

Each failing workspace is classified into an FL-equivalent severity for
§3.3 task-delegation pipeline consumption:

* **FL3** — three thresholds failed (catastrophic trust collapse).
* **FL2** — two thresholds failed.
* **FL1** — one threshold failed.
* **FL0** — all three thresholds met (no friction).

Workspaces at FL≥1 receive a ``MAINT.TRUST.FRICTION`` diagnostic
recommending Task creation. The aggregator emits the recommendation but
**does not** auto-create Tasks (per MAINTENANCE.md §3.3 — "the agent MUST
NOT fix the complex issues directly during the maintenance run").

Diagnostic surface
------------------

Per-workspace pass-through (verbatim from GATE):

    <relpath>::ERROR:TRUST.<code>:<message>

Aggregator-level rollup diagnostic:

    <relpath>::WARN:MAINT.TRUST.FRICTION:<FLn>:<schema>/<beh>/<gov>:recommend-task

Final tally (text format) is emitted to stdout as a Markdown block; JSON
mode emits the same data as ``{"workspaces": [...], "totals": {...}}``.

Exit codes
----------

    0 — advisory mode (always), or strict mode with all workspaces passing.
    1 — strict mode + at least one workspace failed a threshold.
    2 — usage error (bad CLI arg, root path missing, etc.).

The AGGREGATOR is invoked by ``tools/check-governance.sh`` AFTER the per-
workspace GATE (advisory by default; promote with
``FM_TRUST_AUDIT_AGGREGATOR_STRICT=1``). Insertion point: between the
``[opt] Trust-audit GATE`` step and ``[opt] FL declaration linter``.
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
GATE_PATH = TOOLS_DIR / "check-trust-audit.py"

# Cache of fm-toolchain helpers (read_fm) — loaded lazily.
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _load_gate_module():
    """Import the per-workspace GATE module by file path.

    Filename uses a hyphen (``check-trust-audit.py``) so the module cannot
    be imported with ``import tools.check_trust_audit``; fall back to
    ``importlib.util.spec_from_file_location``. The module is cached on
    ``sys.modules`` under the underscore name so subsequent imports re-use
    it (the GATE module mutates its own ``REPO_ROOT`` when patched in
    tests, so we let the test fixture drive that).
    """
    mod_name = "check_trust_audit"
    if mod_name in sys.modules:
        return sys.modules[mod_name]
    spec = importlib.util.spec_from_file_location(mod_name, GATE_PATH)
    if spec is None or spec.loader is None:  # pragma: no cover — defensive
        raise RuntimeError(
            f"unable to load per-workspace GATE module at {GATE_PATH}",
        )
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


# ---- AGGREGATOR DATA MODEL -------------------------------------------------


@dataclass(frozen=True)
class WorkspaceReport:
    """Per-workspace aggregation row."""

    workspace: str  # repo-relative path, e.g. ``research/<slug>``
    schema_score: float
    behavioral_score: float
    governance_score: float
    failed_dimensions: tuple[str, ...]  # subset of {schema, behavioral, governance}
    fl_level: int  # 0..3, count of failed dimensions
    diagnostics: tuple[str, ...]  # GATE-emitted lines, verbatim

    @property
    def passed(self) -> bool:
        return not self.failed_dimensions


@dataclass
class AggregateReport:
    """Top-level rollup over all complete workspaces."""

    workspaces: list[WorkspaceReport] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)  # non-complete or non-workspace

    @property
    def totals(self) -> dict[str, Any]:
        passed = sum(1 for w in self.workspaces if w.passed)
        failed = len(self.workspaces) - passed
        fl_counts = {f"fl{n}": 0 for n in range(4)}
        dim_counts = {"schema": 0, "behavioral": 0, "governance": 0}
        for ws in self.workspaces:
            fl_counts[f"fl{ws.fl_level}"] += 1
            for dim in ws.failed_dimensions:
                dim_counts[dim] += 1
        return {
            "workspaces_total": len(self.workspaces),
            "workspaces_passed": passed,
            "workspaces_failed": failed,
            "skipped": len(self.skipped),
            "fl_buckets": fl_counts,
            "failed_dimensions": dim_counts,
            "friction_count": sum(
                fl_counts[k] for k in ("fl1", "fl2", "fl3")
            ),
        }


# ---- AGGREGATION -----------------------------------------------------------


def _has_phase_complete(readme: Path) -> bool:
    """Lightweight string check matching ``tools/check-governance.sh`` behaviour.

    The shell wrapper greps ``^research_phase: complete``; we replicate
    that here rather than parse YAML, so the AGGREGATOR's selection
    criterion is bit-identical to the GATE's invocation criterion.
    """
    if not readme.is_file():
        return False
    try:
        for line in readme.read_text(encoding="utf-8").splitlines():
            if line.strip() == "research_phase: complete":
                return True
    except OSError:
        return False
    return False


def discover_workspaces(repo_root: Path) -> list[Path]:
    """Return every in-house research workspace at ``research_phase: complete``.

    External-research provider folders (``research/{gemini,gpt,human,other}/``)
    are filtered by the GATE's ``_is_research_workspace`` helper so the
    AGGREGATOR shares the same shape contract.
    """
    research_dir = repo_root / "research"
    if not research_dir.is_dir():
        return []
    gate = _load_gate_module()
    out: list[Path] = []
    for child in sorted(research_dir.iterdir()):
        if not child.is_dir():
            continue
        if not gate._is_research_workspace(child):  # noqa: SLF001 — public-by-contract
            continue
        if _has_phase_complete(child / "readme.md"):
            out.append(child)
    return out


def _classify_failures(result: Any) -> tuple[tuple[str, ...], int]:
    """Return ``(failed_dimensions, fl_level)`` for a GATE TrustResult."""
    gate = _load_gate_module()
    thresholds = gate.DIAGNOSTIC_SCHEMA["thresholds"]
    failed: list[str] = []
    if result.schema_score < thresholds["schema"]:
        failed.append("schema")
    if result.behavioral_score < thresholds["behavioral"]:
        failed.append("behavioral")
    if result.governance_score < thresholds["governance"]:
        failed.append("governance")
    return tuple(failed), len(failed)


def aggregate(repo_root: Path) -> AggregateReport:
    """Walk all complete workspaces, invoke the GATE, return a rollup."""
    gate = _load_gate_module()
    # Patch GATE REPO_ROOT so its ``relative_to`` calls produce paths
    # rooted at our caller's repo (tests pass a temp dir).
    saved_root = gate.REPO_ROOT
    gate.REPO_ROOT = repo_root
    try:
        report = AggregateReport()
        for ws in discover_workspaces(repo_root):
            result = gate.audit(ws)
            failed, fl = _classify_failures(result)
            rel = ws.relative_to(repo_root).as_posix()
            report.workspaces.append(
                WorkspaceReport(
                    workspace=rel,
                    schema_score=result.schema_score,
                    behavioral_score=result.behavioral_score,
                    governance_score=result.governance_score,
                    failed_dimensions=failed,
                    fl_level=fl,
                    diagnostics=tuple(result.diagnostics),
                )
            )
        return report
    finally:
        gate.REPO_ROOT = saved_root


# ---- RENDERING -------------------------------------------------------------


def _friction_diagnostic(ws: WorkspaceReport) -> str:
    """Aggregator-level WARN line — recommends Task creation, never auto-creates."""
    return (
        f"{ws.workspace}::WARN:MAINT.TRUST.FRICTION:FL{ws.fl_level}:"
        f"{ws.schema_score:.2f}/{ws.behavioral_score:.2f}/"
        f"{ws.governance_score:.2f}:recommend-task"
    )


def render_text(report: AggregateReport) -> str:
    """Markdown-friendly text rendering for human review + run-log notes."""
    lines: list[str] = []
    lines.append("=== trust-audit AGGREGATOR (Task 039 ST-5 / MAINTENANCE.md §3.2) ===")
    lines.append("")
    if not report.workspaces:
        lines.append(
            "No research workspaces at research_phase: complete (nothing to roll up).",
        )
        lines.append("")
        lines.append("Totals: 0 / 0 (passed / total).")
        return "\n".join(lines) + "\n"

    lines.append(
        "## Per-workspace summary "
        f"({len(report.workspaces)} complete workspace(s))",
    )
    for ws in report.workspaces:
        verdict = "PASS" if ws.passed else f"FAIL [FL{ws.fl_level}]"
        lines.append(
            f"  {verdict}  {ws.workspace}  "
            f"schema={ws.schema_score:.2f} "
            f"behavioral={ws.behavioral_score:.2f} "
            f"governance={ws.governance_score:.2f}"
            + (
                f"  failed=[{','.join(ws.failed_dimensions)}]"
                if not ws.passed
                else ""
            ),
        )
    lines.append("")

    # Friction recommendations (FL≥1 → WARN, recommend Task creation).
    friction = [w for w in report.workspaces if w.fl_level >= 1]
    if friction:
        lines.append("## Friction recommendations (FL≥1 — file Tasks per §3.3)")
        for ws in friction:
            lines.append(f"  {_friction_diagnostic(ws)}")
        lines.append("")

    totals = report.totals
    lines.append("## Roll-up totals")
    lines.append(
        f"  workspaces: {totals['workspaces_passed']}"
        f" / {totals['workspaces_total']} (passed / total)",
    )
    lines.append(
        f"  FL buckets: FL0={totals['fl_buckets']['fl0']}  "
        f"FL1={totals['fl_buckets']['fl1']}  "
        f"FL2={totals['fl_buckets']['fl2']}  "
        f"FL3={totals['fl_buckets']['fl3']}",
    )
    fd = totals["failed_dimensions"]
    lines.append(
        f"  failed dimensions: schema={fd['schema']}  "
        f"behavioral={fd['behavioral']}  governance={fd['governance']}",
    )
    lines.append(
        f"  friction items recommending Task creation: {totals['friction_count']}",
    )
    return "\n".join(lines) + "\n"


def render_json(report: AggregateReport) -> str:
    payload: dict[str, Any] = {
        "tool": "tools/maintenance/trust-audit.py",
        "schema": "MAINT.TRUST.AGGREGATE.v1",
        "workspaces": [asdict(ws) for ws in report.workspaces],
        "totals": report.totals,
        "friction": [
            _friction_diagnostic(ws)
            for ws in report.workspaces
            if ws.fl_level >= 1
        ],
    }
    # asdict produces lists for tuples — that's the desired JSON shape.
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


# ---- RUN-LOG INTEGRATION ---------------------------------------------------


def _git_head_short(repo_root: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short=7", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        return out.stdout.strip().split()[0] if out.stdout.strip() else "n/a"
    except (OSError, subprocess.SubprocessError):
        return "n/a"


def append_runlog_record(
    *,
    repo_root: Path,
    report: AggregateReport,
    today: dt.date | None = None,
) -> bool:
    """Append a ``nightly-maintenance`` record to ``maintenance/run-log.md``.

    Returns True if a record was written, False if the run-log file is
    absent (best-effort no-op, matching ``tools/adr/runlog.py``).
    """
    run_log = repo_root / "maintenance" / "run-log.md"
    if not run_log.is_file():
        return False
    today = today or dt.date.today()
    sha = _git_head_short(repo_root)
    totals = report.totals
    notes = (
        f">\n  trust-audit aggregator: "
        f"workspaces={totals['workspaces_total']}, "
        f"passed={totals['workspaces_passed']}, "
        f"failed={totals['workspaces_failed']}, "
        f"friction={totals['friction_count']} "
        f"(FL1={totals['fl_buckets']['fl1']}, "
        f"FL2={totals['fl_buckets']['fl2']}, "
        f"FL3={totals['fl_buckets']['fl3']}). "
        f"FL≥1 entries recommend Task creation per MAINTENANCE.md §3.3."
    )
    record_lines = [
        f"### Run {today.isoformat()} — trust-audit-aggregator",
        "- agent: tools/maintenance/trust-audit.py",
        "- routine_type: nightly-maintenance",
        f"- start_commit: {sha}",
        f"- end_commit: {sha}",
        f"- baseline_commit: {sha}",
        "- files_in_delta: 0",
        f"- files_scanned: {totals['workspaces_total']}",
        "- t1_fixes: 0",
        "- t2_fixes: 0",
        "- t3_tasks_created: 0",
        f"- t4_skipped: {totals['workspaces_total']}",
        f"- issues_skipped: {totals['friction_count']}",
        f"- notes: {notes}",
        "",
    ]
    payload = "\n".join(record_lines)

    # Reuse fm-toolchain FileLock so concurrent appenders don't interleave.
    # Load _core by file-spec to avoid polluting sys.modules['fm'] with
    # a negative cache entry from package resolution (which would break
    # downstream tests that `sys.path.insert` tools/fm/ for the bare `fm`
    # dispatcher import — the conflict was observed empirically).
    FileLock = _load_fm_filelock()

    def _do_write() -> None:
        existing = run_log.read_text(encoding="utf-8")
        if not existing.endswith("\n"):
            existing += "\n"
        if not existing.endswith("\n\n"):
            existing += "\n"
        run_log.write_text(existing + payload, encoding="utf-8")

    if FileLock is not None:
        with FileLock(run_log):
            _do_write()
    else:
        _do_write()
    return True


def _load_fm_filelock():
    """Load ``tools/fm/_core.py``'s FileLock without importing the package.

    Uses ``importlib.util.spec_from_file_location`` so we never trigger
    ``import tools.fm`` (which Python resolves by also probing top-level
    ``fm``, leaving a ``None`` entry in ``sys.modules`` that breaks
    ``test_fm_wrapper.py``'s ``sys.path.insert(tools/fm/) ; import fm``
    pattern). Returns the ``FileLock`` class or ``None`` on failure.
    """
    core_path = REPO_ROOT / "tools" / "fm" / "_core.py"
    if not core_path.is_file():
        return None
    cached = sys.modules.get("_fm_core_for_aggregator")
    if cached is not None:
        return getattr(cached, "FileLock", None)
    spec = importlib.util.spec_from_file_location(
        "_fm_core_for_aggregator", core_path
    )
    if spec is None or spec.loader is None:  # pragma: no cover — defensive
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules["_fm_core_for_aggregator"] = module
    try:
        spec.loader.exec_module(module)
    except Exception:  # pragma: no cover — defensive
        sys.modules.pop("_fm_core_for_aggregator", None)
        return None
    return getattr(module, "FileLock", None)


# ---- CLI -------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description=(
            "Cross-research trust-audit AGGREGATOR (C3 partition). "
            "Imports the per-workspace GATE; iterates research_phase: complete "
            "workspaces; emits an aggregated diagnostic stream for "
            "MAINTENANCE.md §3.2 friction-aggregation."
        ),
    )
    ap.add_argument(
        "--threshold-mode",
        choices=("strict", "advisory"),
        default=os.environ.get("MAINT_TRUST_THRESHOLD_MODE", "advisory"),
        help="advisory (default): always exit 0; strict: exit 1 on any failure.",
    )
    ap.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default: text).",
    )
    ap.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root override (default: <this script>/../../).",
    )
    ap.add_argument(
        "--write-runlog",
        action="store_true",
        help=(
            "Append a nightly-maintenance record to maintenance/run-log.md "
            "(no-op if the file is absent)."
        ),
    )
    return ap


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    repo_root = args.root.resolve()
    if not repo_root.is_dir():
        print(
            f"trust-audit-aggregator::ERROR:MAINT.TRUST.INPUT:"
            f"root-missing:{repo_root}",
            file=sys.stderr,
        )
        return 2

    report = aggregate(repo_root)

    if args.format == "json":
        sys.stdout.write(render_json(report))
    else:
        sys.stdout.write(render_text(report))

    if args.write_runlog:
        append_runlog_record(repo_root=repo_root, report=report)

    if args.threshold_mode == "strict":
        return 0 if all(w.passed for w in report.workspaces) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
