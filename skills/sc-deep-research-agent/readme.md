---
type: index
status: active
slug: sc-deep-research-agent
summary: "Directory index for the imported `/sc:deep-research-agent` skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; Agency adaptations live in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-deep-research-agent/`

**What:** Deep research specialist — adaptive strategies + multi-hop reasoning (Agency-adapted per D.8).

**Why here:** Imported under [Task 091](../../tasks/091-port-external-skill-corpora/task.md) ST-1 per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder path per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-deep-research-agent.md`, snapshot SHA `22ad3f48`).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-deep-research-agent.md`](./references/upstream-sc-deep-research-agent.md) — Verbatim mirror of `src/superclaude/agents/deep-research-agent.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- Body acknowledges the upstream MCP set (Tavily, Sequential, Playwright, Serena) as OPTIONAL; Agency runtime uses WebSearch + WebFetch as the primary surface per ADR-0011 D.8.
- Referenced by `sc-research`.
