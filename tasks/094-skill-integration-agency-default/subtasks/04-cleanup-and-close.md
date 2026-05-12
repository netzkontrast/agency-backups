---
type: note
status: active
slug: task-094-st4-cleanup-and-close
summary: "ST-4 (Task 094 Epic): final governance run, flip Epic to task_status: done, update tasks/readme.md index, and author the Epic-level friction-log summary covering ST-1 through ST-4."
created: 2026-05-12
updated: 2026-05-12
---

# ST-4 — Cleanup + Epic close

**Executor:** main-agent.

**Parallelism:** Sequential — strictly last. MUST close after ST-1, ST-2, ST-3 are all `done`.

**Depends on:** ST-1, ST-2, ST-3 all merged to `main`.

## Scope

1. **Final governance run.** `tools/check-governance.sh` MUST exit 0 with no expired waivers, no F.* validator diagnostics, no H.* hook-registration diagnostics. Failure means a prior subtask did not retire its temporary state correctly.

2. **Flip Epic to done.** Use `tools/fm/edit.py --set task_status=done tasks/094-skill-integration-agency-default/task.md`. If the Spec-K.7.1 trust audit demands a `task_owner`, set it to `claude` via the same tool.

3. **Bump `updated:` fields.** `tools/fm/edit.py --bump-updated` on `tasks/094-…/task.md`, `tasks/readme.md`, `skills/readme.md`.

4. **Update `tasks/readme.md`.** Flip the Task 094 row's `Status: open` to `Status: done` and append a PR-trail summary (`PRs #N1/#N2/#N3/#N4` where the placeholders are filled with the actual ST-1/2/3/4 PR numbers).

5. **Author the Epic-level friction-log summary.** Append a `## Epic-level summary` section to `tasks/094-skill-integration-agency-default/friction-log.md` consolidating ST-1, ST-2, ST-3 friction entries and declaring the Highest FL value for the Epic. Pattern: mirror the Task 092 friction-log Epic summary.

6. **No other repo changes.** Skill bodies, plugin manifest, hook scripts are all settled by ST-1/2/3. ST-4 is purely an orchestration close.

## Out of scope

- Any new skill, hook, or root-spec edit — the Epic surface is settled by ST-1/2/3.
- A new ADR — no ADR is filed by this Epic; if Phase 3 surfaces new architecture decisions (e.g. ratifying the `.claude/skills/` symlink as the canonical loader path), file a successor ADR.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: ST-4 closes the Task 094 Epic cleanly

  # anchor: T094.4.1
  Scenario: Final governance still green
    Given ST-4 is complete
    When `tools/check-governance.sh` runs
    Then exit code MUST be 0

  # anchor: T094.4.2
  Scenario: Epic flipped to done
    Given ST-4 is complete
    When a reader greps tasks/094-skill-integration-agency-default/task.md for "task_status:"
    Then the value MUST be "done"
    And the task_owner field MUST NOT be empty
        (Spec-K.7.1 trust audit requirement for done tasks)

  # anchor: T094.4.3
  Scenario: Index synced
    Given ST-4 is complete
    When a reader opens tasks/readme.md
    Then the Task 094 row's status MUST read "Status: done"
    And the row MUST cite all four subtask PRs (ST-1 / ST-2 / ST-3 / ST-4)

  # anchor: T094.4.4
  Scenario: Epic friction-log finalised
    Given ST-4 is complete
    When a reader opens tasks/094-…/friction-log.md
    Then the file MUST carry an Epic-level summary section
    And the summary MUST declare a Highest Frustration Level value (FL0-FL3)
```

## Branch + PR shape

Branch: `claude/task-094-st4-cleanup-and-close`. PR title: `Task 094 ST-4: close Epic — flip task_status: done + Epic friction-log`. PR body MUST include:

- Confirmation that `tools/check-governance.sh` exits 0.
- Output of `grep task_status: tasks/094-…/task.md` showing `done`.
- A summary table of all four subtask PRs (numbers + merge timestamps).
- The Epic-level friction-log declaration.
