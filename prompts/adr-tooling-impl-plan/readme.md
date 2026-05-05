---
type: index
status: active
slug: adr-tooling-impl-plan-prompt-readme
summary: "Index for prompt adr-tooling-impl-plan — drives Task 028, producing a concrete sequenced implementation plan for the agency-adr CLI tool suite."
created: 2026-05-05
updated: 2026-05-05
---

# Prompt — adr-tooling-impl-plan

- [`brief.md`](./brief.md) — Raw user request and context.
- [`prompt.md`](./prompt.md) — The executable task-spec prompt.

## Usage

Execute via Task 028: `tasks/028-adr-tooling-impl-plan/task.md`. Blocked until Task 027 produces `research/adr-spec-research-synthesis/output/SPEC.md`.

## Key Constraints

- No code written here — interface contracts only.
- Reuses `tools/fm/` primitives; does not duplicate them.
- Deliverable: `tasks/028-adr-tooling-impl-plan/implementation-plan.md` §1–§7.
