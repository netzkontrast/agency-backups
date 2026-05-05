---
type: task
status: active
slug: integrate-dramatica-ncp-skills
summary: "Spec-driven, scenario-keyed restructure of dramatica-theory + dramatica-vocabulary, deeply integrated with ncp-author and novel-architect via a shared Narrative Ontology, per-term frontmatter, and a token-efficient Python navigator suite."
created: 2026-05-04
updated: 2026-05-04
task_id: "015"
task_notes_kickoff: "Research kickoff completed 2026-05-04 — see /research/integrate-dramatica-ncp-skills/output/SPEC.md for findings and Plan-step recommendations."
task_owner: "claude-code"
task_status: in_progress
task_priority: P1
task_uses_prompts:
  - integrate-dramatica-ncp-skills
task_spawns_prompts: []
task_spawns_research:
  - integrate-dramatica-ncp-skills
task_affects_paths:
  - skills/dramatica-theory/
  - skills/dramatica-vocabulary/
  - skills/ncp-author/
  - skills/novel-architect/
  - maintenance/schemas/
  - tools/
  - AGENTS.md
---

# Task 015 — Integrate Dramatica Skills With NCP and Novel-Architect

## Goal

Restructure `dramatica-theory` and `dramatica-vocabulary` so that every theoretical chunk and every vocabulary term is (a) carried by a machine-readable frontmatter block conforming to a shared **Narrative Ontology** schema, (b) annotated with the concrete *usage scenarios* (Novel Author and Organist personas) in which the term applies, and (c) reachable via a small Python `tools/dramatica-nav/` suite that performs token-efficient lookup by term, by scenario, by storyform-slot, by quad, by KTAD position, and by NCP enum value — without ever loading the 900K-character source corpus into the model context. The task is `done` when (i) the schemas under `maintenance/schemas/narrative-ontology/` validate every existing term file, (ii) the navigator scripts are exercised by smoke tests in `tools/dramatica-nav/tests/`, (iii) `ncp-author`, `novel-architect`, `dramatica-theory`, and `dramatica-vocabulary` reference the same ontology IDs without duplicating definitions, and (iv) `tools/check-governance.sh` exits 0 on the resulting tree.

## Background — Why This Task Exists

1. **Two Dramatica skills, two vocabularies, one model.** `dramatica-theory` ships nine prose chapters plus six tool files; `dramatica-vocabulary` ships seventeen Type-bucket files plus six extension files, an alphabetical synonym lookup, and a Dynamic-Pairs index. The two skills reach for the same 64 Elements, 64 Variations, 16 Types, 4 Classes — but with no shared identifier scheme, no scenario tagging, and no programmatic bridge. An agent reading `dramatica-theory` to learn *what* a Crucial Element is, then reading `dramatica-vocabulary` to look up the term's Dynamic Pair, traverses ~30 KB of prose to retrieve <500 bytes of relevant data.
2. **`ncp-author` already ran into the cost.** Its `references/canonical-vocabulary.md` reproduces an enum of 463 appreciations and 144 narrative_functions — a list the dramatica skills also implicitly carry, in different language. The skill compensates with a delegation map (`Dramatica Integration Map` in `SKILL.md`), but the map is text; it is not a callable contract. There is no schema today that lets `ncp-author` ask "give me every dramatica term that maps to NCP appreciation `Main Character Issue`".
3. **`novel-architect` orchestrates but cannot index.** It tells agents to consult dramatica-theory, then dramatica-vocabulary, then ncp-author, in that order. The orchestration is correct but expensive — without a shared index, every workflow loads 3–5 files just to confirm a Storyform slot is theoretically defensible.
4. **The user's two real audiences are absent from the skills.**
   - **The novel author** (`novel-architect`'s primary user) needs to ask *"is this scene encoding the Crucial Element or the Symptom?"* and get back a 1-paragraph answer keyed to the project's storyform.
   - **The organist / Suno-lyric-writer user** (the Agency System triptychon work) needs to ask *"which Element-Pair drives Verse↔Chorus tension on this track?"* and get back the same theory pinned to a different artifact type.
   Both users speak in their own working vocabulary — *"Bridge", "Hook", "Refrain", "Beat", "Sequenz", "Setup-Payoff"* — and the dramatica skills don't translate between domains. The synonym lookup is a single layer; it doesn't index *scenarios*.
5. **Token economics get worse at scale.** The full Dramatica corpus, plus the NCP schema and the novel-architect canon, would not fit in context for a working session. Every query that fails to land on a precise file becomes a 4–10 KB pull. Without a frontmatter-keyed navigator, the cost compounds linearly with session length.
6. **Spec-driven hygiene is not yet applied here.** Tasks 009–011 establish the contract for L1/L2 frontmatter and JSON Schemas across the repo, but the skills under `skills/dramatica-*/` predate that contract and carry no per-chunk frontmatter, no scenario tags, and no machine-readable references to the Schema files Task 011 will produce. This task is the place where that gap closes for the narrative subsystem.

## Pre-Work — Critical-Thinking Hooks (per `skills/research-prompt-optimizer/`)

This task is itself a planning artefact for downstream work. Before the Plan section commits, the design SHOULD survive the same critical-thinking methods the research-prompt-optimizer enforces on rendered prompts. Findings logged here become the falsifiable record this task is judged against.

### Bayesian Prior (M05)

- **Prior:** A frontmatter-keyed Python navigator over per-term files will reduce average per-query token load by ≥70% compared to the current "load the chapter" pattern, and the largest single win will be on Encoding queries (Variation/Element + Quad lookup), because Encoding currently forces the agent to load `element-quads.md` plus one Class chapter plus the synonym lookup.
- **Confidence:** medium-high.
- **What would change the prior:** if the navigator's per-term files are themselves >2 KB on average (e.g. because the scenario annotations bloat them), the win shrinks toward 30–50%. If `dramatica-theory`'s chapter prose is only ever loaded in full anyway (because the queries that need theory are conceptual, not lookup), the chapter-side win is near zero and the savings concentrate entirely on the vocabulary side.

### Contradiction Log (M07) on the Current Skills

- **C1.** `dramatica-theory/SKILL.md` says *"Subjective Story (SS)"* throughline. `dramatica-vocabulary/SKILL.md` says *"Relationship (RS)"*. `ncp-author/references/canonical-vocabulary.md` says *"Relationship Story"*. Three names for one entity. **Resolution:** the ontology MUST register a single canonical ID with all three as registered aliases; every skill MUST refer to it by ID in machine-readable contexts and MAY use the localized label in prose.
- **C2.** `dramatica-vocabulary` ships 70 Element entries while `dramatica-theory` and the canonical theory both describe 64. The 6-entry overshoot is documented as `# Element (70)` at the top of `elements.md`. **Resolution:** the schema MUST distinguish `kind: element-canonical` (the 64) from `kind: element-extension` (the 6), and the navigator MUST allow filtering. Silent merging would corrupt downstream Dynamic-Pair logic.
- **C3.** `dramatica-vocabulary` Source-Files have documented gaps (Resolve empty, Universe + Mind missing as Class, Quad listings absent) that Extension-Files fill. Resolution rule already exists in prose. **Resolution:** the schema MUST carry a `provenance` field per entry distinguishing `source-original` from `extension-derived`, so the navigator's audit mode can surface which lookups are answered by extensions.
- **C4.** `dramatica-theory/SKILL.md` lists *"MC Mental Sex (Linear / Holistic)"* and notes the original term *"Male/Female problem-solving"* is dated. `dramatica-vocabulary` carries `Mental Sex` directly. **Resolution:** the ontology MUST register the modern label as canonical and the dated label as a historic alias with a `deprecation` note — the navigator can warn when a query lands on a deprecated alias.
- **C5.** `ncp-author` claims it owns *"JSON-IO and enum-compliance"* and defers theory to `dramatica-theory`. But `ncp-author/SKILL.md` also asserts *"Quad / KTAD integrity is not validated here. NCP encodes appreciations and narrative_functions but not the Knowledge/Thought/Ability/Desire matrix."* This is a real architectural truth, but it means the ncp-schema and the dramatica-theory model are not isomorphic. **Resolution:** the ontology MUST mark which dramatica entries do *not* have a clean NCP enum mirror, so a `ncp-author` round-trip can flag the lossy slots instead of pretending they translate.

### Falsification (M01)

A hypothesis the design rests on: *"Per-term frontmatter is sufficient to power scenario-keyed lookup without a separate scenario index."* What would falsify this:

- If the median number of scenarios per term exceeds 8, per-term frontmatter becomes large and frequent re-parsing is wasteful. Then the navigator MUST instead build an offline `scenario-index.json` from the frontmatter and query the index at runtime. The schemas MUST be designed so this build step is one pass, not a refactor.
- If scenarios cross-reference each other (e.g. "Scene 12 invokes Crucial Element under the Organist's Refrain pattern"), per-term frontmatter cannot capture that — the index would need a second key. The schema therefore MUST permit `scenarios: [scenario-id, …]` as references, not inline structures.

### Contrast Classes (M04)

Compared to *what*, is the proposed structure better?

- **Baseline 1: keep the current prose-chapter design.** Loses on token efficiency for any lookup-shaped query; wins on prose readability and on the ability of a human to read a chapter end-to-end. The new design MUST preserve chapter readability for the human path while adding the per-term path for the agent path. Concretely: chapters remain as today; per-term files are *generated alongside*, not *instead of*.
- **Baseline 2: build one giant JSON file.** Loses on diff-friendliness (every change re-renders the whole file), on direct human readability, and on the Obsidian-graph integration the rest of the repo uses. The new design therefore prefers **per-file frontmatter** plus a *generated* index.
- **Baseline 3: replicate the upstream NCP enum lists verbatim into Dramatica skills.** Loses on canon hierarchy (the NCP project owns its enums; the Dramatica project owns the underlying theory). The right move is one-way mapping — Dramatica IDs ↔ NCP enum strings — recorded once in the ontology, not duplicated in either skill.

### Pre-Mortem (M03) — Top 5 Failure Modes

1. **Schema bloat.** The ontology schema absorbs every edge case discovered during authoring and grows past 30 fields per term, making authoring slower than the prose system it replaced. *Mitigation:* freeze schema at v0.1 with the minimum fields listed in §6 below; add fields only via a documented schema bump. Reject in-flight additions.
2. **Scenario explosion.** The Novel Author and Organist personas spawn so many sub-scenarios (per-chapter, per-track, per-album) that scenarios become per-document IDs and the navigator becomes a project-state index. *Mitigation:* scenarios are *categories*, not project artefacts. The schema reserves `scenario_id` for categorical IDs (e.g. `novel.act-pivot`, `lyric.verse-to-chorus`), and project-level instances live in `novel-architect`'s NCP file or `the-agency-system-architect`'s canon — referenced *from* scenarios, not embedded.
3. **Navigator becomes a god-tool.** A single Python tool that does navigation + validation + extraction + ontology merge becomes too coupled to maintain. *Mitigation:* ship four small scripts (`nav.py`, `extract.py`, `validate.py`, `ontology-build.py`) with a thin shared library. Each script does one thing; the tests target each independently.
4. **Skills end up tightly coupled to the navigator.** If `dramatica-vocabulary/SKILL.md` references the navigator paths, the skill stops working in environments without Python. *Mitigation:* the skills MUST keep the prose lookup discipline as the primary path (already documented). The navigator is a *complement*, not a replacement. Skill prose mentions the navigator as a token-efficiency option, not a dependency.
5. **Cross-skill ontology drift.** `ncp-author`, `novel-architect`, and the dramatica skills update separately and the IDs drift. *Mitigation:* a single ontology file (`maintenance/schemas/narrative-ontology/ontology.json`) is the canonical source of all IDs. Skills reference IDs; they do not coin new ones. CI check (governance script) verifies no skill defines a `narrative-ontology` ID outside that file.

### Adversarial Query Expansion (M13) — Orthogonal Lenses

Lenses considered while drafting this task that the framing did not initially expose:

- **Multilingual lookup lens.** The user works DE/EN; some Dramatica terms have idiomatic German renderings (e.g. *"Hauptfigur"* for MC). The synonym lookup is EN-only today. The schema MUST allow per-locale aliases — at minimum `aliases.de`, `aliases.en` — so DE→canonical lookup is symmetric to EN→canonical.
- **Privacy / portability lens.** The Dramatica source is © Screenplay Systems and not redistributable. The new artefacts MUST NOT extract or re-create copyrighted prose. Per-term frontmatter that quotes >1 line of source text would cross that line. *Constraint:* per-term files carry **structure** (IDs, dynamic pairs, KTAD position, scenario tags) and *short* operational descriptions written from scratch, not lifted definitions.
- **Failure-recovery lens.** What does the navigator do when a query lands on an ID that exists in the ontology but has no per-term file yet? Default behaviour MUST be to surface the missing-file fact, not to silently fall back to the next nearest term. Silent fallback breaks audits.
- **Time-axis lens.** Dramatica theory itself is stable; NCP schema versions move. The ontology MUST carry an `ncp_schema_min_version` field on entries that were authored against a specific NCP schema, so a future NCP bump does not silently invalidate the cross-skill mapping.

### Mini-Reflection (M0) — What's Most Fragile in This Plan?

The single most fragile piece is the **scenario taxonomy**. Schemas are mechanical; navigators are mechanical; the ontology IDs derive directly from Dramatica theory. But scenarios are an authorial choice — they encode *which working contexts the term shows up in*. Get the taxonomy wrong and the term files carry irrelevant tags; get it too coarse and lookup precision drops. The plan therefore commits to authoring scenarios *iteratively* (start with the two personas Novel Author + Organist, freeze the top 12 categorical IDs, expand only with evidence from real lookups) and to logging the additions in a running scenarios changelog.

## Personas and Working Scenarios

The vocabulary extension is keyed to two real users. Each scenario carries a stable ID; the navigator queries terms by `scenarios contains <id>`.

### Persona A — Novel Author Anna (`novel-architect`'s primary user)

Working on a long-form prose project (e.g. *Kohärenz Protokoll*) with a defined Storyform held in NCP. Her queries during a writing session:

| Scenario ID | Scenario name | Typical query | What the term file MUST surface |
|---|---|---|---|
| `novel.storyform-slot-fill` | Filling a Storypoint slot for a Throughline | "Which Element fits MC Problem if MC Resolve = Change and Crucial Element = Test?" | Dynamic pair partner, Quad mates, KTAD position, NCP enum string for the matching appreciation slot |
| `novel.act-pivot` | Designing the Act-2/Act-3 hinge | "What Type-level signpost transition is canonical at the OS Driver pivot?" | Type's Class, neighbouring Types in the Class's sequence, the dynamic-pair Type that often appears mirrored in the Subjective Story |
| `novel.crucial-element-audit` | Auditing whether a draft really pivots on its declared Crucial Element | "Show every scene that activates Trust or its dynamic pair Test." | Element ID, dynamic pair, encoded Variations the Element rolls up to, NCP appreciation strings |
| `novel.character-arc` | Designing or diagnosing a character arc | "Which Variations does Reason carry across the four signposts?" | Archetype's motivation pair, the Element halves that constitute the pair, the Variation each Element slots under per Class |
| `novel.diagnose-flat-draft` | Diagnosing why a draft feels flat | "If MC has no clear Crucial Element, which terms do I check?" | Pointer to anti-patterns, decision-heuristic file, validation file, with line-anchors |
| `novel.dual-storyform` | Encoding two parallel Storyforms (A + B) for an interference-style novel | "Same Element name in Storyform A and Storyform B — is the conflict legitimate?" | Quad-internal vs. cross-storyform conflict semantics; cross-reference to `novel-architect`'s dual-storyform note |

### Persona B — Organist / Lyric Architect Otto (`the-agency-system-architect` + `suno-lyric-writer`)

Working on a triptychon of albums where each track encodes a dramatic micro-arc. His queries:

| Scenario ID | Scenario name | Typical query | What the term file MUST surface |
|---|---|---|---|
| `lyric.verse-chorus-pair` | Choosing the Element-pair that drives Verse↔Chorus tension | "Track is about giving up control — which dynamic pair?" | Element pair (Control ↔ Uncontrolled), encoded shorthand, sample line-pairs in the right register |
| `lyric.bridge-pivot` | Designing a track bridge that flips the pair | "Which dynamic pair flips at the Bridge if the Verse held Logic?" | Logic ↔ Feeling pair, Variation parents, Class context, structural-pair note |
| `lyric.album-arc-mapping` | Mapping an album to a Story Driver / Outcome / Judgment | "Album 1 outcome is Failure-Good — what does that imply track-by-track?" | Outcome × Judgment ending category, Dramatica's four endings, plus the decision heuristics file's pointer |
| `lyric.archetype-as-system-part` | Mapping system architecture parts onto archetypes | "If AEGIS is the Skeptic and Kael is the Reason, what's the Element-pair tension?" | Skeptic ↔ Reason pair, motivation slots, anti-pattern: characters carrying both halves |
| `lyric.refrain-as-restatement` | Refrain as the structural restatement of the same Element | "Refrain restates the same Element across all verses — when does that work?" | Companion-pair vs. dynamic-pair distinction, Quad geometry primer |

### Scenario Taxonomy Rules

- **Stable IDs.** `<persona>.<scenario>` kebab-case. New scenarios go through a tiny PR that adds the ID to `maintenance/schemas/narrative-ontology/scenarios.json` and links *at least one* term file to it.
- **Categorical, not instance.** A scenario is "verse-chorus pair" — *not* "Track 4 Verse-Chorus pair on Album 2". Project instances live in the project's canon (NCP, canon-meta, etc.) and reference the scenario ID.
- **Per-term scenario list is bounded.** A term SHOULD list ≤8 scenarios; if more apply, the term is probably too coarse and SHOULD be split (rare) or the scenarios are too fine and SHOULD be coalesced (common).

## Target Architecture

### A. Shared Narrative Ontology (cross-skill canon)

Lives in `maintenance/schemas/narrative-ontology/`:

```text
maintenance/schemas/narrative-ontology/
├── ontology.schema.json        # JSON Schema for an ontology entry
├── scenarios.schema.json       # JSON Schema for a scenario definition
├── term-frontmatter.schema.json # JSON Schema for per-term file frontmatter
├── theory-chunk.schema.json    # JSON Schema for theory-chapter frontmatter
├── ontology.json               # Canonical entry table (IDs, kinds, aliases, NCP mapping)
├── scenarios.json              # Canonical scenario table (IDs, persona, blurb)
└── readme.md
```

**Ontology entry** is the single canonical record of a Dramatica concept:

```json
{
  "id": "el.trust",
  "kind": "element",
  "canonical_label": "Trust",
  "aliases": {
    "en": ["accept", "credence"],
    "de": ["Vertrauen", "Zutrauen"]
  },
  "deprecated_aliases": [],
  "dynamic_pair_id": "el.test",
  "quad_id": "quad.evidence",
  "ktad_position": "K",
  "class_id": "class.psychology",
  "type_id": "type.conceiving",
  "variation_id": "var.investigation",
  "ncp_appreciation": "Influence Character Problem",
  "ncp_appreciation_partial": false,
  "scenarios": ["novel.crucial-element-audit", "lyric.verse-chorus-pair"],
  "provenance": "source-original",
  "term_file": "skills/dramatica-vocabulary/references/elements.md#trust",
  "ncp_schema_min_version": "1.3.0"
}
```

**Kinds:** `class`, `type`, `variation`, `element`, `archetype`, `character-dynamic`, `plot-dynamic`, `storypoint`, `dynamic-pair`, `quad`, `signpost-slot`, `concept`. The schema enumerates kinds; novel kinds require a schema version bump.

**One-way NCP mapping.** The `ncp_appreciation` field maps a Dramatica entity to the *closest* NCP enum string. If the mapping is partial (e.g. an Element that NCP only represents at Variation granularity), `ncp_appreciation_partial: true` and the term's `validation-rules.md` reference is added.

### B. Per-Term Frontmatter Files (`dramatica-vocabulary/references/`)

The current Type-bucket files (`elements.md`, `variations.md`, etc.) keep their human-readable layout. **Every individual term section** gains a leading frontmatter block:

```yaml
---
ontology_id: el.trust
kind: element
canonical_label: Trust
dynamic_pair_id: el.test
quad_id: quad.evidence
ktad_position: K
class_id: class.psychology
type_id: type.conceiving
variation_id: var.investigation
scenarios:
  - novel.crucial-element-audit
  - lyric.verse-chorus-pair
ncp_appreciation: Influence Character Problem
ncp_appreciation_partial: false
provenance: source-original
ncp_schema_min_version: "1.3.0"
---
```

The frontmatter is the same fields the ontology table holds, plus nothing extra. Drift between the term file and the ontology is a CI failure (caught by `tools/dramatica-nav/validate.py`).

### C. Theory-Chunk Frontmatter (`dramatica-theory/references/`)

Each chapter gets a top-of-file frontmatter block declaring which ontology IDs it covers and which scenarios it serves:

```yaml
---
type: theory-chunk
chunk_id: dt-09-reference
covers_ontology_ids:
  - class.universe
  - class.physics
  - class.mind
  - class.psychology
  - type.* (all 16)
  - variation.* (all 64)
  - element.* (all 64)
serves_scenarios:
  - novel.storyform-slot-fill
  - novel.crucial-element-audit
summary: "Alphabetical glossary plus canonical lists of 16 Types, 64 Variations, 64 Elements."
---
```

`covers_ontology_ids` MAY use the wildcard form `kind.*` for chapters that cover an entire kind (the canonical-list chapter), but specific terms MUST resolve.

### D. Python Tooling (`tools/dramatica-nav/`)

```text
tools/dramatica-nav/
├── nav.py                      # frontmatter-aware lookup CLI
├── extract.py                  # extract a single term section from a Type-bucket file
├── validate.py                 # ontology ↔ frontmatter ↔ NCP enum cross-check
├── ontology-build.py           # rebuild ontology.json + scenarios.json from frontmatter
├── lib/
│   ├── frontmatter.py          # tiny YAML reader (no nesting > 1; per repo rule)
│   ├── ontology.py             # ontology load + index
│   └── ncp_bridge.py           # one-way mapping helpers; reads ncp-schema.json
└── tests/
    ├── test_nav.py
    ├── test_extract.py
    ├── test_validate.py
    └── fixtures/
```

#### D.1 `nav.py` — query interface

```text
usage: nav.py [-h] {by-id,by-alias,by-scenario,by-quad,by-ktad,by-ncp} ...

Examples:
  nav.py by-id el.trust
  nav.py by-alias "accept" --lang en
  nav.py by-scenario novel.crucial-element-audit --kind element
  nav.py by-quad quad.evidence --include-pairs
  nav.py by-ncp "Influence Character Problem"

Output (default): JSON record with ontology fields + a 1-line "where in the
prose to read more" pointer (file + section anchor). Use --full to inline the
prose section. Default deliberately omits prose to keep tokens cheap.
```

#### D.2 `extract.py` — token-efficient prose pull

Given an ontology ID or a `term_file` path with a section anchor, return the bytes between the section heading and the next sibling heading. No YAML, no surrounding chapter; the agent gets the term's prose and nothing else. Used by the skills' `## Lookup-Disziplin` paths when the agent decides it needs the prose.

#### D.3 `validate.py` — the integrity check

Runs four checks and exits non-zero on any failure:

1. **Frontmatter ↔ ontology equality.** Every per-term frontmatter block matches the ontology entry for the same `ontology_id`.
2. **Dynamic-pair reciprocity.** If `el.trust.dynamic_pair_id == el.test`, then `el.test.dynamic_pair_id == el.trust`.
3. **Quad membership integrity.** Every quad has exactly four members, one per KTAD position, with no duplicates.
4. **NCP enum closure.** Every `ncp_appreciation` value MUST exist in the pinned NCP schema enum (resolved via `skills/ncp-author/upstream/schema/ncp-schema.json`); orphan strings fail.

This script is wired into `tools/check-governance.sh` so the CI pipeline catches drift on every PR.

#### D.4 `ontology-build.py` — rebuild from sources

Walks `skills/dramatica-vocabulary/references/*.md`, parses every per-term frontmatter, and writes `ontology.json`. Validates against `ontology.schema.json`. Idempotent; running it twice produces a byte-identical file. The reverse direction (ontology → per-term frontmatter) is *intentionally not supported* — frontmatter is the source of truth, and the table is a *projection*. This avoids the "two sources of truth" failure mode flagged in the Pre-Mortem.

### E. Skill-Side Wiring

- **`skills/dramatica-vocabulary/SKILL.md`** gains a `## Navigator` section pointing at `tools/dramatica-nav/nav.py`. Its `## Lookup-Disziplin` is updated to mention the navigator as the *fast path* for structured queries; prose lookup remains the path for conceptual questions.
- **`skills/dramatica-theory/SKILL.md`** gets the same `## Navigator` mention and a note that `extract.py` can be used to pull a single term from a 90 KB chapter without loading the chapter.
- **`skills/ncp-author/SKILL.md`** updates its `## Dramatica Integration Map` to reference ontology IDs instead of prose-only delegation: *"Dynamic Pair check on any Element or Variation → `nav.py by-id <id> --include-pairs`"*. The delegation rules to `dramatica-theory` and `dramatica-vocabulary` for *meaning* stay; what changes is that the *lookup* is now mechanical.
- **`skills/novel-architect/SKILL.md`** gets a one-paragraph `## Navigator-Backed Lookups` section. Its routing matrix gains a column for "preferred nav.py call" so that workflow steps that are pure lookups don't load full skill chapters.

## Plan

1. **Inventory the term universe.** Walk `skills/dramatica-vocabulary/references/` and produce `notes.md` with one row per term: file, section anchor, kind, canonical label, current dynamic-pair partner (if any), provenance flag (source vs. extension). Output is `notes.md`'s § Inventory table. (No code yet.)
2. **Author the ontology schemas.** Write `maintenance/schemas/narrative-ontology/ontology.schema.json`, `scenarios.schema.json`, `term-frontmatter.schema.json`, `theory-chunk.schema.json`. The schemas MUST validate `oneOf` per `kind`, ISO-8601 dates, and the constraint that `ncp_appreciation` is either absent or a string (no nulls). Linked from `maintenance/schemas/readme.md`.
3. **Author the canonical scenario set.** Write `scenarios.json` with the 12 scenarios listed in the Personas section above. Each entry: `id`, `persona`, `summary` (≤25 words), `created`. Frozen at v0.1.
4. **Bootstrap the ontology table.** Hand-write `ontology.json` for the 4 Classes, 16 Types, 64 Variations, 64 Elements, 8 Archetypes, 4 character-dynamics, 4 plot-dynamics. Source the IDs from current term files; aliases from the synonym lookup. This is the slow step; expect ~140 entries.
5. **Annotate per-term frontmatter.** Generate per-term frontmatter into the existing Type-bucket files in `skills/dramatica-vocabulary/references/`. Implementation: a one-shot helper in `tools/dramatica-nav/ontology-build.py --bootstrap` that reads `ontology.json` and inserts frontmatter blocks at every `## <Term>` section that doesn't already have one. After this step, ontology + frontmatter are equal by construction.
6. **Add scenario tags.** For each of the ≥40 most-loaded terms (decided by ad-hoc count of cross-references inside the existing skill prose), pick the matching scenarios from §Personas. Update both the per-term frontmatter and the `ontology.json` entry. The remaining low-traffic terms keep `scenarios: []` until a real query produces evidence they should be tagged.
7. **Annotate theory-chunk frontmatter.** Add `type: theory-chunk` frontmatter to each of `skills/dramatica-theory/references/*.md`, listing covered ontology IDs (wildcards permitted) and served scenarios.
8. **Implement the navigator scripts.** Build `tools/dramatica-nav/nav.py`, `extract.py`, `validate.py`, `ontology-build.py`, plus the `lib/` shared helpers. Use stdlib + `pyyaml` + `jsonschema` only — same dependency footprint Task 011 already proposes.
9. **Write smoke tests.** `tests/test_nav.py` covers each subcommand on at least three fixtures; `test_validate.py` covers each of the four integrity checks both passing and deliberately broken. Tests run under `pytest tools/dramatica-nav/tests/`.
10. **Wire skills.** Add the `## Navigator` sections to the four skill SKILL.md files. Reference IDs by ontology ID where possible; prose stays prose. The cross-cutting `AGENTS.md § Narrative Ontology` section already names the schemas and the load triggers (NO.1–NO.6) in advance — the SKILL.md sections are the *skill-specific* operational detail under that umbrella.
11. **Wire CI.** Add `tools/dramatica-nav/validate.py` invocation to `tools/check-governance.sh` (gated on `narrative-ontology` files existing, so the rest of the repo doesn't break if narrative-ontology is removed). Update `tools/check-governance.sh` documentation in `PRE_COMMIT.md`. Confirm the load triggers in `AGENTS.md § Narrative Ontology` resolve (paths from placeholder to real); flip the status note if the schemas now exist.
12. **Run an end-to-end token-cost benchmark.** For ten representative queries (3 from Anna's scenario list, 3 from Otto's, plus 4 storyform-validation cases), measure the bytes the agent loads with the old prose-only path vs. the new navigator path. Record results in `notes.md` § Token-Cost Benchmark. Acceptance threshold: ≥60% reduction on lookup-shaped queries; conceptual queries are exempt.
13. **Author the prompt.** Per `PROMPT.md`, store the executable instruction set for downstream research and authoring at `/prompts/integrate-dramatica-ncp-skills/prompt.md`. The Plan above is the Task; the executable instruction is a Prompt and MUST live in `/prompts/`.
14. **Spawn research workspace.** Per `RESEARCH.md`, the workspace at `/research/integrate-dramatica-ncp-skills/` records the actual evidence (corpus inventory, schema authoring scratch, benchmark logs). Its frontmatter sets `research_executes_prompt: integrate-dramatica-ncp-skills`.
15. **Friction log + Closing.** When all checkboxes pass, write `friction-log.md` with the FL declaration per `FRUSTRATED.md`, set `task_status: done`, and run `/sc:createPR` per `AGENTS.md` § Closing Run Procedure.

## Todo

- [x] 1. Author this `task.md` (current step) — set `task_status: in_progress`.
- [x] 2. Inventory term universe → `notes.md` § Inventory. Verified 310 term-level `## ` headings across 22 vocab files (333 total minus 23 alphabetical buckets in `_synonym-lookup.md`). Drift vs. kickoff: 0. Gate passes.
- [x] 3. Author the four schema files under `maintenance/schemas/narrative-ontology/`. All four valid Draft 2020-12; 11/11 fixture cases pass; line counts 152/82/56/61 (cap 200). Plus `readme.md` documenting the OQ-A/B/C resolutions.
- [x] 4. Author `scenarios.json` (12 scenarios) — actually 11 v0.1 scenarios per the persona table; outer wrapper carries schema_version + ontology_version + created. Authored by Sonnet A.
- [x] 5. Bootstrap `ontology.json` (~140 entries) — actually 304 entries (4 classes + 16 types + 4 throughlines + 8 archetypes + 4 char-dynamics + 4 plot-dynamics + 39 concepts + 35 quads + 65 dynamic-pairs + 62 variations + 63 elements). Authored across Sonnet C (74), Sonnet D (101), main-context (125 + 4 bridging concepts). Cross-entry invariants: 0 schema errors, 0 reciprocity violations, 0 unresolved pair_members, 0 unresolved quad_ids; 11/35 quads partial-membership (documented fractal-distortion limitation).
- [x] 6. Insert per-term frontmatter (Strategic plan Step 5; via inline Python bulk-transform since morphllm MCP isn't loaded). 187 blocks across 11 files; 0 schema errors; pure-insertion diff. Coverage gaps documented in notes.md (~50 sub-headings + ~30 meta-meta + ~25 mismatched anchors deferred to v0.2 cleanup).
- [ ] 7. Tag the top-≥40 terms with scenarios. (Strategic plan Step 6 — `/sc:improve --loop --iterations 3`)
- [ ] 8. Add theory-chunk frontmatter to the nine `dramatica-theory/references/*.md` chapters.
- [ ] 9. Implement `nav.py`, `extract.py`, `validate.py`, `ontology-build.py`, `lib/`.
- [ ] 10. Write smoke tests; pytest passes.
- [ ] 11. Update `dramatica-vocabulary/SKILL.md`, `dramatica-theory/SKILL.md`, `ncp-author/SKILL.md`, `novel-architect/SKILL.md` with navigator wiring.
- [ ] 12. Wire `validate.py` into `tools/check-governance.sh`; update `PRE_COMMIT.md`.
- [ ] 13. Run token-cost benchmark; record to `notes.md`.
- [x] 14. Write `/prompts/integrate-dramatica-ncp-skills/{readme.md,brief.md,prompt.md}` — promoted from `status: draft` to `status: active`; encodes the resolved OQ-A/B/C as binding requirements.
- [x] 15a. Spawn `/research/integrate-dramatica-ncp-skills/` (kickoff phase) with frontmatter, three evidence streams, M01 + M07 reflections, and `output/SPEC.md` consolidating findings + recommendations addressed at Plan steps 2–11.
- [ ] 15b. Run the synthesis-phase research pass after Plan steps 2–11 land (re-execute against the schemas + ontology + navigator to verify acceptance criteria empirically).
- [ ] 16. Friction log; flip `task_status: done`; `/sc:createPR`.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: The Narrative Ontology powers token-efficient lookup across narrative skills

  Background:
    Given the repository contains skills/dramatica-theory, skills/dramatica-vocabulary,
          skills/ncp-author, and skills/novel-architect
    And maintenance/schemas/narrative-ontology/ontology.json exists with at least 140 entries
    And tools/dramatica-nav/ contains nav.py, extract.py, validate.py, ontology-build.py

  # anchor: NO.1.1
  Scenario: Look up an Element by canonical ID and get its dynamic pair without prose load
    Given the ontology entry for "el.trust" exists
    When the agent runs "tools/dramatica-nav/nav.py by-id el.trust --include-pairs"
    Then the script MUST exit 0
    And the JSON output MUST contain "dynamic_pair_id" equal to "el.test"
    And the JSON output MUST contain "quad_id" equal to "quad.evidence"
    And the agent MUST NOT load the full elements.md file to obtain that information

  # anchor: NO.1.2
  Scenario: Look up by everyday alias in either supported language
    Given the ontology entry for "el.test" lists "Test" in aliases.en and "Prüfung" in aliases.de
    When the agent runs "tools/dramatica-nav/nav.py by-alias 'Prüfung' --lang de"
    Then the script MUST return the canonical entry for "el.test"
    And the response MUST include the "term_file" pointer

  # anchor: NO.1.3
  Scenario: Filter terms by working scenario
    Given multiple ontology entries list "novel.crucial-element-audit" in their scenarios
    When the agent runs "tools/dramatica-nav/nav.py by-scenario novel.crucial-element-audit --kind element"
    Then the output MUST be a JSON array
    And every array entry's "scenarios" MUST include "novel.crucial-element-audit"
    And every array entry's "kind" MUST equal "element"

  # anchor: NO.1.4
  Scenario: Validate ontology ↔ frontmatter ↔ NCP enum closure
    Given a per-term frontmatter block whose "ncp_appreciation" string is not present in the pinned NCP schema enum
    When tools/dramatica-nav/validate.py runs
    Then the script MUST exit non-zero
    And the report MUST list the offending ontology_id and the offending NCP string

  # anchor: NO.1.5
  Scenario: Pre-commit governance gate catches drift
    Given a developer modifies skills/dramatica-vocabulary/references/elements.md by hand
          and changes the dynamic_pair_id of "el.trust" without updating the ontology
    When the developer attempts to commit
    Then tools/check-governance.sh MUST exit non-zero
    And the failure message MUST cite "validate.py: dynamic-pair reciprocity violated"

  # anchor: NO.1.6
  Scenario: Skill prose stays human-readable after frontmatter is added
    Given a Type-bucket file "skills/dramatica-vocabulary/references/elements.md"
    When per-term frontmatter blocks are inserted at each "## <Term>" section
    Then a human reading the file in Obsidian MUST still see the existing prose unchanged
    And the inserted frontmatter MUST appear as a YAML block with depth ≤ 1

  # anchor: NO.1.7
  Scenario: Token-cost benchmark passes the ≥60% reduction threshold
    Given the ten benchmark queries enumerated in notes.md § Token-Cost Benchmark
    When each query is executed via the prose-only path and via the navigator path
    Then the average bytes loaded via the navigator path MUST be at most 40% of the prose-only path
    And conceptual queries (where the navigator returns a pointer plus extract.py is invoked)
        MUST NOT be counted in the lookup-query average
```

## Schema Skeletons

### `term-frontmatter.schema.json` (excerpt)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "narrative-ontology/term-frontmatter.schema.json",
  "type": "object",
  "required": ["ontology_id", "kind", "canonical_label", "provenance"],
  "properties": {
    "ontology_id":   { "type": "string", "pattern": "^[a-z]+\\.[a-z0-9-]+$" },
    "kind":          { "enum": ["class","type","variation","element","archetype",
                                "character-dynamic","plot-dynamic","storypoint",
                                "dynamic-pair","quad","signpost-slot","concept"] },
    "canonical_label": { "type": "string", "minLength": 1 },
    "dynamic_pair_id": { "type": "string", "pattern": "^[a-z]+\\.[a-z0-9-]+$" },
    "quad_id":         { "type": "string" },
    "ktad_position":   { "enum": ["K","T","A","D"] },
    "scenarios":       { "type": "array", "items": { "type": "string" }, "maxItems": 8 },
    "ncp_appreciation":         { "type": "string" },
    "ncp_appreciation_partial": { "type": "boolean" },
    "provenance":      { "enum": ["source-original","extension-derived"] },
    "ncp_schema_min_version":   { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" }
  },
  "additionalProperties": false
}
```

(Full schemas land in step 3; the skeleton fixes the contract.)

## Open Questions

### Task-side

- **OQ-1.** Do we represent KTAD as a property of every term, or only of Quad members? Current plan: only of Quad members and the four foundational Elements (Knowledge / Thought / Ability / Desire). All other terms carry KTAD via their Quad. Decide before step 5.
- **OQ-2.** Are scenarios a flat namespace or do they carry sub-personas? Current plan: flat, with the persona prefix (`novel.*`, `lyric.*`) carrying the discrimination. Revisit if a third persona appears (game-narrative? screenplay?).
- **OQ-3.** Should the navigator emit Markdown tables in addition to JSON? Useful for human-in-the-loop review; expensive in tokens. Decision: JSON-only by default; `--md` flag opt-in.

### Kickoff-research-side (resolved)

The kickoff research run surfaced three additional open questions; all three are resolved as binding requirements in [`/prompts/integrate-dramatica-ncp-skills/prompt.md § Binding Resolutions of Open Questions`](../../prompts/integrate-dramatica-ncp-skills/prompt.md). The downstream agent MUST NOT re-open them.

- **OQ-A — Locale alias YAML shape.** Resolved: **flattened keys** (`aliases_en`, `aliases_de`, `deprecated_aliases_<locale>`). Preserves the repo-wide depth-1 YAML constraint; no rule exception needed.
- **OQ-B — `# Element (70)` heading.** Resolved: **keep the heading**; per-term `kind: element` vs `kind: concept` does the semantic work. No prose churn.
- **OQ-C — Dynamic-pair representation.** Resolved: **hybrid** — Elements/Variations carry `dynamic_pair_id` for constant-time partner lookup; standalone `kind: dynamic-pair` entries exist per pair (with `pair_member_a` / `pair_member_b`) so pair-level scenario tagging is addressable. `validate.py` enforces the reciprocity invariant.

## Anti-Patterns to Avoid

- **MUST NOT** duplicate Dramatica term definitions in the ontology JSON. The ontology stores IDs, relationships, and pointers — not the prose. Definitional prose stays in the Type-bucket files (vocabulary skill) and the chapter files (theory skill).
- **MUST NOT** let the navigator scripts depend on the SKILL.md files. The navigator reads frontmatter and the schemas; the SKILL.md is the human/agent-facing entry point. Coupling the navigator to SKILL.md prose creates a circular dependency.
- **MUST NOT** mint NCP enum values from the Dramatica side. NCP owns its enums; the ontology *maps* to them. New NCP enums come from the upstream NCP project, not from this task.
- **SHOULD NOT** expand the scenario list past ~25 categorical IDs without a Pre-Mortem on whether scenarios have started encoding project state.

## Links

- Executing prompt: [`/prompts/integrate-dramatica-ncp-skills/prompt.md`](../../prompts/integrate-dramatica-ncp-skills/prompt.md) — to be authored in step 14.
- Spawned research: [`/research/integrate-dramatica-ncp-skills/`](../../research/integrate-dramatica-ncp-skills/) — to be initialized in step 15.
- Governing specs: [`AGENTS.md`](../../AGENTS.md), [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md), [`RESEARCH.md`](../../RESEARCH.md), [`FOLDERS.md`](../../FOLDERS.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md).
- Sibling tasks (do not collide): [`011-skills-frontmatter-schema-files`](../011-skills-frontmatter-schema-files/) (the Schema infrastructure this task consumes), [`010-skills-frontmatter-index-suite`](../010-skills-frontmatter-index-suite/) (the index suite that may also consume the navigator).
- Skills touched: [`dramatica-theory`](../../skills/dramatica-theory/), [`dramatica-vocabulary`](../../skills/dramatica-vocabulary/), [`ncp-author`](../../skills/ncp-author/), [`novel-architect`](../../skills/novel-architect/).
- Critical-thinking source: [`research-prompt-optimizer`](../../skills/research-prompt-optimizer/) — methods M01, M03, M04, M05, M07, M13, M0 applied above.
- Spec discipline source: [`spec-skill`](../../skills/spec-skill/) — Mode 1 (Generate) shape used for Acceptance Criteria.
