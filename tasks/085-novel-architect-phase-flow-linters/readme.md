---
type: index
status: active
slug: novel-architect-phase-flow-linters
summary: "Directory index for Task 085 — sub-task of Epic 083. Ships tools/check-worksheet-order.py + tools/check-scene-audit.py at ERROR-tier, both consuming tools/novel-architect-checks/phase_flow.py structural-walk helper. Validates Phase 2 sub-phase ordering (Task 072 spec) and scene-matrix moment Q1-Q5 completeness (Task 075 spec)."
created: 2026-05-12
updated: 2026-05-12
---

# Task 085 — Phase-Flow Linters

**What:** Sub-task of [Epic 083](../083-novel-architect-v120-enforcement-epic/). Ships two ERROR-tier linters that validate operational sequence over the novel-architect phase + scene-matrix markdown files. `tools/check-worksheet-order.py` enforces Phase 2 sub-phase ordering against Worksheet Steps 0–8 + Validation per [Task 072 prose spec](../072-novel-architect-phase2-worksheet-loop/). `tools/check-scene-audit.py` enforces Q1–Q5 field presence + non-emptiness on every scene-matrix moment per [Task 075 prose spec](../075-novel-architect-scene-level-bridge/). Both linters import a shared `phase_flow.py` helper added to the [Task 084 shared library](../084-novel-architect-storyform-integrity-linter/).

**Why here:** Per [TASK.md §2](../../TASK.md), every coordination unit lives in `/tasks/<NNN>-<slug>/`. The two linters share a structural-walk helper (markdown heading-extraction + structured-block field-presence checking) so they live in the same sub-task; their fixture corpora are independent per the [Epic 083 §1 lumping rationale](../083-novel-architect-v120-enforcement-epic/task.md#sub-tasks-children).

## Navigation

- [task.md](./task.md) — Sub-task spec: Goal, Context, Plan, Todo, Acceptance, Links.

## Assumptions Log

- (none)
