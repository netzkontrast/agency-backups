---
type: index
status: active
slug: sc-load
summary: "Directory index for the imported `/sc:load` skill (SuperClaude_Framework v4.3.0). Serena-MCP session persistence rewritten to Agency filesystem patterns per ADR-0011 D.8; verbatim upstream archived in `references/`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-load/`

**What:** Session-start context loader. Reconstructs prior task state from `tasks/<NNN>-*/task.md` frontmatter + `friction-log.md` without mutating the repo.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder path per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-load.md`, snapshot SHA `22ad3f48`); Serena-MCP surface rewritten to Agency filesystem patterns per D.8.

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys; Serena replaced with Agency filesystem patterns).
- [`references/upstream-sc-load.md`](./references/upstream-sc-load.md) — Verbatim mirror of `src/superclaude/commands/load.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- Active-task identification at load time relies on the branch convention `claude/<slug>-<id>` (CLAUDE.md §11) or the most recently `updated:` task; if neither resolves uniquely, the skill SHOULD ask the user rather than guess.
- Reading prior `friction-log.md` is non-destructive — `sc-load` MUST NOT append to or mutate friction logs (that is `sc-save`'s job).
