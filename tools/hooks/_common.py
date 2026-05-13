"""Shared helpers for the Task 094 ST-3 event-driven hook scripts.

Each hook script (`tools/hooks/<event>.sh`) is a thin bash shim that
delegates to `tools/hooks/_<event>.py`. The Python modules carry the
testable logic; this module factors out the helpers they share:

  * `repo_root()`           — locate the repo root from this file's path.
  * `read_event(stdin)`     — parse the JSON event payload off stdin.
  * `emit(stdout, obj)`     — serialise a hook-output JSON dict to stdout.
  * `active_task(repo, branch=None)` — best-effort active-task heuristic.
  * `skill_exists(repo, slug)`        — `skills/<slug>/SKILL.md` exists.
  * `read_skill_frontmatter(repo, slug)` — minimal YAML parse for one
                                            SKILL.md's frontmatter block.

The helpers are kept dependency-free (Python 3.11 stdlib only) to match
the rest of `tools/`. Frontmatter parsing intentionally avoids importing
`tools/fm/_core.py` because the hooks run inside the Claude Code event
loop (latency-sensitive) and `_core.py` carries the full validator
toolchain. We only need to read a handful of fields, so a minimal
parser is fine.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, TextIO


def repo_root() -> Path:
    """Return the repo root path (the parent of `tools/`)."""
    return Path(__file__).resolve().parents[2]


def read_event(stdin: TextIO) -> dict[str, Any]:
    """Parse the JSON event payload from stdin. Empty stdin → empty dict."""
    raw = stdin.read().strip()
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def emit(stdout: TextIO, obj: dict[str, Any]) -> None:
    """Serialise `obj` to stdout as a single JSON line, no trailing newline."""
    stdout.write(json.dumps(obj, ensure_ascii=False))


def additional_context(text: str) -> dict[str, Any]:
    """Build the canonical hookSpecificOutput envelope used by 3 of the 5 hooks."""
    return {"hookSpecificOutput": {"additionalContext": text}}


_FRONTMATTER_BLOCK = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def read_skill_frontmatter(repo: Path, slug: str) -> dict[str, Any]:
    """Best-effort frontmatter read of `<repo>/skills/<slug>/SKILL.md`.

    Returns an empty dict on any failure (file missing, malformed YAML,
    etc.). Supports the subset of YAML the validator-canonical
    SKILL.md files actually use: scalar strings, list-form values,
    and the `[a, b, c]` flow-list syntax used for `skill_references_skills`.
    """
    path = repo / "skills" / slug / "SKILL.md"
    if not path.is_file():
        return {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    m = _FRONTMATTER_BLOCK.match(text)
    if not m:
        return {}
    body = m.group(1)
    out: dict[str, Any] = {}
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        if not line or line.startswith("#"):
            continue
        # Continuation lines start with whitespace; we don't need block lists
        # for the keys the hooks read, so skip them.
        if line[0].isspace():
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not value:
            out[key] = ""
            continue
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            if not inner:
                out[key] = []
            else:
                out[key] = [item.strip().strip('"').strip("'") for item in inner.split(",") if item.strip()]
            continue
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        out[key] = value
    return out


def skill_exists(repo: Path, slug: str) -> bool:
    """True iff `<repo>/skills/<slug>/SKILL.md` is a regular file."""
    if not slug or "/" in slug or slug.startswith("."):
        return False
    return (repo / "skills" / slug / "SKILL.md").is_file()


def _git_branch(repo: Path) -> str:
    """Best-effort current branch name (empty on any failure)."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
            timeout=2,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _read_task_status(task_md: Path) -> str:
    """Read `task_status:` from a task.md frontmatter (empty on miss)."""
    try:
        text = task_md.read_text(encoding="utf-8")
    except OSError:
        return ""
    m = _FRONTMATTER_BLOCK.match(text)
    if not m:
        return ""
    for line in m.group(1).splitlines():
        line = line.strip()
        if line.startswith("task_status:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return ""


_ACTIVE_STATUSES = frozenset({"in_progress", "open", "updated"})


def active_task(
    repo: Path,
    branch: str | None = None,
    statuses: frozenset[str] = _ACTIVE_STATUSES,
) -> Path | None:
    """Best-effort guess of the active task folder, or None.

    Strategy (deterministic):
      1. If a branch name is given (or git supplies one) and any task
         folder slug appears verbatim in it, return that task folder.
      2. Otherwise, if exactly one task with status ∈ `statuses` exists,
         return it.
      3. Otherwise, of the tasks whose status ∈ `statuses`, return the
         most-recently-modified task.md's parent.
      4. If no candidate exists, return None.

    The branch-name heuristic is gated on the slug appearing as a
    substring so we tolerate the platform-specific suffixes (e.g.
    `claude/execute-close-skill-integration-uPhs0`).
    """
    tasks_dir = repo / "tasks"
    if not tasks_dir.is_dir():
        return None

    if branch is None:
        branch = _git_branch(repo)

    candidates: list[tuple[Path, str, float]] = []
    for task_md in tasks_dir.glob("*/task.md"):
        slug = task_md.parent.name
        status = _read_task_status(task_md)
        if status not in statuses:
            continue
        try:
            mtime = task_md.stat().st_mtime
        except OSError:
            mtime = 0.0
        candidates.append((task_md.parent, slug, mtime))

    if not candidates:
        return None

    if branch:
        # Strip the leading NNN- prefix and try matching the slug-tail.
        for folder, slug, _ in candidates:
            tail = slug.split("-", 1)[1] if "-" in slug else slug
            if tail and tail in branch:
                return folder

    if len(candidates) == 1:
        return candidates[0][0]

    candidates.sort(key=lambda triple: triple[2], reverse=True)
    return candidates[0][0]


def append_invocation_log(task_folder: Path, row: str) -> None:
    """Append a one-line row to `<task_folder>/skill-invocation-log.md`.

    File is auto-created on first append; row is single-line; no
    trailing-newline normalisation beyond ensuring exactly one.
    Failures (permission, disk full, etc.) are swallowed because the
    hooks are non-blocking by design.
    """
    log_path = task_folder / "skill-invocation-log.md"
    try:
        already_exists = log_path.exists()
        with log_path.open("a", encoding="utf-8") as fh:
            if not already_exists:
                fh.write(
                    "# Skill invocation telemetry\n\n"
                    "Auto-generated by `tools/hooks/pre-tool-use.sh` + "
                    "`tools/hooks/post-tool-use.sh` (Task 094 ST-3). "
                    "Each row is `<ISO-8601> <event> <tool_name> "
                    "<slug-or-summary>`. Non-normative; safe to delete "
                    "between task closures.\n\n"
                )
            line = row if row.endswith("\n") else row + "\n"
            fh.write(line)
    except OSError:
        return


# Re-export os/json so the per-event modules can avoid double imports
# when they only need this helper module + sys.
__all__ = [
    "active_task",
    "additional_context",
    "append_invocation_log",
    "emit",
    "read_event",
    "read_skill_frontmatter",
    "repo_root",
    "skill_exists",
]
