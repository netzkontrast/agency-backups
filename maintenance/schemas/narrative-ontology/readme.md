---
type: readme
status: active
slug: narrative-ontology-schemas
summary: "Reader's guide for the four narrative-ontology JSON Schemas — what they bind, how the per-term frontmatter and the canonical ontology table relate, and the binding resolutions of OQ-A/B/C from the kickoff research."
created: 2026-05-04
updated: 2026-05-04
---

# Narrative Ontology — Schemas

Five JSON Schemas (Draft 2020-12) plus two data files form the canonical contract between [`dramatica-theory`](../../../skills/dramatica-theory/), [`dramatica-vocabulary`](../../../skills/dramatica-vocabulary/), [`ncp-author`](../../../skills/ncp-author/), and [`novel-architect`](../../../skills/novel-architect/). The contract is governed by [Task 015](../../../tasks/015-integrate-dramatica-ncp-skills/) and named in [`AGENTS.md § Narrative Ontology`](../../../AGENTS.md). Most repository tasks do not load these files — see `AGENTS.md` rule **NO.5** (token economy: non-narrative work MUST NOT load the ontology).

## Files

| Path | Contract |
|---|---|
| [`ontology.schema.json`](./ontology.schema.json) | One ontology entry — kind, aliases, dynamic-pair links, NCP mapping, provenance, scenarios. |
| [`scenarios.schema.json`](./scenarios.schema.json) | One persona-scenario entry — `novel.*` or `lyric.*` ID, persona, summary. |
| [`term-frontmatter.schema.json`](./term-frontmatter.schema.json) | Per-term YAML block embedded at every `## <Term>` anchor in `dramatica-vocabulary/references/*.md`. Mirrors `ontology.schema.json` minus `term_file`. |
| [`theory-chunk.schema.json`](./theory-chunk.schema.json) | Chapter-head YAML for `dramatica-theory/references/*.md`. Lists `covers_ontology_ids` + `serves_scenarios`. |
| [`precompiled.schema.json`](./precompiled.schema.json) | One denormalised persona-scenario bundle — `primary_terms[]`, `primary_quads[]`, `primary_pairs[]`, `consumer_hints`. Authored by `tools/dramatica-nav/precompile.py`; emitted artefacts live under [`precompiled/`](./precompiled/) (one JSON per scenario). Read by consumers (`novel-architect`, `ncp-author`) as a token-cheap projection of the prose path. |
| `ontology.json` | Canonical entry table (~215 entries). Authored in Task 015 plan step 4; rebuilt from the per-term frontmatter by `tools/dramatica-nav/ontology-build.py`. |
| `scenarios.json` | The eleven v0.1 persona scenarios. Authored in Task 015 plan step 3. |

The two data files (`ontology.json`, `scenarios.json`) land in plan steps 3–4 and are not present until then. The schemas are present from plan step 2 onward.

## Source-of-truth direction

```
per-term frontmatter (in skills/.../references/*.md)
    │  (one-pass projection by ontology-build.py; idempotent)
    ▼
ontology.json (canonical entry table)
    │  (consumed by tools/dramatica-nav/nav.py for queries)
    ▼
agents reading the navigator output
```

The reverse direction (ontology → per-term frontmatter) is **intentionally not supported**. Frontmatter is the source of truth; the table is a projection. This avoids the "two sources of truth" failure mode flagged in [`task.md § Pre-Work § Pre-Mortem`](../../../tasks/015-integrate-dramatica-ncp-skills/task.md).

## Binding resolutions of OQ-A / OQ-B / OQ-C

The kickoff research [`output/SPEC.md`](../../../research/integrate-dramatica-ncp-skills/output/SPEC.md) surfaced three open questions; all three are resolved as binding requirements in the executing prompt. The schemas encode them:

### OQ-A — Locale aliases use flattened depth-1 keys

`aliases_en: [...]`, `aliases_de: [...]`, `deprecated_aliases_<locale>: [...]`. The repo-wide constraint *"YAML MUST NOT nest beyond one level"* ([`AGENTS.md § YAML Depth Rule`](../../../AGENTS.md)) is preserved without exception. The nested form `aliases: { en: [...], de: [...] }` is **rejected** by `additionalProperties: false`. New locales are legal automatically — the schema's `patternProperties` allows any `aliases_[a-z]{2}` and `deprecated_aliases_[a-z]{2}`.

### OQ-B — `kind: element` vs `kind: concept`

The vocabulary's `elements.md` carries 71 `## <Term>` anchors against canon's 64 Elements; `types.md` carries 41 against canon's 16; `archetypes.md` carries 9 against canon's 8. The extras are *meta-entries about structural slots* (Crucial Element, Symptom, Focus, Direction, Concern, Issue, etc.) — they are not Elements/Types/Archetypes themselves.

The schema enum splits them:

- `kind: element` (canonical 64) / `kind: concept` (the 7 meta-entries inside `elements.md`).
- `kind: type` (canonical 16) / `kind: concept` (the 25 meta-entries inside `types.md`).
- `kind: archetype` (canonical 8) / `kind: concept` (the 1 meta-entry inside `archetypes.md`).

The `# Element (70)` heading in the source file is **kept** — it is a count of *file rows*, not a claim about Dramatica theory. The per-term `kind` field carries the discrimination.

### OQ-C — Hybrid dynamic-pair representation

Two complementary representations:

1. **Property of an Element / Variation entry.** `dynamic_pair_id` field points at the partner's ontology ID. Constant-time partner lookup. Forbidden for `kind: archetype | quad | dynamic-pair | concept | class | throughline` (schema enforces).
2. **Standalone `kind: dynamic-pair` entry.** Each of the 75 reciprocal pairs from `dramatica-vocabulary/references/dynamic-pairs-index.md` becomes its own ontology entry with `pair_member_a` + `pair_member_b`. Required-iff-`kind=dynamic-pair`; forbidden otherwise (schema enforces).

**Reciprocity invariant.** For every standalone `dp.X` with `pair_member_a == el.A` and `pair_member_b == el.B`: `el.A.dynamic_pair_id == el.B` and `el.B.dynamic_pair_id == el.A`. Enforced at runtime by `tools/dramatica-nav/validate.py` (Task 015 plan step 9).

## NCP enum closure (≈ 60% partial / 30% absent / 10% clean)

`ncp_appreciation` is **OPTIONAL**. Three regimes:

- **Clean** (10%) — throughlines and story-level appreciations map 1:1 to NCP enum strings. `ncp_appreciation_partial: false`.
- **Partial** (60%) — Elements / Variations / Types appear in NCP only inside `<Throughline> <Slot>` storypoint strings. The mapping points at the closest storypoint slot. `ncp_appreciation_partial: true`.
- **Absent** (30%) — Archetypes, Quads, Dynamic-pairs, Concepts. NCP encodes characters via `narrative_function`; quad geometry is not encoded at all. The schema OMITS the field rather than emitting a partial pointer. The validator treats absence-with-reason as legal for these kinds.

The schema enforces only one of these three: if `ncp_appreciation_partial` is present, `ncp_appreciation` MUST also be present. Other combinations are validated at the data layer by `validate.py`.

## Provenance

Every entry carries `provenance: source-original | extension-derived`. The split is documented in [`/research/integrate-dramatica-ncp-skills/synthesis/inventory.md`](../../../research/integrate-dramatica-ncp-skills/synthesis/inventory.md) — 16 of 22 vocabulary files are source, 6 are extension. The vocabulary `SKILL.md` documents the precedence rule when source and extension disagree (source wins for *wording* of original definitions; extension wins for *mechanics* like Quads, Class distribution, engine rules).

## When to consume these schemas

| Consumer | Schema(s) loaded | Trigger |
|---|---|---|
| `tools/dramatica-nav/validate.py` | all four | Every CI run, gated on `ontology.json` existing. |
| `tools/dramatica-nav/ontology-build.py` | `term-frontmatter`, `ontology` | When rebuilding `ontology.json` from the per-term frontmatter. |
| `tools/dramatica-nav/precompile.py` | `ontology`, `scenarios`, `precompiled` | When emitting / validating the eleven persona-scenario bundles under `precompiled/`. |
| Authoring agent inserting a per-term block | `term-frontmatter` | At every `## <Term>` heading touched. |
| External agents (Jules, Gemini) | `ontology` | When validating an ontology entry handed to them by a user. The schemas are self-contained; no other repo files are required. |
| Non-narrative work | none | `AGENTS.md` rule NO.5 — token economy. |

## What is *not* in scope here

- These schemas do not redefine Dramatica theory. They are the machine-readable contract *about* Dramatica.
- They do not coin new NCP enum values. The NCP project owns its enums; the ontology *maps* to them.
- They do not carry the per-term prose. Prose lives in the `term_file` pointer's target.

## License note

Per [`task.md § Pre-Work § M13`](../../../tasks/015-integrate-dramatica-ncp-skills/task.md), Dramatica source prose is © Screenplay Systems and is not redistributable. The schemas carry only IDs, relationships, and short structural descriptions written from scratch; no source prose is reproduced here or in `ontology.json`.

## Bumping the schema

Schemas are versioned via `$id`. Breaking changes (removing a field, narrowing an enum, tightening a regex pattern) require:

1. Bumping the version segment in `$id`.
2. Updating every consumer (`tools/dramatica-nav/`).
3. Updating the per-term frontmatter blocks if the change affects validity.
4. Recording the bump in [`AGENTS.md § Narrative Ontology`](../../../AGENTS.md) and in this readme.

Additive changes (new optional field, new alias locale via `patternProperties`) do not require a version bump.
