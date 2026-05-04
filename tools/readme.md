---
type: index
status: active
slug: tools-root
summary: "Repository tooling: frontmatter validator, governance lints, and small CLI helpers that consume the frontmatter ontology."
created: 2026-05-04
updated: 2026-05-04
---

# Tools

**What is this folder?** Small scripts that consume the frontmatter ontology defined in [`TASK.md`](../TASK.md) §3.

**Why is it here?** The ontology only has teeth if it is mechanically validated. Future agents can extend this folder with linters, graph dumpers, or a CLI that lists open tasks.

## Contents

- [`validate-frontmatter.py`](./validate-frontmatter.py) — Walks `/tasks/`, `/prompts/`, `/research/` and verifies L1 + L2 keys are present, YAML nesting ≤ 1, no surviving `REPLACE` tokens. Exit 1 on any diagnostic. Required by [`PRE_COMMIT.md`](../PRE_COMMIT.md) §7.

## Workflow Assumptions

- The validator is intentionally dependency-free (pure stdlib) so it runs on any clone without `pip install`.
- It is a parser approximation, not a full YAML library — sufficient for the flat ontology this repo enforces.
- Future linters (directory-structure, linkage-reciprocity) are deliverables of [`/tasks/001-refactor-governance-from-specs/`](../tasks/001-refactor-governance-from-specs/).
