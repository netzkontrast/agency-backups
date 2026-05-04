---
type: prompt
status: active
slug: pr-22-governance-review
summary: "Review PR #22 (governance+tooling refactor) against all active repo specs; produce a structured critique covering correctness, spec compliance, and latent risks."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: task-spec
prompt_framework: RISE-DX
prompt_target_agent: "Claude Code"
prompt_relates_to_task: ""
prompt_spawned_from_research: ""
---

# PR #22 Governance Tooling — Code Review Prompt

## Framework

**RISE-DX** — Role, Input, Steps, Expectations, with Reflection / Discipline blocks.

## R — Role

You are the **Repository Governance Auditor**. Your job is to review a pull request diff against every active governance spec in this repository and produce a structured, actionable critique. You MUST distinguish critical violations from moderate design concerns and from minor style notes.

## I — Input

- PR diff: `git show 75e494642119675eb45dc509263fb1b934fd3a2c`
- Governance specs: `AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`
- Changed files:
  - `FOLDERS.md` (new §8)
  - `research/agentic-eval-trust-improvement-spec/output/SPEC.md` (frontmatter added)
  - `research/repo-maintenance-protocol-spec/output/SPEC.md` (frontmatter added)
  - `research/repo-maintenance-protocol-spec/readme.md` (frontmatter added)
  - `skills/skills-skill-bootstrap/readme.md` (exit-code docs updated)
  - `skills/skills-skill-bootstrap/verify.sh` (ERROR exit code 2 added)
  - `tools/readme.md` (description updated)
  - `tools/validate-frontmatter.py` (classify() hardened, load_waivers() cwd-fixed)

## S — Steps

1. Read the diff and reconstruct intent.
2. For each changed file, check: (a) frontmatter correctness per AGENTS.md ontology; (b) spec compliance per the relevant root spec; (c) referential integrity (slugs that MUST resolve).
3. Check `research_executes_prompt` values against `/prompts/` for existence.
4. Check Task 001 (`tasks/001-refactor-governance-from-specs/task.md`) for whether this work should have updated task state.
5. Review shell arithmetic in `verify.sh` for correctness and readability.
6. Review FOLDERS.md §7 vs §8 for logical consistency.
7. Summarise findings by severity (Critical / Moderate / Minor).

## E — Expectations

Output: `/research/pr-22-governance-review/output/REPORT.md` — a structured review with:
- Positive observations (what was done well).
- Critical issues (spec violations that MUST be fixed).
- Moderate concerns (design issues that SHOULD be addressed).
- Minor notes (style/polish items that MAY be addressed).
- Recommended follow-up actions.

## D — Discipline

- Reference specific spec clauses (e.g., "RESEARCH.md §3", "FOLDERS.md §7") for every finding.
- RFC 2119 normativity; exactly one normative keyword per sentence.
- No speculation without evidence from the diff.
