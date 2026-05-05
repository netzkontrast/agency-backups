---
type: index
status: active
slug: adr-assumption-audit-prompt-readme
summary: "Index for prompt adr-assumption-audit — drives Task 028, deploying three parallel subagents (M13, M07, M06+M08) to audit hidden assumptions, implicit ADRs, and pending decisions."
created: 2026-05-05
updated: 2026-05-05
---

# Prompt — adr-assumption-audit

- [`brief.md`](./brief.md) — Raw user request and context.
- [`prompt.md`](./prompt.md) — The executable research-proposal prompt.

## Usage

Execute via Task 028: `tasks/028-adr-assumption-audit/task.md`. Blocked until Task 026 produces `research/adr-spec-research-synthesis/output/SPEC.md`.

## Key Constraints

- Three parallel subagents: A (M13), B (M07), C (M06+M08).
- Methods applied verbatim from `research/gemini/slug/research-prompt_agency-adr-governance-spec.md`.
- Read-only audit — no modifications to Task 026 output.
- Feeds pending decisions back into Task 027 open-decisions list.
