---
type: index
status: active
slug: sc-save
summary: "Directory index for the imported `/sc:save` skill (SuperClaude_Framework v4.3.0). Serena-MCP memory persistence rewritten to Agency filesystem patterns (frontmatter mutation + friction-log append + git commit) per ADR-0011 D.8."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-save/`

**What:** Session-end checkpoint. Mutates `task_status` / `updated:` via `tools/fm/edit.py`, appends `friction-log.md`, and commits — so the next `/sc:load` can reconstruct state.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder path per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-save.md`, snapshot SHA `22ad3f48`); Serena-MCP surface rewritten to Agency filesystem patterns per D.8.

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys; Serena replaced with Agency filesystem patterns).
- [`references/upstream-sc-save.md`](./references/upstream-sc-save.md) — Verbatim mirror of `src/superclaude/commands/save.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- Frontmatter mutation goes through `tools/fm/edit.py` only — never `sed`/`awk` per CLAUDE.md §14.6.
- New commits, never `--amend`: if a pre-commit hook fails, the commit did not happen, so amending would mutate the previous commit (CLAUDE.md §11).
- Friction-log location depends on session type: `research/<slug>/reflection/friction-log.md` for research runs; commit-message `## Frustration Log` for standard tasks (FRUSTRATED.md).
