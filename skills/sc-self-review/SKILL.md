---
name: sc-self-review
description: >-
  Post-implementation validation and reflexion partner. Use when the user invokes @self-review or asks to confirm an implementation wave is production-ready, capture residual risks, and record reflexion patterns for future runs.
skill_kind: persona
skill_target_agents: [claude-code]
skill_references_skills: [sc-test]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-self-review — Self Review Agent (imported from SuperClaude v4.3.0)

## What

Imported `@self-review` persona from SuperClaude_Framework. Used immediately after an implementation wave to confirm the result is production-ready and to capture lessons learned through four mandatory self-check questions.

## When to use

Use when the user invokes `@self-review` or asks to validate that an implementation wave is complete: tests run, edge cases considered, requirements met, follow-up/rollback steps identified.

## How to use

1. **Review** the task summary and implementation diff supplied by the implementing agent.
2. **Verify test evidence** (command + outcome). If missing, request a rerun before approval.
3. **Run the four mandatory self-check questions**: (a) tests/validation executed? (b) edge cases covered? (c) requirements matched? (d) follow-up or rollback steps needed?
4. **Produce a short checklist-style report** summarising test results, edge cases, requirements match, and follow-ups.
5. **Record reflexion patterns** when defects appear so the implementing agent can avoid repeats.
6. Pair with `sc-test` to gather the underlying test evidence if a rerun is needed.

Full behavioural specification at `references/upstream-sc-self-review.md`.

## References

- Upstream: [`src/superclaude/agents/self-review.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/agents/self-review.md) — verbatim mirror at [`references/upstream-sc-self-review.md`](./references/upstream-sc-self-review.md) (ADR-0011 D.3).
- Agency anchor: CLAUDE.md §13 — `/sc:*` skill invocation policy.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- Known limitation: one-shot snapshot at v4.3.0 — re-syncs require a new Task per ADR-0011 D.9.
