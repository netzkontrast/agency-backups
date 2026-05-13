---
type: index
status: active
slug: fm-toolchain-per-entry-frontmatter
summary: "Directory index for Task 095 — extend tools/fm/edit.py + tools/fm/validate.py so per-entry inline YAML card blocks (MIF Level 3 schema in skills/novel-architect/references/learnings.md) can be mutated and validated entry-by-entry. Blocks Task 088 (MIF L3 backport), which discovered the toolchain limitation."
created: 2026-05-13
updated: 2026-05-13
---

# Task 095 — fm-toolchain: Per-Entry Frontmatter Mutation + MIF L3 Validation

**What:** Tool-extension Task filed during Task 088's working session when the executing agent discovered that `tools/fm/edit.py` operates on a single file-level YAML frontmatter block at byte 0 of a Markdown file and cannot reach inline per-entry card blocks. The MIF Level 3 schema at [`skills/novel-architect/schemas/mif-level3.yaml`](../../skills/novel-architect/schemas/mif-level3.yaml) requires exactly such per-entry blocks. This Task ships the missing capability so Task 088 can proceed.

**Why here:** Per [TASK.md §2](../../TASK.md), every coordination unit lives in `/tasks/<NNN>-<slug>/`. This is a tooling Task (not a sub-task of Epic 083, which is novel-architect-specific) and so lives at top-level under its own ID `095`.

## Navigation

- [task.md](./task.md) — Task spec: Goal, Context, Plan, Todo, Acceptance, Links.

## Assumptions Log

- (none)
