---
type: prompt
status: active
slug: subjective-quality-evaluation
summary: "Follow-up question on developing standardized human-in-the-loop benchmarking for narrative quality."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: follow-up
prompt_framework: RISEN+ReAct
prompt_target_agent: "external"
prompt_spawned_from_research: github-skillmd-novel-authoring-de-en
---

# Follow-up: Subjective Quality Evaluation
# Framework: RISEN+ReAct

## 1. Context
Multi-agent adversarial loops orchestrated by SKILL.md (an open standard markdown format for agentic instructions) pipelines (e.g., "Harsh Critic" evaluating "Writer") rely on identical underlying neural architectures, potentially reinforcing systemic stylistic biases rather than improving literary merit. Standardized human-in-the-loop benchmarking is missing.

## 2. Objective
You MUST design a standardized human-in-the-loop (HITL) benchmarking protocol to evaluate the subjective literary quality of AI-generated prose without relying solely on LLM-as-a-judge models.

## 3. Method
1. Identify key subjective metrics (e.g., pacing, voice distinctiveness, emotional resonance).
2. Create a standard testing schema to route outputs to human evaluators.
3. Define the minimal viable data-collection schema for incorporating feedback into the next generation loop.


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
