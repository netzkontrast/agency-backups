---
name: superpowers-dispatching-parallel-agents
description: >-
  Execute independent tasks via parallel subagent dispatch. Use when work can be partitioned into non-overlapping subtasks; binds Agency's Agent tool with parallel tool-use.
skill_kind: orchestrator
skill_target_agents: [claude-code]
skill_references_skills: [sc-task]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-dispatching-parallel-agents (imported from Superpowers v4.0.3)

## What

Imported parallel-subagent orchestration pattern from the Superpowers corpus. The upstream skill described dispatching "fresh Claude sessions"; Agency expresses the same pattern via the **`Agent` tool with parallel tool-use** — multiple `Agent` calls in a single message run concurrently with isolated context windows.

## When to use

Fire when the work can be partitioned into ≥ 2 **non-overlapping** subtasks whose outputs can be merged after independent execution. Classic cases: parallel research on different subtrees, per-file linting / analysis, multi-source triage (the Task 092 ST-1 pattern).

## How to use

1. Verify the subtasks are truly independent — if a downstream task needs an upstream output, sequence them instead.
2. In a single assistant message, emit multiple `Agent` tool-use blocks. Each block gets its own `description`, `subagent_type` (often `Explore`), and self-contained `prompt`.
3. Each subagent returns one consolidated result. Synthesise the results in the main agent.
4. Set `run_in_background: true` when you have unrelated foreground work to do; otherwise default to foreground for blocking dispatch.

## Relation to Agency native skills

- **`sc-task`** — coordinate the merge of subagent outputs into a single Task.
- **Agency `Agent` tool** — the primitive this skill wraps. The body of each subagent's prompt MUST be self-contained (no prior conversation context).

Full behavioural specification + worked examples at `references/upstream-superpowers-dispatching-parallel-agents.md`.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-dispatching-parallel-agents.md`](./references/upstream-superpowers-dispatching-parallel-agents.md) (Superpowers `skills/dispatching-parallel-agents/SKILL.md` @ SHA `b9e16498`, v4.0.3).
- Triage rationale: [`tasks/092-…/references/triage-notes/superpowers-orchestration-cluster.md`](../../tasks/092-port-skill-corpora-phase-2/references/triage-notes/superpowers-orchestration-cluster.md).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native `Agent` tool primitive only.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
