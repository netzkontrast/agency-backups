---
type: task
status: active
slug: extract-subtask-prompts
summary: "Close the audit-graph debt surfaced by PR #70 review C.3 — extract the 35 inlined `## Execution Brief` blocks from `tasks/03[2-9]*/subtasks/*.md` to proper `/prompts/<slug>/prompt.md` files with `type: prompt` + `prompt_kind: task-spec`, and populate `task_uses_prompts` on Tasks 032–040 to restore the task↔prompt edge across the chain."
created: 2026-05-06
updated: 2026-05-06
task_id: "041"
task_status: done
task_owner: "unassigned"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_affects_paths:
  - prompts/
  - tasks/032-agents-spec-integration/
  - tasks/033-task-spec-integration/
  - tasks/034-prompt-spec-integration/
  - tasks/035-research-spec-integration/
  - tasks/036-folders-spec-integration/
  - tasks/037-pre-commit-spec-integration/
  - tasks/038-frustrated-spec-integration/
  - tasks/039-maintenance-spec-integration/
  - tasks/041-extract-subtask-prompts/
  - tasks/readme.md
---

# Task 041 — Extract Subtask Execution Briefs to Prompts

## Goal

Close the audit-graph compliance gap identified in [PR #70 review C.3](https://github.com/netzkontrast/agency/pull/70#issuecomment-4390879904). Today, 35 subtask files under `tasks/03[2-9]*/subtasks/*.md` carry inlined `## Execution Brief` blocks that are functionally self-contained executable prompts — violating **TASK.md §1** ("A Task MUST NOT inline a prompt; it MUST link to one") and **TASK.md §4.3** ("ensure a prompt exists under `/prompts/<slug>/`"). All 9 parent tasks (032–040) consequently carry `task_uses_prompts: []`, severing the `task → prompt` audit-graph edge.

The Task is **done** when (a) every Execution Brief block has been extracted to a `/prompts/<slug>/prompt.md` file with `type: prompt` + `prompt_kind: task-spec` frontmatter, (b) every parent task `task_uses_prompts` lists the slugs of its child subtask prompts, (c) every subtask file's body cross-references the prompt rather than inlining its content, (d) the new `/prompts/<slug>/` folders carry the F.4.1.1 mandatory three-file scaffold (`brief.md`, `prompt.md`, `readme.md`), and (e) `tools/check-governance.sh` exits 0 — including `tools/lint-linkage.py` (or its successor) verifying the `task_uses_prompts` ↔ `prompt_relates_to_task` reciprocity.

## Context

**Why this is its own Task and not in PR #70:** the PR #70 reviewer's recommended fix would balloon the chain-design PR from 9 tasks to 9 tasks + ~70 new prompt files (35 prompts × 2 scaffold files + 35 brief.md). Review attention dilutes; the slug-allocation policy (some subtasks may legitimately share a prompt; some may need distinct slugs) is non-trivial enough to warrant its own auditable unit of work. Per maintainer decision (PR #70 reply: "B"), the extraction is filed here.

**Sequencing constraint.** Tasks 032–040's subtasks are NOT dispatchable until Task 041 has extracted their prompts — otherwise the dispatching agent reads the inlined Execution Brief and bypasses the audit graph entirely. Task 041 is therefore the **first** task in the chain to execute, even though it carries no `task_blocked_by` declaration. The ordering is documented here in prose + in `tasks/readme.md` adjacent to entries 032–040.

**Slug-allocation policy (Phase 1 of this Task) is non-trivial.** Some Execution Briefs are clearly per-subtask (the 9 research subtasks each have unique research_questions). Some may share (the 6 spec-amendment subtasks all instruct "edit spec X with these acceptance criteria" — nearly identical shape, only the target spec differs). Phase 1 decides whether to extract 35 unique prompts or to consolidate similar ones into shared prompts with parameter blocks.

## Preconditions (satisfied at branch-time)

- **All of Tasks 032–040** are scaffolded with their 35 subtask files (commits `7d1bb5a` + `9e3b59f` + `8c3bec8` + `b16d910`).
- **Task 020** (`audit-prompt-fm-validate-conformance`, open) — establishes the prompt-frontmatter contract this Task's output MUST conform to. If Task 020 has not yet shipped its conformance audit, this Task uses `header-ontology.json` directly as the contract source.
- **Task 016/017/019** — flexible-frontmatter toolchain provides the validation substrate (`tools/fm/validate.py --type-check`, `tools/fm/new.py` if shipped per Task 019 ST-3).

## Build-On

- **`tools/fm/new.py`** (Task 019 ST-3 — if shipped) — template-driven scaffolder that produces the F.4.1.1 three-file scaffold for each new `/prompts/<slug>/`. If not yet shipped, this Task uses manual scaffolding from `templates/prompt.md` + `templates/notes.md`.
- **`tools/fm/extract.py --section "Execution Brief"`** — reads each subtask file's Execution Brief body for migration to `prompt.md`.
- **`tools/fm/edit.py --append-list task_uses_prompts`** — populates the parent task frontmatter post-scaffold without hand-editing.
- **`templates/prompt.md`** — existing template for `prompt.md`; minor adaptation needed for `prompt_kind: task-spec`.

## Plan

1. **Phase 1 — Slug-allocation manifest.** Decide per Execution Brief whether it gets a unique slug or shares with sibling subtasks. Produce `tasks/041-extract-subtask-prompts/slug-manifest.md` with one row per subtask: `(parent-task-id, subtask-id, source-path, target-prompt-slug, prompt_kind, share-with)`. Estimated 35 rows; estimated 28–35 unique prompt slugs after consolidation.
2. **Phase 2 — Bulk prompt scaffold.** For each unique target slug in the manifest, scaffold `/prompts/<slug>/{brief.md, prompt.md, readme.md}` with frontmatter pre-filled (`type: prompt`, `prompt_kind: task-spec`, `prompt_relates_to_task: <parent-task-slug>`, `prompt_target_agent: "Claude Code"`). Migrate the Execution Brief content into `prompt.md` body (R/I/S/E sections per `templates/prompt.md`); migrate the subtask's "Goal + Falsification + Inputs + Acceptance + Dependencies" preamble into `brief.md`.
3. **Phase 3 — Cross-link & cleanup.** (a) Append each new prompt slug to its parent task's `task_uses_prompts` via `tools/fm/edit.py`. (b) In each subtask file, REPLACE the `## Execution Brief` block + its preceding metadata (Goal, Falsification, Inputs, Acceptance, Dependencies, Effort — they all moved to brief.md) with a single one-line cross-reference: `**Prompt:** [`/prompts/<slug>/prompt.md`](../../../prompts/<slug>/prompt.md)`. The subtask file becomes a thin pointer + Parallelism + Executor + Insertion-point metadata only.
4. **Phase 4 — Reciprocity verification.** Run `tools/check-governance.sh` and verify `tools/lint-linkage.py` (or `tools/fm/validate.py --type-check`) exits 0 — confirming `task_uses_prompts` ↔ `prompt_relates_to_task` reciprocity holds across all 9 parent tasks + ~28–35 new prompts.
5. **Phase 5 — Index sync + closure.** Update `tasks/readme.md` (Task 041 status), `prompts/readme.md` (~28–35 new entries), author `friction-log.md` with FL[0-3], set `task_status: done`.

## Sample Gherkin (the maintainer authoring Phase 4 verification scenarios SHOULD produce)

```gherkin
# anchor: T.B.PROMPT.1 — task ↔ prompt audit-graph edge restored
Scenario: Parent task lists every child subtask's prompt
  Given Task 032 has 5 subtask files under `tasks/032-agents-spec-integration/subtasks/`
  And Phase 1 manifest assigns each subtask exactly one target prompt slug
  When Phase 3 cross-link completes
  Then `tasks/032-agents-spec-integration/task.md` frontmatter `task_uses_prompts`
       MUST contain ≥5 entries (one per subtask, after consolidation)
  And every entry MUST resolve to an existing `/prompts/<slug>/prompt.md`
  And every resolved prompt MUST carry `prompt_relates_to_task: agents-spec-integration`
  And `tools/fm/validate.py --type-check` MUST exit 0
```

## Todo

- [x] 1. Phase 1 — `slug-manifest.md` authored: 35 source rows → 35 target slugs (consolidation rejected; rationale in `slug-manifest.md` §Decision).
- [x] 2. Phase 2 — `/prompts/<slug>/{brief.md,prompt.md,readme.md}` scaffold authored for all 35 slugs; content migrated from each parent subtask's Goal / Falsification / Inputs / Acceptance / Dependencies / Estimated Effort / Execution Brief sections. Driver: `scripts/extract.py`.
- [x] 3. Phase 3 — `task_uses_prompts` populated on Tasks 032–039 (5/5/4/5/3/4/3/6 entries respectively); each subtask file collapsed to a thin pointer carrying only L1 frontmatter, H1, Executor / Parallelism / Insertion-point lines, and a one-line `**Prompt:**` cross-reference.
- [x] 4. Phase 4 — `tools/check-governance.sh --no-trust` exits 0; `tools/fm/validate.py --type-check` reports `Checked 370 files; 0 diagnostic(s)`; reciprocity verified across `task_uses_prompts ↔ prompt_relates_to_task` for all 8 parent tasks × 35 child prompts.
- [x] 5. Phase 5 — `tasks/readme.md` updated (Task 041 status flipped to `done`); `prompts/readme.md` lists the 35 new entries grouped by parent task; `friction-log.md` authored with FL[1] declaration; `task_status: done`.

## Falsification

Wrong cut **iff** Phase 1 manifest decides 35 unique prompts (no consolidation) AND post-Phase-3 the 35 prompts are all near-byte-identical apart from a handful of substitutions. Mitigation: Phase 1 explicitly evaluates the 6 spec-amendment subtasks (032 ST-5, 033 ST-5, 034 ST-4, 035 ST-5, 036 ST-3, 037 ST-4, 038 ST-3, 039 ST-6) for shared shape; if shape divergence is <20%, they consolidate to a single `task-spec-amendment-template` prompt parametrized by host-spec + acceptance-anchor list.

## Estimated Effort

Medium (~4–6 hours focused work). Phase 1 is the cognitively heavy step; Phases 2 and 3 are mechanical and may be executed via a Python script that consumes the Phase 1 manifest.

## Links

- Folder index: [`readme.md`](./readme.md)
- Source review: [PR #70 review C.3](https://github.com/netzkontrast/agency/pull/70#issuecomment-4390879904).
- Maintainer decision: [PR #70 reply choosing Option B](https://github.com/netzkontrast/agency/pull/70#issuecomment-4390932076).
- Affected tasks: [Tasks 032–040](../032-agents-spec-integration/task.md).
- Sibling: [Task 020 — audit-prompt-fm-validate-conformance](../020-audit-prompt-fm-validate-conformance/task.md) (corpus-wide prompt-frontmatter conformance; this Task adds new prompts that 020 will eventually re-audit).
- Governing specs: [`TASK.md`](../../TASK.md) §1, §4.3, §7.3 (linkage); [`PROMPT.md`](../../PROMPT.md) §1, §4; [`FOLDERS.md`](../../FOLDERS.md) §F.4.1.1 (prompt scaffold).
