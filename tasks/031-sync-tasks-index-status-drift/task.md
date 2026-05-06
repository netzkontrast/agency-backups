---
type: task
status: active
slug: sync-tasks-index-status-drift
summary: "Sync the 10 stale Status: bullets in tasks/readme.md to match each Task's task_status frontmatter, and add a tasks-index-sync linter check that fulfils TASK.md §7.11 (deferred from Task 019)."
created: 2026-05-06
updated: 2026-05-06
task_id: "031"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tasks/readme.md
  - tools/fm/
  - tools/check-governance.sh
  - TASK.md
---

# Task 031 — Sync Tasks-Index Status Drift + Land §7.11 Linter

## Goal

Bring [`tasks/readme.md`](../readme.md) into byte-level agreement with every `tasks/<NNN>-<slug>/task.md`'s `task_status` frontmatter, AND land the §7.11 mechanical check (`tools/fm/query.py status,supersession --diff tasks/readme.md`, originally promised by Task 019) so the same drift cannot accumulate again. Success is falsifiable: after this Task closes, the script in §Plan-1 MUST emit zero mismatches AND `tools/check-governance.sh` MUST exit non-zero on any future commit that re-introduces a drift.

## Plan

1. **Re-run the drift detector to confirm the population.** The shell loop below MUST report exactly the 10 mismatches recorded in §Snapshot. Any new mismatch since 2026-05-06 SHOULD be folded in.

   ```bash
   for d in tasks/[0-9]*/; do
     task=$(basename "$d")
     ts=$(grep "^task_status:" "$d/task.md" | awk '{print $2}')
     rline=$(grep "^- \[\`$task" tasks/readme.md)
     rstatus=$(echo "$rline" | grep -oE "Status: \`[^\`]+\`" | head -1 | sed 's/Status: `//; s/`$//')
     [ "$ts" != "$rstatus" ] && echo "MISMATCH: $task task.md=$ts vs readme=$rstatus"
   done
   ```

2. **Apply the textual fixes in `tasks/readme.md`.** Each mismatch is a one-line edit: replace `Status: \`<old>\`` with `Status: \`<new>\``. For Tasks whose `task.md` is `task_status: done` but the bullet currently reads `open`/`in_progress`/`blocked`, the agent MUST also drop any "(blocked on Task NNN)" parenthetical that is no longer accurate. Closed-Task bullets MUST remain otherwise unchanged (no prose rewrite).

3. **Bump the index `updated:`** to today's ISO date via `python3 tools/fm/edit.py --bump-updated tasks/readme.md`.

4. **Add the §7.11 mechanical check.** Implement `tools/fm/query.py status,supersession --diff tasks/readme.md` (or an equivalent dispatcher subcommand `tools/fm/fm.py index-diff`) that:
   - Reads every `tasks/<NNN>-<slug>/task.md` and extracts `(task_id, slug, task_status, task_superseded_by)`.
   - Parses every `^- [\`<NNN>-<slug>/\`]…` bullet in `tasks/readme.md` and extracts the cited `Status:` and any "→ superseded by" suffix.
   - Emits one diagnostic per row that disagrees, plus one diagnostic per orphaned bullet (folder absent on disk) and one per missing bullet (folder present, no bullet). Diagnostic format: `tasks/readme.md::ERROR:T.7.11:<NNN>-<slug> bullet status=<bullet> but task.md task_status=<frontmatter>`.

5. **Wire the check into `tools/check-governance.sh`.** Add a step `[N/N] Tasks-index freshness` that runs the new check and contributes to the `FAIL` exit code. The check MUST be sub-second (< 0.5 s) on the current corpus.

6. **Amend `TASK.md §7.0`** table row §7.11 to point at the concrete linter (replace "Task 019" with the post-implementation invocation surface).

7. **Append a `friction-log.md`** with `FL[0-3]` declaration, summary of mismatches found vs fixed, and the diagnostic output of `tools/check-governance.sh` after the linter lands (MUST show 0 errors).

## Todo

- [ ] 1. Confirm the mismatch population by running the §Plan-1 detector against current HEAD.
- [ ] 2. Apply the 10 textual `Status:` fixes in `tasks/readme.md`.
- [ ] 3. Bump `tasks/readme.md`'s `updated:` field.
- [ ] 4. Implement `--diff tasks/readme.md` (or `fm index-diff`) per §Plan-4.
- [ ] 5. Add unit tests in `tests/fm/test_index_diff.py` covering: in-sync (0 errors), single status drift, orphan bullet, missing bullet, supersession-suffix mismatch.
- [ ] 6. Wire the new check into `tools/check-governance.sh` and verify CI exits 0 on a clean tree.
- [ ] 7. Amend `TASK.md §7.0` row §7.11 with the concrete linter invocation.
- [ ] 8. Produce `friction-log.md` with an `FL[0-3]` declaration.

## Snapshot — drift observed at coherence run 2026-05-06

```
007-reconcile-closed-task-linkage         task.md=done         readme=open
008-harden-coherence-baseline-protocol    task.md=in_progress  readme=open
012-review-pr-29                          task.md=done         readme=in_progress
015-integrate-dramatica-ncp-skills        task.md=done         readme=in_progress
016-flexible-frontmatter-toolchain        task.md=done         readme=open
017-migrate-repo-to-flexible-toolchain    task.md=done         readme=blocked
018-fm-section-editor                     task.md=done         readme=open
019-fm-toolchain-suite-integration        task.md=done         readme=open
020-audit-prompt-fm-validate-conformance  task.md=done         readme=open
021-apply-fm-edit-to-deferred-coherence   task.md=done         readme=open
```

## Links

- Found by: coherence-check run 2026-05-06 (see [`maintenance/run-log.md`](../../maintenance/run-log.md)).
- Spec citation: [`TASK.md §4.8`](../../TASK.md) (mandatory tasks-index update) and [`TASK.md §7.11`](../../TASK.md) (linter mapping).
- Predecessor scope: [`Task 019`](../019-fm-toolchain-suite-integration/task.md) deferred this check; this Task picks it up.
- Related: [`Task 025`](../025-maintenance-spec-remaining-findings/task.md) (F2/F3/F4/F7 — separate maintenance-spec gaps).
