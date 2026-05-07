---
type: note
status: active
slug: pr-81-review
summary: "Code review for PR #81 — Close Task 033 (TASK.md spec integration) + scaffold Task 048. One critical FOLDERS.md §3 violation (tools/fm/readme.md not updated), two moderate gaps (F.T.1 drift not in audit graph; subtasks/ subfolder below FOLDERS.md §4.1 threshold), three minor findings. Core tooling (two new linters, 15/15 passing tests, TASK.md spec amendments) is solid."
created: 2026-05-07
updated: 2026-05-07
---

# Code Review — PR #81: Close Task 033 (TASK.md Spec Integration) + Scaffold Task 048

**PR:** [#81 Close Task 033 (TASK.md spec integration) + scaffold Task 048](https://github.com/netzkontrast/agency/pull/81)
**Branch:** `claude/run-close-task-spec-2sW2y` → `main`
**Head commit:** `dce0f1c`
**Reviewer:** claude-code (session `claude/brave-darwin-Kvttc`)
**Date:** 2026-05-07

---

## § RFC 2119

The key words MUST, MUST NOT, SHOULD, and MAY in this document are to be
interpreted as described in RFC 2119 when, and only when, they appear in all
capitals.

---

## Summary Verdict

Task 033 delivers on all six stated Goal conditions (a)–(f), and the Task 048
scaffold follows the §1–§7 build-contract precedent cleanly. The two new linters
(`check-duplicate-task-id.py`, `check-task-lifecycle-classification.py`) are
well-designed: supersession reciprocity is correctly modelled, 15/15 tests pass
against real tempfile fixtures, and the advisory-tier wiring in
`check-governance.sh` is the right choice during the Task 043 migration window.

**One critical omission prevents a clean merge:**

- R-1 (CRITICAL) — `tools/fm/readme.md` was not updated. Two new tools land in
  the `tools/fm/` folder but neither appears in the folder index. This is the
  identical FOLDERS.md §3 violation cited in PR #79 R-2; the pattern has now
  recurred across back-to-back PRs.

Two further moderate/minor gaps are non-blocking but SHOULD be addressed in-branch
or filed as follow-up work before Task 048 opens.

---

## Positive Findings

### P-1 — Supersession Escape Hatch is Sophisticated and Correct

**Location:** `tools/fm/check-duplicate-task-id.py:74–102` (`_explained_by_supersession`).

The identity-resolution layer (`a_refs`, `b_refs` each containing `{task_id,
folder_name, slug_without_prefix}`) handles the three real-world reference forms
(bare id `"031"`, full folder `"031-adr-tooling-impl"`, short slug
`"adr-tooling-impl"`) without requiring callers to normalise. The symmetric
two-case check (either folder can be the predecessor) means the linter is
correct regardless of directory sort order. This is materially better than a
naïve string-equality check, and the four current collisions (006/006, 009/009,
031/031, 032/032) correctly trip ERROR as designed while supersession-explained
pairs pass at INFO.

### P-2 — Tests Are Authentic and Pass

All 15 tests in `test_duplicate_task_id.py` (6 incl. real-repo smoke) and
`test_lifecycle_classification.py` (9) pass locally against the current branch.
Every fixture uses `tempfile.TemporaryDirectory` + direct `task.md` authoring
with no patching of the subjects under test. The smoke test (`TestRealRepoIntegration`)
pins the current known-collision set (006, 009, 031, 032) and will self-update
when Task 043 lands — this is the correct long-term guard-rail shape.

### P-3 — Advisory-Tier Design Is the Right Call

`FM_DUPLICATE_TASK_ID_STRICT=1` gating during the Task 043 window avoids
blocking legitimate commits on pre-existing violations the Task 033 agent does
not own. The advisory / strict flag pattern mirrors Task 031's `FM_TOOLCHAIN`
precedent and is the established repo idiom for "enforced, but not yet blocking."

### P-4 — Task 033 Closure Conditions Explicitly Verified

The friction log accounts for all six Goal conditions (a)–(f) with file-level
evidence: linter ships with five tests (not just claimed), research workspace
`research_phase: complete`, TASK.md §6 gains anchor `T.B.SUP.1`, §3.3 gains
three cross-links. The FL1 declaration is honest and the rationale is traceable.

### P-5 — Task 048 Falsification Clauses Are Tight

The four falsification predicates in `task.md` are concrete and checkable at
synthesis time (tool count < 6, schema duplication, pattern-transfer floor,
amendment count > 3). Following Task 028's §1–§7 build-contract template is the
right structural choice; the deviation from prior scaffolds is that each
subtask explicitly declares a falsification clause of its own, which raises the
bar for ST-3's synthesis SPEC.

### P-6 — `research/readme.md` Updated Correctly

Both new research workspaces (`friction-pattern-synthesis/`,
`spec-staleness-decision-formalization/`) appear in `research/readme.md` with
one-line summaries and relative links to their `output/SPEC.md`. The `updated:`
date is correctly set to 2026-05-07.

### P-7 — README.md §6 Linter Row Added (R.7)

The new `tools/fm/check-duplicate-task-id.py` row in README.md §6 is present,
accurate, and cites the TASK.md §8.1 anchor. This closes the R.7 requirement for
every new linter added to `check-governance.sh`.

---

## Critical Findings

### R-1 (CRITICAL) — `tools/fm/readme.md` Not Updated (FOLDERS.md §3 Violation)

**Location:** `tools/fm/readme.md`, frontmatter line 7 (`updated: 2026-05-05`) and
`## Tools` table.

**Symptom.** The PR adds two new scripts to `tools/fm/`:

- `check-duplicate-task-id.py`
- `check-task-lifecycle-classification.py`

Neither appears in `tools/fm/readme.md`. The `## Tools` table still lists only
the original five fm-tools (`validate`, `extract`, `edit`, `query`, `section`).
The `updated:` frontmatter date is 2026-05-05 — two days stale.

**Rule violated.** FOLDERS.md §3: "EVERY folder MUST contain a `readme.md` …
every file/subfolder listed via relative Markdown links." Two of the most
consequential new additions to the folder are invisible to any agent or human
scanning the folder index.

**Recurrence pattern.** This is the same structural omission that PR #79 R-2
identified for `tools/readme.md` (2 of 3 new linters missing). That finding
was marked CRITICAL and required an in-branch fix before merge. This PR repeats
the pattern for the `tools/fm/` subfolder.

**Impact.** An agent picking up Task 048 ST-2 (existing-tooling inventory) will
consult `tools/fm/readme.md` first (per AGENTS.md AG.1.1: summary before body).
The index returns five tools. The agent may conclude no lifecycle or duplicate-id
tools exist and propose them as new deliverables, introducing waste or
duplication.

**Required fix.** `tools/fm/readme.md` MUST add entries for both tools in the
`## Tools` table, following the existing row format. The `updated:` frontmatter
MUST be bumped to 2026-05-07. Minimal additions:

```markdown
| `check-duplicate-task-id` | Detects unexplained duplicate `task_id` values across active Tasks (closes TASK.md §8.1). Advisory in `check-governance.sh`; strict mode via `FM_DUPLICATE_TASK_ID_STRICT=1`. | [`check-duplicate-task-id.py`](./check-duplicate-task-id.py) |
| `check-task-lifecycle-classification` | Evaluates TASK.md §4.7 four-condition test for `updated` / `abandoned` transitions. Manual helper; NOT wired into `check-governance.sh`. | [`check-task-lifecycle-classification.py`](./check-task-lifecycle-classification.py) |
```

This is a one-file edit and MUST be applied in-branch before merge.

---

## Moderate Findings

### R-2 (MODERATE) — F.T.1 Spec/Implementation Drift Not in Audit Graph

**Location:** `tasks/048-task-tooling-impl-spec/readme.md`, `## Assumptions Log`,
last bullet.

**Symptom.** The Task 048 `readme.md` Assumptions Log notes a known
spec/implementation drift:

> "TASK.md §7.3 documents the `task_uses_prompts` enforcement scope as
> `task_status ∈ {done, updated, abandoned}` only, but `tools/fm/validate.py
> --type-check` (diagnostic code `F.T.1`) currently enforces resolution
> unconditionally."

This is correctly identified as a Task-044-class candidate finding. However, no
Prompt or Task has been filed to address it. The Assumptions Log is not part of
the audit graph — an agent scanning `/tasks/` or `/prompts/` for actionable work
will never find this gap.

**Rule violated.** AGENTS.md AG.2.1 routing and PROMPT.md §1(2): "Follow-up
questions discovered during research MUST be filed as new prompts in `/prompts/`."
The F.T.1 drift is exactly the kind of follow-up gap the PROMPT.md routing rule
was designed to capture.

**Impact.** If Task 048's ST-3 SPEC proposes a tool that resolves `task_uses_prompts`
links unconditionally (consistent with the current linter) without first
knowing this is a disputed enforcement scope, the SPEC will bake in the wrong
behavior. Discovering the contradiction at ST-3 review adds friction and may
require a SPEC revision.

**Required fix.** File `prompts/fix-ft1-scope-drift/` (or add a finding to
Task 044's plan) before Task 048 ST-3 begins synthesis. The finding SHOULD
reference: TASK.md §7.3 (prose enforcement scope), `tools/fm/validate.py --type-check`
(actual enforcement), and the Task 033 friction log entry that first surfaced it.
This SHOULD be applied before merge; if deferred, the Task 048 `task_status`
MUST NOT advance to `in_progress` until the gap is in the graph.

---

### R-3 (MODERATE) — `tasks/048-task-tooling-impl-spec/subtasks/` Below FOLDERS.md §4.1 Threshold

**Location:** `tasks/048-task-tooling-impl-spec/subtasks/`, which contains:

```
01-research-skills-corpus-inspiration.md
02-research-existing-task-tooling-inventory.md
03-spec-task-tooling-impl.md
readme.md
```

**Symptom.** FOLDERS.md §4.1 states: "Do not create a subfolder unless 4+ files
of the exact same category accumulate." The three subtask briefs are the
same-category files; `readme.md` is an index file of a different kind. Three
same-category files is below the 4+ threshold.

**Contrast with Task 033.** Task 033's `subtasks/` folder contains five
subtask briefs (01–05), which clears the threshold. Task 048's three briefs do
not. The convention established by Task 033 does not automatically exempt Task 048.

**Impact.** The violation is structural rather than operational — the subtasks
are well-authored and the falsification clauses are useful. But the subfolder
pre-empts the §4.1 rule for a set of files that could live flat in the parent
Task folder or be appended as `## Subtask N` sections within `task.md`.

**SHOULD fix.** Options:
1. Inline the three briefs as `## ST-1`, `## ST-2`, `## ST-3` appendix sections
   in `task.md` and remove the `subtasks/` folder. (Preferred — no threshold to
   meet, no extra readme required.)
2. Add a fourth same-category subtask brief (if legitimately needed) before the
   subfolder's existence is fully justified.
3. Document an explicit exception in the Task 048 `readme.md` Assumptions Log
   with rationale ("3 subtask briefs justify a subfolder because the parent
   task.md would exceed N lines"). This is non-normative and does not override
   the spec; record it as a deviation, not an exception.

Non-blocking, but SHOULD be addressed before Task 048 is picked up by an executor.

---

## Minor Findings

### M-1 (MINOR) — T.B.SUP.1 Gherkin Executability Not Confirmed

**Location:** `TASK.md §6`, newly-added `T.B.SUP.1` scenario.

**Symptom.** The scenario's `When` step reads:

```gherkin
When `tools/fm/validate.py --type-check` validates Task X at pre-commit
Then the validator MUST treat Task X as still blocked
And the diagnostic MUST cite both Y (superseded) and Z (live successor)
```

The PR test plan has an open reviewer checkbox: "Reviewer confirms `T.B.SUP.1`
Gherkin scenario in TASK.md §6 reads correctly against the §8.7
successor-inheritance prose."

Per AGENTS.md G4: "A scenario MUST be **executable**: a human or agent reading
it MUST be able to enact every step without additional clarification." If
`tools/fm/validate.py --type-check` does not currently implement the
supersession-blocker inheritance logic (chaining through `updated → successor`),
the scenario is aspirational rather than executable, and G4 is violated.

**SHOULD fix.** Before marking this checkbox complete, manually test:
`python3 tools/fm/validate.py --type-check tasks/` on a minimal fixture where
Task X declares `task_blocked_by: ["Y"]` and Task Y is `task_status: updated`
with an open successor Z. If the validator treats X as still blocked AND cites
both Y and Z in its diagnostic, T.B.SUP.1 is executable. If not, the scenario
MUST be labelled `# aspirational` with a comment citing the implementing Task, or
it MUST be replaced with a scenario that describes the current behavior.

Non-blocking given the open test-plan checkbox acknowledges the gap.

---

### M-2 (MINOR) — `check-duplicate-task-id.py` Docstring Inconsistency on `updated` Status

**Location:** `tools/fm/check-duplicate-task-id.py:12–15` (module docstring) vs.
line 130 (scan loop body).

**Symptom.** The docstring states the linter targets `task_status ∈ {open,
in_progress, blocked, done}`. The code defines `ACTIVE_STATUSES = {"open",
"in_progress", "blocked", "done"}` but the loop gate reads:

```python
if status not in ACTIVE_STATUSES and status != "updated":
    continue
```

So `updated`-status tasks ARE included in the scan (to enable supersession
reciprocity checks), but the docstring does not document this. A reader relying
on the docstring alone will expect `updated` tasks to be skipped.

**SHOULD fix.** Update the docstring to read:

```python
"""…exits 1 if any value appears more than once across *active* tasks
(`task_status` ∈ {open, in_progress, blocked, done, updated}). A duplicate
involving a task with `task_status: updated` is explained (INFO, not ERROR)
when the supersession reciprocity conditions hold…"""
```

Non-blocking, but the docstring is consulted by tools and agents before the body
(per AGENTS.md AG.1.1); correctness matters.

---

### M-3 (MINOR) — ST-4 Migration onto Five-Signal Algorithm Not Filed as a Task

**Location:** `tools/fm/check-task-lifecycle-classification.py` docstring (lines
15–22) and `TASK.md §4.7` helper paragraph.

**Symptom.** Both the docstring and the TASK.md prose note that the lifecycle
classifier currently implements the four-condition fallback rather than the
ratified `classify_task` five-signal decision tree from
`research/spec-staleness-decision-formalization/output/SPEC.md §1`. Both
recommend a follow-up migration. No Task or Prompt has been filed for this work.

**Impact.** The migration is a concrete, bounded deliverable. Without a Task
entry, no agent will schedule or discover it. The risk is that the four-condition
fallback remains the implementation indefinitely, silently diverging further from
the ratified algorithm as the SPEC evolves.

**SHOULD fix.** File `tasks/049-migrate-lifecycle-classifier-to-five-signal/`
(or add a subtask to Task 039's plan, which already owns the staleness-algorithm
MAINTENANCE integration) before the PR lands, so the migration enters the
scheduling queue. Non-blocking for this PR.

---

## Action Items

| Finding | Severity | Required action | Blocks merge? |
|---------|----------|-----------------|---------------|
| R-1: `tools/fm/readme.md` missing 2 tool entries + stale `updated:` | Critical | Add rows for `check-duplicate-task-id.py` + `check-task-lifecycle-classification.py`; bump `updated: 2026-05-07` | **YES** — FOLDERS.md §3 violation |
| R-2: F.T.1 scope drift not in audit graph | Moderate | File `prompts/fix-ft1-scope-drift/` or add to Task 044 plan | SHOULD fix before Task 048 picks up; non-blocking for merge |
| R-3: `subtasks/` below FOLDERS.md §4.1 threshold | Moderate | Inline briefs or document exception | SHOULD fix in-branch; non-blocking |
| M-1: T.B.SUP.1 executability unverified | Minor | Test `validate.py --type-check` against blocker-via-supersession fixture | No |
| M-2: `check-duplicate-task-id.py` docstring omits `updated` | Minor | Update docstring to mention `updated` in scope | No |
| M-3: ST-4 five-signal migration not tracked | Minor | File follow-up Task (049?) or add to Task 039 plan | No |

---

## Conclusion

**Merge is conditional on R-1.** The missing `tools/fm/readme.md` update is a
FOLDERS.md §3 violation by the same rule flagged CRITICAL in PR #79 R-2 and MUST
be resolved before landing on `main`. The fix is a one-file, one-minute edit.

R-2 SHOULD be addressed before Task 048's executor is assigned — the F.T.1 scope
drift is precisely the kind of found-during-execution gap the `/prompts/`
routing rule exists to capture, and the executor will be better served by finding
it in the audit graph than in a readme Assumptions Log footnote.

R-3, M-1, M-2, and M-3 do not block merge substance but SHOULD be absorbed into
the Task 048 executor briefing or a follow-up Task to avoid compounding governance
debt.

The core work — two linters with authentic test coverage, a clean TASK.md spec
amendment, two complete research workspaces, and a well-structured Task 048
scaffold — is production-grade and warrants merge once R-1 is cleared.
