---
type: note
status: active
slug: integrate-dramatica-ncp-skills
summary: "Friction log for Task 015 — final entry at closure. Per-FRUSTRATED.md FL declaration."
created: 2026-05-04
updated: 2026-05-05
---

# Task 015 — Friction Log

**FL1** — productive friction with no blockers. The plan ran end-to-end across 18 commits in two contiguous sessions; every friction event was caught in the same session and resolved before close.

## Final summary

The full Task 015 plan (15 steps, plus the strategic-plan recommendations on top of the prompt) executed without abandoning any step. The four parallel-Sonnet pattern paid off twice (Steps 3+7 + 4-fragments; Step 8 navigator scripts). The Pre-Mortem-style discipline of catching delegation-protocol issues mid-execution — rather than at the end — kept friction at FL1 instead of escalating.

## Friction events during execution

### FE1 — Sonnet C populated `ncp_appreciation` on character/plot-dynamic entries with non-NCP-enum values

- **What happened:** my Sonnet C brief said "use `canonical_label` as `ncp_appreciation`" — that produced 8 entries with values like `"Resolve"`, `"Driver"`, `"Approach"` that aren't direct NCP enum strings (per kickoff SPEC §2.5, these kinds map to slot-name patterns).
- **Caught by:** validate.py NCP-enum closure check during Step 8 verification.
- **Fix:** stripped `ncp_appreciation` + `ncp_appreciation_partial` from the 8 entries; documented in commit `e5fde19`.
- **FL impact:** 0 — caught and fixed in the same Step-8 verification cycle.
- **Lesson committed:** `M03-pre-mortem.md` adds *agent-coordination protocol failures* as a sixth Pre-Mortem dimension.

### FE2 — `dynamic-pairs-index.md` listed `Destiny ↔ Fantasy`, conflicting with canonical Fate ↔ Destiny

- **What happened:** Sonnet D faithfully transcribed all 75 pairs from the source-of-truth file, including one that contradicts canonical Dramatica geometry (Fate-Destiny per element-quads.md).
- **Caught by:** validate.py reciprocity check (Destiny couldn't simultaneously pair with Fate AND Fantasy).
- **Fix:** dropped `dp.destiny-fantasy` during Step 4b merge; documented in commit `2d6007c`.
- **FL impact:** 0 — caught and fixed in same step.

### FE3 — Slug-format mismatch between Sonnet C term_file pointers and Step-5 heading-derived slugs

- **What happened:** Sonnet C populated some `term_file` pointers with semantic anchors (`archetypes.md#contents`) instead of canonical-label-derived slugs. Step 5's bulk insertion couldn't auto-match those.
- **Caught by:** Step 5 coverage report — 187 of 293 `## ` headings matched (64%).
- **Mitigation:** documented as known v0.1 limitation in `notes.md`; validate.py emits `term_file-anchor-mismatch` warnings (8 cases) for v0.2 cleanup.
- **FL impact:** FL1 — known limitation, deferred to v0.2 follow-up; doesn't block the navigator's correctness on the 187 matched terms.

### FE4 — Sonnet sub-agent dispatch quota exhausted during Step 9 (test authoring)

- **What happened:** Step 9 brief was dispatched to a Sonnet python-expert; the dispatch returned immediately with a quota-exhaustion notice ("resets 11:50pm UTC").
- **Caught by:** the dispatch itself; quota notice was explicit.
- **Fix:** authored the 42-test pytest suite directly in main context. No quality loss — test count exceeded the 39-minimum and 7/7 Gherkin scenarios are covered.
- **FL impact:** FL1 — small token-budget hit on main context, no schedule impact.

### FE5 — Stop-hook fired on uncommitted Step-11 changes during a back-and-forth turn

- **What happened:** I authored `tools/check-governance.sh` + `PRE_COMMIT.md` edits, paused for user input, and the stop-hook flagged the uncommitted state.
- **Fix:** committed at next opportunity (commit `0a3cfd8`); the linter cleanup of `validate.py` happened in the same commit since both were uncommitted.
- **FL impact:** 0 — process-level reminder, no design impact.

### FE6 — Merge conflict against main (PRs #41 + #43 added overlapping content in `tools/check-governance.sh`)

- **What happened:** `mergeable_state: dirty` after main absorbed PR #41 (lint-runlog.py) at the same insertion point as my Step-11 narrative-ontology validator.
- **Fix:** standard merge, kept both stages in numerical order ([4/4] Run-log → [opt] Narrative-ontology → [5/5] Trust audit). Committed as `8b28062`.
- **FL impact:** 0 — straightforward content-conflict resolution.

### FE7 — Frontmatter linter found Task 015 missing `task_spawns_prompts` after merge

- **What happened:** PR #41 added `task_spawns_prompts` as a mandatory L2 key in TASK.md §3.3; my pre-merge task.md predated this requirement.
- **Caught by:** validate-frontmatter.py during Step-10 verification.
- **Fix:** added `task_spawns_prompts: []` to task.md frontmatter; documented in commit `59f4793`.
- **FL impact:** 0 — auto-detected drift, single-line fix.

## Verdict

**FL1** — productive friction throughout. Zero abandoned steps, zero un-mitigated regressions, zero blocking decisions left for the next session. All seven Gherkin acceptance scenarios pass empirically. The token-cost benchmark cleared the ≥60% gate at 83.4% average reduction.

## Action items (none blocking)

Three v0.2 follow-up tasks recorded in `synthesis/post-impl-acceptance.md`:

- **OQ-X** — multi-quad encoding (`quad_ids: array` schema bump for fractal-distortion entities).
- **OQ-Y** — term_file anchor cleanup (8 hand-authored anchors → canonical slugify).
- **OQ-Z** — DE-locale alias coverage (currently EN-only; DE substitution used for NO.1.2).

These can be standalone follow-up tasks; none are blockers for closing v0.1.
