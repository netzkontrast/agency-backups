---
type: task
status: active
slug: novel-architect-phase2-worksheet-loop
summary: "Refactor Phase 2 (Narrative Architecture) of novel-architect to follow the 8-step Storyform Worksheet from dramatica-theory (00-storyform-worksheet.md): Intent → Throughlines → Classes → Dynamics → Story Points → Crucial Element → Signposts → Validation. Currently Phase 2 says 'auto + consult dramatica-theory' which is too vague. Worksheet-Loop makes the 8 steps explicit sub-phases with corresponding gates."
created: 2026-05-11
updated: 2026-05-11
task_id: "072"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - "071"
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - skills/novel-architect-structure/phases/phase2-narrative-architecture.md
  - skills/novel-architect-structure/methods/storyform/worksheet-workflow.md
  - skills/novel-architect-structure/assets/decision-heuristic-quick-ref.md
  - skills/novel-architect/SKILL.md
---

# Task 072 — Phase 2 Worksheet-Loop

## Goal

Phase 2 (Narrative Architecture) in `novel-architect-structure` becomes a structured **8-step Worksheet-Loop** based on [`dramatica-theory/references/00-storyform-worksheet.md`](../../skills/dramatica-theory/references/00-storyform-worksheet.md). The current "auto + consult dramatica-theory" becomes explicit sub-phases with AskUserQuestion loops grounded in [`dramatica-theory/references/10-decision-heuristics.md`](../../skills/dramatica-theory/references/10-decision-heuristics.md).

`done` when:
1. `phase2-narrative-architecture.md` restructured to 8 sub-phases aligned with the worksheet
2. New `methods/storyform/worksheet-workflow.md` exists in `novel-architect-structure` (or kept in orchestrator's `methods/`)
3. New `assets/decision-heuristic-quick-ref.md` — 1-page condensation of the 10-decision-heuristics.md for inline use
4. Gates 1-3 aligned with worksheet steps (Gate 1 = steps 0-1 Intent+Throughlines, Gate 2 = steps 2-5 Classes+Dynamics+StoryPoints, Gate 3 = steps 6-7 Crucial Element+Signposts+Validation)
5. End-to-end test: creating a Phase 2 architecture follows the 8-step worksheet, not the vague v1.0.0 "auto" path

## Context

v1.0.0's Phase 2 has 3 Gates but the sub-phases 2.1-2.8 say "auto + consult dramatica-theory" without using the existing worksheet. The worksheet is **operational** (fillable, step-by-step), while v1.0.0's approach is **declarative** (here are the slots, fill them somehow). This creates two problems:

1. Authors with no Dramatica knowledge cannot follow "consult dramatica-theory" — they need a step-by-step worksheet.
2. The decision-heuristics file (10-decision-heuristics.md) has practical "Class for OS" / "Change vs Steadfast" / "Action vs Decision Driver" decision trees that v1.0.0 doesn't surface inline.

## Plan

1. Read `dramatica-theory/references/00-storyform-worksheet.md` end-to-end
2. Map the 8 steps to v1.0.0 Phase 2 sub-phases 2.1-2.8 (some 1:1, some merge)
3. Rewrite `phase2-narrative-architecture.md` sub-phases section
4. Create `methods/storyform/worksheet-workflow.md` (or referenced in orchestrator's methods/ if Task 071 keeps method library there)
5. Create `assets/decision-heuristic-quick-ref.md` — 1-page condensation of 10-decision-heuristics.md (Class choice, Change/Steadfast, Action/Decision Driver, Linear/Holistic, Goal level, Optionlock/Timelock, Outcome×Judgment)
6. Update Gate 1/2/3 boundaries to align with worksheet steps
7. Run end-to-end smoke test (manually walk through Phase 2 for `consciousness-novel` example)

## Todo

- [ ] 1. Map worksheet steps to v1.0.0 Phase 2 sub-phases
- [ ] 2. Rewrite phase2 detail file with 8-step structure
- [ ] 3. Create worksheet-workflow.md method file
- [ ] 4. Create decision-heuristic-quick-ref.md asset
- [ ] 5. Align Gates 1-3 with worksheet step boundaries
- [ ] 6. Update SKILL.md Pipeline Overview table
- [ ] 7. End-to-end walk-through smoke test

## Links

- Parent epic: [Task 070](../070-novel-architect-v110-epic/task.md)
- Blocked by: [Task 071](../071-novel-architect-submodule-refactor/task.md)
- Blocks: [Task 073](../073-novel-architect-hard-rules-validation/task.md) (Hard Rules validation needs worksheet structure)
- Source spec: [`dramatica-theory/references/00-storyform-worksheet.md`](../../skills/dramatica-theory/references/00-storyform-worksheet.md), [`dramatica-theory/references/10-decision-heuristics.md`](../../skills/dramatica-theory/references/10-decision-heuristics.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`SKILLS.md`](../../SKILLS.md), [`AGENTS.md`](../../AGENTS.md) (Narrative Ontology NO.2)
