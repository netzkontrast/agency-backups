---
type: note
status: active
slug: friction-pattern-synthesis-friction-log
summary: "Mandatory friction log for the friction-pattern-synthesis research run. Highest FL declared at top per FRUSTRATED.md."
created: 2026-05-07
updated: 2026-05-07
---

# Friction Log — Friction Pattern Synthesis

**Highest Frustration Level: FL1**

## FL Declaration

This research run encountered minor ambiguities (FL1) but no significant frustration (FL2) and no blockers (FL3). Two FL1 entries; both align with patterns the SPEC itself catalogues (a satisfying piece of dogfooding).

## Entries

### Entry 1 — FL declaration regex pluralism in the corpus (FL1)

**What happened.** Extracting the FL level from each of the 53 friction logs required five distinct regex patterns to capture every variant:

- `Highest Frustration Level: FL[0-3]` (Tasks 027, 029; research adr-* runs)
- `Highest Friction Level: FL[0-3]` (Tasks 002, 003, 007, 047; research token-efficiency, pr27)
- `**FL[0-3]**` body marker (Tasks 004, 005, 013, 014, 026, 032-may)
- `FL[0-3]` plain inline (Tasks 006, 008, 009, 012; research integrate-dramatica-ncp-skills)
- `summary:` frontmatter declaration (Tasks 016, 017, 018, 019, 020, 021, 030, 031-adr-tooling-impl, 032-may-2026)

A few logs had the FL declaration only in the `summary:` field with no body marker (e.g. `tasks/032-improve-maintenance-spec-may-2026/friction-log.md`); a few had the FL embedded in a per-friction-event header rather than at the top (e.g. `tasks/030/friction-log.md` uses `### FE-EX-N (FL2, Significant)`). Task 047 already noted and repaired one corpus drift case (`FL: 2` typo on Task 041's friction log) in the same commit. Aggregating across this surface variation cost ~10 minutes of pattern-iteration.

**Why it didn't block.** The variation is itself the feature being measured — the SPEC's §4.3 Amendment 3 proposal reads as a direct response to this very friction. Iteration time was low because the canonical forms are all close cousins.

**Suggested process tweak.** Already authored as SPEC §4.3 Amendment 3 (verbatim TASK.md §7 numbered item 7 replacement). The amendment tightens the regex to `\bFL[0-3]\b` with an explicit forbidden-form note (`FL: <N>` is wrong). Self-referential by design.

**Cost.** ≈ 10 minutes regex iteration + the time to author Amendment 3 itself.

### Entry 2 — Pre-existing baseline ERRORs unrelated to this run (FL1)

**What happened.** `tools/check-governance.sh` reports 2 ERRORs that pre-date this Task at run-end:

- `tasks/046-github-workflow-research/task.md::ERROR:F.4.2:missing required heading '## Todo'`
- `tasks/readme.md::ERROR:T.7.11:033-task-spec-integration bullet status='done' but task.md task_status='open'`

A fifth class (5 × `decisions/000{1..5}-*.md::ERROR:ADR.A.5.4:jsonschema module not importable`) was resolved in-session by `pip install jsonschema` (per AGENTS.md SS.1). Two `tasks/readme.md::T.7.11` ERRORs (045 and 046 bullets missing) and `research/spec-staleness-decision-formalization` missing-readme were already resolved by in-flight branch state changes that landed before this Task ran.

The `tasks/readme.md::T.7.11:033-...` ERROR is the parent Task 033's closure flow (the dispatch explicitly forbids modifying TASK.md or governance specs — flipping `task_status: open` → `done` is the parent's call). The `tasks/046-github-workflow-research/task.md` missing `## Todo` heading is owned by Task 046 itself.

**Why it didn't block.** Following the precedent set by `tasks/032-agents-spec-integration/friction-log.md` F1 ("Pre-existing baseline ERRORs out-of-scope drift owned by `031-sync-tasks-index-status-drift`"), these 4 ERRORs are documented in this Task's `readme.md` Assumptions Log A-3 as deferred to their owning task (Task 031-sync continuation, or a successor sync task) rather than fixed under this Task's scope.

**Pattern this exposes.** The exact same pattern is catalogued in this SPEC's §2 Category 5 ("Pre-existing baseline ERRORs unrelated to current task", 9 events). The recurrence here is the 10th. Task 032's friction log proposed: "Consider amending TASK.md or PRE_COMMIT.md to say 'fix every ERROR introduced or touched by this task; pre-existing baseline ERRORs must be cited in `Assumptions Log` and deferred to their owning task.'" That recommendation is one viable amendment direction; this SPEC does not author it because (a) the proposal is already on record in Task 032's log and (b) Task 032 ratifies AGENTS.md, not TASK.md or PRE_COMMIT.md, so cross-spec routing is required first.

**Suggested process tweak.** None new — the routing is already on record. This entry exists to mark the recurrence count.

**Cost.** Zero post-discovery (the deferral pattern is mechanical now).

## Boundaries Honoured

- The 53 friction logs were read but not modified.
- The four root specs implicated in §4 amendments (TASK.md, FRUSTRATED.md) were NOT modified — amendments are *proposals* awaiting Task 033 / Task 038 ratification.
- No `tasks/<NNN>-<slug>/task.md` was modified (per the Task 033 dispatch: "Do NOT modify TASK.md or any other governance specs — the parent task handles that").
- Every FL2+ row in §3 carries a file:line or file §section anchor.
- `tools/check-governance.sh`: 4 baseline ERRORs deferred per A-3; zero new ERRORs introduced.

## Aggregate FL Pattern (For Maintenance)

This is the third research run to surface the "FL declaration form ambiguity" friction (Tasks 027, 029, and now this one all touched it). Per the maintenance pipeline rule cited in `research/adr-assumption-audit/reflection/friction-log.md` Aggregate FL Pattern paragraph ("after one more occurrence … file a Task to amend the prompt-craft template"), the third occurrence promotes the issue from "recurring observation" to "amendment-grade pattern". §4.3 Amendment 3 in the SPEC is precisely that promotion.

The "pre-existing baseline ERRORs deferred per Task 032 precedent" pattern (Entry 2) is now its 10th surfacing. A future Task that addresses Category 5 directly should also amend AGENTS.md SS.2 to formalise the "fix-introduced-or-touched-only" carve-out the corpus has been honouring de facto.
