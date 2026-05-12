---
type: note
status: active
slug: task-018-friction-log
summary: "FL declaration for Task 018 (fm-section-editor). FL1 — implementation matched the SPEC closely; one invariant-check sign-error caught by tests; one scope item explicitly deferred to Task 020 per SPEC §12.6 phasing."
created: 2026-05-05
updated: 2026-05-05
---

# Friction Log — Task 018

## Frustration Level: FL1

**Reasoning.** SPEC §13 was an unusually concrete contract: every
operation, exit code, and invariant was already enumerated, and the
helpers in `tools/fm/_core.py` (`find_all_section_bodies`,
`detect_shape`, `validate_section_body`, `FileLock`) covered most of
the heavy lifting. Implementation, tests, and the two SPEC amendments
fit a single session. The only friction was a sign-error in the
invariant check on the first run.

## Specific Frictions Encountered

1. **Invariant check used full-file indices for body-relative spans.**
   First implementation of `_verify_unchanged_outside` sliced the
   original text using `span.heading_line` directly, but
   `SectionSpan` uses **body-relative** line indices (so the
   frontmatter's lines are not counted). Every operation failed with
   "internal invariant violated" until the verification was
   re-anchored on the body offset (`orig[len(fm_block):]`). Caught
   immediately by the test suite — under 60 seconds turnaround.

2. **`load_ontology()` couldn't be invoked from outside the repo
   CWD.** The cross-reference unit test creates a temp-dir mock repo
   and chdirs into it, which broke the schema lookup because
   `repo_root_from_cwd` walks upward looking for `AGENTS.md`. Added
   a module-relative fallback so the function gracefully resolves the
   shipped ontology when the CWD-walk yields nothing. This is
   strictly additive — when the repo is laid out normally the old
   path wins.

3. **Phase 3 flip is Task 020 territory.** Step 7 of the task plan
   says "flip --check-body default-on", but SPEC §12.6 explicitly
   places that in Task 020 (after Task 019 migrates the corpus). The
   step was checked-with-deferral so the Todo block stays auditable
   without claiming work that hasn't actually happened. A separate
   sub-task is NOT needed because Task 020 already exists in the
   migration ladder.

## Suggested Follow-Ups

- **Task 019 (corpus migration for body-schema)**: now unblocked.
  The body-schema validator and the section editor are both shipped;
  Task 019 can begin migrating prompts and tasks to the per-type
  body shapes without further tool work.
- **`fm-section --replace --from-text <str>`**: a non-stdin variant
  for shell pipelines that already have the text in a variable.
  Filed as nice-to-have, not blocking.
- **Cross-ref scan for `--rename` is conservative.** It looks for
  Markdown `(...#anchor)` links matching the slugified heading; it
  does NOT detect prose mentions like "the Goal section in
  task-018". A prose-text scan would catch more cases at the cost of
  false positives. Worth revisiting if a contributor surfaces a real
  miss.

## Pointers

- Source SPEC: [`/research/flexible-frontmatter-toolchain/output/SPEC.md §13`](../../research/flexible-frontmatter-toolchain/output/SPEC.md)
- Predecessor: [`../016-flexible-frontmatter-toolchain/`](../016-flexible-frontmatter-toolchain/)
- Migration peer: [`../017-migrate-repo-to-flexible-toolchain/`](../017-migrate-repo-to-flexible-toolchain/)
- Phase 3 successor: [`../020-audit-prompt-fm-validate-conformance/`](../020-audit-prompt-fm-validate-conformance/)
