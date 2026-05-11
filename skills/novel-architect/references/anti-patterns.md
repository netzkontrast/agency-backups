# Anti-Patterns — Cross-Phase Reference

> **Implementiert:** Task 074 (v1.1.0)
> **Quelle:** [`skills/dramatica-theory/references/11-anti-patterns.md`](../../dramatica-theory/references/11-anti-patterns.md) — AP-1 bis AP-14 (Dramatica-natives Anti-Pattern-Inventar)

Diese Datei synthetisiert die 14 Anti-Patterns aus dem Dramatica-Vokabular
durch alle 8 Phasen des `novel-architect`. Jedes Anti-Pattern hat eine
**Phase-Annotation** (in welcher Phase es typischerweise auftritt) und einen
**Detection-Hint** (woran man es im Workspace erkennt).

## Wie diese Datei zu nutzen

Diese Datei wird **on demand** geladen — typischerweise:

1. Vor Phase 2 Gate 2 / Gate 3 (Storyform-Plausibilität)
2. Vor Phase 3 Player-Slot-Approval (Charakter-Rollen-Klärung)
3. Vor Phase 6 Drafting (Per-Kapitel-Pre-Check)

In `methods/conflict/dual-storyform.md` werden Anti-Patterns AP-1, AP-2,
AP-9 explizit referenziert; sie sind dort Vorkonditionen.

## AP-1 bis AP-14

### AP-1 — MC = Protagonist gleichgesetzt

| Aspect | Detail |
|---|---|
| **Phase** | 2 (Throughline-Assignment), 3 (Player-Roles) |
| **Symptom** | `players[]` Protagonist-Slot wird automatisch zur MC erklärt |
| **Wahrheit** | MC = Throughline-Träger der first-person/we-Perspektive. Protagonist = funktional „treibt Goal-Pursuit". Beispiel: To Kill a Mockingbird — Scout (MC) ≠ Atticus (Protagonist). |
| **Detection** | architecture.yaml `mc.player_id` == architecture.yaml `os.protagonist_player_id` UND keine explizite Begründung in `assumptions-log` |
| **Fix** | Phase 2 Worksheet-Schritt 2 (MC-Domain) explizit von Phase 2 Schritt 1 (OS-Concern) entkoppeln |

### AP-2 — IC = Antagonist gleichgesetzt

| Aspect | Detail |
|---|---|
| **Phase** | 2, 3 |
| **Symptom** | Antagonist-Slot wird zur IC erklärt; Konflikt = Held-vs-Schurke |
| **Wahrheit** | IC ist der Charakter, der die MC's Werte/Perspektive challenged. Antagonist = funktional „blockiert Goal". IC kann Mentor, Lover, oder sogar der Antagonist sein — aber das ist nicht ihre Definition. |
| **Detection** | architecture.yaml `ic.player_id` == architecture.yaml `os.antagonist_player_id` ohne Begründung |
| **Fix** | Phase 2 Worksheet-Schritt 3 (IC-Domain) als komplementär zu MC (H3) auflösen, nicht als Antagonist-Korollar |

### AP-3 — Class als Genre missverstanden

| Aspect | Detail |
|---|---|
| **Phase** | 2 (Class-Assignment, vor Gate 1) |
| **Symptom** | "Sci-Fi Roman → OS Class Physics", "Romance → OS Class Mind", etc. |
| **Wahrheit** | Class ist eine *Storyform*-Dimension, kein Genre-Marker. Ein Hard-SF kann OS Mind sein (Solaris); eine Romance kann OS Physics sein (When Harry Met Sally). Class beschreibt **wo der OS-Konflikt sitzt**. |
| **Detection** | OS Class korreliert in 100% der vorherigen Projekte mit Genre — d.h. der Author wählt Class nach Genre-Erwartung, nicht nach Konflikt-Lokus |
| **Fix** | `dramatica-theory` 10-decision-heuristics.md konsultieren; OS Concern *vor* OS Class festlegen |

### AP-4 — Throughline-Concerns aus Class extrapoliert ohne Validation

| Aspect | Detail |
|---|---|
| **Phase** | 2 (Gate 2 Vorbereitung) |
| **Symptom** | OS Concern wird gewählt, ohne `nav.py by-class <class>` zu konsultieren |
| **Wahrheit** | Jede Class hat 4 mögliche Concerns (Types). Die Wahl unter ihnen ist nicht beliebig — sie constrainen die Quad-Identität (H6). Phase 2 darf hier nicht raten. |
| **Detection** | architecture.yaml schreibt Concern OHNE entsprechende `nav.py by-class` Trace in `notes.md` |
| **Fix** | Worksheet-Loop §1 (verbindliche Reihenfolge) hält Class → Concern → Issue ein; H5 Validator catches Verletzungen |

### AP-5 — Issue/Problem/Solution aus verschiedenen Quads

| Aspect | Detail |
|---|---|
| **Phase** | 2 (Gate 2 — Throughline-Detail) |
| **Symptom** | OS Issue ∈ Quad-A, OS Problem ∈ Quad-B (z.B. Hope/Dream und Help/Hinder) |
| **Wahrheit** | H6 — Issue/Problem/Solution leben in derselben Quad innerhalb der Class. Cross-Quad-Wahl ist immer ein Storyform-Modellbruch. |
| **Detection** | `validate_hard_rules` H6 fail |
| **Fix** | Worksheet-Loop §2 zwingt Quad-Konsistenz; Hard-Rules-Check.md Gate-Block |

### AP-6 — Problem ↔ Solution nicht dynamic-pair

| Aspect | Detail |
|---|---|
| **Phase** | 2 (Gate 2) |
| **Symptom** | Problem = "Help", Solution = "Inequity" (kein gültiger Dynamic-Pair) |
| **Wahrheit** | H7 — Problem und Solution sind Dynamic-Pair-Partner innerhalb derselben Quad. `nav.py by-dynamic-pair Help` → "Hinder", nicht "Inequity". |
| **Detection** | `validate_hard_rules` H7 fail |
| **Fix** | Worksheet-Loop schlägt nach jedem Problem-Set das `nav.py`-validierte Solution-Pair vor |

### AP-7 — Driver/Limit als throughline-spezifisch behandelt

| Aspect | Detail |
|---|---|
| **Phase** | 2 (Gate 2) |
| **Symptom** | OS Driver = Action, aber MC Driver wird separat als Decision gesetzt |
| **Wahrheit** | H9/H10 — Driver und Limit sind story-wide (alle 4 Throughlines teilen einen Wert). |
| **Detection** | architecture.yaml hat throughline-pegged Driver-Felder |
| **Fix** | Schema-Constraint: Driver/Limit nur auf Top-Level der architecture.yaml |

### AP-8 — Outcome/Judgment vorzeitig festgeklemmt

| Aspect | Detail |
|---|---|
| **Phase** | 2 (Gate 3) |
| **Symptom** | Outcome/Judgment werden im ersten Phase-2-Durchlauf festgelegt, ohne Phase 5 (Scene Matrix) abzuwarten |
| **Wahrheit** | Outcome/Judgment sind die *finale Auflösung des Storyforms* — sie sind formal H11-required ab Gate 3, aber faktisch erst durch die Scene-Matrix konkretisiert. Vorzeitige Festlegung blockiert Author-Discovery in Phase 5/6. |
| **Detection** | Outcome/Judgment in architecture.yaml *bevor* Phase 5 startet UND ohne `notes.md`-Begründung |
| **Fix** | Gate 3 markiert Outcome/Judgment als *vorläufig* (`provisional: true`); Phase 7 bestätigt sie nach Phase 6 |

### AP-9 — Dual-Storyform-Throughlines sequentiell statt parallel

| Aspect | Detail |
|---|---|
| **Phase** | 2, 3, 5 (alle dual-storyform-Phasen) |
| **Symptom** | Narrative-A wird komplett gefüllt; *dann* Narrative-B. |
| **Wahrheit** | Methods/conflict/dual-storyform.md §3 — beide Narratives MÜSSEN Throughline-für-Throughline parallel gefüllt werden, damit die 5D-Interferenz entsteht. Sequentielle Füllung erzeugt zwei isolierte Storyforms. |
| **Detection** | Workspace `architecture.yaml:narratives[1]` ist leer, während `narratives[0]` komplett ist |
| **Fix** | Worksheet-Loop für dual-storyform pro Slot beide narratives in einem askuser-Call adressieren |

### AP-10 — Genre als Storyform-Constraint missbraucht

| Aspect | Detail |
|---|---|
| **Phase** | 1 → 2 |
| **Symptom** | "Es ist Horror, also Outcome = Failure" |
| **Wahrheit** | Genre ist eine Reception-Kategorie; Storyform-Slots sind orthogonale Strukturen. Horror kann Outcome = Success haben (Get Out). |
| **Detection** | Phase 1 intent.yaml Genre korreliert mit Phase 2 Outcome ohne reasoning trace |
| **Fix** | Phase 2 Worksheet-Loop hat keine Genre-Berücksichtigung in §1; Outcome wird durch H11 enum-validiert, nicht durch Genre |

### AP-11 — MC Approach/Mental Sex stereotypisiert

| Aspect | Detail |
|---|---|
| **Phase** | 2 (H12), 3 |
| **Symptom** | "Männlicher MC → Linear, Do-er; weiblicher MC → Holistic, Be-er" |
| **Wahrheit** | H12 — Approach und Mental Sex sind unabhängige Storyform-Dimensionen, nicht von Charakter-Gender abhängig. |
| **Detection** | architecture.yaml `mc.approach` + `mc.mental_sex` korrelieren mit player[mc].gender ohne reasoning trace |
| **Fix** | Phase 3 player-slot-Befüllung explizit von H12-Slots entkoppeln; `assumptions-log` cite required if correlation present |

### AP-12 — Symptom mit Problem verwechselt

| Aspect | Detail |
|---|---|
| **Phase** | 2 (Gate 2) |
| **Symptom** | OS Symptom = "Imbalance" UND OS Problem = "Imbalance" (Slot-Duplikat) |
| **Wahrheit** | Symptom ist *was die Storyform-Subjekte glauben, dass das Problem ist*; Problem ist *was es wirklich ist*. H8 zwingt sie in dieselbe Quad, aber NICHT identisch. |
| **Detection** | `validate_hard_rules` — wir können einen advisory check für Symptom == Problem einführen (Soft-Rule-Tier) |
| **Fix** | Worksheet-Loop §2 trennt Symptom-Set von Problem-Set; askuser-Frage formuliert die Differenz explizit |

### AP-13 — Concern als Plot-Beat statt Strukturslot gelesen

| Aspect | Detail |
|---|---|
| **Phase** | 2, 5 (Scene Matrix → Concern-Trace) |
| **Symptom** | "OS Concern = Innermost Desires" wird als „Akt 2 Wendepunkt-Thema" interpretiert |
| **Wahrheit** | Concern ist eine *Throughline-Konstante*, kein Plot-Beat. Der Plot-Beat-Track (Signposts → Storypoints → Storybeats) sitzt unter der Concern, nicht statt ihrer. |
| **Detection** | scene-matrix.md schreibt Concern in eine Akt-Zelle UND nicht in den Storyform-Header |
| **Fix** | Phase 5 Render-Template hält Concern im Storyform-Header; Akt-Zellen tragen Signposts/Storypoints, keine Concerns |

### AP-14 — Theme als Outcome gleichgesetzt

| Aspect | Detail |
|---|---|
| **Phase** | 1 → 2 |
| **Symptom** | "Roman-Theme = Verzweiflung, also Outcome = Failure / Judgment = Bad" |
| **Wahrheit** | Theme entsteht aus der **Differenz** zwischen MC-Resolve und Outcome/Judgment, nicht aus deren Identität. Verzweiflung als Theme kann durch Failure/Good (Pyrrhic loss), Success/Bad (toxic victory), oder andere Konstellationen entstehen. |
| **Detection** | Phase 1 intent.yaml `core_conflict_question` enthält direkt Outcome-Vokabular |
| **Fix** | Phase 1 askuser-Loop trennt Theme-Frage von Outcome-Slot; Phase 2 Outcome ist H11-enum, nicht prose-derived |

## Cross-Reference Index

| AP | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 | Phase 7 |
|----|---------|---------|---------|---------|---------|---------|---------|
| AP-1 | | x | x | | | | |
| AP-2 | | x | x | | | | |
| AP-3 | | x (vor Gate 1) | | | | | |
| AP-4 | | x (Gate 2) | | | | | |
| AP-5 | | x (Gate 2) | | | | | |
| AP-6 | | x (Gate 2) | | | | | |
| AP-7 | | x (Gate 2) | | | | | |
| AP-8 | | x (Gate 3) | | | | | x (post-mortem) |
| AP-9 | | x | x | | x | | |
| AP-10 | x | x | | | | | |
| AP-11 | | x (H12) | x | | | | |
| AP-12 | | x (Gate 2) | | | | | |
| AP-13 | | x | | | x | | |
| AP-14 | x | x | | | | | |

## Acceptance Scenarios (Normativ)

```gherkin
Feature: Anti-Patterns are surfaced before phase gates

  # anchor: T074.AP.1
  Scenario: AP-1 (MC=Protagonist) warning fires at Phase 3 player-role gate
    Given architecture.yaml.mc.player_id == architecture.yaml.os.protagonist_player_id
    And notes.md has no entry citing this equivalence
    When Phase 3 reaches its player-role approval gate
    Then the agent MUST surface AP-1 as a WARN before the user approves
    And the user MUST either confirm "intentional" (writing to notes.md) OR change one of the assignments

  # anchor: T074.AP.2
  Scenario: AP-9 (dual-storyform sequential fill) WARN at Phase 2.5
    Given intent.yaml.dramatica_storyform_count == "dual"
    And architecture.yaml.narratives[0] is fully filled while narratives[1] is empty
    When Phase 2.5 (Dynamics) is about to start
    Then the agent MUST emit a WARN that AP-9 is occurring
    And the agent MUST suggest parallel-fill for the remaining slots
```

## Open Questions

- Sollten AP-WARNs gegen Hard-Rules upgegradet werden (z.B. AP-7 Driver-pegging)? — Sequel-Decision.
- AP-Index automatisch in `references/skill-improvement-todo.md` referenzieren? — Sequel.
