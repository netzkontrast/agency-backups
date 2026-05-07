---
type: note
status: active
slug: pr-78-review
summary: "Code review for PR #78 — Land Task 032: Improve maintenance spec and run-log semantics (F8–F13). One critical T1 violation, two moderate gaps, three minor issues, and five positive calls."
created: 2026-05-07
updated: 2026-05-07
---

# Code Review — PR #78: Land Task 032 — Improve Maintenance Spec and Run-Log Semantics

**PR:** [#78 Land Task 032: Improve maintenance spec and run-log semantics](https://github.com/netzkontrast/agency/pull/78)
**Branch:** `claude/close-maintenance-spec-task-Tx7bx` → `main`
**Reviewer:** claude-code (session `claude/brave-darwin-52I86`)
**Date:** 2026-05-07

---

## § RFC 2119

The key words MUST, MUST NOT, SHOULD, and MAY in this document are to be
interpreted as described in RFC 2119 when, and only when, they appear in all
capitals.

---

## Summary Verdict

Task 032 lands five of six findings cleanly (F8, F9, F11, F12, F13) and provides a well-reasoned delegation record for F10. The F13 cross-branch collision guard is the highest-impact change in the PR. However, **one critical T1 violation (stale `updated:` on MAINTENANCE.md) and two moderate omissions require attention before merge is unconditional.** The minor issues are non-blocking but SHOULD be absorbed into Task 025 or Task 044.

---

## Positive Findings

### P-1 — F13 Cross-Branch Collision Guard is the Highest-Impact Change

**Location:** `prompts/repo-coherence-check/prompt.md` Step 4.

The two-command bash recipe (`ls tasks/ | sort` + `git ls-tree origin/main tasks/ | grep …`) is concrete, actionable, and directly addresses the root cause of the three prior collisions (Tasks 013, 024, 043). The explicit "Skipping the cross-branch step is the recurring root cause" sentence earns its place — it is a warning, not rationale prose, and a future agent running the routine cannot miss it.

### P-2 — F8 Graceful-Degrade Architecture is Correct

**Location:** `tools/dramatica-nav/validate.py` lines 28–43.

Choosing WARN + exit 0 over the install.sh pin is the right call: it closes the misleading-FAIL gap for contributors who skip `./install.sh` without imposing a mandatory pip hit on everyone. The early `sys.exit(0)` before any module-level code runs means there are no attribute-error cascade failures. The MAINTENANCE.md §5.1 addendum documents the soft-prerequisite status cleanly.

### P-3 — F9 Backfill is Thorough and Retroactively Valuable

**Location:** `maintenance/run-log.md`, all 13 existing records.

Every record received a `routine_type:` annotation; the four-row table in MAINTENANCE.md §2.3 makes counter semantics unambiguous for both human reviewers and future parsing agents. The clarification that `task-implementation` records are valid awk-fall-forward baselines (because they advance HEAD) prevents a subtle reading error that could have caused agents to skip over valid baselines.

### P-4 — F12 §1.1 Rewrite Eliminates Dead Documentation

**Location:** `MAINTENANCE.md §1.1`.

The stale `tools/.frontmatter-waivers` paragraph has been a latent confusion source since Task 017/019 closed. Its removal, alongside the accurate post-migration toolchain table and the `FM_TOOLCHAIN=0` escape-hatch caveat, leaves §1.1 in a state a new contributor can actually act on. The rewrite correctly positions the legacy toolchain as an advisory shim on a one-release removal schedule.

### P-5 — F10 Delegation Is Well-Reasoned

The friction-log disposition for F10 ("delegated to Task 025 §Plan-4") is correct: Task 025 was the first filer of the post-repair linter-gate requirement, and avoiding duplicate diffs across Tasks is explicitly the goal. The Task 032 plan pre-authorised exactly this delegation.

---

## Critical Findings

### R-1 (CRITICAL) — MAINTENANCE.md `updated:` Date Is Stale (T1 Violation)

**Location:** `MAINTENANCE.md` YAML frontmatter, line 7.

**Symptom.** `MAINTENANCE.md` carries `updated: 2026-05-05` in its frontmatter. This PR lands substantive diffs to §1.1, §2.3, §3.4, §4.1, and §5.1 — at minimum four sections rewritten or extended — on 2026-05-07. The T1 checklist in `MAINTENANCE.md §1` (which this very file defines) states:

> "Stale `updated:` date — if the file was modified in this delta and its `updated:` field predates the last commit date, update it to today (`YYYY-MM-DD`)."

**Risk.** Future agents running the coherence check will flag MAINTENANCE.md as a T1 violation in the next run's delta, creating unnecessary noise and a misleading record that the file was "not updated" on the day its five sections were modified. Worse, the stale date may cause an agent to treat the file as unmodified when computing staleness heuristics.

**Required fix.** Set `updated: 2026-05-07` in MAINTENANCE.md's frontmatter before merge. This is a T1 repair and MUST be applied in-branch.

---

## Moderate Findings

### R-2 (MODERATE) — Coherence Prompt Step 6 Example Missing `routine_type:` Field

**Location:** `prompts/repo-coherence-check/prompt.md` Step 6 (Run Log example block), lines 252–270.

**Symptom.** Finding F9 adds `routine_type:` as a required field to `maintenance/run-log.md`'s Record Format header. The corresponding example record in the coherence prompt's Step 6 was NOT updated to include this field:

```
# Current Step 6 example (incomplete after F9 change):
### Run 2026-05-04 — Repo Coherence Check
- agent: claude-code
- start_commit: f620b6d
- end_commit: a1b2c3d
- baseline_commit: f620b6d
…
# Missing: - routine_type: coherence-check
```

**Risk.** An agent executing the coherence routine follows Step 6's example as a template. Without `routine_type:` in the example, it will produce a record that does not conform to the new format standard it is supposed to enforce. This is a self-undermining gap: the very routine that enforces the standard will violate it on its next run.

**Required fix.** Add `- routine_type: coherence-check` to the Step 6 example record, immediately after the `- agent:` line, to match the field order in the run-log format header. This SHOULD be applied in-branch; if not, it MUST be filed as a finding for Task 025 (which already owns the coherence prompt's Step 4.5 gap).

---

### R-3 (MODERATE) — Task 025 `task_blocked_by: ["019"]` Not Cleared

**Location:** `tasks/025-maintenance-spec-remaining-findings/task.md` frontmatter.

**Symptom.** The friction log entry for F10 states: "Task 025 was previously blocked by Task 019; Task 019 is now `done`, so Task 025 is unblockable." However, Task 025's frontmatter still reads `task_blocked_by: ["019"]` and `task_status: open` with no change applied. Task 019 is `done`; the blocker is resolved. An agent scanning for actionable work reads `task_blocked_by: ["019"]` and may skip Task 025 as still blocked.

**Risk.** If a future coherence run or maintenance agent attempts to pick up Task 025 (which now owns F10), it will check `task_blocked_by` and either skip the task or spend time verifying the blocker — introducing unnecessary friction and potentially missing the F10 fix window.

**Required fix.** Clear `task_blocked_by: []` in `tasks/025-maintenance-spec-remaining-findings/task.md`. This is a T2 repair (adding/removing an L2 key with an unambiguous value) and MUST be applied in this PR since the delegation creates an immediate operational dependency. The `updated:` date on task.md MUST also be bumped to 2026-05-07.

---

## Minor Findings

### M-1 (MINOR) — `files_in_delta: 7` Undercounts by One

**Location:** `maintenance/run-log.md`, 2026-05-07 Task 032 implementation record.

The parenthetical file list in the run-log entry groups the three files under `tasks/032-improve-maintenance-spec-may-2026/` (task.md, readme.md, friction-log.md) as one token, but they are three distinct changed files. The PR metadata (`changed_files: 8`) confirms the correct count. `files_in_delta: 7` SHOULD be corrected to `8` for auditing accuracy.

---

### M-2 (MINOR) — `files_scanned: 391` Semantics Are Undefined for Task-Implementation Records

**Location:** `maintenance/run-log.md`, 2026-05-07 Task 032 implementation record.

F9's own change establishes that task-implementation records' `t1/t2/t3` counters "describe Task-internal work, not a coherence sweep." The same disambiguation should apply to `files_scanned`. For a 7–8 file task implementation, `files_scanned: 391` implies either (a) the agent ran a full-repo scan that the record format does not semantically support for task-implementation records, or (b) the value is a carry-over from a different scan context. MAINTENANCE.md §2.3's new table SHOULD clarify whether `files_scanned` means "files touched by this task" or "files in the repo at run time" for task-implementation records.

---

### M-3 (MINOR) — `end_commit` Backfill Commit Repeats PR #74's R-3 Pattern

**Location:** Commit graph — `0825eb8` (task close) and `a60f437` (backfill end_commit).

The coherence prompt's Step 5 requires a single atomic commit for coherence-check runs. That rule does not explicitly cover task-implementation records, but the existence of a dedicated `chore(task-032): backfill end_commit` commit is the same pattern that PR #74's R-3 identified as a protocol ambiguity. The prompt has no clause for "task-implementation run-log records may require a second commit to fill in the end_commit hash."

This is the same gap Task 044 F17 or a new finding was asked to absorb in PR #74. If that absorption has not yet landed, this PR's second commit provides another data point for the backlog item. Non-blocking, but SHOULD be referenced in Task 044's findings list or Task 025's plan if not already recorded.

---

## Action Items

| Finding | Severity | Required action | Blocks merge? |
|---------|----------|-----------------|---------------|
| R-1: MAINTENANCE.md `updated:` stale | Critical | Bump to `2026-05-07` in-branch | YES — T1 violation by the spec this file defines |
| R-2: Coherence prompt Step 6 missing `routine_type:` | Moderate | Add field to example OR file finding under Task 025 | SHOULD fix in-branch; non-blocking if filed |
| R-3: Task 025 `task_blocked_by` not cleared | Moderate | Clear `task_blocked_by: []`, bump `updated:` | SHOULD fix in-branch; non-blocking if filed separately |
| M-1: `files_in_delta` off by one | Minor | Correct to `8` | No |
| M-2: `files_scanned: 391` semantics | Minor | Add disambiguation prose to §2.3 or Task 025 | No |
| M-3: `end_commit` backfill pattern | Minor | Reference in Task 044 / Task 025 findings | No |

---

## Conclusion

**Merge is conditional on R-1.** The stale `updated: 2026-05-05` on MAINTENANCE.md is a T1 violation by the very protocol this PR is strengthening, and MUST be resolved before landing on `main`. R-2 and R-3 SHOULD be addressed in-branch for operational cleanliness but do not block the substance of the Task 032 findings. The F13 cross-branch guard and F9 backfill are solid, immediately useful additions that justify the merge once R-1 is cleared.
