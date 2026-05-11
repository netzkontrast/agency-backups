# Method: Hard-Rules Validation (H1–H12)

> **Sub-Skill:** `novel-architect-structure`
> **Load when:** Phase 2 Storyform-Validation, vor Gate 2 / Gate 3
> **Quelle:** [`skills/dramatica-theory/references/00-storyform-validation.md`](../../../dramatica-theory/references/00-storyform-validation.md)
> **Implementiert:** Task 073 (PR-Path)

## §0 Wofür Hard Rules?

Dramatica's Storyform-Validation unterscheidet zwischen **Hard Rules** (H1–H12,
strukturelle Invarianten, deren Verletzung das Storyform-Modell bricht) und
**Soft Rules** (S1–Sn, Plausibilitäts-Heuristiken). Hard Rules MÜSSEN
geprüft werden, bevor das Storyform als „ready for Phase 3" deklariert
wird; Soft Rules werden als Warnings gezeigt.

Diese Validation lief in v1.0.0 implizit über `dramatica-theory`-Delegation;
v1.1.0 macht sie explizit + mechanisch.

## §1 Die zwölf Hard Rules

| ID | Rule | Auto-checkbar | Phase-2-Gate |
|----|------|----------------|--------------|
| H1 | Genau 4 Throughlines (OS, MC, IC, SS/Relationship). | ja | Gate 1 |
| H2 | Jede der vier Classes (Universe, Physics, Mind, Psychology) wird genau einmal verwendet. | ja | Gate 1 |
| H3 | MC Class und IC Class sind komplementär (Universe ↔ Mind, Physics ↔ Psychology). | ja | Gate 1 |
| H4 | OS Class und SS Class belegen die zwei verbleibenden Classes (komplementär zueinander). | ja | Gate 1 |
| H5 | Jede Throughline hat genau eine Concern aus dem dafür offenen Type-Set ihrer Class. | ja | Gate 2 |
| H6 | Issue/Problem/Solution einer Throughline gehören alle zur gleichen Quad innerhalb der Class. | ja | Gate 2 |
| H7 | Problem und Solution sind Dynamic-Pair-Partner innerhalb derselben Quad. | ja | Gate 2 |
| H8 | Symptom und Response sind Dynamic-Pair-Partner; sie sitzen in der gleichen Quad wie Problem/Solution. | ja | Gate 2 |
| H9 | Driver ∈ {Action, Decision} und ist konsistent mit allen 4 Throughlines (nicht throughline-spezifisch). | ja | Gate 2 |
| H10 | Limit ∈ {Optionlock, Timelock} und ist nicht throughline-spezifisch. | ja | Gate 2 |
| H11 | Outcome ∈ {Success, Failure}; Judgment ∈ {Good, Bad} — je genau ein Wert pro Storyform. | ja | Gate 2 |
| H12 | MC Approach ∈ {Do-er, Be-er} und MC Mental Sex ∈ {Linear, Holistic} — je genau ein Wert pro MC. | ja | Gate 2 |

Alle 12 Regeln sind durch `tools/dramatica-nav/nav.py` + `dramatica-theory`
ontologisch unterstützt; eine deterministische Validation-Pipeline ist
realisierbar ohne LLM-Reasoning.

## §2 Validation Pipeline

```python
def validate_hard_rules(architecture_yaml: dict, nav) -> list[Diagnostic]:
    """Return list of H-rule violations. Empty list = pass."""
    diagnostics = []
    diagnostics += _check_h1_throughline_count(architecture_yaml)
    diagnostics += _check_h2_class_uniqueness(architecture_yaml)
    diagnostics += _check_h3_mc_ic_complementarity(architecture_yaml, nav)
    diagnostics += _check_h4_os_ss_complementarity(architecture_yaml, nav)
    diagnostics += _check_h5_concern_in_class(architecture_yaml, nav)
    diagnostics += _check_h6_issue_problem_solution_same_quad(architecture_yaml, nav)
    diagnostics += _check_h7_problem_solution_dynamic_pair(architecture_yaml, nav)
    diagnostics += _check_h8_symptom_response_dynamic_pair(architecture_yaml, nav)
    diagnostics += _check_h9_driver_enum(architecture_yaml)
    diagnostics += _check_h10_limit_enum(architecture_yaml)
    diagnostics += _check_h11_outcome_judgment_enum(architecture_yaml)
    diagnostics += _check_h12_mc_approach_mental_sex(architecture_yaml)
    return diagnostics
```

Die `_check_h*` Helper sind reine Funktionen über `architecture.yaml`'s
Frontmatter + `tools/dramatica-nav/nav.py` Ontology-Lookups. Keine NCP-
Mutation. Implementierung sequel Task 073 (siehe `assets/hard-rules-check.md`
für die Checklist-Schablone).

## §3 Hard Rule vs. Soft Rule

| Aspekt | Hard Rule | Soft Rule |
|---|---|---|
| Verletzung | Storyform-Modell ist gebrochen | Storyform ist ungewöhnlich, aber gültig |
| Validation-Verhalten | BLOCKS Gate 2 / Gate 3 | WARNS, lets agent + user weiter |
| Linter-Tier | ERROR | WARN |
| Beispiele | "Concern liegt außerhalb der Class" | "Issue ungewöhnlich für dieses Genre" |

## §4 Integration in den Worksheet-Loop

Pro `methods/storyform/worksheet-loop.md` §2 wird `validate_hard_rules`
nach jedem Slot-Write aufgerufen:

```
for slot in WORKSHEET_ORDER:
    ...
    write(architecture.yaml, slot, answer)
    diagnostics = validate_hard_rules(architecture.yaml, nav)
    if any(d.tier == ERROR for d in diagnostics):
        present_violation_view(diagnostics)
        ask_user_resolve   # never silently skip
        rewrite(architecture.yaml, slot, ...)
```

Pro [`PR #101 review §2.5`](https://github.com/netzkontrast/agency/pull/101#issuecomment-4422239250) ist die `architecture.yaml`-Schreibung die einzige Source-of-Truth; die Validation läuft gegen diese Datei, nicht gegen einen In-Memory-Twin.

## §5 Acceptance Scenarios (Normativ)

```gherkin
Feature: Hard-Rules block Gate 2 on violation

  # anchor: T073.HR.1
  Scenario: H2 violation (Class duplicated) blocks Gate 2
    Given an architecture.yaml lists OS Class = "Universe" AND MC Class = "Universe"
    When the validator runs before Gate 2
    Then validate_hard_rules MUST return at least one diagnostic of tier ERROR
    And the diagnostic MUST cite H2 explicitly
    And Gate 2 MUST NOT pass until the violation is resolved

  # anchor: T073.HR.2
  Scenario: H7 violation (Problem/Solution not dynamic-pair) is caught
    Given an MC Throughline lists Problem = "Help" AND Solution = "Inequity"
    When the validator runs the H7 check
    Then validate_hard_rules MUST return an ERROR-tier diagnostic
    And the diagnostic MUST suggest "Help ↔ Hinder" as the canonical dynamic-pair partner
    And the Worksheet-Loop MUST re-ask the Solution slot
```

## §6 Open Questions

- **`tools/check-hard-rules.py`** als CLI-Linter für CI? Sequel-Task.
- Soft-Rules-Set: nach H1-H12 fundamental sortieren und dokumentieren.
- Dual-Storyform: H1-H12 pro Narrative parallel ausführen; H7/H8 dürfen sich zwischen narratives unterscheiden.
