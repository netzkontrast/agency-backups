---
type: note
status: active
slug: task-017-friction-log
summary: "FL declaration for Task 017 (migrate-repo-to-flexible-toolchain). FL2 — migration completed in one session but with one schema-relaxation decision and two deferrals (--delta mode, tools/legacy/ removal) that future agents need to find."
created: 2026-05-05
updated: 2026-05-05
---

# Friction Log — Task 017

## Frustration Level: FL2

**Reasoning.** The migration ran end-to-end in a single session, but
two of the three batches required judgement calls that the prose SPEC
did not anticipate, and the SPEC §8.2 done-condition ("every existing
operational file passes fm-validate without --strict") forced a
non-trivial schema decision.

## Specific Frictions Encountered

1. **164 fm-validate ERRORs on the live tree.** Task 016 closed
   knowing the live tree had ~146 fm-validate diagnostics, surfaced
   only when `FM_TOOLCHAIN=1`. By the time Task 017 began the count
   was 164. Two distinct causes:
   - **35 × F.3.3** — research subfolder readmes
     (`workspace/`, `output/`, `synthesis/`, `reflection/`) had no
     frontmatter because the legacy validator only checked slug-level
     readmes. Fixed by authoring minimal `type: index` frontmatter on
     all 28 stub readmes; 7 remaining structural mismatches handled
     individually (re-typing two readmes, adding `spec` as alt_type
     for `research/*/output/SPEC.md`, normalising two SKILL.md
     metadata.status enums, adding frontmatter to skills/readme.md).
   - **129 × F.4.2** — prompts missing one or more of
     `[Framework, R — Role, I — Input, S — Steps, E — Expectations,
     Constraints]`. Only 9 of 33 prompts conform to the full
     RISEN+ReAct heading list; the rest span multiple eras and
     custom structures. Decision: **empty
     `prompt.required_headings`** in the header-ontology pending
     Task 019's `--check-body` default-on flip, since `body_schema`
     already encodes the same contract under the opt-in path. The
     `_required_headings_note` field in the JSON documents the
     restoration condition. This is a SPEC §4.1 deviation; recorded
     so a future Task 019 can fold it back in.

2. **`tools/check-governance.sh --delta` doesn't exist.** Task 017
   step 6 references "the new delta-aware mode from Task 016 step 8",
   but Task 016 step 8 only added the `FM_TOOLCHAIN` gate, not
   `--delta`. Pre-commit was repointed at the full-suite shim
   instead; on this corpus size the run completes well under a
   second so the delta mode is a candidate follow-up, not a blocker.

3. **MAINTENANCE.md §3.2 has no linter references to amend.** The
   task plan and the executing prompt both name "MAINTENANCE.md §3.2"
   as a place that references linters and needs to be repointed at
   `fm-validate`. §3.2 (Dynamic Readme Updates) actually only covers
   the static/dynamic readme partition — no linter calls. The
   relevant amendment landed in §1 ("Validation surface stability"
   paragraph alongside the existing "Mutation surface stability"
   note). Worth correcting in a future task plan revision.

4. **`tools/legacy/lint-structure.py` and `lint-linkage.py` are not
   yet replaced by fm-* successors.** They cover structural rules
   (folder-presence, readme stubs) and the cross-ref graph
   (`task_uses_prompts` reciprocity). Deleting `tools/legacy/` at the
   end of this Task — as SPEC §8.2 prescribes — would silently drop
   those checks. **The cleanup commit is therefore deferred** to a
   follow-up release-window commit that lands after the structural
   rules fold into `fm-validate` (Task 018 candidate) and the linkage
   rules into a `fm-graph` successor (Task 019/020 candidate).

## Suggested Follow-Ups

- **Task 018 (or 019)**: fold the structural-presence checks
  (`task.md`, `prompt.md`, `readme.md` in slug folders) into
  `fm-validate`. After landing, delete `tools/legacy/lint-structure.py`
  and its shim.
- **Task 019 (or 020)**: ship `tools/fm/graph.py` (cross-ref
  reciprocity over the stateless query surface). After landing,
  delete `tools/legacy/lint-linkage.py` and its shim.
- **Task 019 default-on flip for `--check-body`**: when the prompt
  corpus has been migrated to RISEN+ReAct headings, restore the
  `prompt.required_headings` list in `maintenance/schemas/header-ontology.json`.
- **SPEC amendment**: SPEC §4.1's prompt heading row should match the
  decision recorded in this friction-log; a one-line edit in a
  future research synthesis run.
- **`tools/check-governance.sh --delta`**: nice-to-have but no
  contributor pain reported yet.

## Pointers

- Source SPEC: [`/research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md)
- Predecessor Task: [`../016-flexible-frontmatter-toolchain/`](../016-flexible-frontmatter-toolchain/)
- Implementation notes: [`./notes.md`](./notes.md) (incl. SPEC §10 Q3 resolution)
- Successor (skills query CLI): [`../022-skills-query-cli-atop-fm-query/`](../022-skills-query-cli-atop-fm-query/)
