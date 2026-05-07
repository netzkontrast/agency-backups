---
type: index
status: active
slug: task-049-folder
summary: "Folder index for Task 049 — migrate the Task 033 ST-4 lifecycle classifier from the four-condition fallback onto the ratified five-signal `classify_task` decision tree from research/spec-staleness-decision-formalization/output/SPEC.md §1."
created: 2026-05-07
updated: 2026-05-07
---

# Task 049 Folder

## What

Operational folder for Task 049 — replaces the four-condition fallback in `tools/fm/check-task-lifecycle-classification.py` with the ratified five-signal `classify_task` algorithm from `research/spec-staleness-decision-formalization/output/SPEC.md §1`. Filed in response to [PR #81 review M-3](../../maintenance/pr-81-review.md).

## Files

- [`task.md`](./task.md) — Goal, Plan, Falsification, Todo.

## Assumptions Log

- The migration is bounded — the helper's CLI surface (`--task`, `--target-status`) stays; only the decision logic and the two attestation flags change. No spec amendment to TASK.md §4.7 beyond the helper-paragraph language refresh.
- Task 039 ST-3 (maintenance-spec-integration) is the sibling consumer of ST-2 SPEC. The Plan SHOULD verify whether absorbing this work into Task 039 ST-3 produces a cleaner cut before authoring as a standalone task; if so, mark Task 049 `task_status: updated` with `task_superseded_by: ["039"]`.
- The five-signal `classify_task` algorithm in SPEC §1 is treated as authoritative; any divergence from the SPEC pseudocode is a falsification per `task.md` Falsification clause 2.
