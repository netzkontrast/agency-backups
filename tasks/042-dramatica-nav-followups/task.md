---
type: task
status: active
slug: dramatica-nav-followups
summary: "Three Task-030 follow-up items surfaced during /sc:improve --introspection: (1) wire precompile.py validate into check-governance.sh; (2) audit term.py + aliases.py for over-engineered surface relative to subtask briefs; (3) decide on the 103 unmapped-heading 'Bucket C structural prose' handling — suppress at validator, formalise as kind: prose-section, or accept as permanent noise."
created: 2026-05-06
updated: 2026-05-06
task_id: "042"
task_status: open
task_owner: "claude"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_supersedes: []
task_superseded_by: []
task_blocked_by: []
task_affects_paths:
  - tools/dramatica-nav/
  - tools/check-governance.sh
  - maintenance/schemas/narrative-ontology/
  - tasks/042-dramatica-nav-followups/
---

# Task 042 — Dramatica-Nav Follow-Ups (Post-Task-030)

## Goal

Three items surfaced by Task 030's `/sc:improve --introspection` retrospective. Each is independently shippable; the task is `done` when all three resolve (resolve = "shipped" OR "explicitly closed without code change, with rationale recorded").

1. **Wire `precompile.py validate` into the governance gate.** Today `cleanup.py --check` runs in `tools/check-governance.sh`; `precompile.py` does not. If the ontology drifts (new scenario tags, prose changes), the 11 precompiled JSONs go stale silently. Add a stanza analogous to ST-6's wire-in. **Tradeoff:** adds a CI failure surface; staleness is recoverable by re-running `emit-all`. Decision: wire it in OR explicitly document why we don't (e.g., precompiled is denormalised; staleness is not a correctness bug).
2. **Audit `term.py` (944 LOC) + `aliases.py` (832 LOC) for over-engineered surface.** Both shipped roughly 3-4× the LOC their subtask briefs estimated (term.py 250 LOC, aliases.py 200 LOC). Skim suggests aliases.py ships a CRUD `add/remove/list` surface that the brief did not explicitly demand. Per AGENTS.md "don't add features beyond what the task requires", the extra surface deserves either a justification (concrete caller / smoke-test pulling on it) or removal. Refactor outcome: either trim, or write a one-line comment per extra subcommand naming its caller.
3. **Decide on Bucket C structural-prose handling.** `validate.py` reports `unmapped-heading: 103`. Of those, ~42 are Bucket C (workflow-chapter headings inside `essential-questions.md`, `encoding-patterns.md`, etc. — legitimately not ontology entries; ST-3 partition table at `tasks/030-cleanup-dramatica-skills-corpus/notes.md §5`). They are warning noise. Three options:
   - **Option A — silence at validator.** Add a config file or per-section `<!-- nav-ontology-skip -->` marker that the validator honours.
   - **Option B — formalise as `kind: prose-section`** in the ontology schema. Schema bump; needs Task 029 ADR sign-off.
   - **Option C — accept as permanent noise** and document the validator output as "ignore Bucket C lines" in the navigator readme.

## Background

Task 030 closed all four §Goal gates but its `/sc:improve --introspection` retrospective surfaced these three items as judgment calls we declined to bundle into 030's closure. Items 1 and 2 are mechanical; item 3 has a schema-bump option that may require Task 029 absorption.

## Plan

Three independent items, no inter-item ordering:

1. **Item-1 (wire-in).** Edit `tools/check-governance.sh` to add a `precompile.py validate` stanza after the existing `cleanup.py --check` stanza, gated on the same `ontology.json` predicate. Add a row to `PRE_COMMIT.md §7`. ~15 LOC change, no test additions needed (precompile.py already has its own tests).
2. **Item-2 (audit).** Read `term.py` and `aliases.py` end to end. For each subcommand, identify the caller (test, brief reference, or absent). Trim subcommands without callers OR document them with a one-line `# why kept` comment. Re-run pytest after trim.
3. **Item-3 (decide).** Two-step: (a) read the partition table to confirm the 42 Bucket C count and the structure; (b) pick A/B/C. If B (schema bump), file as Task-029-ADR input and close item-3 with rationale "deferred to ADR pipeline".

## Todo

- [ ] 1. Item-1: edit `tools/check-governance.sh` (stanza + PRE_COMMIT.md row) — OR document the no-wire-in decision.
- [ ] 2. Item-2: audit `term.py` subcommands; for each, justify or trim. Re-run `pytest tools/dramatica-nav/tests/`.
- [ ] 3. Item-2: same audit on `aliases.py`. Re-run pytest.
- [ ] 4. Item-3a: confirm Bucket C count and structure from `tasks/030-.../notes.md §5`.
- [ ] 5. Item-3b: pick option A/B/C; document the choice + rationale in this task's `notes.md`.
- [ ] 6. If A: implement validator carve-out for Bucket C; verify `validate.py` unmapped-heading drops accordingly.
- [ ] 7. If B: file ADR input against Task 029; close item-3 in this task with "deferred to ADR pipeline" rationale.
- [ ] 8. If C: add a one-paragraph "noise floor" section to `tools/dramatica-nav/readme.md` (or wherever the navigator's user-facing docs live).
- [ ] 9. Run end-to-end gates (`tools/check-governance.sh`, `pytest tools/dramatica-nav/tests/`).
- [ ] 10. Set `task_status: done`. Push.

## Acceptance Criteria

```gherkin
Feature: Task 030 follow-up items resolve

  Scenario: precompile.py validate wired into governance
    When tools/check-governance.sh runs after a precompiled JSON drifts
    Then it MUST exit 1 with a precompile-stale diagnostic
    Or the decision to NOT wire is documented in PRE_COMMIT.md or a /no-wire-in note

  Scenario: term.py + aliases.py surface justified
    Given each subcommand in term.py and aliases.py
    When the audit completes
    Then every subcommand has either a caller (test/brief/CI) or a one-line # why-kept comment
    And the LOC delta vs. brief estimate is justified or trimmed

  Scenario: Bucket C handling decided
    Given the 103 unmapped-heading warnings
    When the decision lands
    Then the chosen option (A/B/C) is documented in this task's notes.md
    And if A, the validator no longer surfaces Bucket C entries
    And if B, an ADR has been filed against Task 029
    And if C, navigator readme documents the noise floor
```

## Anti-Patterns to Avoid

- **MUST NOT** bump the ontology schema in this task without an ADR. Item 3 Option B routes through Task 029, not directly.
- **MUST NOT** trim public CLI surfaces from `term.py` or `aliases.py` without verifying no smoke test or downstream tool depends on them.
- **MUST NOT** treat "the brief said 250 LOC" as a hard contract — over-shipping is sometimes correct. The audit is a justification check, not a forced trim.

## Links

- Predecessor (closed): [`/tasks/030-cleanup-dramatica-skills-corpus/`](../030-cleanup-dramatica-skills-corpus/) — ships the four scripts under audit + the precompiled artefacts.
- Process input (open): [`/tasks/029-adr-assumption-audit/`](../029-adr-assumption-audit/) — receives item 3 Option B if chosen, plus the FE-EX-1..FE-EX-5 process observations Task 030's friction-log catalogues.
- Affected tooling: `tools/dramatica-nav/{term,aliases,precompile}.py`, `tools/check-governance.sh`, `PRE_COMMIT.md §7`, `maintenance/schemas/narrative-ontology/`.
