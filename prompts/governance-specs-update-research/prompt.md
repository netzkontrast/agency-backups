---
type: prompt
status: active
slug: governance-specs-update-research
summary: "Research the current tooling and specs to create a detailed update plan for MAINTENANCE.md, PRE_COMMIT.md, and FOLDERS.md."
created: 2026-05-05
updated: 2026-05-05
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: update-governance-specs-from-research
---

# Governance Specs Update Research Prompt

## Framework: RISEN+ReAct

## (R - Role)
You are an expert repository governance engineer. Your task is to analyze the current state of root specifications (`MAINTENANCE.md`, `PRE_COMMIT.md`, `FOLDERS.md`, etc.) and the recently updated tooling ecosystem (e.g., `tools/check-governance.sh`), comparing them to the changes introduced by Task 001.

## (I - Input)
You have full access to the repository, specifically:
- `MAINTENANCE.md`
- `PRE_COMMIT.md`
- `FOLDERS.md`
- `TASK.md`
- `tools/check-governance.sh`
- `tasks/001-refactor-governance-from-specs/task.md` and related context.

## (S - Steps)
Execute a ReAct cycle to gather the required information.
1. Read `tasks/001-refactor-governance-from-specs/task.md` to understand what was done.
2. Review the current contents of `MAINTENANCE.md`, `PRE_COMMIT.md`, `FOLDERS.md`, and `TASK.md`.
3. Explore the `tools/` folder, especially `check-governance.sh` and other governance linting tools to see the current enforced mechanisms.
4. Synthesize the findings into a clear, actionable plan that outlines what needs to be updated in the root specs to align them with the current tooling and repository state.

## (E - Expectations)
Produce a detailed `SPEC.md` document in `/research/governance-specs-update-research/output/`. The document MUST contain:
- A summary of the current gap between the specs and the actual implemented tooling.
- A section-by-section update plan for `MAINTENANCE.md`.
- A section-by-section update plan for `PRE_COMMIT.md`.
- A section-by-section update plan for `FOLDERS.md`.
- Any required changes to other governance specs (like `TASK.md` or `PROMPT.md`) to resolve ambiguities or contradictions.

## (N - Narrowing)
- Do NOT modify the root specifications themselves. Your output is strictly an update plan.
- Use RFC 2119 keywords (`MUST`, `SHOULD`, `MAY`) correctly when formulating recommendations.


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
