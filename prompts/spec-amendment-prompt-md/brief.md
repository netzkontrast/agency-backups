---
type: brief
status: active
slug: spec-amendment-prompt-md-brief
summary: "Brief for prompt spec-amendment-prompt-md — extracted from tasks/034-prompt-spec-integration/subtasks/04-spec-amendment-prompt-md.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-4: Spec Amendment — PROMPT.md

## Raw User Request

> Extract the inlined Execution Brief from `tasks/034-prompt-spec-integration/subtasks/04-spec-amendment-prompt-md.md` (ST-4) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 034 `prompt-spec-integration`](../../tasks/034-prompt-spec-integration/task.md), specifically subtask ST-4 (04-spec-amendment-prompt-md.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-4 of [Task prompt-spec-integration](../../tasks/034-prompt-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2, ST-3. MUST wait for Phase A converge.

## Goal (from subtask)

Land the PROMPT.md edits closing Task 034: ≥6 Gherkin scenarios per P.B.1-P.B.6 anchors (one per principle), §4.3 framework-selection decision tree, §6.5 provider-folder backward-link clarification, references to ST-2/ST-3 linters.

## Falsification (from subtask)

Wrong cut **iff** the framework decision tree adds >5 new framework names beyond the canonical RISEN/RISE-DX/ReAct/RISEN+ReAct/CoT. Mitigation: ST-1's research output bounds the set.

## Inputs (from subtask)

- ST-1 output: `research/prompt-engineering-principle-mechanizability/output/SPEC.md`.
- ST-2 implementation: `tools/check-prompt-self-containedness.py`.
- ST-3 implementation: `tools/check-prompt-framework-declaration.py`.
- `skills/research-prompt-optimizer/SKILL.md` (decision-tree prior art).

## Acceptance Criteria (from subtask)

1. PROMPT.md §6 has ≥6 new Gherkin scenarios anchored P.B.1..P.B.6 (one per topic).
2. PROMPT.md §4.3 has a decision tree (≥5 nodes) replacing the current 5-line list.
3. PROMPT.md §6.5 explains `prompt_spawned_from_research` resolution for `/research/<provider>/<slug>/`.
4. PROMPT.md cites ST-2 + ST-3 linters in §6 (Pre-Commit Checks).
5. `tools/check-governance.sh` exits 0.

## Dependencies (from subtask)

ST-1, ST-2, ST-3 MUST land first.

## Estimated Effort (from subtask)

Medium (~2 hours; 6 scenarios + decision tree authoring).
