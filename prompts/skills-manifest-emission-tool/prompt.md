---
type: prompt
status: active
slug: skills-manifest-emission-tool
summary: "Specify the contract, JSON Schema, exit-code surface, and integration points of tools/skills-index.py (emit/get/verify)."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: follow-up
prompt_framework: RISEN
prompt_target_agent: "any"
prompt_relates_to_task: ""
prompt_spawned_from_research: skills-navigation-bootstrap
---

# Skills Manifest Emission Tool — Follow-up Research

## Framework: RISEN

## Role

You are a CLI designer with experience in deterministic tools that participate in a pre-commit gate.

## Instructions

Given the manifest emitter sketch in `research/skills-navigation-bootstrap/output/SPEC.md` §6, produce a complete contract: JSON Schema for the manifest, exit-code surface for each verb, and integration points.

## Steps

1. **Read** `research/skills-navigation-bootstrap/output/SPEC.md` §6.
2. **Author** the JSON Schema for `<runtime-skills-dir>/.index.json`. Re-use vocabulary from the `skill_*` namespace once `skills-namespace-ontology` lands.
3. **Specify** exit codes for `emit`, `get`, `verify` — including: empty repo, missing skill, malformed YAML, schema-version mismatch, partial section-name match.
4. **Map** integration points: how `skills/skills-skill-bootstrap/sync.sh` calls `emit` post-sync; how `verify.sh` calls `verify`; how `tools/check-governance.sh` invokes `verify` in the pre-commit gate.
5. **Specify** the matching rule for `get --section <name>` (case-insensitive, trim, hyphen/space-equivalent, etc.).
6. **Produce** `output/SPEC.md` with the schema, exit codes, integration map, and Gherkin scenarios.

## End Goal

A research workspace whose output is the implementation contract for **Task 010** (`skills-frontmatter-index-suite`).

## Narrowing / Constraints

- MUST adhere to RFC 2119.
- MUST NOT implement the tool — only specify its contract.
- MUST cite the `skill_*` vocabulary by reference; do not duplicate it.
- SHOULD respect the ≤ 8 KB / 14-skill manifest size budget from `skills-navigation-bootstrap/output/SPEC.md` §6.1.


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
