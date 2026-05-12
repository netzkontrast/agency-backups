---
name: sc-analyze
description: >-
  Comprehensive code analysis across quality, security, performance, and architecture domains. Use when the user invokes /sc:analyze or asks for a multi-domain code audit, vulnerability scan, or technical-debt review.
skill_kind: analysis
skill_target_agents: [claude-code]
skill_references_skills: [sc-test, sc-improve, sc-refactoring-expert]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-analyze — `/sc:analyze` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:analyze` command from SuperClaude_Framework. Performs comprehensive static code analysis across quality, security, performance, and architecture domains, producing severity-rated findings with actionable recommendations.

## When to use

Use when the user invokes `/sc:analyze` or asks for code-quality assessment, security vulnerability scanning, performance bottleneck identification, or architecture/technical-debt review.

## How to use

1. **Discover** sources via Glob and language detection to categorise files.
2. **Scan** with domain-specific techniques (quality/security/performance/architecture) and pattern matching.
3. **Evaluate** findings, assigning severity and impact.
4. **Recommend** prioritised, actionable fixes with implementation guidance.
5. **Report** results as a structured document with metrics and a roadmap.
6. Hand off to `sc-improve` to apply fixes or `sc-refactoring-expert` for deeper restructuring; `sc-test` validates resulting changes.

Full behavioural specification at `references/upstream-sc-analyze.md`.

## References

- Upstream: [`src/superclaude/commands/analyze.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/analyze.md) — verbatim mirror at [`references/upstream-sc-analyze.md`](./references/upstream-sc-analyze.md) (ADR-0011 D.3).
- Agency anchor: CLAUDE.md §13 — `/sc:*` skill invocation policy.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- Known limitation: one-shot snapshot at v4.3.0 — re-syncs require a new Task per ADR-0011 D.9.
