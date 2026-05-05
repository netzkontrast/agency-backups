---
type: index
status: active
slug: adr-assumption-audit-readme
summary: "Index for Task 029 — three parallel subagents (M13, M07, M06+M08) audit hidden assumptions, implicit ADRs, and pending decisions in the ADR governance spec."
created: 2026-05-05
updated: 2026-05-05
---

# Task 029 — ADR Assumption Audit (Critical-Thinking)

- [`task.md`](./task.md) — Goal, Plan, Todo, Links.

## State

`task_status: open`, blocked by Task 027. The three subagents cannot run until the Task 027 SPEC.md exists as their primary input.

## Subagent Map

| Subagent | Method | Output |
|----------|--------|--------|
| A | M13 Adversarial Query Expansion | `m13-hidden-assumptions.md` |
| B | M07 Contradiction Log | `m07-implicit-adrs.md` |
| C | M06 Source Triangulation + M08 WWCMM | `m06-m08-pending-decisions.md` |

## Design Note

The critical-thinking methods used here are drawn verbatim from the Research Prompt Optimizer specification (`research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md`). Subagents are not permitted to modify or abbreviate the method templates — they MUST apply them as defined.
