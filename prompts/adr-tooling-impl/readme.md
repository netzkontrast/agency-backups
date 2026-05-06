---
type: index
status: active
slug: adr-tooling-impl-prompt-readme
summary: "Index for prompt adr-tooling-impl — task-spec prompt that drives Task 031 (implementation successor to Task 028). Reverse-engineered from the build contract in tasks/028-adr-tooling-impl-plan/implementation-plan.md."
created: 2026-05-06
updated: 2026-05-06
---

# Prompt — adr-tooling-impl

- [`brief.md`](./brief.md) — Raw user request and context.
- [`prompt.md`](./prompt.md) — The executable task-spec prompt.

## Usage

Execute via [Task 031](../../tasks/031-adr-tooling-impl/task.md). The prompt presupposes the predecessor's build contract at [`../../tasks/028-adr-tooling-impl-plan/implementation-plan.md`](../../tasks/028-adr-tooling-impl-plan/implementation-plan.md) and the ADR governance spec at [`../../research/adr-spec-research-synthesis/output/SPEC.md`](../../research/adr-spec-research-synthesis/output/SPEC.md).

## Key Constraints

- Implementation only — does not modify the spec or the build contract.
- Reuses `tools/fm/_core.py` primitives (parsing, diagnostics, file locking, ontology loading).
- Determinism: synthesised guarded section MUST be byte-stable across runs (ADR.A.3.6).
- Spec citations: every diagnostic and every test docstring MUST cite the `ADR.A.<aspect>.<stmt>` anchor it enforces.
