---
type: task
status: active
slug: dramatica-nav-followups
summary: "Ten Task-030 follow-up items: (1) precompile validate wire-in; (2) term.py + aliases.py over-engineering audit; (3) Bucket C structural-prose decision; (4) Bucket D (41 disputed entries) triage; (5) AGENTS.md NO.5 amendment for precompiled/*.json; (6) ST-7 alias conflict resolution (27 conflicts); (7) six ontology entries without source YAML blocks; (8) derived-kind scenario-tag schema decision (dynamic-pair + quad); (9) `## Mental Sex` body content correction; (10) hardcoded test-count baseline drift."
created: 2026-05-06
updated: 2026-05-06
task_id: "042"
task_status: open
task_owner: "claude"
task_priority: P2
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
  - skills/dramatica-vocabulary/references/
  - AGENTS.md
  - tasks/042-dramatica-nav-followups/
---

# Task 042 — Dramatica-Nav Follow-Ups (Post-Task-030)

## Goal

Close ten items that surfaced during Task 030's execution but were deliberately scoped out of its §Goal acceptance gates. The items split into three buckets — **mechanical** (do it), **decision** (pick a route), **schema-touching** (file ADR or amend with care). The task is `done` when each item is either shipped OR explicitly closed with a recorded rationale (deferred / out-of-scope / superseded). No item is allowed to silently age out.

§Goal items 1–4 of Task 030 remain green during and after this task; nothing here is allowed to regress them.

## Background

Task 030 closed all four §Goal gates but its `/sc:improve --introspection` retrospective and the PR #68 independent review surfaced ten items beyond the gates. Two trivial dead-code removals (`_strip_artifacts.py`, `st7-partial/`) were folded into Task 030's closure. The other ten warrant their own task surface so the trade-offs are explicit and not buried in commit footnotes.

Sources are referenced inline per item.

## Items

Each item carries: **trigger** (where it surfaced), **scope** (what changes), **decision points** (when a judgment call is required), **acceptance** (what `done` means).

### Item 1 — Wire `precompile.py validate` into `check-governance.sh`

- **Trigger.** PR #68 review OQ-2; `/sc:improve --introspection` finding #4.
- **Scope.** Add a stanza after the existing `cleanup.py --check` block in `tools/check-governance.sh`, gated on `ontology.json` existing. Add a row to `PRE_COMMIT.md §7`. ~15 LOC.
- **Decision.** Wire it in OR document the no-wire decision (e.g., precompiled is denormalised; staleness is not a correctness bug, only a freshness one).
- **Acceptance.** `tools/check-governance.sh` exits 1 when `precompile.py validate` finds a stale JSON. OR a one-paragraph rationale lives in `PRE_COMMIT.md §7` explaining the absence.

### Item 2 — Audit `term.py` (944 LOC) and `aliases.py` (832 LOC) for over-engineered surface

- **Trigger.** PR #68 review Q-1; `/sc:improve --introspection` finding #5.
- **Scope.** Both modules shipped roughly 3–4× their subtask brief estimates (term.py 250, aliases.py 200). Skim suggests aliases.py ships an `add` / `remove` / `list` CRUD surface the brief did not explicitly require.
- **Decision.** Per AGENTS.md "don't add features beyond what the task requires", every subcommand needs a justification — concrete caller / smoke-test / brief reference — OR a one-line `# why kept` comment, OR removal.
- **Acceptance.** For every public subcommand in `term.py` and `aliases.py`: either a caller exists, a comment names why it's kept, or it's deleted. Tests still pass.

### Item 3 — Bucket C structural-prose handling (~42 of the 103 unmapped headings)

- **Trigger.** ST-3 partition table at `tasks/030-cleanup-dramatica-skills-corpus/notes.md §5`. Reviewer Q-1 echoes.
- **Scope.** 42 workflow-chapter sub-headings (`## Why Quads matter for Encoding`, `## Phase 1 — Throughline Class assignments`, etc.) inside extension files. Legitimately not ontology entries; surface as warning noise.
- **Decision.** Three options — see [§Decision Matrix](#decision-matrix-bucket-c) below.
- **Acceptance.** Pick one option; document choice + rationale in this task's `notes.md`. If A: implement validator carve-out; if B: file ADR input against the appropriate ADR pipeline; if C: add "noise floor" paragraph to navigator readme.

### Item 4 — Bucket D triage (41 disputed entries needing future ratification)

- **Trigger.** ST-3 commit `9dc6b92` body + partition table; PR #68 review OQ-1.
- **Scope.** 41 unmapped headings ST-3 named "disputed" — three semantic clusters:
  1. enum-value-of-character-dynamic / -plot-dynamic (~16 rows; needs `kind: enum-value` schema decision).
  2. candidate canonical Dramatica concepts not bootstrapped in Task 015 (~15 rows; mechanical mint pass candidates).
  3. meta-terms naming the ontology kinds themselves (~10 rows; meta-self-reference ratification).
- **Decision.** Per cluster: mint, alias, demote to Bucket C, or file as ADR input. Reviewer's specific ask: "Triage-Timeline und Validator-Silence" — i.e., when does each cluster get closed, and how does the validator stop surfacing them in the meantime?
- **Acceptance.** Triage table in this task's `notes.md` mapping each of the 41 to a disposition. Validator-silence: either resolved (entries have ontology IDs) or carried over to Item 3's Bucket C carve-out if A is chosen.

### Item 5 — Amend `AGENTS.md §NO.5` to cover `precompiled/*.json`

- **Trigger.** Task 030 `notes.md §FE-10`; PR #68 review P-3.
- **Scope.** NO.5 currently forbids loading `ontology.json` in non-narrative work but says nothing about the new `maintenance/schemas/narrative-ontology/precompiled/*.json` artefact surface. A literal-rule reader is not blocked from loading the precompiled JSONs in inappropriate contexts.
- **Decision.** Two-line amendment vs. routing through an ADR. Architectural significance is low (the rule's intent is obvious; the amendment is mechanical) but AGENTS.md is a governing spec, so a reviewer may prefer the ADR route.
- **Acceptance.** Either AGENTS.md §NO.5 explicitly names `precompiled/` and the load-trigger rule extends with the same predicate, OR an ADR-input file is created naming this as a pending amendment.

### Item 6 — Resolve ST-7's 27 alias conflicts

- **Trigger.** ST-7 commit body + `tasks/030-cleanup-dramatica-skills-corpus/notes.md §8`. 21 blocking + 6 partial-resolution conflicts; conflict-free aliases were loaded; conflicts were left for follow-up.
- **Scope.** Each conflict is an alias whose canonical-label appears on multiple ontology IDs. Resolution is per-conflict: pick the disambiguating ID, OR fold into a `kind: concept` entry, OR demote the alias.
- **Decision.** Per-row; no schema bump expected. The `Problem` non-unique-canonical-label case (ST-7 FE-4) is the canonical example.
- **Acceptance.** `notes.md §8` table updated with a disposition column. `tools/dramatica-nav/aliases.py conflict-report` exits 0 OR exits 1 with a strictly smaller conflict count and the residual conflicts are filed against a future task.

### Item 7 — Six ontology entries lack source YAML blocks

- **Trigger.** ST-8 friction event FE-ST8-1.
- **Scope.** `class.mind`, `throughline.main`, `throughline.objective`, `var.work`, `concept.concern`, `concept.story-limit` — all reachable via `nav.py by-id` (they have ontology table entries) but unreachable via `term.py edit` (no source block to mutate). Pre-existing data gap from Task 015.
- **Decision.** Mint source blocks (preferred — restores tooling parity) OR document them as "ontology-only entries" with a runtime probe in `term.py` that emits an explicit error rather than silently failing.
- **Acceptance.** Either six new `<!-- nav-ontology -->` blocks land in the appropriate reference files (and `term.py edit` round-trips them), OR `term.py edit` emits a named error class `OntologyOnlyEntry` with the six IDs documented in this task's notes.

### Item 8 — Derived-kind scenario-tag schema decision

- **Trigger.** ST-8 friction event FE-ST8-3 (deviation explicitly logged).
- **Scope.** `dynamic-pair` (65 entries) and `quad` (35 entries) are derived ontology entries — they exist only in `ontology.json`, never in source YAML blocks. ST-8 patched 50 dynamic-pair entries' `scenarios` array directly to hit the ≥250 target. The deviation works but motivates a schema-level decision: either project source blocks for derived kinds (so `term.py edit` can reach them), OR formally recognise the derived-kind scenario-tag surface as ontology.json-owned (so the direct patch becomes the canonical workflow).
- **Decision.** Schema-touching. Best routed through an ADR.
- **Acceptance.** Either project source blocks (Item 7's pattern at 100-entry scale) OR file an ADR input + amend the term.py contract to surface "derived kind, edit ontology.json directly" as a documented exit.

### Item 9 — `## Mental Sex` body content is misattributed

- **Trigger.** ST-2 truncation catalog; flagged for ST-3 but never addressed.
- **Scope.** `skills/dramatica-vocabulary/references/character-dynamics.md` lines 302–350: the `## Mental Sex` body content actually describes Methodology/Mind Class, not Mental Sex / Problem-solving Style. Pre-existing PDF-extraction artefact.
- **Decision.** Either restore the correct body (≤1 line of source prose per Anti-Patterns), OR delete the body and mark with `<!-- truncated; consult original source -->`, OR keep with a clear truncation comment.
- **Acceptance.** `## Mental Sex` body content matches its heading semantically OR a truncation comment makes the mismatch explicit.

### Item 10 — Hardcoded test-count baseline drift

- **Trigger.** FE-EX-3 in Task 030 friction-log. Confirmed pattern: `test_walk_vocab_blocks_count` asserted `== 187`, broke after Phase A added 7 blocks, was updated to `== 194`. The next task that adds or removes a block will break it again.
- **Scope.** Replace the magic-number assertion with a data-driven invariant — e.g., "block count equals number of canonical entries in ontology.json with a source-block reference" — so the test self-updates with the corpus.
- **Decision.** Mechanical; no judgment.
- **Acceptance.** `test_walk_vocab_blocks_count` no longer carries a hardcoded count. Adding a new term doesn't break the test.

## Decision Matrix (Bucket C, Item 3)

| Option | Effort | Pros | Cons | Schema bump? |
|---|---|---|---|---|
| **A — silence at validator.** Per-section `<!-- nav-ontology-skip -->` marker honored by `validate.py`. | S | Mechanical; no schema change; reviewer sees signal-rich output. | New repo convention; needs documentation. | No. |
| **B — formalise as `kind: prose-section`.** Bucket C entries get ontology IDs of a new kind. | M | Audit-graph completeness; prose sections become first-class. | Schema bump; new kind in enum; downstream tooling impact. | Yes. |
| **C — accept as permanent noise.** Document the unmapped-heading floor as expected. | XS | Zero code change. | Validator output stays noisy; future readers wonder why 42 warnings persist. | No. |

## Plan

Phasing — mechanical first to compress the surface area, then decisions, then schema-touching:

```
Phase 1 (mechanical, parallel-safe): Items 1, 2, 9, 10.
Phase 2 (decisions, sequential per item): Items 3, 4, 6, 7.
Phase 3 (schema-touching, may file ADR inputs instead of shipping): Items 5, 8.
```

Items in Phase 1 ship in one focused commit each. Items in Phase 2 each produce a single decision-record commit (which may itself ship code, file an ADR input, or close the item with rationale). Items in Phase 3 either ship or file ADR inputs; in either case, this task closes them.

## Todo

- [ ] 1. Item 1: wire `precompile.py validate` into `tools/check-governance.sh` OR record no-wire rationale in `PRE_COMMIT.md §7`.
- [ ] 2. Item 2: audit `term.py` subcommands; per command, justify (caller / smoke-test / brief reference) or trim. Re-run `pytest tools/dramatica-nav/tests/`.
- [ ] 3. Item 2: same audit on `aliases.py`. Re-run pytest.
- [ ] 4. Item 9: correct `## Mental Sex` body or mark with truncation comment.
- [ ] 5. Item 10: replace `test_walk_vocab_blocks_count` magic number with a data-driven invariant.
- [ ] 6. Item 3a: read ST-3 partition table; confirm Bucket C count and structure.
- [ ] 7. Item 3b: pick A/B/C; document choice + rationale in `notes.md`. Implement consequences.
- [ ] 8. Item 4: triage 41 Bucket D entries; per-entry disposition (mint/alias/demote/ADR) recorded in `notes.md`.
- [ ] 9. Item 6: walk 27 ST-7 alias conflicts; resolve, fold into Bucket B, or file residual to a future task. Update `notes.md §8`.
- [ ] 10. Item 7: mint source blocks for the six ontology-only entries OR add `OntologyOnlyEntry` error class to `term.py edit`.
- [ ] 11. Item 5: amend `AGENTS.md §NO.5` to cover `precompiled/*.json` OR file ADR input.
- [ ] 12. Item 8: derived-kind scenario-tag schema decision — project source blocks OR file ADR input + document direct-edit exit.
- [ ] 13. Run end-to-end gates: `tools/check-governance.sh`, `pytest tools/dramatica-nav/tests/`, `tools/dramatica-nav/cleanup.py --check`. All exit 0.
- [ ] 14. Set `task_status: done`. Push.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: Task 030 follow-up items resolve

  Background:
    Given Task 030's four §Goal gates remain green
    And tools/check-governance.sh exits 0
    And pytest tools/dramatica-nav/tests/ passes

  Scenario: Item 1 — precompile validate wire-in or documented absence
    When tools/check-governance.sh runs
    Then either it invokes precompile.py validate
    Or PRE_COMMIT.md §7 carries a recorded no-wire rationale

  Scenario: Item 2 — term.py + aliases.py surface justified
    Given each public subcommand in term.py and aliases.py
    When the audit completes
    Then every subcommand has a caller, a justification comment, or has been removed
    And LOC delta vs. brief estimate is recorded with rationale

  Scenario: Item 3 — Bucket C decision recorded
    When the decision lands
    Then the chosen option (A/B/C) is documented in notes.md
    And the validator's unmapped-heading count reflects the chosen treatment

  Scenario: Item 4 — Bucket D triaged
    Given the 41 disputed entries from ST-3
    When the triage completes
    Then each entry has a disposition (mint/alias/demote/ADR)
    And the validator-silence policy for the residual is recorded

  Scenario: Item 5 — AGENTS.md §NO.5 covers precompiled
    When the amendment lands or is filed as ADR input
    Then a literal-rule reader cannot reasonably miss the precompiled load-trigger

  Scenario: Item 6 — Alias conflicts resolved or filed
    When this task closes
    Then notes.md §8 carries a disposition column for all 27 ST-7 conflicts
    And aliases.py conflict-report exits 0 OR with a strictly smaller and filed-residual count

  Scenario: Item 7 — Source-blockless entries reachable or explicit
    Given the six ontology-only entries from FE-ST8-1
    When this task closes
    Then either each has a source block AND term.py edit round-trips it
    Or term.py edit emits an OntologyOnlyEntry error naming all six

  Scenario: Item 8 — Derived-kind scenario-tag decision lands
    When the decision is made
    Then either dynamic-pair + quad entries have source blocks
    Or term.py contract documents the direct-edit exit AND an ADR input is filed

  Scenario: Item 9 — Mental Sex body content corrected
    When the fix lands
    Then the body matches the heading semantically OR carries an explicit truncation comment

  Scenario: Item 10 — Test count drift fixed
    When test_walk_vocab_blocks_count runs after a new ontology entry lands
    Then the test passes without manual update
```

## Anti-Patterns to Avoid

- **MUST NOT** bump the ontology schema in this task without filing an ADR input. Items 3 (Option B) and 8 route through ADRs; if the ADR pipeline isn't available, the item closes with "schema bump deferred" rationale, not silently shipped.
- **MUST NOT** trim public CLI surfaces in Item 2 without verifying no smoke test, downstream tool, or documentation references them. Removal needs a `git grep <subcommand>` audit per subcommand.
- **MUST NOT** treat "the brief said 250 LOC" as a hard contract — over-shipping is sometimes correct. Item 2's audit is a justification check, not a forced trim.
- **MUST NOT** silently widen the AGENTS.md §NO.5 rule (Item 5) to cover artefact surfaces beyond `precompiled/`. Each new surface needs its own load-trigger consideration.
- **MUST NOT** mint Bucket B or Bucket D entries in Item 4 with quoted source prose >1 line (preserves Task 015's copyright-respect rule).
- **SHOULD NOT** bundle Phase 1 mechanical items into a single commit — each lands separately so a bisect-style revert is per-item.

## Links

- Predecessor (closed): [`/tasks/030-cleanup-dramatica-skills-corpus/`](../030-cleanup-dramatica-skills-corpus/) — ships the four scripts under audit, the precompiled artefacts, and the ST-3 partition table.
- PR feedback: [PR #68 review comment](https://github.com/netzkontrast/agency/pull/68#issuecomment-4389689106) — sources Items 1, 2, 5, 4, plus the P-2 todo-marking fix already landed.
- Sibling-process inputs (correction): Task 029 is `done` and did NOT absorb Task 030's friction patterns. The actual routing (per Task 030's friction-log §Pattern routing post-mortem):
  - [`/tasks/040-superclaude-spec-evaluation/`](../040-superclaude-spec-evaluation/) — FE-2, FE-6, FE-EX-1, FE-EX-2, FE-EX-4, FE-EX-5 (the `/sc:*` and parallel-dispatch surface).
  - [`/tasks/033-task-spec-integration/`](../033-task-spec-integration/) — FE-1, FE-5, FE-8, FE-9 (subtask format + task↔prompt edges).
  - [`/tasks/032-agents-spec-integration/`](../032-agents-spec-integration/) — FE-10 (AGENTS.md §NO.5 preview lifecycle).
  - [`/tasks/034-prompt-spec-integration/`](../034-prompt-spec-integration/) — FE-4 (renderer YAML).
  - [`/tasks/038-frustrated-spec-integration/`](../038-frustrated-spec-integration/) — FE-7 (verbose-by-design).
  - [`/tasks/039-maintenance-spec-integration/`](../039-maintenance-spec-integration/) — FE-3 (frontmatter↔readme drift).
  - This task does NOT re-surface the patterns; it consumes the work the spec-integration chain produces.
- Affected tooling: `tools/dramatica-nav/{term,aliases,precompile,validate}.py`, `tools/dramatica-nav/tests/`, `tools/check-governance.sh`, `PRE_COMMIT.md §7`, `AGENTS.md §NO.5`, `maintenance/schemas/narrative-ontology/`, `skills/dramatica-vocabulary/references/character-dynamics.md`.
