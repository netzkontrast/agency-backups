---
name: superpowers-brainstorming
description: >-
  Collaborative requirement & design discovery before implementation. Use to reduce ambiguity at the start of a project — pairs with sc-brainstorm and sc-requirements-analyst.
skill_kind: discipline
skill_target_agents: [claude-code]
skill_references_skills: [sc-brainstorm, sc-requirements-analyst]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-brainstorming (imported from Superpowers v4.0.3)

## What

Imported brainstorming discipline from the Superpowers corpus. Focuses on **early ambiguity reduction** — surfacing assumptions, constraints, and unknowns *before* a plan or implementation is written.

## When to use

Fire at the start of a project / feature / refactor when the user's request leaves real questions unanswered. Pairs with `sc-brainstorm` (SuperClaude Socratic discovery) and `sc-requirements-analyst` (PRD authoring); brainstorming is the upstream step that feeds both.

## How to use

1. Restate the user's request in your own words; confirm the restatement.
2. Surface ≥ 3 questions the user has not answered. Prefer questions whose answers change the design.
3. List ≥ 2 assumptions you are about to make if the user does not answer; flag the cost of each.
4. Wait for the user to triage your questions before writing a plan.
5. Output of this phase: a Prompt (`prompts/<slug>/prompt.md`) or a Task draft, never an implementation.

## Relation to Agency native skills

- **`sc-brainstorm`** — broader Socratic discovery during requirements elicitation; superpowers-brainstorming is more narrowly scoped to "what do we not yet know?"
- **`sc-requirements-analyst`** — consumes brainstorm output and produces a PRD with Gherkin acceptance criteria.
- **`superpowers-writing-plans`** — downstream of brainstorming once ambiguity has been resolved.

Full behavioural specification at `references/upstream-superpowers-brainstorming.md`.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-brainstorming.md`](./references/upstream-superpowers-brainstorming.md) (Superpowers `skills/brainstorming/SKILL.md` @ SHA `b9e16498`, v4.0.3).
- Triage rationale: [`tasks/092-…/references/triage-notes/superpowers-brainstorming.md`](../../tasks/092-port-skill-corpora-phase-2/references/triage-notes/superpowers-brainstorming.md).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native tools only.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
