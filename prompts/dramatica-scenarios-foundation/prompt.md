---
type: prompt
status: active
slug: dramatica-scenarios-foundation
summary: "Foundational deep-research prompt for the dramatica-scenarios Epic. Drives a single research run that produces SPEC.md covering: (a) content-template system for skills/dramatica-theory/scenarios/<id>.md, (b) build-time line-indexing for ontology.json, (c) scenario-taxonomy gap analysis. Output feeds the Epic Task body + child-Task list."
created: 2026-05-11
updated: 2026-05-11
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: "dramatica-scenarios-epic"
---

# `dramatica-scenarios-foundation` — Foundational Research Prompt

## Framework

**RISEN+ReAct.** RISEN locks the executor's structured outputs (R/I/S/E/N) at prompt-author time so the SPEC.md sections are committed in advance, not improvised. ReAct gives iterative tool use (read → reason → cross-cite → re-plan) across three interleaved corpora — required because every recommendation MUST cite a specific (file, line) tuple, and the line tuples cannot be predicted at prompt-author time. Two-letter combination chosen because the prompt has both a **structured-artifact requirement** (the SPEC.md skeleton, fixed) and a **tool-using exploration requirement** (corpus traversal with citation tracing, dynamic).

## R — Role

You are a **narrative-systems researcher** with deep familiarity with Dramatica theory (Phillips & Huntley, 2001) and a software-engineering background sufficient to design build-time tooling and content-template DSLs. You write **operational specifications** (not academic prose); every claim you make is backed by a file:line citation from the supplied corpora; you NEVER assert a Dramatica fact without grounding it in either the source-derivative theory chunks or the vocabulary reference files in this repo.

## I — Input

You execute against the agency repo at `/home/user/agency/` (or the URL where it's accessible). The three corpora you traverse:

### Corpus A — Theory chunks (15 files, ~900 KB total) [reader-test:FR-01]

Path: `/home/user/agency/skills/dramatica-theory/references/`

| File | Role |
|---|---|
| `00-storyform-worksheet.md` | Operational template: 8-step storyform build (already operationalized by Task 072). |
| `00-storyform-validation.md` | The 12 hard rules H1–H12 (canonical numbering). |
| `01-foundations.md` | Story Mind premise, four throughlines, four classes. |
| `02-characters.md` | Archetypes, motivation elements, dramatic functions. |
| `03-deep-theory.md` | Story Mind metaphor, perspective theory. |
| `04-theme.md` | Issues, themes, value-arguments. |
| `05-plot-genre.md` | Genre as Mode of Expression. |
| `06-storyforming.md` | Class/Type/Variation/Element selection mechanics. |
| `07-storyencoding.md` | Signposts, journeys, storyweaving. |
| `08-storyweaving-reception.md` | Audience perception, narrative ordering. |
| `09-reference.md` | Term index, dynamic-pair glossary. |
| `10-decision-heuristics.md` | Per-decision tests + indicators (already condensed by Task 072 quick-ref). |
| `11-anti-patterns.md` | AP-1 to AP-14: catalog of failure modes. |
| `12-scene-level-bridge.md` | Q1–Q5 scene-level audit (already operationalized by Task 075). |
| `13-worked-storyforms.md` | Hand-worked examples per Class. |

### Corpus B — Vocabulary reference files (24 files, ~265 indexed terms) [reader-test:FR-02]

Path: `/home/user/agency/skills/dramatica-vocabulary/references/`

| File | Role |
|---|---|
| `dramatica-fundamentals.md` | Class / Type / Variation / Element hierarchy. |
| `archetypes.md` | The 8 archetypes, motivation-element distribution. |
| `character-dynamics.md` | Resolve / Growth / Approach / Mental Sex. |
| `domains.md` | Universe / Physics / Mind / Psychology operational definitions. |
| `elements.md` | The 64 OS Character Elements. |
| `variations.md` | The 64 Variations. |
| `types.md` | The 16 Types. |
| `classes.md` | The 4 Classes. |
| `dynamic-pairs-index.md` | The 75 dynamic pairs. |
| `element-quads.md` | The 16 Element-level quads. |
| `encoding-patterns.md` | How abstract storyform → concrete story encoding. |
| `essential-questions.md` | The questions each Throughline must answer. **High-relevance for Step 1 audit-archetype scenarios.** |
| `storyform-mechanics.md` | Slot-fill mechanics + constraint propagation. **High-relevance for Step 1 slot-fill-archetype scenarios.** |
| `plot-dynamics.md` | Driver / Limit / Outcome / Judgment operational distinctions. |
| `plot-structures.md` | Goal / Requirements / Consequences / Forewarnings / Dividends / Costs / Prerequisites / Preconditions. |
| `character-appreciations.md` | Per-character thematic appreciations (Concern / Issue / Problem / Solution / Symptom / Response). |
| `overview-appreciations.md` | OS-level thematic appreciations. |
| `main-vs-impact-character.md` | MC ≠ Protagonist; IC vs Antagonist distinctions. |
| `dramatica-definitions.md` | Glossary / canonical definitions. |
| `dramatica-terms.md` | Term usage notes + common mistranslations. |
| `dynamic-terms.md` | Dynamic terminology canon. |
| `structural-terms.md` | Structural terminology canon. |
| `storytelling.md` | Storyweaving / encoding-vs-storytelling distinction. |
| `_synonym-lookup.md` | Reverse alias map (e.g. "Faith" → `el.faith`). |

All 24 files are in-scope. The deep-research executor SHOULD weight reads by
relevance to the active Step (e.g. Step 1's audit-archetype design pulls
heavily from `essential-questions.md` + `character-appreciations.md`; Step
1's slot-fill-archetype design pulls heavily from `storyform-mechanics.md` +
`plot-dynamics.md`).

### Corpus C — Ontology JSON (machine-readable)

Path: `/home/user/agency/maintenance/schemas/narrative-ontology/ontology.json`

Schema: `entries[]` array. Each entry has fields `id`, `kind` (`element|variation|type|class|archetype|dynamic-pair|concept|quad|domain`), `canonical_label`, `term_file`, `quad_id`, `ktad_position`, `dynamic_pair_id`, `scenarios[]`, `aliases_en`, `aliases_de`. **Read** the file once; do NOT modify (this prompt's output is design, not implementation).

You may also consult — as supporting context, but do NOT cite as primary source for Dramatica claims:

- `/home/user/agency/skills/novel-architect/SKILL.md` — Pipeline Overview, Phase 0–7.
- `/home/user/agency/skills/novel-architect/phases/phase2-narrative-architecture.md` — Task 072's 8-step Worksheet-Loop binding contract.
- `/home/user/agency/skills/novel-architect-structure/methods/storyform/worksheet-loop.md` — operational walkthrough of one pipeline-archetype (slot-fill).
- `/home/user/agency/skills/novel-architect-structure/methods/validation/hard-rules.md` — Task 073's H1–H12 auto-check pipeline (validation-archetype).
- `/home/user/agency/skills/novel-architect-scene/methods/scene-level-bridge.md` — Task 075's Q1–Q5 audit (audit-archetype).
- `/home/user/agency/tools/dramatica-nav/` — current `nav.py` source and tests.

### Pre-supplied intent (skip re-extraction)

The bullets below are **sufficient** to execute this prompt; `brief.md` is
**archival only** (it captures the askuser exchange that produced these
answers and is not required reading). Salient compressions:

- **Scope:** novel.* scenarios only; lyric.* deferred. Expand the taxonomy first, then author.
- **Tooling:** new `nav.py instruct <entry> <scenario>` subcommand; pre-compile line-numbers into `ontology.json`'s `term_file_line:` field; index scope = vocabulary refs + theory chunks + new scenarios/*.md (self-indexing).
- **Authoring:** content-template SYSTEM (not a single template) — supports multiple pipeline-archetypes (audit / arc-design / slot-fill / validation / encoding / pivot-anatomy).
- **Location:** `skills/dramatica-theory/scenarios/<scenario_id>.md`.
- **Bilingual contract:** EN throughout (matches dramatica-theory).
- **Done bar per scenario:** pipeline + heuristics + anti-patterns + Gherkin + ontology cross-refs + nav.py test + per-scenario end-to-end worked example.

### Existing scenario_ids (current ontology — Step 3 input baseline) [reader-test:FR-03]

The ontology currently defines **6 in-scope `novel.*` scenario_ids** (and 5
`lyric.*` IDs which are out-of-scope per N.4.4). The 6 novel.* keepers
are the FLOOR for §3.4's FINAL taxonomy; gap analysis adds to this floor:

| Existing scenario_id | Approx. novel-architect phase | Tagged-entry count (today) |
|---|---|---|
| `novel.act-pivot` | Phase 5 (Scene Matrix) | 57 |
| `novel.character-arc` | Phase 3 (Character Architecture) | 73 |
| `novel.crucial-element-audit` | Phase 2 (Step 6) + Phase 7 (Iteration) | 73 |
| `novel.diagnose-flat-draft` | Phase 7 (Iteration audit-mode) | 61 |
| `novel.dual-storyform` | Phase 2 (storyform-count branch) | 55 |
| `novel.storyform-slot-fill` | Phase 2 (Steps 1-7) | 74 |

The 5 out-of-scope `lyric.*` IDs (`lyric.album-arc-mapping`,
`lyric.archetype-as-system-part`, `lyric.bridge-pivot`,
`lyric.refrain-as-restatement`, `lyric.verse-chorus-pair`) live alongside
in `ontology.json` but MUST NOT appear in §3.4's final taxonomy.

The naming convention for new scenario_ids (N.2.1) is established by
the existing 6: `novel.<verb>-<object>` (e.g. `act-pivot`,
`crucial-element-audit`) or `novel.<noun-phrase>` (e.g. `character-arc`).
Use this benchmark.

## S — Steps

You MUST execute these four numbered investigative steps in order. Each step has its own observation rule and its own SPEC.md output section. [reader-test:FR-08]

### Step 1 — Content-template system design

**Goal:** specify the meta-template that produces a per-scenario document. The template is a SYSTEM, not a single skeleton, because the existing scenarios fall into at least three pipeline-archetypes (slot-fill, audit, arc-design) and the discovery in Step 3 will likely surface 2–3 more.

**ReAct loop for this step:**

1. **Observe**: read all 6 in-scope `novel.*` scenarios' usage patterns (see "Existing scenario_ids" table in `## I — Input`). For each, identify the `kind` (element/variation/type/etc.) of the entries that reference it. Record which `novel-architect` phase each scenario serves. The 5 `lyric.*` IDs are out-of-scope per N.4.4; ignore them.
2. **Reason**: cluster scenarios by pipeline-archetype. Initial hypothesis (test it; revise if data disagrees):
   - **Slot-fill archetype** — `novel.storyform-slot-fill`, `novel.dual-storyform`. Pipeline shape: ordered Steps with constraint propagation. Output: filled `architecture.yaml` slots.
   - **Audit archetype** — `novel.crucial-element-audit`, `novel.diagnose-flat-draft`. Pipeline shape: question-set with PASS/FAIL/PARTIAL verdicts, surfaces canon-vs-draft disagreements.
   - **Arc-design archetype** — `novel.character-arc`, `novel.act-pivot`. Pipeline shape: temporal-progression (Act I → IV) with milestones at signposts.
3. **Act**: for each archetype, draft a sub-template skeleton with required sections (e.g. for slot-fill: § Pipeline Steps / § Per-Step Inputs / § Constraint Propagation Rules / § Validation Hooks / § Worked Example).
4. **Observe-again**: cross-check the skeletons against Task 072's `worksheet-loop.md` (slot-fill exemplar), Task 073's `hard-rules.md` (validation exemplar), and Task 075's `scene-level-bridge.md` (audit exemplar). Are the section names from the existing exemplars carried into your skeleton, or did you invent new ones? If invented, justify or revert.
5. **Reason-again**: design the SHARED meta-template wrapper (frontmatter schema, mandatory cross-reference sections, ontology-id-citation rule, EN-throughout enforcement). The shared wrapper is the glue; archetype skeletons are the body.

**Step-1 output sections** (subsections of SPEC.md §1):

| §1.x | Subsection | Required content |
|---|---|---|
| §1.1 | Meta-template wrapper | YAML frontmatter spec (type, status, slug, summary, scenario_id, scenario_archetype, novel_architect_phases_served[], created, updated). Mandatory body sections (in order). EN-throughout rule. |
| §1.2 | Archetype skeletons | One sub-section per archetype. For each: section names, required content per section, RFC-2119 normative rules. |
| §1.3 | Cross-reference shape | How a scenario doc cites ontology entries by id (e.g. `[el.faith](../../../maintenance/schemas/narrative-ontology/ontology.json#el.faith)`); how it cites theory chunks (with line numbers, post-Step-2); how it cites the dynamic-pair index. |
| §1.4 | Acceptance Gherkin pattern | Gherkin scenario template (`Feature: <scenario_id>` / `Scenario: <named test case>` / `Given … When … Then … MUST …`). Each scenario doc carries ≥ 3 Gherkin scenarios — one per acceptance criterion in the user-defined "done bar." |
| §1.5 | Worked example pattern | Required: every scenario doc has ONE end-to-end worked example walking the pipeline against a fictional but fully-specified storyform. Fictional storyform spec lives in §6 of the doc; reuses across scenarios where possible. |
| §1.6 | nav.py-test pattern | The required pytest case(s) per scenario doc — what they assert, how they're discovered. |

**Citation rule for Step 1:** every section-design choice MUST cite at least one source — either a Task 072/073/075 file (these are the working exemplars) OR a `dramatica-theory/references/*.md` chunk (these are the theory SSoT). No prose-only design choices.

### Step 2 — Build-time line-indexing implementation spec

**Goal:** specify how line numbers get into `ontology.json` and which files are indexed.

**ReAct loop for this step:**

1. **Observe**: read `tools/dramatica-nav/precompile.py` (the current build pipeline), `tools/dramatica-nav/lib_ontology.py` (the ontology I/O layer), and any `*_index.py` files. Note the existing pre-compile cadence and where `term_file` values get populated.
2. **Reason**: identify the integration point for adding `term_file_line: <int>` and `term_file_anchor: <str>` (the resolved heading-anchor name) to each entry. Decide: regex-based heading anchor resolution, or a markdown-AST parser? The existing `term_file` values use the form `<path>#<anchor-slug>` so anchor → line resolution is straightforward; spec the algorithm.
3. **Act**: design the precompile sub-step. Inputs: list of files to index (vocabulary refs + theory chunks + scenarios/*.md). For each file: parse heading lines, build `{anchor → line_number}` map, then walk `entries[]` and resolve each entry's `term_file` anchor against the map. Persist `term_file_line: <int>` next to existing fields.
4. **Observe-again**: identify failure modes — orphan entries (anchor not found in file), duplicate anchors (same anchor twice in one file), scenarios/*.md self-reference (entry cites a scenario doc that doesn't exist yet). Spec the failure handling: WARN-tier diagnostics + non-fatal continuation? Or ERROR-tier fail-loud? Recommend ERROR-tier for vocabulary refs (must be authoritative) + WARN-tier for scenarios/*.md (incremental authoring tolerated).
5. **Reason-again**: design idempotency. Re-running precompile MUST produce byte-identical `ontology.json` if no inputs changed. Spec: stable iteration order, sorted JSON keys, deterministic anchor resolution. The Spec-K trust audit will fail-loud on non-determinism, so this is non-negotiable.
6. **Act-again**: design the self-indexing cadence. When does precompile re-run? Spec recommendation: on every commit that touches `skills/dramatica-vocabulary/references/`, `skills/dramatica-theory/references/`, or `skills/dramatica-theory/scenarios/`. Either via `pre-commit` hook step or a `make` rule. Cite the existing pre-commit-hook patterns in `.githooks/pre-commit` for consistency.

**Step-2 output sections** (subsections of SPEC.md §2):

| §2.x | Subsection | Required content |
|---|---|---|
| §2.1 | Integration point in precompile.py | Specific function-level integration (which function adds the new step, before/after which existing step). Cite the file:line target. |
| §2.2 | Anchor → line resolution algorithm | Pseudocode + edge cases (case-insensitive anchor matching, slug normalization, duplicate-anchor handling). |
| §2.3 | Failure handling tiers | ERROR / WARN / INFO per file class; surfaced via the existing `Diag` mechanism (cite `tools/fm/_core.py:145` if integrating with fm/ diagnostics). |
| §2.4 | Idempotency guarantees | Specific invariants. Test cases that must pass: byte-identical re-run, byte-identical after re-ordering inputs. |
| §2.5 | Self-indexing cadence | When precompile re-runs; integration with pre-commit; CLI command (e.g. `python3 tools/dramatica-nav/precompile.py --rebuild-line-index`). |
| §2.6 | New ontology.json schema | The new fields' types, presence rules, and migration path (existing entries without `term_file_line:` should NOT cause ERROR until first re-precompile completes). |

**Citation rule for Step 2 (relaxed per reader-test FR-04):** design
recommendations SHOULD cite an existing analogous pattern in
`tools/dramatica-nav/` or `tools/fm/`. If the recommendation is genuinely
novel and no analogous pattern exists, declare it as such in §5
("Novel design — no analogous pattern in tools/") with a one-paragraph
justification — do NOT manufacture a citation that doesn't substantively
support the claim. The hard "every claim cites" rule (N.1) still applies
to claims about Dramatica theory and to claims about existing repo state;
it relaxes ONLY for prescriptive design choices in Step 2.

### Step 3 — Scenario-taxonomy gap analysis

**Goal:** enumerate scenarios missing from the current 6-scenario in-scope `novel.*` set (see "Existing scenario_ids" table in `## I — Input`), with rationale grounded in `novel-architect`'s 8-phase pipeline.

**ReAct loop for this step:**

1. **Observe**: read `skills/novel-architect/SKILL.md` Pipeline Overview (Phases 0–7) and the 8 `phases/phase*.md` files. For each phase, record the operational moments where an agent would reach for theory-grounded guidance. Examples: Phase 2 Step 7 (Signposts) → an agent needs guidance on Signpost-encoding (which Type goes where in the act order) — is there a scenario_id for this? Currently NO; this is a gap.
2. **Reason**: cluster the gap-points by archetype (Step 1's classification). For each cluster, propose 1-3 scenario_ids. Naming convention: `novel.<verb>-<object>` or `novel.<noun-phrase>` (consistent with existing names).
3. **Act**: produce the candidate-scenario table:
   - Columns: `scenario_id`, `novel-architect phase`, `archetype`, `1-line summary`, `entries it would tag` (as ontology-kind class, e.g. "all `el.*` Elements with `quad_id` in OS-Class"), `priority` (P0/P1/P2 for Epic ordering).
4. **Observe-again**: cross-check candidates against the existing 6 in-scope `novel.*` IDs — are any duplicates? Are any too narrow (covered by an existing scenario with a small extension)? Recommend: ADD / EXTEND-EXISTING / SKIP for each candidate.
5. **Reason-again**: produce the FINAL scenario taxonomy = (existing 6 `novel.*` keepers) + (ADD candidates) - (REMOVE redundant existing ones, if any). For each, provide priority for the Epic's child-Task ordering.

**Step-3 output sections** (subsections of SPEC.md §3):

| §3.x | Subsection | Required content |
|---|---|---|
| §3.1 | Phase-by-phase gap walk | Per `novel-architect` phase, list operational moments where theory-grounded guidance is needed but no scenario_id covers. |
| §3.2 | Candidate scenarios table | Columns above; ≥ 1 candidate per gap. |
| §3.3 | ADD / EXTEND / SKIP verdicts | Per candidate, with rationale. |
| §3.4 | FINAL scenario taxonomy | Final list with `scenario_id`, archetype, phase, priority. This list IS the input to the Epic's child-Task list. |
| §3.5 | Per-scenario pipeline-archetype assignment | For every scenario in §3.4: which archetype skeleton from §1.2 applies. If a scenario doesn't fit any archetype, FLAG and recommend a new archetype skeleton. |

**Citation rule for Step 3:** every gap-claim MUST cite a specific phase file (e.g. `skills/novel-architect/phases/phase3-character-architecture.md:42`) showing the operational moment that needs guidance. No "I think this might be a gap" — only "phase N file:line says X, no scenario covers X."

### Step 4 — Decomposition recommendation for the Epic Task

**Goal:** produce the child-Task list for the Epic, with priority-ordered sequencing and a dependency graph.

**ReAct loop for this step:**

1. **Observe**: count §3.4 scenarios (call it `N`). Count §1.2 archetype skeletons (call it `K`).
2. **Reason** [reader-test:FR-05]**:** the Epic's child Tasks fall into four cohorts. Cohort sizes
   are derived from §1.2 archetype count (`K`) and §3.4 scenario count
   (`N`); do NOT hard-code:
   - **Foundation cohort** (≥ 3 Tasks; one per: meta-template + per-archetype
     authoring scaffold; line-index implementation; `nav.py instruct` command
     implementation). Size grows if §1.2 produces > 3 archetypes that warrant
     separate scaffold Tasks.
   - **Discovery confirmation cohort** (1 Task): formalize §3.4's taxonomy in
     `ontology.json` (add new `scenarios[]` tags to entries; remove any §3.3
     SKIP-verdicted IDs).
   - **Authoring cohort** (`N` Tasks; fully parallel after Foundation +
     Discovery): one Task per scenario in §3.4. `N` is determined by §3.4,
     not pre-committed here.
   - **Integration cohort** (≥ 2 Tasks; novel-architect phase wire-up +
     integration tests). Size may grow if multiple novel-architect phases
     each need their own integration Task.
3. **Act**: produce the child-Task table:
   - Columns: `task_id` (proposed), `slug`, `task_blocked_by`, `1-line goal`, `priority`, `est. authoring units (S/M/L)`.
4. **Observe-again**: walk the dependency graph. Is any Task blocked by something not yet accounted for? Is there a critical path that single-threads the Epic? If so, recommend mitigations (e.g. authoring template MAY land before all archetype skeletons if the wrapper is stable).
5. **Reason-again**: priority-order the cohorts. P0 = Foundation. P1 = Discovery confirmation. P2 = Authoring (within authoring, sub-prioritize by which scenarios are most-cited from `novel-architect`'s existing phase files; high-citation scenarios author first).

**Step-4 output sections** (SPEC.md §4):

| §4.x | Subsection | Required content |
|---|---|---|
| §4.1 | Cohort 1 — Foundation Tasks | ≥ 3 sub-task specs (each: slug, goal, blocked_by, est size, acceptance Gherkin). Justify the count from §1.2 archetype count if > 3. |
| §4.2 | Cohort 2 — Discovery confirmation Task | 1 sub-task spec. |
| §4.3 | Cohort 3 — Authoring Tasks | One sub-task per §3.4 scenario (table). Cardinality `N` matches §3.4 row count. |
| §4.4 | Cohort 4 — Integration Tasks | ≥ 2 sub-task specs. Justify the count from the novel-architect phase set §3.5 surfaces as integration-touched. |
| §4.5 | Dependency graph | Mermaid `graph TD` diagram. |
| §4.6 | Critical-path analysis | Longest dependency chain length; mitigations if > 4 hops. |

## E — Expectations (Output deliverables)

You MUST write the SPEC.md to:

```text
/home/user/agency/research/dramatica-scenarios-foundation/output/SPEC.md
```

The output workspace structure (per RESEARCH.md):

```text
/research/dramatica-scenarios-foundation/
├── readme.md                 # MANDATORY (FOLDERS.md §3) — captures research_status frontmatter
├── workspace/                # Your scratchpad — file-reads, intermediate notes, you write here freely
├── synthesis/                # Cross-corpus syntheses (e.g. archetype-cluster.md, gap-analysis.md)
├── reflection/               # MANDATORY: friction-log.md with FL declaration
└── output/
    └── SPEC.md               # THE deliverable: the document below
```

**SPEC.md skeleton** (mirrors S — Steps; do NOT invent your own structure):

```markdown
---
type: research
status: complete
slug: dramatica-scenarios-foundation
research_executes_prompt: dramatica-scenarios-foundation
research_phase: complete
summary: "..."
created: <ISO>
updated: <ISO>
---

# dramatica-scenarios — Foundational Research SPEC

## §0 — Executive summary (one paragraph + bullet list of the §3.4 final scenarios + §4 critical path)

## §1 — Content-template system

### §1.1 Meta-template wrapper (frontmatter + body sections)
### §1.2 Archetype skeletons (one sub-section per archetype)
### §1.3 Cross-reference shape (ontology + theory + dynamic-pair)
### §1.4 Acceptance Gherkin pattern
### §1.5 Worked-example pattern
### §1.6 nav.py-test pattern

## §2 — Build-time line-indexing

### §2.1 Integration point in precompile.py
### §2.2 Anchor → line resolution algorithm
### §2.3 Failure handling tiers
### §2.4 Idempotency guarantees
### §2.5 Self-indexing cadence
### §2.6 New ontology.json schema (term_file_line, term_file_anchor)

## §3 — Scenario-taxonomy gap analysis

### §3.1 Phase-by-phase gap walk
### §3.2 Candidate scenarios table
### §3.3 ADD / EXTEND / SKIP verdicts
### §3.4 FINAL scenario taxonomy (this is the input to the Epic child-Task list)
### §3.5 Per-scenario pipeline-archetype assignment

## §4 — Epic decomposition recommendation

### §4.1 Cohort 1 — Foundation (≥ 3 Tasks; justify cardinality from §1.2)
### §4.2 Cohort 2 — Discovery confirmation (1 Task)
### §4.3 Cohort 3 — Authoring (N Tasks; N = §3.4 row count)
### §4.4 Cohort 4 — Integration (≥ 2 Tasks; justify cardinality from §3.5)
### §4.5 Dependency graph (Mermaid)
### §4.6 Critical-path analysis

## §5 — Risks, blind-spots, deferred decisions

## §6 — Citation index (alphabetized; every cited file:line touched in §1–§4)
```

**Frontmatter rule:** the SPEC.md frontmatter MUST set `research_executes_prompt: dramatica-scenarios-foundation` (mandatory cross-reference per `tools/lint-linkage.py`).

**Friction log:** also write `/home/user/agency/research/dramatica-scenarios-foundation/reflection/friction-log.md` per FRUSTRATED.md FR.B.4. Carries `Highest Frustration Level: FL[0-3]` declaration line.

## Constraints

The N.1–N.7 normative rules below are the binding constraint set for this
research run; they enforce citation discipline, ontology-first naming,
bilingual contract, out-of-scope clarity, reader-test reception, failure-
loud-on-uncertainty, and reproducibility. Honor each as RFC-2119 normative.

## N — Normalization & non-negotiables (constraints + failure modes)

These are RFC-2119 normative.

### N.1 Citation discipline (HARD GATE)

- N.1.1 Every prose recommendation in SPEC.md §1, §2, §3, §4 MUST carry at least one inline citation in the form `[file:line]` or `[file §section]`. Theory-free assertions are forbidden — if you cannot cite, you cannot claim.
- N.1.2 The §6 citation index MUST list every distinct (file, line) tuple cited in §1–§4. Duplicates collapsed; alphabetized by path.
- N.1.3 If a Step requires a citation you cannot find in the supplied corpora, surface it in §5 ("Deferred decisions: claim X needs source Y which is not in the supplied corpus") rather than assert without citation.
- N.1.4 **Cross-corpus citation balance (per reader-test FR-Cross).** The §6 citation index MUST have ≥ 5 distinct citations into each of: Corpus A (theory chunks), Corpus B (vocabulary refs), Corpus C (ontology.json entries — cite as `ontology.json#<entry-id>`). This prevents the executor from passing the ≥ 30-tuple bar with one corpus deeply mined and the other two skimmed. If you genuinely cannot find ≥ 5 in one corpus for a substantive reason, surface it in §5.

### N.2 Ontology-first naming (per AGENTS.md NO.2)

- N.2.1 When you propose a new `scenario_id` in §3.2, the name MUST be lowercase, dot-separated, with the prefix `novel.` and a kebab-case suffix.
- N.2.2 When you propose `entries it would tag` in §3.2, you MUST identify them by ontology-kind + filter (e.g. "all `el.*` entries with `quad_id` in `quad.order-chaos-el`"), NOT by inventing entry names.
- N.2.3 If a recommendation requires an entry that does NOT exist in the current ontology, flag the missing entry in §5 ("Ontology gap: needs `el.foo` to support scenario `novel.bar`") rather than reasoning from a non-existent entry.

### N.3 Bilingual contract

- N.3.1 SPEC.md is **EN throughout** (matches `dramatica-theory`).
- N.3.2 The §1.1 meta-template wrapper MUST mandate EN-throughout for all `scenarios/<id>.md` it produces. Task 079 registers `type: scenario` in `maintenance/schemas/header-ontology.json`; recommend either (a) a `scenario_language: en` frontmatter field on the new namespace (preferred — machine-enforceable), or (b) a body-convention rule applied at content review (no frontmatter change). The L1 schema lacks a generic `language` key today, so do NOT recommend reusing `prompt_language` — it lives in the `prompt_*` namespace and would constitute cross-namespace bleed.

### N.4 Out-of-scope

- N.4.1 Do NOT author actual scenario content (that's the per-scenario child Tasks).
- N.4.2 Do NOT modify `ontology.json` (you read it; child Tasks write to it).
- N.4.3 Do NOT modify `nav.py` source (you spec the new subcommand in §2 and §4; child Tasks implement).
- N.4.4 Do NOT cover `lyric.*` scenarios — the suno-lyric-writer skill owns those.

### N.5 Reader-test (Phase-4 audit) findings reception [reader-test:FR-07]

The prompt-author ran a fresh-frame reader-test on this prompt before you
received it. Audit findings folded back in are marked with the inline tag
`[reader-test:<finding-id>]` (and as parenthetical "per reader-test FR-XX"
in section prose). **Operational protocol:** treat each tagged instruction
as RFC-2119 **MUST** (not SHOULD). Do **NOT** remove the tags — the
prompt-author tracks their resolution through your output. If you find a
tagged instruction unactionable, surface in §5 ("Reader-test finding
FR-XX is not actionable because …") rather than silently skipping it.

### N.6 Failure-loud on uncertainty

- N.6.1 If, mid-execution, you discover that the supplied corpora cannot answer one of the 4 Steps, do NOT proceed by guessing. Stop, write what you have to §5 (Deferred decisions), and exit with `research_phase: partial` in the SPEC.md frontmatter. A partial output is more useful than a confidently-wrong complete output.

### N.7 Reproducibility

- N.7.1 Your `workspace/` directory MUST contain enough notes that a second researcher reading only `workspace/` could re-derive your §1–§4 conclusions. The synthesis isn't private mental state; it's an audit trail.

## Execution mode

Single-shot. You execute this prompt once, write the deliverables, log friction, and exit. No follow-up turns; if the user wants iteration, they'll spawn a new prompt with `prompt_kind: follow-up` and `prompt_spawned_from_research: dramatica-scenarios-foundation`.

## Acceptance signal

The research run is **accepted** when:

1. `research/dramatica-scenarios-foundation/output/SPEC.md` exists with all 6 sections (§0–§6) populated.
2. SPEC.md frontmatter passes `tools/fm/validate.py --type-check`.
3. `tools/lint-linkage.py` confirms `research_executes_prompt: dramatica-scenarios-foundation` resolves to this prompt.
4. `reflection/friction-log.md` exists with a parseable `Highest Frustration Level: FL[0-3]` line.
5. The §6 citation index has ≥ 30 distinct (file, line) tuples AND satisfies the cross-corpus balance from N.1.4 (≥ 5 per corpus).
6. The §3.4 FINAL scenario taxonomy has ≥ 9 entries — the 6 existing `novel.*` keepers as a floor, plus at least 3 ADD-verdicted additions from §3.3. Stricter than "several more" — concrete number. [reader-test:FR-06]
7. The §4.5 dependency graph is a valid Mermaid `graph TD` block (renders without syntax error).

## Authoring metadata

- **Composed by:** Claude Code session 018fi26mmkoWAovM6X4DYGFa, executing the
  `research-prompt-optimizer` v3.3 method by hand (the skill is not loaded as
  a Claude Code skill; pipeline followed manually with the same five phases).
- **Phase 1 — Intent:** four AskUserQuestion rounds, 14 questions, captured in
  [`brief.md`](./brief.md).
- **Phase 2 — Planning:** implicit (the brief's captured answers + this
  prompt's `## R / I / S / E / N` decomposition collectively are the planning
  artifact).
- **Phase 3 — Render:** this file.
- **Phase 4 — Reader Test:** to be run by a fresh-frame subagent; findings
  fold back into this file before the Epic Task is created.
- **Phase 5 — Finalize:** the three-file scaffold (`brief.md` + `prompt.md` +
  `readme.md`) is the workspace; lives in the agency repo, not in a tmp zip.
