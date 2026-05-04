---
type: research
status: active
slug: integrate-dramatica-ncp-skills
summary: "Kickoff specification — consolidated findings from the corpus inventory, cross-skill ID audit, and scenario-tag survey, with concrete recommendations addressed at Task 013 plan steps 2 through 11."
created: 2026-05-04
updated: 2026-05-04
research_phase: kickoff
research_executes_prompt: integrate-dramatica-ncp-skills
research_friction_level: FL0
---

# Kickoff Specification — Integrate Dramatica Skills With NCP and Novel-Architect

## §0. Status & Provenance

| Field | Value |
|---|---|
| **Maturity** | Draft — kickoff phase |
| **Last review date** | 2026-05-04 |
| **Primary sources** | `skills/dramatica-theory/`, `skills/dramatica-vocabulary/`, `skills/ncp-author/`, `skills/novel-architect/`, `skills/research-prompt-optimizer/`, `skills/spec-skill/`; the eleven persona scenarios in [`/tasks/013-integrate-dramatica-ncp-skills/task.md`](../../../tasks/013-integrate-dramatica-ncp-skills/task.md). |
| **Methods applied** | Corpus walk via Explore subagent; M01 Falsification; M07 Contradiction Log. |
| **Out of scope** | Schema authoring, ontology bootstrap, navigator implementation — those are downstream Task 013 plan steps and produce their own artefacts. |

## §1. Normative Conventions

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

The findings in §3 are normative for downstream Task 013 work. The discussion in §2 is rationale; recommendations in §4 are the operative output.

## §2. Findings

### §2.1 Corpus is large but bounded

22 vocabulary files / 310 distinct term entries / 75 reciprocal dynamic pairs / 512 synonym aliases. 15 theory chapters totalling ~1010 KB. The full inventory is in [`/research/integrate-dramatica-ncp-skills/synthesis/inventory.md`](../synthesis/inventory.md).

The bootstrap target for `ontology.json` is approximately **140 canonical entries** (4 Classes + 16 Types + 64 Variations + 64 Elements + 8 Archetypes + 4 character-dynamics + 4 plot-dynamics + miscellaneous), plus approximately **35 concept-class meta-entries** (Crucial Element, Symptom, Focus, etc.).

### §2.2 Three concrete cross-skill ID contradictions

(Detail in [`/research/integrate-dramatica-ncp-skills/synthesis/id-audit.md`](../synthesis/id-audit.md). All three are *naming*, not theory.)

1. **Fourth throughline.** `Subjective Story (SS)` (theory) ≠ `Relationship (RS)` (vocabulary) ≠ `Relationship Story` (NCP). Resolution: canonical = `Relationship Story` (NCP enum compliance); the rest are aliases.
2. **Third throughline.** `Impact Character (IC)` (theory + vocab) ≠ `Influence Character` (NCP). Resolution: canonical = `Influence Character`; `Impact Character` and `IC` are aliases.
3. **MC dynamic for problem-solving.** `Mental Sex` (theory + vocab) ≠ `Problem-solving Style` (NCP). Resolution: canonical = `Problem-solving Style`; `Mental Sex` is an alias; `Male/Female problem-solving` is a deprecated alias.

In all three cases NCP's label is selected as canonical because it is the only label with a hard machine-enforcement contract (schema enum); the other labels MAY remain in prose.

### §2.3 Element / Type "overshoot" is meta-entries, not theory drift

The vocabulary's `elements.md` carries 70–71 entries against canon's 64; `types.md` carries 41 against canon's 16; `archetypes.md` carries 9 against canon's 8. The extras are **concept-class meta-entries** (Crucial Element, Symptom, Focus, Direction; Concern, Issue, Problem, Solution; the meta-entry "Archetype" itself).

Schema MUST distinguish:

- `kind: element` (canonical 64)
- `kind: type` (canonical 16)
- `kind: archetype` (canonical 8)
- `kind: concept` (the meta-entries)

Silent merging would corrupt downstream Dynamic-Pair logic — a Crucial Element does not have a dynamic pair; it *is* a slot pointing at one of the 64 Elements.

### §2.4 Source-vs-Extension provenance is already documented

Six of 22 vocabulary files are explicitly marked as Extension (`dramatica-fundamentals`, `storyform-mechanics`, `element-quads`, `encoding-patterns`, `essential-questions`, `_synonym-lookup`). The vocabulary SKILL.md already prescribes the precedence rule. The schema's `provenance: source-original | extension-derived` enum maps cleanly onto this.

### §2.5 NCP enum closure is partial, not clean

Running the dramatica term universe against the pinned NCP schema:

| Kind | NCP coverage | Schema treatment |
|---|---|---|
| Throughlines (4) | clean — `<Throughline>` enum | `ncp_appreciation` present |
| Storypoint slots (24×4 + 84×4) | clean — `<Throughline> <Slot>` enum | `ncp_appreciation` present |
| Elements (64) | partial — appear only inside storypoint slots | `ncp_appreciation_partial: true` |
| Variations (64) | partial — same | `ncp_appreciation_partial: true` |
| Types (16) | partial — same | `ncp_appreciation_partial: true` |
| Archetypes (8) | absent — NCP uses `narrative_function` enum | `ncp_appreciation` MUST be omitted |
| Quads (16), Dynamic-pairs (75) | absent | `ncp_appreciation` MUST be omitted |

This finding **refines** `task.md § Target Architecture`: the proposed `ncp_appreciation_partial: false` default is wrong. The realistic split is approximately **60% partial / 30% omitted / 10% clean**. The schema MUST allow `ncp_appreciation` to be **absent** (not just flagged `partial: true`).

### §2.6 Scenario taxonomy is tractable

The eleven persona scenarios from `task.md` map to bounded subsets of the term universe. First-pass survey: **median ≈ 2.4 scenarios per tagged term**, **hottest term ≈ 4–5 scenarios** — well under the schema's per-term `scenarios: ≤8` cap. Total tag emissions ≈ 126 across ≈ 80 terms.

The kickoff Falsification check (M01) confirms: per-term frontmatter is structurally sufficient for the lookup workload defined by the eleven scenarios. No separate `scenario-index.json` is required for the v0.1 design.

A pre-commitment is recorded: if Task 013 plan step 6 produces a real per-term tag median > 5, plan step 8 expands to add `scenario-index.py`. The contingency is small (≈80 lines) and does not require schema changes.

### §2.7 Multilingual lookup gap

The synonym lookup is EN-only (512 rows) but the vocabulary skill triggers explicitly on German queries. The schema MUST allow `aliases.<locale>` (at minimum `aliases.en` and `aliases.de`) so DE→canonical lookup is symmetric to EN.

## §3. Normative Recommendations for Task 013

### §3.1 Plan step 2 — Schema authoring

- **R.3.1.1.** `term-frontmatter.schema.json` MUST include `kind: concept` alongside `element / type / archetype / variation / class / character-dynamic / plot-dynamic / dynamic-pair / quad / signpost-slot`.
- **R.3.1.2.** `term-frontmatter.schema.json` MUST allow `ncp_appreciation` to be **absent**. The `ncp_appreciation_partial` field MUST be present only when `ncp_appreciation` is present.
- **R.3.1.3.** `term-frontmatter.schema.json` MUST allow `aliases.<locale>` keyed by ISO-639-1 codes (depth-1; the existing repo rule that YAML MUST NOT nest beyond one level forbids deeper structure — `aliases.en: [...]` is depth-1 if treated as a flattened key, so the schema MUST express this either via the flattened form `aliases_en: [...]` or via tolerant validation; the choice is at the schema author's discretion in step 2).
- **R.3.1.4.** `ontology.schema.json` MUST include `deprecated_aliases` per locale to surface dated terms (e.g. "Mental Sex").

### §3.2 Plan step 3 — Scenario set

- **R.3.2.1.** `scenarios.json` v0.1 MUST contain exactly the eleven scenarios enumerated in `task.md § Personas and Working Scenarios`. Adding scenarios goes through the proposal procedure already declared in `task.md § Scenario Taxonomy Rules`.
- **R.3.2.2.** Each scenario entry MUST carry `id`, `persona` (`novel` or `lyric`), `summary` (≤ 25 words), `created`.

### §3.3 Plan step 4 — Ontology bootstrap

- **R.3.3.1.** The three contradictions in §2.2 above MUST be encoded with NCP labels as canonical and the others as aliases.
- **R.3.3.2.** The `ontology.json` MUST distinguish `kind: element` (64 canonical) from `kind: concept` (≈ 35 meta-entries). The seven concept entries inside `elements.md` (Crucial Element, MC Problem, OS Problem/Response/Solution/Symptom, Symptom Element) MUST be authored with `kind: concept`, NOT `kind: element`.

### §3.4 Plan step 5 — Per-term frontmatter

- **R.3.4.1.** The bootstrap helper MUST insert frontmatter blocks at every `## <Term>` anchor in the 22 vocabulary files, totalling 310 blocks.
- **R.3.4.2.** Each block MUST declare `provenance` matching the host file's already-documented status (16 source / 6 extension files, per `synthesis/inventory.md`).

### §3.5 Plan step 6 — Scenario tagging

- **R.3.5.1.** The first pass MUST tag the ~80 candidate terms identified in `synthesis/scenario-survey.md`, capped at 8 scenarios per term.
- **R.3.5.2.** After step 6 completes, the resulting median tag-count per term MUST be measured and recorded; if median > 5 the M01 contingency in `reflection/M01-falsification.md` activates and Plan step 8 is expanded.

### §3.6 Plan step 9 — `validate.py`

- **R.3.6.1.** The four integrity checks already named in `task.md` (Frontmatter↔ontology equality, dynamic-pair reciprocity, quad membership, NCP enum closure) are correct.
- **R.3.6.2.** The NCP enum closure check MUST treat *absent* `ncp_appreciation` as legal for `kind: archetype | quad | dynamic-pair | concept`. Missing-with-reason ≠ missing-by-omission.
- **R.3.6.3.** A fifth check SHOULD be added: **alias-uniqueness** — no alias string MAY appear in two different ontology entries' alias maps in the same locale. This catches drift introduced by step 6.

### §3.7 Plan step 11 — Skill wiring

- **R.3.7.1.** All four affected skill SKILL.md files (`dramatica-theory`, `dramatica-vocabulary`, `ncp-author`, `novel-architect`) MUST gain a `## Navigator` section pointing at `tools/dramatica-nav/nav.py`.
- **R.3.7.2.** `ncp-author/SKILL.md § Dramatica Integration Map` MUST be updated to reference ontology IDs (e.g. `nav.py by-id <id>`) in addition to its existing prose-delegation rules. The prose delegation MUST be retained — it answers *meaning* questions; the navigator answers *lookup* questions.

## §4. Open Questions Surfaced

The kickoff surfaces three questions that block clean schema authoring. Per `RESEARCH.md §4.9` they are filed as follow-up prompts in `/prompts/` for downstream resolution; here we record them so the SPEC is closed.

| ID | Question | Threshold for closure |
|---|---|---|
| **OQ-A** | Should `aliases.<locale>` be expressed in YAML as a depth-2 nested map (`aliases: { en: [...], de: [...] }`) — which violates the repo's depth-1 rule — or as flattened keys `aliases_en: [...]`, `aliases_de: [...]`? | Decide before Plan step 2. The flattened form is the safer default; the nested form would require a repo-wide rule exception. |
| **OQ-B** | The vocabulary's `elements.md` heading says "Element (70)". Do we keep that heading and rely on the `kind` distinction, or rewrite the heading to "Element (64) + Concept (6)"? | Decide before Plan step 6 (scenario tagging touches the file). Recommendation: keep the heading; the per-term `kind` field handles the semantics. |
| **OQ-C** | Do we mint ontology IDs for the 75 entries in `dynamic-pairs-index.md` (one ID per pair) or treat dynamic-pairs as a *property* of an Element entry (`dynamic_pair_id: el.partner`) and not as standalone entries? Hybrid is also possible. | Decide before Plan step 4. Recommendation: hybrid — Elements carry the `dynamic_pair_id` property, and pairs *also* get standalone `kind: dynamic-pair` entries that point at both halves. This makes `nav.py by-quad` and `nav.py by-pair` callable without reverse-walking. |

These three questions are filed under the Task's Open Questions list for the agent who picks up Plan step 2.

## §5. Acceptance Criteria for the Kickoff

```gherkin
Feature: Kickoff research delivers the evidence Task 013 plan steps 2–11 require

  # anchor: KO.1.1
  Scenario: Corpus inventory exists and is complete
    Given the kickoff run has completed
    When an agent inspects /research/integrate-dramatica-ncp-skills/synthesis/inventory.md
    Then the file MUST list every vocabulary file under skills/dramatica-vocabulary/references/
    And the file MUST list every theory chapter under skills/dramatica-theory/references/
    And per-file rows MUST carry term count, kind, provenance flag

  # anchor: KO.1.2
  Scenario: Cross-skill ID contradictions are surfaced and resolved on paper
    Given the kickoff run has completed
    When an agent inspects /research/integrate-dramatica-ncp-skills/synthesis/id-audit.md
    Then the file MUST enumerate at least the three throughline-related contradictions
    And each contradiction MUST carry a "Resolution" block naming the canonical label
        and the aliases that the ontology will register

  # anchor: KO.1.3
  Scenario: Scenario-tag survey produces actionable input for Plan step 6
    Given the kickoff run has completed
    When an agent inspects /research/integrate-dramatica-ncp-skills/synthesis/scenario-survey.md
    Then the file MUST cover all eleven personas-scenarios named in task.md
    And the per-scenario candidate term count MUST be at most the host file's term total

  # anchor: KO.1.4
  Scenario: Falsification check on the per-term frontmatter hypothesis is recorded
    Given the kickoff run has completed
    When an agent inspects /research/integrate-dramatica-ncp-skills/reflection/M01-falsification.md
    Then the file MUST state the hypothesis verbatim
    And MUST list the falsification triggers from task.md
    And MUST record a verdict (survive / fail) against the kickoff measurements
    And MUST declare a pre-commitment that activates if downstream tagging falsifies the hypothesis

  # anchor: KO.1.5
  Scenario: Friction log is present even at FL0
    Given the kickoff run has completed
    When an agent inspects /research/integrate-dramatica-ncp-skills/reflection/friction-log.md
    Then the file MUST declare an FL value at the top
    And the FL declaration MUST hold for FL0 just as for higher FLs
```

## §6. Limitations

This kickoff:

- Did **not** author any JSON Schema. That is Task 013 plan step 2.
- Did **not** modify any skill file. That is Task 013 plan step 11.
- Did **not** implement any Python script. That is Task 013 plan step 9.
- Did **not** measure token-cost reduction. That is Task 013 plan step 13.
- Treated provenance as per-entry (coarse). A per-field provenance map may be needed later; recorded as a meta-question in `reflection/M07-contradiction-log.md`.

## §7. Source Index

- [`/tasks/013-integrate-dramatica-ncp-skills/task.md`](../../../tasks/013-integrate-dramatica-ncp-skills/task.md) — the binding plan this kickoff feeds.
- [`/prompts/integrate-dramatica-ncp-skills/prompt.md`](../../../prompts/integrate-dramatica-ncp-skills/prompt.md) — the executing prompt (currently `status: draft`).
- [`/research/integrate-dramatica-ncp-skills/synthesis/inventory.md`](../synthesis/inventory.md) — corpus inventory.
- [`/research/integrate-dramatica-ncp-skills/synthesis/id-audit.md`](../synthesis/id-audit.md) — cross-skill ID audit.
- [`/research/integrate-dramatica-ncp-skills/synthesis/scenario-survey.md`](../synthesis/scenario-survey.md) — first-pass scenario-tag survey.
- [`/research/integrate-dramatica-ncp-skills/reflection/M01-falsification.md`](../reflection/M01-falsification.md), [`M07-contradiction-log.md`](../reflection/M07-contradiction-log.md), [`friction-log.md`](../reflection/friction-log.md) — reflection artefacts.
- `skills/dramatica-theory/SKILL.md`, `skills/dramatica-vocabulary/SKILL.md`, `skills/ncp-author/SKILL.md`, `skills/novel-architect/SKILL.md` — primary corpus.
- `skills/research-prompt-optimizer/SKILL.md`, `skills/research-prompt-optimizer/catalog.yaml` — methodology source for M01 + M07.
- `skills/spec-skill/SKILL.md` — spec-discipline source for §0–§7 schema.
- Phillips, Melanie Anne & Huntley, Chris. *Dramatica: A New Theory of Story.* 4th ed. Burbank: Screenplay Systems Inc., 2001 — original theory under © Screenplay Systems Inc.
