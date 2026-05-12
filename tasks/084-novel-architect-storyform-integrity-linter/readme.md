---
type: index
status: active
slug: novel-architect-storyform-integrity-linter
summary: "Directory index for Task 084 — foundation sub-task of Epic 083. Ships tools/novel-architect-checks/ shared library + tools/check-hard-rules.py ERROR-tier linter validating H1-H12 + worksheet_audit body-schema on architecture.yaml. Unblocks Tasks 085, 086, 087."
created: 2026-05-12
updated: 2026-05-12
---

# Task 084 — Storyform Integrity Linter (foundation)

**What:** Foundation sub-task of [Epic 083](../083-novel-architect-v120-enforcement-epic/). Ships the `tools/novel-architect-checks/` shared library (loader, Finding dataclass, Severity enum, JSON-artefact writer) plus the first ERROR-tier consumer `tools/check-hard-rules.py`, validating H1–H12 (Task 073 prose spec) and `worksheet_audit.step_*_set` body-schema (Task 072 schema growth) on `architecture.yaml`. Writes `<workspace>/<slug>/.architecture-validation.json` consumed by Task 087's `render_architecture.py` Phase 2.13 wiring.

**Why here:** Per [TASK.md §2](../../TASK.md), every coordination unit lives in `/tasks/<NNN>-<slug>/`. This task is the foundation of Epic 083's linter cluster — Tasks 085, 086, and 087 all `task_blocked_by: ["084"]` because they import from the shared library bootstrapped here.

## Navigation

- [task.md](./task.md) — Sub-task spec: Goal, Context, Plan, Todo, Acceptance, Links.

## Assumptions Log

- (none)
