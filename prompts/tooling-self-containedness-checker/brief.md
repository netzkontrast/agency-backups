---
type: note
status: active
slug: tooling-self-containedness-checker-brief
summary: "Brief for prompt tooling-self-containedness-checker — extracted from tasks/034-prompt-spec-integration/subtasks/02-tooling-self-containedness-checker.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-2: `check-prompt-self-containedness` — Mechanizes P.5.1

## Raw User Request

> Extract the inlined Execution Brief from `tasks/034-prompt-spec-integration/subtasks/02-tooling-self-containedness-checker.md` (ST-2) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 034 `prompt-spec-integration`](../../tasks/034-prompt-spec-integration/task.md), specifically subtask ST-2 (02-tooling-self-containedness-checker.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-2 of [Task prompt-spec-integration](../../tasks/034-prompt-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-3 but soft-depends on ST-1 SPEC §3 heuristic recipe. Phase A may proceed with stub heuristic + upgrade post-ST-1.

**Insertion point:** `[opt]` WARN-tier — runs only on changed `/prompts/<slug>/prompt.md` files.

## Goal (from subtask)

Ship `tools/check-prompt-self-containedness.py` that scans `/prompts/<slug>/prompt.md` files and detects self-containedness violations: external context references that the executor cannot resolve. Per the FPR taxonomy from Task 034 ST-1, focus on the highest-leverage signals (e.g., references to "this conversation", "the user mentioned", "as discussed", "see above").

## Falsification (from subtask)

Wrong cut **iff** false-positive rate exceeds the threshold set by ST-1's empirical study. Mitigation: ST-1 SPEC §3 specifies the exact heuristics; ST-2 implements them faithfully.

## Inputs (from subtask)

- `research/prompt-engineering-principle-mechanizability/output/SPEC.md` (Task 034 ST-1 output) §3 self-containedness recipe.
- [`PROMPT.md`](../../../PROMPT.md) §5.1.
- [`skills/research-prompt-optimizer/phases/phase4-reader-test.md`](../../../skills/research-prompt-optimizer/phases/phase4-reader-test.md) (prior art).
- All `/prompts/<slug>/prompt.md` (test corpus).

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/check-prompt-self-containedness.py <prompt.md>` exits 0 (pass) or 2 (WARN).
2. **Checks.** Implements the regex + structural rules from ST-1 SPEC §3.
3. **Tests.** `tests/test_prompt_self_containedness.py` includes synthetic prompts that trigger each ST-1 rule.
4. **Integration.** `tools/check-governance.sh` runs WARN-tier on changed `/prompts/<slug>/prompt.md`.

## Dependencies (from subtask)

ST-1 (research) MUST land first.

## Estimated Effort (from subtask)

Medium (~120 LOC + 100 LOC tests).
