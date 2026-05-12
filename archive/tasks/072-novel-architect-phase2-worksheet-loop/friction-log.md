---
type: note
status: active
slug: novel-architect-phase2-worksheet-loop-friction-log
summary: "Friction log for Task 072 — Phase 2 Worksheet-Loop implementation (FL1)."
created: 2026-05-11
updated: 2026-05-11
---

# Friction Log — Task 072

**Highest Frustration Level: FL1**

## What worked

- **Worksheet → Sub-phase mapping was clean.** The 8 steps of
  `dramatica-theory/references/00-storyform-worksheet.md` map 1:1 onto
  the 3-gate discipline once you draw the seams at Steps 0+1, 2–5, and
  6+7+Validation. No worksheet steps had to be split across gates; no
  gate had to span an awkward step boundary. The worksheet itself is
  already gate-friendly — v1.0.0's "auto + consult" was hiding a clean
  decomposition.
- **Quick-ref condensation was straightforward.** The decision-heuristics
  source file (`dramatica-theory/references/10-decision-heuristics.md`)
  is already structured by decision point; condensing into the 1-page
  quick-ref was mechanical extraction of indicators + the explicit
  "test that actually works" line per heuristic. The §10 Crucial Element
  coherence section I had to compose from worksheet Step 6's prose,
  since the source file doesn't have a dedicated heuristic block for it.
- **YAML SSoT refactor (PR #101 review §2.5) was small and bounded.**
  Adding the `_meta._required` / `_meta._optional` block to
  `intent-template.yaml` + a runtime loader in `render_intent.py` was
  ~70 LOC including fallback handling and 11 new test cases. The
  `phase1-intent-capture.md` table got a "Derived view" callout + a
  footer date — minimal touch, drift now obvious on inspection.
- **Slot-state polish (PR #101 review §2.7) was a clean collapse.** The
  pre-existing 4-branch ordering had `value == "<PLACEHOLDER>"` then
  `"<PLACEHOLDER>" in value` testing the same data twice. New shape is
  3 branches: empty (None/""/empty-list) → partial-or-empty (string
  containing `<PLACEHOLDER>`, returning empty for the bare string,
  partial otherwise) → filled. 7 parametrized test cases sweep the
  classification matrix including the int-zero / dict / list-with-items
  cases that the original code had no coverage for.
- **Tests run fast and clean.** 31 cases / 0.14 s on the new
  `render/tests/test_render_intent.py`; no pytest fixtures shared with
  other skill modules, so no cross-skill flakiness.

## What rubbed

- **Task 071 ordering — implementation landed under the v1.0.0 monolith,
  then migrated at merge.** Task 072 is `task_blocked_by: 071`. When the
  worksheet-loop / quick-ref work started, this branch was rooted at
  `main` *before* PR #102 (Task 070 Epic close) landed — so the
  sub-skill directories (`skills/novel-architect-structure/`) did not
  yet exist. I implemented under the monolith layout
  (`skills/novel-architect/methods/storyform/worksheet-workflow.md` +
  `skills/novel-architect/assets/decision-heuristic-quick-ref.md`) with
  a forward-compat plan: "when Task 071 lands, files `git mv` to
  `novel-architect-structure/` and internal links survive (they're
  relative)." When PR #102 landed on `main` and I rebased, the
  migration was clean — `worksheet-workflow.md` → `worksheet-loop.md`
  (matching main's lean version's filename) under the sub-skill, and
  the asset to `novel-architect-structure/assets/`. Friction was the
  two-step landing (implement under monolith, migrate at merge), not
  the link-survival itself; the forward-compat plan worked.
- **Architecture-template schema growth.** Adding `name` to throughlines,
  `story_points` block, `crucial_element` block, `signposts` +
  `journeys` arrays, `ending_type`, `genre_mode`, and `worksheet_audit`
  flags doubled the template's surface area. This is correct per the
  worksheet, but `render/render_architecture.py` (Phase 2.13) will need
  updating to surface the new blocks in the architecture-status-view.
  That render-side change is **outside Task 072's scope** (the task is
  about the worksheet-loop *spec*, not the renderer for it) — left for
  a future Task 070-Epic-closure or the Phase 2.13 render-side work
  noted in `methods/storyform/worksheet-loop.md` §7.
- **Bilingual contract surface.** Phase 2 prose stays German (per
  SKILL.md "Bilingual Contract"); the new `decision-heuristic-quick-ref.md`
  is English (matches the dramatica-theory source language). The
  worksheet-loop.md is German prose + English schema/term names —
  same pattern as the existing phase files. §9 of `worksheet-loop.md`
  documents this explicitly so the next maintainer doesn't try to
  translate the worksheet terms.

## What I would do differently

- **Wire render_architecture.py to the new schema in the same task** —
  would have been ~half a day extra but would close the loop end-to-end
  (template → renderer → status-view). I chose to keep Task 072 scoped
  to the *spec* deliverables per the task.md `done when:` list.
- **Add a body-schema check for `worksheet_audit`** in
  `tools/fm/validate.py` so any architecture.yaml claiming Gate-3
  approval but missing `worksheet_audit.step_*_set: true` flags fails
  governance. Currently the audit is by convention, not mechanically
  enforced.

## What I learned

- The dramatica worksheet is **operational by design** — every step has
  a concrete fillable table, a constraint that narrows downstream
  choices (e.g. OS Class determines SS Class via the pair rule), and a
  "the test that actually works" diagnostic. v1.0.0's "auto + consult"
  treated the worksheet as a *reference* when it should have been
  treated as the *algorithm itself*. The lesson generalizes: when a
  source spec already contains step-by-step operational structure,
  don't paraphrase it into vague phase prose — bind directly to it and
  let the source's own structure carry the gate boundaries.

## Frustration tally

- FL0 incidents: many (the work flowed cleanly given the worksheet's
  structure).
- FL1 incidents: 1 (the Task 071 ordering required the forward-compat
  workaround; not a blocker, but adds a "do this on Task 071 merge"
  step).
- FL2+ incidents: 0.

**Highest Frustration Level: FL1.**
