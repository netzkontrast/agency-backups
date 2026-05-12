---
type: note
status: active
slug: triage-note-sc-business-panel
summary: "Triage note for SuperClaude commands/business-panel.md + agents/business-panel-experts.md + modes/MODE_Business_Panel.md trio. Decision: port the command (adapt D.8), skip the agent + mode (consolidated coverage)."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — Business-Panel trio

The upstream framework distributes business-panel functionality across **three files**:

1. `commands/business-panel.md` (3.7 KB, sequential+context7 binding) — entry-point command.
2. `agents/business-panel-experts.md` (9.8 KB) — describes the 9 thought-leaders (Christensen, Porter, Drucker, Godin, Kim&Mauborgne, Collins, Taleb, Meadows, Doumont).
3. `modes/MODE_Business_Panel.md` (11.8 KB, sequential+context7+magic+playwright binding) — behavioural mode with 3 adaptive sub-modes.

## Why one port + two skips

- **Port the command** (`sc-business-panel`, decision `adapt` D.8): the user-facing entry point. Strip sequential+context7. Bundle the 9-expert framework as `references/expert-profiles.md` extracted from the agent body.
- **Skip the agent** (row 34): its content (the 9 experts) is moved into the command's `references/`. Listing it as a standalone agent duplicates Agency's existing built-in `business-panel-experts` agent type (already available via the Agent tool).
- **Skip the mode** (row 41): D.6 + D.8 violation **and** content duplicates the command's Behavioral Flow.

## Adaptation plan (ST-2)

1. Port `commands/business-panel.md` body to `skills/sc-business-panel/SKILL.md` (strip MCP).
2. Extract the 9 expert profiles from `agents/business-panel-experts.md` to `skills/sc-business-panel/references/expert-profiles.md`. Each profile ≤ 500 bytes for total ~5 KB reference file.
3. Extract the 3 sub-modes (discussion/debate/socratic) from MODE_Business_Panel into `skills/sc-business-panel/references/sub-modes.md`.
4. Body cap: SKILL.md body ≤ 4 KB after MCP-strip.

## Landing folder

`skills/sc-business-panel/` with `references/expert-profiles.md` + `references/sub-modes.md`. Tier L2.

## Audit-graph linkage

- `skill_source: "superclaude_framework@v4.3.0"`
- `skill_references_skills: [sc-spec-panel]` — both share the multi-expert panel pattern.
