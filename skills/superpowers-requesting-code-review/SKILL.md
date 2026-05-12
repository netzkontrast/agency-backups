---
name: superpowers-requesting-code-review
description: >-
  Dispatch a code-reviewer subagent after task completion. Wraps Agency's built-in code-reviewer agent type with the Superpowers calling convention.
skill_kind: orchestrator
skill_target_agents: [claude-code]
skill_references_skills: [superpowers-code-reviewer, superpowers-receiving-code-review]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-requesting-code-review (imported from Superpowers v4.0.3)

## What

Imported review-dispatch pattern from the Superpowers corpus. Wraps Agency's built-in `code-reviewer` agent type with the Superpowers calling convention: after task completion, dispatch a reviewer subagent that has no execution context — only the diff and the plan.

## When to use

Fire after every substantive task completion before opening a PR. Especially important for: schema changes, security-sensitive code, architecture refactors, anything the user flagged as "review carefully".

## How to use

1. Confirm the task is functionally complete (tests pass, governance clean).
2. Invoke `Agent({subagent_type: "code-reviewer", description: "Review <task>", prompt: <self-contained context>})`.
3. The prompt MUST be self-contained: include the diff (or the file paths), the plan / specification it implements, and any specific risk areas to inspect.
4. Read the reviewer's verdict; address blocking items via `superpowers-receiving-code-review` discipline (technical verification before agreeing).

## Relation to Agency native primitives

Agency's `Agent` tool exposes a built-in `code-reviewer` `subagent_type`. This skill is the **prompt template** for invoking it — not a competing implementation. The downstream skill `superpowers-code-reviewer` provides the reviewer-side discipline.

Full behavioural specification at `references/upstream-superpowers-requesting-code-review.md`.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-requesting-code-review.md`](./references/upstream-superpowers-requesting-code-review.md) (Superpowers `skills/requesting-code-review/SKILL.md` @ SHA `b9e16498`, v4.0.3).
- Triage rationale: [`tasks/092-…/references/triage-notes/superpowers-orchestration-cluster.md`](../../tasks/092-port-skill-corpora-phase-2/references/triage-notes/superpowers-orchestration-cluster.md).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native `Agent` tool with `code-reviewer` subagent type.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
