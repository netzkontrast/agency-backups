---
type: note
status: active
slug: task-041-friction-log
summary: "Friction log for Task 041 — audit-graph repair extracting 35 subtask briefs to /prompts/<slug>/. FL declaration + frictions encountered during execution."
created: 2026-05-06
updated: 2026-05-06
---

# Friction Log — Task 041

## FL Declaration (FRUSTRATED.md FL[0-3])

**FL: 1** — Minor frictions encountered (small scope mismatches between Task 041's stated scope and the actual subtask corpus shape) but no blocker; the task closed with `tools/check-governance.sh` exiting 0 across 370 files.

## Frictions

### F1 — Task description over-counts Execution Brief blocks

**What.** Task 041's `task.md` describes "35 inlined `## Execution Brief` blocks" as the target of extraction. Inspection of the corpus surfaced only **14** subtask files carrying an explicit `## Execution Brief` heading; the other 21 (mostly `tooling-*` and `spec-amendment-*` subtasks) inline their prompt content as freestanding `## Goal` / `## Acceptance Criteria` / `## Falsification` / `## Inputs` / `## Dependencies` / `## Estimated Effort` sections without a wrapping Execution Brief.

**Why it didn't block.** The Task's broader acceptance criteria are clear: every subtask file's body MUST cross-reference a prompt rather than inline its content (PROMPT.md §1 + TASK.md §1). The Phase 1 manifest therefore included all 35 subtasks rather than only the 14 with explicit `## Execution Brief` blocks. Each subtask received its own prompt slug; the 21 implicit-brief subtasks had their `## Goal` / `## Acceptance Criteria` / etc. lifted into the prompt's `brief.md` and synthesised into `prompt.md` Steps + Expectations + Constraints.

**Resolution.** Documented in `slug-manifest.md` and in this log. No spec amendment needed — the Task description was directionally correct; the count was a minor over-count that did not change the overall extraction shape.

### F2 — Phase 1 consolidation evaluation: 8 spec-amendment subtasks remained distinct

**What.** Task 041's Falsification clause invited consolidating the 8 spec-amendment subtasks (032 ST-5, 033 ST-5, 034 ST-4, 035 ST-5, 036 ST-3, 037 ST-4, 038 ST-3, 039 ST-6) into a single `task-spec-amendment-template` prompt parametrised by host-spec + acceptance-anchor list, **iff shape divergence is <20%**.

**Why it didn't block.** Inspection of all 8 spec-amendment subtasks surfaced ~70-80% body divergence per pair: different host specs, different cited research SPECs, different precursor linters, different §-anchors, different Gherkin-anchor namespaces, different counts of new scenarios, different dependency chains. Consolidation rejected; each spec-amendment subtask received its own prompt slug.

**Resolution.** Decision documented in `slug-manifest.md` §Decision. The 35 source subtasks map to 35 unique target prompt slugs. Re-running the consolidation evaluation in a future Task is unnecessary unless a follow-up amendment harmonises the 8 spec-amendment subtask bodies.

### F3 — `tools/fm/new.py` was not used; bespoke scaffolder was authored instead

**What.** The Task's "Build-On" section names `tools/fm/new.py` as the template-driven scaffolder for new `/prompts/<slug>/` folders. The actual extraction used a bespoke Python script at `tasks/041-extract-subtask-prompts/scripts/extract.py` rather than `tools/fm/new.py`.

**Why.** `tools/fm/new.py prompt --slug ...` produces a single `prompt.md` file (no `brief.md` or `readme.md`) and writes it to the current working directory rather than to `/prompts/<slug>/`. Producing the F.4.1.1-mandatory three-file scaffold + populating each file with content migrated from the parent subtask file requires logic beyond `fm-new`'s remit. The bespoke `extract.py` is a one-shot driver; it lives under `tasks/041-extract-subtask-prompts/scripts/` per the readme's expectation (`Assumptions Log` bullet 2).

**Resolution.** No drift — the Task readme explicitly anticipates this case ("The Task ships that script under `tasks/041-extract-subtask-prompts/scripts/extract.py` if useful"). A successor Task could harden `tools/fm/new.py` to emit the three-file scaffold + accept a content-migration source path; that is out of scope for Task 041.

### F4 — Frontmatter quote-style preservation required line-based edits

**What.** First-pass extraction used a YAML round-trip (parse → mutate `task_uses_prompts` → re-serialise) on parent task.md files. The round-trip dropped quotes from string-typed values (`task_id: "032"` → `task_id: 032`; `task_owner: "unassigned"` → `task_owner: unassigned`) — semantically equivalent under the validator but a noisy diff.

**Why it didn't block.** `tools/fm/validate.py --type-check` accepted both forms (0 diagnostics either way). The diff noise was cosmetic.

**Resolution.** The script was refactored to do a line-based frontmatter edit that preserves all original lines verbatim and only mutates `task_uses_prompts` (replaced with the new list) and `updated` (bumped to today's date). The first-pass output was reverted and the script re-run, producing a minimal diff against the original task.md frontmatter blocks.

## Validation

- `tools/check-governance.sh --no-trust` exits 0; frontmatter linter reports `Checked 370 files; 0 diagnostic(s)` (was 300 pre-Task; 70 new files = 35 prompts × `brief.md` + `prompt.md` + `readme.md` − 35 since the change includes the slug-manifest, friction-log, and script under `tasks/041-extract-subtask-prompts/`).
- `tools/fm/validate.py --type-check` exits 0; reciprocity holds across `task_uses_prompts ↔ prompt_relates_to_task` for all 8 parent tasks × 35 child prompts.
- Every `/prompts/<slug>/` folder carries the F.4.1.1-mandatory three-file scaffold (`brief.md`, `prompt.md`, `readme.md`).
- Every subtask file under `tasks/03[2-9]*/subtasks/[0-9]*.md` has been collapsed to a thin pointer carrying only L1 frontmatter, H1 title, the original Executor / Parallelism / Insertion-point metadata lines, and a one-line `**Prompt:** [...](.../prompt.md)` cross-reference.
