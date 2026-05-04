# Cross-Skill ID Audit

Reproducible greps across the four primary skills (`dramatica-theory`, `dramatica-vocabulary`, `ncp-author`, `novel-architect`). Three concrete naming contradictions surface; all are resolvable by the canonical-ID + aliases pattern proposed in [`/tasks/013-integrate-dramatica-ncp-skills/task.md § Target Architecture`](../../../tasks/013-integrate-dramatica-ncp-skills/task.md).

## Contradiction 1 — Fourth throughline (the MC↔IC relationship)

| Skill | Label used | Source |
|---|---|---|
| `dramatica-theory/SKILL.md` line 33 | **Subjective Story (SS)** | `\| Subjective Story (SS) \| "we" \| The MC↔IC relationship, treated as its own story \|` |
| `dramatica-theory/SKILL.md` line 3 (description) | **Subjective/Relationship** | `four throughlines (Overall Story, Main Character, Impact Character, Subjective/Relationship)` |
| `dramatica-vocabulary/SKILL.md` line 56 | **Relationship (RS)** | `**Relationship (RS)**: die *Beziehung* zwischen MC und IC als eigene Erzähleinheit` |
| `ncp-author/references/canonical-vocabulary.md` line 20 | **Relationship Story** | `Main Character \| Influence Character \| Objective Story \| Relationship Story` |
| `novel-architect/SKILL.md` line 114 | **RS** | `MC/IC/OS/RS encoden` |

**Resolution.** The ontology MUST register one canonical entity:

```
id: throughline.relationship
canonical_label: "Relationship Story"   # NCP enum compliance — binds JSON output
aliases.en: ["Subjective Story", "RS", "SS"]
aliases.de: ["Beziehungs-Throughline"]
```

NCP's `Relationship Story` is selected as canonical because it is the **enum string** that schema validation rejects unknowns against — i.e. it is the only label with a hard machine-enforcement contract. The theory and vocabulary skills MAY continue to use `Subjective Story (SS)` and `Relationship (RS)` in prose; the ontology's alias map carries the equivalence.

## Contradiction 2 — Third throughline (the foil to MC)

| Skill | Label used | Source |
|---|---|---|
| `dramatica-theory/SKILL.md` line 32 | **Impact Character (IC)** | `\| Impact Character (IC) \| "you" \| The character whose existence challenges the MC's worldview \|` |
| `dramatica-vocabulary/SKILL.md` line 55 | **Impact Character (IC)** | `**Impact Character (IC)**: ein Gegenpol, der den MC herausfordert` |
| `ncp-author/references/canonical-vocabulary.md` line 20 | **Influence Character** | `Main Character \| Influence Character \| Objective Story \| Relationship Story` |
| `novel-architect/SKILL.md` line 114 | **IC** | (uses `Impact` in prose) |

**Resolution.** Same pattern as Contradiction 1:

```
id: throughline.influence
canonical_label: "Influence Character"   # NCP enum compliance
aliases.en: ["Impact Character", "IC"]
aliases.de: ["Einflussfigur", "Impactfigur"]
```

The change in name from "Impact" to "Influence" reflects an evolution within the Dramatica project's own publications (Phillips/Huntley themselves moved to "Influence" in later writings on the model); NCP encodes the newer canonical label.

## Contradiction 3 — MC dynamic for problem-solving style

| Skill | Label used | Source |
|---|---|---|
| `dramatica-theory/SKILL.md` line 88 | **Mental Sex (Linear / Holistic)** | `*Mental Sex* (Linear / Holistic; original term "Male/Female problem-solving" is dated)` |
| `dramatica-vocabulary/SKILL.md` line 93 | **Mental Sex** | `**Mental Sex** (Problem-solving style): Linear ↔ Holistic` |
| `ncp-author/references/canonical-vocabulary.md` line 35 | **Problem-solving Style** | `Benchmark         Problem-solving Style` (suffix in the per-throughline appreciation table) |
| `ncp-author/references/canonical-vocabulary.md` line 209 | **Problem-solving Style** | `\`Problem-solving Style\` are hyphenated exactly as shown.` |

**Resolution.** The original term "Mental Sex" is documented in the theory skill as *dated*; the vocabulary skill already glosses it as "Problem-solving style". NCP's `Problem-solving Style` (hyphenated) is the modern canonical:

```
id: character-dynamic.problem-solving-style
canonical_label: "Problem-solving Style"   # NCP enum compliance
aliases.en: ["Mental Sex"]
deprecated_aliases.en: ["Male/Female problem-solving"]
aliases.de: ["Problemlöse-Stil"]
```

The `deprecated_aliases` field surfaces the dated term so navigator audit-mode can warn when a query lands on it.

## Element / Type cardinality overshoot

| Source | Reported count | Canonical count | Delta | Nature of delta |
|---|---:|---:|---:|---|
| `dramatica-vocabulary/references/elements.md` heading line 1 | 70 | 64 | +6 | Meta-entries: Crucial Element, MC Problem, OS Problem/Response/Solution/Symptom, Symptom Element, Focus, Direction. |
| Explore-subagent walk of `elements.md` | 71 | 64 | +7 | Same 7 plus an extra "Element" introduction entry. |
| Explore-subagent walk of `types.md` | 41 | 16 | +25 | 16 canonical Types + 25 Type-related concepts (Concern, Issue, Problem, etc.). |
| `dramatica-vocabulary/references/archetypes.md` | 9 | 8 | +1 | "Archetype" itself listed as a meta-entry. |

**Resolution.** Schema MUST distinguish two kinds:

- `kind: element` (canonical 64, `kind: type` (canonical 16), `kind: archetype` (canonical 8) — the structural inventory.
- `kind: concept` — meta-entries that *describe* a structural slot but do not occupy one. Crucial Element, Symptom, Focus, etc. live here.

Silently merging the two kinds would corrupt downstream Dynamic-Pair logic — the Crucial Element does not have a dynamic pair; it *is* a slot pointing at one of the 64 Elements.

## Documented gaps (already resolved by Extension files)

| Gap | Source-file behaviour | Extension-file resolution |
|---|---|---|
| Resolve definition empty | `character-dynamics.md` carries the term but no body | `dramatica-fundamentals.md` ships substantive Resolve entry + Steadfast/Change definitions |
| Universe + Mind missing as Class | `classes.md` lists only 2 of 4 Classes | `dramatica-fundamentals.md` ships Universe + Mind entries |
| 16 Element-Quads not enumerated | `dynamic-terms.md` describes Quad concept; no list | `element-quads.md` enumerates all 16 Quads with KTAD positions |
| Linear / Holistic missing as separate entries | implicit in `character-dynamics.md` | `dramatica-fundamentals.md` ships separate entries |

The vocabulary SKILL.md already prescribes the resolution: when source and extension contradict on **mechanics** (Quads, Class distribution, engine rules), extension wins; when they contradict on **wording of an existing definition**, source wins. The schema's `provenance` field encodes which authority answered the lookup.

## NCP enum closure check (preview)

Running `ncp-author/upstream/schema/ncp-schema.json` against the dramatica term universe:

- **Throughlines (4):** clean. NCP's `Main Character | Influence Character | Objective Story | Relationship Story` covers the four with the canonical labels above.
- **Storypoints (24 conceptual + 84 sequenced per throughline):** every storypoint slot maps to a `<Throughline> <Slot>` appreciation string in NCP. No dramatica term is unmappable at this layer.
- **Elements (64):** **partial mapping.** NCP encodes Elements only at the storypoint level (`MC Problem`, `OS Solution`), not as standalone enum values. A query for "what NCP enum represents the Element 'Trust'?" returns the *throughline-slot* the Element occupies in a given storyform, not the Element itself. Schema MUST set `ncp_appreciation_partial: true` for ontology Elements when the closest NCP target is a storypoint slot.
- **Variations (64) and Types (16):** same partial pattern — they appear in NCP only inside `<Throughline> Issue` / `<Throughline> Concern` slot fills, not as standalone enum strings.
- **Archetypes (8):** **no NCP mapping at all.** NCP encodes characters via `narrative_function` enum and Player records; Archetype is dramatica-skill-only. Schema MUST omit `ncp_appreciation` for `kind: archetype` rather than emitting a partial pointer.
- **Quads (16) and Dynamic-pairs (75):** **no NCP mapping.** NCP doesn't encode quad geometry. Schema MUST omit `ncp_appreciation` here too.

This finding refines `task.md` § Target Architecture: the proposed `ncp_appreciation_partial: false` default is wrong. The realistic split is approximately **60% partial / 30% omitted / 10% clean**. The schema MUST allow the `ncp_appreciation` field to be absent (not just `ncp_appreciation_partial: true`).

## What this audit does not resolve

The audit identifies *where* the skills disagree on names; it does not author the resolution. Authoring the canonical `aliases` map for every entity is **Task 013 plan step 4** (bootstrap `ontology.json`). This audit's job is to ensure that step has the data it needs.
