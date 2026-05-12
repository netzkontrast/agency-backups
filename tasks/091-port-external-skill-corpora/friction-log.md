---
type: note
status: active
slug: task-091-friction-log
summary: "Friction log for Task 091 ST-1 (Phase 1 corpus port). Two FL1 entries: F.B.7 diagnostic-code clash forced renumber to F.B.8/F.B.9, and TA.1.4 manifest-reciprocity AC unimplementable against current toolchain."
created: 2026-05-12
updated: 2026-05-12
---

# Task 091 — ST-1 Friction Log

**Highest Frustration Level: FL1**

## Context

ST-1 (Phase 1 corpus) execution: validator extension + 14 `skills/sc-*/` skill folders ported from SuperClaude_Framework v4.3.0 @ `22ad3f48` per [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). The Epic plan in [`references/full-plan-part-4.md` §10](./references/full-plan-part-4.md) was largely actionable; the entries below capture the two places where the plan diverged from the actual codebase shape and required real-time adaptation.

## Friction entries

### FL1.1 — `F.B.7` diagnostic-code clash

**What happened.** The §10.2 validator-extension spec reserved `F.B.7` (skill_source on bare-slug → ERROR) and `F.B.8` (malformed value → ERROR) for the new check. Inspection of [`tools/fm/validate.py`](../../tools/fm/validate.py:143) revealed that `F.B.7` is already in use as a **WARN-tier** code for the task_list completion check inside `_check_body_for_type`. Sharing the code across two unrelated check families would have been confusing for grep/triage and would conflict with the diagnostic-explanations registry (`maintenance/schemas/diagnostic-explanations.json`).

**Resolution.** Renumbered the new ERROR codes to `F.B.8` / `F.B.9`. All references — the validator emit sites in [`tools/fm/validate.py`](../../tools/fm/validate.py), the 6 tests in [`tools/tests/fm/test_validate_skill_source.py`](../../tools/tests/fm/test_validate_skill_source.py), and the ontology `skill_source` key_doc in [`maintenance/schemas/header-ontology.json`](../../maintenance/schemas/header-ontology.json) — point at `F.B.8` / `F.B.9` consistently.

**Recommendation.** ADR-0011's verbatim Gherkin (ADR.11.2) still cites `F.B.7` for the bare-slug rejection. **This was originally recommended as a T2 additive edit to the Accepted ADR — that was wrong.** Per MAINTENANCE.md §1, an `Accepted` ADR is **T4-immutable**: editing its `## Acceptance Criteria` Gherkin block — even "additively" — changes the normative record of what the ADR's acceptance test asserts and so is prohibited. The correction was caught in peer review (see [`review-st1.md`](./review-st1.md) Issue 2).

**Correct remediation path.** File a **new ADR** that amends/clarifies ADR-0011 without editing it:

- `decisions/0012-skill-source-validator-diagnostic-codes.md` (or next free slot)
- `adr_status: Accepted` after review
- `adr_supersedes: []` (amendment, not supersession — D.1–D.9 normative clauses are unchanged)
- `adr_relates_to: [ADR-0011]`
- Body: "ADR-0011 §10.2 design specified F.B.7 / F.B.8. Implementation in PR #115 used F.B.8 / F.B.9 due to F.B.7 pre-existing use as a WARN-tier code in `_check_body_for_type`. This ADR ratifies F.B.8 / F.B.9 as the authoritative code pair and supersedes the F.B.7 reference inside ADR-0011 §ADR.11.2 Gherkin."

The diagnostic-explanations registry (`maintenance/schemas/diagnostic-explanations.json`) should also gain entries for `F.B.8` / `F.B.9` when the amendment ADR lands. **Filing this as a sibling Task is out-of-scope for ST-1** but blocking for any ADR-level coherence sweep; recommended for the ST-2 reviewer to triage.

### FL1.2 — TA.1.4 manifest-reciprocity AC has no implementation backing

**What happened.** AC `TA.1.4` (verbatim from `references/full-plan-part-4.md` §10.5) reads:

```
Given the 14 skill folders are committed
When the manifest is regenerated
Then the manifest entry for sc-system-architect MUST list referenced_by: [sc-implement]
And the manifest entry for sc-quality-engineer MUST list referenced_by: [sc-test, sc-improve]
```

Step (8) of the §10.5 Task A plan calls for `bash skills/skills-skill-bootstrap/sync.sh --emit-manifest` (or its equivalent — "verify exact invocation against `sync.sh` source"). Inspection found:

1. No `.skills-manifest.json` (or equivalent) artifact exists anywhere in the repo today.
2. [`skills/skills-skill-bootstrap/sync.sh`](../../skills/skills-skill-bootstrap/sync.sh) supports only tree-sync + bundle materialisation; there is **no** `--emit-manifest` flag.
3. The closest thing in the codebase is [`tools/fm/graph.py`](../../tools/fm/graph.py), which emits a slug/edge graph but does **not** crawl `skill_references_skills` (`fm-graph --format=json` over the repo today returns `skill_references_skills` edges: 0; the field is not in its closed traversal set).

**Resolution.** Forward references are correctly declared in YAML on every imported SKILL.md:

```
skills/sc-implement/SKILL.md:
  skill_references_skills: [sc-system-architect, sc-backend-architect,
                            sc-frontend-architect, sc-security-engineer,
                            sc-quality-engineer]
skills/sc-test/SKILL.md:
  skill_references_skills: [sc-quality-engineer]
skills/sc-improve/SKILL.md:
  skill_references_skills: [sc-quality-engineer, sc-refactoring-expert,
                            sc-performance-engineer]
```

Reciprocity is therefore **derivable** ad-hoc:

```bash
$ grep -l "sc-system-architect" skills/sc-*/SKILL.md | grep -v sc-system-architect
skills/sc-implement/SKILL.md

$ grep -l "sc-quality-engineer" skills/sc-*/SKILL.md | grep -v sc-quality-engineer
skills/sc-improve/SKILL.md
skills/sc-test/SKILL.md
```

The TA.1.4 invariant **holds** in the YAML; what is missing is the *materialised* manifest file the AC asserts against.

**Recommendation.** The manifest emitter is a real gap, but adding it is materially out-of-scope for ST-1 (it would be a separate ADR-level decision about manifest format, location, and update cadence — closer to the deferred `tasks/010-skills-frontmatter-index-suite/` work). Two viable closure paths for the AC:

1. **Relax TA.1.4** in a sibling Task to assert "forward refs declared" rather than "manifest entry shows reciprocity" until the manifest emitter ships. The forward refs are the source of truth; reciprocity is a computed view.
2. **Implement a minimal manifest emitter** under Phase 2 of the Epic plan. This should be a new ADR (mirroring ADR-0007's pattern for `skill_bundles_tools`) that ratifies the manifest schema, location, and the lint-linkage edge-traversal extension.

ST-1 ships the corpus + the validator extension; the manifest gap is logged here, not silently swept.

## What worked smoothly

- The §10.3 per-skill design table was directly executable — frontmatter values, tier classification, bundle declarations, references/ layout all dropped in without re-design.
- The `tools/fm/edit.py`-free approach (writing SKILL.md files via a generator script with the existing Anthropic `name`+`description` skill shape) avoided fighting the validator and kept the body-cap honest.
- ADR-0011 D.8 (Tavily → OPTIONAL relocation) was textually unambiguous; the sc-research adaptation was 4 lines of Edit, not a body rewrite.

## What didn't fire

The plan listed four ST-1 falsification clauses (§10.7 verification recipe). Items 1–4 (`./install.sh`, governance, ADR validation, validator regression) and item 6 (body cap) all passed cleanly. Item 5 (`lint-linkage.py` reciprocity over `skills/sc-*/`) is logged under FL1.2 above. Item 9 (smoke test of the Skill tool in Claude Code) is out of band — it cannot be exercised inside this session because the deferred Skill tool is gated on session-level skill registration, which is a follow-up after ST-2 hookup.

## Final state

- ✅ ST-1 validator extension landed (`F.B.8` / `F.B.9` ERROR codes + 6 new tests, all green).
- ✅ 14 sc-* skill folders landed (`skill_source: "superclaude@v4.3.0"`, body-cap clean, verbatim upstream archived at `references/upstream-sc-<slug>.md`).
- ✅ 2 MODE references bundled (Orchestration → sc-implement; DeepResearch → sc-research).
- ✅ `skills/readme.md` updated with the "Imported from SuperClaude (v4.3.0)" section.
- ✅ `tools/check-governance.sh` exits 0; JSON-Schema mirrors regenerated.
- ⚠️ TA.1.4 manifest-reciprocity AC documented above as gap; forward refs are correctly declared.

ST-2 (AGENTS.md + RESEARCH.md hookup) is sequenced per the Epic plan and may start once ST-1 merges to `main`.
