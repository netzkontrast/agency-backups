---
type: task
status: active
slug: frustrated-spec-integration
summary: "Resolve the FRUSTRATED.md §28 vs PRE_COMMIT.md §2 contradiction (reciprocal with Task 036), justify the FL0-mandatory rule, mechanically enforce the FL declaration at commit time, and add ≥4 Gherkin acceptance scenarios."
created: 2026-05-06
updated: 2026-05-06
task_id: "037"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - FRUSTRATED.md
  - tools/check-fl-declaration.py
---

# Task 037 — FRUSTRATED.md Spec Integration

## Goal

Make FRUSTRATED.md mechanically gating, harmonise it with PRE_COMMIT.md, and add Gherkin-anchored acceptance criteria. The Task is `done` when (a) the §28 readme-cadence wording is reconciled with PRE_COMMIT.md §2 (output of joint subtask with Task 036), (b) FL0–FL3 declarations are mechanically validated on commit by `tools/check-fl-declaration.py`, (c) §FL.0 carries a research-backed rationale for why FL0 entries are still mandatory, (d) ≥4 Gherkin scenarios cover the closing-run, FL.Special bloat trigger, FL.Log.1 (research) vs FL.Log.2 (standard) surfaces, and missing-log rejection.

## Context

FRUSTRATED.md governance debt:

- **Contradiction with PRE_COMMIT.md §2** (see Task 036 context).
- **FL0 rationale** — "mandatory even when nothing went wrong" is asserted, never justified. Agents experience FL0 as bureaucracy; a research-backed answer to "what does an FL0 entry feed upstream?" closes the legitimacy gap.
- **No mechanical enforcement** — TASK.md §313 enforces friction-log existence for closed tasks, but the *FL declaration substance* (a line beginning `Highest Frustration Level: FL[0-3]`) is never parsed or validated.
- **No Gherkin scenarios** — like PROMPT.md, RESEARCH.md, FOLDERS.md, FRUSTRATED.md is Gherkin-free.

The §28 reconciliation is intentionally co-owned with Task 036 — both tasks must converge on the same wording. The shared subtask `01-research-fl0-value-justification` outputs a single research SPEC consumed by both.

## Plan

1. **Phase 1 — Research head.** Subtask `01-research-fl0-value-justification` analyses every closed-task `friction-log.md` for FL0 vs FL1+ distinguishing signal and produces a normative justification.
2. **Phase 2 — Tooling.** Subtask `02-tooling-fl-declaration-linter` parses friction-log.md and PR descriptions for the canonical declaration line; rejects malformed/missing.
3. **Phase 3 — Spec amendment.** Subtask `03-spec-amendment-frustrated-md`: §28 reconciled wording (jointly with Task 036's spec edit), FL0 rationale, §FL.Log enforcement reference, Gherkin scenarios.

## Todo

- [ ] 1. Dispatch subtask `01-research-fl0-value-justification`.
- [ ] 2. Dispatch subtask `02-tooling-fl-declaration-linter` (Phase A).
- [ ] 3. Dispatch subtask `03-spec-amendment-frustrated-md` (Phase B; coordinated with Task 036 subtask 04).
- [ ] 4. Run `tools/check-governance.sh`.
- [ ] 5. Update `README.md §6` per R.7.
- [ ] 6. Update `tasks/readme.md`.
- [ ] 7. Author `friction-log.md`.
- [ ] 8. Set `task_status: done`.

## Links

- Subtask index: [`subtasks/readme.md`](./subtasks/readme.md)
- Co-touched: [Task 036 — PRE_COMMIT.md spec integration](../036-pre-commit-spec-integration/task.md) (the §28 reconciliation is reciprocal).
- Governing specs: [`FRUSTRATED.md`](../../FRUSTRATED.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md) §2, [`TASK.md`](../../TASK.md) §313, [`README.md`](../../README.md) §11.3
