---
type: note
status: active
slug: task-031-friction-log
summary: "Friction log for Task 031 — sync 13 stale Status: bullets in tasks/readme.md against each Task's task_status frontmatter, add missing 042 entry, and land the §7.11 tasks-index linter that Task 019 deferred."
created: 2026-05-07
updated: 2026-05-07
---

# Friction Log — Task 031

## FL Declaration (FRUSTRATED.md FL[0-3])

**FL: 1** — Execution was straightforward; the only friction was that the §Snapshot block in `task.md` (10 mismatches at coherence run 2026-05-06) had drifted further by the time this Task ran (13 mismatches at HEAD = `8fc223d`, 2026-05-07). Per §Plan-1's "any new mismatch since 2026-05-06 SHOULD be folded in" instruction, the three additional mismatches were folded into the textual fix without spec amendment.

## Frictions

### F1 — §Snapshot drifted between Task filing and Task execution

**What.** The Task was filed on 2026-05-06 citing 10 mismatches. By the time it executed (2026-05-07), three additional mismatches had accumulated: `030-cleanup-dramatica-skills-corpus` flipped to `done` (PR #68 merge), `031-adr-tooling-impl` flipped to `done` (PR #67 merge), and Task 042 was filed (`042-dramatica-nav-followups`) without a corresponding bullet in `tasks/readme.md`. The drift detector at `task.md` §Plan-1 reported all 13 mismatches.

**Why it didn't block.** §Plan-1 explicitly anticipates this case: "Any new mismatch since 2026-05-06 SHOULD be folded in." The fix scope expanded from 10 → 13 mismatches without requiring a spec amendment. The `042-dramatica-nav-followups` row had no bullet at all (the detector reported `readme=` empty) — handled by **adding** a new bullet to the contents list rather than editing an existing one.

**Resolution.** All 13 mismatches reconciled:
- 11 status-drift bullet edits (`007`, `008`, `012`, `015`, `016`, `017`, `018`, `019`, `020`, `021`, `030`, `031-adr-tooling-impl`, `012-review-pr-29`).
- 1 stale-parenthetical drop (`017` was `blocked (gated on Task 016)`; `016` is now `done`, so the parenthetical was removed).
- 1 stale-parenthetical drop (`021` was `open (blocked by [017])`; `017` is now `done`, so the parenthetical was removed).
- 1 stale-parenthetical drop (`031-adr-tooling-impl` was `in_progress (PR open; flips to done on merge)`; PR #67 has merged, parenthetical removed).
- 1 new bullet added for `042-dramatica-nav-followups` (Status: `open`).

The post-fix detector reports zero mismatches (validated by both the §Plan-1 awk loop and the new `tools/fm/index_diff.py`).

### F2 — TASK.md §7.0 row §7.11 referenced a tool that was never built

**What.** TASK.md §7.0 row §7.11 cited `tools/fm/query.py status,supersession --diff tasks/readme.md` (Task 019) as the linter for tasks-index freshness. Task 019 closed without delivering the `--diff` flag on `fm-query`. The §7.11 promise had no mechanical surface — exactly the gap that allowed the 10-bullet drift to accumulate silently between 2026-05-04 and 2026-05-06.

**Why it didn't block.** Task 031 is the explicit successor to that deferred work (per its `task.md` §Goal: "land the §7.11 mechanical check ... originally promised by Task 019").

**Resolution.** Implemented `tools/fm/index_diff.py` as a standalone module (also dispatchable via `python3 tools/fm/fm.py index-diff`) rather than bolting `--diff` onto `fm-query`. Rationale: `fm-query`'s API is "comma-joined selectors with optional filters"; tasks-index drift detection has fundamentally different I/O (read frontmatter from N folders, parse markdown bullets from one index, emit diagnostics). A dedicated module keeps `fm-query`'s contract clean and gives the new check its own test surface (`tests/fm/test_index_diff.py`). The §7.0 row was amended to point at the concrete linter.

### F3 — `tools/check-governance.sh` step numbers required renumbering

**What.** The script's step labels used `[N/5]` notation (1/5 through 5/5 across frontmatter/structure/linkage/runlog/ADR). Adding the new tasks-index check required either appending without renumbering (visually misleading) or bumping every step from `/5` → `/6`.

**Resolution.** Renumbered all five existing steps from `[N/5]` to `[N/6]`; appended the new check as `[6/6] Tasks-index freshness (TASK.md §7.11)`. The `index_diff.py` step runs in ~58ms on the current corpus (well under the §Plan-5 sub-second budget).

## Validation

- `python3 tools/fm/index_diff.py` exits 0 against `HEAD`.
- `python3 -m pytest tests/fm/` passes 169 tests (161 pre-existing + 8 new in `test_index_diff.py`); 1 pre-existing skip.
- `tools/check-governance.sh --no-trust` step `[6/6]` exits 0 (the overall script exits 1 only because of an unrelated optional `narrative-ontology validator` failing on a missing `jsonschema` install — that is Task 032's F8 finding, not regression of this Task).
- `tools/fm/index_diff.py` measured at 58ms cold-start.
