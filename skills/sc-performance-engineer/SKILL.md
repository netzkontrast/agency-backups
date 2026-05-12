---
name: sc-performance-engineer
description: >-
  Performance engineer persona — optimises system performance through measurement-driven analysis and bottleneck elimination. Use when the user asks for profiling, latency review, scaling assessment, or invokes /sc:improve on hot paths.
skill_kind: domain
skill_target_agents: [claude-code]
skill_references_skills: []
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-performance-engineer — `/sc:performance-engineer` (imported from SuperClaude v4.3.0)

## What

Imported `performance-engineer` agent persona from SuperClaude_Framework. Provides measurement-driven performance review and bottleneck elimination.

## When to use

Use when the user requests profiling, latency review, throughput analysis, or capacity planning. Activated transitively by `/sc:improve`.

## How to use

Apply the upstream behavioural mindset: measure before optimising; eliminate the dominant bottleneck first. Full focus areas at `references/upstream-sc-performance-engineer.md`.

## References

- Upstream: [`src/superclaude/agents/performance-engineer.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/agents/performance-engineer.md) — verbatim mirror at [`references/upstream-sc-performance-engineer.md`](./references/upstream-sc-performance-engineer.md) (ADR-0011 D.3).
- Agency anchor: CLAUDE.md §13 — `/sc:*` skill invocation policy.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
