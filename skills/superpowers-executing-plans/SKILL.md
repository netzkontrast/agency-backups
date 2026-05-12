---
name: superpowers-executing-plans
description: >-
  Execute bite-sized tasks from a plan with batch checkpoints. Maps to Agency Task layer's ## Plan and ## Todo sections; pairs with superpowers-writing-plans.
skill_kind: discipline
skill_target_agents: [claude-code]
skill_references_skills: [sc-task, sc-implement, superpowers-writing-plans]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-executing-plans (imported from Superpowers v4.0.3)

## What

Imported plan-execution discipline from the Superpowers corpus. Maps directly onto Agency's **Task layer**: each `tasks/<NNN>-<slug>/task.md` has `## Plan` (steps) and `## Todo` (checklist) sections that this skill operationalises.

## When to use

Fire when there is an existing plan to execute (Agency Task `## Plan` section, an external PRD, or a brainstorm/research output). The skill is **not** for ad-hoc work — if there is no plan, run `superpowers-writing-plans` first.

## How to use

1. Read the plan top-to-bottom; identify the smallest executable task.
2. Execute exactly **one task at a time**. Mark it `in_progress` in the Task `## Todo` (via TodoWrite or frontmatter edit).
3. Verify completion (run the test, observe the artefact) **before** marking it `[x]`.
4. After every batch (~3–5 tasks) checkpoint: re-read the plan, confirm tasks still match the intent, adjust if reality drifted.
5. Never batch completions across multiple tasks — mark each one as it lands.

Full behavioural specification at `references/upstream-superpowers-executing-plans.md`.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-executing-plans.md`](./references/upstream-superpowers-executing-plans.md) (Superpowers `skills/executing-plans/SKILL.md` @ SHA `b9e16498`, v4.0.3).
- Triage rationale: [`tasks/092-…/references/triage-notes/superpowers-orchestration-cluster.md`](../../tasks/092-port-skill-corpora-phase-2/references/triage-notes/superpowers-orchestration-cluster.md).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native Task layer + TodoWrite only.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
