# Phase 2 — Planning (Detail Reference)

> **Companion to:** the Phase-2 section in `SKILL.md`.
> **Spec source of truth:** `phase2-design-plan.md` v1.2 (FROZEN
> 2026-05-02).
> **Purpose of this file:** edge cases, full algorithms, walked
> example. SKILL.md gives Claude the knobs; this file explains *why*
> each knob is positioned where it is and what to do when reality
> doesn't match the happy path.
>
> **v1.2 addition (Q6):** Phase 2 applies seven of its own catalog
> methods to its planning work. Each sub-phase below has a
> **🪞 Self-applied hook** subsection where applicable, explaining
> what the hook does, when it runs, and what it writes to
> `meta-prompt.self_reflection.*`. See `SKILL.md` → "Self-Applied
> Hooks Map" for the consolidated overview.
>
> **v3.2 addition:** the monolithic Soft-Cap-5 Approval Loop (§9 in
> this file) was replaced by three mini-gates in SKILL.md (Gate 1
> after 2.2, Gate 2 after 2.5, Gate 3 after 2.8). The §9 algorithm
> below remains as historical detail; live behaviour follows the
> SKILL.md gate model.

## Table of Contents

| § | Topic | Lines |
|---|-------|-------|
| 0 | [Phase 2 in One Picture](#0-phase-2-in-one-picture) — pipeline diagram + happy path | ~30 |
| 1 | [Sub-Phase 2.1 — Load & Validate Intent](#1-sub-phase-21--load--validate-intent) | ~36 |
| 2 | [Sub-Phase 2.2 — Category Routing](#2-sub-phase-22--category-routing) | ~45 |
| 3 | [Sub-Phase 2.3 — Module Selection](#3-sub-phase-23--module-selection) | ~86 |
| 4 | [Sub-Phase 2.4 — Batch Detection](#4-sub-phase-24--batch-detection) | ~56 |
| 5 | [Sub-Phase 2.5 — Constraint Block Authoring](#5-sub-phase-25--constraint-block-authoring) | ~56 |
| 6 | [Sub-Phase 2.6 — Seed Queries + Orthogonal Lens](#6-sub-phase-26--seed-queries--orthogonal-lens-bundled--v11) | ~77 |
| 7 | [Sub-Phase 2.7 — Slot Fill Collection](#7-sub-phase-27--slot-fill-collection) | ~50 |
| 8 | [Sub-Phase 2.8 — Render Plan View](#8-sub-phase-28--render-plan-view) | ~36 |
| 9 | [Sub-Phase 2.9 — Approval (legacy Soft-Cap-5; superseded by mini-gates in v3.2)](#9-sub-phase-29--approval-loop-hybrid--soft-cap--5--v11) | ~118 |
| 10 | [Sub-Phase 2.10 — Write meta-prompt.yaml](#10-sub-phase-210--write-meta-promptyaml) | ~29 |
| 11 | [Worked Example — EU AI Act](#11-worked-example--eu-ai-act) | ~103 |
| 12 | [Self-Applied Critical Thinking (Q6 · v1.2)](#12-self-applied-critical-thinking-q6--v12) | ~106 |
| 13 | [Hard Rules for Phase 2](#13-hard-rules-for-phase-2) | end |

**Reading order:** §0 for orientation; §1–§10 for the algorithm in
order; §11 to see it executed end-to-end on a real case; §12 for
the meta-cognitive layer; §13 for the invariants.

---

## 0. Phase 2 in One Picture

```
intent_<slug>.yaml  (Phase-1 output, frozen)
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│  Phase 2.1   Load & Validate Intent             (silent)         │
│  Phase 2.2   Category Routing                   (silent / 1 ask) │
│  Phase 2.3   Module Selection                   (silent)         │
│  Phase 2.4   Batch Detection                    (silent / 1 ask) │
│  Phase 2.5   Constraint Block Authoring         (silent)         │
│  Phase 2.6   Seed Queries + Orthogonal Lens     (1 BUNDLED ask)  │
│  Phase 2.7   Slot Fill Collection               (0–1 ask)        │
│  Phase 2.8   Render Plan View                   (silent)         │
│  Phase 2.9   Approval Loop                      (1+ ask)         │
│  Phase 2.10  Write meta-prompt.yaml             (silent)         │
└──────────────────────────────────────────────────────────────────┘
        │
        ▼
meta-prompt_<slug>.yaml  (Phase-2 output, ready for Phase-3 render)
```

**Total askuser turns** in a typical run: **3** (2.6 bundled + 2.7
slots + 2.9 approve). Best case: **2**. Edit-heavy: **5–6** with
soft-cap hint at iteration 5.

---

## 1. Sub-Phase 2.1 — Load & Validate Intent

### Algorithm

```
1. Read /mnt/user-data/uploads/intent_<slug>.yaml
   (or, if not in uploads, ask user for path).
2. Parse YAML.
3. Validate against Schema 1 (research-prompt-intent, v1.0):
   - All required slots present
   - schema_version == "1.0" (warn but continue if newer)
   - No null required fields
4. If invalid → emit a structured error, refuse to proceed.
   Error format:
     "Intent file fails validation:
        - Missing field: <path>
        - Invalid value at <path>: <reason>
      Please run Phase 1 again or fix the file manually."
```

### Edge cases

- **No intent file uploaded:** Ask the user to either upload one or
  re-run Phase 1. Do not attempt to fabricate intent fields.
- **Multiple intent files in uploads:** Ask user which one to load.
  Do not pick automatically (slug collisions are rare but real).
- **schema_version mismatch:** Soft-warn for forward versions, hard-
  fail for missing schema_version (intent file without version is
  not a valid Phase-1 output).

### Output of 2.1

In-memory dict: `intent` (validated, all fields present).

---

## 2. Sub-Phase 2.2 — Category Routing

### Algorithm

```
1. If intent.routing_hints.category_signal is set (Phase 1 already
   decided):
     → use it. Done. No askuser.

2. Otherwise (legacy or partial intents):
   Score categories A / B / C using research_question_unpacked +
   research_question:
     - A (Compare/Decide): triggers on "vs.", "compare", "best",
       "should I", "recommend", "decision", "pick", "choose"
     - B (Analyze/Decompose): triggers on "analyze", "decompose",
       "factors", "drivers", "structure", "breakdown", "what's
       in", "components"
     - C (Investigate/Synthesize): triggers on "why", "how", "what
       happened", "trace", "root cause", "explain", "history of"

3. If a single category scores ≥ 2× the runner-up → pick it. Done.

4. If two categories tie or are close (< 2×) → askuser:
     question: "Welche Routing-Kategorie passt am besten?"
     options: top-2 categories with one-line rationale each
              + "Beide sind relevant — bespoke synthesis nutzen"
```

### Edge cases

- **No category triggers fire** (rare; intent is too abstract):
  default to **C** (Investigate/Synthesize) — it's the most
  permissive and rarely produces actively wrong structure.
- **All three categories fire equally:** treat as Cat-A by default
  (Compare/Decide) because A's structural overhead is the lowest.
  Plan View will surface this for user override.
- **User picks "bespoke synthesis"** in the askuser: skip Cat-default
  framework and force the bespoke path in 2.3.

### Output of 2.2

`category` ∈ {a, b, c}. Stored in meta-prompt under `routing.category`.

---

## 3. Sub-Phase 2.3 — Module Selection

### 3.1 Mandatory modules (always selected)

These six load **regardless** of category, signals, or intent content:

| Module | Role | Reason it's mandatory |
|--------|------|----------------------|
| `methods/m13` | Adversarial Query Expansion | Prevents seed-query lock-in |
| `frameworks/react` | ReAct loop | The execution spine |
| `replication/m0-reflection` | Mid-run baseline reflection | Anti-drift |
| `replication/m1-constraint-blocks` | CB rendering | All hard rules sit here |
| `replication/m2-restatement-checkpoint` | Mandatory restatement | Anti-amnesia |
| `replication/m4-pre-synthesis-verification` | 8-item self-check | Quality gate |

### 3.2 Method selection (3–5 + M13)

```
1. Start with category default methods (catalog.yaml, per category):
     - A: M01 (falsification), M02 (steelman), M07 (decision matrix)
     - B: M03 (decomposition), M05 (multi-perspective), M08 (data triangulation)
     - C: M04 (genealogy), M06 (counterfactual), M11 (synthesis-of-syntheses)

2. Apply signal swaps from intent.routing_hints.signal_words:
     - "ethical", "should we" → swap in M09 (ethical reasoning)
     - "predict", "forecast" → swap in M10 (scenario modeling)
     - "consensus", "best practice" → swap in M12 (convergent evidence)

3. Hard cap: 5 methods (excluding M13). If signal swaps would push
   over 5, drop the lowest-scoring default to make room.

4. M13 is mandatory and always added.
```

### 3.3 Framework selection

```
1. Default per category:
     - A: TIDD-EC (Task / Inputs / Do / Don't / Examples / Constraints)
     - B: RISEN (Role / Input / Steps / Expectations / Narrowing)
     - C: CARE (Context / Action / Result / Example) or CRISPE depending
          on whether output is exploratory (CRISPE) or summary (CARE)

2. Override triggers — count how many of these fire:
     - "extract structured data" + "with hard constraints"  → +1
     - "for a specific audience" + "with a specific tone"    → +1
     - "produce N parallel outputs" + "consistent format"    → +1
     - "compare across dimensions" + "with explicit criteria" → +1

3. v1.1 LENIENT bespoke trigger:
     - If ≥2 override_triggers fire → bespoke synthesis.
     - Generate provenance map: which component from which catalog framework.
     - Emit warning in plan view: "Bespoke framework synthesised from
       components of: <list>. Review before approval."

4. If 0 or 1 override fires → use category default. No bespoke.
```

### 3.4 Cross-pollination (paired by category, locked at 2)

```
Per category, the cross-pollination pair is fixed (not user-chosen):
  - A → B-into-A + C-into-A
  - B → A-into-B + C-into-B
  - C → A-into-C + B-into-C

The user can swap one of the pair via the Approval edit branch in 2.9
("Edit modules → Cross-Pollination anpassen"), but Phase 2 never
asks proactively. This is deliberate: cross-pollination quality is
about category opposition, not about user preference.
```

### Output of 2.3

```yaml
modules:
  methods: ["m13", "<3-5 from selection>"]
  framework: "<one or 'bespoke'>"
  bespoke_framework_components: [...] # only if framework == "bespoke"
  replication: ["m0-reflection", "m1-constraint-blocks",
                "m2-restatement-checkpoint", "m4-pre-synthesis-verification"]
  cross_pollination: ["<2 fixed for category>"]
```

---

## 4. Sub-Phase 2.4 — Batch Detection

### Algorithm

```
1. Scan research_question + research_question_unpacked + output_format
   for batch markers:
     - "each <noun>" / "per <noun>" / "for every <noun>"
     - "across <plural>" / "compare <plural>"
     - "list of N <items>"
     - explicit count: "the 5 competitors", "13 regulations"

2. If marker found AND a concrete item list is enumerable from intent:
     → Generate batch automatically.
     → Add M3 (per-item replication) to replication modules.

3. If marker found BUT no item list enumerable:
     → 1 askuser:
         question: "Du sprichst von '<batch term>' — welche konkreten
                    Items sind das?"
         type: free_text follow-up (no enum, this is content)

4. If no marker found → no batch. M3 not added.

5. Standard batches (always added regardless of detection):
     - M13: 4-axis batch (adjacent, opposing, abstraction, orthogonal)
     - M0: 5-checkpoint batch (timed reflections)
     - M4: 8-item batch (pre-synthesis self-check)
```

### Edge cases

- **Multiple batch markers:** Each becomes its own batch. M3 still
  added once (it's a mechanism, not a per-batch loader).
- **Batch term too generic** ("each item"): treat as no enumerable
  list, ask user.
- **Batch list very long (50+):** add a warning in plan view that the
  prompt will instruct sequential processing, not parallel.

### Output of 2.4

```yaml
batches:
  - id: "b1_competitors"     # domain-specific, from detection
    items: [...]
  - id: "b_m13_axes"          # standard
    items: ["adjacent", "opposing", "abstraction", "orthogonal"]
  - id: "b_m0_checkpoints"    # standard
    items: ["10%", "30%", "50%", "70%", "90%"]
  - id: "b_m4_verification"   # standard
    items: ["sources", "freshness", "contradictions", "gaps",
            "biases", "claims", "structure", "completeness"]
```

---

## 5. Sub-Phase 2.5 — Constraint Block Authoring

### Algorithm

```
Three default blocks always authored:

  Block 1 — Source Priority:
    Render from intent.priors_and_constraints.source_priority +
    intent.priors_and_constraints.source_exclusions.
    Default if both empty: "primary > peer-reviewed > reputable
    secondary > everything else; reject anonymous forum posts as
    primary evidence."

  Block 2 — Temporal Scope:
    Render from intent.priors_and_constraints.temporal_scope.
    Default if empty: "no hard temporal constraint; prefer most
    recent within last 5 years for evolving topics, no preference
    for stable topics."

  Block 3 — Output Exclusions:
    Render from intent.output_format.must_exclude.
    Default if empty: "no marketing language, no unsupported
    superlatives, no fabricated citations."

Optional Block 4+ added in Approval edit branch only.
```

### Edge cases

- **Conflicting source priority** (intent says "prefer X" but exclusions
  forbid X): emit a warning in plan view, ask user to resolve in
  Approval.
- **Temporal scope is "all time" or "no constraint":** make it
  explicit in the rendered block — silence is interpreted as
  "everything is in scope".
- **Block 3 has 5+ exclusions:** still render as one block; long
  exclusion lists are good signal of high precision needed.

### Output of 2.5

```yaml
constraint_blocks:
  - id: "cb1_source_priority"
    title: "Source Priority"
    body: "<rendered prose>"
  - id: "cb2_temporal_scope"
    title: "Temporal Scope"
    body: "<rendered prose>"
  - id: "cb3_output_exclusions"
    title: "Output Exclusions"
    body: "<rendered prose>"
```

---

## 6. Sub-Phase 2.6 — Seed Queries + Orthogonal Lens (BUNDLED · v1.1)

### Algorithm

```
GENERATION PHASE (silent, before askuser):

  6.1 Seed queries (5–10):
    - Mechanical decomposition of research_question (always part of seed set)
    - Plus 2–4 LLM-creative seeds covering different facets
    - Each seed: 1–6 words (per web_search guidance)
    - Diversity check: no two seeds share more than 2 words

  6.2 M13 expansion axes — auto-generate three of four:
    - adjacent: synonyms / neighbouring sub-fields
    - opposing: failure case / opposite school of thought
    - abstraction: one level up OR down (direction picked from
      whether question is broad or narrow)
    - orthogonal: ASKUSER (highest-leverage, lock-in-prone)

BUNDLED ASKUSER (1 turn, 2 questions):

  Q1: "Diese Seed-Queries hat Claude aus deinem Intent abgeleitet —
       passt die Auswahl?"
       <render seed list, 5-10 lines, numbered>
       options:
         - "Approve seeds — los geht's"
         - "Edit seeds (free text)"
         - "Use decomposition only — keine LLM-Creativity, nur
            mechanische Zerlegung der research_question"

  Q2: "Welche orthogonale Linse hat in deiner Frage bisher niemand
       angesetzt?"
       options (auto-generated from lenses NOT in research_question):
         - 3 candidate lenses, e.g. "ökonomisch (Kosten/Nutzen)",
           "historisch (Entwicklung über Zeit)",
           "rechtlich (Compliance)"
         - "Andere — ich nenne (free text)"

POST-USER PROCESSING:

  Q1 == "Approve":          use as-generated.
  Q1 == "Edit seeds":       follow-up free-text turn for new list.
  Q1 == "Decomposition only":
                            re-generate seeds as mechanical
                            permutations only (no LLM creativity);
                            user sees them in plan view at 2.8.

  Q2 == auto-option:        use as orthogonal axis.
  Q2 == "Andere":           follow-up free-text turn.
```

### Edge cases

- **Intent already specifies orthogonal lens** in
  `routing_hints.unconsidered_angle`: skip Q2, use that value, note
  in plan view "orthogonal lens taken from intent".
- **All 3 auto-generated lens candidates feel weak:** prepend a 4th
  option "Auto-Pick erscheint schwach — lass uns auf eine
  bessere kommen (free text)".
- **Q1 picks "Decomposition only" but research_question is a single
  short sentence:** decomposition yields only 1–2 seeds; warn in
  plan view and offer to add 3 mechanical permutations as fallback.

### Output of 2.6

```yaml
seed_queries: ["...", "...", "..."]
expansion_axes_plan:
  adjacent: "..."
  opposing: "..."
  abstraction: "..."
  orthogonal: "..."  # from bundled askuser
```

---

## 7. Sub-Phase 2.7 — Slot Fill Collection

### Algorithm

```
1. Iterate selected modules. For each module:
     - Read frontmatter slot definitions (per §6 of design plan)
     - For each slot:
         type == "phase2_fill"             → must be resolved now
         type == "phase2_fill_or_runtime"  → resolve now if intent has
                                              the value, else defer to
                                              agent_runtime_fill
         type == "agent_runtime_fill"      → skip (left as {{slot}} in
                                              rendered prompt)
         type == "fill_from"               → resolve programmatically
                                              from intent path

2. For each phase2_fill slot, attempt to fill from intent:
     - Direct path lookup (e.g., intent.research_question)
     - Inferred path (e.g., intent.priors_and_constraints.X for
       constraint slots)

3. Collect all UNFILLED phase2_fill slots into a single askuser turn:
     question: "Diese Slots brauchen Werte — kannst du jeden kurz
                ausfüllen?"
     For each unfilled slot:
       - Emit slot_id + module + 1-line description + free-text input

4. Most well-formed intents produce 0 unfilled slots → askuser skipped.
```

### Edge cases

- **Slot is phase2_fill but value can be inferred from another
  resolved slot:** infer it, log inference in plan view, do not ask
  user. Example: `m13.target_concept` can be inferred from
  `intent.research_question_unpacked.subject`.
- **User skips a required slot in the batched askuser:** re-ask only
  for that one slot (don't re-bundle the others).
- **Slot-fill turn has 5+ unfilled slots:** that's a Phase-1 quality
  problem; emit a soft warning in plan view that intent capture was
  incomplete.

### Output of 2.7

All phase2_fill slots resolved (in-memory dict
`slot_fills: {slot_id: value}`).

---

## 8. Sub-Phase 2.8 — Render Plan View

### Algorithm

```
1. Compose the plan view as compact YAML preview:
     - 40–80 lines target
     - Sections: language warning (if non-EN), category, modules,
       constraint_blocks (titles only), batches (counts only),
       seed_queries, expansion_axes, slot_fills
     - Hide: full module content, full slot definitions, internal IDs

2. v1.1 LANGUAGE WARNING — if intent.language != "en":
     Prepend the block from modules/partials/language-warning.md
     verbatim (paste-ready, not generated).

3. Emit to chat as a fenced ```yaml block.
```

### Edge cases

- **Plan view exceeds 80 lines:** still emit, but add a summary line
  at top: "Plan ist großer als üblich (X Zeilen). Häufiger Grund:
  viele constraint_blocks oder bespoke framework."
- **Bespoke framework selected:** prepend a bold note above plan view:
  "⚠ Bespoke framework synthesised — review components in §framework."
- **No askuser in the next step (everything resolved):** emit plan view
  immediately followed by the Approval askuser; no intermediate
  prose.

### Output of 2.8

Plan view rendered to chat. No file written yet.

---

## 9. Sub-Phase 2.9 — Approval Loop (Hybrid · Soft Cap @ 5 · v1.1)

### Algorithm — Top-Level Dispatch

```
ITERATION 1..N (no hard cap):

  TOP-LEVEL ASKUSER:
    question: "Plan stimmt — oder welche Sektion willst du editieren?"
    options:
      - "Approve — Plan in meta-prompt.yaml schreiben"
      - "Edit modules"
      - "Edit constraint blocks"
      - "Edit search seed / expansion axes"
      - "Edit other (free text)"

  Branch to corresponding sub-handler.
  After any edit: re-render plan view (2.8) and re-loop.

SOFT CAP @ ITERATION 5 (one-time hint):

  When entering iteration 5 (i.e., user is about to make their 5th
  edit), prepend to the approval question:

    "Hinweis: 5. Edit-Zyklus. Echte Bedenken oder Detail-Tweaks?
    Falls Tweaks: lass uns approven, du kannst das fertige Markdown
    danach schneller direkt editieren als hier in weiteren
    Plan-Zyklen."

  This is a HINT, not a block. Hint fires exactly once.
```

### Sub-Handler — "Edit modules"

```
SUB-ASKUSER:
  question: "Welcher Modul-Bereich?"
  options:
    - "Methods tauschen"
        → multi_select over 13 methods, current selection prefilled,
          M13 always checked + locked.
    - "Framework überschreiben"
        → single_select over 5 catalog frameworks + "bespoke synthesis".
    - "Cross-Pollination anpassen"
        → multi_select over 6 CPs, current 2 prefilled,
          must end with exactly 2 selected (validated).
    - "Edit other (free text)"
        → fall through to free-text turn.
```

### Sub-Handler — "Edit constraint blocks"

```
SUB-ASKUSER:
  question: "Welcher Block?"
  options:
    - "Block 1 (Source Priority) editieren"
        → free-text turn for new content, replaces body.
    - "Block 2 (Temporal Scope) editieren"
        → free-text turn for new content, replaces body.
    - "Block 3 (Output Exclusions) editieren"
        → free-text turn for new content, replaces body.
    - "Neuen Block 4+ hinzufügen"
        → free-text turn:
            "Titel + Inhalt für den neuen Block?"
    - "Edit other (free text)"
        → free-text turn.
```

### Sub-Handler — "Edit search seed / expansion axes"

```
SUB-ASKUSER:
  question: "Was?"
  options:
    - "Seed-Query hinzufügen"
        → free-text turn for new query (1-6 words).
    - "Seed-Query entfernen"
        → multi_select on current list, drop selected.
    - "Orthogonal axis ersetzen"
        → free-text turn for new orthogonal lens.
    - "Adjacent / Opposing / Abstraction axis ersetzen"
        → sub-question: which axis? → free-text turn for new value.
```

### Sub-Handler — "Edit other (free text)"

```
DIRECT FREE-TEXT TURN:
  question: "Schreib mir, was du editieren willst — ich rendere den
             Plan neu."

  Parse user response:
    - If response references a module → route to "Edit modules"
    - If response references CB → route to "Edit constraint blocks"
    - If response references seeds/axes → route to "Edit search..."
    - Otherwise: best-effort interpret + rerender + ask user
      "passt das jetzt?"
```

### Edge cases

- **User picks an edit option but the resulting edit yields no change**
  (e.g., picks the same item from prefill): treat as no-op, do NOT
  count toward the 5-iteration soft cap.
- **User picks "Approve" but plan view has open warning** (e.g.,
  conflicting source priority from 2.5): one-time confirmation
  "Es gibt eine ungelöste Warnung in CB1 — trotzdem approven?".
- **User abandons the loop** (long silence): no automatic action;
  Phase 2 simply does not write the meta-prompt. Re-engaging
  resumes from current iteration.

### Output of 2.9

`approved == true` and final plan ready for write.

---

## 10. Sub-Phase 2.10 — Write meta-prompt.yaml

### Algorithm

```
1. Compose final YAML per Schema 2 (see meta-prompt-spec.md):
     - All Phase 2 outputs serialised
     - schema_version: "2.0"
     - created_at: ISO-8601 timestamp
     - phase: "phase2"
     - intent_ref: original intent file path or slug

2. Write to /mnt/user-data/outputs/meta-prompt_<slug>.yaml
     - Use intent slug as filename
     - If file exists, version-suffix: meta-prompt_<slug>_v2.yaml etc.

3. Call present_files with the new file.

4. Emit a one-line confirmation:
     "Plan v<N> in meta-prompt_<slug>.yaml geschrieben.
      Phase 3 (Render) startet, sobald du sie auslöst."
```

### Output of 2.10

File written, presented to user. Phase 2 complete.

---

## 11. Worked Example — EU AI Act

Walking through the EU-AI-Act intent example end-to-end:

### Inputs (from `examples/example-intent.yaml`)

```yaml
slug: eu-ai-act-saas-2026
language: de
research_question: "Welche EU-AI-Act-Pflichten gelten für mein
                   B2B-SaaS-Produkt im Compliance-Risk-Scoring?"
research_question_unpacked:
  subject: "EU-AI-Act compliance obligations"
  object: "B2B SaaS product, compliance risk scoring use case"
  scope: "operational requirements 2026"
routing_hints:
  category_signal: "b"  # decompose obligations
  signal_words: ["compliance", "obligations", "risk", "categorise"]
priors_and_constraints:
  source_priority: ["EUR-Lex official text", "Commission guidance",
                    "national supervisory authority statements"]
  temporal_scope: "post-2024 implementation phase"
  source_exclusions: ["vendor marketing", "anonymous forum posts"]
output_format:
  must_include: ["per-obligation table", "risk-tier classification",
                 "implementation timeline"]
  must_exclude: ["legal advice disclaimer boilerplate", "marketing"]
```

### Phase 2 trace

**2.1 Load:** validates clean, all required fields present.

**2.2 Routing:** `category_signal: "b"` from intent → category = B
(Analyze/Decompose). No askuser.

**2.3 Module selection:**
  - Methods (Cat-B defaults + M13): M03, M05, M08, M13. (4 methods)
  - Signal "compliance" + "obligations" + "categorise" don't trigger
    swaps → no swap.
  - Framework: Cat-B default = RISEN. Override triggers checked:
    - "extract structured data" + "with hard constraints" → +1
      (per-obligation table is structured + temporal_scope is hard)
    - Other triggers don't fire → 1 trigger total < 2 → no bespoke.
    - Framework = RISEN.
  - Replication: M0, M1, M2, M4 (mandatory) + M3 (batches detected,
    see 2.4).
  - Cross-pollination: B → A-into-B, C-into-B (locked pair).

**2.4 Batch detection:**
  - Marker: "per-obligation table" in must_include → batch over
    obligations.
  - Item list NOT enumerable from intent (obligations not listed)
    → askuser:
      "Du sprichst von 'Obligations' — welche konkreten Items sind
       das? (Frei reinschreiben, eine Liste oder 'lass Claude im Run
       erkennen')"
  - User answers: "lass Claude im Run erkennen" → batch declared
    with `items: "agent_runtime_fill"` placeholder.
  - M3 added.
  - Standard batches added: M13 (4 axes), M0 (5 checkpoints), M4
    (8 items). Total batches: 4.

**2.5 Constraint blocks:**
  - CB1 (Source Priority): rendered from priors. 3-tier ordering.
  - CB2 (Temporal Scope): rendered as "post-2024 EU AI Act
    implementation phase".
  - CB3 (Output Exclusions): rendered as "no legal advice disclaimer
    boilerplate, no marketing language".

**2.6 Seeds + Orthogonal (BUNDLED askuser):**
  - Generated seeds: ["EU AI Act high-risk classification",
                       "AI Act SaaS provider obligations",
                       "AI Act risk tier criteria",
                       "AI Act compliance timeline 2026",
                       "Commission guidance AI Act"]
  - Generated orthogonal candidates: ["ökonomisch
    (Compliance-Kosten/ROI)", "operativ (interne
    Prozessauswirkungen)", "wettbewerblich (Marktzugang)"]
  - Q1: User approves seeds.
  - Q2: User picks "operativ".

**2.7 Slot fills:**
  - All phase2_fill slots resolvable from intent → 0 unfilled.
  - askuser skipped.

**2.8 Plan view:**
  - Language warning prepended (intent.language = "de").
  - Plan view rendered, ~55 lines.

**2.9 Approval:**
  - User clicks "Approve" on iteration 1.

**2.10 Write:**
  - `meta-prompt_eu-ai-act-saas-2026.yaml` written, presented.

**Total askuser turns:** 3 (2.4 batch list + 2.6 bundled + 2.9
approve). One above the typical case because intent didn't enumerate
the obligation list — that's fine, it's a real ambiguity worth
asking about.

---

## 12. Self-Applied Critical Thinking (Q6 · v1.2)

Phase 2 applies the same critical-thinking methods to its own work
that it embeds in generated prompts. The skill demands what it itself
practices.

Seven hooks are anchored at the sub-phases shown above. Each hook is
silent unless it surfaces a finding (contradiction, falsifying signal,
fragility, pre-mortem risk, integrity violation). All findings land
in `meta-prompt.self_reflection`.

### 12.1 Hook map

| # | Sub-phase | Method | Hook role | Output field |
|---|-----------|--------|-----------|--------------|
| 1 | 2.1 Load | M07 Contradiction Log | Scan intent for internal inconsistencies (depth ↔ output, scope ↔ priors, etc.) | `self_reflection.contradictions[]` |
| 2 | 2.2 Routing | M05 Bayesian Prior | Write down prior + confidence BEFORE the cascade runs | `self_reflection.routing.prior` |
| 3 | 2.2 Routing | M01 Falsification | AFTER the cascade decides, run one counter-pass; escalate to askuser if non-trivial counter-signals | `self_reflection.routing.falsification_check` |
| 4 | 2.3 Modules | M0 Mini-Reflection (2-Q) | Surface fragile method choices and trigger validity | `self_reflection.module_selection` |
| 5 | 2.6 Seeds | M13 Self-Application | Reflect on auto-axis direction BEFORE generation; adjust if lock-in detected | `self_reflection.expansion_axes_plan_reflection` |
| 6 | 2.8 Plan-View | M03 Pre-Mortem | Generate top-3 (or top-5 if `depth=exhaustive`) failure modes for the plan | `self_reflection.pre_mortem[]` |
| 7 | 2.8 Plan-View | M4 Pre-Synthesis Integrity | 6-item plan completeness check; blocks rendering on fail | `self_reflection.integrity_check` |

### 12.2 Depth-scaling rules

```
intent.depth == "surface"      → Hook 7 only (M4 integrity check).
                                  All other hooks skipped.
                                  Rationale: surface intents are quick;
                                  meta-reflection overhead would dwarf
                                  the actual research budget.

intent.depth == "standard"     → All 7 hooks active.
                                  M03 Pre-Mortem produces 3 items.

intent.depth == "exhaustive"   → All 7 hooks active.
                                  M03 Pre-Mortem may produce 5 items.
```

When hooks are skipped, `self_reflection.hooks_skipped_reason` is
populated with a one-line explanation (e.g., `"intent.depth=surface
— only M4 integrity_check active"`).

### 12.3 Blocking vs. non-blocking hooks

Most hooks are **non-blocking** — they record findings but do not stop
Phase 2 progression. The user sees findings in the plan view and
decides during Approval whether to act on them.

Two exceptions:

- **M01 Falsification (Hook 3)** — if non-trivial counter-signals are
  found AND the original cascade did not escalate to askuser, the hook
  forces the askuser branch. The user explicitly confirms or overrides
  the routing.
- **M4 Integrity Check (Hook 7)** — if `overall: "fail"`, plan view
  rendering is blocked. Phase 2 enters a self-correction loop:
  identify the failed item, attempt automatic repair (e.g., add
  missing mandatory module), re-run the integrity check. If three
  self-correction attempts fail, surface the failure to the user as a
  hard error before approval.

### 12.4 Compact rendering in plan view

The `self_reflection:` block sits between `slot_fills_summary` and the
constraint-blocks listing. Renders **compact by default**:

- Empty list / null → single ✓-line: `🪞 M07 contradictions: ✓ none`
- Populated → 1-2 line summary: `🪞 M07 contradictions: 1 low-severity (depth↔output)`
- Failed integrity → expanded: full 6-item table with ✗ markers

Full content remains available in the YAML output but does not
inflate the plan view itself. User can always request "show me the
full self_reflection" via the Approval edit-loop.

### 12.5 Why these 7, not more

Other catalog methods were considered and rejected for Phase-2-internal use:

- **M02 Steelmanning** — overlap with M01 Falsification; Phase 2 has
  no "mainstream position" to bekämpfen
- **M04 Contrast Classes** — module selection is not claim-evaluative
- **M06 Source Triangulation** — `intent.yaml` is single-source by
  construction
- **M08 What Would Change My Mind** — overlap with M01
- **M09 Red Team** — overlap with M03 Pre-Mortem
- **M10 First-Principles Decomposition** — `research_question_unpacked`
  from Phase 1 already provides this
- **M11 Assumption-Decay** — Phase 2 is single-shot, no decay dimension
- **M12 Base-Rate Anchoring** — Phase 2 has no numeric claims

These could be added in a future iteration if Real-Use experience
shows specific gaps the current 7 hooks don't cover.

### 12.6 Catalog cross-reference

The full hook specification per module lives in `catalog.yaml`:

- Each affected module entry has `self_applicable: true`
- Each affected module entry has a `self_applied_phase2:` sub-section
  with `sub_phase`, `hook_role`, `depth_active`
- Top-level `self_applied_phase2_index:` enumerates all 7 hooks for
  programmatic discovery

---

## 13. Hard Rules for Phase 2

These are **invariants** — Phase 2 must never violate them:

1. **No code execution.** Phase 2 is Claude reasoning over the
   intent + catalog. Python lands only in Phase 3 (Render).

2. **No fabricated intent values.** If a value is missing from
   intent and can't be inferred or asked-about, fail the sub-phase
   with a clear error pointing to the missing slot.

3. **M13 is always selected.** No edit branch can deselect it.
   Anti-lock-in is a foundational guarantee, not a preference.

4. **Cross-pollination pair is locked at 2.** User can swap one of
   the pair, never reduce below 2.

5. **Plan view is not the meta-prompt.** Plan view is a compact
   preview. The actual meta-prompt.yaml has full content. Approval
   approves the plan; rendering uses the full data.

6. **No write before approval.** `meta-prompt_<slug>.yaml` is only
   written at 2.10 after explicit approve. Edit iterations do NOT
   produce intermediate files.

7. **Soft cap is a hint, not a block.** User may continue past
   iteration 5. The hint fires exactly once.

8. **Bundled askuser is one tool call.** Q1 and Q2 of 2.6 must be
   issued in a single `ask_user_input_v0` call with two questions in
   the questions array — not two separate calls.

---

*End of Phase 2 detail reference. Build artefacts under `modules/`,
schema in `meta-prompt-spec.md` Schema 2, design rationale in
`phase2-design-plan.md` v1.1.*
