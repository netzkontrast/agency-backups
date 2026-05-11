---
type: task
status: active
slug: novel-architect-phase2-worksheet-loop
summary: "Refactor Phase 2 (Narrative Architecture) of novel-architect to follow the 8-step Storyform Worksheet from dramatica-theory (00-storyform-worksheet.md): Intent → Throughlines → Classes → Dynamics → Story Points → Crucial Element → Signposts → Validation. Currently Phase 2 says 'auto + consult dramatica-theory' which is too vague. Worksheet-Loop makes the 8 steps explicit sub-phases with corresponding gates."
created: 2026-05-11
updated: 2026-05-11
task_id: "072"
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
  - skills/novel-architect/SKILL.md
  - skills/novel-architect/render/render_intent.py
  - skills/novel-architect/assets/intent-template.yaml
  - skills/novel-architect/phases/phase2-narrative-architecture.md
  - skills/novel-architect/methods/readme.md
  - skills/novel-architect/assets/architecture-template.yaml
  - skills/novel-architect/phases/phase1-intent-capture.md
  - skills/novel-architect/render/tests/test_render_intent.py
  - skills/novel-architect-structure/methods/storyform/worksheet-loop.md
  - skills/novel-architect-structure/methods/storyform/readme.md
  - skills/novel-architect-structure/assets/decision-heuristic-quick-ref.md
  - skills/novel-architect-structure/assets/readme.md
---

# Task 072 — Phase 2 Worksheet-Loop

## Goal

Phase 2 (Narrative Architecture) in `novel-architect-structure` becomes a structured **8-step Worksheet-Loop** based on [`dramatica-theory/references/00-storyform-worksheet.md`](../../skills/dramatica-theory/references/00-storyform-worksheet.md). The current "auto + consult dramatica-theory" becomes explicit sub-phases with AskUserQuestion loops grounded in [`dramatica-theory/references/10-decision-heuristics.md`](../../skills/dramatica-theory/references/10-decision-heuristics.md).

`done` when:
1. `phase2-narrative-architecture.md` restructured to 8 sub-phases aligned with the worksheet
2. New `methods/storyform/worksheet-loop.md` exists in `novel-architect-structure` (or kept in orchestrator's `methods/`)
3. New `assets/decision-heuristic-quick-ref.md` — 1-page condensation of the 10-decision-heuristics.md for inline use
4. Gates 1-3 aligned with worksheet steps (Gate 1 = steps 0-1 Intent+Throughlines, Gate 2 = steps 2-5 Classes+Dynamics+StoryPoints, Gate 3 = steps 6-7 Crucial Element+Signposts+Validation)
5. End-to-end test: creating a Phase 2 architecture follows the 8-step worksheet, not the vague v1.0.0 "auto" path
6. **Slot-list source-of-truth consolidated** (see §"Slot-List Consolidation" below) — addresses [PR #101 review §2.5](https://github.com/netzkontrast/agency/pull/101#issuecomment-4422239250)
7. **`render_intent.py` slot-state classification** simplified per PR #101 review §2.7 (current ordering has redundant `value == "<PLACEHOLDER>"` then `"<PLACEHOLDER>" in value` checks — collapse to one)

## Context

v1.0.0's Phase 2 has 3 Gates but the sub-phases 2.1-2.8 say "auto + consult dramatica-theory" without using the existing worksheet. The worksheet is **operational** (fillable, step-by-step), while v1.0.0's approach is **declarative** (here are the slots, fill them somehow). This creates two problems:

1. Authors with no Dramatica knowledge cannot follow "consult dramatica-theory" — they need a step-by-step worksheet.
2. The decision-heuristics file (10-decision-heuristics.md) has practical "Class for OS" / "Change vs Steadfast" / "Action vs Decision Driver" decision trees that v1.0.0 doesn't surface inline.

## Slot-List Consolidation (PR #101 review §2.5)

The Phase 1 slot set is currently duplicated across **three** locations:

1. `skills/novel-architect/render/render_intent.py:42-57` — `REQUIRED_SLOTS` + `OPTIONAL_SLOTS` Python lists
2. `skills/novel-architect/phases/phase1-intent-capture.md` §1 — canonical Markdown table
3. `skills/novel-architect/assets/intent-template.yaml` — YAML template

When a new slot is added (this Task will add Phase 2 worksheet slots; future tasks may add more), all three need updating in lockstep. Only the YAML write/read path fails loudly on drift — the other two silently render incomplete status-views.

**Fix in this Task:**
- Promote `intent-template.yaml` to single source of truth.
- Add `_required:` / `_optional:` metadata block (or extract from key naming convention).
- `render_intent.py` reads `REQUIRED_SLOTS` / `OPTIONAL_SLOTS` from the YAML at runtime (single canonical list).
- `phase1-intent-capture.md` table becomes auto-generated from the YAML (or carries a "regenerated from intent-template.yaml on YYYY-MM-DD" footer to make drift obvious).

This pattern repeats for Phase 2 (architecture.yaml slots), Phase 3 (character-architecture.yaml), Phase 5 (scene-matrix.md fields). This Task lands the pattern for intent.yaml; other tasks (074, 075) can adopt it incrementally.

## Plan

1. Read `dramatica-theory/references/00-storyform-worksheet.md` end-to-end
2. Map the 8 steps to v1.0.0 Phase 2 sub-phases 2.1-2.8 (some 1:1, some merge)
3. Rewrite `phase2-narrative-architecture.md` sub-phases section
4. Create `methods/storyform/worksheet-loop.md` (or referenced in orchestrator's methods/ if Task 071 keeps method library there)
5. Create `assets/decision-heuristic-quick-ref.md` — 1-page condensation of 10-decision-heuristics.md (Class choice, Change/Steadfast, Action/Decision Driver, Linear/Holistic, Goal level, Optionlock/Timelock, Outcome×Judgment)
6. Update Gate 1/2/3 boundaries to align with worksheet steps
7. Run end-to-end smoke test (manually walk through Phase 2 for `consciousness-novel` example)

## Todo

- [x] 1. Map worksheet steps to v1.0.0 Phase 2 sub-phases
- [x] 2. Rewrite phase2 detail file with 8-step structure
- [x] 3. Create worksheet-loop.md method file
- [x] 4. Create decision-heuristic-quick-ref.md asset
- [x] 5. Align Gates 1-3 with worksheet step boundaries
- [x] 6. Update SKILL.md Pipeline Overview table
- [x] 7. End-to-end walk-through smoke test
- [x] 8. **Slot-list consolidation**: promote `intent-template.yaml` to single source of truth; refactor `render_intent.py` to read REQUIRED_SLOTS/OPTIONAL_SLOTS from YAML at runtime; mark `phase1-intent-capture.md` table as derived. *(PR #101 review §2.5)*
- [x] 9. **render_intent.py slot-state polish**: collapse redundant `value == "<PLACEHOLDER>"` then `"<PLACEHOLDER>" in value` checks into one. *(PR #101 review §2.7)*

## Closure (2026-05-11)

`task_status: done`. All 9 todos closed.

This branch (`claude/implement-task-72-ZCpe1`) was rebased onto `main` after
the Task 070 Epic landed (PR #102). Main's Epic close included a **lean**
Task 072 implementation (`skills/novel-architect-structure/methods/
storyform/worksheet-loop.md`, ~98 lines). This branch supersedes that
lean version with a **deep** implementation merged into the same file
location — `novel-architect-structure/methods/storyform/worksheet-loop.md`
now contains the full 8-step operational walkthrough (per-step askuser
shape, inline decision heuristic, recovery path, NCP slot map, worked
example for `consciousness-novel`).

### Implementation summary

1. **Worksheet → Sub-phase mapping** — Phase 2 now runs 14 sub-phases
   (2.1–2.14) bound to Worksheet Steps 0–8 + Validation Pass; mapping
   table in [`phases/phase2-narrative-architecture.md` §2](../../skills/novel-architect/phases/phase2-narrative-architecture.md#2-sub-phases-mit-3-gates-8-step-worksheet-loop).
2. **Phase 2 detail file rewritten** —
   [`skills/novel-architect/phases/phase2-narrative-architecture.md`](../../skills/novel-architect/phases/phase2-narrative-architecture.md)
   now binds every sub-phase to a Worksheet Step with explicit Gate
   boundaries (Gate 1 = Steps 0+1, Gate 2 = Steps 2–5, Gate 3 = Steps 6+7+V).
   `architecture.yaml` grew `name` fields on throughlines, `story_points`
   block (static/driver/thematic), `crucial_element` block, `signposts`
   + `journeys` arrays, optional `genre_mode`, auto-derived `ending_type`,
   and a `worksheet_audit` step-completion tracker.
3. **`novel-architect-structure/methods/storyform/worksheet-loop.md`** —
   replaced main's lean Epic-bundled version (~98 lines) with the deep
   operational walkthrough (~360 lines): per-step askuser shape, inline
   decision-heuristic excerpts (HR.M2.3), recovery paths, NCP slot mapping,
   worked example for `consciousness-novel`.
4. **`novel-architect-structure/assets/decision-heuristic-quick-ref.md`** —
   new 1-pager with §1 Class choice, §2 Change/Steadfast, §3 Start/Stop,
   §4 Doer/Beer, §5 Linear/Holistic, §6 Action/Decision Driver,
   §7 Optionlock/Timelock, §8 Outcome×Judgment, §9 Goal level, §10
   Crucial Element coherence. Designed for inline embedding in
   Step 2–7 askuser status-views (HR.M2.3 / HR.P2.8).
5. **Gate alignment** — Gate 1 (Steps 0+1: shape + throughline names),
   Gate 2 (Steps 2+3+4+5: classes + 8 dynamics + story points), Gate 3
   (Steps 6+7+(8) + Validation: crucial element + signposts + 5 hard checks).
6. **SKILL.md Pipeline Overview** updated — Phase 2 row now references
   the 8-Step Worksheet and the
   `novel-architect-structure/methods/storyform/worksheet-loop.md`
   implementation; `## Phase 2` section rewritten with the new sub-phase
   pseudocode and the inline-heuristic delegations.
7. **End-to-end smoke test** — manual walkthrough for `consciousness-novel`
   (Hard-SF, single storyform): 7 askuser turns to fill all worksheet
   slots; rendered an example `architecture.yaml` shape passing all 5
   validation checks. `render_intent` smoke test on real intent.yaml
   shape produced correct status-view markdown.
8. **Slot-list consolidation** — `intent-template.yaml` gained a `_meta`
   block (`_required` + `_optional` lists). `render_intent.py` now reads
   the slot list via `load_slot_lists()` at runtime, with graceful
   fallback to embedded constants if the template is missing / malformed.
   `phase1-intent-capture.md` §1 table marked as "Derived view"
   with a "Regenerated from intent-template.yaml on 2026-05-12" footer.
   Drift between the three locations is now mechanically prevented.
9. **`render_intent.py` slot-state polish** — collapsed redundant
   placeholder checks. The classifier branches into 3 paths now (empty /
   partial / filled); a bare `<PLACEHOLDER>` returns empty inside the
   single `_PLACEHOLDER in value` check via an explicit equality guard.

**Tests:** 31 new pytest cases in
`skills/novel-architect/render/tests/test_render_intent.py` (slot_state
classification matrix + load_slot_lists fallback paths + module constant
wiring). All pass: `python3 -m pytest skills/novel-architect/render/tests/ -v` → 31/31.

## Links

- Parent epic: [Task 070](../070-novel-architect-v110-epic/task.md)
- Blocked by: [Task 071](../071-novel-architect-submodule-refactor/task.md)
- Blocks: [Task 073](../073-novel-architect-hard-rules-validation/task.md) (Hard Rules validation needs worksheet structure)
- PR #101 review: [comment 4422239250](https://github.com/netzkontrast/agency/pull/101#issuecomment-4422239250) §2.5 + §2.7
- Source spec: [`dramatica-theory/references/00-storyform-worksheet.md`](../../skills/dramatica-theory/references/00-storyform-worksheet.md), [`dramatica-theory/references/10-decision-heuristics.md`](../../skills/dramatica-theory/references/10-decision-heuristics.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`SKILLS.md`](../../SKILLS.md), [`AGENTS.md`](../../AGENTS.md) (Narrative Ontology NO.2)
