---
type: task
status: archived
slug: retire-novel-architect-legacy
summary: "Standalone gated Task (NOT a sub-task of Epic 083). Retire skills/novel-architect-legacy@0.3.3-archived per the §Legacy Retirement Criterion enumerated in Task 070. task_status: blocked until all three observable conditions (a)/(b)/(c) from Task 070 §Legacy Retirement Criterion hold. Filed in Epic 083's scaffold session for discoverability — without this Task the criteria sit buried in 070's body and the wait-state is invisible to subsequent agents."
created: 2026-05-12
updated: 2026-05-12
task_id: "089"
task_status: blocked
task_owner: "claude-code"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - skills/novel-architect-legacy/
---

# Task 089 — Retire Novel-Architect Legacy

## Goal

Remove the `skills/novel-architect-legacy@0.3.3-archived` skill directory once the [Task 070 §Legacy Retirement Criterion](../070-novel-architect-v110-epic/task.md#legacy-retirement-criterion-pr-101-review-43) three observable conditions hold. This Task is filed at `task_status: blocked` in [Epic 083's](../083-novel-architect-v120-enforcement-epic/) scaffold session for discoverability; transition to `open` and subsequently `done` happens in a future session when ANY criterion-monitoring run reports all three conditions met.

`done` when:

1. The three §Gating Criteria below are all satisfied (verifiable from observable repo + workspace state).
2. `skills/novel-architect-legacy/` directory has been removed in a clean commit; `git log --oneline -- skills/novel-architect-legacy/` shows the removal commit.
3. Every `task_blocked_by` reference to `novel-architect-legacy` paths in `tasks/` has been resolved (either the referencing Task closed or the reference removed).
4. A removal-audit entry is appended to `skills/novel-architect/references/learnings.md` recording the date, the validating evidence for each criterion, and a pointer to this Task's closure commit.

## Gating Criteria (from Task 070 §Legacy Retirement Criterion)

The legacy skill MUST NOT be retired until all three of the following hold. Each criterion is observable; do NOT proceed on inferred satisfaction.

- **(a) Productive use in migrated workspace.** The Kohärenz Protokoll project workspace at `/home/claude/novel-projects/kohaerenz-protokoll/` (or wherever the migrated workspace lives) has been used productively in **≥ 3 separate sessions** without falling back to the legacy skill. Productive = the agent invoked `skills/novel-architect/` (v1.1.0 or later) phases and completed at least one Gate transition or scene-matrix update per session. Evidence: 3+ commit timestamps on novel-projects content, none of which touch `skills/novel-architect-legacy/`.
- **(b) NCP validation passes.** The migrated `kohaerenz-protokoll.ncp.json` (or equivalent for whichever project is used) passes against the latest `ncp-author` schema, validated by `scripts/bootstrap_project.sh`'s `validate_ncp()` helper. Evidence: a clean exit code from that helper on the migrated NCP file.
- **(c) No legacy task_blocked_by entries.** A repo-wide grep for `novel-architect-legacy` in `tasks/**/task.md` `task_blocked_by:` frontmatter fields returns zero matches. Evidence: `grep -r "novel-architect-legacy" tasks/ --include="task.md" -l` returns empty, OR every match is in a closed Task body (not a frontmatter cross-reference).

## Context

[Task 070 §Legacy Retirement Criterion](../070-novel-architect-v110-epic/task.md#legacy-retirement-criterion-pr-101-review-43) explicitly framed the retirement as a follow-up Task:

> When all three hold, file a new Task `<NNN>-retire-novel-architect-legacy` that `task_supersedes: ["novel-architect-legacy"]` and removes the directory. Until then, the legacy skill stays.

This Task is that follow-up, filed proactively at scaffold time rather than reactively when the criteria first hold. The proactive filing is the [/sc:design §1 design call](../083-novel-architect-v120-enforcement-epic/task.md#sub-tasks-children) "FR-5 structural unblock" — the gating criteria are discoverable in `/tasks/` rather than buried in 070's body, so the wait-state is visible to subsequent agents and shows up in `tasks/readme.md` lifecycle audits as `Status: blocked`.

This Task is **NOT** a sub-task of Epic 083. Epic 083's closure does NOT depend on Task 089's closure — they unblock independently. Task 089's `task_blocked_by:` is empty because its gating is on observable workspace + repo conditions, not on other Tasks; the lifecycle classifier should not treat an empty `task_blocked_by` as "stalled" but rather read the `task_status: blocked` declaration directly.

Per [TASK.md](../../TASK.md), `task_supersedes: ["novel-architect-legacy"]` records the intention; the actual supersession lands at this Task's closure (not at filing time).

## Plan

1. **Monitor gating criteria** — at each Nightly Maintenance Run (or equivalent recurring audit), check criteria (a)/(b)/(c) and record the result in this Task's friction log (created when the Task transitions out of blocked). Do NOT close this Task on partial satisfaction.
2. **Transition to `task_status: open`** — when all three criteria hold, edit this Task's `task_status: blocked` → `open` via `tools/fm/edit.py --set task_status=open` and update `updated:`. Append a friction-log entry documenting the criteria-satisfaction evidence (commit hashes, validation outputs, grep results).
3. **Execute retirement** — `git rm -r skills/novel-architect-legacy/` in a single commit; update any stale references in skill manifests (`skills/readme.md`, root `README.md` if applicable); verify `tools/check-governance.sh` exits 0 post-removal.
4. **Append removal-audit entry** to `skills/novel-architect/references/learnings.md` recording the retirement date, evidence per criterion, and a pointer to the closure commit hash.

## Todo

- [ ] 1. (Recurring) At each maintenance run, check criteria (a)/(b)/(c) and record in friction log.
- [ ] 2. (One-shot, when criteria hold) Transition `task_status: blocked` → `open` via `tools/fm/edit.py --set`.
- [ ] 3. (One-shot, after transition) Execute `git rm -r skills/novel-architect-legacy/` and audit any stale references.
- [ ] 4. (One-shot, post-removal) Run `tools/check-governance.sh` → exit 0.
- [ ] 5. (One-shot, post-removal) Append removal-audit entry to `skills/novel-architect/references/learnings.md`.
- [ ] 6. (One-shot, post-removal) Close this Task: `task_status: archived` + final friction log.

## Acceptance

```gherkin
Feature: Task 089 closes only when all three Gating Criteria hold and the legacy skill is removed cleanly

  # anchor: 089.AC.1
  Scenario: Criterion (a) verification — productive workspace use without legacy fallback
    Given the migrated novel-projects workspace at /home/claude/novel-projects/kohaerenz-protokoll/ (or equivalent)
    When the maintenance run inspects git log for the workspace
    Then there MUST be ≥3 commit timestamps reflecting productive use of skills/novel-architect/ (v1.1.0+)
    And NO commit since v1.1.0 close MAY touch skills/novel-architect-legacy/

  # anchor: 089.AC.2
  Scenario: Criterion (b) verification — NCP validation passes
    Given the migrated kohaerenz-protokoll.ncp.json (or equivalent)
    When the agent runs scripts/bootstrap_project.sh validate_ncp <path>
    Then the helper MUST exit 0
    And the friction log MUST capture the exit code + validation output

  # anchor: 089.AC.3
  Scenario: Criterion (c) verification — no legacy task_blocked_by references
    When the agent runs grep -r "novel-architect-legacy" tasks/ --include="task.md" -l filtering for task_blocked_by frontmatter context
    Then the result MUST be empty
    OR every match MUST be in a closed Task's body prose, not in a frontmatter task_blocked_by field

  # anchor: 089.AC.4
  Scenario: Removal commit is clean and audited
    Given all three Gating Criteria hold (per AC.1, AC.2, AC.3)
    And task_status has transitioned to "open"
    When the agent runs git rm -r skills/novel-architect-legacy/ and commits
    Then tools/check-governance.sh MUST exit 0 on the post-removal commit
    And skills/novel-architect/references/learnings.md MUST contain a removal-audit entry citing the closure commit hash
```

## Links

- Source criterion: [Task 070 §Legacy Retirement Criterion (PR #101 review §4.3)](../070-novel-architect-v110-epic/task.md#legacy-retirement-criterion-pr-101-review-43)
- Companion Epic (NOT parent — this Task is standalone): [Task 083](../083-novel-architect-v120-enforcement-epic/task.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`MAINTENANCE.md`](../../MAINTENANCE.md)
- Removal target: [`skills/novel-architect-legacy/`](../../skills/novel-architect-legacy/) (if currently present)
- Audit-trail target: [`skills/novel-architect/references/learnings.md`](../../skills/novel-architect/references/learnings.md)
- Validation tool: [`scripts/bootstrap_project.sh`](../../scripts/bootstrap_project.sh) (if currently present) — `validate_ncp()` helper
