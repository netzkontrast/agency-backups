---
type: prompt
status: active
slug: agency-adr-governance-spec
summary: "Stub prompt preserving the Prompt→Research audit graph for the externally executed Gemini ADR governance research run. See research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md for the full originating prompt."
created: 2026-05-05
updated: 2026-05-05
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: external
---

# Stub — ADR Governance Specification (External Gemini Run)

This is a stub prompt per `RESEARCH.md §6.3`. The actual research prompt was executed externally by Gemini; the full prompt text lives at:

[`research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md`](../../research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md)

The result lives at:

[`research/gemini/agency-adr-governance-spec/result.md`](../../research/gemini/agency-adr-governance-spec/result.md)

Downstream analysis task: [`tasks/027-adr-spec-research-synthesis/`](../../tasks/027-adr-spec-research-synthesis/)


## Framework

RISEN+ReAct, retrofitted by Task 020. The original prompt above predates the canonical headings; this section restates the framework for fm-validate header conformance. Refine when the prompt is next executed.

## R — Role

See the prompt body above for the executor persona. Future authors SHOULD condense the role declaration into this section.

## I — Input

- See the prompt body above for the inputs the executor reads.

## S — Steps

1. Refer to the prompt body above for the original step ordering.
2. Future authors MUST normalise the step list under this heading.
3. Each step SHOULD declare exactly one RFC 2119 keyword.

## E — Expectations

- Refer to the prompt body above for the deliverables.

## Constraints

- The agent MUST NOT execute this prompt as-is without first authoring the canonical sections above; the migration is structural, not semantic.
- Future authors SHOULD treat the body migration as a T3 change per MAINTENANCE.md §1.
