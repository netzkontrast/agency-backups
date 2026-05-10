---
type: task
status: active
slug: promote-check-body-to-gating
summary: "Promote tools/fm/validate.py --check-body to a gating step in tools/check-governance.sh and codify body-shape repair tier (T3) for closed Tasks in MAINTENANCE.md."
created: 2026-05-10
updated: 2026-05-10
task_id: "064"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts:
  - repo-coherence-check
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - tools/check-governance.sh
  - prompts/repo-coherence-check/prompt.md
  - MAINTENANCE.md
  - tasks/039-maintenance-spec-integration/task.md
---

# Task 064 — Promote --check-body to gating and codify body-shape repair tier

## Goal

The body-schema check `tools/fm/validate.py --check-body` MUST run as a gating step inside `tools/check-governance.sh`, the coherence-check prompt MUST drop its stale "Task 019 default-on" forward reference, and `MAINTENANCE.md §1` MUST classify body-shape ERROR repairs on `task_status: done` files as T3 (Structural). The Task is `done` when (a) `tools/check-governance.sh` invokes `python3 tools/fm/validate.py --check-body` against the operational corpus and exits non-zero on any F.B.* diagnostic, (b) `prompts/repo-coherence-check/prompt.md §Step 2.5` no longer carries the parenthetical `(Task 019)` forward reference, (c) `MAINTENANCE.md §1`'s tier table contains an explicit row covering body-shape repairs on closed Tasks (T3), and (d) the two pre-existing F.B.1 ERRORs on `tasks/039-maintenance-spec-integration/task.md` are either repaired (via this Task's Plan step 5) or surfaced as a follow-up T3 cleanup Task.

## Context

The 2026-05-10 coherence run discovered that `python3 tools/fm/validate.py --check-body` emits two F.B.1 ERROR diagnostics against `tasks/039-maintenance-spec-integration/task.md` (`## Goal` shape mismatch, `## Links` shape mismatch). The errors pre-existed the delta; the Task is now `task_status: done`, which makes editing its body sections a T3 (Structural) action per `MAINTENANCE.md §1`. The coherence run cannot fix them in-place. Three structural gaps were identified:

1. `tools/check-governance.sh` has zero references to `--check-body`; the body-schema rule is invocable manually but never gated. Body-shape ERRORs accumulate silently between coherence runs.
2. `prompts/repo-coherence-check/prompt.md` Step 2.5 still says `When --check-body lands as default-on (Task 019), promote here`. Task 019 (`fm-toolchain-suite-integration`) is `task_status: done`. The forward reference is stale and the promotion never landed.
3. `MAINTENANCE.md §1` does not classify body-shape ERROR repairs on closed Tasks. The current tier table covers heading renames (T3) and frontmatter mutations (T1/T2), but the body-shape repair pattern (e.g. converting an `unordered_list` to a `link_list` in `## Links`) sits in a gap.

## Plan

1. Wire `--check-body` into `tools/check-governance.sh` as an explicit step (placed after step `[1/6]` `fm-validate --type-check` so the type-check exit code is preserved). The new step MUST scan `tasks/`, `prompts/`, and operational `research/` workspaces and MUST exit non-zero on any F.B.* diagnostic. Keep the legacy step numbering or re-flow per `research/toolchain-flip-criteria/output/SPEC.md §3.4`.
2. Edit `prompts/repo-coherence-check/prompt.md §Step 2.5`: drop the `(Task 019)` parenthetical and promote `python3 tools/fm/validate.py --check-body <changed-paths>` from the conditional code-block tail to a mandatory invocation alongside the existing `--type-check` line. Update Reflection gate R2.5 to reference the body-shape rule explicitly.
3. Add a new row to `MAINTENANCE.md §1` repair-permission tier table: "Body-shape repair on `task_status: done` task.md (e.g. reshaping `## Goal` from mixed to paragraph, or `## Links` from unordered_list to link_list)" → T3 (Structural). The new row MUST cite `tools/fm/validate.py --check-body` as the diagnostic surface. Add a Gherkin scenario under the next free anchor (M.B.8) per the §6 closing rule.
4. Repair the two F.B.1 errors on `tasks/039-maintenance-spec-integration/task.md` as part of the Task 064 Plan (reshape `## Goal` to a single paragraph and `## Links` to a `link_list`). Per the new T3 row added in step 3, this work is the Task's own deliverable and is therefore in-scope; subsequent body-shape errors on already-closed Tasks will follow this same pattern (file a Task; do not edit during a coherence run).
5. Run `tools/check-governance.sh` end-to-end against `HEAD` and verify zero F.B.* diagnostics survive the pre-commit gate. Add a regression test under `tools/tests/fm/test_body_schema.py` if one does not already cover the gating wiring.

## Todo

- [ ] 1. Edit `tools/check-governance.sh` to invoke `tools/fm/validate.py --check-body` with non-zero exit on F.B.* diagnostics.
- [ ] 2. Edit `prompts/repo-coherence-check/prompt.md §Step 2.5` to drop the stale `(Task 019)` parenthetical and promote `--check-body` to a mandatory line.
- [ ] 3. Edit `MAINTENANCE.md §1` repair-tier table to classify body-shape repairs on closed Tasks as T3, with a Gherkin acceptance scenario at anchor M.B.8.
- [ ] 4. Repair the two F.B.1 ERRORs in `tasks/039-maintenance-spec-integration/task.md` (`## Goal` paragraph shape, `## Links` link_list shape).
- [ ] 5. Add or extend a test in `tools/tests/fm/test_body_schema.py` covering the gating wiring.
- [ ] 6. Run `tools/check-governance.sh` end-to-end; verify zero F.B.* diagnostics; record the run in `maintenance/run-log.md` per §2.3.

## Links

- Executing prompt: [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md)
- Source SPEC: [`research/toolchain-flip-criteria/output/SPEC.md`](../../research/toolchain-flip-criteria/output/SPEC.md)
- Governing spec: [`MAINTENANCE.md`](../../MAINTENANCE.md) §1.
- Gating script: [`tools/check-governance.sh`](../../tools/check-governance.sh).
- Pre-existing F.B.1 source: [`tasks/039-maintenance-spec-integration/task.md`](../039-maintenance-spec-integration/task.md).
- Found by: [`maintenance/run-log.md`](../../maintenance/run-log.md) entry 2026-05-10.
