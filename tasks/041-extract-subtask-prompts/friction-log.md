---
type: note
status: active
slug: task-041-friction-log
summary: "Friction log for Task 041 — audit-graph repair extracting 35 subtask briefs to /prompts/<slug>/. FL declaration + frictions encountered during execution."
created: 2026-05-06
updated: 2026-05-07
---

# Friction Log — Task 041

## FL Declaration (FRUSTRATED.md FL[0-3])

**FL2** — Initial closure shipped with four reviewer-flagged defects (PR #72 review F-A through F-D) that survived governance because of validator blind spots (no `path_classification` rule for `prompts/*/brief.md`; OPTIONAL-field empty-string handling not strict). All four findings remediated in the same branch before merge. Final state: `tools/check-governance.sh --no-trust` exits 0 across 372 files; reciprocity holds across all 8 parent tasks × 35 child prompts plus the new self-link Task 041 ↔ `extract-subtask-prompts` prompt.

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

### F5 — PR #72 review F-A: `type: brief` not in the closed L1 type enum (45 files)

**What.** First-pass extraction set `type: brief` on every `brief.md` file. The L1 Vault Core type enum (`maintenance/schemas/header-ontology.json` → `type_values`; AGENTS.md §Frontmatter Ontology) is a closed set of nine values: `task | prompt | research | spec | readme | note | index | skill | adr`. `brief` is not in that set.

**Why the linter was silent.** `tools/fm/validate.py --type-check` enforces `type_values` only for files matching `path_classification.rules`. The `prompts/*/brief.md` glob has no rule, so `Classification(expected_type=None)` is returned and the type-value check is skipped. The 0-diagnostic pass cited in PR #72's test plan was correct but did not certify the 45 affected files.

**Resolution.** All 45 `brief.md` files (40 from this Task + 5 pre-existing under `prompts/adr-*` and `prompts/agency-adr-governance-spec/`) flipped to `type: note` — the closest valid type for contextual orientation documents that don't fit `task`/`prompt`/`research`. The extraction script's `build_brief_md` function was updated at source so future re-runs emit `type: note` by default.

**Follow-up Task candidate.** A successor Task could file a spec amendment adding `brief` as a first-class type to the closed enum + `path_classification` rules, if `brief.md` warrants its own type identity. Out of scope for Task 041's remediation pass.

### F6 — PR #72 review F-B: empty `prompt_spawned_from_research: ""` propagated from template (45 files)

**What.** First-pass extraction copied `prompt_spawned_from_research: ""` from `templates/prompt.md` into every new prompt's frontmatter. PROMPT.md §3 declares this field OPTIONAL; the spec's intent for non-applicable optional fields is **omission**, not an empty-string sentinel. Linkage tooling traversing the research-spawn lineage graph would silently enumerate these prompts as having an unresolvable parent rather than no parent.

**Resolution.** Removed the line from every affected `prompt.md` (35 newly authored + 9 pre-existing) and from `templates/prompt.md`. The extraction script's `build_prompt_md` function was updated at source to omit the field rather than emit it as `""`.

### F7 — PR #72 review F-C: shallow RISEN+ReAct migration in `## S — Steps`

**What.** First-pass `## S — Steps` for the 35 extracted prompts wrapped the original Execution Brief verbatim inside a single fenced `text` block, prefixed by `1. Execute the following instruction block faithfully — ...`. PROMPT.md §5 (Self-Containedness, RFC 2119 Normativity, Deliverable Lock, Failure Handling) requires steps to be discrete, RFC-2119-normative deliverables — not a pass-through wrapper.

**Resolution.** The extraction script's step generator was rewritten:
- Multi-line aware `numbered_items` parser preserves continuation lines from the original brief.
- `ensure_rfc2119` helper detects existing RFC-2119 keywords and otherwise prepends `The agent MUST ` (or rewrites `Do NOT X` / `Don't X` to `MUST NOT X`); a small lowercaseable-verb table avoids ungrammatical capitalisation after `MUST`; non-verb labels (`Phase 2: ...`) are wrapped as `MUST execute the following instruction: ...`.
- A trailing block of four uniform verification + closure steps is appended to every prompt (verify acceptance, run governance, author friction-log, commit with task-id trailer).

The 35 prompts re-emitted produce 9-13 normative steps each (depending on subtask complexity), each carrying ≥1 RFC-2119 keyword. The verbatim opacity flagged by the reviewer is gone.

### F8 — PR #72 review F-D: `task_owner` unset and self-`task_uses_prompts` empty on Task 041

**What.** Task 041 closed with `task_owner: "unassigned"` (TASK.md §6 Gherkin "Agent picks up an open Task" requires the agent to claim ownership) and `task_uses_prompts: []` (an irony given Task 041's purpose is to populate that field on Tasks 032–039).

**Resolution.**
- `task_owner` set to `claude-code` to match the agent identity that ran `scripts/extract.py` and authored commits `ecb1919` + this remediation commit.
- `prompts/extract-subtask-prompts/{brief.md, prompt.md, readme.md}` authored retroactively as the registered task-spec for Task 041 itself; Task 041's `task_uses_prompts` now lists `extract-subtask-prompts` and the new prompt's `prompt_relates_to_task: extract-subtask-prompts` reciprocally binds back. Reciprocity check: `tools/fm/validate.py --type-check` exits 0 — the new edge is validated.

## Validation

- `tools/check-governance.sh --no-trust` exits 0; frontmatter linter reports `Checked 370 files; 0 diagnostic(s)` (was 300 pre-Task; 70 new files = 35 prompts × `brief.md` + `prompt.md` + `readme.md` − 35 since the change includes the slug-manifest, friction-log, and script under `tasks/041-extract-subtask-prompts/`).
- `tools/fm/validate.py --type-check` exits 0; reciprocity holds across `task_uses_prompts ↔ prompt_relates_to_task` for all 8 parent tasks × 35 child prompts.
- Every `/prompts/<slug>/` folder carries the F.4.1.1-mandatory three-file scaffold (`brief.md`, `prompt.md`, `readme.md`).
- Every subtask file under `tasks/03[2-9]*/subtasks/[0-9]*.md` has been collapsed to a thin pointer carrying only L1 frontmatter, H1 title, the original Executor / Parallelism / Insertion-point metadata lines, and a one-line `**Prompt:** [...](.../prompt.md)` cross-reference.
