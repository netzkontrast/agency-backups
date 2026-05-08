---
type: index
status: active
slug: maintenance-session-logs
summary: "Append-only runtime-state logs lifted out of root governance specs (Task 055). One file per agent; no cross-file editing."
created: 2026-05-08
updated: 2026-05-08
---

# `/maintenance/session-logs/`

**What is this folder?** Per-agent, append-only runtime state — the
records each agent writes once per loop iteration. Lives here, not in
the root governance specs, because `README.md §11.6 R.19` forbids
runtime-state sections from the entry-point files.

**Why is it here?** Task 055 lifted Jules' `## LOOP_LOG` block out of
`AGENTS.md` (lines 442–504 at branch-time) and the matching
`tools/check-spec-runtime-state.py` linter now flags any
re-introduction of the pattern at pre-commit time.

## Linked Navigation

- [`jules-loop-log.md`](./jules-loop-log.md) — Jules per-iteration
  records.

## Conventions

- One file per agent (`<agent>-loop-log.md`).
- Append-only; no rewriting prior iteration entries.
- Each iteration is an `### Iteration <n> — <date>` H3 block. The H2
  heading is `## Records`, never one of the closed-vocabulary names
  (`LOOP_LOG`, `SESSION_LOG`, `RUN_LOG`, `ITERATION_LOG`, `STATE`) —
  the linter at `tools/check-spec-runtime-state.py` only scans root
  specs for those names, but keeping them out of session-logs too
  preserves the substrate-vs-state separation.
- Frontmatter MUST be L1 Vault Core (`type: note`).

## Assumptions Log

(none)
