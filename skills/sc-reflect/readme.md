---
type: index
status: active
slug: sc-reflect
summary: "Directory index for the imported `/sc:reflect` skill (SuperClaude_Framework v4.3.0). Serena-MCP think_about_* tools rewritten to TodoWrite + Gherkin acceptance review per ADR-0011 D.8; bundles MODE_Introspection per D.5."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-reflect/`

**What:** Mid-session reflection and completion gate. Reviews `task_status` against Gherkin acceptance criteria via TodoWrite + `friction-log.md` reading, with Introspection mode active.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder path per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-reflect.md`, snapshot SHA `22ad3f48`); Serena-MCP surface rewritten to Agency filesystem patterns per D.8; MODE_Introspection bundled per D.5.

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys; Serena `think_about_*` replaced with TodoWrite + Gherkin review).
- [`references/upstream-sc-reflect.md`](./references/upstream-sc-reflect.md) — Verbatim mirror of `src/superclaude/commands/reflect.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.
- [`references/mode-introspection.md`](./references/mode-introspection.md) — Verbatim mirror of `src/superclaude/modes/MODE_Introspection.md` from upstream at SHA `22ad3f48`. Bundled per ADR-0011 D.5 — modes are behavioural overlays, not standalone skills.

## Assumptions Log

- `/sc:reflect` is read-only with respect to task frontmatter: status mutation belongs to `/sc:save`, not `/sc:reflect`.
- Introspection mode activates silently on every `/sc:reflect` invocation; users do not need to pass `--introspect` explicitly.
- Gherkin acceptance criteria (CLAUDE.md §5) are the canonical adherence rubric — flat bullet-list "acceptance" sections SHOULD be treated as defects and flagged, not silently scored.
