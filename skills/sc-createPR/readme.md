---
type: index
status: active
slug: sc-createPR
summary: "Directory index for the imported `/sc:createPR` skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; Agency adaptations live in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-createPR/`

**What:** Open a pull request as the closing step of a Claude Code session (canonical session-closer per AGENTS.md CR.1–CR.7).

**Why here:** Imported under [Task 091](../../tasks/091-port-external-skill-corpora/task.md) ST-1 per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder path per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-createPR.md`, snapshot SHA `22ad3f48`).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-createPR.md`](./references/upstream-sc-createPR.md) — Verbatim mirror of `src/superclaude/commands/createPR.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- Canonical session-closer for Claude Code per AGENTS.md CR.1–CR.7 + CLAUDE.md §10.
- Re-runs `tools/check-governance.sh` before opening the PR (defence-in-depth on CR.3).
