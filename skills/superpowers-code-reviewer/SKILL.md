---
name: superpowers-code-reviewer
description: >-
  Subagent template for code review against plan & standards. Use as the prompt body when dispatching Agency's built-in code-reviewer agent type via Agent tool.
skill_kind: agent-template
skill_target_agents: [claude-code]
skill_references_skills: [superpowers-requesting-code-review, superpowers-receiving-code-review]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-code-reviewer (imported from Superpowers v4.0.3)

## What

Imported code-reviewer agent template from the Superpowers corpus. Agency already exposes a **built-in `code-reviewer` agent type** (see the top of every agent's system prompt). This skill is the **prompt template** for invoking that built-in — not a competing reviewer implementation.

## When to use

Fire when the main agent dispatches a code review via `Agent({subagent_type: "code-reviewer", ...})`. The body of this SKILL.md is what becomes the `prompt` argument (or part of it).

## How to use (as the dispatcher)

```
Agent({
  subagent_type: "code-reviewer",
  description: "Review <task>",
  prompt: <self-contained context: diff + plan + risk areas>
})
```

The reviewer has no execution context — that is the point. The prompt MUST be self-contained: include the diff (or file paths), the plan / spec it implements, and any specific risk areas to inspect.

## How to use (as the reviewer)

When this skill is loaded as the reviewer's system prompt:

1. Read the diff against the plan / spec. Do not write code; do not run commands.
2. Identify **blocking** issues (correctness, security, governance violations) — these MUST be fixed before merge.
3. Identify **advisory** issues (style, minor refactors) — these MAY be fixed pre-merge or deferred.
4. Verify the AC anchors cited in the PR body match the diff.
5. Return a structured verdict: Verified / Blocking / Advisory sections.

## Relation to Agency native primitives

- **Agency's built-in `code-reviewer` agent type** — the underlying mechanism. This skill names the prompt; the harness wires it up.
- **`superpowers-requesting-code-review`** — caller-side discipline for dispatching this skill.
- **`superpowers-receiving-code-review`** — discipline for reading the verdict without performative compliance.

Full behavioural specification at `references/upstream-superpowers-code-reviewer.md`.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-code-reviewer.md`](./references/upstream-superpowers-code-reviewer.md) (Superpowers `agents/code-reviewer.md` @ SHA `b9e16498`, v4.0.3).
- Triage rationale: [`tasks/092-…/references/triage-notes/superpowers-orchestration-cluster.md`](../../tasks/092-port-skill-corpora-phase-2/references/triage-notes/superpowers-orchestration-cluster.md).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code` (as both dispatcher and reviewer).
- No MCP bindings; Agency-native `Agent` tool only.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
