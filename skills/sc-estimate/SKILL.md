---
name: sc-estimate
description: "Provide development estimates for tasks, features, or projects with intelligent analysis"
skill_kind: analysis
skill_target_agents: [claude-code]
skill_references_skills: [sc-task, sc-workflow]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-estimate — `/sc:estimate` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:estimate` command from SuperClaude_Framework. Produces an estimation **report only** — no implementation. Covers time, effort, complexity, and risk with confidence intervals. Body adapted per ADR-0011 D.8: **`Read` + native reasoning + Markdown synthesis are the primary surface** (see `## Compatibility` for upstream MCP notes).

## When to use

Use when the user invokes `/sc:estimate` or asks for time/effort/complexity sizing of a feature or migration. After the report lands, the user decides next steps: use `sc-workflow` for planning or `sc-task` for executable breakdown.

## When NOT to use

Do NOT begin implementation. Do NOT create or stage execution tasks during estimation — the upstream "CRITICAL BOUNDARIES → STOP AFTER ESTIMATION" clause is preserved.

## How to use

1. **Scope**: `Read` the target spec/code/issue and `Grep` for cross-cutting touchpoints. Note explicit unknowns.
2. **Decompose**: break the scope into 3–8 work-package slices (e.g. data model, API, UI, tests, migration). For each slice, surface complexity drivers — novelty, integration surface, test cost, regulatory load.
3. **Estimate**: assign per-slice ranges (e.g. 1–3 days) using a chosen methodology (time-based, t-shirt sizing, complexity points). State the methodology explicitly. Apply a multiplier for explicit unknowns.
4. **Validate**: cross-check totals against any historical benchmarks the user supplies; flag slices whose ranges exceed a 3× spread for further decomposition.
5. **Synthesise**: write the estimation report in Markdown — per-slice breakdown, total with confidence interval (e.g. 70% / 90%), top 3 risk factors, resource assumptions, and explicit out-of-scope items.
6. **Stop**: present the report. Do NOT initiate execution. Suggest `sc-workflow` (planning) or `sc-task` (execution breakdown) as the next-step skill.

## Adaptations from upstream

- **Dropped MCP bindings**: `sequential` and `context7` (D.8). The "Sequential MCP integration for systematic analysis and complexity assessment" loop collapses to native chain-of-thought over `Read`/`Grep` outputs; "Context7 MCP integration for framework-specific patterns and historical benchmark data" becomes inline knowledge plus user-supplied benchmarks (no automated lookup).
- Multi-persona coordination (architect / performance / project-manager) survives as inline lenses applied during step 2 decomposition.
- The "STOP AFTER ESTIMATION" critical boundary is preserved verbatim in spirit.

## References

- Upstream: [`src/superclaude/commands/estimate.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/estimate.md) — verbatim mirror at [`references/upstream-sc-estimate.md`](./references/upstream-sc-estimate.md) (ADR-0011 D.3).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md) §D.8.
- Companion skills: [`skills/sc-task`](../sc-task/SKILL.md), [`skills/sc-workflow`](../sc-workflow/SKILL.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface).
- MCP servers used: **none required**.
- **Sequential MCP** is OPTIONAL — when present, MAY substitute for the native chain-of-thought used in `How to use` steps 2–4 (decomposition, sizing, validation); when absent, native reasoning is sufficient (ADR-0011 D.8).
- **Context7 MCP** is OPTIONAL — when present, MAY substitute for the framework-pattern / benchmark lookup that otherwise relies on inline knowledge plus user-supplied data; when absent, the inline approach is sufficient (ADR-0011 D.8).
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
