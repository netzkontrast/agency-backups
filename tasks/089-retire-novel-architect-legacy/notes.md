---
type: note
status: active
slug: retire-novel-architect-legacy-notes
summary: "Implementation notes for Task 089 — gating-criteria monitoring procedure, expected evidence per criterion, and disposition guidance for the recurring Nightly Maintenance Run that will eventually transition this Task out of blocked."
created: 2026-05-12
updated: 2026-05-12
---

# Task 089 — Implementation Notes

## 1. Why this Task is filed at `task_status: blocked`

[Task 070 §Legacy Retirement Criterion (PR #101 review §4.3)](../070-novel-architect-v110-epic/task.md#legacy-retirement-criterion-pr-101-review-43) framed the legacy-skill retirement as a follow-up Task to be filed **when** all three observable criteria hold. Filing at that future point preserves the gating but loses **discoverability** — the criteria sit buried in 070's body and no `/tasks/` entry surfaces the wait-state.

This Task inverts the trade-off: file the Task **now** at `task_status: blocked` so that the criteria are discoverable in `tasks/readme.md`, in lifecycle audits, and in any future agent's repo-orientation pass. The blocked state is the canonical TASK.md §8.4 representation of "filed but not yet actionable."

## 2. Gating criteria (verbatim from Task 070, with monitoring guidance)

### (a) Productive use in migrated workspace

**Statement.** The Kohärenz Protokoll project workspace at `/home/claude/novel-projects/kohaerenz-protokoll/` (or wherever the migrated workspace lives in the actor's environment) has been used productively in **≥ 3 separate sessions** without falling back to `skills/novel-architect-legacy/`.

**Productive = the agent invoked `skills/novel-architect/` (v1.1.0 or later) phases and completed at least one of:**
- A Gate 1, Gate 2, or Gate 3 transition in Phase 2 (architecture worksheet);
- A scene-matrix moment add / update / delete in Phase 5;
- A canon-status entry add / update / delete in Phase 4 or Phase 7.

**Expected evidence at unblock time.** 3+ commit hashes from the migrated workspace, each touching `architecture.yaml` / `scene-matrix.md` / `canon-meta.md`. The agent monitoring the criterion runs `git log --oneline -- novel-projects/kohaerenz-protokoll/` and counts qualifying commits since 2026-05-11 (v1.1.0 Epic close). Commits MUST be from ≥3 distinct calendar dates (a single-day burst does not count as "separate sessions").

**Common false-positive trap.** Commits touching only `references/learnings.md` or `references/canon-meta.md` without an architecture or scene-matrix change do NOT qualify — they are bookkeeping, not productive Phase work.

### (b) NCP validation passes

**Statement.** The migrated `kohaerenz-protokoll.ncp.json` (or equivalent for whichever project is used) passes against the latest `ncp-author` schema, validated by `scripts/bootstrap_project.sh`'s `validate_ncp()` helper.

**Expected evidence at unblock time.** Clean exit code (`$? == 0`) from the helper invocation, captured in the Task 089 friction log along with the helper output. If the helper does not yet exist or has moved, that is itself a blocker on (b) and SHOULD be filed as a sub-Task before (b) can be evaluated.

### (c) No legacy `task_blocked_by` entries

**Statement.** A repo-wide grep for `novel-architect-legacy` in `tasks/**/task.md` frontmatter `task_blocked_by:` lists returns zero matches.

**Expected evidence at unblock time.** The output of:
```bash
grep -r "novel-architect-legacy" tasks/ --include="task.md" -l
```
MUST be empty, OR every match MUST be in a closed Task's body prose (not in a frontmatter `task_blocked_by:` list). The maintenance run that evaluates this criterion MUST distinguish frontmatter matches from body matches via `tools/fm/extract.py` rather than relying on prose-grep alone.

## 3. Monitoring cadence

This Task transitions out of `blocked` when **ALL** three criteria hold simultaneously. The expected monitoring cadence is the [Nightly Maintenance Run](../../MAINTENANCE.md#2-nightly-maintenance-run) — once per audit cycle, the agent running the maintenance pass:

1. Counts qualifying commits per criterion (a).
2. Invokes `validate_ncp()` per criterion (b).
3. Greps frontmatter `task_blocked_by:` per criterion (c).
4. If ALL three hold, transitions this Task's `task_status: blocked` → `open` via `tools/fm/edit.py --set task_status=open`, bumps `updated:`, and appends a friction-log entry capturing the per-criterion evidence (commit hashes, helper exit code, grep output).

Partial-satisfaction maintenance runs (e.g., (a) + (b) hold but (c) does not) MUST NOT transition the Task out of `blocked`; they SHOULD instead append an audit entry to this `notes.md` recording which criteria currently hold and the remaining gap.

## 4. Why `task_supersedes` is `[]` rather than `["novel-architect-legacy"]`

[Task 070's prose](../070-novel-architect-v110-epic/task.md#legacy-retirement-criterion-pr-101-review-43) suggested the future retirement Task would carry `task_supersedes: ["novel-architect-legacy"]`. The `tools/fm/validate.py` F.T.1 rule rejects this value because there is no `tasks/*/task.md` with `task_id` or `slug` matching `novel-architect-legacy` (the legacy entity is a *skill*, not a *task*, and `task_supersedes` references task-side identifiers exclusively).

This Task therefore carries `task_supersedes: []` at the frontmatter level; the supersession intent is preserved in body prose and in this notes file. At closure time the supersession is realized via `git rm -r skills/novel-architect-legacy/` rather than via a frontmatter graph edge. The audit-graph integrity is preserved by the removal-audit entry in `references/learnings.md` (Task 089 Goal §4).

## 5. Pre-conditions on (b) — `scripts/bootstrap_project.sh` may not exist yet

The `scripts/bootstrap_project.sh` referenced by criterion (b) is the bootstrap script for the migrated workspace. As of this notes file's filing date (2026-05-12), the script's existence is **assumed but not verified** — the file lives outside this repo, in the migrated workspace itself. If the maintenance run that evaluates (b) cannot locate the script or its `validate_ncp()` helper, criterion (b) MUST be marked as "pre-blocked: script not found"; a separate sub-Task to author the helper is then required before (b) can be evaluated cleanly.

This pre-condition is documented here rather than in the Task body so that the body remains a stable specification of the retirement intent; pre-conditions on the monitoring tooling are an implementation detail of the criterion-evaluation pass.
