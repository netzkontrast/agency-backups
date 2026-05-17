---
type: note
status: active
slug: improve-maintenance-spec-may-2026-v2-friction
summary: "Session friction log for Task 097 — filed during the 2026-05-17 Repo Coherence Check that surfaced findings F14–F19. FL0 — no tool failures or rework."
created: 2026-05-17
updated: 2026-05-17
---

# Friction Log — Task 097 Filing Session (2026-05-17)

Highest Frustration Level: FL0

## Session scope

Executed the Repo Coherence Check routine ([`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md)) from baseline `6e4859d` (the previous run's `end_commit`, an `adr-synthesize` record) to HEAD `867453e`. The delta covered 40+ files across the Task 094 Skills Integration Epic merge and several Codex-review rounds. Drove triage from `tools/check-governance.sh` output (linter-first triage — the same pattern Run 2026-05-04 claude-code session established as the canonical approach).

## What surfaced

1. **T.7.11 drift** — `tasks/readme.md` bullet for Task 093 said `Status: open` but `task.md task_status: done`. T1 mechanical fix landed in-place via direct edit + `tools/fm/edit.py --bump-updated`.
2. **Dup-id `090` collision** — `tools/fm/check-duplicate-task-id.py` reported `090-codex-pr-review` (`in_progress`) ↔ `090-review-pr109-archive-spec` (`done`) without supersession reciprocity. Per §3.5, evaluated the four auto-fire predicates:
   - P1 single collision pair ✓
   - P2 no covering open Task in `task_affects_paths` ✓
   - P3 ≥1 open member (`090-codex-pr-review` is `in_progress`) ✓
   - P4 `routine_type: coherence-check` ✓
   All four held → filed Task 096 autonomously.
3. **Six MAINTENANCE.md spec gaps** — distilled F14–F19 into Task 097 (this Task) following the structural pattern set by Task 068's F8–F13 framing.

## What worked

- Linter-first triage scaled cleanly to a 40-file delta; reading `check-governance.sh` output was faster than walking every changed file.
- `tools/fm/check-duplicate-task-id.py` surfaced the collision before any cross-reference chain rewrite became necessary.
- The §3.5 auto-fire-predicate algorithm produced an unambiguous fire decision — no agent judgment was required beyond evaluating four boolean facts.

## What rubbed

(Each entry is one of the six findings F14–F19; see [`task.md`](./task.md) for the full statement and concrete-diff options.)

- **F14** — Evaluating §3.5 predicate P2 (no covering open Task) required `grep -l` + `grep -rn task_affects_paths` across the corpus. The linter could surface this directly.
- **F15** — The promised `FM_DUPLICATE_TASK_ID_STRICT` default flip never landed despite Task 043 closing. The 090 collision proves the spec's flip condition was not mechanically verified.
- **F16** — "Corpus clean" in §3.2 has no numeric threshold; agent cannot tell when the dynamic-readme-partition linter is eligible for promotion.
- **F17** — `MAINT_STALE_DAYS` per-routine binding is illustrative-only; the routine doesn't enforce its window.
- **F18** — §1.0.1 commit-message-rationale rule is socially enforced; no linter walks `git log` for it.
- **F19** — §3.6 acknowledges the over-sampling risk but provides no mechanical guard.

## What I'd do next

The natural next step is to execute Task 097 — pick one finding (probably F14 or F15 first; both are mechanical and high-leverage) and land the diff. The Task is structured so each finding closes independently with a one-paragraph friction-log disposition, mirroring the Task 068 pattern that closed F8–F13 over multiple sessions.

## Frustration declaration

Highest Frustration Level: FL0

No tool failures, no rework, no contradictions encountered. The routine performed as designed: it found drift, it found a collision, it surfaced enforcement gaps, it filed Tasks. The friction-log itself documents the patterns that argue for further mechanization (F14–F19), but the routine's *execution* during this session was frictionless.
