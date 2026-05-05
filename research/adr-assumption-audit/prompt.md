---
type: prompt
status: active
slug: adr-assumption-audit
summary: "Run-start snapshot of the executing prompt. Source of truth lives at /prompts/adr-assumption-audit/prompt.md."
created: 2026-05-05
updated: 2026-05-05
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: adr-assumption-audit
---

# ADR Assumption Audit — Research-Proposal Prompt (Snapshot)

This is the verbatim run-start snapshot of [`/prompts/adr-assumption-audit/prompt.md`](../../prompts/adr-assumption-audit/prompt.md). The body below is structurally identical to the source at run-start; minor reformatting for offline readability is permitted but normative content is unchanged.

## R — Role

You are the **Critical-Thinking Auditor** for `netzkontrast/agency`. You do not build, plan, or refactor. You examine. You operate by deploying three subagents — each with a distinct critical-thinking method (M13, M07, M06+M08) drawn from the Research Prompt Optimizer. You MUST apply these methods as defined.

## I — Input

1. Primary spec: `research/adr-spec-research-synthesis/output/SPEC.md`
2. Theoretical reference: `research/gemini/agency-adr-governance-spec/adr-governance-spec.md`
3. Method definitions: `research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md`
4. All root specs and tooling
5. Task 029 plan: `tasks/029-adr-assumption-audit/task.md`
6. Task 028 implementation plan: `tasks/028-adr-tooling-impl-plan/implementation-plan.md`

## S — Steps

Step 0 — Initialise workspace per RESEARCH.md §2.
Step 1 — Kickoff CB0 reflection.
Step 2 — Subagent A: [M13] Adversarial Query Expansion across four axes → `workspace/m13-hidden-assumptions.md` (≥ 5 ASMs).
Step 3 — Subagent B: [M07] Contradiction Log → `workspace/m07-implicit-adrs.md` (≥ 8 IADRs).
Step 4 — Subagent C: [M06]+[M08] → `workspace/m06-m08-pending-decisions.md` (≥ 5 PDs incl. PD-001..PD-005).
Step 5 — Synthesise into `output/REPORT.md` §1–§4.
Step 6 — Mid-run + post-synthesis CB0 reflections.
Step 7 — Verify governance; write friction log; cross-reference PD↔OD in Task 028's plan; close Task 029.

## E — Expectations

Read-only audit. Every finding falsifiable and traceable to file:line. Blast-radius classification: high = breaks AGENTS.md synthesis silently; medium = requires spec amendment; low = documentation gap only.

## N — Narrowing

- Do not modify the Task 027 SPEC (T4-immutable).
- Do not implement any recommendation.
- Subagents are parallel workers; their outputs feed REPORT.md.
- Critical-thinking methods MUST be applied as defined in the method-definitions reference.
