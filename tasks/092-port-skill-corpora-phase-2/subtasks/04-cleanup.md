---
type: note
status: active
slug: task-092-st4-cleanup
summary: "ST-4 (Task 092 Epic): retire the upstream snapshot — delete tasks/091-…/references/upstream-snapshot/ in its entirety; strip the two governance waivers; bump skills/readme.md. Final governance run."
created: 2026-05-12
updated: 2026-05-12
---

# ST-4 — Snapshot cleanup

**Executor:** main-agent.

**Parallelism:** Sequential — strictly last. MUST close after ST-1, ST-2, ST-3 are all `done`.

**Depends on:** ST-2 ([`02-superclaude-phase-2.md`](./02-superclaude-phase-2.md)) and ST-3 ([`03-superpowers-port.md`](./03-superpowers-port.md)) both at `task_status: done` AND merged to `main`. The keep-list MUST be fully ported before the snapshot is destroyed.

## Scope

1. **Delete the snapshot directory.** `rm -rf tasks/091-port-external-skill-corpora/references/upstream-snapshot/`. The directory was created in Task 091 PR #115 commit `dff5e61` and the user explicitly framed it as "just copy for now — so we can then Concept them one by one" (FRUSTRATED.md FL-style note in the snapshot's `readme.md` "Governance carve-outs" section). The Concepting is done by ST-1; the ports are done by ST-2 + ST-3; the snapshot's purpose is exhausted.
2. **Strip the two waivers.**
   - [`tools/.frontmatter-waivers`](../../../tools/.frontmatter-waivers): delete the row whose path-glob is `tasks/091-port-external-skill-corpora/references/upstream-snapshot/*`.
   - [`tools/.script-allowlist`](../../../tools/.script-allowlist): delete the `tasks/091-port-external-skill-corpora/references/upstream-snapshot/*` glob and its preceding comment block.
3. **Update `skills/readme.md`.** The `## Imported from SuperClaude (v4.3.0)` and `## Imported from Superpowers (v4.0.3)` sections should already be in their final shape after ST-2 + ST-3; bump `updated:` to today and verify the skill count line is correct.
4. **Final governance run.** `tools/check-governance.sh` MUST exit 0 with no expired waivers, no PC.1.1 violations against ex-snapshot scripts, and no F.* validator diagnostics. Failure means a prior subtask did not retire its temporary state correctly.

## Out of scope

- Any new skill port — the keep-list is settled by ST-2 + ST-3.
- Bumping ADR-0011 — the ADR's `Accepted` status is T4-immutable; if Phase 2 surfaces new normative needs (e.g. ratifying the `superpowers-` prefix as `Accepted`), file a new ADR.
- Re-running the triage matrix — ST-1 closes that work permanently.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: ST-4 retires the snapshot cleanly

  # anchor: T092.4.1
  Scenario: Snapshot directory deleted
    Given ST-4 is complete
    When `find tasks/091-port-external-skill-corpora/references/upstream-snapshot/ -type f` runs
    Then it MUST return zero files
    And the directory itself MUST NOT exist

  # anchor: T092.4.2
  Scenario: Waivers stripped
    Given ST-4 is complete
    When a reader greps tools/.frontmatter-waivers for "upstream-snapshot"
    Then the grep MUST return zero matches
    And the same grep against tools/.script-allowlist MUST return zero matches

  # anchor: T092.4.3
  Scenario: No expired waivers (deadline pressure)
    Given ST-4 is committed before 2026-08-12
    When a reader inspects tools/.frontmatter-waivers
    Then no row MUST have an expiry date earlier than today
        (the upstream-snapshot row was the only 90-day waiver; ST-4 closure removes it)

  # anchor: T092.4.4
  Scenario: Governance still green
    Given ST-4 is complete
    When `tools/check-governance.sh` runs
    Then exit code MUST be 0
    And `python3 tools/fm/validate.py skills/` MUST emit 0 ERROR diagnostics
    And `python3 tools/check-clean-working-directory.py` MUST exit 0
        (no orphan .py/.sh files left under tasks/091-…/references/)
```

## Branch + PR shape

Branch: `claude/task-092-st4-cleanup`. PR title: `Task 092 ST-4: retire upstream snapshot + waivers`. PR body MUST include:

- Output of `find tasks/091-port-external-skill-corpora/references/upstream-snapshot/ -type f | wc -l` → `0`.
- Diff of `tools/.frontmatter-waivers` + `tools/.script-allowlist` showing the row removals.
- `tools/check-governance.sh` exit-0 confirmation.
- Final friction-log declaration covering the entire Epic (the Epic-level summary). At this PR's merge, the Epic flips `task_status: done`.
