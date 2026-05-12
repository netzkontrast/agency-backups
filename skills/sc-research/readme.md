---
type: index
status: active
slug: sc-research
summary: "Directory index for the imported `/sc:research` skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; Agency adaptations live in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-research/`

**What:** Deep web research with adaptive planning — Agency-adapted per ADR-0011 D.8 (WebSearch primary; Tavily OPTIONAL). Bundles MODE_DeepResearch.

**Why here:** Imported under [Task 091](../../tasks/091-port-external-skill-corpora/task.md) ST-1 per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder path per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-research.md`, snapshot SHA `22ad3f48`).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-research.md`](./references/upstream-sc-research.md) — Verbatim mirror of `src/superclaude/commands/research.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.
- [`references/MODE_DeepResearch.md`](./references/MODE_DeepResearch.md) — upstream DeepResearch mode, bundled per ADR-0011 D.5.

## Assumptions Log

- Body **materially adapted** per ADR-0011 D.8: WebSearch + WebFetch are the primary research surface; Tavily MCP is OPTIONAL when present.
- The verbatim Tavily-first upstream body is preserved at `references/upstream-sc-research.md` for traceability.
- Deliverables MUST land at `/research/<slug>/output/SPEC.md` per RESEARCH.md §6.5.
