---
type: note
status: active
slug: triage-note-confidence-check
summary: "Triage note for confidence-check (snapshot appears in 4 locations). Canonical = src/superclaude/skills/; the other 3 are mirrors. Decision adapt with D.7 audit required."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — `confidence-check` (4 snapshot copies)

The upstream SuperClaude_Framework ships the same `confidence-check` skill in four locations:

1. `superclaude_framework/src/superclaude/skills/confidence-check/SKILL.md` — **canonical source.**
2. `superclaude_framework/.claude/skills/confidence-check/SKILL.md` — Claude-CLI surface.
3. `superclaude_framework/plugins/superclaude/skills/confidence-check/SKILL.md` — plugin packaging.
4. `superclaude_framework/skills/confidence-check/SKILL.md` — root-level mirror.

All four bodies are byte-equivalent. ST-2 MUST port from (1) only and treat (2)–(4) as redundant.

## Why `adapt` and not `port`

ADR-0011 D.7 prohibits SessionStart-injection. The Claude-CLI / plugin packaging of `confidence-check` may register a SessionStart hook to auto-load the skill at session start (mirroring `superpowers/hooks/session-start.sh` behaviour). ST-2 MUST:

1. Read `superclaude_framework/src/superclaude/skills/confidence-check/SKILL.md` body verbatim.
2. Grep adjacent hook / plugin manifest files for SessionStart references.
3. Strip any SessionStart binding from the ported `skills/sc-confidence-check/SKILL.md` body, replacing with an explicit "user-invocable only" note.
4. Document the strip in a `## Adaptations` section per ADR-0011 D.8 convention.

## Body adaptation budget

Upstream body ≈ 2.1 KB. After D.7 strip, body fits comfortably under the 5 KB cap (D.6). No `references/` extraction expected.

## Audit-graph linkage

- `skill_source: "superclaude@v4.3.0"`
- `skill_references_skills: [sc-implement, sc-research]` — confidence-check is conceptually a gate **before** implementation, so it forward-references the heavy implementation skills.
