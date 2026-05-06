---
type: brief
status: active
slug: tooling-narrative-ontology-load-discipline-brief
summary: "Brief for prompt tooling-narrative-ontology-load-discipline — extracted from tasks/032-agents-spec-integration/subtasks/02-tooling-narrative-ontology-load-discipline.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-2: `check-narrative-ontology-load` — NO.5 Enforcement

## Raw User Request

> Extract the inlined Execution Brief from `tasks/032-agents-spec-integration/subtasks/02-tooling-narrative-ontology-load-discipline.md` (ST-2) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 032 `agents-spec-integration`](../../tasks/032-agents-spec-integration/task.md), specifically subtask ST-2 (02-tooling-narrative-ontology-load-discipline.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-2 of [Task agents-spec-integration](../../tasks/032-agents-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-3, ST-4. No inter-dependencies.

**Insertion point:** `[opt]` WARN-tier — runs alongside the existing narrative-ontology validator block (does not gate).

## Goal (from subtask)

Ship `tools/check-narrative-ontology-load.py` that scans a recent session's tool-call log and emits a WARN when the 215-entry `maintenance/schemas/narrative-ontology/ontology.json` was loaded by an agent whose Task did not declare `task_affects_paths` referencing dramatica/ncp/skills folders. Closes the AGENTS.md NO.5 (§251) enforcement gap.

## Falsification (from subtask)

Wrong cut **iff** session-trace data is unavailable to the linter at commit time. Mitigation: tools can read the active task's frontmatter `task_affects_paths` field and the staged-files diff to infer narrative-vs-non-narrative scope without needing live tool-call traces.

## Inputs (from subtask)

- [`AGENTS.md`](../../../AGENTS.md) §NO.1–NO.6 (rules to enforce).
- `tools/dramatica-nav/` (existing narrative-ontology tooling).
- `maintenance/schemas/narrative-ontology/ontology.json`.
- `tools/fm/_core.py` (frontmatter parser).

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/check-narrative-ontology-load.py <task-folder>` exits 0 (no violation) or 2 (WARN — narrative ontology loaded in non-narrative task).
2. **Heuristic.** WARN when (a) the active task's `task_affects_paths` does NOT include `skills/dramatica-*` / `skills/ncp-*` / `skills/novel-*` AND (b) the staged diff shows reads against `maintenance/schemas/narrative-ontology/`.
3. **Tests.** `tests/test_narrative_ontology_load.py` covers: positive case (narrative task loads — pass), negative case (non-narrative task loads — WARN), edge case (no task context — exit 0).
4. **Integration.** Listed in `tools/check-governance.sh` as a WARN-tier check (not gating).
5. **Cookbook entry.** Add a one-line note to `tools/readme.md` describing the new linter.

## Dependencies (from subtask)

None. Phase A.

## Estimated Effort (from subtask)

Small (~80 LOC + 60 LOC tests).
