---
type: prompt
status: draft
slug: refactor-governance-from-specs
summary: "Skeleton task-spec prompt that drives Task 001: convert Spec-A/B/C + G/H/I + J/K/L into linters, hooks, templates."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: task-spec
prompt_framework: RISE-DX
prompt_target_agent: "Claude Code"
prompt_relates_to_task: refactor-governance-from-specs
prompt_spawned_from_research: ""
---

# Refactor Governance from Specs — Task-Spec Prompt (Skeleton)

> **Status:** This is a **skeleton**. Plan step 1 of [`/tasks/001-refactor-governance-from-specs/task.md`](../../tasks/001-refactor-governance-from-specs/task.md) is to flesh this prompt out per `PROMPT.md`. Until then, the body below is the *outline* an executing agent must fill in before running the task.

## Framework

**RISE-DX** — Role, Input, Steps, Expectations, with explicit Reflection / Discipline blocks.

## R — Role

You are the **Repository Governance Engineer**. Your job is to take prose specifications and turn them into deterministic, mechanically-enforced rules: linters, pre-commit hooks, and templates that a future agent cannot violate without an exit-code-1 diagnostic.

## I — Input (to flesh out)

- Three source specs:
  - `/research/agent-prompt-specs-3-systems-sdd/output/SPEC.md` (A/B/C)
  - `/research/agentic-session-continuity-spec/output/` (G/H/I)
  - `/research/agentic-eval-trust-improvement-spec/output/` (J/K/L)
- The repo's current governance specs: `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`.
- The frontmatter ontology: `/research/obsidian-frontmatter-agentic-spec/output/SPEC.md`.

## S — Steps (to flesh out)

The full step list is documented in [`/tasks/001-refactor-governance-from-specs/task.md`](../../tasks/001-refactor-governance-from-specs/task.md) §Plan. This prompt's job, when fleshed out, is to expand each Plan step into RFC-2119 instructions with concrete acceptance criteria and failure-handling rules.

## E — Expectations (to flesh out)

Deliverables, on full execution:

1. `tools/lint-frontmatter.{sh,py}`
2. `tools/lint-structure.{sh,py}`
3. `tools/lint-linkage.{sh,py}`
4. `.githooks/pre-commit`
5. `templates/task.md`, `templates/prompt.md`, `templates/research-readme.md`
6. Updates to `PRE_COMMIT.md` invoking the linters.
7. Continuity-hook artifacts per Spec-G/H/I.
8. Trust-audit script per Spec-J/K/L.

## D — Discipline

- RFC 2119 normativity, exactly one normative keyword per sentence.
- Output format locked per `PROMPT.md` §5.
- Failure handling: if a source spec is missing or unparseable, the agent MUST stop and file a follow-up prompt under `/prompts/` rather than guessing.

---

**Next action for the executing agent:** Replace each "to flesh out" block above with concrete RISE-DX content, then mark this prompt's `status: active`.
