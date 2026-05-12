---
type: index
status: active
slug: sc-business-panel
summary: "Directory index for the imported `/sc:business-panel` skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; expert profiles + sub-mode playbook extracted into companion reference files per ADR-0011 D.6."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-business-panel/`

**What:** Multi-expert business strategy analysis: simulates a panel of nine renowned business thought leaders (Christensen, Porter, Drucker, Godin, Kim & Mauborgne, Collins, Taleb, Meadows, Doumont) analysing a document through three adaptive interaction modes (discussion, debate, Socratic). Synthesis-only — no implementation.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 (heavy-adapt cluster A) per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-business-panel.md`, snapshot SHA `22ad3f48`). D.6 body extraction: the 9-expert catalog and the 3-sub-mode playbook are split into companion reference notes so `SKILL.md` stays ≤ 5 KB.

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-business-panel.md`](./references/upstream-sc-business-panel.md) — Verbatim mirror of `src/superclaude/commands/business-panel.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.
- [`references/expert-profiles.md`](./references/expert-profiles.md) — Extracted 9-expert profile catalog (sourced from upstream `agents/business-panel-experts.md@22ad3f48`).
- [`references/sub-modes.md`](./references/sub-modes.md) — Extracted three-sub-mode playbook + expert-selection algorithm + document-type mappings + synthesis-output templates (sourced from upstream `modes/MODE_Business_Panel.md@22ad3f48`).

## Assumptions Log

- Two upstream files (`agents/business-panel-experts.md` and `modes/MODE_Business_Panel.md`) were **deliberately not registered** as standalone Agency skills (skipped per Task-092 row-34 and row-41 triage); their substantive content is consolidated into this skill's `references/` to avoid sprawl.
- The skill is **synthesis-only** per upstream's CRITICAL BOUNDARIES; any implementation step requires a follow-up `/sc:design`, `/sc:implement`, or `/sc:workflow` invocation.
- Wave-mode, persona-coordination, and MCP-integration sections of the upstream mode were intentionally dropped from `sub-modes.md` (MCP-strip + Agency irrelevance); the full verbatim mode remains accessible in the Task-091 snapshot for any caller that needs it.
