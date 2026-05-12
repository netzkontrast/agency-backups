---
name: sc-self-review
description: >-
  Post-implementation validation and reflexion partner. Use immediately after an implementation wave to confirm the result is production-ready and capture lessons learned.
skill_kind: specialist
skill_target_agents: [claude-code]
skill_references_skills: [sc-test]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-self-review — Self Review agent (imported from SuperClaude v4.3.0)

## What

Imported Self Review agent persona from SuperClaude_Framework. Invoked **after** an implementation wave to verify production-readiness and capture lessons learned. Distinct from `sc-quality-engineer` (which audits *before* shipping) — `sc-self-review` is the closing gate.

## When to use

Use when an implementation is "done" and you need an evidence-based check before opening a PR. The four mandatory self-check questions live in `references/upstream-sc-self-review.md`.

## How to use

1. Treat the persona as a sub-agent: invoke via the `Agent` tool with this skill's body as the system prompt.
2. Run the four self-check questions in order; do not skip any.
3. Confirm the test suite ran clean (delegate to `sc-test` if needed).
4. Record the friction log entry per AGENTS.md FR rules.

Full behavioural specification at `references/upstream-sc-self-review.md`.

## References

- Upstream verbatim mirror: [`references/upstream-sc-self-review.md`](./references/upstream-sc-self-review.md) (SuperClaude_Framework `src/superclaude/agents/self-review.md` @ SHA `22ad3f48`, v4.3.0).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native tools only.
- Known limitation: one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
