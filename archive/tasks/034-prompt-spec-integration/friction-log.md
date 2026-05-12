---
type: note
status: active
slug: 034-prompt-spec-integration-friction-log
summary: "Mandatory closure friction log for Task 034 (TASK.md §7.7). Records the FL declaration and summary for the run that closed the task."
created: 2026-05-07
updated: 2026-05-07
---

# Task 034 Friction Log

**Highest Frustration Level: FL1**

## Summary

Task 034 closed cleanly. Two FL1 frictions surfaced; neither blocked the work.

## FL Declaration

1. **Pre-existing corpus inconsistency surfaced by ST-3** — the framework-declaration validator flagged
   `prompts/pr27-governance-review/prompt.md` because its frontmatter declares `prompt_framework: CoT`
   but the body's `## Framework` section spells the framework as "Chain-of-Thought" (long form) without
   the canonical token `CoT`. The linter is doing its job; the prompt is a legitimate WARN. The finding
   is intentionally left unfixed — the linter is shipped WARN-tier so existing prompts remain
   committable while authors converge on the canonical token. ≈ 2 min triage cost.

2. **`prompt_spawned_from_research` provider-folder clarification was already partially in PROMPT.md** —
   the §6.5 clause shipped under Task 026 already covers the `/research/<provider>/<slug>/` resolution
   path that this Task's acceptance clause (e) names. ST-4's edit therefore tightens the existing prose
   and adds a Gherkin scenario rather than introducing a new clause. ≈ 3 min context-switch cost.

## Outcome

- `tools/check-prompt-self-containedness.py` (P.5.1 / P.B.6) shipped at WARN-tier with tests.
- `tools/check-prompt-framework-declaration.py` (P.5.2 / P.B.4) shipped at WARN-tier with tests; 1
  legitimate WARN on the existing 72-prompt corpus (1.4% rate).
- `research/prompt-engineering-principle-mechanizability/output/SPEC.md` documents per-principle
  mechanizability with empirical FPRs for the seven principles.
- PROMPT.md §4.3 replaced with a framework-selection decision tree; PROMPT.md §6 carries six Gherkin
  scenarios anchored P.B.1..P.B.6; PROMPT.md §6.5 includes the provider-folder resolution scenario.
- `tools/check-governance.sh` exits 0.
- `tasks/readme.md` Task 034 entry flipped to `done`.
