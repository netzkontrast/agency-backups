---
type: note
status: active
slug: task-094-st3-event-driven-hooks
summary: "ST-3 (Task 094 Epic): author 5 D.7-compliant event-driven hooks under tools/hooks/, register them in .claude/settings.json, add the tools/check-hooks.py governance check + tools/tests/test_hooks.py fixtures, and document the framework in CLAUDE.md §14 + PRE_COMMIT.md §7.A."
created: 2026-05-12
updated: 2026-05-12
---

# ST-3 — Event-driven hooks (5 hooks total, D.7-compliant)

**Executor:** main-agent.

**Parallelism:** Sequential after ST-2 (the `.claude/settings.json` from ST-2 is the registration surface).

**Depends on:** ST-2 closed `done` (`.claude/settings.json` exists, plugin manifest declared).

## Scope

### Five hook scripts under `tools/hooks/`

Per the [Anthropic hooks doc](https://docs.anthropic.com/en/docs/claude-code/hooks), each hook is a shell command receiving a JSON event payload on stdin and emitting structured JSON on stdout. Exit codes: `0` = success, `2` = blocking error (read stderr).

#### 1. `tools/hooks/user-prompt-submit.sh` (event: `UserPromptSubmit`)

Fires when the user submits a prompt. Reads the prompt text, runs the [`superpowers-using-superpowers`](../../../skills/superpowers-using-superpowers/SKILL.md) discipline-gate selector logic (see that SKILL.md's `## How to use` table), and emits a single `additionalContext` line suggesting which Agency skill to load.

- **Input parsing:** JSON on stdin → `prompt` field.
- **Heuristic table** (matches the upstream meta-skill):
  - keywords `["fix", "bug", "broken", "failing", "error"]` → suggest `/sc:troubleshoot` (light) or `superpowers-systematic-debugging` (deep).
  - keywords `["done", "complete", "ready", "finished"]` → suggest `superpowers-verification-before-completion`.
  - keywords `["test", "tdd", "red-green"]` → suggest `/sc:test` + `superpowers-tdd`.
  - keywords `["review", "feedback", "lgtm"]` → suggest `superpowers-receiving-code-review`.
- **Output:** stdout JSON `{"hookSpecificOutput": {"additionalContext": "Consider loading: <skill-suggestion>"}}`.
- **Block:** never; non-blocking.

#### 2. `tools/hooks/pre-tool-use.sh` (event: `PreToolUse`, matcher: `Skill|Agent`)

Fires before any Skill or Agent tool invocation. Three responsibilities:

- **Manifest verification:** check the invoked skill exists in the `.skills-manifest.json` produced by `skills/skills-skill-bootstrap/sync.sh`. If missing, exit 2 with stderr.
- **Completion-claim gating:** if `tool_input.prompt` contains "done"|"complete"|"ready" verbs, inject `superpowers-verification-before-completion` context via `additionalContext`.
- **Telemetry:** if a Task is active (heuristic: `tasks/<NNN>-*/task.md` with `task_status: in_progress`), append a one-line log row to `tasks/<active>/skill-invocation-log.md` (file auto-created on first invocation).
- **Block:** only on manifest-miss.

#### 3. `tools/hooks/post-tool-use.sh` (event: `PostToolUse`, matcher: `Skill|Agent`)

Fires after a successful Skill or Agent tool. Two responsibilities:

- **Telemetry:** append a row to the active Task's `skill-invocation-log.md` with `tool_response` summary (≤ 200 chars).
- **Chain suggestion:** read the just-completed skill's `skill_references_skills` frontmatter; if any are forward-chain (e.g. `sc-implement` → `sc-test`), emit `additionalContext` suggesting the chain step.
- **Block:** never.

#### 4. `tools/hooks/stop.sh` (event: `Stop`)

Fires when Claude finishes its turn. Enforces the [AGENTS.md Closing Run Procedure](../../../AGENTS.md#closing-run-procedure) (CR.1–CR.7):

- **FL declaration check:** if the active Task's `friction-log.md` does not carry `Highest Frustration Level: FL[0-3]`, exit 2 with stderr reminding the user.
- **Index sync reminder:** check `tasks/readme.md`'s row for the active Task matches the current `task_status` frontmatter; emit `additionalContext` if drift.
- **PR reminder:** if the branch has unmerged commits + no open PR for it, emit `additionalContext` suggesting `/sc:createPR`.
- **Block:** only on FL declaration miss.

#### 5. `tools/hooks/subagent-stop.sh` (event: `SubagentStop`, matcher: `code-reviewer|deep-research`)

Fires when a code-reviewer or deep-research subagent finishes:

- **Review-routing:** emit `additionalContext` framing the subagent's output through the [`superpowers-receiving-code-review`](../../../skills/superpowers-receiving-code-review/SKILL.md) discipline (technical-verification-before-action rule).
- **Block:** never.

### Hook registration in `.claude/settings.json`

Replace the empty `hooks` block from ST-2 with the 5-event configuration:

```json
{
  "hooks": {
    "UserPromptSubmit": [{ "matcher": "", "hooks": [{ "type": "command", "command": "tools/hooks/user-prompt-submit.sh" }] }],
    "PreToolUse": [{ "matcher": "Skill|Agent", "hooks": [{ "type": "command", "command": "tools/hooks/pre-tool-use.sh" }] }],
    "PostToolUse": [{ "matcher": "Skill|Agent", "hooks": [{ "type": "command", "command": "tools/hooks/post-tool-use.sh" }] }],
    "Stop": [{ "matcher": "", "hooks": [{ "type": "command", "command": "tools/hooks/stop.sh" }] }],
    "SubagentStop": [{ "matcher": "code-reviewer|deep-research", "hooks": [{ "type": "command", "command": "tools/hooks/subagent-stop.sh" }] }]
  }
}
```

### Governance check `tools/check-hooks.py`

- For every script under `tools/hooks/*.sh`, verify it is registered in `.claude/settings.json`. Emit `H.1.1` ERROR on orphan script.
- For every event in `.claude/settings.json hooks.*`, verify the registered command exists on disk and is executable. Emit `H.1.2` ERROR on orphan registration.
- Emit `H.1.3` ERROR if any hook is registered on `SessionStart` (D.7 enforcement).
- Wire into `tools/check-governance.sh` step matrix; `PRE_COMMIT.md §7.A` adds a row.

### Test fixtures `tools/tests/test_hooks.py`

- One pytest case per hook, feeding a sample event payload from `tools/tests/fixtures/hooks/<event>.json`.
- Each case asserts: exit code, stdout JSON shape, stderr emptiness (or non-emptiness if block expected).
- Coverage target: every code path in every hook script.

### Documentation

- **`CLAUDE.md §14`** — new section "Hooks" documenting:
  - The 5-event framework (one paragraph per hook, with the event name and rough behavior).
  - D.7 enforcement: hooks MUST NOT register on `SessionStart`.
  - How to author a new hook (point at `tools/hooks/` directory + the test-fixture pattern).
  - Stable anchors: `HK.14.1` through `HK.14.5` (one per hook).
- **`PRE_COMMIT.md §7.A`** — add a `tools/check-hooks.py` row to the toolchain precedence matrix.

## Out of scope

- SessionStart hooks (D.7).
- Hooks for non-Skill-non-Agent tool kinds (the `PreToolUse` / `PostToolUse` matchers are scoped to `Skill|Agent` to keep blast radius small; can be expanded in a follow-up Task).
- Telemetry dashboards / metrics export.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: ST-3 lands the 5-hook framework

  # anchor: T094.3.1
  Scenario: Every hook fires correctly on its event
    Given ST-3 is complete
    When `pytest tools/tests/test_hooks.py -v` runs
    Then every hook's test case MUST pass
    And every hook MUST exit 0 in the success case
    And the Stop hook MUST exit 2 in the FL-missing case

  # anchor: T094.3.2
  Scenario: Hook registration is bidirectionally consistent
    Given ST-3 is complete
    When `python3 tools/check-hooks.py` runs
    Then exit code MUST be 0
    And no script under tools/hooks/ MAY be unregistered (no H.1.1 errors)
    And no registration in .claude/settings.json MAY point at a missing script (no H.1.2)

  # anchor: T094.3.3
  Scenario: D.7 enforced — no SessionStart hooks
    Given ST-3 is complete
    When a reader greps .claude/settings.json for "SessionStart"
    Then the grep MUST return zero matches
    And `python3 tools/check-hooks.py` MUST emit no H.1.3 errors

  # anchor: T094.3.4
  Scenario: Documentation lands
    Given ST-3 is complete
    When a reader opens CLAUDE.md
    Then §14 "Hooks" MUST exist with anchors HK.14.1 through HK.14.5
    And PRE_COMMIT.md §7.A MUST include the tools/check-hooks.py row
```

## Branch + PR shape

Branch: `claude/task-094-st3-event-driven-hooks`. PR title: `Task 094 ST-3: 5 event-driven hooks + governance check + CLAUDE.md §14`. PR body MUST include:

- Tree-listing of new `tools/hooks/` + `tools/tests/test_hooks.py` + fixtures.
- Output of `pytest tools/tests/test_hooks.py -v` (all green).
- Output of `python3 tools/check-hooks.py` (exit 0).
- Confirmation grep for D.7: zero `SessionStart` in `.claude/settings.json`.
- Friction-log declaration.
