---
type: note
status: active
slug: novel-architect-hard-rules-validation-friction-log
summary: "Friction log for Task 073 — Hard Rules H1-H12. FL1 from original Task 070 Epic close (2026-05-11); FL0 from Audit & Gap-Fill pass (2026-05-12). Highest across sessions: FL1."
created: 2026-05-11
updated: 2026-05-12
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

---

## Audit & Gap-Fill (2026-05-12)

**Highest Frustration Level: FL0**

Follow-up session: audited the v1.1.0 landing against the task's six
acceptance criteria. Two real gaps inside T1/T2 repair scope were filled
in place (AC#3 soft-rule table populated S1–S8; AC#5 Gate 3 `Hard Rules:
X/12 pass` askuser template added). One light addition for AC#6 (`# anchor:
T073.HR.3` on a new H1 Gherkin scenario) gives Task 084 a citation handle.
DRIFT in `task_affects_paths` and the body's "Phase 2.7" wording resolved
via T1 mechanical repair.

### Friction items

(none — FL0)

### Deferred (correctly out of T1/T2 scope)

- AC#4 status-view 🔴/⚠ rendering → **Task 087** (`render_architecture.py`
  JSON-artefact wiring). Building it here would create a parallel
  `worksheet_audit.hard_rules.*` rendering path that Task 087 has to
  immediately replace with the JSON-artefact read.
- AC#6 executable pytest → **Task 084** (`tools/check-hard-rules.py`
  ships the validator + its tests). Writing a smoke test now would
  shadow Task 084's scope.

### Why FL0

The sc-chain (`/sc:analyze → brainstorm → design → workflow → implement`)
surfaced the bleed boundary with Tasks 084/087 early in brainstorm; no
rework, no governance-gate retries, no spec contradictions.

### Post-self-review polish (same session)

A second `/sc:analyze` pass over the just-shipped artefacts surfaced
three cosmetic findings, all fixed in-place on the same branch:

- **M1** — soft-rule table reshaped to 4 columns (`Soft Rule | Statement | Status | Warning (if active)`), mirroring the Hard-Rule table above it.
- **M2** — our two German `MUSS` keywords flipped to English `MUST` (AGENTS.md R1). File-wide DE→EN sweep of RFC 2119 keywords logged as a follow-up assumption rather than widened into this PR.
- **L1** — askuser MUSS-line now carries a `(Renderer-Wiring: siehe Task 087)` forward-pointer so a reader hitting the normative requirement sees the implementation path.

FL0 holds — the polish surfaced from re-reading our own artefacts, not from
friction with the spec or tooling.
