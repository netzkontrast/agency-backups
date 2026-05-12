---
type: index
status: active
slug: task-019-fm-toolchain-suite-integration
summary: "Index for the suite-integration epic that decomposes the gap between atomic fm-* tools and the complete authoring/refactoring/validation surface into nine parallelizable /sc:agent subtasks."
created: 2026-05-05
updated: 2026-05-05
---

# Task 019 — fm Toolchain Suite Integration

**What is this folder?** The orchestration unit for the v2 toolchain. Plan + acceptance live in [`task.md`](./task.md); the parallelizable agent prompts live under [`subtasks/`](./subtasks/).

**Why is it here?** Tasks 016 (atoms) and 018 (body editor) ship the read/write primitives. Task 019 builds the molecules — the cross-file refactors, scaffolds, validation extensions, docs, and SPEC amendments that turn the atoms into a complete tooling surface. Each subtask is sized for one `/sc:agent` invocation and most can run in parallel.

## Linked Navigation

- [`task.md`](./task.md) — frontmatter, plan, todo, links, falsification table.
- [`subtasks/readme.md`](./subtasks/readme.md) — index of the nine parallelizable subtask prompts and the recommended spawn recipe.
- Source SPEC: [`/research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md).
- Predecessor: [`/tasks/016-flexible-frontmatter-toolchain/`](../016-flexible-frontmatter-toolchain/).
- Peer (parallel): [`/tasks/018-fm-section-editor/`](../018-fm-section-editor/).
