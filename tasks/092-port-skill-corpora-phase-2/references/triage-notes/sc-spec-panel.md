---
type: note
status: active
slug: triage-note-sc-spec-panel
summary: "Triage note for SuperClaude commands/spec-panel.md. Decision adapt (D.6 + D.8): 18 KB body and sequential+context7 MCPs. Heavy references/ extraction required for 11 expert profiles."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — `superclaude_framework/src/superclaude/commands/spec-panel.md`

## Why `adapt` (D.6 + D.8)

- 18.3 KB body — 3.7× the D.6 5 KB cap.
- Cites sequential + context7 MCPs.
- Content lists **11 spec-engineering experts** (one of: Beck, Hunt, Martin, Spolsky, etc.) with multi-paragraph profiles each → natural extraction candidate.

## Adaptation plan (ST-2)

1. **SKILL.md body** ≤ 4 KB — keep only:
   - Trigger / Usage / Behavioral Flow.
   - High-level expert-roster summary (one-line per expert, total ≤ 1 KB).
   - `## Adaptations from upstream` section noting MCP strip.
2. **Extract expert profiles** to `skills/sc-spec-panel/references/expert-profiles.md` — verbatim from upstream body, headed by `# Expert profiles` and one `## <Name>` heading per expert.
3. **Extract review-output templates** (if present) to `skills/sc-spec-panel/references/review-template.md`.
4. Strip sequential / context7 references; Agency reviewers can fetch official docs via WebFetch where the user authorises.

## Landing folder

`skills/sc-spec-panel/` + `references/expert-profiles.md` + `references/review-template.md`. Tier L3 (relies on `sc-spec-panel-experts` content + Agency's spec stack).

## Audit-graph linkage

- `skill_source: "superclaude@v4.3.0"`
- `skill_references_skills: [sc-business-panel, spec-skill]` — sibling panel pattern + Agency's spec authoring substrate.
