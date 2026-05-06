---
type: task
status: active
slug: prompt-spec-integration
summary: "Add the missing Gherkin acceptance scenarios to PROMPT.md, mechanize enforcement of the seven engineering principles (P.5.1–P.5.7) where mechanically expressible, add a framework-selection decision tree (P.4.3), and clarify the prompt_spawned_from_research linkage with provider folders."
created: 2026-05-06
updated: 2026-05-06
task_id: "033"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - PROMPT.md
  - tools/check-prompt-self-containedness.py
  - tools/check-prompt-framework-declaration.py
---

# Task 033 — PROMPT.md Spec Integration

## Goal

Bring PROMPT.md to parity with TASK.md in mechanical enforceability and acceptance-test transparency. The Task is `done` when (a) PROMPT.md §6 contains ≥6 Gherkin scenarios covering brief→prompt linkage, task reciprocity, follow-up filing, framework declaration, RFC-2119 keyword usage, and self-containedness; (b) a §4.3 framework-selection decision tree replaces the current 5-line description; (c) a self-containedness pre-commit linter exists; (d) a framework-declaration validator exists; and (e) §6.5 explains how `prompt_spawned_from_research` resolves when the source research lives under a `/research/<provider>/<slug>/` external folder.

## Context

PROMPT.md has zero Gherkin scenarios — a structural anomaly given that TASK.md has 10 and AGENTS.md has 16. Six of the seven prompt-engineering principles (P.5.1–P.5.2, P.5.4–P.5.7) are human-review-only. Framework selection (P.4.3) lists five frameworks but provides no decision criteria; agents authoring prompts default to RISEN+ReAct without rationale. P.6.5 (Backward Link Resolves) does not specify how to handle external-research provider folders introduced by RESEARCH.md §6.

The research-prompt-optimizer skill (`/skills/research-prompt-optimizer/SKILL.md`) embodies the kind of decision-tree + intent-capture pipeline that PROMPT.md §4.3 should reference but does not. It is also the canonical example of a mechanizable "self-containedness" check (Phase 4 reader-test).

## Plan

1. **Phase 1 — Research head.** Subtask `01-research-prompt-engineering-principle-mechanizability` produces a per-principle assessment: which of P.5.1–P.5.7 are mechanically expressible, what tooling each requires, what the false-positive rate is on the existing prompt corpus.
2. **Phase 2 — Tooling.** Subtask `02-tooling-self-containedness-checker` and subtask `03-tooling-framework-declaration-validator` ship mechanical gates for the two principles ranked highest-leverage by subtask 01.
3. **Phase 3 — Spec amendment.** Subtask `04-spec-amendment-prompt-md` adds Gherkin scenarios, the framework decision tree, and the §6.5 provider-folder clarification.
4. **Phase 4 — README sync.** Update README.md §6 if linter table changes.

## Todo

- [ ] 1. Dispatch subtask `01-research-prompt-engineering-principle-mechanizability`.
- [ ] 2. Dispatch subtask `02-tooling-self-containedness-checker` (Phase A).
- [ ] 3. Dispatch subtask `03-tooling-framework-declaration-validator` (Phase A).
- [ ] 4. Dispatch subtask `04-spec-amendment-prompt-md` (Phase B; depends on 01).
- [ ] 5. Run `tools/check-governance.sh`.
- [ ] 6. Update `README.md §6` if needed.
- [ ] 7. Update `tasks/readme.md`.
- [ ] 8. Author `friction-log.md`.
- [ ] 9. Set `task_status: done`.

## Links

- Subtask index: [`subtasks/readme.md`](./subtasks/readme.md)
- Source research (under-cited):
  - [`research/agent-prompt-specs-3-systems-sdd/output/SPEC.md`](../../research/agent-prompt-specs-3-systems-sdd/output/SPEC.md) §A.2 (RFC-2119 + Gherkin contract)
  - [`skills/research-prompt-optimizer/SKILL.md`](../../skills/research-prompt-optimizer/SKILL.md) (Phase 4 reader-test = mechanizable self-containedness check)
- Sibling: [Task 020 — audit-prompt-fm-validate-conformance](../020-audit-prompt-fm-validate-conformance/task.md)
- Governing specs: [`PROMPT.md`](../../PROMPT.md), [`TASK.md`](../../TASK.md) §3.3, [`README.md`](../../README.md) §11.3
