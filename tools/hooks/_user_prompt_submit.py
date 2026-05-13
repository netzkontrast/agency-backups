"""UserPromptSubmit hook — discipline-gate suggester (Task 094 ST-3 HK.14.1).

Reads the user's submitted prompt off stdin (JSON envelope per
docs.anthropic.com/en/docs/claude-code/hooks) and emits a single
`additionalContext` line suggesting an Agency skill to load before
Claude responds. Heuristic mirrors the upstream
`superpowers-using-superpowers` selector — bug/test/done/review verb
families map to the relevant discipline gate or `/sc:*` command.

Never blocks (exit 0). When no keyword matches, exits silent.
"""
from __future__ import annotations

import sys
from typing import TextIO

from _common import additional_context, emit, read_event

# Keyword tables. Order matters: the first matching family wins so the
# suggestion stays one line.
SUGGESTIONS: tuple[tuple[tuple[str, ...], str], ...] = (
    (
        ("fix", "bug", "broken", "failing", "error"),
        "/sc:troubleshoot (light) or superpowers-systematic-debugging (deep)",
    ),
    (
        ("done", "complete", "ready", "finished"),
        "superpowers-verification-before-completion",
    ),
    (
        ("test", "tdd", "red-green"),
        "/sc:test + superpowers-tdd",
    ),
    (
        ("review", "feedback", "lgtm"),
        "superpowers-receiving-code-review",
    ),
)


def _select(prompt: str) -> str:
    """Return a suggestion string, or empty when nothing matches."""
    text = prompt.lower()
    # Word-boundary-ish match: each keyword must appear surrounded by
    # whitespace or punctuation so we don't fire on substrings like
    # "errorless" matching "error". Simple split-and-set is sufficient.
    tokens = set()
    for chunk in text.replace("/", " ").replace(",", " ").replace(".", " ").split():
        tokens.add(chunk.strip("()[]:;!?\"'`"))

    for keywords, suggestion in SUGGESTIONS:
        for keyword in keywords:
            if keyword in tokens:
                return suggestion
    return ""


def main(stdin: TextIO, stdout: TextIO, stderr: TextIO) -> int:
    event = read_event(stdin)
    prompt = ""
    if isinstance(event, dict):
        raw_prompt = event.get("prompt", "")
        if isinstance(raw_prompt, str):
            prompt = raw_prompt
    suggestion = _select(prompt)
    if suggestion:
        emit(stdout, additional_context(f"Consider loading: {suggestion}"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.stdin, sys.stdout, sys.stderr))
