"""SubagentStop hook (matcher code-reviewer|deep-research) — HK.14.5.

Routes a code-reviewer or deep-research subagent's output through the
`superpowers-receiving-code-review` discipline gate (the
technical-verification-before-action rule).

Never blocks (exit 0).
"""
from __future__ import annotations

import sys
from typing import TextIO

from _common import additional_context, emit, read_event

ROUTING_BY_AGENT = {
    "code-reviewer": (
        "Code-reviewer subagent output received. Before acting on any "
        "suggestion, route through superpowers-receiving-code-review "
        "(technical-verification-before-action: verify each claim is "
        "correct before responding)."
    ),
    "deep-research": (
        "Deep-research subagent output received. Before citing as "
        "evidence, route through superpowers-receiving-code-review's "
        "verification discipline; cross-check claims against primary "
        "sources in the workspace/."
    ),
    "superpowers-code-reviewer": (
        "Code-reviewer subagent output received. Before acting on any "
        "suggestion, route through superpowers-receiving-code-review "
        "(technical-verification-before-action: verify each claim is "
        "correct before responding)."
    ),
}


def main(stdin: TextIO, stdout: TextIO, stderr: TextIO) -> int:
    event = read_event(stdin)
    name = ""
    if isinstance(event, dict):
        # Anthropic surfaces the subagent name under `subagent_name` or
        # `subagent_type` depending on the source primitive; accept both.
        for key in ("subagent_name", "subagent_type", "matcher"):
            value = event.get(key, "")
            if isinstance(value, str) and value:
                name = value.strip().lower()
                break
    text = ROUTING_BY_AGENT.get(name)
    if text is None:
        # Default route — still useful, but generic.
        text = (
            "Subagent output received. Route through "
            "superpowers-receiving-code-review's "
            "technical-verification-before-action discipline before acting."
        )
    emit(stdout, additional_context(text))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.stdin, sys.stdout, sys.stderr))
