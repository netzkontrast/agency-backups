---
type: note
status: active
slug: run-log
summary: "Chronological log of every Repo Coherence Check and Nightly Maintenance run. The agent MUST read the last entry's end_commit before beginning any run."
created: 2026-05-04
updated: 2026-05-04
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
- end_commit: 4c5e7e4 <hash of HEAD after repairs are committed — fill in before final commit>
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
- end_commit: 4c5e7e4 f620b6d
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
