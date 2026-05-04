# Meta-Prompt Spec — YAML Schemas

> The contract between phases of the research-prompt-optimizer
> pipeline. Every phase reads and writes a YAML file conforming to one
> of the schemas below. **Schema = contract.** No prose hand-off.

This file defines three schemas — all live as of v3.2.0:

1. `research-prompt-intent` (schema_version 1.1) — the Phase 1 output
2. `research-prompt-plan` (schema_version 2.1) — the Phase 2 output
3. `research-prompt-render` (schema_version 3.1) — the Phase 3 output

All three schemas carry a normalised `provenance` block plus an
append-only `revisions[]` log (see §Schema 1, §Schema 2, §Schema 3
below for the canonical shape).

## Table of Contents

| § | Topic |
|---|-------|
| [Schema 1](#schema-1--research-prompt-intent-phase-1--phase-2) | Phase 1 → Phase 2 — intent.yaml shape + field validation rules |
| [Schema 2](#schema-2--research-prompt-plan-phase-2--phase-3) | Phase 2 → Phase 3 — meta-prompt.yaml; 15 sub-sections covering routing, modules, constraints, batches, seeds, slot fills, self-reflection, verification, warnings, validation, examples |
| [Schema 3](#schema-3--research-prompt-render-phase-3-output) | Phase 3 output — rendered Markdown with provenance frontmatter (§3.1) and document-body structure (§3.2) |
| [Backwards Compatibility](#backwards-compatibility-note) | Schema-version bump policy, migration notes |

**Reading order for implementers:** Schema 1 → Schema 2 → Schema 3,
then Backwards Compatibility for the bump rules. Schema 2 is the
largest section (15 sub-sections in fixed order); Schema 1 and 3
are short.

---

## Schema 1 — `research-prompt-intent` (Phase 1 → Phase 2)

**File location:** `/mnt/user-data/outputs/intent_<slug>.yaml`

**Status:** ✅ Live — Phase 1 produces files conforming to this
schema and writes them to disk after explicit user approval.

```yaml
# REQUIRED HEADER
schema_version: "1.1"                       # bumped at v3.2.0 (provenance block)
schema: research-prompt-intent
approved: true                              # always true; written only post-approval
approved_at: "2026-05-02T14:23:00+02:00"

# IDENTITY
slug: "eu-ai-act-saas-2026"                 # kebab-case ASCII, ≤ 60 chars
language: "de"                              # ISO-639-1; conversation language

# PROVENANCE — written by Phase 1, normalised across all skill outputs
provenance:
  created: "2026-05-02T14:23:00+02:00"      # ISO-8601 with timezone
  skill_version: "3.2.0"
  phase: "phase1"
  slug: "eu-ai-act-saas-2026"
  output_filename: "intent_eu-ai-act-saas-2026.yaml"
  category_signal: "B"                       # mirrored from routing_hints for cross-phase access
  previous_version: null                     # set if this file supersedes an earlier _vN
  revision_count: 0                          # incremented by append_revision()

# REVISIONS — append-only log of post-approval edits (empty at first write)
revisions: []
# Each entry:
#   { timestamp: ISO-8601, phase: str, field_path: str,
#     before: any, after: any, rationale: str | null }

# CORE INTENT — all fields required
intent:
  research_question: |
    Welche AI-Act-Pflichten treffen SaaS-Startups in der EU, und
    welche müssen bis Q3/2026 operativ implementiert sein?

  research_question_unpacked: |
    Nicht: allgemeine DSGVO-Pflichten, US-Pendants (Colorado AI Act,
    NIST AI RMF), Detailfragen zu High-Risk-Systemen außerhalb des
    Plattform-Use-Cases.

  audience: |
    Technischer Mitgründer mit Strategie- und Implementierungs-Mandat.
    Versteht Tech-Stack-Begriffe; braucht keine Jura-Einführung,
    aber ist kein Jurist.

  output_format: "comparison_matrix"
  # Enum: report | comparison_matrix | executive_summary | json_schema |
  #       table | hybrid_summary_with_appendix | other

  output_format_detail: |
    Matrix: Pflicht-Kategorie × Stichtag × Status (offen / in
    Arbeit / done) × Quelle. Tabelle als Markdown-Hauptergebnis,
    Quellenliste als Anhang.

  temporal_scope:
    from: "2024-08-01"
    to: "2027-08-01"
    rationale: |
      AI Act In-Force-Window (gestaffelte Anwendbarkeit
      08/2025 – 08/2027).

  depth: "standard"
  # Enum: surface | standard | exhaustive

  success_criterion: |
    Nach der Recherche kann ich entscheiden, welche AI-Act-Pflichten
    bis Q3/2026 implementiert sein müssen, und welche wir auf
    spätere Stichtage schieben können — mit konkretem
    Implementierungs-Backlog.

# OPTIONAL — set to null if user gives nothing
priors_and_constraints:
  known_priors: |
    Vermutung: High-Risk-System-Klassifikation greift für unseren
    Plattform-Use-Case nicht; nur Transparenz- und
    GPAI-Pflichten relevant.

  known_constraints: |
    Nur EU-Quellen, keine Paywall-Quellen. Vertraulichkeit:
    interner Use; keine Weitergabe an Dritte.

  domain_context: null

# DERIVED — auto-extracted by Claude, never asked
routing_hints:
  category_signal: "B"                     # A | B | C
  category_rationale: |
    Signale: 'Vergleichsmatrix' (output_format), 'compile/list'
    (research_question), bekannte-Antwort-pattern.

# OPTIONAL — populated only if scope drifted during the loop
scope_drift_log: []
# Each entry: { turn: int, addition: str, accepted: bool }

# OPTIONAL — populated only if a slot is unspecified by user choice
unspecified_slots: []
# Each entry: { slot: str, user_rationale: str }
```

### Field-by-Field Validation Rules

| Field | Rule |
|-------|------|
| `slug` | Regex `^[a-z0-9]+(-[a-z0-9]+)*$`, max 60 chars; ä→ae, ö→oe, ü→ue, ß→ss |
| `language` | ISO-639-1 two-letter code |
| `output_format` | One of the enum values OR `"other"` (then `output_format_detail` mandatory) |
| `temporal_scope.from`/`to` | ISO-8601 dates OR literal string `"unbounded"` (then `rationale` mandatory) |
| `depth` | `surface` · `standard` · `exhaustive` |
| `routing_hints.category_signal` | `A` · `B` · `C` · `null` (Phase 2 routes if null) |
| `approved` | Always `true` in a written file. Phase 2 refuses unsigned files. |

### What Phase 2 Will Read From This

Phase 2 inputs `intent.yaml` and decides:

- Category routing (uses `routing_hints` as a hint, makes its own call)
- Method selection (uses `priors` to e.g. prioritise M05 if priors exist)
- Constraint blocks (uses `known_constraints` and `domain_context`)
- Slot fills for templates (extracted from intent fields)
- Batch detection (from `output_format` and `research_question` shape)

Phase 2 does **not** modify `intent.yaml`. It produces a separate
`meta-prompt.yaml`.

---

## Schema 2 — `research-prompt-plan` (Phase 2 → Phase 3)

**File location:** `/mnt/user-data/outputs/meta-prompt_<slug>.yaml`

**Status:** ✅ Live — Phase 2 produces files conforming to this
schema and writes them after explicit user approval in the
Approval Loop (Phase 2.9).

### 2.1 Top-Level Structure

```yaml
# REQUIRED HEADER
schema_version: "2.1"                       # bumped at v3.2.0 (provenance block)
schema: research-prompt-plan
approved: true                              # always true — written only post-approval
approved_at: "2026-05-02T15:47:00+02:00"

# IDENTITY (pulled forward from intent)
slug: "eu-ai-act-saas-2026"
language: "de"
intent_ref: "intent_eu-ai-act-saas-2026.yaml"

# PROVENANCE — written by Phase 2, normalised across all skill outputs
provenance:
  created: "2026-05-02T15:47:00+02:00"      # ISO-8601 with timezone
  skill_version: "3.2.0"
  phase: "phase2"
  slug: "eu-ai-act-saas-2026"
  output_filename: "meta-prompt_eu-ai-act-saas-2026.yaml"
  category_signal: "B"                       # mirrored from routing.category for cross-phase access
  selected_methods: ["M01", "M02", "M06", "M13"]
  selected_framework_structural: "tidd-ec"
  cross_pollination_pair: ["a-into-b", "c-into-b"]
  previous_version: null                     # set if this file supersedes an earlier _vN
  revision_count: 0

# REVISIONS — append-only log of post-approval edits (empty at first write)
revisions: []
# Each entry:
#   { timestamp: ISO-8601, phase: str, field_path: str,
#     before: any, after: any, rationale: str | null }

# SECTIONS (each described in detail below)
routing: { ... }
modules: { ... }
constraint_blocks: [ ... ]
batches: [ ... ]
seed_queries: [ ... ]
expansion_axes_plan: { ... }
slot_fills: { ... }
self_reflection: { ... }                   # NEW v1.2 (Q6) — Phase-2's
                                            # own application of its
                                            # critical-thinking methods
verification_expectations: { ... }
warnings: [ ... ]                          # optional, populated if any
```

### 2.2 `routing` — Category & Framework Decisions

```yaml
routing:
  category: "b"                            # a | b | c
  category_source: "intent"                # "intent" (from category_signal)
                                            # | "auto" (Phase 2 scored)
                                            # | "user" (askuser disambiguation)
  category_rationale: |
    Cat-B: signals "obligations", "decompose", "structure" present in
    research_question_unpacked.

  framework: "risen"                       # risen | tidd-ec | co-star
                                            # | care | crispe | bespoke
  framework_source: "category_default"     # "category_default"
                                            # | "override_triggered"
                                            # | "user_override"
  framework_overrides_fired: 1             # int — how many trigger
                                            # conditions matched. v1.1
                                            # bespoke threshold: ≥2.
  bespoke_components: null                 # null unless framework == "bespoke"
                                            # then: { component: source_framework }
                                            # e.g., { task: "tidd-ec",
                                            #        steps: "risen", ... }
```

### 2.3 `modules` — Selected Module Set

```yaml
modules:
  agentic_framework: "react"               # always — anti-drift spine
  structural_framework: "risen"            # mirrors routing.framework

  methods:                                 # 3-5 + M13 (M13 always)
    - "m03"
    - "m05"
    - "m08"
    - "m13"
  methods_source: "category_default"       # how the set was assembled
                                            # | "category_default"
                                            # | "category_default + signal_swap"
                                            # | "user_override"

  replication:                             # mandatories + conditional M3
    - "m0-reflection"                      # always
    - "m1-constraint-blocks"               # always
    - "m2-restatement-checkpoint"          # always
    - "m3-per-batch-replication"           # only if any batch detected
    - "m4-pre-synthesis-verification"      # always

  cross_pollination:                       # locked at 2, paired by category
    - "a-into-b"                           # for category B: A→B + C→B
    - "c-into-b"
```

### 2.4 `constraint_blocks` — Hard Rules for the Executing Agent

```yaml
constraint_blocks:
  - id: "cb1_source_priority"
    title: "Source Priority"
    body: |
      Primary: EUR-Lex official text, Commission guidance, national
      supervisory authority statements.
      Secondary: peer-reviewed legal analysis, reputable sectoral press.
      Reject: vendor marketing, anonymous forum posts, AI-generated
      summaries without primary citation.

  - id: "cb2_temporal_scope"
    title: "Temporal Scope"
    body: |
      In-scope: post-2024 EU AI Act implementation phase. Prefer
      sources from August 2024 onward; older sources only for
      historical context.

  - id: "cb3_output_exclusions"
    title: "Output Exclusions"
    body: |
      Do not include legal advice disclaimer boilerplate.
      Do not use marketing language or unsupported superlatives.

  # cb4+ optional — only added in Approval edit branch
```

**Rules:**

- IDs are `cb<N>_<slug>`, ordered by N.
- `cb1`, `cb2`, `cb3` are always present (defaults from intent).
- Body is rendered prose, ready for direct insertion into the prompt.
- Plan View shows titles only; full bodies live here.

### 2.5 `batches` — Iteration Declarations

Phase 3 wraps any batch with M3 (per-batch replication mechanism).
Standard batches (M13, M0, M4) are always present; domain batches
appear only on detection.

```yaml
batches:
  # Domain batch (from 2.4 detection)
  - id: "b1_obligations"
    type: "domain"
    items: "agent_runtime_fill"            # if user chose "let Claude
                                            # detect at runtime"
    # OR
    # items: ["High-Risk Classification", "Transparency", "GPAI", ...]
    nested_methods: ["m07"]                # which methods loop per item

  # Standard batch — M13
  - id: "b_m13_axes"
    type: "standard"
    items: ["adjacent", "opposing", "abstraction", "orthogonal"]
    nested_methods: []

  # Standard batch — M0
  - id: "b_m0_checkpoints"
    type: "standard"
    items: ["10pct", "30pct", "50pct", "70pct", "90pct"]
    nested_methods: []

  # Standard batch — M4
  - id: "b_m4_verification"
    type: "standard"
    items: ["sources", "freshness", "contradictions", "gaps",
            "biases", "claims", "structure", "completeness"]
    nested_methods: []
```

**Rules:**

- `id` for domain batches: `b<N>_<term>`.
- `id` for standard: fixed (`b_m13_axes`, `b_m0_checkpoints`,
  `b_m4_verification`).
- `items` may be a list OR the literal string `"agent_runtime_fill"`
  if the user opted to defer enumeration to the executing agent.
- `nested_methods` lists method IDs that the executing agent runs
  *per item* in the batch.

### 2.6 `seed_queries` — Search Vocabulary

```yaml
seed_queries:
  - "EU AI Act high-risk classification"
  - "AI Act SaaS provider obligations"
  - "AI Act risk tier criteria"
  - "AI Act compliance timeline 2026"
  - "Commission guidance AI Act"

seed_queries_source: "approved"            # "approved" | "edited" | "decomposition_only"
```

**Rules:**

- 5–10 queries.
- Each query: 1–6 words (per `web_search` tool guidance).
- `source` records the user's choice in Phase 2.6 Q1.

### 2.7 `expansion_axes_plan` — M13 Four-Axis Plan

```yaml
expansion_axes_plan:
  adjacent: "AI Act high-risk system criteria; AI provider duties"
  opposing: "Why AI Act might NOT apply (out-of-scope cases, sector
             carve-outs)"
  abstraction: "EU regulatory landscape for AI (one level up)"
  orthogonal: "Operative Prozessauswirkungen — interner Workflow-Impact"

orthogonal_source: "user_selected"         # "user_selected" | "intent_provided"
```

**Rules:**

- All 4 axes always present.
- `adjacent`, `opposing`, `abstraction` auto-generated by Phase 2.
- `orthogonal` from bundled askuser Q2 (or from intent if
  `routing_hints.unconsidered_angle` was set in Phase 1).

### 2.8 `slot_fills` — Resolved Phase-2 Slots

Slots are organized by source module. Only `phase2_fill` and resolved
`phase2_fill_or_runtime` slots appear here. `agent_runtime_fill` slots
remain as `{{slot}}` in the rendered prompt.

```yaml
slot_fills:
  m13:
    target_concept: "EU AI Act compliance for B2B SaaS"
    source_intent_field: "intent.research_question_unpacked.subject"

  m03:
    decomposition_target: "AI Act obligations applicable to SaaS providers"
    source_intent_field: "intent.research_question_unpacked.object"

  cb1_source_priority:
    body_filled: true                      # boolean — was filled programmatically
    source: "intent.priors_and_constraints.source_priority"

  # ... one entry per resolved phase2_fill slot
```

### 2.9 Slot Type Distinction (v3.0 — KEY INNOVATION)

Each slot in a module's frontmatter has one of four types. Schema 2
records how each was handled:

| Type | When resolved | Where it appears |
|------|---------------|------------------|
| `phase2_fill` | At Phase 2.7 | In `slot_fills` |
| `phase2_fill_or_runtime` | Phase 2.7 if intent has it; else deferred | In `slot_fills` (resolved) OR left as `{{slot}}` in prompt |
| `agent_runtime_fill` | At runtime by executing agent | NOT in `slot_fills`; rendered as `{{slot}}` |
| `fill_from` | Programmatically from intent path | In `slot_fills` with `source_intent_field` |

This distinction is the v3.0 fix to v2.1's over-asking failure mode:
v2.1 collapsed all bracket placeholders into a single
"ask the user" pattern. v3.0 distinguishes the four resolution paths.

### 2.10 `self_reflection` — Phase-2 Self-Applied Critical Thinking (Q6 · v1.2)

This block records the output of the seven Phase-2 internal hooks
(see Phase-2 Design Plan §10). The block is **always present** but
its substantive content is gated by `intent.depth`:

```yaml
self_reflection:
  # ---- M07 — Contradiction Log (sub-phase 4.1) -----------------------
  contradictions:                          # list — empty if none found
    - field_a: "intent.depth=surface"
      field_b: "intent.output_format=exhaustive matrix"
      severity: "medium"                   # low | medium | high
      note: "surface depth conflicts with exhaustive output structure"
    # zero or more entries

  # ---- M05 + M01 — Routing Reflection (sub-phase 4.2) ----------------
  routing:
    prior:                                 # M05 Bayesian Prior
      category: "B"
      confidence: 0.7                      # float 0.0–1.0
      rationale: "structured taxonomy + known output template"
    falsification_check:                   # M01 Falsification
      counter_signals: []                  # list — phrases that would
                                           # falsify the routing
      escalated_to_askuser: false          # true if non-trivial
                                           # counter-signals forced
                                           # the askuser branch (4.2.4)

  # ---- M0 mini — Module Selection Reflection (sub-phase 4.3) ---------
  module_selection:
    fragile_choice: "M11 Assumption-Decay — trigger present but weak"
    non_default_activations:               # methods activated by signal
                                           # not category default
      - method: "M11"
        trigger: "intent.priors=well-established theory pre-2020"
        validity: "confirmed"              # confirmed | weak | spurious

  # ---- M13 self-app — Seed/Axis Reflection (sub-phase 4.6) -----------
  expansion_axes_plan_reflection:
    self_reflection_note: |
      Initial seed pushes toward technical/regulatory framing; the
      genuine opposite is socio-economic; abstraction-up is under-
      served vs. abstraction-down for this intent.
    auto_axes_adjusted: true               # true if reflection caused
                                           # the auto-generated axes
                                           # to be revised before askuser

  # ---- M03 — Pre-Mortem (sub-phase 4.8) ------------------------------
  pre_mortem:                              # list of 3 (standard) or
                                           # 5 (exhaustive) failure modes
    - "Cross-pollination A→C may dilute focus if intent.depth=standard"
    - "Orthogonal axis 'rechtlich' overlaps Constraint Block 1 — risk
       of redundant search budget"
    - "Bespoke synthesis (overrides=2) untested in this domain combo;
       monitor first run for structural drift"

  # ---- M4 6-item — Plan Integrity Check (sub-phase 4.8) --------------
  integrity_check:                         # all bools — overall is the
                                           # AND of all individual items
    react_partial: true
    m0_module: true
    m13_module: true
    cb1_authored: true
    cp_pair_exact: true                    # exactly 2 cross-pollinations
    no_unfilled_slots: true                # no <UNFILLED> markers in
                                           # phase2_fill slot results
    overall: "pass"                        # "pass" | "fail"

  # ---- Meta info -----------------------------------------------------
  hooks_active:                            # which depth-gated hooks ran
    M07_contradiction_log: true
    M05_bayesian_prior: true
    M01_falsification: true
    M0_mini_reflection: true
    M13_self_application: true
    M03_pre_mortem: true
    M4_integrity_check: true
  hooks_skipped_reason: null               # str — populated if depth=
                                           # "surface" (most hooks
                                           # skipped except M4)
                                           # e.g., "intent.depth=surface
                                           # only M4 integrity_check active"
```

**Depth-gated population rules:**

| Field | surface | standard | exhaustive |
|-------|---------|----------|------------|
| `contradictions` | empty list | populated | populated |
| `routing.prior` | `null` | populated | populated |
| `routing.falsification_check` | `null` | populated | populated |
| `module_selection` | `null` | populated | populated |
| `expansion_axes_plan_reflection` | `null` | populated | populated |
| `pre_mortem` | empty list | 3 items | 5 items |
| `integrity_check` | populated | populated | populated |
| `hooks_active.*` | M4 only | all 7 | all 7 |
| `hooks_skipped_reason` | populated | `null` | `null` |

**Rendering in plan view (§4.8):** the `self_reflection:` block sits
between `slot_fills_summary` and the constraint-blocks listing. By
default it renders **compact**: empty lists become single ✓-lines,
populated fields become 1–2 line summaries. Full content is available
in the YAML output but does not bloat the plan-view itself.

**Catalog reference:** see `catalog.yaml` → top-level
`self_applied_phase2_index` for the navigation map of which catalog
modules feed which hook.

### 2.11 `verification_expectations` — Self-Check for Phase 3

Phase 3 reads these to verify its own output:

```yaml
verification_expectations:
  expected_methods_count: 4                # M13 + 3 others (Cat-B default)
  expected_replication_count: 5            # M0, M1, M2, M3, M4
  expected_cross_pollinations: 2           # always 2
  expected_constraint_blocks: 3            # cb1, cb2, cb3
  expected_batches: 4                      # 1 domain + 3 standard
  mandatories_present:
    - "m13"                                # always
    - "react"                              # always
    - "m0-reflection"                      # always
    - "m1-constraint-blocks"               # always
    - "m2-restatement-checkpoint"          # always
    - "m4-pre-synthesis-verification"      # always
  language_warning_present: true           # true if intent.language != "en"
```

### 2.12 `warnings` — Surfaced Issues (Optional)

Populated only if Phase 2 emitted warnings during the run. Empty array
if clean.

```yaml
warnings:
  - id: "language_mix"
    severity: "info"
    message: "intent.language == 'de'; rendered prompt will mix EN
              templates with DE prose."
    surfaced_at: "phase2.8_plan_view"

  - id: "batch_items_deferred"
    severity: "info"
    message: "Domain batch 'b1_obligations' deferred to runtime by
              user choice; executing agent must enumerate."
    surfaced_at: "phase2.4_batch_detection"

  - id: "bespoke_framework"
    severity: "warning"
    message: "Framework synthesised from components. Review provenance
              in routing.bespoke_components."
    surfaced_at: "phase2.3_framework_selection"

  - id: "high_iteration_count"
    severity: "info"
    message: "Approval loop reached iteration 5; soft-cap hint shown
              once."
    surfaced_at: "phase2.9_approval_loop"
```

**Severity values:** `info` · `warning` · `error`.
- `error` would prevent write — Phase 2 fails closed.
- `warning` requires user acknowledgment in Plan View.
- `info` is logged but does not block.

### 2.13 Field Validation Rules

| Field | Rule |
|-------|------|
| `slug` | Must match intent file's slug; mismatch = error. |
| `schema_version` | `"2.0"` exactly. |
| `routing.category` | `a` · `b` · `c` (lowercase). |
| `routing.framework` | One of: `risen`, `tidd-ec`, `co-star`, `care`, `crispe`, `bespoke`. |
| `routing.bespoke_components` | Required iff framework == `bespoke`; null otherwise. |
| `modules.methods` | 4–6 entries; must include `m13`. |
| `modules.replication` | Must include `m0-reflection`, `m1-constraint-blocks`, `m2-restatement-checkpoint`, `m4-pre-synthesis-verification`. `m3-per-batch-replication` only if any batch present. |
| `modules.cross_pollination` | Exactly 2 entries; must be the locked pair for the chosen category. |
| `constraint_blocks` | At least cb1, cb2, cb3 present. |
| `batches` | At minimum 3 standard batches (m13_axes, m0_checkpoints, m4_verification). |
| `seed_queries` | 5–10 entries. |
| `expansion_axes_plan` | All 4 keys present, all non-empty strings. |
| `verification_expectations.mandatories_present` | Must contain the 6 mandatory module IDs. |

### 2.14 What Phase 3 Will Read From This

Phase 3 (`render.py`) reads `meta-prompt.yaml` and:

- Loads each module file referenced in `modules.*` from `catalog.yaml`
- Composes them in the order documented in Schema 3 below
- Substitutes slot fills from `slot_fills` (and leaves
  `agent_runtime_fill` slots as `{{slot}}`)
- Renders constraint blocks inline in CB1..N positions
- Wraps batch sections with M3 mechanism
- Validates output against `verification_expectations`
- Writes the final Markdown prompt

Phase 3 does **not** modify `meta-prompt.yaml`. It produces a separate
`research-prompt_<slug>.md`.

### 2.15 Worked Example

A complete Schema-2-conformant file for the EU-AI-Act intent is shipped
as `examples/example-meta-prompt.yaml` (~290 lines). It demonstrates:

- All required fields populated
- Domain batch with deferred items
- All 3 standard batches
- Full slot_fills section
- Language warning in `warnings[]`
- Verification expectations matching the Plan View shown to the user

Use it as the canonical reference when implementing Schema-2 readers
or writers.

---

## Schema 3 — `research-prompt-render` (Phase 3 output)

**File location:** `/mnt/user-data/outputs/research-prompt_<slug>.md`

**Status:** ✅ Live — Phase 3 (`render/render.py`) produces files
conforming to this schema.

This is the **final Markdown research prompt** that gets handed to the
external AI agent. It is not a YAML — it is a self-contained Markdown
file with YAML frontmatter (the rendered version of the plan,
projected into a structure the target AI can execute).

### 3.1 YAML Frontmatter (provenance + minimal context)

The frontmatter at the top of every rendered prompt carries the
normalised provenance block + the minimum context an external agent
needs to run the prompt without seeing intent.yaml or meta-prompt.yaml:

```yaml
---
schema_version: "3.1"                         # bumped at v3.2.0 (provenance block)
schema: research-prompt-render

# PROVENANCE — written by Phase 3, normalised across all skill outputs
provenance:
  created: "2026-05-02T16:02:00+02:00"        # render time
  skill_version: "3.2.0"
  phase: "phase3"
  slug: "eu-ai-act-saas-2026"
  output_filename: "research-prompt_eu-ai-act-saas-2026.md"
  category_signal: "B"
  selected_methods: ["M01", "M02", "M06", "M13"]
  selected_framework_structural: "tidd-ec"
  cross_pollination_pair: ["a-into-b", "c-into-b"]
  previous_version: null                       # set to research-prompt_<slug>.md when re-rendered
  revision_count: 0
  intent_ref: "intent_eu-ai-act-saas-2026.yaml"
  meta_prompt_ref: "meta-prompt_eu-ai-act-saas-2026.yaml"

# AGENT CONTEXT — what the executing agent needs to know
language: "de"
target_agent: "model-agnostic"
---
```

### 3.2 Document Structure (after frontmatter)

After the frontmatter described in §3.1, the body follows this fixed
order:

1. Title + "for-the-executing-AI" callout
2. Meta-Header (Category block + ReAct + structural framework — three inline expansions)
3. Research Objective
4. CONSTRAINT BLOCKS (0 first, then 1..N)
5. Critical-Thinking Methods (3–5 + M13)
6. Structural-framework component sections (e.g. RISEN: R, I, S, E, N)
7. Per-step Restatement Checkpoints + Reflection entries (inside Steps)
8. Cross-pollinated steps (Phase 2b — flagged as imports, inside Steps)
9. Batch procedures (M3 wraps any iteration block)
10. Pre-Synthesis Integrity Check (M4)
11. Synthesis schema (target output template)
12. Self-verification checklist for the executing AI (11 items)
13. End marker

The composition order is implemented in `render/render.py`. The spec
only fixes the **structure** of the output, not the assembly logic.

---

## Backwards Compatibility Note

Schema versions are bumped on every additive or breaking change.
v3.2.0 introduced the normalised `provenance` block and the
append-only `revisions` log across all three schemas:

- Schema 1: 1.0 → 1.1 (additive)
- Schema 2: 2.0 → 2.1 (additive)
- Schema 3: 3.0 → 3.1 (additive)

A reader written against the older schema versions will still find
the fields it expects (the old `created` / `created_by_skill` /
`approved` fields' content has moved into `provenance.*`, but
`approved` remains at the top level for backwards-compat checks).
Strict-mode readers should validate against `schema_version` and
fall back to the older schema if encountered.
