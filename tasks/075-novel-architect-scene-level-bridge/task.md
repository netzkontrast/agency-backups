---
type: task
status: active
slug: novel-architect-scene-level-bridge
summary: "Integrate the Scene-Level-Bridge 5-question audit (Q1-Q5) from dramatica-theory/12-scene-level-bridge.md into Phase 5 (per-moment) and Phase 6 (pre-draft) of novel-architect-scene. Adds NCP schema fields: throughline_focus, operating_level, motivation_elements, plot_story_point. Without this audit, Phase 5 produces moments that are NCP-valid but Dramatica-empty."
created: 2026-05-11
updated: 2026-05-11
task_id: "075"
task_status: done
task_owner: "claude-code"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - 071
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - skills/novel-architect-scene/phases/phase5-scene-matrix.md
  - skills/novel-architect-scene/phases/phase6-drafting.md
  - skills/novel-architect/references/ncp-integration-contract.md
  - skills/novel-architect-scene/assets/scene-matrix-template.md
  - skills/novel-architect-scene/assets/chapter-draft-template.md
---

# Task 075 — Scene-Level-Bridge Q1-Q5

## Goal

Per-moment and per-chapter audit using the 5 questions from [`dramatica-theory/references/12-scene-level-bridge.md`](../../skills/dramatica-theory/references/12-scene-level-bridge.md):

- **Q1:** Which throughline is dominant in this moment? (OS/MC/IC/SS)
- **Q2:** Which throughlines are also present (secondary)?
- **Q3:** At what level is the scene operating? (Class / Type / Variation / Element)
- **Q4:** Which static/progressive plot story point does this scene serve? (Goal / Requirement / Consequence / Cost / Dividend / Signpost / Journey)
- **Q5:** Which Motivation Elements are in play? (from the 64-element list; Crucial Element MUST appear when MC present)

`done` when:
1. Phase 5 detail file has new §X "Scene-Level Audit" sub-phase implementing Q1-Q5 per moment
2. Phase 6 detail file has new pre-draft check that walks Q1-Q5 for the chapter being drafted
3. NCP integration contract (`references/ncp-integration-contract.md`) documents 4 new moment fields: `throughline_focus`, `operating_level`, `motivation_elements`, `plot_story_point`
4. `assets/scene-matrix-template.md` extended with Q1-Q5 fields per moment
5. `assets/chapter-draft-template.md` Pre-Draft Checklist extended with Q1-Q5
6. ncp-author delegation updated to write the new moment fields
7. Smoke test: a moment without Q1-Q5 answers fails Gate 3 of Phase 5

## Context

v1.0.0's Phase 5 produces moments with title + scene-summary + parent_storybeat. These are NCP-valid but **Dramatica-empty** — there's no encoded reason for the moment in storyform terms. Without throughline-dominance per moment, the drafting agent has no signal for which voice/perspective/Element to centre.

The Scene-Level-Bridge file is the canonical operational bridge from storyform → scene-work. v1.0.0 missing it means the storyform encoded in Phase 2 has no operational pull on Phase 5/6 work.

## Plan

1. Read `dramatica-theory/references/12-scene-level-bridge.md` end-to-end for Q1-Q5 + throughline-dominance-by-act patterns + scene-types
2. Design NCP schema extension: 4 fields per moment (consult `ncp-author` for namespace conventions; likely `custom_*` per AGENTS.md NO.2 if no native NCP field)
3. Update `references/ncp-integration-contract.md` with new fields + how they're written
4. Author Phase 5 §X "Scene-Level Audit Workflow" — per-moment Q1-Q5 loop
5. Update Phase 6 pre-draft checks (already has 7 items; add Q1-Q5 as item 8)
6. Extend asset templates
7. Smoke test

## Todo

- [x] 1. Read 12-scene-level-bridge.md in full
- [x] 2. Design moment-schema extension (NCP native vs custom_*)
- [x] 3. Consult `ncp-author` skill for namespace conventions
- [x] 4. Update ncp-integration-contract.md
- [x] 5. Author Phase 5 §X Scene-Level Audit Workflow
- [x] 6. Update Phase 6 pre-draft checklist
- [x] 7. Extend scene-matrix-template.md
- [x] 8. Extend chapter-draft-template.md
- [x] 9. Smoke test on existing example (consciousness-novel)

## Links

- Parent epic: [Task 070](../070-novel-architect-v110-epic/task.md)
- Blocked by: [Task 071](../071-novel-architect-submodule-refactor/task.md)
- Source spec: [`dramatica-theory/references/12-scene-level-bridge.md`](../../skills/dramatica-theory/references/12-scene-level-bridge.md)
- Affects skill: [`skills/ncp-author/`](../../skills/ncp-author/) (schema extension consultation)
- Governing specs: [`TASK.md`](../../TASK.md), [`AGENTS.md`](../../AGENTS.md) (NO.2 — ontology resolution for new fields)
