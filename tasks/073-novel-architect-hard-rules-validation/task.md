---
type: task
status: active
slug: novel-architect-hard-rules-validation
summary: "Implement 12 Hard Rules (H1-H12) from dramatica-theory/00-storyform-validation.md as a Phase 2 Gate 3 pre-write check in novel-architect-structure. Failing rules surface in the Gate 3 status-view; user must fix or explicitly override before approval. Prevents storyform schema-drift before NCP skeleton is written."
created: 2026-05-11
updated: 2026-05-11
task_id: "073"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - "072"
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - skills/novel-architect-structure/phases/phase2-narrative-architecture.md
  - skills/novel-architect-structure/methods/validation/hard-rules-check.md
  - skills/novel-architect-structure/assets/hard-rules-checklist.md
---

# Task 073 — Hard Rules Validation (H1-H12)

## Goal

Insert a **Hard Rules pre-Gate-3 validation step** in Phase 2 (Narrative Architecture). The 12 Hard Rules from [`dramatica-theory/references/00-storyform-validation.md`](../../skills/dramatica-theory/references/00-storyform-validation.md) are run against `architecture.yaml` before Gate 3 final approval. Any failing rule appears in the status-view with severity marker; user must fix or document an override-rationale.

`done` when:
1. Phase 2.7 (new sub-phase between Gate 2 and Gate 3) implements H1-H12 checks
2. New `methods/validation/hard-rules-check.md` documents each rule + test
3. New `assets/hard-rules-checklist.md` — 1-page checkable list (H1-H12 + 8 soft checks)
4. Validation failures render in `architecture-status-view.md` with 🔴 / ⚠ markers
5. Gate 3 askuser prompts include "Hard Rules: X/12 pass" status
6. Smoke test: deliberately-bad architecture (e.g. OS+MC in same Class) → validation surfaces H2/H3 violation

## Hard Rules (H1-H12) summary

From `dramatica-theory/references/00-storyform-validation.md`:

- **H1:** Exactly four throughlines named (OS, MC, IC, SS)
- **H2:** Each Class (Universe/Physics/Mind/Psychology) used exactly once
- **H3:** OS-SS and MC-IC are complementary dynamic pairs
- **H4:** Story Goal at Type level
- **H5:** Crucial Element at Element level
- **H6:** Crucial Element in OS throughline
- **H7:** MC Resolve ↔ Crucial Element agreement
- **H8:** IC sits on dynamic-pair partner of MC's Element
- **H9:** No character carries both Elements of a pair
- **H10:** Outcome × Judgment yields one of four endings (Success/Good, Success/Bad, Failure/Good, Failure/Bad)
- **H11:** Story Driver consistent across all act transitions (Action OR Decision throughout)
- **H12:** All four Signposts of a throughline are the four Types of that throughline's Class

## Plan

1. Read `dramatica-theory/references/00-storyform-validation.md` for canonical H1-H12 + soft-check texts
2. Decide implementation location:
   - Python helper script in `skills/novel-architect-structure/render/validate_hard_rules.py` (parses architecture.yaml + NCP, returns list of pass/fail)?
   - Pure-prose checklist in skill file that the agent walks manually?
   - Hybrid: Python script for mechanical checks (H1, H2, H3, H10), agent-narrative for context-dependent (H7, H11)
3. Implement chosen approach
4. Integrate into Phase 2.7 (new sub-phase between Gate 2 and Gate 3)
5. Update `architecture-status-view.md` template to include Hard Rules pass/fail table
6. Document soft checks (8 advisory) — same path, lower severity
7. Smoke test with a deliberately-bad architecture

## Todo

- [ ] 1. Implementation decision: pure-prose vs Python helper vs hybrid
- [ ] 2. Author `methods/validation/hard-rules-check.md`
- [ ] 3. Author `assets/hard-rules-checklist.md`
- [ ] 4. Insert Phase 2.7 in `phase2-narrative-architecture.md`
- [ ] 5. Update status-view rendering (architecture-status-view.md template)
- [ ] 6. Smoke test
- [ ] 7. Frontmatter validation

## Links

- Parent epic: [Task 070](../070-novel-architect-v110-epic/task.md)
- Blocked by: [Task 072](../072-novel-architect-phase2-worksheet-loop/task.md) (needs 8-step worksheet for clear pre-Gate-3 trigger point)
- Source spec: [`dramatica-theory/references/00-storyform-validation.md`](../../skills/dramatica-theory/references/00-storyform-validation.md)
- Related: [Task 074](../074-novel-architect-anti-patterns/task.md) (Anti-Patterns) — separate diagnostic, runs alongside Hard Rules
- Governing specs: [`TASK.md`](../../TASK.md), [`AGENTS.md`](../../AGENTS.md) (NO.2 — Dramatica ontology resolution)
