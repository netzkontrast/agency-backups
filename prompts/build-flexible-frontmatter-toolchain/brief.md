# Brief — build-flexible-frontmatter-toolchain

## Raw user request

Spawned from `/research/flexible-frontmatter-toolchain/output/SPEC.md`. The original user request (see `/prompts/flexible-frontmatter-toolchain/brief.md`) explicitly asks for "a new Task, for implementing the newly defined toolchain". This prompt is that implementation prompt.

## Target audience / intended model

- Executor: Claude Code (Opus 4.7) or any equivalently capable Python-tooling agent.
- Runtime: repo-local Python 3.11 stdlib, no extra dependencies.

## Use-case context

- The implementation Task is `/tasks/016-flexible-frontmatter-toolchain/`.
- The four CLI tools (`fm-validate`, `fm-extract`, `fm-edit`, `fm-query`) are specified in SPEC §5.
- Legacy linters (`tools/validate-frontmatter.py`, `tools/lint-structure.py`, `tools/lint-linkage.py`) MUST stay live during this Task — Task 017 retires them.

## Decisions captured before drafting

- One-diagnostic-per-problem shape (modelled on `skills/skill-creator/scripts/quick_validate.py`).
- Token caps (4 KB / 2 KB / 1 KB) are normative; not config options.
- `fm-edit` is restricted to T1+T2; T3/T4 changes file as a Task.
- Header ontology lives in `maintenance/schemas/header-ontology.json`; Python loads it, never hardcodes.
