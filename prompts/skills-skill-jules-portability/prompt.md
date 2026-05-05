---
type: prompt
status: active
slug: skills-skill-jules-portability
summary: "Research Jules skill/instruction loading to determine if SKILL.md is natively compatible or needs an adapter."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: follow-up
prompt_framework: RISEN
prompt_target_agent: Claude Code
prompt_relates_to_task: ""
prompt_spawned_from_research: skills-skill-architecture
---

# Research: Jules Skill-Loading Convention

## Context

The `skills-skill` architecture must serve skill content to four agents. Claude Code is confirmed compatible (same SKILL.md format). Jules compatibility is unknown. This prompt follows up on R2-Q1 in the Gemini Deep Research prompt.

## Research Question

1. Does Jules support custom instruction files analogous to SKILL.md?
2. If yes: what path, format, trigger?
3. Is the format compatible with SKILL.md (YAML frontmatter + Markdown)?
4. If not: what adapter is needed?

## Required Output

If Jules has no native skill mechanism: document the recommended custom-instruction approach and create `skills/skills-skill/adapters/jules/` with a README explaining the adapter.

If Jules is natively compatible: confirm in `research/skills-skill-architecture/output/SPEC.md` Section 7.1 and update the R6 table.

## Prerequisite

Check Gemini PDF at `research/skills-skill-architecture/workspace/gemini-deep-research.pdf` section R2-Q1 first.


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
