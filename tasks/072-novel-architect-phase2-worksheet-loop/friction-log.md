---
type: note
status: active
slug: novel-architect-phase2-worksheet-loop-friction-log
summary: "Friction log for Task 072 — Phase 2 Worksheet-Loop (part of Task 070 Epic close). FL1 single-session inclusion."
created: 2026-05-11
updated: 2026-05-11
---

# Friction Log — Task 072 (Phase 2 Worksheet-Loop)

**Highest Frustration Level: FL1**

## What landed

`novel-architect-structure/methods/storyform/worksheet-loop.md` written. Codifies the Dramatica `00-storyform-worksheet.md` slot order as the SSoT for Phase 2 — `architecture.yaml` writes follow the worksheet sequence; Gate 1/2/3 mappings explicit.

## FL1 sources

- **Sub-task closed as part of Task 070 Epic batch.** Single-session Epic close
  meant that this sub-task's review/iterate cycle was compressed — depth was
  traded for breadth. Method files landed at "lean but real" depth referencing
  the source `dramatica-theory` corpus rather than re-deriving content.
- **Pre-existing schema-mirror drift in `maintenance/schemas/l2-skill.schema.json`**
  was repaired in the Epic close commits (regenerated via `tools/fm/gen_schema_mirror.py`).
  Not a defect of this sub-task; logged here so reviewers don't attribute it to
  this work.

## Sequel work

CLI linter `tools/check-worksheet-order.py` deferred to a sequel task.

## Closing Procedure

- [x] Friction log written with FL declaration (this file)
- [x] tasks/readme.md index synced via Epic close
- [x] tools/check-governance.sh — passes via Epic close commits
- [x] PR — see Task 070 PR for the bundled close
