---
type: index
status: active
slug: adr-tooling-impl-plan-readme
summary: "Index for Task 028 — design the concrete implementation plan for the agency-adr CLI tool suite from the spec produced by Task 027."
created: 2026-05-05
updated: 2026-05-05
---

# Task 028 — ADR Tooling Implementation Plan

- [`task.md`](./task.md) — Goal, Plan, Todo, Links.
- [`implementation-plan.md`](./implementation-plan.md) — §1–§7 build plan for `agency-adr`.
- [`friction-log.md`](./friction-log.md) — Closure friction log (FL1).

## State

`task_status: done`. Task 027 (the blocker) closed in the same branch. The implementation plan is the build contract for the implementing-agent Task that succeeds Task 028.

## Artefacts

| Artefact | Status | Path |
|----------|--------|------|
| Implementation plan | done | [`./implementation-plan.md`](./implementation-plan.md) |
| Executing prompt | verified complete | [`../../prompts/adr-tooling-impl-plan/prompt.md`](../../prompts/adr-tooling-impl-plan/prompt.md) |
| Friction log | done | [`./friction-log.md`](./friction-log.md) |

## Scope Boundary

This task produces a **plan**, not an implementation. The plan artifact is what an implementing agent (or human) executes. No code under `tools/adr/`, no test files under `tests/adr/`, and no `.github/workflows/adr-validate.yml` were authored here — those are the responsibility of the successor implementation Task.
