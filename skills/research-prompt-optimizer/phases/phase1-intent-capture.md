# Phase 1 — Intent Capture · Detail Reference

> Load this file from SKILL.md only when the conversation hits an edge
> case in Phase 1: ambiguity that the simple loop cannot resolve, a
> contradiction between slots, a user who pushes back on a question, or
> a slot whose mapping to a question is not obvious.
>
> For straightforward intent capture the SKILL.md algorithm alone is
> sufficient. Don't pre-load this file unless needed — context overload
> is the enemy this skill is designed to fight.

## Table of Contents

0. [The Loop — Algorithm](#0-the-loop--algorithm) — the four-step
   pseudocode (EXTRACT / ASK / CONFIRM / EXIT) that drives Phase 1.
1. [Slot-to-Question Mapping](#1-slot-to-question-mapping) — how each
   intent slot maps to one or more askuser questions, with worked
   options.
2. [Loop-Termination Examples](#2-loop-termination-examples) — three
   worked walkthroughs from raw user input to approved intent.yaml.
3. [Anti-Patterns Specific to Phase 1](#3-anti-patterns-specific-to-phase-1)
4. [Edge Cases](#4-edge-cases) — contradictions, scope drift, user
   refusal, mid-loop edits, language switching.
5. [The Confirm-Turn — Format Specification](#5-the-confirm-turn--format-specification)
6. [Why This Design](#6-why-this-design) — the rationale behind the
   askuser-loop choice, file-first principle, and 100% clarity bar.

---

## 0. The Loop — Algorithm

The thin SKILL.md gives a one-line summary of Phase 1's loop. The
full pseudocode lives here:

```
1. EXTRACT  — parse user input; mark each slot filled / partial / missing.

2. ASK (file-first) — while any required slot is partial/missing:
     a. Write intent-status_<slug>.md (✓/⚠/✗ groups + intent so far)
        via io_helpers.write_status_view(). present_files.
     b. Group ≤ 3 thematically-coherent slots; ask_user_input_v0 with
        1–3 questions (HARD CAP 3). single_select where enum exists;
        free-text only for genuinely open slots.
     c. Re-extract after each response; surface contradictions in
        next status view.

3. CONFIRM — once all required slots filled:
     a. Write intent_<slug>.yaml + final status view. present_files.
        DO NOT print YAML in chat.
     b. askuser single_select: "Approve" / "Edit <slot>" / "Edit other".
     c. On "Approve": mark approved, fill provenance via
        io_helpers.make_provenance, present_files, proceed to Phase 2.
     d. On "Edit X": append_revision if file already exists; loop to ASK.

4. EXIT — intent_<slug>.yaml on disk with approved=true AND user chose
   Approve AND present_files called on final intent + status view.
```

The loop's invariant: every iteration leaves the workspace in a
state where the user can stop, read the status view, and resume
later. The status-view file is the user's window into the loop's
reasoning.

---

## 1. Slot-to-Question Mapping

For each required slot, the canonical phrasing of the question and the
preferred `ask_user_input_v0` shape.

### `research_question`

**Default:** the user already states it explicitly. Skip the question.

**Ambiguous case** ("hilf mir bei der KI-Verordnung"):

```
type: "single_select"  -- but use multi_select if the user signals breadth
question: "Welche Frage steht für dich im Zentrum?"
options:
  - "Welche Pflichten treffen mein Unternehmen konkret"
  - "Wie unterscheidet sich der AI Act von der DSGVO"
  - "Welche Übergangsfristen und Stichtage gelten wann"
  - "Etwas anderes — ich formuliere selbst"
```

If "Etwas anderes" is picked, follow up with a free-text question.

### `research_question_unpacked`

**This slot exists to catch the gap between what was asked and what was
meant.** Always confirm via free-text after `research_question` is set,
unless the user's original phrasing is already unambiguous and bounded.

```
question: >-
  In einem Satz: was ist das Recherche-Ergebnis NICHT? Welche benachbarte
  Frage soll explizit ausgeschlossen sein?
```

This is the slot that prevents Phase 2 from researching the wrong thing
"because it sounded close enough".

### `audience`

```
type: "single_select"
question: "Wer ist die primäre Leserschaft des Endergebnisses?"
options:
  - "Technische Geschäftsführung (Strategie, kein Jura/Detail-Stack)"
  - "Fachexperte (volle Tiefe, Begriffe selbstverständlich)"
  - "Operative Umsetzung (To-do-Liste, Checklisten, Templates)"
  - "Externe (Investor, Aufsicht, Kunde) — Tonalität anpassen"
```

Adjust options to the domain. The four options above fit a
business/regulatory ask; for academic literature substitute "fellow
researcher / supervisor / public / journal review".

### `output_format`

```
type: "single_select"
question: "In welcher Form soll der Deep-Research-Agent das Ergebnis liefern?"
options:
  - "Erzählender Report (Fließtext, Quellen, Synthese)"
  - "Strukturierte Tabelle / Vergleichsmatrix"
  - "Executive Summary + tieferer Anhang"
  - "JSON / strukturiertes Daten-Schema"
  - "Etwas anderes — ich beschreibe"
```

If "etwas anderes": free-text follow-up, then map to a concrete shape.

### `temporal_scope`

```
type: "single_select"
question: "Welcher Zeitraum gilt für die Recherche?"
options:
  - "Nur aktueller Stand (heute zurück bis ~6 Monate)"
  - "Letztes Jahr (rolling)"
  - "Konkrete Periode — ich gebe Daten an"
  - "Unbeschränkt (mit Rationale)"
```

If "konkrete Periode" → free-text follow-up for `from` and `to`.
If "unbeschränkt" → free-text follow-up for the rationale (this is
required because the rendered prompt's CONSTRAINT BLOCK 2 needs it).

### `language`

```
type: "single_select"
question: "Sprache des erzeugten Prompts?"
options:
  - "Deutsch (Default)"
  - "English"
  - "Andere — bitte nennen"
```

Default to the user's conversation language. Only ask if the
conversation has been mixed.

### `depth`

```
type: "single_select"
question: "Wie tief soll der Agent gehen?"
options:
  - "Surface — schneller Überblick (5–15 min Agent-Laufzeit)"
  - "Standard — gründlich, aber zielgerichtet (20–40 min)"
  - "Exhaustive — alle Quellen, alle Verzweigungen (60+ min)"
```

### `success_criterion`

**Always a free-text question.** This slot is the single most
load-bearing — it is the user's explicit success-test that Phase 4 of
the rendered prompt will check against.

```
question: >-
  Vervollständige den Satz: "Ich werde wissen, dass die Recherche
  erfolgreich war, wenn ..."
```

If the user gives a vague answer ("wenn ich gut informiert bin"), push
back with one follow-up that demands operational specificity:
*"Operativ: woran konkret? Eine konkrete Entscheidung, die du danach
treffen kannst? Eine konkrete Liste, die danach abgehakt ist?"*

### `known_priors` (optional)

```
question: >-
  Hast du eine Vermutung, eine Hypothese oder einen Bauchverdacht zur
  Antwort? (Wenn ja: schreibe sie auf — sie wird im Prompt als
  expliziter Bayesian Prior verankert, nicht als Antwort.)
```

If the user says "nein, ich weiß es nicht" → set `known_priors: null`.
Do **not** invent a prior.

### `known_constraints` (optional)

```
type: "multi_select"
question: "Gibt es Einschränkungen, die der Agent kennen muss?"
options:
  - "Nur EU-Quellen / nur DACH-Kontext"
  - "Keine Paywall-Quellen"
  - "Vertraulichkeit / kein Output an Dritte"
  - "Konkrete Quellen-Ausschlüsse — ich nenne sie"
  - "Keine Einschränkungen"
```

If "konkrete Ausschlüsse" → free-text follow-up.

### `domain_context` (optional)

Free-text. Asked only if the topic is technical/specialised and the
research question alone would not give an outsider AI enough context to
search effectively.

```
question: >-
  Gibt es ein paar Sätze Domänen-Kontext, die ein fremder Agent ohne
  dein Vorwissen nicht erraten könnte? (z. B. spezielle Begriffe,
  Branchenlogik, Vorgeschichte des Themas.)
```

### `category_signal` (derived, never asked)

Auto-extracted by Claude from the input + answers. Never put this slot
to the user. The signals:

| Found in input | → Signal |
|---|---|
| "warum scheitert", "find gaps", "unbekannte Ursache", "explore", "hypothesize" | A — Exploration |
| "vergleichen", "Liste aller", "Marktanalyse", "Due Diligence", "compile" | B — Extraction |
| "laufendes Monitoring", "über Monate verfolgen", "incremental updates" | C — Lifecycle |
| no clear signal | leave empty, Phase 2 will route |

This is a hint for Phase 2, not a binding decision.

---

## 2. Loop-Termination Examples

### Example A — Well-specified input, two batches

User: *"Erstell mir einen Deep Research Prompt zur EU-AI-Act-Compliance
für SaaS-Startups, gerichtet an meinen technischen Mitgründer, als
Vergleichsmatrix der Pflichten gegen die Stichtage 2025–2027. Tief
genug, dass wir danach wissen, was wir bis Q3/2026 implementiert haben
müssen."*

Filled from input alone:
- `research_question` ✓
- `audience` ✓ (technischer Mitgründer)
- `output_format` ✓ (Vergleichsmatrix)
- `temporal_scope` ✓ (2025–2027)
- `success_criterion` ✓ (operativ konkret)
- `language` ✓ (de — conversation language)
- `category_signal` → B (auto)

Missing: `research_question_unpacked`, `depth`, `known_priors`,
`known_constraints`, `domain_context`.

**Batch 1** (1 question): unpack the question.

> *"Damit ich nicht die falsche Nachbarfrage recherchieren lasse: was
> soll EXPLIZIT NICHT Teil der Antwort sein? (z. B. allgemeine
> DSGVO-Pflichten, US-Pendants wie Colorado AI Act, etc.)"*

**Batch 2** (3 questions, single_select): depth + priors + constraints.

> *"Drei knappe Punkte:"*
> Q1: Wie tief? [surface / standard / exhaustive]
> Q2: Hast du schon eine Vermutung welche Pflicht-Kategorie kritisch ist? [single_select with named categories + "keine Vermutung"]
> Q3: Quellen-Einschränkungen? [multi_select wie oben]

`domain_context` wird nicht gefragt, weil EU AI Act + SaaS für jeden
Agent erschließbar ist.

**Confirm-Turn:** zeige die 30-Zeilen-YAML-Vorschau, frage Approve / Edit.

→ 3 askuser-Turns total. Phase 1 done.

### Example B — Vague input, four batches

User: *"Ich brauche Hilfe bei meiner Recherche zu KI-Tools."*

Almost nothing filled. Loop:

**Batch 1**: research_question + audience.
**Batch 2**: research_question_unpacked + output_format.
**Batch 3**: temporal_scope + depth + success_criterion.
**Batch 4** (only if needed): priors + constraints.
**Confirm-Turn**.

→ 5 turns. Vague inputs cost more turns. That's the deal.

### Example C — Contradiction surfaces mid-loop

User in Batch 1: *"Audience ist mein Mitgründer, technisch."*
User in Batch 2 about output_format: *"Soll wie ein Vortrag für unseren
nicht-technischen Investor klingen."*

→ Contradiction detected. Surface explicitly:

> *"Kurzer Check: in Batch 1 hast du 'technischer Mitgründer' als
> Audience genannt, jetzt 'nicht-technischer Investor' als Tonalität.
> Was hält? Drei Optionen:"*

```
options:
  - "Audience = Investor (Tonalität non-technisch)"
  - "Audience = Mitgründer (Tonalität technisch)"
  - "Zwei separate Outputs — Investor-Summary + Tech-Anhang"
```

Resolve before moving on.

---

## 3. Anti-Patterns Specific to Phase 1

| Anti-Pattern | Why It Fails | Recovery |
|---|---|---|
| Filling a slot with a "reasonable default" the user did not state | Phase 2 gets a planted assumption that compounds | Always ask if the slot is required; defaults only for `language` and `depth` |
| Asking the same slot twice in different phrasing | The user feels interrogated and your model state is confused | Track filled slots explicitly; never re-ask without an explicit edit signal |
| Skipping `research_question_unpacked` because "the question is clear" | This is the single most common failure mode of Phase 1 — the user's question has neighbours, and Phase 2 can't tell them apart | Ask it always, except when the user has already stated what is *out of scope* |
| Using `multi_select` where `single_select` would do | Increases cognitive load on mobile; reduces decisiveness | Default to `single_select`; reach for `multi_select` only when items are genuinely combinable (constraints, axes) |
| Ending Phase 1 without writing the intent.yaml file | The downstream phases have no input | Writing the file is part of the exit gate, not an option |
| Writing the intent.yaml before user approval | Approval is the gate | Confirm-Turn first, file second |
| Not detecting that `temporal_scope` "letztes Jahr" became stale | Rolling temporal scopes need today's date pinned | Resolve "letztes Jahr" to concrete `from`/`to` based on conversation date |

---

## 4. Edge Cases

### 4a. The user explicitly refuses to specify a slot

*"Mach einfach was du für sinnvoll hältst."*

This is a refusal, not consent to invent. Push back once:

> *"Ich kann das Feld als 'unspecified' setzen — dann beschäftigt sich
> Phase 2 explizit mit dem Risiko, dass das Output deshalb breit oder
> beliebig wird. Oder: nimm einen der Default-Vorschläge unten als
> 'gut genug' an."*

If they still refuse, set the slot to `unspecified` (a literal string,
not null) and continue. Phase 2 must treat `unspecified` as a known
gap, not as license.

### 4b. The user keeps adding scope mid-loop

*"Ach übrigens, kann der Agent auch noch ___ machen?"*

Add to a `scope_drift` list inside the YAML and surface at the
Confirm-Turn. Don't silently merge — the user should see the
accumulated scope before approving.

### 4c. The user's question is malformed (unanswerable)

*"Ist meine Strategie richtig?"* — not a research question.

Flag it: *"Diese Frage kann ein Recherche-Agent nicht beantworten — sie
ist eine Bewertungsfrage zu einer Strategie, die er nicht kennt. Drei
Reformulierungen, die recherchierbar sind:"* — then propose three.

### 4d. The user gives the answer they want, not the question

*"Ich glaube X ist richtig — recherchier mir das."*

This is a `known_priors` event, not a `research_question`. Reformulate
the request explicitly:

> *"Du hast einen Prior: 'X ist richtig'. Den nehme ich in
> known_priors auf. Die Forschungsfrage selbst lautet vermutlich:
> 'Stimmt X — und was wären die stärksten Gegenargumente?' — passt
> das?"*

This converts a confirmation request into a falsifiable
research-question, which is what Phase 2 needs.

### 4e. The conversation language is mixed German/English

Default `language` to the language of the user's last message. If
mixed within one message, ask once. Do not infer from project memory.

---

## 5. The Confirm-Turn — Format Specification

The compact YAML preview shown at the Confirm-Turn must be ≤ 30 lines
and human-scannable. Format:

```yaml
# Intent — preview
slug:        eu-ai-act-saas-2026
language:    de

research_question: >-
  Welche AI-Act-Pflichten treffen SaaS-Startups, und welche sind bis
  Q3/2026 implementiert sein müssen?

unpacked:    "Nicht: DSGVO, US-Pendants, allgemeines AI-Recht."
audience:    "Technischer Mitgründer (Strategie + Technik)"
output:      "Vergleichsmatrix: Pflicht × Stichtag × Status"
scope:       2024-08-01 → 2027-08-01  (AI Act in-force window)
depth:       standard
success:     "Wir wissen, was bis Q3/2026 implementiert sein muss."

priors:      "Wir vermuten: High-Risk-System gilt für uns nicht."
constraints: "Nur EU-Quellen; keine Paywall."
domain_ctx:  null

routing:     B (Extraction) — Signale: 'Vergleichsmatrix', 'compile'
```

Then the `ask_user_input_v0` call:

```
question: "Stimmt das so? Was möchtest du editieren?"
options:
  - "Approve — Phase 1 done"
  - "Edit research_question / unpacked"
  - "Edit scope or depth"
  - "Edit priors / constraints"
```

Pick the 3–4 most likely edit-targets based on what's least
specified. "Approve" is always an option.

---

## 6. Why This Design

The user mandate for v3.0:

- *"zuerst Erfassung intent (mit askuser tool Rückfragen stellen bis 100%
  Klarheit über den Auftrag herrscht)"*
- *"festes Format - wie jeder Meta-prompt"*

The askuser-loop is the gate. Approve is the contract. The intent.yaml
is the hand-off. Everything Phase 2 does, it does on the basis of an
explicitly-approved spec — never on the basis of inference from the
chat.

This eliminates the v2.1 failure mode where "Phase 1: Intent
Recognition" was a single compound question and Phase 2 silently
invented anything missing. v3.0 makes the gap visible, asks about it,
and writes it down.
