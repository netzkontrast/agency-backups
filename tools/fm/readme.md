---
type: index
status: active
slug: tools-fm-readme
summary: "Entry point for the flexible-frontmatter toolchain: stateless CLIs that read, validate, query, and edit frontmatter and body sections across the repo."
created: 2026-05-05
updated: 2026-05-05
---

# `tools/fm/` — Flexible Frontmatter Toolchain

**What is this folder?** The stateless CLI surface that operationalises the frontmatter ontology. Each script does one job, exits non-zero on failure, and stays composable through stdout. The normative contract lives in [`/research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md); this folder is the implementation.

## Tools

| Name | One-line summary | Link |
| --- | --- | --- |
| `fm-validate` | Walks paths, enforces required keys + headings, optional body schemas. | [`validate.py`](./validate.py) |
| `fm-extract` | Reads frontmatter, sections, body, or TOC out of a single file. | [`extract.py`](./extract.py) |
| `fm-edit` | Mutates frontmatter scalars and lists; bumps `updated:`. | [`edit.py`](./edit.py) |
| `fm-query` | Selector-based search across operational roots; emits text, JSON, or paths. | [`query.py`](./query.py) |
| `fm-section` | Section-scoped body edits: replace, append, check-task, rename. | [`section.py`](./section.py) |

## Quick start

```shell
python3 tools/fm/validate.py tasks/                         # lint a subtree
python3 tools/fm/extract.py path/to/file.md --section Goal  # read one section
python3 tools/fm/query.py "type=task,status=active"          # find open tasks
```

## See also

- [`cookbook.md`](./cookbook.md) — eight worked examples with shell snippets.
- [`SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) — normative behaviour, exit codes, and diagnostics.
- [`../readme.md`](../readme.md) — how this folder fits the wider tooling layer.
