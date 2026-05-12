---
type: index
status: active
slug: sc-brainstorm
summary: "Directory index for the imported `/sc:brainstorm` skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; Agency adaptations live in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-brainstorm/`

**What:** Socratic requirements-discovery dialogue: transforms an ambiguous idea into a structured requirements specification (functional, non-functional, user stories, open questions). Plans only — no architecture, no code.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 (heavy-adapt cluster A) per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-brainstorm.md`, snapshot SHA `22ad3f48`). Body extraction per D.6 — six upstream MCP bindings stripped while preserving the five-phase Behavioral Flow.

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-brainstorm.md`](./references/upstream-sc-brainstorm.md) — Verbatim mirror of `src/superclaude/commands/brainstorm.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- `MODE_Brainstorming` was deliberately NOT bundled (skipped per row-40 of the Task-092 triage). Its content duplicates the upstream command body almost verbatim; bundling would be redundant.
- Requirements output lands at `prompts/<slug>/brief.md` per [PROMPT.md](../../PROMPT.md) (or as inline session output); it MUST NOT be filed under `research/`.
- Follow-up questions discovered mid-brainstorm are filed as NEW Prompts under `/prompts/`, never appended to a closed research workspace ([CLAUDE.md §1](../../CLAUDE.md)).
