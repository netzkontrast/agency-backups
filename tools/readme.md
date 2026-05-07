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

- [`validate-frontmatter.py`](./validate-frontmatter.py) — Walks `/tasks/`, `/prompts/`, `/research/`, `/templates/`, `/tools/` and verifies L1 + L2 keys are present, YAML nesting ≤ 1, no surviving `REPLACE` tokens. Path classification anchors on the first known governance root in the path, so the validator works whether invoked with repo-relative or absolute paths and from any cwd. Waivers live in [`./.frontmatter-waivers`](./.frontmatter-waivers) and are resolved relative to the script (not cwd). Exit 1 on any diagnostic. Required by [`PRE_COMMIT.md`](../PRE_COMMIT.md) §7.
- [`check-narrative-ontology-load.py`](./check-narrative-ontology-load.py) — WARN-tier (exit 2) heuristic for AGENTS.md NO.5: flags tasks whose `task_affects_paths` does NOT match `skills/dramatica-*` / `skills/ncp-*` / `skills/novel-*` yet still read `maintenance/schemas/narrative-ontology/`. Accepts a task folder or `task.md`; advisory only inside `check-governance.sh`.

## Workflow Assumptions

- The validator is intentionally dependency-free (pure stdlib) so it runs on any clone without `pip install`.
- It is a parser approximation, not a full YAML library — sufficient for the flat ontology this repo enforces.
- Future linters (directory-structure, linkage-reciprocity) are deliverables of [`/tasks/001-refactor-governance-from-specs/`](../tasks/001-refactor-governance-from-specs/).
