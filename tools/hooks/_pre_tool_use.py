"""PreToolUse hook (matcher Skill|Agent) — Task 094 ST-3 HK.14.2.

Three responsibilities per the subtask spec:

  1. Manifest verification — the invoked skill MUST resolve to
     `<repo>/skills/<slug>/SKILL.md`. Missing → exit 2 with stderr.
  2. Completion-claim gating — if `tool_input.prompt` contains
     "done"|"complete"|"ready" verbs, emit additionalContext suggesting
     `superpowers-verification-before-completion`.
  3. Telemetry — append a one-line row to the active Task's
     `skill-invocation-log.md` (file auto-created on first invocation).

Blocking is reserved for manifest-miss only; the other two paths are
advisory.
"""
from __future__ import annotations

import datetime as _dt
import sys
from typing import Any, TextIO

from _common import (
    active_task,
    additional_context,
    append_invocation_log,
    emit,
    read_event,
    repo_root,
    skill_exists,
)


COMPLETION_VERBS = ("done", "complete", "ready", "finished")


def _extract_skill_slug(tool_name: str, tool_input: dict[str, Any]) -> str:
    """Best-effort skill-slug extraction from the event payload."""
    if not isinstance(tool_input, dict):
        return ""
    if tool_name == "Skill":
        slug = tool_input.get("skill", "")
        if isinstance(slug, str):
            return slug.strip()
    if tool_name == "Agent":
        # The Agent tool's subagent_type is not a skill slug per se, but
        # some `.claude/agents/*.md` re-exports share the slug. Treat it
        # as best-effort.
        slug = tool_input.get("subagent_type", "")
        if isinstance(slug, str):
            return slug.strip()
    return ""


def _contains_completion_claim(tool_input: dict[str, Any]) -> bool:
    """True iff tool_input.prompt mentions a completion verb."""
    if not isinstance(tool_input, dict):
        return False
    prompt = tool_input.get("prompt", "")
    if not isinstance(prompt, str):
        return False
    lower = prompt.lower()
    return any(verb in lower for verb in COMPLETION_VERBS)


def main(stdin: TextIO, stdout: TextIO, stderr: TextIO) -> int:
    event = read_event(stdin)
    tool_name = event.get("tool_name", "") if isinstance(event, dict) else ""
    tool_input = event.get("tool_input", {}) if isinstance(event, dict) else {}
    if not isinstance(tool_name, str):
        tool_name = ""
    if not isinstance(tool_input, dict):
        tool_input = {}

    repo = repo_root()

    # 1. Manifest verification (Skill invocations only — Agent slugs are
    #    not authoritatively bound to skill SKILL.md files).
    if tool_name == "Skill":
        slug = _extract_skill_slug(tool_name, tool_input)
        if slug and not skill_exists(repo, slug):
            stderr.write(
                f"PreToolUse: skill slug '{slug}' has no skills/{slug}/"
                "SKILL.md backing it. Refusing the invocation; see "
                "CLAUDE.md §13 for the skill index.\n"
            )
            return 2

    # 2. Completion-claim gating (advisory).
    suggestion_parts: list[str] = []
    if _contains_completion_claim(tool_input):
        suggestion_parts.append(
            "Completion verb detected; consider routing through "
            "superpowers-verification-before-completion before claiming done."
        )

    # 3. Telemetry (best-effort, non-blocking).
    task_folder = active_task(repo)
    if task_folder is not None:
        slug_for_log = _extract_skill_slug(tool_name, tool_input) or "(no-slug)"
        ts = _dt.datetime.now(tz=_dt.UTC).isoformat(timespec="seconds")
        row = f"{ts} PreToolUse {tool_name} {slug_for_log}"
        append_invocation_log(task_folder, row)

    if suggestion_parts:
        emit(stdout, additional_context(" ".join(suggestion_parts)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.stdin, sys.stdout, sys.stderr))
