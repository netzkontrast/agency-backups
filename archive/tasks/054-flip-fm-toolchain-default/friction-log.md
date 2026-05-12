---
type: note
status: active
slug: 054-flip-fm-toolchain-default-friction
summary: "Friction log for Task 054 closure. Highest Frustration Level: FL1."
created: 2026-05-08
updated: 2026-05-08
---

# Task 054 — Friction Log

Highest Frustration Level: FL1

## Summary

Mostly mechanical, with one scope-narrowing decision worth recording.

## Entries

- **FL1 — Task spec asked for more than its falsifiable outcome.** The
  task.md Plan included "Retire the four legacy linter scripts;
  either delete or relocate" but `tools/check-maintenance-bypass.py`
  still calls them, and TASK.md / RESEARCH.md / PROMPT.md / SKILLS.md
  / FOLDERS.md / README.md still link them as canonical paths.
  Retiring the scripts in this Task would either break the bypass
  index or require a multi-spec T3 sweep.

  Resolution: narrow the scope to the Goal's falsifiable outcome —
  the `FM_TOOLCHAIN` env var is gone, `tools/fm/validate.py` is the
  only frontmatter linter invoked from the gate. Recorded follow-up
  Tasks in `notes.md` for the rule-folding and spec-doc rewrites.

- **FL0 — Edits otherwise straightforward.** Removed the
  `FM_TOOLCHAIN` branch + advisory legacy call from
  `tools/check-governance.sh:23-48`; updated PRE_COMMIT.md §7 + §7.A
  + precedence rules; updated MAINTENANCE.md §1.1; verified no
  remaining env-var reads anywhere; ran the gate clean.
