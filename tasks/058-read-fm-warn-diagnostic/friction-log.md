---
type: note
status: active
slug: 058-read-fm-warn-diagnostic-friction
summary: "Friction log for Task 058 closure. Highest Frustration Level: FL1."
created: 2026-05-08
updated: 2026-05-08
---

# Task 058 — Friction Log

Highest Frustration Level: FL1

## Summary

Mostly smooth. One self-corrected misstep.

## Entries

- **FL1 — initial trigger condition was too narrow.** First implementation
  raised the WARN only inside `except Diag` under `strict=False`, but
  `parse_frontmatter(strict=False)` never raises — it silently drops
  bad lines. The first falsification test (depth-2 nesting) caught
  this within one run-cycle. Restructured `read_fm_with_diag` to
  always run the strict pass internally and surface the WARN even
  when the lenient salvage produced a partial dict. Adjusted the
  test expectation (the salvaged dict is no longer required to be
  empty when a WARN is emitted; only the diagnostic itself matters).

## What worked

- `tools/tests/fm/test_falsification_attacks.py` already had the
  P-series scaffold; adding TestP6 with five new cases took ~5 min
  and ran in 0.07s.
- The tuple-return surface was a clear win over the module-sink
  alternative; no thread-race concern, no global state, back-compat
  preserved by keeping `read_fm()` as a one-line wrapper.

## What did not work

- Pre-existing test isolation in `tools/tests/fm/` is fragile: the
  full pytest run reports 6 `test_fm_wrapper` failures regardless of
  whether my changes are applied (verified by stashing + re-running).
  Surfaced as out-of-scope for this Task; recorded here so a future
  Task can deflake.
