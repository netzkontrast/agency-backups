---
type: index
status: active
slug: sc-design
summary: "Directory index for the imported `/sc:design` skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; Agency-facing body in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-design/`

**What:** Design system architecture, APIs, component interfaces, and database schemas with comprehensive specifications.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder path per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-design.md`, snapshot SHA `22ad3f48`).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-design.md`](./references/upstream-sc-design.md) — Verbatim mirror of `src/superclaude/commands/design.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- (none)
