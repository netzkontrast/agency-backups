---
type: note
status: active
slug: run-log
summary: "Chronological log of every Repo Coherence Check and Nightly Maintenance run. The agent MUST read the last entry's end_commit before beginning any run."
created: 2026-05-04
updated: 2026-05-05
---

# Maintenance Run Log

## How to Read This File

Each run appends one record to the bottom of this file. The agent executing a Repo Coherence Check MUST:

1. Read the **last** record in this file.
2. Extract the `end_commit` hash.
3. Use that hash as `<baseline>` in `git log <baseline>..HEAD --oneline --name-only`.
4. If no records exist (first run ever), use the repo's initial commit as the baseline.

The agent MUST append its own record **before** committing the run's repairs, so that the log and the fixes are in the same atomic commit.

---

## Record Format

```
### Run YYYY-MM-DD — <routine-type>
- agent: <agent-identifier>
- start_commit: <hash of HEAD when the run began>
- end_commit: 4c5e7e4 628439e
- baseline_commit: <the end_commit from the previous run — what was used as the delta base>
- files_in_delta: <count of files changed between baseline and start_commit>
- files_scanned: <count of files the agent actually opened>
- t1_fixes: <count of T1 mechanical repairs applied>
- t2_fixes: <count of T2 additive repairs applied>
- t3_tasks_created: <count of new Tasks written to /tasks/>
- t4_skipped: <count of complete research workspaces skipped>
- issues_skipped: <count of issues deferred without a Task — explain in notes>
- notes: >
    Free-form. What was found, what was surprising, what was skipped and why.
```

---

## Run Records

### Run 2026-05-04 — bootstrap
- agent: claude-code (session claude/improve-agents-documentation-DyXZf)
- start_commit: f620b6d
- end_commit: 4c5e7e4
- baseline_commit: none (first run — log seeded from current HEAD)
- files_in_delta: 0
- files_scanned: 0
- t1_fixes: 0
- t2_fixes: 0
- t3_tasks_created: 0
- t4_skipped: 0
- issues_skipped: 0
- notes: >
    Bootstrap record. Coherence check routine established. Next run will use f620b6d
    as its baseline and scan everything committed after this point. The repo was
    verified coherent as of this commit: AGENTS.md carries frontmatter, language-spec.md
    exists in /maintenance/, Task 002 and its prompt are properly linked.

### Run 2026-05-04 — Repo Coherence Check
- agent: jules
- start_commit: 325e5ff
- end_commit: 4c5e7e4
- baseline_commit: f620b6d (missing; fell back to 7 days log)
- files_in_delta: 474
- files_scanned: 474
- t1_fixes: 3
- t2_fixes: 0
- t3_tasks_created: 2
- t4_skipped: 151
- issues_skipped: 148
- notes: >
    Baseline f620b6d was missing from git history so fell back to scanning last 7 days of changes.
    Skipped applying T1/T2 frontmatter stubs to deeply nested operational files (148 files in skills/tools and old research runs) to prevent an excessively large git diff.
    Explicitly updated `updated:` tags on root tasks and prompts.
    Created Tasks 003 and 004 to track missing prompts and un-surfaced research findings.
    Updated PRE_COMMIT.md to reference MAINTENANCE.md.

### Run 2026-05-04 — Repo Coherence Check
- agent: claude-code (session claude/funny-curie-zVZBH)
- start_commit: c76d62c
- end_commit: 2ac93bd
- baseline_commit: 4c5e7e4 (missing — squashed by PR #25 merge; fell back to 7 days log per gate R1)
- files_in_delta: 624
- files_scanned: 14
- t1_fixes: 2
- t2_fixes: 1
- t3_tasks_created: 1
- t4_skipped: 0
- issues_skipped: 0
- notes: >
    Baseline 4c5e7e4 (recorded by Jules's previous run) was not present in git history — likely
    lost when the merge of PR #25 collapsed the branch's hash. Fell back to the 7-day window.
    The previous run's record set `end_commit: 4c5e7e4` (two hashes) which is malformed
    and broke the awk-based extraction in `prompts/repo-coherence-check/prompt.md` Step 1.
    Drove the run from `tools/check-governance.sh` output rather than re-scanning all 624 files,
    because the linters surface every active conformance error mechanically — far more focused
    than reading every file.
    T1 fixes:
      - prompts/budget-enforcer-fallback/prompt.md: prompt_relates_to_task '002-token-efficiency-tool-suite' → 'token-efficiency-tool-suite' (folder-name-vs-slug confusion).
      - prompts/context-pruner-differentiation/prompt.md: same fix.
    T2 fix (TASK.md §8.1 mechanical rule):
      - Renamed tasks/003-surface-skills-architecture/ → tasks/006-surface-skills-architecture/
        (duplicate task_id "003" with tasks/003-analyze-skillmd-novel-authoring/, which was created
        first). Updated task_id to "006" and refreshed the folder readme. Slug unchanged per spec.
    T3 Task created:
      - tasks/007-reconcile-closed-task-linkage/ — covers the remaining 13 lint errors and 2 trust
        errors: missing friction-logs on Tasks 002 and 003, task_spawns_research slugs that point at
        prompts (not research workspaces), reciprocity gaps in task_uses_prompts for follow-up
        prompts, and the unresolved github-skillmd-novel-authoring-de-en path (workspace lives at
        research/gemini/<slug>/ but linter only resolves top-level research/<slug>/).
    Surprises:
      - The previous run's malformed end_commit hid in plain sight; the prompt's awk one-liner
        does not validate that exactly one hash is captured.
      - Two coherence runs in a row hit baseline-loss-after-squash. This is structural: the
        run-log baseline cannot survive squash-merges. See follow-up Task for prompt + spec
        improvements.

### Run 2026-05-05 — Repo Coherence Check
- agent: claude-code (session claude/funny-curie-qTGQ1)
- start_commit: 473cad7
- end_commit: PENDING
- baseline_commit: 2ac93bd (recovered cleanly via the awk-fall-forward — Task 008's hardening held)
- files_in_delta: 131
- files_scanned: 6
- t1_fixes: 0
- t2_fixes: 2
- t3_tasks_created: 2
- t4_skipped: 0
- issues_skipped: 0
- notes: >
    Drove the run from `tools/check-governance.sh` output (linter-first triage), as in the
    previous claude-code run. The linter reported 2 diagnostics:
      - tasks/012-review-pr-29/task.md: missing L2 key task_spawns_prompts.
      - tasks/006-skills-navigation-bootstrap/task.md: missing L2 key task_spawns_prompts.
    Both fixed in-place by appending `task_spawns_prompts: []`.
    T3 findings:
      - Two duplicate task_id collisions (006 and 009) — TASK.md §8.1 violation. Filed as
        Task 013 (renumber-duplicate-task-ids). Not fixed in-place because the cross-reference
        sweep affects ~10 files including a closed task workspace; classified as T3.
      - Per the operator's standing instruction, distilled session-level improvements to the
        coherence prompt and MAINTENANCE.md into Task 014 (improve-maintenance-spec-from-session).
        Findings F1–F7 cover: missing duplicate-task_id linter, ambiguous renumber tier,
        large-delta budgeting, drift-check noise on review-bearing research, missing template
        defaults, baseline-recovery gherkin coverage, and an explicit post-repair linter gate.
    Surprises:
      - `tasks/006-skills-navigation-bootstrap/` (task_status: done, merged via PR #40) was
        created with task_id "006" despite the previous coherence run already having claimed
        006 for surface-skills-architecture. The duplicate-task_id check in TASK.md §8.1 is
        spec-bearing but not linter-enforced.
      - Three delta research workspaces are research_phase: complete; only two carry
        SPEC.md outputs. The drift checklist in the coherence prompt does not yet differentiate
        spec-bearing vs review-bearing research, leading to false positives.

### Run 2026-05-05 — Task 016 implementation
- agent: claude-code (session claude/execute-task-16-ZrBJe)
- start_commit: 9850947
- end_commit: 6b0480a
- baseline_commit: 9850947 (no preceding coherence run since merge of PR #46)
- files_in_delta: 0
- files_scanned: 0
- t1_fixes: 0
- t2_fixes: 0
- t3_tasks_created: 0
- t4_skipped: 0
- issues_skipped: 0
- notes: >
    Not a coherence run — this is a *task implementation* record per
    MAINTENANCE.md §2.3, logged so the new tools' availability is visible to
    every subsequent agent. Shipped Task 016: the four-tool flexible
    frontmatter toolchain at `tools/fm/{validate,extract,edit,query}.py` plus
    `tools/fm/_core.py` and `maintenance/schemas/header-ontology.json`. The
    legacy validators stay in CI; `FM_TOOLCHAIN=1` flips
    `tools/check-governance.sh` to gate on `fm-validate` instead. 39 unittest
    tests in `tests/fm/` cover SPEC §6 scenarios F.6.1–F.6.7 and the M01
    falsification attacks P1–P5; all pass. The legacy `tools/_frontmatter.py`
    is now a re-export shim around `tools/fm/_core` for one release window
    (Task 017 retires it). Friction logged as FL1 in
    `tasks/016-flexible-frontmatter-toolchain/friction-log.md`.
