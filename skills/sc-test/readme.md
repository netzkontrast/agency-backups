---
type: index
status: active
slug: sc-test
summary: "Directory index for the imported `/sc:test` skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; Agency adaptations live in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-test/`

**What:** Execute tests with coverage analysis and automated quality reporting. Bundles tools/tests.

**Why here:** Imported under [Task 091](../../tasks/091-port-external-skill-corpora/task.md) ST-1 per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder path per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-test.md`, snapshot SHA `22ad3f48`).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-test.md`](./references/upstream-sc-test.md) — Verbatim mirror of `src/superclaude/commands/test.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- Bundles `tools/tests` per `skill_bundles_tools` (ADR-0007). The bundled directory is materialised into `scripts/_bundled/tests/` under `~/.claude/skills/` by `skills/skills-skill-bootstrap/sync.sh`.
