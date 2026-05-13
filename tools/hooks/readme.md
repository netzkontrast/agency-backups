---
type: index
status: active
slug: tools-hooks
summary: "Folder index for tools/hooks/ — five D.7-compliant event-driven hooks authored by Task 094 ST-3 (UserPromptSubmit / PreToolUse / PostToolUse / Stop / SubagentStop). Each .sh script is a thin shim that exec's its sister _<event>.py module; the Python modules carry the testable logic. Registered in .claude/settings.json. Governance check at tools/check-hooks.py."
created: 2026-05-13
updated: 2026-05-13
---

# `tools/hooks/`

Five event-driven hook scripts that integrate the imported skill corpus with Claude Code's runtime, authored by [Task 094 ST-3](../../tasks/094-skill-integration-agency-default/subtasks/03-event-driven-hooks.md). Per [ADR-0011 D.7](../../decisions/0011-external-skill-corpora-import.md), `SessionStart` is **NOT** in the set: the bootstrap contract in [`AGENTS.md SS.1–SS.3`](../../AGENTS.md#session-setup) remains canonical.

## Hook contract

Each hook script is a `.sh` shim that exec's its sister `_<event>.py` Python module (Python 3.11 stdlib only, no external deps). The split lets `pytest` import the Python module directly (`tools/tests/test_hooks.py`) while keeping the registered command a shell script per the Anthropic hooks doc.

| Event | Matcher | Script | Logic module | Blocks? |
|---|---|---|---|---|
| `UserPromptSubmit` | (any) | [`user-prompt-submit.sh`](./user-prompt-submit.sh) | [`_user_prompt_submit.py`](./_user_prompt_submit.py) | never |
| `PreToolUse` | `Skill\|Agent` | [`pre-tool-use.sh`](./pre-tool-use.sh) | [`_pre_tool_use.py`](./_pre_tool_use.py) | manifest-miss only |
| `PostToolUse` | `Skill\|Agent` | [`post-tool-use.sh`](./post-tool-use.sh) | [`_post_tool_use.py`](./_post_tool_use.py) | never |
| `Stop` | (any) | [`stop.sh`](./stop.sh) | [`_stop.py`](./_stop.py) | FL-missing only |
| `SubagentStop` | `code-reviewer\|deep-research` | [`subagent-stop.sh`](./subagent-stop.sh) | [`_subagent_stop.py`](./_subagent_stop.py) | never |

Shared helpers live in [`_common.py`](./_common.py): JSON-event parsing, repo-root discovery, active-Task detection, skill-frontmatter reading, telemetry-append.

## Registration

Hooks are registered in [`.claude/settings.json`](../../.claude/settings.json) at the `hooks` key. The governance check [`tools/check-hooks.py`](../check-hooks.py) verifies bidirectional consistency:

- Every script under `tools/hooks/*.sh` MUST be registered (diagnostic `H.1.1`).
- Every registration MUST point at an executable script that exists (`H.1.2`).
- No script MAY be registered on `SessionStart` (`H.1.3` — ADR-0011 D.7).

## Adding a new hook

1. Pick a D.7-permitted event (`UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `Notification`, `PreCompact`, `SessionEnd`).
2. Author `tools/hooks/<event>.sh` (1–6 lines; exec the Python module) + `tools/hooks/_<event>.py` (the logic).
3. Add a pytest case to [`tools/tests/test_hooks.py`](../tests/test_hooks.py) — feed a sample event payload from `tools/tests/fixtures/hooks/<event>.json` and assert exit code + stdout/stderr.
4. Register the hook in `.claude/settings.json` using **exec form** so the path resolves regardless of cwd: `{"type": "command", "command": "${CLAUDE_PROJECT_DIR}/tools/hooks/<event>.sh", "args": []}`.
5. `chmod +x tools/hooks/<event>.sh`.
6. Run `python3 tools/check-hooks.py` — expect exit 0. The linter resolves `${CLAUDE_PROJECT_DIR}` / `$CLAUDE_PROJECT_DIR` against the repo root.

## Assumptions Log

- The Claude Code hooks runtime is the system-of-record for hook event payload schemas; the modules here read defensively (best-effort parse, swallow malformed JSON) so a payload-shape change upstream doesn't break the gate.
- "Active task" is a best-effort heuristic: branch-name slug match → unique `in_progress`/`open`/`updated` task → most-recently-modified active task. If no unique active task can be identified, telemetry is silently skipped (no false-positive block).
- The chain suggester in `_post_tool_use.py` reads `skill_references_skills` frontmatter as a flat list. Skills lacking the field still work (suggestion is silently skipped).
