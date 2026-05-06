---
type: brief
status: active
slug: research-spec-staleness-decision-formalization-brief
summary: "Brief for prompt research-spec-staleness-decision-formalization — extracted from tasks/033-task-spec-integration/subtasks/02-research-spec-staleness-decision-formalization.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-2: Research — Staleness Decision Formalization

## Raw User Request

> Extract the inlined Execution Brief from `tasks/033-task-spec-integration/subtasks/02-research-spec-staleness-decision-formalization.md` (ST-2) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 033 `task-spec-integration`](../../tasks/033-task-spec-integration/task.md), specifically subtask ST-2 (02-research-spec-staleness-decision-formalization.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-2 of [Task task-spec-integration](../../tasks/033-task-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-3, ST-4. **Cross-Task shared with Task 039 ST-2** — whichever Task dispatches first authors the SPEC; the other consumes via filesystem detection (test -f).

## Goal (from subtask)

Produce `research/spec-staleness-decision-formalization/output/SPEC.md` containing a decision tree that converts observable git-history + repo-state signals into one of four staleness buckets without subjective judgment, plus the `MAINT_STALE_DAYS` declaration mechanism.

## Falsification (from subtask)

Wrong cut **iff** the decision tree requires more than 5 levels or more than 12 leaf rules. Mitigation: TASK.md §4.7 already enumerates 4 buckets; the algorithm need only deterministically map signals → buckets.

## Inputs (from subtask)

- [`MAINTENANCE.md`](../../../MAINTENANCE.md) §3.4 (current prose algorithm).
- [`TASK.md`](../../../TASK.md) §4.7 (lifecycle states).
- [`tasks/014-improve-maintenance-spec-from-session/`](../../014-improve-maintenance-spec-from-session/) (F2/F3/F4/F7 findings).
- [`tasks/025-maintenance-spec-remaining-findings/`](../../025-maintenance-spec-remaining-findings/) (carry-forward findings).
- All currently-open tasks (~7) as test cases for the algorithm.

## Acceptance Criteria (from subtask)

1. SPEC.md at `/research/spec-staleness-decision-formalization/output/SPEC.md`.
2. §1 contains a decision tree expressible in <30 lines of pseudocode.
3. §2 lists ≤5 signals; each has a one-line extraction recipe.
4. §3 walks through ≥4 currently-open tasks (e.g., 022, 023, 024, 025) and assigns each a bucket per the algorithm.
5. §4 declares the configuration mechanism (env var, repo file, or TASK.md frontmatter).
6. Two test runs by independent agents agree on bucket assignment for the §3 walkthroughs.

## Dependencies (from subtask)

None. Phase A. NOTE: Task 039 ST-2 is the *same* research subtask (cross-Task shared input). Whichever lands first authors the SPEC; the second references it.

## Estimated Effort (from subtask)

Medium (~3 hours).
