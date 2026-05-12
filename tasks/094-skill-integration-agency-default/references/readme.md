---
type: index
status: active
slug: task-094-references
summary: "References for Task 094 — holds the source planning artifact (Plan-mode output) that this Epic spec is built from."
created: 2026-05-12
updated: 2026-05-12
---

# Task 094 — References

**What:** Source-of-truth attachments for the Epic spec. Currently a single artifact:

- [`source-plan.md`](./source-plan.md) — verbatim mirror of the Claude-Code Plan-mode planning artifact. The user explicitly asked for the plan to ship with the Epic so the design rationale + user-locked decisions stay attached to the Task folder, not just on the Plan-mode harness's `/root/.claude/plans/` path.

**Why here:** Per Agency's convention, every Epic that comes out of a structured planning session SHOULD cite its source plan. The plan covers exploration findings, three integration-pattern alternatives, the design rationale for choosing event-driven hooks over per-skill or per-kind hooks, and the user-locked decisions captured via `AskUserQuestion` in Plan mode.

## Assumptions Log

- The plan was authored at `/root/.claude/plans/now-please-look-at-greedy-cascade.md` in Claude-Code session `01WBrHNUZUEoew9PE9A7SguS` on 2026-05-12. The mirror in this folder is the **canonical record**; the original `/root/.claude/plans/` path is a per-session ephemeral location.
- The plan content is **not** re-edited as the Epic progresses — it represents the planning state at Epic spec authoring time. If a subsequent subtask deviates from the plan (e.g. ST-2 needs to defer a feature), the deviation is recorded in `../friction-log.md`, not in the plan mirror.
