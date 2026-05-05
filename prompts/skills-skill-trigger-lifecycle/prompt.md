---
type: prompt
status: active
slug: skills-skill-trigger-lifecycle
summary: "Research how claude.ai's native skill-trigger mechanism selects and activates skills for a given user message."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: follow-up
prompt_framework: RISEN
prompt_target_agent: Claude Code
prompt_relates_to_task: ""
prompt_spawned_from_research: skills-skill-architecture
---

# Research: claude.ai Skill Trigger Lifecycle

## Context

The `skills-skill` architecture (see `research/skills-skill-architecture/output/SPEC.md`) contains an UNCERTAIN marker (U3) about how claude.ai's host selects which installed skill to activate. This question is partially covered by the Gemini Deep Research prompt at `research/skills-skill-architecture/output/gemini-prompt.md` (question R1-Q2).

This follow-up prompt is to be executed AFTER the Gemini PDF is available, if R1-Q2 in the PDF does not fully resolve U3.

## Research Question

How does claude.ai's native skill-trigger mechanism work?

1. Does the host use the `description` field from SKILL.md frontmatter for matching? What algorithm?
2. Does the host pass the raw user message or a pre-processed intent signal to the activated skill body?
3. Can a skill's description be written as a catch-all so it activates for any user message?
4. When only one skill is installed (the stub), does the host always activate it?

## Required Output

Update `research/skills-skill-architecture/output/SPEC.md` sections 2.3 (Activation Trigger) and 4.1 (Two-Tier Routing Model) with normative RFC-2119 language, replacing the UNCERTAIN (U3) and UNCERTAIN (U5) markers.

## Prerequisite

Gemini PDF at `research/skills-skill-architecture/workspace/gemini-deep-research.pdf` should be consulted first. Only run this prompt if R1-Q2 in that PDF is incomplete.


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
