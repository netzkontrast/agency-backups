---
name: superpowers-subagent-driven-development
description: >-
  Two-stage subagent review workflow — dispatch a fresh subagent per task, then a second reviewer subagent. Use to maintain quality across long-horizon development.
skill_kind: orchestrator
skill_target_agents: [claude-code]
skill_references_skills: [superpowers-code-reviewer, sc-task, superpowers-dispatching-parallel-agents]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-subagent-driven-development (imported from Superpowers v4.0.3)

## What

Imported subagent-driven-development workflow from the Superpowers corpus. Two-stage pattern: (1) dispatch a fresh subagent to execute one task with clean context; (2) dispatch a **reviewer** subagent to audit the work before merging. The discipline keeps the main agent's context window healthy and forces a peer-review checkpoint.

## When to use

Fire on long-horizon multi-task work where context budget is a real constraint, or where each task benefits from independent review. Pairs with Agency's Task layer (each `tasks/<NNN>-<slug>/` becomes one subagent invocation).

## How to use

1. Identify the task boundary — typically one Task or one subtask file.
2. **Stage 1 (execute):** dispatch a fresh subagent via `Agent` tool with the task body as `prompt`. Use `subagent_type: claude` (or a specialist). The subagent works in its own context.
3. **Stage 2 (review):** dispatch a reviewer subagent (use `superpowers-code-reviewer` skill body as prompt) over the Stage-1 output. The reviewer has no execution context — that's the point.
4. Synthesise both outputs in the main agent; address blocking review items before merging.

Full behavioural specification + two-stage review checklist at `references/upstream-superpowers-subagent-driven-development.md`.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-subagent-driven-development.md`](./references/upstream-superpowers-subagent-driven-development.md) (Superpowers `skills/subagent-driven-development/SKILL.md` @ SHA `b9e16498`, v4.0.3).
- Triage rationale: [`tasks/092-…/references/triage-notes/superpowers-orchestration-cluster.md`](../../tasks/092-port-skill-corpora-phase-2/references/triage-notes/superpowers-orchestration-cluster.md).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native `Agent` tool only.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
