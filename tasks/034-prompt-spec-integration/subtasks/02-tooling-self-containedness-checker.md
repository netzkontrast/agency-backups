---
type: note
status: draft
slug: task-034-st2-tooling-self-containedness-checker
summary: "Subtask ST-2: ship tools/check-prompt-self-containedness.py — a structural linter that checks PROMPT.md §5.1 self-containedness via heuristics derived from the research-prompt-optimizer Phase 4 reader-test prior art."
created: 2026-05-06
updated: 2026-05-06
---

# ST-2: `check-prompt-self-containedness` — Mechanizes P.5.1

**Executor:** main-agent
**Insertion point:** `[opt]` WARN-tier — runs only on changed `/prompts/<slug>/prompt.md` files.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-3 but soft-depends on ST-1 SPEC §3 heuristic recipe. Phase A may proceed with stub heuristic + upgrade post-ST-1.

## Goal

Ship `tools/check-prompt-self-containedness.py` that scans `/prompts/<slug>/prompt.md` files and detects self-containedness violations: external context references that the executor cannot resolve. Per the FPR taxonomy from Task 034 ST-1, focus on the highest-leverage signals (e.g., references to "this conversation", "the user mentioned", "as discussed", "see above").

## Falsification

Wrong cut **iff** false-positive rate exceeds the threshold set by ST-1's empirical study. Mitigation: ST-1 SPEC §3 specifies the exact heuristics; ST-2 implements them faithfully.

## Inputs

- `research/prompt-engineering-principle-mechanizability/output/SPEC.md` (Task 034 ST-1 output) §3 self-containedness recipe.
- [`PROMPT.md`](../../../PROMPT.md) §5.1.
- [`skills/research-prompt-optimizer/phases/phase4-reader-test.md`](../../../skills/research-prompt-optimizer/phases/phase4-reader-test.md) (prior art).
- All `/prompts/<slug>/prompt.md` (test corpus).

## Acceptance Criteria

1. **Surface.** `python3 tools/check-prompt-self-containedness.py <prompt.md>` exits 0 (pass) or 2 (WARN).
2. **Checks.** Implements the regex + structural rules from ST-1 SPEC §3.
3. **Tests.** `tests/test_prompt_self_containedness.py` includes synthetic prompts that trigger each ST-1 rule.
4. **Integration.** `tools/check-governance.sh` runs WARN-tier on changed `/prompts/<slug>/prompt.md`.

## Dependencies

ST-1 (research) MUST land first.

## Estimated Effort

Medium (~120 LOC + 100 LOC tests).

## Execution Brief

```text
Implement tools/check-prompt-self-containedness.py per ST-1 SPEC §3.


Pre-flight: test -f research/prompt-engineering-principle-mechanizability/output/SPEC.md
If absent, abort.

When done:
  python3 -m unittest discover -s tests
  python3 tools/check-prompt-self-containedness.py prompts/*/prompt.md
  Commit "feat(tools): prompt self-containedness checker (Task 034 ST-2, mechanizes P.5.1)".
  Do NOT push.
```
