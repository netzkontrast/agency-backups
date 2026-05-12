---
type: index
status: active
slug: novel-architect-canon-status-linter
summary: "Directory index for Task 086 — sub-task of Epic 083. Ships tools/check-canon-status.py at ERROR-tier validating canon-meta.md entries against the Dual-Kernel canon-status hierarchy per Task 076 prose spec."
created: 2026-05-12
updated: 2026-05-12
---

# Task 086 — Canon-Status Linter

**What:** Sub-task of [Epic 083](../083-novel-architect-v120-enforcement-epic/). Ships `tools/check-canon-status.py` at ERROR-tier validating `canon-meta.md` entries (and their references from NCP moment files) against the canon-status hierarchy declared in [Task 076 prose spec](../076-novel-architect-canon-status-schema/): `confirmed > provisional > disputed > uncertain > decanonized`. Catches `disputed` blocking active phases, `decanonized` still referenced from non-archived NCPs, missing `variants:` provenance blocks, and invalid status values.

**Why here:** Per [TASK.md §2](../../TASK.md), every coordination unit lives in `/tasks/<NNN>-<slug>/`. This linter is independent from the worksheet-order + scene-audit pair (Task 085) because its file domain (`canon-meta.md` + NCP references) is different and its lifecycle semantics (status-hierarchy enforcement) shares only the Findings emitter with the other linters.

## Navigation

- [task.md](./task.md) — Sub-task spec: Goal, Context, Plan, Todo, Acceptance, Links.

## Assumptions Log

- (none)
