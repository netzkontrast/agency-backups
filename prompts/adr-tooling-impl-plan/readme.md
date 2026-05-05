---
type: index
status: active
slug: adr-tooling-impl-plan-prompt-readme
summary: "Index for prompt adr-tooling-impl-plan — drives Task 027, producing a concrete sequenced implementation plan for the agency-adr CLI tool suite."
created: 2026-05-05
updated: 2026-05-05
---

# Prompt — adr-tooling-impl-plan

- [`prompt.md`](./prompt.md) — The executable task-spec prompt.

## Usage

Execute via Task 027: `tasks/027-adr-tooling-impl-plan/task.md`. Blocked until Task 026 produces `research/adr-spec-research-synthesis/output/SPEC.md`.

## Key Constraints

- No code written here — interface contracts only.
- Reuses `tools/fm/` primitives; does not duplicate them.
- Deliverable: `tasks/027-adr-tooling-impl-plan/implementation-plan.md` §1–§7.
