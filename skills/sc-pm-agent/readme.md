---
type: index
status: active
slug: sc-pm-agent
summary: "Directory index for the imported `/sc:pm-agent` skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; Agency adaptations live in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-pm-agent/`

**What:** Project Manager agent — coordinates SuperClaude /sc:* workflows.

**Why here:** Imported under [Task 091](../../tasks/091-port-external-skill-corpora/task.md) ST-1 per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder path per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-pm-agent.md`, snapshot SHA `22ad3f48`).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-pm-agent.md`](./references/upstream-sc-pm-agent.md) — Verbatim mirror of `src/superclaude/agents/pm-agent.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- **Inert at SessionStart** per ADR-0011 D.7 — Agency does not port the upstream SessionStart restore hook. Activated only when the user explicitly invokes `/sc:pm`.
