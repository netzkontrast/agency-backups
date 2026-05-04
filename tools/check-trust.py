#!/usr/bin/env python3
"""
Spec-J/K/L Trust Audit for the agency repository.

Spec-J (Agentic Output Quality Evaluation):
  J.7.1: Every closed task MUST have a friction-log.md as its quality record.

Spec-K (Human-Agent Trust Calibration):
  K.7.1: Telemetry/metadata MUST include the autonomy level tag.
          Here approximated as: every done task MUST declare task_owner.

Spec-L (Governance Improvement Loop):
  L.3.1: All friction MUST be categorized FL0-FL3.
          Checked by verifying friction-log.md contains a "FL[0-3]" declaration.
  L.4.1: FL2+ signals MUST be flagged for governance review.
          Checked by verifying FL2+ friction logs emit a visible governance flag line.
  L.7.1: Governance updates MUST be traceable to the originating friction log.
          Approximated by checking that friction-log.md is non-empty.

Usage:
    python3 tools/check-trust.py

Exits 0 on success, 1 on any diagnostic.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _frontmatter import parse_frontmatter, str_val

FL_DECL_RE = re.compile(r"\bFL[0-3]\b")
TASK_DIR_RE = re.compile(r"^\d{3}-.+$")


def audit_tasks(tasks_root: Path) -> list[str]:
    errors: list[str] = []
    for task_dir in sorted(tasks_root.iterdir()):
        if not task_dir.is_dir() or not TASK_DIR_RE.match(task_dir.name):
            continue
        task_md = task_dir / "task.md"
        if not task_md.exists():
            continue
        fm = parse_frontmatter(task_md.read_text(encoding="utf-8"), strict=False)
        task_status = str_val(fm, "task_status")
        if task_status != "done":
            continue

        # J.7.1 + L.3.1: friction-log.md MUST exist and declare FL level
        friction_log = task_dir / "friction-log.md"
        if not friction_log.exists():
            errors.append(
                f"{task_dir}: done task has no friction-log.md "
                f"(Spec-J.7.1 / Spec-L.3.1)"
            )
            continue

        log_text = friction_log.read_text(encoding="utf-8")
        if not log_text.strip():
            errors.append(
                f"{friction_log}: friction-log.md is empty — "
                f"must declare FL level (Spec-L.7.1)"
            )
            continue

        if not FL_DECL_RE.search(log_text):
            errors.append(
                f"{friction_log}: friction-log.md does not contain an FL[0-3] "
                f"declaration (Spec-L.3.1)"
            )

        # L.4.1: FL2+ must include a governance flag
        fl_match = re.search(r"\bFL([0-3])\b", log_text)
        if fl_match and int(fl_match.group(1)) >= 2:
            if "governance" not in log_text.lower():
                errors.append(
                    f"{friction_log}: FL{fl_match.group(1)} friction must include "
                    f"a governance flag/recommendation (Spec-L.4.1)"
                )

        # K.7.1: task_owner must be set (not 'unassigned' or empty)
        owner = str_val(fm, "task_owner")
        if not owner or owner == "unassigned":
            errors.append(
                f"{task_md}: done task has no task_owner set "
                f"(Spec-K.7.1)"
            )

    return errors


def main(argv: list[str]) -> int:
    root = Path(".")
    tasks_root = root / "tasks"

    all_errors: list[str] = []
    if tasks_root.exists():
        all_errors.extend(audit_tasks(tasks_root))
    else:
        print("check-trust: no /tasks/ directory found; skipping.")
        return 0

    for e in all_errors:
        print(f"ERROR {e}", file=sys.stderr)

    print(f"check-trust: {len(all_errors)} error(s).")
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
