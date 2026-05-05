---
type: prompt
status: active
slug: mega-context-limit-management
summary: "Follow-up question on empirical testing of sliding window truncation vs infinite context for 100k-word manuscripts."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: follow-up
prompt_framework: RISEN+ReAct
prompt_target_agent: "external"
prompt_spawned_from_research: github-skillmd-novel-authoring-de-en
---

# Follow-up: Mega-Context Limit Management
# Framework: RISEN+ReAct

## 1. Context
The progressive disclosure model (often orchestrated using SKILL.md, an open standard markdown format for agentic instructions) manages metadata efficiently, but the handling of a completed, continuous 100,000-word manuscript is unresolved. Some tools utilize a truncation marker to pass only the last 1,000 words. It is unknown whether this damages long-term narrative foreshadowing and character arcs.

## 2. Objective
You MUST design and execute a benchmark to evaluate whether localized "sliding window" context truncation causes significant narrative degradation compared to theoretically infinite context windows.

## 3. Method
1. Define a set of character arcs and foreshadowing events in a massive manuscript.
2. Execute drafting scenarios using both a 1000-word truncation and full-document injection.
3. Compare continuity and narrative consistency.


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
