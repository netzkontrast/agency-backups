---
type: note
status: active
slug: pr-74-review
summary: "Code review for PR #74 — 2026-05-07 coherence run + Task 043/044 filing. Three critical findings and two positive calls."
created: 2026-05-07
updated: 2026-05-07
---

# Code Review — PR #74: 2026-05-07 Coherence Run

**PR:** [#74 chore(coherence): 2026-05-07 run + Task 044 maintenance-spec follow-up](https://github.com/netzkontrast/agency/pull/74)
**Branch:** `claude/funny-curie-rX7a4` → `main`
**Reviewer:** claude-code (session `claude/brave-darwin-ACBGY`)
**Date:** 2026-05-07

---

## § RFC 2119

The key words MUST, MUST NOT, SHOULD, and MAY in this document are to be
interpreted as described in RFC 2119 when, and only when, they appear in all
capitals.

---

## Summary Verdict

The coherence run correctly identified and repaired the sole linter-visible T1
issue (FL declaration format) and produced solid, well-documented T3 Task
scaffolding. However, **three findings below require attention before Task 043
can be executed safely**. Two are mechanical correctness issues introduced
within this PR itself; one is a governance-spec compliance gap.

---

## Positive Findings

### P-1 — T1 Repair Executed Correctly

`tasks/041-extract-subtask-prompts/friction-log.md`: the `**FL: 2**`
(with colon-space) → `**FL2**` conversion is the correct minimal fix.
The `updated:` bump was applied as a paired action per T1 checklist
item 1. No over-engineering.

### P-2 — Task 043 Justification Table Is Sound

The rationale column in `tasks/043-renumber-duplicate-task-ids-v3/task.md`
correctly applies the "later-created / least-downstream-disruption" criterion
from MAINTENANCE.md §3.5. Choosing the open `031-sync-tasks-index-status-drift`
over the in-flight `031-adr-tooling-impl/` (which is referenced by Tasks
033–039) is the right call.

### P-3 — Run-Log Entry Is Thorough

The 2026-05-07 run-log record covers every mandatory field, explains the
`t4_skipped: 2` and `issues_skipped: 1` dispositions in prose, and names the
specific awk fall-forward path used to recover the `baseline_commit`. This is
the most detailed run record in the file to date and sets a good template for
future runs.

---

## Critical Findings

### R-1 (CRITICAL) — Self-Inflicted task_id: "044" Collision

**Location:** `tasks/043-renumber-duplicate-task-ids-v3/task.md` §Goal +
`tasks/044-improve-maintenance-spec-may-07-2026/task.md` frontmatter.

**Symptom.** Task 043's Goal section states:

> `tasks/031-sync-tasks-index-status-drift/` MUST be renumbered to the next
> free slot (proposed: `044` if `043` and `044` are unclaimed at staging time).

However, Task 044 (`044-improve-maintenance-spec-may-07-2026/`, `task_id:
"044"`) was filed in the very same session — in the second commit of this PR
(`ad53c05`). Slot `044` is therefore already claimed when Task 043 lands on
`main`. The documented proposal in Task 043's Goal body is stale the moment the
PR merges.

**Risk.** An agent picking up Task 043 will read the Goal, see "proposed: `044`
", check disk, find `044` is occupied, and have to improvise. The free-slot
check in Task 043 Plan step 1 provides a safety net ("pick the next free pair
otherwise"), but the documented proposal is wrong and will cause unnecessary
confusion. Worse, if the agent skips step 1 and blindly follows the `044`/`045`
proposal, it will create a third `task_id: "044"` collision — the exact anti-
pattern Task 043 exists to eliminate.

**Required fix.** Task 043 Goal MUST be updated to reflect that slot `044` is
now taken:

```
proposed: `046` and `047` (since `044` is taken by Task 044 filed in this
session and `045` is the next candidate after that).
```

Alternatively, the agent SHOULD renumber Task 043's proposal dynamically at
execution time, which the Plan already mandates in step 1 — but the Goal body
MUST NOT contradict that step.

---

### R-2 (MODERATE) — Undocumented L2 Frontmatter Fields on Both New Tasks

**Location:** `tasks/043-renumber-duplicate-task-ids-v3/task.md` and
`tasks/044-improve-maintenance-spec-may-07-2026/task.md`, YAML frontmatter.

**Symptom.** Both new task files include these keys:

```yaml
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
```

None of these appear in the Task namespace definition at `TASK.md §3.3`. The
canonical L2 Task namespace lists exactly seven keys: `task_id`, `task_status`,
`task_owner`, `task_priority`, `task_uses_prompts`, `task_spawns_research`,
`task_affects_paths`.

**Risk.** Adding undocumented keys to frontmatter directly contradicts `TASK.md
§3.3`'s role as the normative Task namespace. If future agents or tooling
(e.g. `tools/fm/validate.py --type-check`) enforce the schema strictly, these
fields will fail or be silently ignored. If the keys ARE intentional extensions
(which they appear to be — `task_blocked_by` and `task_supersedes` are useful),
they MUST be ratified in `TASK.md §3.3` first, then backported to existing
Tasks.

**Required fix.** Either:

- (Preferred) File a sub-finding under Task 044 F14 or a new finding to
  formally extend `TASK.md §3.3` with these four keys, including type and
  purpose documentation; OR
- Remove the four undocumented keys from both task files until the schema is
  updated.

This finding partially overlaps Task 032 §F8 (schema rigidity) and Task 033
(`task-spec-integration`), but neither covers this specific schema-pollution
case.

---

### R-3 (MINOR) — Single-Atomic-Commit Constraint Violated

**Location:** PR commit graph — two commits:
- `9172de7` — coherence check T1 repairs + Task 043 + run-log
- `ad53c05` — Task 044 filing

**Symptom.** `prompts/repo-coherence-check/prompt.md` Step 5 states:

> "All T1 and T2 repairs, any new Tasks, and the run-log entry (Step 6) MUST
> be committed together in a single atomic commit."

Task 044 is a T3 finding distilled from session insights per the operator's
standing instruction. The PR description explains the second commit as an
"operator-instructed" action, not part of the coherence run's T3 output. This
is a reasonable operational distinction — but the prompt currently makes no
provision for a separate "operator-instructed" category.

**Risk.** Future agents and reviewers cannot distinguish a legitimate
post-run operator-instructed commit from a protocol violation without reading
the PR body. The protocol is ambiguous on this boundary.

**Required fix (for Task 044 to record):**

- `prompts/repo-coherence-check/prompt.md` §Step 5 SHOULD add a clause:
  "If the operator issues an additional instruction after the coherence
  commit (e.g. to distil session findings into a follow-up Task), that
  action MAY be committed separately with a `feat(task-NNN):` prefix commit
  message distinct from the `chore(coherence):` commit."

This is a prompt-spec improvement, not a blocking issue for this PR; filing it
here so Task 044 F17 (§/sc: skill fit) or a new F18 can absorb it.

---

## Traceability Gap (Non-Blocking)

### G-1 — 289 Files Unaccounted in Scan Log

**Location:** `maintenance/run-log.md` 2026-05-07 entry.

`files_in_delta: 297`, `files_scanned: 8`, `t4_skipped: 2`. That leaves 287
files whose disposition is explained only in the prose `notes:` block as
"already conformant." The prompt's Step 2 triage table approach supports this
pattern for large deltas, but the run-log format has no field for
`files_confirmed_conformant` vs `files_skipped_as_conformant`. Future audits
cannot mechanically verify that the 289 non-scanned files were actually
inspected and found clean rather than silently ignored.

This is an informational gap, not a data error. It is a candidate for
Task 044 F16 or a new F18 (run-log schema extension).

---

## Action Items for Downstream Tasks

| Finding | Severity | Absorbing Task | Required before Task 043 executes? |
|---------|----------|----------------|-------------------------------------|
| R-1: Task 043 proposal names taken slot 044 | Critical | Fix inline in Task 043 now | YES |
| R-2: Undocumented L2 fields | Moderate | Task 033 or Task 044 | No (but SHOULD precede any schema tooling run) |
| R-3: Two-commit coherence run | Minor | Task 044 F17 or new F18 | No |
| G-1: 289 files unaccounted | Informational | Task 044 F16 or new F18 | No |

---

## Conclusion

Merge is **conditional**: R-1 MUST be resolved in this branch before Task 043
can be safely delegated to any agent. R-2 and R-3 do not block merge but SHOULD
be absorbed into the existing Task 044 findings log. The coherence run mechanics
and the Task 043 rationale table are otherwise solid work.
