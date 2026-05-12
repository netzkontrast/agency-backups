---
name: sc-test
description: >-
  Execute tests with coverage analysis and automated quality reporting. Use when the user invokes /sc:test, asks to run the test suite, or requests coverage analysis.
skill_kind: tool
skill_target_agents: [claude-code]
skill_references_skills: [sc-quality-engineer]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
skill_bundles_tools:
  - tools/tests
---

# sc-test — `/sc:test` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:test` command from SuperClaude_Framework. Runs the test suite with coverage analysis and quality reporting.

## When to use

Use when the user invokes `/sc:test` or asks to run the test suite with coverage. Delegates persona work to `sc-quality-engineer`.

## How to use

1. Discover test scope (changed files vs. full suite).
2. Invoke pytest via `tools/tests/` (bundled).
3. Report coverage + failed/skipped breakdown.

Full behavioural specification at `references/upstream-sc-test.md`.

## References

- Upstream: [`src/superclaude/commands/test.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/test.md) — verbatim mirror at [`references/upstream-sc-test.md`](./references/upstream-sc-test.md) (ADR-0011 D.3).
- Agency anchor: CLAUDE.md §13 — `/sc:*` skill invocation policy.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
