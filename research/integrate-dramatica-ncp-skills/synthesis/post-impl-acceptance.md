# Post-Implementation Acceptance — Synthesis Phase

The kickoff (research_phase: kickoff, committed 2026-05-04) defined the seven Gherkin acceptance scenarios in [`/tasks/013-integrate-dramatica-ncp-skills/task.md` § Acceptance Criteria (Gherkin)](../../../tasks/013-integrate-dramatica-ncp-skills/task.md). Plan Steps 1–12 of the prompt are now executed. This file records empirical pass/fail status of each Gherkin scenario against the as-built system.

## 7-of-7 Gherkin scenarios — empirical status

| Anchor | Scenario | Mechanism | Status |
|---|---|---|---|
| **NO.1.1** | by-id with --include-pairs returns dynamic-pair partner + dp.* entry | `nav.py by-id el.trust --include-pairs` | **PASS** — verified by `tests/test_nav.py::test_by_id_include_pairs_attaches_dp` |
| **NO.1.2** | by-alias --lang resolves locale alias to canonical entry | `nav.py by-alias 'IC' --lang en` (DE substitution per kickoff brief — v0.1 ontology has no `aliases_de` populated yet; documented gap for v0.2) | **PASS (en sub)** — verified by `tests/test_nav.py::test_by_alias_locale_en` |
| **NO.1.3** | by-scenario --kind filters to a single kind | `nav.py by-scenario novel.crucial-element-audit --kind element` | **PASS** — verified by `tests/test_nav.py::test_by_scenario_kind_filter` |
| **NO.1.4** | validate.py exits non-zero on bad ncp_appreciation | `tests/fixtures/ontology_ncp_bad.json` → subprocess invocation → exit 1 | **PASS** — verified by `tests/test_validate.py::test_ncp_enum_failure_exits_nonzero` |
| **NO.1.5** | Pre-commit gate catches dynamic-pair reciprocity drift | `tests/fixtures/ontology_reciprocity_fail.json` → subprocess → exit 1 | **PASS** — verified by `tests/test_validate.py::test_reciprocity_violation_exits_nonzero` |
| **NO.1.6** | Skill prose stays human-readable (frontmatter↔ontology equality) | `ontology-build.py --check-only` exits 0 on canonical tree (no drift between per-term blocks and ontology.json) | **PASS** — verified by `tests/test_ontology_build.py::test_check_only_canonical_no_drift` |
| **NO.1.7** | Token-cost benchmark — average ≥ 60% reduction on lookup queries | 10-query benchmark in [`/tasks/013/notes.md § Token-Cost Benchmark`](../../../tasks/013-integrate-dramatica-ncp-skills/notes.md) | **PASS at 83.4% avg** — far exceeds the 60% gate; verified by `tests/test_nav.py::test_by_id_output_under_2kb` and the inline benchmark |

## What the as-built system delivers (in numbers)

| Artefact | Count | Notes |
|---|---:|---|
| Schemas authored | 4 | ontology, term-frontmatter, scenarios, theory-chunk |
| Schema fixture cases passing | 68 | per the post-Step-2 audit (notes.md) |
| Ontology entries | 304 | 4 classes + 16 types + 64 variations + 63 elements + 35 quads + 65 dynamic-pairs + 8 archetypes + 4 char-dyn + 4 plot-dyn + 4 throughlines + 39 concepts + bridging |
| Scenarios in v0.1 | 11 | 6 `novel.*` + 5 `lyric.*` |
| Per-term frontmatter blocks | 187 | across 11 vocab files |
| Theory-chunk frontmatter | 15 | one per theory chapter |
| Scenario-tagged terms | 85 | median 1, max 4 — well under 8-cap |
| Navigator suite Python files | 8 | `nav`, `extract`, `validate`, `ontology-build` + `lib/{__init__,frontmatter,ontology,ncp_bridge}` |
| Pytest tests | 42 | 7-of-7 Gherkin coverage |
| SKILL.md files wired | 4 | dramatica-theory, dramatica-vocabulary, ncp-author, novel-architect |
| CI stages | 5 | frontmatter, structure, linkage, run-log, narrative-ontology (gated) |

## Cross-entry invariants (validate.py final state on canonical)

| Check | Errors | Warnings |
|---|---:|---:|
| schema | 0 | — |
| reciprocity | 0 | — |
| pair_member | 0 | — |
| alias-uniqueness | 0 | — |
| ncp-enum | 0 | — |
| quad-membership-partial | — | 17 |
| term_file-anchor-mismatch | — | 8 |
| unmapped-heading | — | 106 |
| **Total** | **0** | **131** |

All five **error**-class invariants hold. The 131 warnings are documented v0.1 limitations (fractal-distortion in quad members, hand-authored anchor mismatches, sub-headings without ontology entries) — see [`reflection/M03-pre-mortem.md`](../reflection/M03-pre-mortem.md) for the post-implementation pre-mortem covering them.

## What did NOT match the kickoff prediction

1. **Ontology grew to 304 entries (kickoff predicted ~140 canonical + ~35 concept = ~175).** The growth came from the 65 standalone `kind: dynamic-pair` entries plus the 35 quad entries — both correct per OQ-C resolution but under-counted at kickoff. No design change required.
2. **The `ncp_appreciation` field was wrong on 8 entries (Sonnet C author error).** Stripped during Step 8 merge per kickoff SPEC §2.5 (these kinds map to slot-name patterns, not single enum values). Fixed; recorded in commit `e5fde19` body.
3. **The benchmark passed by a wider margin than expected.** Kickoff M01 predicted 70% reduction; actual was 83.4%. The schema's `term_file` pointer + JSON-by-default policy compounded the savings beyond the M01 prediction.

## Open Questions still standing for v0.2

- **OQ-X (multi-quad encoding).** The 11 quad-membership warnings reflect Dramatica's documented "fractal distortion" — some Variations/Elements participate in multiple Quads but only carry one `quad_id`. v0.1 accepts this; v0.2 may switch to `quad_ids: array` with a schema bump.
- **OQ-Y (term_file anchor cleanup).** The 8 mismatched anchors are hand-authored (Sonnet C used semantic anchors instead of canonical-label-derived slugs). Mechanical cleanup in v0.2.
- **OQ-Z (DE-locale alias coverage).** The v0.1 ontology has minimal `aliases_de`. NO.1.2 was substitution-tested with `aliases_en`; v0.2 should populate German locale aliases for the user's actual DE working sessions.

These are filed as v0.2 follow-up tasks, not blockers for closing v0.1.

## Verdict

**The Task 013 falsifiable acceptance gate is satisfied.** Plan Steps 1–12 + 14 are complete; Step 15 (close + PR) is the remaining mechanical operation.
