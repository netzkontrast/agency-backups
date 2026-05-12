---
type: index
status: active
slug: novel-architect-mif-l3-backport
summary: "Directory index for Task 088 — sub-task of Epic 083. Retroactively applies subset MIF Level 3 frontmatter (cognitive_type, decay_rate, derivation_chain) to historical entries in skills/novel-architect/references/learnings.md per Task 077 prose spec; T4 archived entries receive metadata-only edits per MAINTENANCE.md §1.0.1."
created: 2026-05-12
updated: 2026-05-12
---

# Task 088 — MIF Level 3 Backport (references/learnings.md)

**What:** Sub-task of [Epic 083](../083-novel-architect-v120-enforcement-epic/). Closes the deferred MIF Level 1/2 → 3 backport flagged by [Task 070 friction log §"Sub-task summary"](../070-novel-architect-v110-epic/friction-log.md#sub-task-summary). Applies the subset MIF L3 schema from [`skills/novel-architect/schemas/mif-level3.yaml`](../../skills/novel-architect/schemas/mif-level3.yaml) retroactively to every entry in `references/learnings.md`. Archived entries get frontmatter-only edits per the [MAINTENANCE.md §1.0.1](../../MAINTENANCE.md#101-closed-research-t1t2-repair-allowance-task-059) closed-research T1/T2 repair allowance.

**Why here:** Per [TASK.md §2](../../TASK.md), every coordination unit lives in `/tasks/<NNN>-<slug>/`. This Task is independent of the Epic 083 linter cluster — it touches `skills/novel-architect/references/learnings.md` exclusively and shares no infrastructure with Tasks 084-087. The independence is captured in its `task_blocked_by: ["083"]` (Epic-only, no upstream sub-task gate).

## Navigation

- [task.md](./task.md) — Sub-task spec: Goal, Context, Plan, Todo, Acceptance, Links.
- `migration-audit.md` — *To be created during this Task's working session*. Enumerates every migrated entry with its assigned cognitive_type, decay_rate, and derivation_chain source. Reviewer-facing artefact.

## Assumptions Log

- (none)
