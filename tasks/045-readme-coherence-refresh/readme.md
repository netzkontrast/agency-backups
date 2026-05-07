---
type: index
status: active
slug: readme-coherence-refresh
summary: "Folder index for Task 045 — the R.13/R.14 vehicle that reframes the README to a four-concern model and adds the Narrative Ontology section."
created: 2026-05-07
updated: 2026-05-07
---

# Task 045 — README Coherence Refresh

**What is this folder?** The Task that owns the README changes deferred from
the Wave A pass on branch `claude/update-root-readme-Qufdr`. It is the
authorised vehicle (per [README.md R.13 / R.14](../../README.md#11-spec--how-this-readme-must-be-updated))
for restructuring the README's top-level numbered sections and for changing
the meaning of the Machine / Actor / Space framing.

**Why is it here?** Wave A closed every drift fix that did *not* require a
Task (topology tree, namespace summary, linter table, ADR change-control sub-
section, session-bootstrap quick-start, root-spec reference index). Wave B
covers the items that do require a Task: the §3 reframe to a four-concern
model (Capability = `/skills/`) and the new §12 *Narrative Ontology (load-
gated)* section. The /Agency-System/ exemption added to FOLDERS.md §8 in
commit `3a5c09a` is doc-only; this Task authors the backing ADR.

## Contents

- [`task.md`](./task.md) — Goal, plan, todo, links.

## Assumptions Log

- This Task was originally scaffolded as `043-readme-coherence-refresh` on
  branch `claude/update-root-readme-Qufdr` cut from `main@8fc223d`. `main`
  subsequently advanced to include `tasks/043-renumber-duplicate-task-ids-v3`
  and `tasks/044-improve-maintenance-spec-may-07-2026`, forcing a rename to
  slot `045`. The rename was performed before the Task left `task_status: open`.
- This Task is opened on the same branch as Wave A (`claude/update-root-readme-Qufdr`)
  per the directive that all development for this session lives on the
  designated branch. A future maintainer MAY split it onto its own branch
  before execution.
- The `/Agency-System/` exemption added in commit `3a5c09a` is documentation-
  only until ADR 0001 is `Accepted`. This Task treats authoring that ADR as
  in-scope rather than spinning a separate Task.
- The `/tests/` disposition (move under `tools/tests/` vs. add to FOLDERS.md
  §8 via ADR 0002) is left as an open decision in the Task plan; this folder
  index does not pre-empt it.
