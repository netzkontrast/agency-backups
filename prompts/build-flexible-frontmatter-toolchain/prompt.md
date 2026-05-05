---
type: prompt
status: active
slug: build-flexible-frontmatter-toolchain
summary: "Implementation prompt for Task 016: build the four-tool stateless frontmatter toolchain (fm-validate, fm-extract, fm-edit, fm-query) plus header-ontology JSON, per /research/flexible-frontmatter-toolchain/output/SPEC.md."
created: 2026-05-05
updated: 2026-05-05
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: "flexible-frontmatter-toolchain"
prompt_spawned_from_research: "flexible-frontmatter-toolchain"
---

# Build the Flexible Frontmatter Toolchain — Implementation Prompt

## Framework

**RISEN + ReAct.** Implementation work proceeds via Reason→Act→Observe cycles per CLI tool; RISEN frames the deliverable surface.

## R — Role

You are a Python tooling engineer with zero tolerance for hidden state. You write small, single-file CLI scripts that read the live filesystem and emit deterministic diagnostics. You do not introduce new runtime dependencies.

## I — Input

- `/research/flexible-frontmatter-toolchain/output/SPEC.md` — the contract. Read in full before writing code.
- `/tools/_frontmatter.py`, `/tools/validate-frontmatter.py`, `/tools/lint-structure.py`, `/tools/lint-linkage.py`, `/tools/check-governance.sh` — current linter set. The new tools coexist with these for one release window.
- `/tools/dramatica-nav/extract.py`, `/tools/dramatica-nav/validate.py`, `/tools/dramatica-nav/nav.py` — direct prior art for split-by-concern + ERROR/WARN diagnostic shape.
- `/skills/skill-creator/scripts/quick_validate.py` — diagnostic-shape inspiration (one diagnostic per problem, plain text).
- `/maintenance/language-spec.md §4` — frontmatter ontology source of truth.

## S — Steps

1. The implementer MUST scaffold `tools/fm/` per SPEC §5.5: `__init__.py`, `_core.py`, `validate.py`, `extract.py`, `edit.py`, `query.py`. Move `tools/_frontmatter.py` into `tools/fm/_core.py` and replace the original with a re-export shim.
2. The implementer MUST encode the §3 required-key matrix and §4 required-heading matrix in `maintenance/schemas/header-ontology.json` and load them from there in `fm-validate`. Hardcoding the matrices in Python is forbidden.
3. The implementer MUST implement `fm-validate` matching the diagnostic shape in SPEC §5.1 byte-for-byte. The `did-you-mean` rule (SPEC §3.4) MUST use Levenshtein distance ≤ 1.
4. The implementer MUST implement `fm-extract` honouring the 4 KB / 2 KB output caps in SPEC §5.2 and emit the `[truncated; original N bytes]` marker exactly.
5. The implementer MUST implement `fm-edit` with an OS file lock (`fcntl.flock`) and a post-write byte-identical-body assertion (SPEC §5.3).
6. The implementer MUST implement `fm-query` with no writes, no `.agent_cache/` reads, and the default-scope cap (SPEC §5.4). Output MUST default to ≤ 1 KB.
7. The implementer MUST write `tests/fm/` using only `unittest`. Coverage MUST include every Gherkin scenario in SPEC §6 (F.6.1–F.6.7) plus every falsification attack in `reflection/M01-falsification.md` (P1–P5).
8. The implementer MUST add a feature-flagged step to `tools/check-governance.sh`: when `FM_TOOLCHAIN=1`, run `fm-validate` instead of the legacy validator. Default = unset = legacy behaviour. Task 017 flips the default.
9. The implementer MUST close the task with a `friction-log.md` declaring FL[0–3] and a one-line append to `maintenance/run-log.md`.

## E — Expectations

- A new `tools/fm/` package containing five files plus tests under `tests/fm/`.
- A new `maintenance/schemas/header-ontology.json` matching SPEC §4.1.
- A re-export shim at `tools/_frontmatter.py` that imports from `tools.fm._core` for one release cycle.
- `tools/check-governance.sh` exit 0 on the staged tree, both with and without `FM_TOOLCHAIN=1`.
- `tasks/016-flexible-frontmatter-toolchain/friction-log.md` declaring an FL.
- A short append in `maintenance/run-log.md` per `MAINTENANCE.md §2.3`.

## Constraints

- **No new runtime dependencies.** Python 3.11 stdlib only. No `pyyaml`, no `jsonschema`, no `pydantic`. Hand-rolled YAML parsing reuses the existing `_frontmatter.py` parser.
- **No persisted index.** `fm-query` MUST NOT read or write any cache file. Process-local memoisation per invocation is fine.
- **No T3/T4 mutations from `fm-edit`.** The tool refuses any operation that would touch a heading, rename a slug, or modify root governance — those go to a Task per `MAINTENANCE.md §1`.
- **One diagnostic per problem.** `fm-validate` MUST NOT emit cumulative or summary lines except a final one-line `Checked N files; M diagnostic(s).` footer.
- **Token budgets are normative.** `fm-extract --section` ≤ 4 KB; `fm-extract --frontmatter` ≤ 2 KB; `fm-query` default ≤ 1 KB. Exceeding any cap is an implementation bug, not a config option.
- **The legacy linters STAY** during this task. Removing them is Task 017's job. The two run side-by-side until the migration cuts over.
