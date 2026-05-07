---
type: index
status: active
slug: tools-fm-readme
summary: "Entry point for the flexible-frontmatter toolchain: stateless CLIs that read, validate, query, and edit frontmatter and body sections across the repo."
created: 2026-05-05
updated: 2026-05-07
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
| `check-duplicate-task-id` | Detects unexplained duplicate `task_id` values across active tasks (closes [TASK.md §8.1](../../TASK.md#81-concurrent-task-numbering)). Advisory in `tools/check-governance.sh` during the Task 043 migration window; promote to gating with `FM_DUPLICATE_TASK_ID_STRICT=1`. (Task 033 ST-3.) | [`check-duplicate-task-id.py`](./check-duplicate-task-id.py) |
| `check-task-lifecycle-classification` | Manual helper that evaluates the [TASK.md §4.7](../../TASK.md#47-the-updated-lifecycle-closure-with-continuity) four-condition test for a Task transitioning to `updated` or `abandoned` (and the [§8.3](../../TASK.md#83-abandonment) abandonment rationale). Implements the four-condition fallback; pending migration onto the ratified five-signal `classify_task` algorithm at [`research/spec-staleness-decision-formalization/output/SPEC.md §1`](../../research/spec-staleness-decision-formalization/output/SPEC.md). NOT wired into `tools/check-governance.sh`. (Task 033 ST-4.) | [`check-task-lifecycle-classification.py`](./check-task-lifecycle-classification.py) |

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
