---
type: index
status: active
slug: sc-root-cause-analyst
summary: "Directory index for the imported root-cause-analyst skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; Agency adaptations live in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-root-cause-analyst/`

**What:** Root Cause Analyst agent — evidence-based hypothesis testing for complex / recurring / multi-component failures.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder path per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-root-cause-analyst.md`, snapshot SHA `22ad3f48`).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-root-cause-analyst.md`](./references/upstream-sc-root-cause-analyst.md) — Verbatim mirror of `src/superclaude/agents/root-cause-analyst.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- This skill was triaged as a **pure port** in Task 092 ST-1 ([triage matrix](../../tasks/092-port-skill-corpora-phase-2/references/triage-matrix.md)): no MCP bindings, body ≤ 5 KB, no SessionStart-injection clauses to strip.
- Upstream YAML frontmatter (`name`, `description`, `category`, `complexity`, `mcp-servers`, `personas`) is replaced with Agency L2 frontmatter; the verbatim body is preserved in `references/` for audit.
