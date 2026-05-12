---
type: note
status: active
slug: triage-note-superpowers-finishing-a-branch
summary: "Triage note for superpowers/skills/finishing-a-development-branch/SKILL.md. Decision port (with D.1, D.6 verify-and-extract): 5.3 KB body at cap. Aligns with AGENTS.md Closing Run Procedure but Superpowers variant adds merge/PR/discard decision tree."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — `superpowers/skills/finishing-a-development-branch/SKILL.md`

## Why `port` (D.1 + verify D.6)

- 5.3 KB body — slightly over the D.6 5 KB cap; verify exact bytes against `tools/fm/validate.py F.B.10` during ST-3 import.
- No MCP bindings.
- Content: structured branch-completion workflow (test pass → present merge/PR/discard options → cleanup).
- Closely overlaps Agency's **AGENTS.md Closing Run Procedure** (CR.1–CR.7) but adds the **discard option** Agency does not yet codify (some branches are abandoned post-research without merging).

## Adaptation plan (ST-3)

1. **Body** ≤ 5 KB:
   - Keep the 3-option decision tree (merge / PR / discard).
   - Keep the test-pass + governance precondition.
2. **If body > 5 KB after preserve:** extract the worked-example "discard" flow to `skills/superpowers-finishing-a-branch/references/discard-flow.md`.
3. **Cross-reference** AGENTS.md Closing Run Procedure (§ Closing Run Procedure, rules CR.1–CR.7) in body via Markdown link.
4. **Cite Agency's `sc-createPR`** as the "PR" branch of the decision tree.

## Landing folder

`skills/superpowers-finishing-a-branch/`. Tier L1 (leaf workflow; depends only on Agency's git + governance substrate).

## Audit-graph linkage

- `skill_source: "superpowers@v4.0.3"`
- `skill_references_skills: [sc-createPR, superpowers-verification-before-completion]`
