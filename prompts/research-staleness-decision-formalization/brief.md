---
type: note
status: active
slug: research-staleness-decision-formalization-brief
summary: "Brief for prompt research-staleness-decision-formalization — extracted from tasks/039-maintenance-spec-integration/subtasks/02-research-staleness-decision-formalization.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-2: Research — Staleness Decision Formalization (cross-link)

## Raw User Request

> Extract the inlined Execution Brief from `tasks/039-maintenance-spec-integration/subtasks/02-research-staleness-decision-formalization.md` (ST-2) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 039 `maintenance-spec-integration`](../../tasks/039-maintenance-spec-integration/task.md), specifically subtask ST-2 (02-research-staleness-decision-formalization.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-2 of [Task maintenance-spec-integration](../../tasks/039-maintenance-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — **Cross-Task shared with Task 033 ST-2** — see that file for the canonical briefing; this is a cross-link stub. Whichever Task dispatches first authors the SPEC; the second consumes via filesystem detection (`test -f`).

## Goal (from subtask)

(no Goal section in source)

## Falsification (from subtask)

If both Tasks dispatch this subtask in parallel without coordination, the second one MUST detect the existing output via a `test -f` check and abort with a "stub-already-fulfilled" message rather than re-running.

## Inputs (from subtask)

(none listed)

## Acceptance Criteria (from subtask)

(none stated)

## Dependencies (from subtask)

Either Task 033 ST-2 OR Task 039 ST-2 — exactly one runs the actual research. The other reads the output.

## Estimated Effort (from subtask)

(unspecified)
