---
type: task
status: active
slug: novel-architect-anti-patterns
summary: "Integrate all 14 anti-patterns (AP-1 to AP-14) from dramatica-theory/11-anti-patterns.md across novel-architect phases 2, 3, and 6 as Pre-Checks. Currently v1.0.0 only references AP-1 (MC ≠ Protagonist). Each AP is classified by phase where it most likely surfaces: Phase 2 (storyform-design APs), Phase 3 (character APs), Phase 6 (drafting APs)."
created: 2026-05-11
updated: 2026-05-11
task_id: "074"
task_status: done
task_owner: "claude-code"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - 071
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - skills/novel-architect-structure/phases/phase2-narrative-architecture.md
  - skills/novel-architect-character/phases/phase3-character-architecture.md
  - skills/novel-architect-scene/phases/phase6-drafting.md
  - skills/novel-architect/methods/diagnostic/anti-patterns.md
---

# Task 074 — Anti-Patterns durchgängig (AP-1 to AP-14)

## Goal

Each of the 14 Anti-Patterns from [`dramatica-theory/references/11-anti-patterns.md`](../../skills/dramatica-theory/references/11-anti-patterns.md) becomes a Pre-Check in the phase where it most likely surfaces. v1.0.0 only references AP-1 (MC ≠ Protagonist) in Phase 3; the other 13 are unused despite being directly applicable.

`done` when:
1. All 14 APs classified to phases (Phase 2 / 3 / 6) with rationale
2. Each phase's detail file lists its assigned APs as a Pre-Check section
3. New `methods/diagnostic/anti-patterns.md` indexes all 14 with diagnostic questions
4. Smoke test: an architecture with intentional AP violations (e.g. abstract Crucial Element = AP-4) triggers warning

## AP Distribution Plan (draft)

### Phase 2 (Storyform-Design APs)

- **AP-1** MC ≠ Protagonist (intentional?)
- **AP-3** Goal at wrong level (must be Type, per H4)
- **AP-5** Class double-assignment (per H2)
- **AP-7** Outcome × Judgment collapsed
- **AP-10** Linear/Holistic mistaken as gender
- **AP-13** Premature Storyform-Lock

### Phase 3 (Character APs)

- **AP-1** (also here, character-resolution flavor)
- **AP-2** Subjective Story forgotten (only "their relationship")
- **AP-14** IC defined only as MC's foil (no independent arc)

### Phase 6 (Drafting APs)

- **AP-4** Crucial Element too abstract to write (vs concrete scene)
- **AP-6** MC Resolve ↔ Crucial Element disagreement in draft
- **AP-8** Mental Sex misapplied as character trait
- **AP-9** Inconsistent Driver (Action vs Decision changes scene-to-scene)
- **AP-11** Signpost confused with Plot Point
- **AP-12** Genre as Mode-of-Expression collapsed into Story Goal

(Note: some APs are duplicated across phases by design — they reveal differently at different stages.)

## Plan

1. Read all 14 APs in detail from `11-anti-patterns.md`
2. Confirm phase-classification (draft above) with sub-task review
3. Author `methods/diagnostic/anti-patterns.md` — index + diagnostic-question per AP
4. For each phase (2, 3, 6): add "Anti-Pattern Pre-Checks" section with assigned APs + diagnostic-question + remediation-pointer
5. Smoke test: deliberately-violated architecture triggers correct AP warning
6. Decide whether AP failures are advisory (warning) or blocking (gate)

## Todo

- [x] 1. Read all 14 APs, confirm classification
- [x] 2. Author `methods/diagnostic/anti-patterns.md`
- [x] 3. Update phase2 detail file with Phase 2 APs as Pre-Check section
- [x] 4. Update phase3 detail file with Phase 3 APs
- [x] 5. Update phase6 detail file with Phase 6 APs
- [x] 6. Smoke test
- [x] 7. Decide advisory vs blocking severity

## Links

- Parent epic: [Task 070](../070-novel-architect-v110-epic/task.md)
- Blocked by: [Task 071](../071-novel-architect-submodule-refactor/task.md) (needs sub-module phase files in place)
- Source spec: [`dramatica-theory/references/11-anti-patterns.md`](../../skills/dramatica-theory/references/11-anti-patterns.md)
- Related: [Task 073](../073-novel-architect-hard-rules-validation/task.md) (Hard Rules — different but complementary diagnostic)
- Governing specs: [`TASK.md`](../../TASK.md), [`AGENTS.md`](../../AGENTS.md)
