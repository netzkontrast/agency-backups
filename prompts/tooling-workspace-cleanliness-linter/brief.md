---
type: brief
status: active
slug: tooling-workspace-cleanliness-linter-brief
summary: "Brief for prompt tooling-workspace-cleanliness-linter — extracted from tasks/035-research-spec-integration/subtasks/02-tooling-workspace-cleanliness-linter.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-2: `check-workspace-cleanliness` — Closes RESEARCH.md R.4.4 Gap

## Raw User Request

> Extract the inlined Execution Brief from `tasks/035-research-spec-integration/subtasks/02-tooling-workspace-cleanliness-linter.md` (ST-2) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 035 `research-spec-integration`](../../tasks/035-research-spec-integration/task.md), specifically subtask ST-2 (02-tooling-workspace-cleanliness-linter.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-2 of [Task research-spec-integration](../../tasks/035-research-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-3, ST-4. No inter-dependencies.

**Insertion point:** `[opt]` WARN-tier — runs over changed `/research/<slug>/workspace/` paths only.

## Goal (from subtask)

Ship `tools/check-workspace-cleanliness.py` that scans staged `/research/<slug>/workspace/` paths for execution-script stragglers (`.py`, `.sh`, `.log`) and emits a WARN diagnostic. Closes the R.4.4 enforcement gap (currently human-review only).

## Falsification (from subtask)

Wrong cut **iff** legitimate `.py` files for the worked-example need to live under `/workspace/` long-term. Mitigation: the linter accepts a `.cleanignore` file at the workspace root listing exempt paths with rationale.

## Inputs (from subtask)

- `RESEARCH.md` R.4.4 (rule statement).
- `tools/fm/_core.py` (path iteration helpers).
- `tools/adr/runlog.py` (diagnostic format prior art).

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/check-workspace-cleanliness.py [<paths>]` (defaults to scanning `research/`).
2. **Heuristic.** Flag any `.py`/`.sh`/`.log` under `/research/<slug>/workspace/`; honour `.cleanignore`.
3. **Diagnostic format.** `<relpath>::WARN:R.4.4:execution-script-not-cleaned`.
4. **Tests.** `tests/test_workspace_cleanliness.py` covers: clean workspace, straggler `.py`, ignored path, missing-workspace edge case.
5. **Integration.** `tools/check-governance.sh` runs WARN-tier.

## Dependencies (from subtask)

None. Phase A.

## Estimated Effort (from subtask)

Small (~80 LOC + 60 LOC tests).
