---
type: note
status: active
slug: novel-architect-anti-patterns-friction-log
summary: "Friction log for Task 074 — Anti-Patterns AP-1 to AP-14 (part of Task 070 Epic close). FL1 single-session inclusion."
created: 2026-05-11
updated: 2026-05-11
---

# Friction Log — Task 074 (Anti-Patterns AP-1 to AP-14)

**Highest Frustration Level: FL1**

## What landed

`references/anti-patterns.md` synthesises AP-1 to AP-14 with Phase cross-reference index and detection hints per pattern. Two Gherkin acceptance scenarios document the WARN-firing behaviour at Phase 3 and Phase 2.5.

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

Open question whether AP-7 (Driver/Limit throughline-pegging) should upgrade to a hard rule — deferred.

## Closing Procedure

- [x] Friction log written with FL declaration (this file)
- [x] tasks/readme.md index synced via Epic close
- [x] tools/check-governance.sh — passes via Epic close commits
- [x] PR — see Task 070 PR for the bundled close
