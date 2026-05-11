#!/usr/bin/env python3
"""Task lifecycle classification helper (Task 049 — five-signal algorithm).

Given a Task path and a proposed `task_status` transition target
(`updated` or `abandoned`), classify the Task via the ratified five-signal
`classify_task` decision tree from
`research/spec-staleness-decision-formalization/output/SPEC.md` §1 and
report PASS / FAIL against the target.

Migrated from the four-condition attestation-flag fallback (Task 033 ST-4)
to the deterministic five-signal classifier (Task 049). The CLI surface
`--task <path> --target-status {updated,abandoned}` is preserved; the two
attestation flags (`--goal-still-desirable`, `--plan-drifted`) are removed
because the SPEC mechanises both predicates into pure-function signals
(S1/S4) consumed by `classify_task`. Example::

    $ python3 tools/fm/check-task-lifecycle-classification.py \\
          --task tasks/010-skills-frontmatter-index-suite/task.md \\
          --target-status updated
    check-task-lifecycle-classification: PASS — bucket=DRIFTED (target=updated).

The five-signal algorithm is a pure function of repo state with no LLM
judgement: signals reduce to `git`/filesystem invocations whose outputs
are reproducible at a given `HEAD`. Two agents running the helper against
the same commit MUST produce identical bucket assignments.

Bucket → target mapping:
    DRIFTED                 → target=`updated` PASS
    COMPLETED_BY_DRIFT      → target=`updated` PASS (and the agent SHOULD
                              consider `done` instead; the helper emits a
                              WARN to that effect)
    NO_LONGER_DESIRABLE     → target=`abandoned` PASS (plus §8.3 notes.md
                              precondition check below)
    STILL_ACCURATE          → no transition warranted; both targets FAIL

For the `abandoned` transition the helper additionally verifies the §8.3
preconditions:

  A1. `notes.md` exists in the Task folder.
  A2. `notes.md` contains a "## Partial Artifacts" or "abandonment" reason
      paragraph (heuristic: the literal word `abandon` or a `## Partial
      Artifacts` heading).

Usage::

    python3 tools/fm/check-task-lifecycle-classification.py \\
        --task tasks/<NNN>-<slug>/task.md \\
        --target-status {updated,abandoned}

Exit codes:
    0  — transition is justified (computed bucket matches target).
    1  — transition is unjustified; diagnostics name the computed bucket and signal vector.
    2  — fatal usage error (e.g. unreadable task.md).
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))  # tools/ on path so `fm._core` resolves

from fm._core import read_fm  # noqa: E402
from fm._lifecycle_signals import (  # noqa: E402
    classify_task,
    Bucket,
    COMPLETED_BY_DRIFT,
    DRIFTED,
    NO_LONGER_DESIRABLE,
    STILL_ACCURATE,
)


def _check_abandoned_preconditions(task_path: Path) -> list[tuple[str, str]]:
    """Return §8.3 precondition failures for an `abandoned` transition."""
    diags: list[tuple[str, str]] = []
    notes = task_path.parent / "notes.md"
    if not notes.exists():
        diags.append((
            "ERROR",
            "§8.3(A1): notes.md MUST exist in the Task folder before "
            "transitioning to `abandoned`. Author it with the abandonment "
            "reason and last reproducible state.",
        ))
        return diags
    body = notes.read_text(encoding="utf-8").lower()
    has_reason = "abandon" in body or "## partial artifacts" in body
    if not has_reason:
        diags.append((
            "ERROR",
            "§8.3(A2): notes.md does not contain an abandonment rationale "
            "(no occurrence of the word 'abandon' or a '## Partial "
            "Artifacts' heading). Append a dated entry stating the reason.",
        ))
    return diags


def _expected_buckets(target_status: str) -> set[Bucket]:
    if target_status == "updated":
        return {DRIFTED, COMPLETED_BY_DRIFT}
    return {NO_LONGER_DESIRABLE}


def _format_signals(signals: dict) -> str:
    parts: list[str] = []
    for k, v in signals.items():
        if isinstance(v, float):
            parts.append(f"{k}={v:.2f}")
        else:
            parts.append(f"{k}={v}")
    return ", ".join(parts)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Classify a Task via the five-signal classify_task "
                    "algorithm and validate a proposed `updated` / "
                    "`abandoned` transition.",
    )
    ap.add_argument("--task", required=True, type=Path,
                    help="Path to tasks/<NNN>-<slug>/task.md")
    ap.add_argument("--target-status", required=True,
                    choices=["updated", "abandoned"],
                    help="Proposed task_status target.")
    ap.add_argument("--stale-days", type=int, default=None,
                    help="Override MAINT_STALE_DAYS (default: env or 7).")
    args = ap.parse_args(argv)

    if not args.task.exists():
        print(f"check-task-lifecycle-classification: {args.task}: not found",
              file=sys.stderr)
        return 2

    fm = read_fm(args.task, strict=False)
    if not fm:
        print(f"check-task-lifecycle-classification: {args.task}: "
              f"missing or unparseable frontmatter", file=sys.stderr)
        return 2

    if args.stale_days is not None:
        stale_days = args.stale_days
    else:
        try:
            stale_days = int(os.environ.get("MAINT_STALE_DAYS", "7"))
        except ValueError:
            print("check-task-lifecycle-classification: MAINT_STALE_DAYS "
                  "must be an integer", file=sys.stderr)
            return 2

    repo = args.task.resolve().parent.parent.parent
    today = date.today()
    result = classify_task(args.task, repo, today, stale_days)

    diags: list[tuple[str, str]] = []
    expected = _expected_buckets(args.target_status)

    if result.bucket not in expected:
        diags.append((
            "ERROR",
            f"classify_task -> {result.bucket.name} "
            f"({result.bucket.description}); target=`{args.target_status}` "
            f"expected one of {{{', '.join(b.name for b in expected)}}}. "
            f"Signals: {_format_signals(result.signals)}. Trace: {result.trace}",
        ))
    else:
        # Bucket matches target; emit a WARN if COMPLETED_BY_DRIFT under
        # target=updated, since `done` may be the more accurate closure.
        if result.bucket is COMPLETED_BY_DRIFT and args.target_status == "updated":
            diags.append((
                "WARN",
                "classify_task -> COMPLETED_BY_DRIFT (every Todo satisfied "
                "AND every affects-path present). The §4.7 `updated` "
                "transition is justified, but the agent SHOULD verify "
                "that `done` is not the more accurate closure before "
                "proceeding.",
            ))

    if args.target_status == "abandoned":
        diags.extend(_check_abandoned_preconditions(args.task))

    errors = [d for d in diags if d[0] == "ERROR"]
    warns = [d for d in diags if d[0] == "WARN"]

    for sev, msg in diags:
        stream = sys.stderr if sev == "ERROR" else sys.stdout
        print(f"check-task-lifecycle-classification: {sev}: {msg}",
              file=stream)

    if errors:
        print(
            f"check-task-lifecycle-classification: FAIL — "
            f"transition `{args.target_status}` is unjustified "
            f"(bucket={result.bucket.name}, {len(errors)} ERROR(s), "
            f"{len(warns)} WARN(s)).",
            file=sys.stderr,
        )
        return 1
    print(
        f"check-task-lifecycle-classification: PASS — bucket="
        f"{result.bucket.name} (target=`{args.target_status}`, "
        f"{len(warns)} WARN(s))."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
