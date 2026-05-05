---
type: index
status: active
slug: task-018-fm-section-editor
summary: "Implementation Task: ship the fm-section editor (body-side complement to fm-edit) and flip --check-body default-on once the corpus is clean."
created: 2026-05-05
updated: 2026-05-05
---

# Task 018 — fm-section Editor + Body-Schema Phasing

**What is this folder?** The orchestration unit for the body-side editor and the Phase-3 flip of `--check-body`. Plan and contract live in [`task.md`](./task.md).

**Why is it here?** Task 016 shipped frontmatter mutation (`fm-edit`) and body validation (`fm-validate --check-body`, opt-in). Task 018 closes the loop with body mutation (`fm-section`) and promotes the body-schema check from opt-in to default-on once Task 019 has migrated the corpus.

## Linked Navigation

- [`task.md`](./task.md) — frontmatter, plan, todo, links.
- Source SPEC: [`/research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) (§13 fm-section surface, §12.6 phasing).
- Predecessor: [`/tasks/016-flexible-frontmatter-toolchain/`](../016-flexible-frontmatter-toolchain/).
