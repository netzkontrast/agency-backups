---
type: prompt
status: draft
slug: integrate-dramatica-ncp-skills
summary: "Stub prompt for Task 013 — the binding instruction set is authored in Task 013 step 14; this stub exists so /tasks/013/ link integrity passes the linkage linter."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: integrate-dramatica-ncp-skills
prompt_spawned_from_research: ""
---

# Integrate Dramatica Skills With NCP and Novel-Architect — Stub

## Status

`draft`. The full executable instruction set is authored as **step 14** of [`/tasks/013-integrate-dramatica-ncp-skills/task.md`](../../tasks/013-integrate-dramatica-ncp-skills/task.md). This file is intentionally a stub right now so that:

1. The linkage linter (`tools/lint-linkage.py`, [`TASK.md §7.2`](../../TASK.md)) accepts the `task_uses_prompts: integrate-dramatica-ncp-skills` declaration on the Task.
2. Future agents reading the Task can navigate to this folder and find the in-progress prompt rather than a 404.

## Framework

**RISEN + ReAct.** Authoring will use `RISEN` for the structured output sections (schemas, navigator CLI, scenario taxonomy) and `ReAct` for the tool-use loop that walks the existing skills, extracts term sections, and generates per-term frontmatter blocks.

## § RFC 2119

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

## What this prompt will contain when authored

The full version (filled in step 14 of the Task plan) MUST include:

- **R — Role.** A schema author + Python tool author + Dramatica-vocabulary annotator who is fluent in the repo's frontmatter ontology and the NCP schema.
- **I — Input.** Pointers to the four touched skills, the relevant `maintenance/schemas/` files (Task 011 dependency), the NCP pinned schema, and the persona/scenario tables from this Task.
- **S — Steps.** A ReAct loop that walks Type-bucket files, emits per-term frontmatter, builds `ontology.json`, and runs `validate.py` after every batch.
- **E — Expectations.** The seven Gherkin scenarios in `task.md § Acceptance Criteria (Gherkin)` MUST all pass; the token-cost benchmark MUST hit the ≥60% reduction threshold.
- **N — Narrowing.** Out-of-scope: re-licensing Dramatica prose, coining new NCP enums, refactoring `novel-architect`'s NCP canon file, prose drafting for the persona projects.

## Provisional pre-conditions for promoting this prompt to `status: active`

The author MUST verify, before flipping `status` from `draft` to `active`:

- **PR-1.** The schemas in `maintenance/schemas/narrative-ontology/` are merged or scoped within this task's `task_affects_paths`.
- **PR-2.** The persona/scenario set in `task.md` has not changed since the prompt body was drafted (or this prompt is updated accordingly).
- **PR-3.** The NCP pinned upstream SHA recorded in `skills/ncp-author/SKILL.md` matches the `ncp_schema_min_version` referenced by the schemas.

## Links

- Owning Task: [`/tasks/013-integrate-dramatica-ncp-skills/task.md`](../../tasks/013-integrate-dramatica-ncp-skills/task.md)
- Governing specs: [`PROMPT.md`](../../PROMPT.md), [`TASK.md`](../../TASK.md), [`AGENTS.md`](../../AGENTS.md)
- Critical-thinking source: [`/skills/research-prompt-optimizer/`](../../skills/research-prompt-optimizer/)
- Spec-discipline source: [`/skills/spec-skill/`](../../skills/spec-skill/)
