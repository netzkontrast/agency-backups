---
type: note
status: active
slug: novel-architect-hard-rules-validation-friction-log
summary: "Friction log for Task 073 — Hard Rules H1-H12 (part of Task 070 Epic close). FL1 single-session inclusion."
created: 2026-05-11
updated: 2026-05-11
---

# Friction Log — Task 073 (Hard Rules H1-H12)

**Highest Frustration Level: FL1**

## What landed

`novel-architect-structure/methods/validation/hard-rules.md` + `assets/hard-rules-check.md` written. All 12 hard rules from `00-storyform-validation.md` enumerated with auto-checkable flag + Gate-binding.

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

`tools/check-hard-rules.py` CLI linter deferred. Soft-rule set not yet enumerated.

## Closing Procedure

- [x] Friction log written with FL declaration (this file)
- [x] tasks/readme.md index synced via Epic close
- [x] tools/check-governance.sh — passes via Epic close commits
- [x] PR — see Task 070 PR for the bundled close
