---
type: brief
status: active
slug: research-toolchain-flip-criteria-brief
summary: "Brief for prompt research-toolchain-flip-criteria — extracted from tasks/039-maintenance-spec-integration/subtasks/01-research-toolchain-flip-criteria.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-1: Research — Toolchain Flip Criteria

## Raw User Request

> Extract the inlined Execution Brief from `tasks/039-maintenance-spec-integration/subtasks/01-research-toolchain-flip-criteria.md` (ST-1) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 039 `maintenance-spec-integration`](../../tasks/039-maintenance-spec-integration/task.md), specifically subtask ST-1 (01-research-toolchain-flip-criteria.md). Default executor: **maintenance-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-1 of [Task maintenance-spec-integration](../../tasks/039-maintenance-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3, ST-4, ST-5. No inter-dependencies.

## Goal (from subtask)

Produce `research/toolchain-flip-criteria/output/SPEC.md` containing the deterministic flip criteria + post-flip cleanup checklist for the MAINTENANCE.md §1.1.2 dual-toolchain transition. Includes: (a) quantifiable criteria (zero outstanding waivers, X% test coverage, all required Tasks done), (b) flip-day procedure (atomic commit shape), (c) post-flip cleanup (which legacy linters retire, which warning-mode rules graduate to ERROR), (d) rollback plan if the flip breaks production.

## Falsification (from subtask)

Wrong cut **iff** the criteria cannot be evaluated mechanically (e.g., requires LLM judgment). Mitigation: the criteria are git/grep-extractable (waiver count, task_status, lint exit codes).

## Inputs (from subtask)

- [`MAINTENANCE.md`](../../../MAINTENANCE.md) §1.1.2.
- [`PRE_COMMIT.md`](../../../PRE_COMMIT.md) §7.A and §7.B.
- [`research/governance-specs-update-research/output/SPEC.md`](../../../research/governance-specs-update-research/output/SPEC.md) §2.
- [`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../../research/flexible-frontmatter-toolchain/output/SPEC.md).
- `tools/check-governance.sh`, `tools/.frontmatter-waivers`.
- Closed Tasks 016, 017, 018, 019.

## Acceptance Criteria (from subtask)

1. SPEC.md at `/research/toolchain-flip-criteria/output/SPEC.md`.
2. §1 checklist has ≤7 mechanically-verifiable items.
3. §2 flip procedure is a single git commit shape (file changes enumerated).
4. §3 post-flip cleanup names every linter to retire and every WARN-to-ERROR promotion.
5. §4 rollback procedure tested mentally against §2.
6. `research_phase: complete`; reflection friction-log.

## Dependencies (from subtask)

None. Phase A. Sibling subtask ST-2 (staleness formalization) runs in parallel.

## Estimated Effort (from subtask)

Medium (~3 hours).
