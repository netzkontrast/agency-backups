---
type: index
status: active
slug: adr-assumption-audit-prompt-readme
summary: "Index for prompt adr-assumption-audit — drives Task 029, deploying three parallel subagents (M13, M07, M06+M08) to audit hidden assumptions, implicit ADRs, and pending decisions."
created: 2026-05-05
updated: 2026-05-05
---

# Prompt — adr-assumption-audit

- [`brief.md`](./brief.md) — Raw user request and context.
- [`prompt.md`](./prompt.md) — The executable research-proposal prompt.

## Usage

Execute via Task 029: `tasks/029-adr-assumption-audit/task.md`. Blocked until Task 027 produces `research/adr-spec-research-synthesis/output/SPEC.md`.

## Key Constraints

- Three parallel subagents: A (M13), B (M07), C (M06+M08).
- Methods applied verbatim from `research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md`.
- Read-only audit — no modifications to Task 027 output.
- Feeds pending decisions back into Task 028 open-decisions list.
