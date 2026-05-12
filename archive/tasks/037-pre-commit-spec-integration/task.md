---
type: task
status: archived
slug: pre-commit-spec-integration
summary: "Resolve the FRUSTRATED.md §28 vs PRE_COMMIT.md §2 readme-cadence contradiction, add a toolchain-precedence matrix for the THREE-WAY legacy / flexible / ADR toolchain (§7.A + §7.C from Task 031), mechanize PC.1.1 clean-working-directory checks, and shift PC.7.B waivers from per-file to per-rule granularity."
created: 2026-05-06
updated: 2026-05-12
task_id: "037"
task_status: archived
task_owner: "claude-code (session claude/run-close-task-37-a0umf)"
task_priority: P2
task_uses_prompts:
  - research-pre-commit-readme-update-cadence
  - tooling-clean-working-directory-linter
  - tooling-per-rule-waiver-mechanism
  - spec-amendment-pre-commit-md
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - PRE_COMMIT.md
  - tools/check-clean-working-directory.py
  - tools/.frontmatter-waivers
  - tools/check-governance.sh
---

# Task 037 — PRE_COMMIT.md Spec Integration

## Goal

Eliminate the load-bearing contradiction with FRUSTRATED.md, harden mechanical enforcement of PC.1.1 cleanliness, give the toolchain-precedence rule (§7.A) a normative matrix that now spans THREE toolchains (Legacy / Flexible / ADR), and refine the waiver protocol (§7.B) from per-file to per-rule granularity. The Task is `done` when (a) the readme-cadence rule is harmonised across PRE_COMMIT.md §2 and FRUSTRATED.md §28, (b) §7.A contains a Legacy↔Flexible↔ADR tool-mapping table that explicitly references the §7.C ADR Governance Validator (PRE_COMMIT.md:107) as step `[5/5]` of `tools/check-governance.sh`, (c) `tools/check-clean-working-directory.py` exists and is invoked by `tools/check-governance.sh` (and ignores `decisions/` per the §8 exemption), (d) `tools/.frontmatter-waivers` supports per-rule scoping (rule scopes include the new `ADR.A.*` codes from §7.C), **and (e) each of the following anchors carries ≥1 Gherkin scenario in PRE_COMMIT.md (total ≥4)**:

- **PC.B.1 §6 hand-off** — context-specific delegation to TASK.md/PROMPT.md/RESEARCH.md.
- **PC.B.2 §7 governance gate** — `tools/check-governance.sh` exit-0 contract.
- **PC.B.3 §7.B per-rule waivers** — waiver scope including `ADR.A.*` codes.
- **PC.B.4 §7.C ADR validator interaction** — what happens on a `decisions/**` edit (Task 031 contract).

> **Cross-spec wording-convergence note (per spec-panel m1):** the §2 readme-cadence wording produced by subtask `04-spec-amendment-pre-commit-md` MUST be byte-identical (modulo spec-name prefix) to the §28 wording produced by [Task 038 ST-3](../038-frustrated-spec-integration/subtasks/readme.md). The two amendments land in a single coordinated commit; if they diverge, an authoring error occurred and one spec MUST be reverted to match the other before merge.

## Context

The audit identified one outright contradiction and three governance debts. Task 031 also added a third toolchain (ADR Governance Validator §7.C, PRE_COMMIT.md:107–129) that the §7.A precedence matrix MUST now incorporate:

- **Contradiction.** FRUSTRATED.md §28 advises *batching* readme updates at pre-commit (treats per-file updates as FL2). PRE_COMMIT.md §2 says "EVERY folder ... MUST have its `readme.md` updated *now*, right before the commit." Agents read the former as "do nothing until pre-commit"; the latter as "update on touch". The intent is aligned (batched at pre-commit); the wording is not.
- **PC.7.A toolchain precedence (§56–62)** — describes Legacy + Flexible parallel operation but provides no table mapping individual tools (legacy `validate-frontmatter.py` ↔ `tools/fm/validate.py`, etc.). Now also misses the ADR validator (§7.C) entirely. Agents must infer a three-way matrix that PRE_COMMIT.md never states.
- **PC.1.1 clean working directory (§5–6)** — "no .py / .sh script scratchpads" — relies on agent discipline. A `.py` left in `/research/<slug>/workspace/` will silently slip through. Tooling MUST also exempt `decisions/` per FOLDERS.md §8 (no `.py` files expected there, but the linter must not falsely flag the directory).
- **PC.7.B waiver protocol (§69–79)** — per-file scope. A file with multiple violations gets all of them silenced. Per-rule scoping is acknowledged as a weakness in the spec ("A waiver disables the entire validator for the listed file") but no plan exists. Per-rule scoping must accommodate the new `ADR.A.<aspect>.<stmt>` diagnostic codes from §7.C (PRE_COMMIT.md:113).

## Preconditions (satisfied at branch-time)

- **Task 016/017** — flexible toolchain shipped (the "Flexible" column of the §7.A matrix).
- **Task 031** — ADR validator shipped (the "ADR" column of the §7.A matrix; PRE_COMMIT.md §7.C source).

## Build-On

- **`tools/check-governance.sh`** — the one-stop entry point; subtask 02 + 03 extend it (no parallel script).
- **`tools/.frontmatter-waivers`** — current per-file waiver mechanism; subtask 03 refactors in place rather than introducing a parallel file.
- **`tools/adr/cli.py validate`** — the §7.C diagnostic-code emitter (`ADR.A.<aspect>.<stmt>`); subtask 03's per-rule waiver vocabulary MUST accept these codes verbatim.

## Plan

1. **Phase 1 — Research head.** Subtask `01-research-pre-commit-readme-update-cadence` produces the canonical decision (immediate vs. batched-at-precommit) backed by token-cost analysis on the existing corpus.
2. **Phase 2 — Tooling.** Subtask `02-tooling-clean-working-directory-linter` (PC.1.1). Subtask `03-tooling-per-rule-waiver-mechanism` (PC.7.B refactor).
3. **Phase 3 — Spec amendment.** Subtask `04-spec-amendment-pre-commit-md`: harmonise §2 with FRUSTRATED.md §28 (joint commit with [Task 038 ST-3](../038-frustrated-spec-integration/subtasks/readme.md)), add §7.A precedence matrix, document new linters, document per-rule waivers, add one Gherkin per PC.B.1–PC.B.4 anchor.

## Sample Gherkin (shape the maintainer authoring subtask 04 should produce)

```gherkin
# anchor: PC.B.4 — §7.C ADR validator interaction
Scenario: Edit to AGENTS.md guarded section triggers ADR validator
  Given a commit modifies `AGENTS.md` between the markers
        `<!-- BEGIN AGENCY-ADR SYNTHESIS -->` and `<!-- END AGENCY-ADR SYNTHESIS -->`
  When `tools/check-governance.sh` runs step `[5/5]`
  Then `tools/adr/cli.py validate` MUST exit 1 with diagnostic code `ADR.A.3.5`
  And `tools/check-governance.sh` MUST exit non-zero
  And the commit MUST be blocked until the markers are restored
        OR the edit is moved outside the guarded section
        OR the maintainer re-runs `tools/adr/cli.py synthesize` to refresh the section
```

## Todo

- [x] 1. Dispatch subtask `01-research-pre-commit-readme-update-cadence`.
- [x] 2. Dispatch subtask `02-tooling-clean-working-directory-linter` (Phase A).
- [x] 3. Dispatch subtask `03-tooling-per-rule-waiver-mechanism` (Phase A).
- [x] 4. Dispatch subtask `04-spec-amendment-pre-commit-md` (Phase B).
- [x] 5. Run `tools/check-governance.sh`.
- [x] 6. Update `README.md §6` per R.7.
- [x] 7. Update `tasks/readme.md`.
- [x] 8. Author `friction-log.md`.
- [x] 9. Set `task_status: done`.

## Links

- Subtask index: [`subtasks/readme.md`](./subtasks/readme.md)
- Source research:
  - [`research/governance-specs-update-research/output/SPEC.md`](../../research/governance-specs-update-research/output/SPEC.md) §4 (PRE_COMMIT.md amendments — linter transition + waiver burn protocol)
- Co-touched: [Task 038 — FRUSTRATED.md spec integration](../038-frustrated-spec-integration/task.md) (the contradiction is reciprocal).
- Governing specs: [`PRE_COMMIT.md`](../../PRE_COMMIT.md), [`FRUSTRATED.md`](../../FRUSTRATED.md) §28, [`MAINTENANCE.md`](../../MAINTENANCE.md), [`README.md`](../../README.md) §11.3
