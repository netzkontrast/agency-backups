# Method: Storyform Worksheet-Loop (Phase 2)

> **Sub-Skill:** `novel-architect-structure`
> **Load when:** Phase 2 (Narrative Architecture) Gates 1–3 ablaufen
> **Quelle:** [`skills/dramatica-theory/references/00-storyform-worksheet.md`](../../../dramatica-theory/references/00-storyform-worksheet.md)
> **Implementiert:** Task 072 (PR-Path)

## §0 Wofür dieser Loop?

Das Dramatica Storyform-Worksheet legt eine **deterministische Reihenfolge**
fest, in der ein vollständiges Storyform Slot-für-Slot ausgefüllt wird. Der
Loop bildet diese Reihenfolge auf die Phase-2-Sub-Phasen ab, sodass jede
askuser-Frage genau einen Slot adressiert und keine Order-Inversion entsteht
(z.B. Throughline-Class wählen *bevor* Concern feststeht).

Ohne diesen Loop tendiert Phase 2 dazu, Slots in der Reihenfolge der
Vokabular-Verfügbarkeit zu setzen — was zu Backtracking führt, weil
spätere Slots (Issue, Problem, Solution) frühere (Concern, Genre) constrainen.

## §1 Slot-Reihenfolge (verbindlich)

Pro [`dramatica-theory/references/00-storyform-worksheet.md`](../../../dramatica-theory/references/00-storyform-worksheet.md):

1. **OS Throughline** Class → Concern → Issue → Problem → Solution → Symptom → Response → Catalyst → Inhibitor
2. **MC Throughline** Domain → Concern → Issue → Problem → Solution → Symptom → Response → Catalyst → Inhibitor → Approach (Do-er/Be-er) → Mental Sex (Linear/Holistic)
3. **IC Throughline** Domain (= MC's complement) → Concern → Issue → Problem → Solution → Symptom → Response → Catalyst → Inhibitor
4. **SS / Relationship Throughline** Domain (= 4. Class) → Concern → Issue → Problem → Solution → Symptom → Response → Catalyst → Inhibitor
5. **Story Dynamics** Driver, Limit, Outcome, Judgment, Goal, Consequence, Cost, Dividend, Requirements, Prerequisites, Preconditions, Forewarnings

Jeder Schritt ist eine separate askuser-Frage (Cap 3 Slots/Call per `ask_user_input_v0`-Konvention).

## §2 Loop-Algorithmus

```
state = load(architecture.yaml or empty skeleton)

for slot in WORKSHEET_ORDER:
    if state[slot] is filled and approved:
        continue
    candidates = consult_dramatica_theory(state, slot)
    if len(candidates) == 1:
        proposal = candidates[0]
        ask_confirm(proposal)
    else:
        ask_select(candidates, max=3)
    write(architecture.yaml, slot, answer)
    update_status_view()
    if Gate-relevant (1, 2, 3):
        present_gate_view + ask_user_approve_or_edit

emit("architecture.yaml ready for Phase 3")
```

## §3 Gate-Mapping

Pro `phases/phase2-narrative-architecture.md`:

| Worksheet-Block | Phase-2 Gate | Approve-Triggert |
|---|---|---|
| OS + MC Class assigned | Gate 1 — Storyform-Shape | nur Class-Tupel, noch keine Concerns |
| Alle 4 Throughlines + Dynamics | Gate 2 — Throughlines/Classes/Dynamics | YAML komplett für Phase 2.5 |
| NCP-Skeleton + architecture.yaml final | Gate 3 — Final Architecture | Phase-2-Closure |

## §4 Slot-List Consolidation (PR #101 review §2.5)

Vorher: Slot-Namen wurden in `intent-template.yaml`, `architecture-template.yaml`,
`render_intent.py` und einzelnen Phase-Files dupliziert. Im Worksheet-Loop ist
**das `dramatica-theory`-Worksheet die Single Source of Truth**: alle Phase-2-
Slots leiten sich aus seiner Reihenfolge ab. `architecture-template.yaml`
referenziert nur die Top-Level-Throughline-Struktur; die Slot-Detail-Namen
werden bei jedem askuser-Call frisch über `nav.py` aufgelöst.

## §5 Acceptance Scenarios (Normativ)

```gherkin
Feature: Phase 2 follows the Dramatica worksheet order

  # anchor: T072.W.1
  Scenario: Slot order matches dramatica-theory worksheet
    Given a fresh project workspace with intent.yaml approved
    When Phase 2 runs askuser-Loops
    Then the askuser sequence MUST start with the OS Throughline Class
    And MUST NOT ask about Issue/Problem before the corresponding Concern is set

  # anchor: T072.W.2
  Scenario: Gate 1 fires after Class assignment for OS + MC
    Given OS Class and MC Domain are both filled in architecture.yaml
    And no other slots are filled yet
    When the askuser-loop reaches Gate 1
    Then the agent MUST present the gate view BEFORE asking about Concern
    And MUST collect approve/edit before continuing
```

## §6 Open Questions (für Task 073 / Folgearbeiten)

- Hard-Rules-Validierung (T073): nach jedem Slot-Write das Worksheet gegen H1–H12 prüfen.
- Soft-Rules-Hinting (T073): nach jedem Slot-Write Soft-Rule-Warnings anzeigen, ohne den Loop zu blockieren.
- Dual-Storyform: pro Worksheet-Schritt **beide** Narratives parallel füllen (per `methods/conflict/dual-storyform.md` §3).
