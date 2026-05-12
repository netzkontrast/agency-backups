---
type: index
status: active
slug: sc-implement
summary: "Directory index for the imported `/sc:implement` skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; Agency adaptations live in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-implement/`

**What:** Feature and code implementation with intelligent persona activation. Bundles tools/fm + MODE_Orchestration.

**Why here:** Imported under [Task 091](../../tasks/091-port-external-skill-corpora/task.md) ST-1 per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder path per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-implement.md`, snapshot SHA `22ad3f48`).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-implement.md`](./references/upstream-sc-implement.md) — Verbatim mirror of `src/superclaude/commands/implement.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.
- [`references/MODE_Orchestration.md`](./references/MODE_Orchestration.md) — upstream Orchestration mode, bundled per ADR-0011 D.5.

## Assumptions Log

- Bundles `tools/fm` per `skill_bundles_tools` (ADR-0007). The bundled directory is materialised into `scripts/_bundled/fm/` under `~/.claude/skills/` by `skills/skills-skill-bootstrap/sync.sh`.
- Frontmatter mutations MUST use `tools/fm/edit.py` per CLAUDE.md §14.6 — never `sed` / `awk`.
