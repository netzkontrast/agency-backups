#!/usr/bin/env python3
"""Trust-audit GATE — Task 035 ST-4 / RESEARCH.md §5.7.

Implements the per-workspace trust-audit gate from
``research/agentic-eval-trust-improvement-spec/output/SPEC.md`` (Spec-J/K/L).
The gate emits diagnostics on the three trust dimensions and is invoked
by ``tools/check-governance.sh`` when a research workspace transitions
to ``research_phase: complete``.

C3 partition (per spec-panel review): this module is the **GATE**. It
operates on exactly one workspace at a time. The cross-workspace
**AGGREGATOR** (rolls findings up across all workspaces for the
maintenance run) lives in Task 039 ST-5 and imports the
``DIAGNOSTIC_SCHEMA`` constant exported below.

Surface
-------

    python3 tools/check-trust-audit.py <workspace-path>

A *workspace* is a directory at ``research/<slug>/`` (the in-house run
shape). External-research result.md folders under ``research/<provider>/<slug>/``
are out of scope: they bypass the workspace pipeline by design (see
RESEARCH.md §6).

Thresholds (from brief AC-2)
----------------------------

  * schema-conformance ≥ 80%
  * behavioral          ≥ 90%
  * governance          ≥ 95%

Per-dimension checks
--------------------

Schema (10 items):
    1.  readme.md present
    2.  workspace/   subdirectory present
    3.  synthesis/   subdirectory present
    4.  reflection/  subdirectory present
    5.  output/      subdirectory present
    6.  readme.md frontmatter has all six L1 keys
    7.  readme.md frontmatter has the three research_* L2 keys
    8.  output/ contains SPEC.md or REPORT.md
    9.  output/SPEC.md (or REPORT.md) has frontmatter
    10. workspace/session.log exists

Behavioral (5 items):
    1.  workspace/session.log non-empty
    2.  synthesis/post-synthesis-log.md non-empty
    3.  synthesis/state.md present
    4.  synthesis/methodology.md present
    5.  reflection/ contains friction-log.md and at least one method file

Governance (5 items):
    1.  reflection/friction-log.md exists and declares an FL[0-3] line
    2.  research_executes_prompt resolves to /prompts/<slug>/prompt.md
    3.  research_phase value is in the valid enum
    4.  workspace/ has no execution-script stragglers (.py/.sh) — R.4.4
    5.  every required readme.md present in the four subdirs

Diagnostic format
-----------------

    <relpath>::ERROR:TRUST.<code>:<message>

The TRUST namespace mirrors the ADR validator's ``ADR.A.*`` shape so a
single MAINTENANCE.md aggregator parser can ingest both. ``DIAGNOSTIC_SCHEMA``
exports the parseable fields.

Exit codes
----------

  0 — all three thresholds met.
  1 — at least one threshold missed (or invalid invocation).
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.fm._core import read_fm, str_val  # noqa: E402

# Public schema contract — Task 039 ST-5 (AGGREGATOR) imports this.
DIAGNOSTIC_SCHEMA: dict[str, object] = {
    "format": "<relpath>::ERROR:TRUST.<code>:<message>",
    "namespace": "TRUST",
    "thresholds": {
        "schema": 0.80,
        "behavioral": 0.90,
        "governance": 0.95,
    },
    "codes": {
        "SCHEMA": "schema-conformance below threshold",
        "BEHAVIORAL": "behavioral score below threshold",
        "GOVERNANCE": "governance score below threshold",
        "PARTITION": "single-workspace-only",
        "PHASE": "invalid research_phase value",
        "INPUT": "input is not a research workspace",
    },
}

_VALID_PHASES = {"kickoff", "synthesis", "reflection", "complete"}
_L1_KEYS = ("type", "status", "slug", "summary", "created", "updated")
_RESEARCH_L2_KEYS = (
    "research_phase",
    "research_executes_prompt",
    "research_friction_level",
)
_FL_RE = re.compile(r"\bFL[0-3]\b")
_FORBIDDEN_SUFFIXES = (".py", ".sh")


@dataclass(frozen=True)
class TrustResult:
    schema_score: float
    behavioral_score: float
    governance_score: float
    diagnostics: tuple[str, ...]

    @property
    def passed(self) -> bool:
        t = DIAGNOSTIC_SCHEMA["thresholds"]
        return (
            self.schema_score >= t["schema"]
            and self.behavioral_score >= t["behavioral"]
            and self.governance_score >= t["governance"]
        )


def _exists_nonempty(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def _ratio(passes: int, total: int) -> float:
    return passes / total if total else 0.0


def _score_schema(workspace: Path) -> tuple[float, list[str]]:
    failures: list[str] = []
    rel = workspace.relative_to(REPO_ROOT)
    checks: list[tuple[str, bool]] = [
        ("readme-present", (workspace / "readme.md").exists()),
        ("workspace-subdir", (workspace / "workspace").is_dir()),
        ("synthesis-subdir", (workspace / "synthesis").is_dir()),
        ("reflection-subdir", (workspace / "reflection").is_dir()),
        ("output-subdir", (workspace / "output").is_dir()),
    ]

    readme = workspace / "readme.md"
    fm = read_fm(readme) if readme.exists() else {}
    checks.append(
        ("readme-l1", all(str_val(fm, k) for k in _L1_KEYS) if fm else False),
    )
    checks.append(
        (
            "readme-l2",
            all(str_val(fm, k) for k in _RESEARCH_L2_KEYS) if fm else False,
        ),
    )

    output_dir = workspace / "output"
    output_doc = None
    if output_dir.is_dir():
        for cand in ("SPEC.md", "REPORT.md"):
            p = output_dir / cand
            if p.exists():
                output_doc = p
                break
    checks.append(("output-doc", output_doc is not None))
    if output_doc is not None:
        out_fm = read_fm(output_doc)
        checks.append(("output-fm", bool(out_fm)))
    else:
        checks.append(("output-fm", False))
    checks.append(("session-log", (workspace / "workspace" / "session.log").exists()))

    passes = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        if not ok:
            failures.append(
                f"{rel}::ERROR:TRUST.SCHEMA:{name}:schema item failed",
            )
    return _ratio(passes, len(checks)), failures


def _score_behavioral(workspace: Path) -> tuple[float, list[str]]:
    failures: list[str] = []
    rel = workspace.relative_to(REPO_ROOT)
    checks: list[tuple[str, bool]] = [
        (
            "session-log-nonempty",
            _exists_nonempty(workspace / "workspace" / "session.log"),
        ),
        (
            "post-synthesis-log",
            _exists_nonempty(workspace / "synthesis" / "post-synthesis-log.md"),
        ),
        ("state-md", (workspace / "synthesis" / "state.md").exists()),
        ("methodology-md", (workspace / "synthesis" / "methodology.md").exists()),
    ]

    reflection = workspace / "reflection"
    method_files = (
        list(reflection.glob("M*-*.md")) if reflection.is_dir() else []
    )
    has_friction = (reflection / "friction-log.md").exists()
    checks.append(("reflection-content", bool(method_files) and has_friction))

    passes = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        if not ok:
            failures.append(
                f"{rel}::ERROR:TRUST.BEHAVIORAL:{name}:behavioral item failed",
            )
    return _ratio(passes, len(checks)), failures


def _score_governance(workspace: Path) -> tuple[float, list[str]]:
    failures: list[str] = []
    rel = workspace.relative_to(REPO_ROOT)
    checks: list[tuple[str, bool]] = []

    flog = workspace / "reflection" / "friction-log.md"
    fl_ok = False
    if flog.exists():
        try:
            text = flog.read_text(encoding="utf-8")
            fl_ok = bool(_FL_RE.search(text))
        except OSError:
            fl_ok = False
    checks.append(("friction-fl", fl_ok))

    readme_fm = read_fm(workspace / "readme.md") if (workspace / "readme.md").exists() else {}
    prompt_slug = str_val(readme_fm, "research_executes_prompt")
    prompt_ok = False
    if prompt_slug:
        prompt_ok = (REPO_ROOT / "prompts" / prompt_slug / "prompt.md").exists()
    checks.append(("prompt-linkage", prompt_ok))

    phase = str_val(readme_fm, "research_phase")
    checks.append(("phase-enum", phase in _VALID_PHASES))

    ws_dir = workspace / "workspace"
    no_stragglers = True
    if ws_dir.is_dir():
        for f in ws_dir.rglob("*"):
            if f.is_file() and f.suffix in _FORBIDDEN_SUFFIXES:
                no_stragglers = False
                break
    checks.append(("workspace-clean", no_stragglers))

    readmes_present = all(
        (workspace / sub / "readme.md").exists()
        for sub in ("workspace", "synthesis", "reflection", "output")
    )
    checks.append(("subdir-readmes", readmes_present))

    passes = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        if not ok:
            failures.append(
                f"{rel}::ERROR:TRUST.GOVERNANCE:{name}:governance item failed",
            )
    return _ratio(passes, len(checks)), failures


def audit(workspace: Path) -> TrustResult:
    schema, schema_diag = _score_schema(workspace)
    behav, behav_diag = _score_behavioral(workspace)
    gov, gov_diag = _score_governance(workspace)

    rel = workspace.relative_to(REPO_ROOT)
    summary: list[str] = list(schema_diag + behav_diag + gov_diag)

    t = DIAGNOSTIC_SCHEMA["thresholds"]
    if schema < t["schema"]:
        summary.append(
            f"{rel}::ERROR:TRUST.SCHEMA:threshold:"
            f"schema-conformance {schema:.2f} below threshold {t['schema']:.2f}",
        )
    if behav < t["behavioral"]:
        summary.append(
            f"{rel}::ERROR:TRUST.BEHAVIORAL:threshold:"
            f"behavioral {behav:.2f} below threshold {t['behavioral']:.2f}",
        )
    if gov < t["governance"]:
        summary.append(
            f"{rel}::ERROR:TRUST.GOVERNANCE:threshold:"
            f"governance {gov:.2f} below threshold {t['governance']:.2f}",
        )
    return TrustResult(
        schema_score=schema,
        behavioral_score=behav,
        governance_score=gov,
        diagnostics=tuple(summary),
    )


def _is_research_workspace(path: Path) -> bool:
    """In-house research workspace shape: research/<slug>/ with subdirs."""
    if not path.is_dir():
        return False
    try:
        rel = path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        return False
    parts = rel.parts
    if len(parts) != 2 or parts[0] != "research":
        return False
    # Provider folders (gemini/gpt/human/other) host external results, not
    # in-house workspaces — skip.
    if parts[1] in {"gemini", "gpt", "human", "other"}:
        return False
    return True


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Per-workspace trust-audit GATE (Spec-J/K/L). "
            "Emits TRUST.<code> diagnostics; exits 1 on threshold miss."
        ),
    )
    ap.add_argument(
        "workspace",
        nargs="+",
        type=Path,
        help="Single research/<slug>/ workspace path.",
    )
    args = ap.parse_args(argv)

    if len(args.workspace) > 1:
        print(
            "<input>::ERROR:TRUST.PARTITION:single-workspace-only:"
            "multi-workspace invocation rejected (Task 039 ST-5 owns aggregation)",
            file=sys.stderr,
        )
        return 1

    target = args.workspace[0]
    if not target.exists():
        print(
            f"{target}::ERROR:TRUST.INPUT:path-missing:workspace path does not exist",
            file=sys.stderr,
        )
        return 1
    if not _is_research_workspace(target):
        print(
            f"{target}::ERROR:TRUST.INPUT:not-a-workspace:"
            "path is not an in-house research workspace (research/<slug>/)",
            file=sys.stderr,
        )
        return 1

    result = audit(target.resolve())
    for line in result.diagnostics:
        print(line, file=sys.stderr)
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
