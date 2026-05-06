---
type: brief
status: active
slug: research-pre-commit-readme-update-cadence-brief
summary: "Brief for prompt research-pre-commit-readme-update-cadence — extracted from tasks/037-pre-commit-spec-integration/subtasks/01-research-pre-commit-readme-update-cadence.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-1: Research — Pre-Commit Readme-Update Cadence

## Raw User Request

> Extract the inlined Execution Brief from `tasks/037-pre-commit-spec-integration/subtasks/01-research-pre-commit-readme-update-cadence.md` (ST-1) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 037 `pre-commit-spec-integration`](../../tasks/037-pre-commit-spec-integration/task.md), specifically subtask ST-1 (01-research-pre-commit-readme-update-cadence.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-1 of [Task pre-commit-spec-integration](../../tasks/037-pre-commit-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3. **Cross-Task: this subtask's output also feeds Task 038 ST-3 (FRUSTRATED.md §28 reconciliation); both Task 037 ST-4 and Task 038 ST-3 consume the same SPEC.**

## Goal (from subtask)

Produce `research/pre-commit-readme-update-cadence/output/SPEC.md` that resolves the contradiction surfaced by the spec audit. Output: (a) a single normative rule on when readme.md is updated (immediate / batched-at-pre-commit / hybrid), (b) token-cost data backing the choice, (c) verbatim before/after wording for FRUSTRATED.md §28 and PRE_COMMIT.md §2.

## Falsification (from subtask)

Wrong cut **iff** any choice yields >2× token cost vs. status quo. Mitigation: existing closed tasks already have an emergent practice; the research can codify the cheapest one.

## Inputs (from subtask)

- [`FRUSTRATED.md`](../../../FRUSTRATED.md) §28.
- [`PRE_COMMIT.md`](../../../PRE_COMMIT.md) §2.
- [`MAINTENANCE.md`](../../../MAINTENANCE.md) §3.2.
- [`research/repo-maintenance-protocol-spec/output/SPEC.md`](../../../research/repo-maintenance-protocol-spec/output/SPEC.md) §3.1 (static/dynamic partition).
- ≥3 recent merged PRs as token-cost evidence (one with many readme updates, one with few).

## Acceptance Criteria (from subtask)

1. SPEC.md at `/research/pre-commit-readme-update-cadence/output/SPEC.md`.
2. §1 token-cost comparison covers ≥3 cadence choices.
3. §2 normative rule is unambiguous and consistent with MAINTENANCE.md §3.2.
4. §3 contains drop-in wording for FRUSTRATED.md §28 AND PRE_COMMIT.md §2.
5. §4 walkthrough on a recent session shows the rule yields the expected behaviour.
6. `research_phase: complete`; reflection friction-log.

## Dependencies (from subtask)

None. Phase A.

## Estimated Effort (from subtask)

Medium (~3 hours).
