# Phase 2 — Narrative Architecture (3-Gate Approval)

> **Load when:** Phase 2 ist aktiv, oder Edge-Case bei Storyform-Wahl /
> Throughline-Assignment / Class-Decision / Dynamic-Conflict

## §0 Goal

Produziere `architecture.yaml` + NCP-Skeleton in `canon/<slug>.ncp.json`.
Storyform-Wahl (single/dual), Throughlines (OS/MC/IC/SS), Klassen
(Universe/Physics/Mind/Psychology), Dynamics festgelegt — **3 Approval Gates**
analog `research-prompt-optimizer` Phase 2.

## §1 Input / Output

**Input:** `intent.yaml` aus Phase 1 (approved=true). Refuse to start if not approved.

**Output:**
- `architecture.yaml` (Schema 2, approved)
- `canon/<slug>.ncp.json` (NCP-Skeleton via `ncp-author`)
- `architecture-status-view.md` (final)

## §2 Sub-Phases mit 3 Gates

```
Phase 2.1   Load & Validate intent.yaml + select methods       (silent)
Phase 2.2   Storyform Count Decision                            (auto from intent, askuser only on conflict)
            ──── GATE 1 (storyform shape) ────                  (1 askuser: Approve / Edit)
Phase 2.3   Throughline Assignment (OS/MC/IC/SS)                (auto + dramatica-theory consult)
Phase 2.4   Class Assignment (Universe/Physics/Mind/Psychology) (auto, validated by dramatica-theory)
Phase 2.5   Dynamics Selection (Driver/Limit/Outcome/Judgment)  (delegate dramatica-vocabulary)
            ──── GATE 2 (throughlines+classes+dynamics) ────    (1 askuser: Approve / Edit each)
Phase 2.6   NCP Skeleton Write                                  (delegate ncp-author)
Phase 2.7   Render Architecture View                            (file-first)
            ──── GATE 3 (final architecture) ────               (1 askuser: Approve / Edit / Loop back)
Phase 2.8   Write architecture.yaml (approved) + present_files  (file + present_files)
```

**Best case:** 3 askuser turns (3 gates, alle first-try approved)
**Typical:** 4–6 turns (1–3 edits)
**Cap:** 8 askuser turns across all gates

## §3 Gate-Details

### §3.1 Gate 1 — Storyform Shape

Frage: *„Single oder Dual Storyform?"*

- **Single** (Default für die meisten Romane): Ein Storyform mit OS+MC+IC+SS
- **Dual** (Advanced): Zwei parallele Storyforms (A+B), die als 5D-Interferenz wirken
  - Bei `intent.dramatica_storyform_count: dual` automatisch wählen, aber bestätigen lassen

**Approval-Optionen:** Approve / Switch to <other>

### §3.2 Gate 2 — Throughlines + Classes + Dynamics

Eine konsolidierte Approval-View mit drei Sektionen:

**A. Throughline-Assignment (für jeden Narrative):**
- Welche Charakter-Funktion ist MC? IC? Wer treibt OS? Was ist SS-Beziehung?

**B. Class-Assignment (für jede Throughline):**
- OS in Universe/Physics/Mind/Psychology?
- MC in welcher? (Constraint: OS+SS = eine Dynamic Pair, MC+IC = andere)

**C. Dynamics-Selection (für jeden Narrative):**
- MC Resolve: Change / Steadfast
- MC Growth: Start / Stop
- MC Approach: Doer / Beer
- MC Mental Sex: Linear / Holistic
- Plot Driver: Action / Decision
- Plot Limit: Timelock / Optionlock
- Outcome: Success / Failure
- Judgment: Good / Bad

**Approval-Optionen:** Approve / Edit Throughlines / Edit Classes / Edit Dynamics

### §3.3 Gate 3 — Final Architecture

Komplette `architecture.yaml` zur Approval. User kann:
- **Approve** → write final + present_files
- **Edit specific section** → loop zurück zur entsprechenden Sub-Phase
- **Loop back to Phase 1** → Intent-Änderung nötig

## §4 Delegations (verbindlich)

| Frage | Delegate to | Navigator |
|---|---|---|
| Why is this Class/Type/Variation correct? | `dramatica-theory` | (prose) |
| Storyform diagnosis (does the storyform hold together?) | `dramatica-theory` | (prose) |
| Dynamic Pair check on Element | `dramatica-vocabulary` | `nav.py by-id <id> --include-pairs` |
| KTAD coherence (Knowledge/Thought/Ability/Desire) | `dramatica-vocabulary` | `nav.py by-ktad K\|T\|A\|D` |
| Element-Quad lookup | `dramatica-vocabulary` | `nav.py by-quad quad.<name>-el` |
| NCP enum string for Storypoint | `ncp-author` | `nav.py by-ncp '<string>'` |
| Schema-Validierung | `ncp-author` | `node skills/ncp-author/scripts/validate.js <file>` |

**AGENTS.md NO.2 Regel:** Dramatica-flavored Slots MUST resolve through
ontology before written into NCP. Use `nav.py by-id <ontology-id>` to find
the NCP enum string.

## §5 NCP-Skeleton Workflow (delegated to ncp-author)

Phase 2.6 ruft `ncp-author` auf mit:

1. **Input:** `architecture.yaml`
2. **Operation:** Create empty NCP skeleton
3. **Template:** `skills/ncp-author/assets/template-empty.json` oder `template-storyform.json`
4. **Output:** `canon/<slug>.ncp.json` mit:
   - `narratives[]` array (1 oder 2 depending on storyform_count)
   - Pro narrative: `subtext.perspectives[]` mit 4 throughlines (OS/MC/IC/SS)
   - Pro narrative: `subtext.dynamics[]` mit allen Plot+Character Dynamics
   - Empty `players[]`, `storypoints[]`, `storybeats[]`, `moments[]`
5. **Validation:** `node skills/ncp-author/scripts/validate.js canon/<slug>.ncp.json`

## §6 Hard Rules

- **3 Approval Gates, keine monolithische Loop.** Edits in einem Gate re-run nur dieses Gate
- **Approval ist File-Write-Trigger.** Silent state advancement bricht Audit-Trail
- **intent.yaml ist read-only in Phase 2.** Bei Edit-Wunsch zurück zu Phase 1
- **NCP-Schema-Validierung passed muss sein** vor Gate 3
- **Bei dual storyform: Storyform A + B parallel encodieren.** Niemals A komplett vor B
- **Dramatica-Lookups über nav.py.** Niemals Element-Namen frei coinen — Ontology-IDs first

## §7 Edge Cases

### §7.1 User wählt single, aber intent.yaml sagt dual

→ Surface in Gate 1: *„intent.yaml sagt dual, du wählst jetzt single. Intent-Change nötig?"*
→ Optionen: Update intent → Phase 1 / Continue single / Switch dual

### §7.2 OS + MC in derselben Class

→ Dramatica-Constraint violated (OS+SS = Pair, MC+IC = Pair).
→ Surface in Gate 2: *„Constraint violated. Beide in Universe ist invalid. Welche bleibt?"*

### §7.3 NCP-Validation failed

→ Surface error from `ncp-author/scripts/validate.js`
→ Show problematic slot in status-view, askuser to fix

### §7.4 dramatica-theory sagt Storyform hält nicht zusammen

→ Diagnostic-Report von dramatica-theory in status-view embedden
→ askuser: Fix Dynamic / Switch Throughline / Re-check Intent

## §8 architecture.yaml Schema 2

Vollständig in `assets/architecture-template.yaml`. Hier die Key-Sektionen:

```yaml
schema_version: "1.0"
provenance: { ... }
architecture:
  storyform_count: single|dual
  narratives:
    - id: storyform_a
      throughlines: { os, mc, ic, ss }
      dynamics: { mc_resolve, mc_growth, mc_approach, mc_mental_sex, plot_driver, plot_limit, outcome, judgment }
ncp:
  skeleton_written: bool
  ncp_file: <path>
  validation_status: passed|failed|pending
gates:
  gate_1_storyform_shape: { approved: bool, edits: int }
  gate_2_throughlines_classes_dynamics: { approved: bool, edits: int }
  gate_3_final_architecture: { approved: bool, edits: int }
approved: bool
revisions: []
```

## §9 Exit Gate

Phase 2 ist done, wenn:
- `architecture.yaml` mit `approved: true`
- `canon/<slug>.ncp.json` exists, validation passed
- Alle 3 Gates approved
- `architecture-status-view.md` final geschrieben
- `present_files` aufgerufen

→ Übergang zu Phase 3 (Character Architecture)

## §10 /sc:-Mapping

| Schritt | /sc: Command |
|---|---|
| Architektur-Skizze | `sc:design` |
| Storyform-Validation | `sc:analyze` |
| Theorie-Check | `sc:explain` |
