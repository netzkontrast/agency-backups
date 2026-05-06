---
type: note
status: draft
slug: task-038-st2-research-staleness-decision-formalization
summary: "Subtask ST-2 (research, shared with Task 032 ST-2): cross-Task duplicate of the staleness-formalization research run; whichever Task lands first authors the SPEC, the second references it. Briefing identical to /tasks/032-task-spec-integration/subtasks/02-research-spec-staleness-decision-formalization.md."
created: 2026-05-06
updated: 2026-05-06
---

# ST-2: Research — Staleness Decision Formalization (cross-link)

This subtask is the **same research run** as Task 032 ST-2. The full briefing, intent block, and agent prompt live there:

→ [`/tasks/032-task-spec-integration/subtasks/02-research-spec-staleness-decision-formalization.md`](../../032-task-spec-integration/subtasks/02-research-spec-staleness-decision-formalization.md)

## Coordination Rule

Whichever of Task 032 / Task 038 dispatches this subtask first authors `research/spec-staleness-decision-formalization/output/SPEC.md`. The second task's parent task.md cites the existing SPEC; this stub remains as the cross-reference anchor.

## Acceptance (for this stub)

1. The SPEC at `/research/spec-staleness-decision-formalization/output/SPEC.md` exists.
2. Task 038 ST-6 (spec amendment) cites that SPEC by file:line in the MAINTENANCE.md §3.4 amendment.

## Dependencies

Either Task 032 ST-2 OR Task 038 ST-2 — exactly one runs the actual research. The other reads the output.

## Falsification

If both Tasks dispatch this subtask in parallel without coordination, the second one MUST detect the existing output via a `test -f` check and abort with a "stub-already-fulfilled" message rather than re-running.
