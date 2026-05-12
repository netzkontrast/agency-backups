---
name: superpowers-writing-plans
description: >-
  Create bite-sized task implementation plans with exact code references. Maps to Agency Task ## Plan section and pairs with sc-workflow for PRD → plan translation.
skill_kind: discipline
skill_target_agents: [claude-code]
skill_references_skills: [sc-workflow, sc-task, superpowers-executing-plans]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-writing-plans (imported from Superpowers v4.0.3)

## What

Imported plan-authoring discipline from the Superpowers corpus. Produces **bite-sized** plans — every task small enough to verify atomically, every reference precise enough that an executor agent can act without re-reading the parent doc.

## When to use

Fire after `superpowers-brainstorming` / `sc-brainstorm` has reduced ambiguity, and before `superpowers-executing-plans` starts work. Pairs with Agency's `sc-workflow` (PRD → workflow) — `superpowers-writing-plans` is the granular task-list authoring step downstream of `sc-workflow`'s structural pass.

## How to use

1. State the plan's goal in one sentence at the top.
2. Break into tasks each ≤ 1 hour of agent-time. If a task is bigger, split it.
3. Every task MUST cite: the file path(s) it touches, the change in one sentence, and a verification step.
4. List tasks in execution order; mark dependencies explicitly.
5. Land the plan in `tasks/<NNN>-<slug>/task.md` `## Plan` (with `## Todo` for the checklist).

## Relation to Agency native skills

- **`sc-workflow`** — translates a PRD or requirements document into a workflow scaffold (PRD → structure). `superpowers-writing-plans` lives one layer deeper (structure → granular tasks).
- **`sc-task`** — the layer that **holds** the plan once it is written.
- **`superpowers-executing-plans`** — the downstream consumer.

Full behavioural specification at `references/upstream-superpowers-writing-plans.md`.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-writing-plans.md`](./references/upstream-superpowers-writing-plans.md) (Superpowers `skills/writing-plans/SKILL.md` @ SHA `b9e16498`, v4.0.3).
- Triage rationale: [`tasks/092-…/references/triage-notes/superpowers-orchestration-cluster.md`](../../tasks/092-port-skill-corpora-phase-2/references/triage-notes/superpowers-orchestration-cluster.md).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native Task layer + TodoWrite.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
