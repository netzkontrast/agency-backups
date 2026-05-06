---
type: brief
status: active
slug: research-friction-pattern-synthesis-brief
summary: "Brief for prompt research-friction-pattern-synthesis — extracted from tasks/033-task-spec-integration/subtasks/01-research-friction-pattern-synthesis.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-1: Research — Friction Pattern Synthesis

## Raw User Request

> Extract the inlined Execution Brief from `tasks/033-task-spec-integration/subtasks/01-research-friction-pattern-synthesis.md` (ST-1) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 033 `task-spec-integration`](../../tasks/033-task-spec-integration/task.md), specifically subtask ST-1 (01-research-friction-pattern-synthesis.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-1 of [Task task-spec-integration](../../tasks/033-task-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3, ST-4. No inter-dependencies. Sibling research subtask Task 038 ST-1 (FL0 justification) reads same corpus and may run in parallel for token-cost amortization.

## Goal (from subtask)

Produce `research/friction-pattern-synthesis/output/SPEC.md` aggregating every `friction-log.md` in `/tasks/<NNN>-<slug>/` and `/research/<slug>/reflection/` into a structured synthesis: (a) FL distribution histogram, (b) recurring root-cause taxonomy (≥6 categories), (c) per-spec friction-attribution (which root spec generated which friction), (d) recommended TASK.md / FRUSTRATED.md amendments grounded in evidence.

## Falsification (from subtask)

Wrong cut **iff** fewer than 15 closed tasks have a non-empty friction-log.md. Mitigation: 16 closed tasks (per Task 029 closure note) already exist; this is a sufficient corpus.

## Inputs (from subtask)

- All `tasks/<NNN>-<slug>/friction-log.md` (~20 files; closed tasks only).
- All `research/<slug>/reflection/friction-log.md`.
- [`tasks/030-cleanup-dramatica-skills-corpus/notes.md`](../../030-cleanup-dramatica-skills-corpus/notes.md) §3 (FE-1..FE-10 already classified).
- [`research/adr-assumption-audit/output/REPORT.md`](../../../research/adr-assumption-audit/output/REPORT.md) §1 (high-blast assumptions).

## Acceptance Criteria (from subtask)

1. SPEC.md at `/research/friction-pattern-synthesis/output/SPEC.md`.
2. §1 histogram counts FL0/FL1/FL2/FL3 across both surfaces (PR descriptions + reflection files); covers ≥15 closed tasks.
3. §2 root-cause taxonomy has ≥6 categories with frequency counts.
4. §3 per-spec attribution: which root spec each FL2+ entry implicates.
5. §4 amendments: ≥3 verbatim spec-text proposals with file:line targets.
6. `research_phase: complete`; friction-log.md present.

## Dependencies (from subtask)

None. Phase A.

## Estimated Effort (from subtask)

Large (~5 hours; corpus aggregation + thematic coding).
