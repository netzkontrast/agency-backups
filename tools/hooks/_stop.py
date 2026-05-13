"""Stop hook — Closing-Run-Procedure enforcer (Task 094 ST-3 HK.14.4).

Three responsibilities derived from AGENTS.md "Closing Run Procedure"
(CR.1–CR.7):

  1. FL declaration check — the active Task's `friction-log.md` MUST
     carry `Highest Frustration Level: FL[0-3]` (or one of the variant
     forms documented in research/fl0-value-justification/output/SPEC.md
     §2.2). Missing → exit 2 with stderr.
  2. Index-sync reminder — `tasks/readme.md`'s row for the active Task
     MUST reflect the current `task_status:` frontmatter. Drift → emit
     additionalContext (non-blocking).
  3. PR reminder — if the branch has unmerged commits + no open PR for
     it, emit additionalContext suggesting `/sc:createPR`.

The PR-presence check uses a deliberately weak heuristic (no GitHub API
call) — it just reminds the user when the branch differs from `main`.
The richer probe is done by the platform's PR primitive itself.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import TextIO

from _common import (
    active_task,
    additional_context,
    emit,
    read_event,
    repo_root,
)

# FL declaration regex — accepts the canonical form plus the variants
# enumerated in research/fl0-value-justification/output/SPEC.md §2.2.
FL_DECLARATION_RE = re.compile(
    r"(?im)^[\*\s_-]*"
    r"(?:highest\s+(?:frustration|friction)\s+level|"
    r"highest\s+friction\s+level\s+experienced|"
    r"highest\s+fl\s+experienced|"
    r"friction\s+level)"
    r"[:\s\*_-]+(FL[0-3])\b",
)
# Bare-prose variant: "**FL0** — plan obsolesced cleanly." style.
FL_BARE_RE = re.compile(r"(?m)^\s*\*?\*?(FL[0-3])\b")


def _fl_declared(text: str) -> bool:
    """True iff the friction-log body carries a parseable FL declaration."""
    if FL_DECLARATION_RE.search(text):
        return True
    # Variant 5 (bare prose) — only credit when the FL token is at the
    # start of a line so we don't false-positive on a body that just
    # mentions "FL1" in flowing prose.
    if FL_BARE_RE.search(text):
        return True
    return False


def _check_index_sync(repo: Path, task_folder: Path) -> str | None:
    """Return a reminder string if the tasks index row is stale, else None."""
    index = repo / "tasks" / "readme.md"
    if not index.is_file():
        return None
    task_md = task_folder / "task.md"
    if not task_md.is_file():
        return None
    try:
        task_text = task_md.read_text(encoding="utf-8")
        index_text = index.read_text(encoding="utf-8")
    except OSError:
        return None
    status_match = re.search(r"(?m)^task_status:\s*(\S+)", task_text)
    if not status_match:
        return None
    status = status_match.group(1).strip().strip('"').strip("'")
    slug = task_folder.name
    # Look for the slug's row in tasks/readme.md and check its mention of
    # the status (the column shape varies; substring match is sufficient).
    row_match = re.search(rf"(?m)^[\|\s\*-].*{re.escape(slug)}.*$", index_text)
    if not row_match:
        # Slug not in index — definitely drift.
        return (
            f"tasks/readme.md has no row for active Task '{slug}'; "
            "run `python3 tools/fm/index_diff.py` and update the index."
        )
    row = row_match.group(0)
    if status not in row:
        return (
            f"tasks/readme.md row for '{slug}' does not mention current "
            f"task_status '{status}'; run `python3 tools/fm/index_diff.py`."
        )
    return None


def _branch_ahead_of_main(repo: Path) -> bool:
    """True iff the current branch has commits ahead of `main`/`master`."""
    try:
        branch_result = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
            timeout=2,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return False
    if branch_result.returncode != 0:
        return False
    branch = branch_result.stdout.strip()
    if branch in ("", "main", "master", "HEAD"):
        return False
    for base in ("origin/main", "origin/master", "main", "master"):
        try:
            result = subprocess.run(
                [
                    "git", "-C", str(repo),
                    "rev-list", "--count", f"{base}..HEAD",
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=2,
            )
        except (FileNotFoundError, subprocess.SubprocessError):
            continue
        if result.returncode == 0 and result.stdout.strip().isdigit():
            return int(result.stdout.strip()) > 0
    return False


def main(stdin: TextIO, stdout: TextIO, stderr: TextIO) -> int:
    # stdin payload not consulted today — Anthropic ships it for symmetry
    # but the Stop hook is project-state-driven, not event-driven.
    read_event(stdin)

    repo = repo_root()
    task_folder = active_task(repo)

    # 1. FL declaration check. Only gates when we can uniquely identify
    # the active Task; otherwise we're silent (no false-positive block).
    if task_folder is not None:
        log_path = task_folder / "friction-log.md"
        if not log_path.is_file():
            stderr.write(
                f"Stop hook: active Task '{task_folder.name}' has no "
                "friction-log.md. Author one with `Highest Frustration "
                "Level: FL[0-3]` before closing the session "
                "(AGENTS.md CR.1).\n"
            )
            return 2
        try:
            log_text = log_path.read_text(encoding="utf-8")
        except OSError:
            log_text = ""
        if not _fl_declared(log_text):
            stderr.write(
                f"Stop hook: friction-log.md for active Task "
                f"'{task_folder.name}' is missing a parseable "
                "`Highest Frustration Level: FL[0-3]` declaration "
                "(FRUSTRATED.md §FL.Log).\n"
            )
            return 2

    # 2. Advisory reminders.
    parts: list[str] = []
    if task_folder is not None:
        drift = _check_index_sync(repo, task_folder)
        if drift:
            parts.append(drift)
    if _branch_ahead_of_main(repo):
        parts.append(
            "Branch is ahead of main. If the session is closing, run "
            "`/sc:createPR` (CLAUDE.md §10 step 4)."
        )

    if parts:
        emit(stdout, additional_context(" ".join(parts)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.stdin, sys.stdout, sys.stderr))
