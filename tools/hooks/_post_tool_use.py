"""PostToolUse hook (matcher Skill|Agent) — Task 094 ST-3 HK.14.3.

Two responsibilities:

  1. Telemetry — append a row to the active Task's
     `skill-invocation-log.md` summarising `tool_response` (≤ 200 chars).
  2. Chain suggestion — read the just-completed skill's
     `skill_references_skills` frontmatter; if any forward-chain
     entries exist (e.g. `sc-implement` → `sc-test`), emit
     additionalContext suggesting the chain step.

Never blocks (exit 0).
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
    read_skill_frontmatter,
    repo_root,
)

# Hardcoded list because no SuperClaude / Superpowers SKILL.md currently
# carries the symmetric inverse — the chain suggester runs forward only.
# A future Task can lift this list into per-skill frontmatter.
MAX_RESPONSE_SUMMARY = 200


def _summarise(tool_response: Any) -> str:
    """Compress tool_response to ≤ MAX_RESPONSE_SUMMARY chars, single-line."""
    if tool_response is None:
        return ""
    if isinstance(tool_response, str):
        text = tool_response
    else:
        text = repr(tool_response)
    text = text.replace("\n", " ").replace("\r", " ")
    if len(text) > MAX_RESPONSE_SUMMARY:
        text = text[: MAX_RESPONSE_SUMMARY - 1] + "…"
    return text


def _chain_suggestion(repo, slug: str) -> str:
    """Return a one-line chain suggestion from skill_references_skills, or ""."""
    if not slug:
        return ""
    fm = read_skill_frontmatter(repo, slug)
    chain = fm.get("skill_references_skills", "")
    if isinstance(chain, list) and chain:
        # Truncate to first three to keep the additionalContext compact.
        forward = chain[:3]
        return (
            f"Skill '{slug}' chains into: "
            f"{', '.join(forward)}. Consider invoking one as the next step."
        )
    return ""


def main(stdin: TextIO, stdout: TextIO, stderr: TextIO) -> int:
    event = read_event(stdin)
    tool_name = event.get("tool_name", "") if isinstance(event, dict) else ""
    tool_input = event.get("tool_input", {}) if isinstance(event, dict) else {}
    tool_response = event.get("tool_response", "") if isinstance(event, dict) else ""
    if not isinstance(tool_name, str):
        tool_name = ""
    if not isinstance(tool_input, dict):
        tool_input = {}

    slug = ""
    if isinstance(tool_input, dict):
        if tool_name == "Skill":
            raw = tool_input.get("skill", "")
            if isinstance(raw, str):
                slug = raw.strip()
        elif tool_name == "Agent":
            raw = tool_input.get("subagent_type", "")
            if isinstance(raw, str):
                slug = raw.strip()

    repo = repo_root()

    # 1. Telemetry.
    task_folder = active_task(repo)
    if task_folder is not None:
        ts = _dt.datetime.now(tz=_dt.UTC).isoformat(timespec="seconds")
        summary = _summarise(tool_response)
        slug_for_log = slug or "(no-slug)"
        row = f"{ts} PostToolUse {tool_name} {slug_for_log} :: {summary}"
        append_invocation_log(task_folder, row)

    # 2. Chain suggestion.
    chain = _chain_suggestion(repo, slug)
    if chain:
        emit(stdout, additional_context(chain))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.stdin, sys.stdout, sys.stderr))
