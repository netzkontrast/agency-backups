---
type: index
status: active
slug: fix-ft1-scope-drift-prompt-readme
summary: "Index for prompt fix-ft1-scope-drift — investigate and resolve the F.T.1 spec/implementation drift surfaced in PR #81 review R-2: TASK.md §7.3 documents closure-only enforcement; validate.py --type-check enforces unconditionally."
created: 2026-05-07
updated: 2026-05-07
---

# Prompt — fix-ft1-scope-drift

- [`brief.md`](./brief.md) — Goal, Falsification, Inputs, Acceptance, Dependencies, Effort.
- [`prompt.md`](./prompt.md) — The executable RISEN+ReAct tool-instruction prompt.

## Usage

Standalone follow-up prompt. Not yet adopted by a Task; the resolving agent MAY file a Task at dispatch time (preferred) or absorb the work into Task 044 (`improve-maintenance-spec-may-07-2026`) findings list as `F18`.

## Source

Filed in response to [PR #81 review R-2](../../maintenance/pr-81-review.md) which escalated the F.T.1 drift from a Task 048 Assumptions-Log footnote to an audit-graph artefact, per AGENTS.md AG.2.1 + PROMPT.md §1(2): follow-up gaps discovered during execution MUST be filed as new prompts.

## Assumptions Log

- The drift was first observed during [Task 048 scaffolding](../../tasks/048-task-tooling-impl-spec/) when pre-declared prompt slugs (`research-skills-corpus-inspiration-survey`, `research-existing-task-tooling-inventory`, `spec-task-tooling-impl`) were rejected by `validate.py --type-check` despite TASK.md §7.3 prose claiming closure-only enforcement. Workaround applied: leave the lists empty, document in Task 048 readme.
- The decision (loosen linter vs. tighten prose) is itself out of scope for the prompt; the prompt instructs the executor to MAKE the decision and record it. The brief's Acceptance Criterion 1 names the artefact (ADR or research note) but not the choice.
