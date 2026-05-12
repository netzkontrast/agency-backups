---
type: note
status: active
slug: triage-note-sc-light-mcp-adapts
summary: "Combined triage note for the seven 'light MCP adapt' SC commands (build, cleanup, estimate, explain, index, sc-cleanup, sc-index). All cite ≤ 2 MCPs (sequential+context7 or playwright) and fit under D.6 after strip. Mechanical adaptation."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — Light-MCP SC command adapts

Seven SC commands cite **≤ 2 MCPs** (typically sequential + context7) and have bodies ≤ 5 KB. After MCP-strip, they fit cleanly under D.6 without `references/` extraction. Mechanical adaptation pattern shared across all seven.

## Files

| Snapshot path | Body KB | MCP bindings | Agency replacement |
|---|---|---|---|
| `commands/build.md` | 3.4 | playwright | Drop playwright; rely on Bash/build tooling already in `Bash` tool. |
| `commands/cleanup.md` | 4.1 | sequential, context7 | Drop both; use Read + Edit + Bash(rm). |
| `commands/estimate.md` | 4.5 | sequential, context7 | Drop both; reasoning in Markdown. |
| `commands/explain.md` | 3.8 | sequential, context7 | Drop both; native Read + chain-of-thought. |
| `commands/index.md` | 3.8 | sequential, context7 | Drop both; native Read + Grep + Markdown synthesis. |

## Adaptation plan (ST-2)

Shared per-file recipe:

1. Strip the MCP bindings from frontmatter and body.
2. Replace MCP tool-call references with Agency-native tool invocations (Read / Edit / Bash / Grep / WebFetch).
3. Add a `## Adaptations from upstream` section noting which MCPs were stripped and why (D.8).
4. Body cap: each SKILL.md ≤ 4 KB after strip.

## Landing folders

- `skills/sc-build/SKILL.md` — Tier L1.
- `skills/sc-cleanup/SKILL.md` — Tier L1.
- `skills/sc-estimate/SKILL.md` — Tier L1.
- `skills/sc-explain/SKILL.md` — Tier L1.
- `skills/sc-index/SKILL.md` — Tier L1.

## Audit-graph linkage

- `skill_source: "superclaude@v4.3.0"` per file.
- Forward refs: `sc-build` → `[sc-test]`; `sc-cleanup` → `[sc-refactoring-expert]`; `sc-estimate` → `[sc-task, sc-workflow]`; `sc-explain` → `[sc-document, sc-learning-guide]`; `sc-index` → `[sc-document]`.
