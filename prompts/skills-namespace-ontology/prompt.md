---
type: prompt
status: active
slug: skills-namespace-ontology
summary: "Define the exact value vocabulary, reciprocity rule, and migration path for the skill_* L2 namespace proposed by skills-navigation-bootstrap."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: follow-up
prompt_framework: RISEN
prompt_target_agent: "any"
prompt_relates_to_task: ""
prompt_spawned_from_research: skills-navigation-bootstrap
---

# Skills Namespace Ontology — Follow-up Research

## Framework: RISEN

## Role

You are an ontology designer with deep familiarity with the `TASK.md` §3 frontmatter ontology and Anthropic's `SKILL.md` schema.

## Instructions

Given the `skill_*` L2 namespace proposed in `research/skills-navigation-bootstrap/output/SPEC.md` §3.2, ratify a complete, machine-validatable ontology and produce a migration plan for the 14 existing skill bodies.

## Steps

1. **Read** `research/skills-navigation-bootstrap/output/SPEC.md` §3 and Annex A §A.4-§A.6.
2. **Enumerate** the full value vocabulary for `skill_kind` and `skill_tier`. Audit the 14 existing skills (`skills/*/SKILL.md`) and check that every existing skill maps cleanly to one value of each.
3. **Specify** the reciprocity rule for `skill_uses` ↔ `skill_complements`. Decide: warning (current draft) vs. error. Justify.
4. **Draft** a migration plan for the 14 existing skills. Include: (a) which `metadata.*` keys are deprecated by which `skill_*` keys; (b) which prose-encoded trigger phrases need lifting into `skill_triggers`; (c) order of migration to minimise PR churn.
5. **Produce** `output/SPEC.md` containing the ratified ontology table, the reciprocity rule with rationale, and the migration plan.

## End Goal

A research workspace whose output is consumed by:

- Task 009 — `SKILLS.md` ratification (Annex A in `skills-navigation-bootstrap`).
- Task 011 — `skills-frontmatter.schema.json` authoring.

## Narrowing / Constraints

- MUST adhere to RFC 2119.
- MUST NOT modify any `SKILL.md` body in this run — migration is *planned*, not executed.
- MUST flat-list all proposed values; no nested YAML.
- SHOULD reuse existing pattern from `task_*`, `prompt_*`, `research_*` namespaces wherever possible.


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
