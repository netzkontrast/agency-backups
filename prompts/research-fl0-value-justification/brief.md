---
type: note
status: active
slug: research-fl0-value-justification-brief
summary: "Brief for prompt research-fl0-value-justification — extracted from tasks/038-frustrated-spec-integration/subtasks/01-research-fl0-value-justification.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-1: Research — FL0 Value Justification

## Raw User Request

> Extract the inlined Execution Brief from `tasks/038-frustrated-spec-integration/subtasks/01-research-fl0-value-justification.md` (ST-1) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 038 `frustrated-spec-integration`](../../tasks/038-frustrated-spec-integration/task.md), specifically subtask ST-1 (01-research-fl0-value-justification.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-1 of [Task frustrated-spec-integration](../../tasks/038-frustrated-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2. No inter-dependencies.

## Goal (from subtask)

Produce `research/fl0-value-justification/output/SPEC.md` answering the question "what does an FL0 entry contribute upstream that an absent log does not". Inputs: every closed-task friction log. Outputs: (a) FL0-frequency stats, (b) qualitative analysis of FL0 entry content, (c) the upstream consumers that depend on FL0 presence (e.g., MAINTENANCE.md §3.2 friction aggregation), (d) verbatim §FL.0 rationale paragraph for FRUSTRATED.md.

## Falsification (from subtask)

Wrong cut **iff** FL0 entries provide no measurable upstream signal — in that case, the recommendation should be to make FL0 *optional* (a finding that itself justifies a spec amendment).

## Inputs (from subtask)

- All closed-task `friction-log.md` files (~16 closed tasks).
- All `research/<slug>/reflection/friction-log.md`.
- [`MAINTENANCE.md`](../../../MAINTENANCE.md) §3.2 (upstream consumer).
- [`TASK.md`](../../../TASK.md) §306 (mandate restatement).

## Acceptance Criteria (from subtask)

1. SPEC.md at `/research/fl0-value-justification/output/SPEC.md`.
2. §1 covers ≥15 closed tasks.
3. §2 quotes ≥10 distinct FL0 entries verbatim.
4. §3 names ≥1 concrete upstream consumer that depends on FL0 presence.
5. §4 verdict is one of {mandate / make-optional / clarify} with rationale.
6. §5 contains a drop-in §FL.0 paragraph for FRUSTRATED.md.
7. `research_phase: complete`; reflection friction-log.

## Dependencies (from subtask)

None. Phase A. NOTE: Task 033 ST-1 (friction-pattern-synthesis) is a sibling — they share the same corpus but ask orthogonal questions (patterns vs FL0 specifically). They can run in parallel; the FL0 study cites the pattern-synthesis if it lands first.

## Estimated Effort (from subtask)

Medium (~2.5 hours).
