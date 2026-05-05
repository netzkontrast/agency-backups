---
type: prompt
status: active
slug: context-pruner-differentiation
summary: "Follow-up research prompt: Investigate how a Context-Pruner can differentiate noise from critical context without invoking an LLM."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: follow-up
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_spawned_from_research: "token-efficiency-tool-suite"
---

# Follow-up: Context-Pruner Differentiation

Research how context pruning algorithms distinguish between noise and critical context structurally, without relying on secondary LLM calls that consume additional tokens.


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
