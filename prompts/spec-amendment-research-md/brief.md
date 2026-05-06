---
type: note
status: active
slug: spec-amendment-research-md-brief
summary: "Brief for prompt spec-amendment-research-md — extracted from tasks/035-research-spec-integration/subtasks/05-spec-amendment-research-md.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-5: Spec Amendment — RESEARCH.md

## Raw User Request

> Extract the inlined Execution Brief from `tasks/035-research-spec-integration/subtasks/05-spec-amendment-research-md.md` (ST-5) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 035 `research-spec-integration`](../../tasks/035-research-spec-integration/task.md), specifically subtask ST-5 (05-spec-amendment-research-md.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-5 of [Task research-spec-integration](../../tasks/035-research-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2, ST-3, ST-4. MUST wait for all four to land.

## Goal (from subtask)

Land the RESEARCH.md edits per Task 035 (a)-(g): §2.2 spec-chunking rule, §4 session-continuity reference, §5.7 trust-audit clause, R.4.3 prompt-snapshot mid-run disambiguation, ≥6 Gherkin scenarios per R.B.1-R.B.6 anchors, references to ST-2/ST-3/ST-4 linters.

## Falsification (from subtask)

Wrong cut **iff** the §5.7 trust-audit clause references a cross-workspace AGGREGATOR (that belongs to Task 039). Mitigation: ST-5 cites ST-4's per-workspace GATE only.

## Inputs (from subtask)

- ST-1 output: `research/session-continuity-protocol-instantiation/output/SPEC.md`.
- ST-2/ST-3/ST-4 implementations.
- `research/agentic-eval-trust-improvement-spec/output/SPEC.md`.
- `research/spec-driven-research-agentic-workflows/output/SPEC.md` §spec-chunking.
- `research/agentic-session-continuity-spec/output/SPEC.md`.

## Acceptance Criteria (from subtask)

1. RESEARCH.md §2.2 mandates spec-chunking for synthesis runs >50k tokens.
2. RESEARCH.md §4 references session-continuity protocol per ST-1 output.
3. RESEARCH.md §5.7 mandates trust-audit GATE invocation at `research_phase: complete`.
4. RESEARCH.md R.4.3 disambiguates mid-run prompt-snapshot policy (lock-at-start preferred).
5. RESEARCH.md §5 has ≥6 Gherkin scenarios per R.B.1-R.B.6 anchors.
6. `tools/check-governance.sh` exits 0.

## Dependencies (from subtask)

ST-1, ST-2, ST-3, ST-4 MUST land first.

## Estimated Effort (from subtask)

Medium (~2 hours).
