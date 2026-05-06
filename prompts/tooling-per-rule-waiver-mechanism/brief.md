---
type: note
status: active
slug: tooling-per-rule-waiver-mechanism-brief
summary: "Brief for prompt tooling-per-rule-waiver-mechanism — extracted from tasks/037-pre-commit-spec-integration/subtasks/03-tooling-per-rule-waiver-mechanism.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-3: `per-rule-waiver-mechanism` — PC.7.B Refactor

## Raw User Request

> Extract the inlined Execution Brief from `tasks/037-pre-commit-spec-integration/subtasks/03-tooling-per-rule-waiver-mechanism.md` (ST-3) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 037 `pre-commit-spec-integration`](../../tasks/037-pre-commit-spec-integration/task.md), specifically subtask ST-3 (03-tooling-per-rule-waiver-mechanism.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-3 of [Task pre-commit-spec-integration](../../tasks/037-pre-commit-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2. No inter-dependencies.

**Insertion point:** `[1/5]` frontmatter linter — modifies the existing waiver-loading pathway in `tools/fm/validate.py`.

## Goal (from subtask)

Refactor `tools/.frontmatter-waivers` from per-file scope to per-rule scope. Each waiver row now carries (path-glob, rule-id, rationale, expires) where rule-id is a diagnostic code (e.g., `L1.summary-too-long`, `ADR.A.3.5`, `R.4.4`). Closes the spec-acknowledged weakness in PC.7.B.

## Falsification (from subtask)

Wrong cut **iff** the new format breaks parsing of existing per-file waivers. Mitigation: a one-time migration script translates legacy per-file waivers to per-rule waivers using the rule-id `*` (wildcard) — semantically identical. Migration runs once in this subtask; legacy format support is dropped after.

## Inputs (from subtask)

- `PRE_COMMIT.md` §7.B (current per-file rule + acknowledged weakness).
- Current `tools/.frontmatter-waivers` corpus.
- `tools/fm/validate.py` (waiver loader).
- `tools/adr/cli.py` (`ADR.A.*` diagnostic codes that must be accepted as rule-ids).

## Acceptance Criteria (from subtask)

1. `tools/.frontmatter-waivers` schema is `<path-glob>\t<rule-id>\t<rationale>\t<expires-iso8601>` (TSV).
2. Migration script `tools/scripts/migrate-waivers.py` translates legacy per-file rows to per-rule wildcard rows.
3. `tools/fm/validate.py` accepts the new format; rejects mixed legacy+new in one file.
4. **Tests.** `tests/fm/test_per_rule_waivers.py` covers: per-rule match, wildcard, expired, malformed, mixed-format-rejection.
5. `tools/adr/cli.py validate` correctly applies ADR-scope waivers.

## Dependencies (from subtask)

None. Phase A.

## Estimated Effort (from subtask)

Medium (~150 LOC refactor + migration + 100 LOC tests).
