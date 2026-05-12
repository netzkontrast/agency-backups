---
name: sc-spec-panel
description: >-
  Multi-expert specification review using renowned spec / software-engineering experts. Use when the user invokes /sc:spec-panel or asks for a panel-style critique of a specification.
skill_kind: analysis
skill_target_agents: [claude-code]
skill_references_skills: [sc-business-panel, sc-design]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-spec-panel — `/sc:spec-panel` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:spec-panel`. Coordinates a simulated expert panel (requirements, architecture, testing, cloud) that reviews a spec and produces priority-ranked recommendations. Runs in `discussion`, `critique`, or `socratic` mode.

## When to use

When the user invokes `/sc:spec-panel`, pastes a spec / requirements doc and asks for an expert critique, or asks to "review this spec like Wiegers / Fowler / Cockburn would". Pair with [`sc-design`](../sc-design/SKILL.md) when output drives architecture; with [`sc-business-panel`](../sc-business-panel/SKILL.md) when business implications appear.

## How to use

1. **Parse** the spec (`Read` `@file` or inline). Scope: requirements / architecture / testing / compliance.
2. **Select panel** — relevant experts (≤5 per pass). Honour `--experts "a,b"`.
3. **Pick mode**: `discussion` (sequential build-on), `critique` (severity + fix + impact), `socratic` (probing questions only).
4. **Run panel** in Markdown. Each expert speaks per their profile (`references/experts/<name>.md`).
5. **Synthesise** — group by severity, dedupe, surface consensus + disagreements.
6. **Output** `standard` / `structured` / `detailed`. Land into the active task / research workspace; do not inline into the spec.
7. **Iterate** if `--iterations N` — pass 1 structural, pass 2 detail, pass 3 polish.

Mode templates, focus-area panels, output formats, and workflow examples are verbatim in [`references/upstream-sc-spec-panel.md`](./references/upstream-sc-spec-panel.md).

### Expert roster

| Expert | Domain | Profile |
|---|---|---|
| Karl Wiegers | requirements engineering, SMART | [`experts/wiegers.md`](./references/experts/wiegers.md) |
| Gojko Adzic | specification by example, BDD | [`experts/adzic.md`](./references/experts/adzic.md) |
| Alistair Cockburn | use cases, goal-oriented analysis | [`experts/cockburn.md`](./references/experts/cockburn.md) |
| Martin Fowler | architecture, evolutionary design | [`experts/fowler.md`](./references/experts/fowler.md) |
| Michael Nygard | reliability, failure modes | [`experts/nygard.md`](./references/experts/nygard.md) |
| Sam Newman | microservices, service boundaries | [`experts/newman.md`](./references/experts/newman.md) |
| Gregor Hohpe | enterprise integration patterns | [`experts/hohpe.md`](./references/experts/hohpe.md) |
| Lisa Crispin | agile testing, quality attributes | [`experts/crispin.md`](./references/experts/crispin.md) |
| Janet Gregory | collaborative testing, three amigos | [`experts/gregory.md`](./references/experts/gregory.md) |
| Kelsey Hightower | cloud-native, operations | [`experts/hightower.md`](./references/experts/hightower.md) |

## Adaptations from upstream

- **D.6 extraction** — per-expert profiles + mode / workflow examples moved to `references/experts/*.md` + verbatim mirror; SKILL.md keeps a compact roster.
- **D.8 MCP strip** — upstream "MCP Integration" citing **Sequential MCP** (panel coordination) and **Context7 MCP** (industry docs) is removed. Agency runs the panel as plain Markdown reasoning; doc lookups via `WebFetch` / `WebSearch`.
- **YAML stripped** — upstream `name`, `description`, `category`, `complexity`, `mcp-servers`, `personas` replaced by Agency L1+L2 frontmatter.
- **D.7** — no SessionStart hook present upstream; no strip required.

## References

- Upstream: [`src/superclaude/commands/spec-panel.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/spec-panel.md) — verbatim mirror at [`references/upstream-sc-spec-panel.md`](./references/upstream-sc-spec-panel.md) (ADR-0011 D.3).
- Per-expert profiles: [`references/experts/`](./references/experts/) (D.6).
- Agency anchor: CLAUDE.md §13 — `/sc:*` invocation policy.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- **Sequential MCP** is OPTIONAL — when present, MAY substitute for the in-prompt sequential reasoning the Agency body uses; absent, native chain-of-thought-in-Markdown is sufficient (ADR-0011 D.8).
- **Context7 MCP** is OPTIONAL — when present, MAY substitute for industry-doc lookups during review; absent, native `WebFetch` / `WebSearch` is sufficient (ADR-0011 D.8).
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
