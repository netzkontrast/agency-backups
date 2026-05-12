---
type: task
status: active
slug: relocate-agents-loop-log
summary: "Move the LOOP_LOG runtime-state section out of AGENTS.md (R.19 violation) into maintenance/session-logs/, and ship a WARN-tier linter that prevents runtime-state sections from creeping into root governance specs."
created: 2026-05-07
updated: 2026-05-08
task_id: "055"
task_status: done
task_owner: "claude-opus-4-7"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - AGENTS.md
  - maintenance/session-logs/
  - tools/check-spec-runtime-state.py
  - tools/check-governance.sh
  - tests/check_spec_runtime_state/
---

# Task 055 — Relocate `AGENTS.md` `LOOP_LOG` + Spec Runtime-State Linter

## Goal

`AGENTS.md` lines 340–403 carry a `## LOOP_LOG` section with Jules session iteration records — runtime state living in a governance spec, which `README.md §11.6 R.19` forbids. This Task moves those records to a dedicated location and lands a mechanical guard so the entry-point spec cannot drift back. Falsifiable outcome: `AGENTS.md` contains no runtime-state heading, the records are preserved at a non-spec path, and `tools/check-spec-runtime-state.py` exits non-zero on a fixture that re-introduces the pattern.

## Plan

1. **Create** `maintenance/session-logs/jules-loop-log.md` with the verbatim records lifted from `AGENTS.md` lines 340–403, plus a one-paragraph provenance note.
2. **Strip** the `## LOOP_LOG` heading and body from `AGENTS.md`; replace with a one-line pointer to the new file.
3. **Author** `tools/check-spec-runtime-state.py`: scan root spec files (`AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`, `MAINTENANCE.md`) for headings matching a closed runtime-state vocabulary (`LOOP_LOG`, `SESSION_LOG`, `RUN_LOG`, `ITERATION_LOG`, `STATE`); emit WARN per occurrence, ERROR if `--strict` is set.
4. **Wire** the new linter into `tools/check-governance.sh` as advisory by default.
5. **Test** with three fixtures under `tests/check_spec_runtime_state/`: clean spec, spec with one banned heading, spec with a heading whose body is empty (still flagged).

## Todo

- [ ] Lift records from `AGENTS.md:340-403` into `maintenance/session-logs/jules-loop-log.md`.
- [ ] Strip `LOOP_LOG` from `AGENTS.md`; add pointer line.
- [ ] Author `tools/check-spec-runtime-state.py` (stdlib only, follow `tools/fm/_core.py Diagnostic` shape).
- [ ] Author three pytest fixtures under `tests/check_spec_runtime_state/`.
- [ ] Wire the linter into `tools/check-governance.sh` (advisory).
- [ ] Write `friction-log.md` with FL[0–3] declaration on closure.

## Links

- Parent dispatch: [Task 053](../053-core-architecture-review-followups/) finding B.2.
- Governance violated at branch-time: [`README.md §11.6 R.19`](../../README.md), basis for the fix.
- Affected lines at branch-time: `AGENTS.md` lines 340–403.
