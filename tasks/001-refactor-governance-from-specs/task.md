---
type: task
status: archived
slug: refactor-governance-from-specs
summary: "Encode the rules from Spec-A/B/C (3-Systems SDD), Spec-G/H/I (Session Continuity), and Spec-J/K/L (Eval/Trust/Improvement) into repository linters, pre-commit hooks, and templates."
created: 2026-05-04
updated: 2026-05-12
task_id: "001"
task_status: updated
task_owner: "claude-code"
task_priority: P1
task_uses_prompts:
  - refactor-governance-from-specs
task_spawns_research: []
task_spawns_prompts: []
task_superseded_by:
  - "026"
task_affects_paths:
  - PRE_COMMIT.md
  - .githooks/
  - tools/
  - templates/
  - tasks/001-refactor-governance-from-specs/
---

# Task 001 — Refactor Governance from Specs

## Goal

Convert the *theoretical* recommendations of the recently-completed research specs into *enforced* repository rules. Concretely: produce linters, pre-commit hooks, and frontmatter templates that mechanically check the conventions described in Spec-A/B/C, Spec-G/H/I, and Spec-J/K/L, so the next agent that writes a Task, Prompt, or Research run cannot drift from the architecture without the hook flagging it. The Task is **done** when a clean clone of this repo can run `tools/check-governance.sh` (or equivalent) and that script verifies every applicable rule from the three spec families on every file under `/tasks/`, `/prompts/`, and `/research/`.

## Plan

1. **Author the executing prompt.** Flesh out [`/prompts/refactor-governance-from-specs/prompt.md`](../../prompts/refactor-governance-from-specs/prompt.md) per `PROMPT.md` — RISE-DX framework, RFC-2119 normativity, output lock on the linter spec.
2. **Inventory rules.** Read the three source specs:
   - [`research/agent-prompt-specs-3-systems-sdd/output/SPEC.md`](../../research/agent-prompt-specs-3-systems-sdd/output/SPEC.md) (A/B/C)
   - [`research/agentic-session-continuity-spec/output/`](../../research/agentic-session-continuity-spec/output/) (G/H/I)
   - [`research/agentic-eval-trust-improvement-spec/output/`](../../research/agentic-eval-trust-improvement-spec/output/) (J/K/L)
   For each spec, extract every MUST/SHOULD/MAY clause that can be mechanically checked.
3. **Categorize checks.** For each clause, decide enforcement layer: `frontmatter-linter`, `directory-structure-linter`, `pre-commit hook`, or `human-review-only` (out of scope).
4. **Author the frontmatter linter.** A script that walks `/tasks/`, `/prompts/`, `/research/`, validates L0+L1 keys per `TASK.md` §3, validates the appropriate L2 namespace, and rejects YAML nesting > 1.
5. **Author the directory-structure linter.** Validates: `task.md` exists in every `/tasks/<NNN>-<slug>/`; `prompt.md` and `brief.md` exist in every `/prompts/<slug>/`; the four canonical subfolders exist in every non-archived `/research/<slug>/`; readme.md presence per `FOLDERS.md`.
6. **Author the linkage validator.** For each `task.md`, every slug in `task_uses_prompts` resolves; every slug in `task_spawns_research` resolves; reciprocity between `prompt_relates_to_task` and `task_uses_prompts`; reciprocity between `research_executes_prompt` and the prompt slug.
7. **Wire the pre-commit hook.** Update `PRE_COMMIT.md` to mandate running these linters; add the actual hook script under `.githooks/` and a thin shim under `tools/`.
8. **Author templates.** `templates/task.md`, `templates/prompt.md`, `templates/research-readme.md` — pre-populated with the L1+L2 frontmatter so future agents copy-and-edit instead of authoring from memory.
9. **Continuity hooks (Spec-G/H/I).** Translate the session-continuity rules into concrete artifacts: e.g., a `/tasks/<NNN>-<slug>/notes.md` template requiring a "Resumption Checklist" if `task_status: blocked`.
10. **Eval/Trust hooks (Spec-J/K/L).** Translate evaluation/trust rules into a `tools/check-trust.sh` that audits whether closed tasks have non-empty friction logs and reciprocal linkage.
11. **Self-test.** Run all linters against the current repository; fix every diagnostic by either correcting the file or relaxing the rule with documented rationale.
12. **Close.** Update `task_status: archived`, add `friction-log.md`, append every spawned research run (if any) to `task_spawns_research`.

## Todo

- [x] 1. Author `/prompts/refactor-governance-from-specs/prompt.md` per `PROMPT.md`.
- [x] 2. Inventory mechanically-checkable clauses from Spec-A/B/C.
- [x] 3. Inventory mechanically-checkable clauses from Spec-G/H/I.
- [x] 4. Inventory mechanically-checkable clauses from Spec-J/K/L.
- [x] 5. Categorize each clause (frontmatter / structure / pre-commit / human-only).
- [x] 6. Implement `tools/lint-frontmatter.{sh,py}` — delivered as `tools/validate-frontmatter.py` (pre-existed, verified complete).
- [x] 7. Implement `tools/lint-structure.{sh,py}` — `tools/lint-structure.py` created.
- [x] 8. Implement `tools/lint-linkage.{sh,py}` — `tools/lint-linkage.py` created.
- [x] 9. Wire `.githooks/pre-commit` and update `PRE_COMMIT.md`.
- [x] 10. Add `templates/task.md`, `templates/prompt.md`, `templates/research-readme.md` — pre-existed; added `templates/notes.md`.
- [x] 11. Add continuity-hook artifacts per Spec-G/H/I — `templates/notes.md` with Resumption Checklist section.
- [x] 12. Add eval/trust audit script per Spec-J/K/L — `tools/check-trust.py` created.
- [x] 13. Run linters against the current repo and resolve all diagnostics — all 4 scripts exit 0.
- [x] 14. Write `friction-log.md`.
- [x] 15. Set `task_status: done` and update `updated:` field. (Later updated to `updated` lifecycle via Task 026).

## Links

- Executing prompt: [`/prompts/refactor-governance-from-specs/prompt.md`](../../prompts/refactor-governance-from-specs/prompt.md)
- Source spec (A/B/C): [`/research/agent-prompt-specs-3-systems-sdd/output/SPEC.md`](../../research/agent-prompt-specs-3-systems-sdd/output/SPEC.md)
- Source spec (G/H/I): [`/research/agentic-session-continuity-spec/`](../../research/agentic-session-continuity-spec/)
- Source spec (J/K/L): [`/research/agentic-eval-trust-improvement-spec/`](../../research/agentic-eval-trust-improvement-spec/)
- Frontmatter ontology backing this task: [`/research/obsidian-frontmatter-agentic-spec/output/SPEC.md`](../../research/obsidian-frontmatter-agentic-spec/output/SPEC.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md), [`RESEARCH.md`](../../RESEARCH.md), [`FOLDERS.md`](../../FOLDERS.md)
