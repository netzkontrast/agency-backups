---
type: note
status: active
slug: tooling-external-result-downstream-task-linter-brief
summary: "Brief for prompt tooling-external-result-downstream-task-linter — extracted from tasks/035-research-spec-integration/subtasks/03-tooling-external-result-downstream-task-linter.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-3: `check-external-result-downstream-task` — Closes RESEARCH.md R.6.5 Gap

## Raw User Request

> Extract the inlined Execution Brief from `tasks/035-research-spec-integration/subtasks/03-tooling-external-result-downstream-task-linter.md` (ST-3) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 035 `research-spec-integration`](../../tasks/035-research-spec-integration/task.md), specifically subtask ST-3 (03-tooling-external-result-downstream-task-linter.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-3 of [Task research-spec-integration](../../tasks/035-research-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-4. No inter-dependencies.

**Insertion point:** `[1/5]` frontmatter linter extension — runs as part of `tools/fm/validate.py --type-check` when external-research files are staged.

## Goal (from subtask)

Ship `tools/check-external-result-downstream-task.py` that, for every staged `/research/<provider>/<slug>/result.md`, verifies a corresponding `/tasks/<NNN>-<slug-or-related>/task.md` exists and references the result. Closes R.6.5 (currently human-review only).

## Falsification (from subtask)

Wrong cut **iff** the slug-matching heuristic produces false negatives because downstream Tasks legitimately use a different slug (precedent: Task 027 = `adr-spec-research-synthesis` for `/research/gemini/agency-adr-governance-spec/`). Mitigation: the linter accepts a back-link via `task_affects_paths` containing the result.md path, OR `task_uses_prompts` containing the provider slug.

## Inputs (from subtask)

- `RESEARCH.md` §6.5 (rule statement).
- `tools/fm/query.py` (frontmatter query for `task_affects_paths` cross-reference).
- Existing precedent pairs:
  - `research/gemini/agency-adr-governance-spec/` ↔ `tasks/027-adr-spec-research-synthesis/`
  - `research/gemini/superclaude-agency-orchestration-spec/` ↔ `tasks/040-superclaude-spec-evaluation/`

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/check-external-result-downstream-task.py [<paths>]`.
2. **Algorithm.** Detect any `/research/<provider>/<slug>/result.md` lacking a back-linked open Task; emit ERROR-tier diagnostic.
3. **Diagnostic format.** `<result.md path>::ERROR:R.6.5:no-downstream-task`.
4. **Tests.** `tests/test_external_result_downstream_task.py` covers: linked Task (pass), missing Task (fail), differently-slugged but back-linked Task (pass via `task_affects_paths`).
5. **Integration.** `tools/check-governance.sh` step `[1/5]` extension; ERROR-tier (gating).

## Dependencies (from subtask)

None. Phase A.

## Estimated Effort (from subtask)

Small (~100 LOC + 80 LOC tests).
