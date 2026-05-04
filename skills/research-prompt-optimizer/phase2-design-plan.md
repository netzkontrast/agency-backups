# Phase 2 — Design Plan (v3.0-phase2)

> **Status:** v1.2 — FROZEN, ready for implementation.
> **Frozen on:** 2026-05-02
> **Decisions sealed:** all 6 questions resolved (see §8).
>
> This document specifies the behaviour, decision logic, data model, and
> user interaction of Phase 2 (Planning). Implementation builds against
> this spec verbatim. Spec-first, GSD-style.
>
> **Changelog v1.0 → v1.1:**
> - Q1 (language) → EN templates only; Plan-View warns on `language != "en"`
> - Q2 (edit UX) → Hybrid: Sub-Enums for common edit paths + "Edit other (free text)" fallback
> - Q3 (bespoke trigger) → Lenient: ≥2 override_triggers fire → bespoke
> - Q4 (seed query confirm) → Mid-Phase-2.6 askuser bundles seeds + orthogonal lens in 1 turn
> - Q5 (edit-loop cap) → Soft cap at 5 iterations with one-time hint, user decides further
>
> **Changelog v1.1 → v1.2:**
> - Q6 (self-applied methods) → 7 critical-thinking hooks anchored across Phase-2 sub-phases, scaled by `intent.depth`. New §10 specifies hooks; §4 sub-phases reference them at the right moments.

---

## 1. Executive Summary

Phase 2 takes an approved `intent_<slug>.yaml` from Phase 1 and produces
an approved `meta-prompt_<slug>.yaml` that is the deterministic input
for Phase 3 (Render). Between input and output sit ten internal
sub-phases that route the research, select modules from the catalog,
detect batches, author constraint blocks, plan the search vocabulary,
collect slot fills, render a plan view, and loop on user approval until
the plan is signed.

**Phase 2 does not write a research prompt.** It writes a *plan* of a
research prompt. Phase 3 renders the plan into Markdown.

---

## 2. Contract — Inputs and Outputs

### Input

A file `intent_<slug>.yaml` conforming to Schema 1 (frozen, see
`meta-prompt-spec.md`). Phase 2 refuses to start if `approved != true`.

### Output

A file `meta-prompt_<slug>.yaml` conforming to Schema 2 (this iteration
freezes Schema 2). File written to `/mnt/user-data/outputs/`,
`present_files` called.

### Hand-off

No prose. Only the YAML file. Phase 3 reads exactly that file and
nothing from chat history.

---

## 3. Sub-Phases — Pipeline

```
Phase 2.1   Load & Validate Intent           (silent)
Phase 2.2   Category Routing                 (silent · auto · 1 askuser only on ambiguity)
Phase 2.3   Module Selection                 (silent · auto from defaults + signal swap)
Phase 2.4   Batch Detection                  (silent · auto + 1 askuser if Cat-B with no item list)
Phase 2.5   Constraint Block Authoring       (silent · auto from intent)
Phase 2.6   Seed Queries + Orthogonal Lens   (1 BUNDLED askuser · v1.1: 2 questions in one turn)
Phase 2.7   Slot Fill Collection             (1 batched askuser for genuine phase2_fill gaps)
Phase 2.8   Render Plan View                 (silent · adds DE-warning if language != "en")
Phase 2.9   Approval Loop                    (askuser · hybrid Sub-Enums + Free-Text fallback · soft cap @ 5)
Phase 2.10  Write meta-prompt.yaml           (silent · file + present_files)
```

**Total expected user touchpoints:** 1–4 askuser turns.

- **Best case** (well-specified intent, no ambiguity, no missing slots): 2 turns (Phase 2.6 bundled + Phase 2.9 Approval).
- **Typical case** (one slot-fill batch + bundled 2.6 + Approval): 3 turns.
- **Worst case** (ambiguous routing + missing batch list + missing slots + edit loop): 5–6 turns.

This is acceptable. Phase 1 already established the heavy clarification
budget; Phase 2 is mostly machine work on top of an approved intent.

---

## 4. Sub-Phase Specifications

### 4.1 — Load & Validate Intent

```
INPUT:  intent_<slug>.yaml path
ACTION: parse YAML; validate against Schema 1; assert approved == true
OUTPUT: in-memory intent dict
ASKUSER: never
ERROR HANDLING:
  - schema_version mismatch → abort with clear message
  - approved != true → abort with "intent must be approved before Phase 2"
  - file not found → abort
```

**Self-applied hook (§10 ref):** **M07 Contradiction Log** — after parse,
scan intent for internal inconsistencies (e.g., `depth=surface` paired
with `output_format=exhaustive matrix`; `temporal_scope=last 3 months`
paired with `priors=well-established theory pre-2020`). If detected:
log to `meta-prompt.contradictions[]` and surface in Plan-View at 2.8.
Skipped when `intent.depth=surface`.

### 4.2 — Category Routing (A / B / C)

```
INPUT:  intent.routing_hints.category_signal  (may be null)
        intent.intent.research_question
        intent.intent.research_question_unpacked
        intent.intent.output_format
DECISION RULES (in priority order):

  1. If intent.routing_hints.category_signal ∈ {A, B, C} → USE IT.
     Phase 1 already decided. Don't second-guess.

  2. Else apply Signal-Word Detection on research_question +
     research_question_unpacked:

     | Signal pattern (case-insensitive) | → Category |
     |-----------------------------------|------------|
     | "warum scheitert", "find gaps", "unbekannte ursache",
       "explore", "hypothesize", "i suspect", "what's really" | A |
     | "compare", "list all", "vergleichen", "matrix", "list of",
       "due diligence", "benchmark", "inventory", "catalog",
       "summarize the field" | B |
     | "ongoing", "monitor", "track over months", "incremental",
       "weekly/monthly/quarterly refresh", "watch list",
       "running brief" | C |

  3. Output_format strong-signal override:
     - output_format == "comparison_matrix" → B (high confidence)
     - output_format == "json_schema" → B (high confidence)

  4. If two categories tie OR no signal at all → askuser.
     ask_user_input_v0:
       question: "Welcher Recherche-Typ trifft am besten zu?"
       options:
         - "Exploration — Antwort unbekannt, Hypothesen testen"
         - "Extraction — Antwort bekannt, strukturiert sammeln"
         - "Lifecycle — laufend über Wochen/Monate aktualisieren"

OUTPUT: category ∈ {A, B, C}, plus routing_rationale (1 sentence)
ASKUSER: only on ambiguity
```

**Self-applied hooks (§10 ref):**

- **M05 Bayesian Prior** — before running the cascade, write down a
  one-line prior with confidence: *"Prior: Cat-B at confidence 0.7,
  because intent specifies known taxonomy (regulations × subcategories)
  with structured output."* Logged to `meta-prompt.routing.prior`.
- **M01 Falsification** — after the cascade decides, run one
  counter-pass: *"What signals would falsify this routing?"* Document
  in `meta-prompt.routing.falsification_check`. If counter-signals
  exist and are non-trivial, escalate to the askuser branch (step 4
  above) even if the cascade did not tie.

Skipped entirely when `intent.depth=surface` (cascade decides silently).

### 4.3 — Module Selection

This is the heart of Phase 2. It operates on the `catalog.yaml`
(specified in §5).

```
INPUT:  category, intent
ACTION: select modules from catalog according to rules below
OUTPUT: dict of selected modules (methods, framework_structural,
        replication, cross_pollination, with mandatories already
        attached)
ASKUSER: never (this is silent auto-selection)
```

#### 4.3.1 — Method Selection (target: 4–6 methods)

```
ALGORITHM:

  1. mandatory = [M13]
  2. defaults_by_category = {
       A: [M01, M02, M04, M05, M10],
       B: [M06, M07, M08, M12],
       C: [M03, M07, M09, M11],
     }
  3. base_set = mandatory + defaults_by_category[category]
  4. signal_swaps = scan(intent.research_question + unpacked +
                          known_priors) for triggers from the table:

     | If text contains … (≥1 strong match)            | swap_in |
     |--------------------------------------------------|---------|
     | "from first principles", "ground up"             | M10     |
     | "prior", "my hunch", "vermute"                   | M05     |
     | "risk", "fail", "could go wrong"                 | M03     |
     | "compared to", "alternatives", "vs baseline"     | M04     |
     | "challenge", "is it really", "skeptical"         | M02     |
     | "how common", "typical rate"                     | M12     |

     Apply swap-in if not already in base_set; cap total at 6.

  5. If intent.priors_and_constraints.known_priors is not null
     AND M05 is not yet in the set → ADD M05 (priors deserve a
     dedicated method).

  6. If len(set) > 6 → drop lowest-priority method (priority order
     within category: defaults first, then swaps in trigger-strength
     order). Always keep M13.

OUTPUT: ordered list of method IDs (M13 last, others by canonical order)
```

#### 4.3.2 — Framework Selection (Agentic + Structural)

```
agentic_spine: ALWAYS "react" (mandatory)

structural:
  defaults_by_category = {A: "risen", B: "risen", C: "risen"}
  override_triggers (in priority — first match wins):

    | If intent meets …                                | structural |
    |--------------------------------------------------|------------|
    | audience tone is decisive AND output is for      |            |
    |  external/non-expert reader                      | co-star    |
    | known_constraints contains explicit forbidden-   |            |
    |  actions OR research is compliance-focused       | tidd-ec    |
    | output_format == "multiple_variants" OR          |            |
    |  research_question contains "alternatives"       | crispe     |
    | research_question contains "follow this rule:"   |            |
    |  OR known_constraints lists worked examples      | care       |

  bespoke_synthesis_trigger (Q3 lenient · v1.1):
    - ≥2 override_triggers fire simultaneously → bespoke
    - When bespoke, generate provenance map: which component from
      which catalog framework
    - Rationale: lenient threshold accepts that real research tasks
      often combine multiple structural demands; forcing them into
      one catalog framework is the silent failure mode worth fighting

  fallback: if 0 or 1 override fires, use category default.

OUTPUT: framework_structural ∈ {risen, tidd-ec, co-star, care, crispe, bespoke}
        bespoke_components: null OR provenance map
```

#### 4.3.3 — Cross-Pollination Selection (always exactly 2)

```
fixed_pairs_by_category = {
  A: [b-into-a, c-into-a],
  B: [a-into-b, c-into-b],
  C: [a-into-c, b-into-c],
}

selected = fixed_pairs_by_category[category]

OUTPUT: 2 cross-pollination module IDs, both will be inline-expanded
        and tagged "(cross-pollination from Category [X])" in Phase 3
```

#### 4.3.4 — Replication Mechanism Selection

```
replication = [M0]   # M0 always (Reflection Baseline / CONSTRAINT BLOCK 0)
replication += [M1]  # always — constraint blocks have anchors
replication += [M2]  # always — every step gets a restatement checkpoint

# M3 is conditional on batches existing
if Phase 2.4 detects ≥1 batch: replication += [M3]

# M4 is the pre-synthesis integrity check — always
replication += [M4]

# Result for typical case: [M0, M1, M2, M3, M4] (Cat B almost always)
# Result for Cat-A without batches: [M0, M1, M2, M4]
# (Cat-C always has batches via session-iterations: [M0, M1, M2, M3, M4])
```

**Self-applied hook (§10 ref):** **M0 Mini-Reflection (2-Q variant)** —
after module selection commits, answer two questions silently and log
to `meta-prompt.module_selection.reflection`:
1. *Which method choice in this set is the most fragile? (i.e., least
   solid signal in the intent)*
2. *Which non-default method did I activate, and is the trigger really
   present?*

Skipped when `intent.depth=surface`.

### 4.4 — Batch Detection

```
INPUT:  intent, category, framework_structural
OUTPUT: list of batch declarations

DEFAULT BATCHES (always present, regardless of category):
  - "per-axis-query-expansion": M13 → 4 axes [adjacent, opposing, abstraction, orthogonal]
  - "per-reflection-checkpoint": M0 → 5 checkpoints [kickoff, mid-run, post-expansion, pre-synthesis, post-synthesis]
  - "per-pre-synthesis-audit": M4 → 8 items

DOMAIN BATCHES (auto-detected from intent):

  Cat-A: typically NO domain batch (exploration is recursive, not
         iterative). Exception: "for each candidate cause, do X" →
         batch.

  Cat-B: ALMOST ALWAYS has a per-item batch. Detection:
    - intent.research_question matches "for each X" / "list of N" /
      "compare X across" → per-item batch
    - intent.output_format == "comparison_matrix" with 2+ axes →
      per-item batch on the row axis
    - If detected but item list is unknown:
        ASKUSER (1 turn):
          question: "Welche konkreten Items sollen verglichen / extrahiert werden?"
          type: free_text  # falls back to text turn since list-input is open

  Cat-C: ALWAYS has a per-session batch. Cardinality starts at "indefinite"
         (modeled as N=∞ with explicit per-session schema).

BATCH SCHEMA in meta-prompt.yaml:
  batches:
    - name: "per-pflicht-analyse"
      cardinality: 7                  # int OR "indefinite" for Cat-C
      items: [Datennutzung, Transparenz, ...]   # OR null if cardinality="indefinite"
      nested_methods: [M06, M07]      # methods active inside each iteration
      nested_constraint_blocks: [0, 1, 2, 3]  # blocks restated per iteration
      output_schema_per_iteration:
        - field: "Item"
        - field: "Finding"
        - field: "PrimarySource"
        - field: "ConfirmationSources"
        - field: "Contradictions"
        - field: "Confidence"

ASKUSER: at most 1 turn, only when Cat-B with unknown item list
```

### 4.5 — Constraint Block Authoring

```
INPUT:  intent
OUTPUT: ordered list of constraint blocks for the rendered prompt

ALWAYS PRESENT:
  Block 0: M0 Reflection Baseline (auto, no content authoring needed —
           the M0 template is self-contained)

DERIVED FROM INTENT:
  Block 1: Source Priority Rules
    Default content: canonical M1 text (primary > secondary > aggregator)
    Override: if intent.known_constraints mentions sources, adapt the
              default to include those source restrictions

  Block 2: Temporal Scope
    Content: rendered from intent.temporal_scope
            f"Research covers {from} through {to}. {rationale}"

  Block 3: Output Exclusions
    Content: derived from intent.research_question_unpacked
            (the "EXPLIZIT NICHT Teil der Antwort" section)

CUSTOM (only if intent has more):
  Block 4+: only if intent.priors_and_constraints.known_constraints
            contains material that doesn't fit Blocks 1-3
            (e.g., privacy/confidentiality, data-residency)

ASKUSER: never (all derived from intent)

OUTPUT in meta-prompt.yaml:
  constraint_blocks:
    - id: 0
      title: "Reflection Baseline (Always Active)"
      source: "module"  # = use M0 template, no custom content
      module_ref: "m0-reflection"
    - id: 1
      title: "Source Priority Rules"
      source: "authored"
      content: "Primary sources..."
    - id: 2
      ...
```

### 4.6 — Seed Queries + Orthogonal Lens (Bundled · v1.1)

```
INPUT:  intent, category, selected_methods
OUTPUT: seed_queries + expansion_axes_plan

GENERATION (silent, before askuser):

  SEED QUERIES (5–10):
    Generated by Claude from research_question + research_question_unpacked
    + domain_context. Each query 1–6 words (per web_search guidance).
    Diversity: cover different facets of the question.

  M13 EXPANSION AXES — auto-generate three of four:
    - adjacent: synonyms, neighbouring sub-fields → Claude generates
                from the seed vocabulary
    - opposing: failure case / opposite school → Claude generates
    - abstraction: one level up OR down → Claude generates (direction
                   picked based on whether question is broad or narrow)
    - orthogonal: ASKUSER (highest-leverage axis, prone to lock-in)

BUNDLED ASKUSER (1 turn, 2 questions in same call):

  Q1: "Diese Seed-Queries hat Claude aus deinem Intent abgeleitet —
       passt die Auswahl?"
       <render seed list, 5-10 lines>
       options:
         - "Approve seeds — los geht's"
         - "Edit seeds (free text)"
         - "Use decomposition only — keine LLM-Creativity, nur
            mechanische Zerlegung der research_question"

  Q2: "Welche orthogonale Linse hat in deiner Frage bisher niemand
       angesetzt?"
       options (auto-generated by Claude based on lenses NOT present
       in research_question):
         - 3 candidate lenses, e.g. "ökonomisch (Kosten/Nutzen)",
           "historisch (Entwicklung über Zeit)", "rechtlich (Compliance)"
         - "Andere — ich nenne (free text)"

POST-USER PROCESSING:

  If Q1 == "Approve seeds": use as-generated.
  If Q1 == "Edit seeds": follow-up free-text turn for replacement list.
  If Q1 == "Use decomposition only":
    re-generate seeds as mechanical permutations of research_question
    (no LLM-creativity); user sees them in plan view at 2.8.

  If Q2 selects auto-option: use that as orthogonal axis.
  If Q2 == "Andere": follow-up free-text turn.

ASKUSER: 1 turn (bundled); +1 follow-up if Q1 or Q2 needs free text

OUTPUT in meta-prompt.yaml:
  seed_queries: ["...", "...", "..."]
  expansion_axes_plan:
    adjacent: "..."
    opposing: "..."
    abstraction: "..."
    orthogonal: "..."  # from bundled askuser
```

**Self-applied hook (§10 ref):** **M13 Self-Application** — before
auto-generating the three non-orthogonal axes (adjacent / opposing /
abstraction), Claude reflects: *"In which conceptual direction does
the initial seed-vocabulary push me? Where is the genuine opposite?
Is my abstraction direction (up vs. down) actually the under-served
one for this intent?"* The reflection is logged to
`meta-prompt.expansion_axes_plan.self_reflection_note` and used to
adjust the auto-generated axes before the bundled askuser. Without
this hook, all four axes drift toward Claude's local minimum and the
bundled askuser becomes cosmetic.

Skipped when `intent.depth=surface` — auto-generation runs without
self-reflection on the three axes.

### 4.7 — Slot Fill Collection

```
INPUT:  selected_modules, intent
OUTPUT: slot_fills dict (only for phase2_fill slots)

ALGORITHM:

  1. For each selected module, look up its slot definitions in
     catalog.yaml. Each slot has:
       type: phase2_fill | agent_runtime_fill
       description: "..."
       required: true | false
       fill_from_intent: <intent path or null>

  2. agent_runtime_fill slots are SKIPPED entirely. They become
     {{placeholder}} in the rendered prompt and the agent fills them
     during execution.

  3. For each phase2_fill slot:
     a. If fill_from_intent is set, attempt to extract from intent.
        E.g., m03_topic ← intent.intent.research_question (first 100 chars)
     b. If extracted value is non-empty, use it.
     c. Else mark as gap.

  4. Collect all gaps. If any:
     ASKUSER (1 batch, max 3 questions):
       Group thematically. Examples of typical phase2_fill gaps:
       - m05_prior_reason (if M05 selected and intent.known_priors is null)
         → "Warum dieser Prior? Eine Zeile reicht."
       - m13_seed_vocabulary_extras (if Claude wants to validate)
         → "Stimmen diese Seed-Begriffe? [show generated]"
       - cb1_source_priority_overrides (if known_constraints partial)
         → "Spezifische Quellen, die priorisiert werden müssen?"

     Most realistic case: 0–2 gaps total. Often this turn doesn't fire.

ASKUSER: at most 1 turn, often skipped

OUTPUT in meta-prompt.yaml:
  slot_fills:
    m03_topic: "EU AI Act Pflichten für SaaS-Startups"
    m05_prior_reason: "..."
    m13_seed_vocabulary: ["AI Act SaaS", "KI-Verordnung Pflichten", ...]
    cb1_source_priority_extra: "EUR-Lex und BfDI sind Primärquellen"
    # ... only phase2_fill slots; agent_runtime_fill slots not listed
```

### 4.8 — Render Plan View

The compact YAML preview shown to the user before approval. Target:
40–80 lines, human-scannable, mobile-readable.

**v1.1 addition — Language Warning:** if `intent.language != "en"`, the
plan view prepends a warning block:

```
⚠ LANGUAGE NOTE
Templates are English-only in v3.0. Your intent.language = "de", so the
rendered prompt will mix:
  · German prose (intent, framing, your custom CB content)
  · English methods/frameworks (M01 "Falsification", RISEN section
    headers, etc.)
This is intentional — English template anchors prevent semantic drift
in restatement loops. If you want a pure-German prompt, abort and
request DE-template support in a future iteration.
```

```yaml
# Plan View — Research Prompt Composition
slug: eu-ai-act-saas-2026
language: de
intent_ref: intent_eu-ai-act-saas-2026.yaml

routing:
  category: B (Extraction)
  rationale: "Antwort bekannt, comparison_matrix → B"

modules:
  agentic_spine: ReAct (always)
  structural: RISEN
  methods: [M06 SourceTriangulation, M07 ContradictionLog, M08 WhatWouldChangeMyMind, M12 BaseRate, M13 AdversarialQueryExpansion]
  cross_pollination:
    - a-into-b (Hidden-items + Schema-gap)
    - c-into-b (World-Change Check)
  replication: [M0, M1, M2, M3, M4]   # M0 mandatory, M3 because batches

constraint_blocks:
  - 0: Reflection Baseline (M0)
  - 1: Source Priority — "EUR-Lex und BfDI primary; keine Paywall"
  - 2: Temporal Scope — 2024-08-01 → 2027-08-01
  - 3: Output Exclusions — "Keine DSGVO; keine US-Pendants; keine HRS-Details"

batches:
  - per-pflicht-analyse: 7 items × M06+M07
    items: [Datennutzung, Transparenz, Logging, Risikobewertung, ...]
  - per-axis-query-expansion: 4 axes (always)
  - per-reflection-checkpoint: 5 (always)
  - per-pre-synthesis-audit: 8 (always)

search_seed:
  queries: ["AI Act SaaS provider", "KI-Verordnung Pflichten", "AI Act compliance Mittelstand", ...]
  expansion_axes:
    adjacent:    "GDPR spillover KI"
    opposing:    "AI Act Kritik Disproportional"
    abstraction: "KI-Regulierung global Vergleich"
    orthogonal:  "ökonomische Kosten Compliance vs Marktzugang"  ← from your input

slot_fills_summary:
  3 phase2-slots filled from intent
  1 from your slot-fill turn
  9 agent-runtime slots will be filled by the executing agent during the run
```

**Self-applied hooks (§10 ref):** Run BEFORE rendering the plan view.

- **M4 Pre-Synthesis Integrity Check (Phase-2 variant)** — 6-item
  silent self-check before the plan view is presented. Any ✗ blocks
  rendering and forces a self-correct loop:
  ```
  ☐ ReAct framework partial included (mandatory)
  ☐ M0 Reflection module included (mandatory)
  ☐ M13 Adversarial Query Expansion module included (mandatory)
  ☐ Constraint Block 1 (Source Priority) authored
  ☐ Cross-pollination pair = exactly 2 (per category)
  ☐ All `phase2_fill` slots resolved (no `<UNFILLED>` markers)
  ```
- **M03 Pre-Mortem** — generate top-3 failure modes for this plan. The
  list is rendered into the plan view as a `pre_mortem:` section, so
  the user reviews predicted weak points alongside the plan itself.
  Format:
  ```yaml
  pre_mortem:
    - "Cross-pollination A→C may dilute focus if intent.depth=standard"
    - "Orthogonal axis 'rechtlich' overlaps Constraint Block 1 — risk
      of redundant search budget"
    - "Bespoke synthesis (overrides=2) untested in this domain combo;
      monitor first execution for structural drift"
  ```

Both hooks **active for `depth=standard` and `depth=exhaustive`**.
For `depth=surface`: only M4 runs (the integrity check is too cheap
to skip); M03 Pre-Mortem is omitted.

### 4.9 — Approval Loop (Hybrid · Soft Cap @ 5)

**v1.1 mode:** Hybrid Sub-Enums for the three common edit paths, with
"Edit other (free text)" as escape hatch.

```
ITERATION 1..N:

  ASKUSER (top-level approval):
    question: "Plan stimmt — oder welche Sektion willst du editieren?"
    options:
      - "Approve — Plan in meta-prompt.yaml schreiben"
      - "Edit modules"
      - "Edit constraint blocks"
      - "Edit search seed / expansion axes"
      - "Edit other (free text)"

  Branch behaviour:

    "Approve" → exit loop, proceed to 4.10

    "Edit modules" → SUB-ASKUSER:
      question: "Welcher Modul-Bereich?"
      options:
        - "Methods tauschen"        → multi_select over 13 methods,
                                      current selection prefilled
                                      (M13 always checked, locked)
        - "Framework überschreiben" → single_select over 5 + bespoke
        - "Cross-Pollination anpassen" → multi_select over 6 CPs
                                      (paired-by-category, locked
                                      to 2 entries)
        - "Edit other (free text)"  → fall through to free-text turn

    "Edit constraint blocks" → SUB-ASKUSER:
      question: "Welcher Block?"
      options:
        - "Block 1 (Source Priority) editieren"
        - "Block 2 (Temporal Scope) editieren"
        - "Block 3 (Output Exclusions) editieren"
        - "Neuen Block 4+ hinzufügen"          → free-text turn
        - "Edit other (free text)"             → free-text turn
      For "edit existing": free-text turn for new content.

    "Edit search seed / expansion axes" → SUB-ASKUSER:
      question: "Was?"
      options:
        - "Seed-Query hinzufügen"        → free-text turn
        - "Seed-Query entfernen"         → multi_select on current list
        - "Orthogonal axis ersetzen"     → free-text turn
        - "Adjacent / Opposing / Abstraction axis ersetzen" → free-text turn

    "Edit other (free text)" → direct free-text turn:
      "Schreib mir, was du editieren willst — ich rendere den Plan neu."

  After any edit branch: re-run §4.8 (render plan view) and re-loop.

SOFT CAP @ ITERATION 5 (Q5 · v1.1):

  When entering Iteration 5 (i.e., user is about to make their 5th
  edit), prepend a one-time hint to the approval question:

    "Hinweis: 5. Edit-Zyklus. Echte Bedenken oder Detail-Tweaks? Falls
    Tweaks: lass uns approven, du kannst das fertige Markdown danach
    schneller direkt editieren als hier in weiteren Plan-Zyklen."

  This is a HINT, not a block. User may continue editing past 5.
  The hint fires exactly once (Iteration 5); not on every subsequent
  iteration.

OUTPUT: approved == true (or termination on user abort)
```

### 4.10 — Write meta-prompt.yaml

```
ACTION:
  - serialize the in-memory plan to YAML (pyyaml, default_flow_style=False)
  - validate one final time against Schema 2
  - write to /mnt/user-data/outputs/meta-prompt_<slug>.yaml
  - call present_files

ANNOUNCE:
  "Phase 2 abgeschlossen. meta-prompt.yaml geschrieben. Phase 3 (Render)
  ist in v3.0-phase2 noch nicht implementiert; sobald die nächste
  Iteration ausgeliefert ist, kann ich diese Datei in den Render-Schritt
  geben."
```

---

## 5. Catalog Format — `catalog.yaml`

The single source of truth for all modules. Loaded by Phase 2 (for
selection) and Phase 3 (for rendering).

```yaml
schema_version: "1.0"
catalog_version: "1.0"

# ============================================================================
# CATEGORIES (3)
# ============================================================================
categories:
  A:
    full_name: "Exploration (Recursive Search / Tree of Thoughts)"
    inline_block_module: "categories/a-exploration"
    default_methods: [M01, M02, M04, M05, M10]
    default_framework_structural: "risen"
    cross_pollination_pair: ["b-into-a", "c-into-a"]
    typical_batches: []   # exploration is rarely a batch
    signal_words: ["why does", "warum scheitert", "find gaps", "explore",
                   "hypothesize", "i suspect", "what's really going on"]

  B:
    full_name: "Extraction (Plan-and-Execute / Deterministic Collection)"
    ...

  C:
    full_name: "Lifecycle (Long-Running Context Engineering)"
    ...

# ============================================================================
# MODULES — flat dict, lookup by ID
# ============================================================================
modules:

  # ----- METHODS (M01–M13) -----------------------------------------------
  M01:
    type: method
    file: "modules/methods/m01-falsification.md"
    full_name: "Falsification (Karl Popper)"
    short_anchor: "M01-Falsification"
    mandatory: false
    applies_to_categories: [A, B, C]
    default_for: [A]
    triggered_by_signals: ["prove", "show that", "validate", "validate"]
    pairs_well_with: [M02, M08]
    escape_criterion: "≥3 orthogonal disconfirmations OR contra-evidence >20%"
    slots:
      hypothesis:
        type: agent_runtime_fill   # Agent generates these during the tree search
        description: "The current hypothesis being tested as a falsifiable statement"
        required: true
      disprove_phrase:
        type: agent_runtime_fill
        description: "Search phrase designed to surface counter-evidence"
        required: true
      failure_mode_phrase:
        type: agent_runtime_fill
        description: "Phrase capturing the failure case"
        required: true

  M03:
    type: method
    file: "modules/methods/m03-pre-mortem.md"
    full_name: "Pre-Mortem Analysis"
    ...
    slots:
      topic:
        type: phase2_fill                    # known at composition time
        description: "The research topic"
        required: true
        fill_from_intent: "intent.research_question"
      source_type:
        type: agent_runtime_fill              # agent enumerates risks
        description: "Source-type risk the agent identifies"
        required: false
      temporal_window:
        type: agent_runtime_fill
        description: "Temporal-window risk"
        required: false

  M05:
    type: method
    ...
    slots:
      expected_finding:
        type: phase2_fill
        description: "User's prior — what they expect the answer to be"
        required: true
        fill_from_intent: "priors_and_constraints.known_priors"
        fill_from_intent_required: false   # null if user has no prior
      prior_reason:
        type: phase2_fill
        description: "Why the user holds this prior"
        required: true
        fill_from_intent: null              # must be asked if prior exists

  M11:
    type: method
    ...
    slots:
      foundational_assumptions:
        type: phase2_fill_or_runtime         # hybrid — agent extends, but seed from intent if available
        description: "List of foundational assumptions"
        seed_from_intent: "priors_and_constraints.known_priors"
      concrete_check:
        type: agent_runtime_fill
        description: "Decay test per assumption"

  M13:
    type: method
    file: "modules/methods/m13-adversarial-query-expansion.md"
    full_name: "Adversarial Query Expansion"
    short_anchor: "M13-AdversarialQueryExpansion"
    mandatory: true                          # MANDATORY in every prompt
    applies_to_categories: [A, B, C]
    default_for: [A, B, C]                   # always
    slots:
      seed_vocabulary:
        type: phase2_fill
        description: "Initial query vocabulary the agent expands from"
        fill_from_intent: "intent.research_question"   # extracted as seed
      orthogonal_lens:
        type: phase2_fill
        description: "A lens not present in the framing"
        fill_from_intent: null               # asked in Phase 2.6
      adjacent_term:
        type: agent_runtime_fill              # axis 1 — auto-expanded
      opposing_term:
        type: agent_runtime_fill
      higher_level_term:
        type: agent_runtime_fill

  # ----- FRAMEWORKS (1 mandatory + 5 + 1 protocol) -----------------------
  react:
    type: framework
    role: agentic_spine
    mandatory: true
    file: "modules/frameworks/react.md"
    full_name: "ReAct (Reason + Act + Observe)"
    short_anchor: "ReAct"
    slots:
      active_methods_table:
        type: phase2_fill                    # NEW in v3.0 — anchored Reason phase
        description: "Table of active methods with anchors and escape criteria"
        fill_from: "selected_methods"        # programmatic, not from intent

  risen:
    type: framework
    role: structural_layer
    mandatory: false
    file: "modules/frameworks/risen.md"
    full_name: "RISEN (Role · Input · Steps · Expectations · Narrowing)"
    selected_when:
      - default_for_category: [A, B, C]
    slots:
      role:
        type: phase2_fill
        description: "Role description for the executing agent"
        fill_from_intent: "intent.audience"  # mirror, not literal
      # ... R, I, S, E, N components

  # ----- REPLICATION MECHANISMS (5) --------------------------------------
  m0-reflection:
    type: replication
    mandatory: true
    file: "modules/replication/m0-reflection.md"
    constraint_block_id: 0
    full_name: "Reflection Baseline (CONSTRAINT BLOCK 0)"
    slots: {}                                # template is self-contained

  m1-constraint-blocks:
    type: replication
    mandatory: true
    ...

  m3-batch:
    type: replication
    mandatory: false                          # only when batches exist
    selected_when:
      - "len(plan.batches) >= 1"
    slots:
      batch_name:
        type: phase2_fill
      cardinality:
        type: phase2_fill
      items:
        type: phase2_fill
      iteration_steps:
        type: phase2_fill
      output_schema_per_iteration:
        type: phase2_fill

  # ----- CROSS-POLLINATION (6) -------------------------------------------
  a-into-b:
    type: cross_pollination
    file: "modules/cross-pollination/a-into-b.md"
    inject_into_category: B
    source_category: A
    full_name: "Exploration Sanity Pass (Hidden-items + Schema-gap)"
    slots: {}                                 # generic, no slot fills needed

  # ... and so on for all 6
```

### Catalog Schema Validation

A single Python validator (later, in Phase 3 work) ensures:

- Every module file referenced exists
- Every mandatory module is selectable
- Every slot has either `fill_from_intent`, `fill_from`, or
  `agent_runtime_fill`
- Cross-pollination pairs are consistent across categories
- Default methods per category are 4–5 (≤ 6 with M13)

---

## 6. Slot-Type Distinction (Critical Concept)

| Type | Filled By | When | Example |
|---|---|---|---|
| **`phase2_fill`** | Phase 2 logic | composition time | `m03_topic` — extracted from `intent.research_question` |
| **`phase2_fill_or_runtime`** | Phase 2 seeds, Agent extends | both | `m11_foundational_assumptions` — seeded from `known_priors`, extended by agent |
| **`agent_runtime_fill`** | Target Agent | execution time | `m01_hypothesis` — agent generates inside the hypothesis tree |
| **`fill_from`** | Phase 2 programmatic | composition time | `react_active_methods_table` — derived from `selected_methods` |

**Why this matters:**

- v2.1 collapsed all of these into `[BRACKETS]` and forced Phase 1 (or
  the user) to specify all of them upfront. This either over-asked
  (asking for hypothesis-content the agent should generate) or
  under-asked (treating runtime-fills as if they were known).
- v3.0 separates them. Phase 2 only collects `phase2_fill` slots.
  `agent_runtime_fill` slots become `{{placeholder}}` text in the
  rendered prompt with a one-line directive to the agent: *"You fill
  this during execution; the format is X."*
- Net effect: Phase 2 askuser turns drop from typically 5–10 (v2.1) to
  1–4 (v3.0), and the rendered prompt is more honest about what is
  asked of the agent.

---

## 7. ReAct Loop Anchored — The Key Innovation

In v2.1 the ReAct template had a generic 3-question Reason phase. In
v3.0 the Reason phase is **dynamically anchored to the selected
methods**.

The `react.md` template gets a `{{active_methods_table}}` slot that
Phase 2 fills with a literal table:

```markdown
## ReAct Loop — Anchored for THIS Run

Active methods you may invoke in any Reason phase:

| Anchor | Method | When to choose |
|--------|--------|----------------|
| [M06]  | Source Triangulation       | Before committing any citation |
| [M07]  | Contradiction Log          | When sources disagree |
| [M08]  | What Would Change My Mind  | Before locking a tentative conclusion |
| [M12]  | Base-Rate Anchoring        | Whenever a frequency claim appears |
| [M13]  | Adversarial Query Expansion | Always-on; minimum once per 10 min |

In every Reason phase you fill this template verbatim:

> **Active method this Act:** [M__] — one sentence why this and not another.
> **Constraint compliance:** CB__ — one example of how the next Act honors it.
> **Local-minimum check:** [low / medium / high] — if medium/high → invoke M13 first.
> **Reflection trigger:** [is this an M0 checkpoint?] — if yes, write the entry HERE before Act.
> **Plan:** [the concrete next Act in one line]
```

This makes method-drift visible. A Reason phase that doesn't name an
active method or doesn't reference a CB has a missing field — visible
to the next reviewer, and visible to the agent itself when it
re-reads its own log.

This is the single biggest behavioural change v3.0 makes to the
generated prompts.

---

## 8. Decisions Frozen (v1.2)

All six questions from v1.0/v1.1 are resolved as of 2026-05-02.
Implementation builds against these:

| ID | Question | Decision | Where in spec |
|----|----------|----------|---------------|
| **Q1** | Language handling DE/EN | **(a) EN templates only.** Plan-View prepends a Language Note when `intent.language != "en"` explaining the EN/DE mix and pointing to a future iteration for pure-DE templates. | §4.8 |
| **Q2** | Edit-loop UX | **(b+a) Hybrid.** Three Sub-Enum paths (Edit modules / Edit constraint blocks / Edit search seed) for the common edits, plus "Edit other (free text)" as an explicit escape hatch on every level. | §4.9 |
| **Q3** | Bespoke framework trigger | **(b) Lenient.** ≥2 override_triggers fire simultaneously → bespoke. Rationale: real research tasks often combine multiple structural demands; force-fitting one catalog framework is the silent failure mode worth preventing. | §4.3.2 |
| **Q4** | Seed-query confirmation | **(b) Bundled mid-Phase-2.6 askuser.** Seeds shown together with orthogonal-lens question in one turn, with three options (Approve / Edit / Decomposition-only). | §4.6 |
| **Q5** | Edit-loop cap | **(b) Soft cap @ 5.** One-time hint fires when entering iteration 5; user may continue editing past 5. No hard block. Hint appears exactly once per Phase-2 run. | §4.9 |
| **Q6** | Self-applied critical thinking | **(c) Depth-scaled.** 7 hooks anchored at sub-phases (M07, M05, M01, M0-mini, M13-self, M03, M4). Full set active for `depth=standard/exhaustive`; `surface` runs only M4 integrity check. | §10 |

### Implications for the implementation

- **Total askuser budget per Phase-2 run** (typical case):
  - Phase 2.6 bundled: **1 turn** (was: 1 in v1.0 — unchanged but now bundles Q4 with orthogonal lens)
  - Phase 2.7 slot fills: **0–1 turns** (often 0 if intent is rich)
  - Phase 2.9 approval: **1+ turns** (1 if direct approve, 2–6 if editing)
  - **Best case: 2 turns. Typical: 3 turns. Edit-heavy: 5–6 turns (with hint at iteration 5).**

- **Catalog implication:** Q3 leniency means more bespoke synthesis events.
  The `synthesis.md` partial template needs to be production-quality, not
  emergency-only.

- **Plan View implication:** Q1 means the language warning is a *standing*
  feature of the plan view for non-EN intents. The warning is paste-ready
  text, not generated dynamically.

- **Approval-loop UX implication:** Q2's hybrid means the edit-loop
  algorithm has explicit multi-level dispatch (top-level enum →
  sub-enum → optional free-text). The implementation needs to handle
  "Edit other" cleanly at every level — it's not a special case, it's
  an always-present option.

---

## 9. Test Cases (validated after implementation)

When code lands, validate against these:

### T1 — Well-specified Cat-B intent
Use `examples/example-intent.yaml` (EU AI Act).
Expected output:
- routing: B
- methods: [M06, M07, M08, M12, M13] (no swaps; M05 added because
  known_priors present → 6 total)
- framework: RISEN
- batches: per-pflicht-analyse (cardinality 7) + 3 standard batches
- 1 askuser for orthogonal lens, 0 for slot fills, then approval.

### T2 — Vague Cat-A intent
Construct a Phase-1 intent with:
- research_question: "Why does our churn rate spike after month 3?"
- output_format: report
- routing_hints.category_signal: A

Expected:
- routing: A
- methods: defaults + M13 = 6
- framework: RISEN (no override triggers)
- batches: only 3 standard ones (no domain batch)
- 1 askuser orthogonal-lens, 1 askuser for M01.hypothesis-source-of
  (or: leave as agent_runtime_fill — preferred)
- approval

### T3 — Cat-C lifecycle intent
Construct Phase-1 intent with:
- research_question: "Monitor EU AI Act enforcement actions monthly"
- output_format: periodic_brief
- temporal_scope: from=2025-08-01, to=unbounded

Expected:
- routing: C
- methods: defaults + M13
- replication: full set including M3 (per-session batch)
- batches: per-session + 3 standard
- One Cat-C-specific challenge: cardinality="indefinite" handling

### T4 — Bespoke framework trigger
Construct Phase-1 intent with:
- research_question: complex compliance + audience-tone + multi-variant
  output requirements
- expected: 3 override triggers fire → bespoke synthesis proposed

### T5 — Edit-loop stress test
Run T1, then in approval pick "Edit modules" 4 times in sequence
(swap M06 for M02, then back, then swap framework to TIDD-EC, then
back).
Expected: edit loop survives, plan view re-renders correctly each
time, final approve writes correct YAML.

---

## 10. Skill-Internal Critical Thinking (Self-Applied Methods)

**Principle.** The methods Phase 2 selects for the *generated* prompt
are the same methods Phase 2 should apply to its *own* planning work.
Forcing reflection only on external research agents while running the
planning step un-reflectively is a structural inconsistency: the
skill demands discipline it does not practise.

**Resolution (Q6 · v1.2):** seven critical-thinking hooks are anchored
at specific sub-phases. Each hook is silent unless it surfaces a
finding (contradiction, falsifying signal, fragility, pre-mortem
risk). Hooks are scaled by `intent.depth` to keep the plan view from
turning into a meta-essay for trivial intents.

### 10.1 — Hook Map

| # | Sub-Phase | Method | Function |
|---|-----------|--------|----------|
| 1 | 4.1 Load | **M07** Contradiction Log | Scan intent for internal inconsistencies (depth ↔ output, scope ↔ priors, etc.) |
| 2 | 4.2 Routing | **M05** Bayesian Prior | Write down prior + confidence before cascade runs |
| 3 | 4.2 Routing | **M01** Falsification | After cascade decides, run one counter-pass |
| 4 | 4.3 Modules | **M0** Mini-Reflection (2-Q) | Surface fragile method choices and trigger-validity |
| 5 | 4.6 Seeds | **M13** Self-Application | Reflect on auto-axis direction before generation, prevent local-minimum lock-in |
| 6 | 4.8 Plan-View | **M03** Pre-Mortem | Top-3 failure modes for the plan, rendered into plan view |
| 7 | 4.8 Plan-View | **M4** Pre-Synthesis Integrity | 6-item completeness self-check, blocks rendering on fail |

### 10.2 — Depth Skalierung

```
intent.depth == "surface"      → MINIMAL: hooks 6 (M03 omitted) + 7 only
                                  (rationale: surface intents are quick;
                                  meta-reflection overhead would dwarf
                                  research budget)

intent.depth == "standard"     → FULL: all 7 hooks active

intent.depth == "exhaustive"   → FULL: all 7 hooks active + Pre-Mortem
                                  list is allowed to grow to 5 items
                                  instead of 3
```

### 10.3 — Output Format

All self-reflection output lands in the meta-prompt under a dedicated
`self_reflection:` block. The block is rendered visibly in the plan
view (compact form: 1 line per hook unless a finding exists).

```yaml
# meta-prompt_<slug>.yaml — self_reflection: block

self_reflection:
  contradictions:        # M07 — empty list if none found
    - field_a: "depth=surface"
      field_b: "output_format=exhaustive matrix"
      severity: "medium"
  routing:
    prior:               # M05
      category: "B"
      confidence: 0.7
      rationale: "structured taxonomy + known output template"
    falsification_check: # M01
      counter_signals: []
      escalated_to_askuser: false
  module_selection:      # M0 mini
    fragile_choice: "M11 Assumption-Decay — trigger present but weak"
    non_default_activations:
      - method: "M11"
        trigger: "intent.priors=well-established theory pre-2020"
        validity: "confirmed"
  expansion_axes_plan:
    self_reflection_note: "Initial seed pushes toward technical/regulatory; opposite is socio-economic; abstraction-up under-served vs. abstraction-down."
  pre_mortem:            # M03 — Top 3 (5 if exhaustive)
    - "Cross-pollination A→C may dilute focus if depth=standard"
    - "Orthogonal axis 'rechtlich' overlaps Constraint Block 1 — risk of redundant search budget"
    - "Bespoke synthesis untested in this domain combo; monitor first run"
  integrity_check:       # M4 — passes/fails
    react_partial: true
    m0_module: true
    m13_module: true
    cb1_authored: true
    cp_pair_exact: true
    no_unfilled_slots: true
    overall: "pass"
```

### 10.4 — Build Implications

- `meta-prompt-spec.md` Schema 2 must include the `self_reflection:`
  block with all sub-fields above.
- `phases/phase2-planning.md` references this section (§10) at every
  sub-phase that has a hook — no separate "self-reflection chapter"
  in the implementation prose.
- Catalog entries for M07, M05, M01, M0, M13, M03, M4 already exist —
  they need an additional `self_applicable: true` flag in
  `catalog.yaml` so a Phase-3 dev tool could later compute "which
  catalog methods are also Phase-2-internal".
- Plan View rendering: `self_reflection:` block sits between
  `slot_fills_summary` and the constraint blocks listing, in folded
  form by default (`<details>`-style if Markdown supports it for the
  user's surface).

### 10.5 — Honest Trade-off

The hooks add 5–15 seconds of Claude reasoning per Phase-2 run, plus
20–60 lines to the plan view. For `depth=surface` intents this is
disproportionate, hence the depth skalierung. For `depth=standard`
and `exhaustive` intents the trade-off pays off twice: (1) better
plans, (2) the user sees *why* the plan is what it is, not just *that*
it is what it is.

The risk is over-engineered self-reporting that nobody reads. The
mitigation is the compact-by-default rendering: only findings surface;
empty hooks render as a single ✓-line.

---

## 11. Implementation Estimate

When approved, the build is roughly:

| Component | Estimated Lines | Notes |
|---|---|---|
| `phases/phase2-planning.md` (replaces stub) | ~300 | Detail spec mirroring this plan |
| `catalog.yaml` | ~600 | Master index of all 34 modules |
| `modules/categories/{a,b,c}.md` (3 files) | ~150 total | Templated from v2.1 inline blocks + frontmatter |
| `modules/methods/m{01..13}.md` (13 files) | ~520 total | Templated from v2.1 + slot frontmatter |
| `modules/frameworks/{react,risen,...,synthesis}.md` (7 files) | ~280 total | Templated from v2.1 + slot frontmatter; ReAct gets new active_methods_table slot |
| `modules/replication/{m0..m4}.md` (5 files) | ~320 total | Templated from v2.1 + slot frontmatter |
| `modules/cross-pollination/*.md` (6 files) | ~300 total | Templated from v2.1 + slot frontmatter |
| `modules/partials/` (frontmatter, meta-header, react-anchored, synthesis-schema) | ~150 total | New |
| `modules/verification/final-checklist.md` | ~80 | Templated from v2.1 |
| Phase 2 logic (lives inside Claude's behaviour, not as Python) | n/a | The skill prose IS the algorithm |
| `examples/example-meta-prompt.yaml` | ~120 | Worked Phase 2 output |
| Update to `SKILL.md` (Phase 2 section becomes live) | ~80 added | Replace stub with full algorithm |
| Update to `meta-prompt-spec.md` (Schema 2 frozen) | ~100 added | Spec out Schema 2 fully |
| **Total NEW content** | **~3,000 lines** | Most of it is templated module content already 90% existing in v2.1 |

Net addition over v3.0-phase1: ~2,000 lines of genuinely new spec +
~1,000 lines of templated v2.1 content with v3.0 frontmatter overlay.

The Phase 2 *logic* itself is ~300 lines of skill prose (the
algorithm in §4 fully written out). No Python in this phase — Phase 2
runs as Claude's behaviour, like Phase 1.

---

## 12. Build Sequence (post-freeze)

Spec is sealed as of 2026-05-02 (v1.2). Implementation order:

1. **`SKILL.md` Phase 2 section** (replaces stub) — algorithm from §4
   written as Claude-readable prose, mirroring the v1.1 decisions.
2. **`meta-prompt-spec.md` Schema 2** (frozen at end of build) — full
   schema for `meta-prompt_<slug>.yaml`, building on §5 catalog refs.
3. **`catalog.yaml`** — master index of all 34 modules per §5 schema.
4. **`modules/` tree** — 34 partial files with v3.0 frontmatter
   (slot definitions per §6) wrapping the templated v2.1 content.
5. **`modules/partials/`** — new shared partials (frontmatter, meta-
   header, **react-loop-anchored** per §7, synthesis-schema, language-
   warning-block per Q1).
6. **`phases/phase2-planning.md`** — detail-doc replacing the stub
   (mirrors §4 in greater depth, plus edge cases and worked examples).
7. **`examples/example-meta-prompt.yaml`** — worked Phase-2 output
   for the EU-AI-Act intent (test case T1).
8. **Package** — `research-prompt-optimizer-v3.0.0-phase2.zip` +
   `.tar.gz` + manifest, drop-in installable per `ARCHIVE_NOTE.md`.

No code is written for Phase 2 itself — Phase 2 runs as Claude's
behaviour, guided by SKILL.md prose. Python lands in Phase 3.

---

*End of Phase 2 design plan v1.2 (FROZEN).*
