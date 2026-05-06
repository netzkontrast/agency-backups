---
type: note
status: active
slug: research-prompt-engineering-principle-mechanizability-brief
summary: "Brief for prompt research-prompt-engineering-principle-mechanizability — extracted from tasks/034-prompt-spec-integration/subtasks/01-research-prompt-engineering-principle-mechanizability.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-1: Research — Prompt-Engineering Principle Mechanizability

## Raw User Request

> Extract the inlined Execution Brief from `tasks/034-prompt-spec-integration/subtasks/01-research-prompt-engineering-principle-mechanizability.md` (ST-1) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 034 `prompt-spec-integration`](../../tasks/034-prompt-spec-integration/task.md), specifically subtask ST-1 (01-research-prompt-engineering-principle-mechanizability.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-1 of [Task prompt-spec-integration](../../tasks/034-prompt-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3. No inter-dependencies.

## Goal (from subtask)

Produce `research/prompt-engineering-principle-mechanizability/output/SPEC.md` containing a per-principle assessment for PROMPT.md §5.1 (self-containedness), §5.2 (framework declaration), §5.3 (RFC 2119), §5.4 (deliverable lock), §5.5 (anti-ambiguity), §5.6 (constraint isolation), §5.7 (failure handling). For each: (a) is it mechanically expressible? (b) what tool/heuristic? (c) false-positive rate against existing `/prompts/<slug>/prompt.md` corpus, (d) recommended ERROR vs WARN vs human-only verdict.

## Falsification (from subtask)

Wrong cut **iff** none of P.5.1–P.5.7 (other than P.5.3 which is already linted) admits a mechanical check below 20% false-positive rate. Mitigation: P.5.1 (self-containedness) is testable via "render the prompt to a fresh-context agent and ask for fidelity" — research-prompt-optimizer Phase 4 prior art proves the pattern.

## Inputs (from subtask)

- [`PROMPT.md`](../../../PROMPT.md) §5 (the seven principles).
- All `/prompts/<slug>/prompt.md` files (~33 active).
- [`skills/research-prompt-optimizer/SKILL.md`](../../../skills/research-prompt-optimizer/SKILL.md) (Phase 4 reader-test prior art).
- [`research/agent-prompt-specs-3-systems-sdd/output/SPEC.md`](../../../research/agent-prompt-specs-3-systems-sdd/output/SPEC.md) §A.2 (RFC-2119 + Gherkin contract).

## Acceptance Criteria (from subtask)

1. SPEC.md at `/research/prompt-engineering-principle-mechanizability/output/SPEC.md`.
2. §1 table: 7 rows × 5 columns (principle, mechanical recipe, FPR, ERROR/WARN/human, sample-size).
3. §2 documents the FPR-measurement methodology reproducibly.
4. §3 specifies tooling for each enforceable principle (the spec for ST-2 + ST-3 to consume).
5. §4 names the principles that stay human-review.
6. `research_phase: complete`; reflection friction-log.

## Dependencies (from subtask)

None. Phase A.

## Estimated Effort (from subtask)

Medium (~3 hours; corpus-scan + statistical FPR calc).
