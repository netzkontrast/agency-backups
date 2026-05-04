---
type: index
status: active
slug: templates-root
summary: "Copy-and-edit starter files carrying the L1 + L2 frontmatter required by TASK.md §3."
created: 2026-05-04
updated: 2026-05-04
---

# Templates

**What is this folder?** Frontmatter-correct starter files for new Tasks, Prompts, and Research workspaces.

**Why is it here?** The new architecture (see [`TASK.md`](../TASK.md)) requires every operational file to carry L1 + a domain L2 namespace. Without templates, future agents reauthor frontmatter from memory and drift. Copy a template, fill the `REPLACE` markers, validate with `tools/validate-frontmatter.py`.

## Contents

- [`task.md`](./task.md) — Starter for `/tasks/<NNN>-<slug>/task.md`.
- [`prompt.md`](./prompt.md) — Starter for `/prompts/<slug>/prompt.md`.
- [`research-readme.md`](./research-readme.md) — Starter for `/research/<slug>/readme.md`.

## Workflow Assumptions

- Templates carry `REPLACE` markers in every field that requires a value. The validator flags any `REPLACE` token that survives into a real file.
- Templates intentionally omit the optional `tags`, `aliases`, `cssclasses` (L0) keys; add them only when needed.
