# Phase 2 — Narrative Architecture (8-Step Worksheet-Loop, 3-Gate Approval)

> **Load when:** Phase 2 ist aktiv, oder Edge-Case bei Storyform-Wahl /
> Throughline-Assignment / Class-Decision / Dynamic-Conflict / Crucial-
> Element-Identifikation.
>
> **Source spec:** [`dramatica-theory/references/00-storyform-worksheet.md`](../../dramatica-theory/references/00-storyform-worksheet.md)
> **Operational method:** [`methods/storyform/worksheet-loop.md`](../../novel-architect-structure/methods/storyform/worksheet-loop.md)
> **Inline-ask heuristics:** [`assets/decision-heuristic-quick-ref.md`](../../novel-architect-structure/assets/decision-heuristic-quick-ref.md)
> **Anti-pattern catalog:** [`dramatica-theory/references/11-anti-patterns.md`](../../dramatica-theory/references/11-anti-patterns.md)

## §0 Goal

Produziere `architecture.yaml` + NCP-Skeleton in `canon/<slug>.ncp.json`,
indem du das vollständige **8-Schritte-Storyform-Worksheet** aus
`dramatica-theory` durchläufst — nicht „auto + consult", sondern eine
operationale Loop mit AskUserQuestion-Slots pro Schritt und inline-
zitierten Entscheidungs-Heuristiken aus
[`decision-heuristic-quick-ref.md`](../../novel-architect-structure/assets/decision-heuristic-quick-ref.md).

Die acht Schritte des Worksheet (mit dem **`novel-architect` 3-Gate-Mapping**):

| Worksheet-Step | Was wird gefüllt | Gate |
|---|---|---|
| **0** Author's Intent / Premise | gelesen aus `intent.yaml` (Phase 1) | — (Precondition) |
| **1** Four Throughlines (OS / MC / IC / SS) | `throughlines.*.name` | **Gate 1** |
| **2** Class Assignment | `throughlines.*.class` | **Gate 2** |
| **3** Character Dynamics (4 binaries) | `dynamics.{mc_resolve,mc_growth,mc_approach,mc_mental_sex}` | **Gate 2** |
| **4** Plot Dynamics (4 binaries) | `dynamics.{plot_driver,plot_limit,outcome,judgment}` | **Gate 2** |
| **5** Plot Story Points | `story_points.*` (static / driver / thematic) | **Gate 2** |
| **6** Crucial Element | `crucial_element` + `dynamic_pair_partner` | **Gate 3** |
| **7** Signposts + Journeys | `signposts[][]` (4 per throughline) + 3 Journeys | **Gate 3** |
| (8) Optional Genre Mode | `genre_mode` | **Gate 3** (skip on default) |
| **V** Validation pass | run `00-storyform-validation.md` hard checks | **Gate 3** |

The Worksheet is the **SSoT for Phase 2 slot order**. v1.0.0's
"auto + consult dramatica-theory" is retired — every sub-phase below
binds to a worksheet step explicitly.

## §1 Input / Output

**Input:** `intent.yaml` aus Phase 1 (`approved=true`). Refuse to start
if not approved. Phase 1's `intent.dramatica_storyform_count`
(`single` / `dual`) determines whether one or two `narratives[]` entries
get built — when `dual`, the loop runs **Throughline-für-Throughline
through BOTH narratives simultaneously** (constraint from
`SKILL.md` "Dual-Storyform-Integrität").

**Output:**
- `architecture.yaml` (Schema 2, approved) — see [`assets/architecture-template.yaml`](../assets/architecture-template.yaml)
- `canon/<slug>.ncp.json` (NCP-Skeleton via `ncp-author`)
- `phase2-architecture-status-view.md` (final, rendered by `render/render_architecture.py`)

## §2 Sub-Phases mit 3 Gates (8-Step Worksheet-Loop)

```
Phase 2.1   Load intent.yaml + select methods                                 (silent)
Phase 2.2   Step 0: read Author's Intent + Storyform-count from intent.yaml   (silent)
Phase 2.3   Step 1: name the 4 Throughlines (OS / MC / IC / SS)               (askuser; ≤3 slots/turn)
            ──── GATE 1 (storyform shape + throughlines) ────                 (approve / edit-N)
Phase 2.4   Step 2: assign each Throughline to a Class (pair constraint)      (askuser; quick-ref §1 inline)
Phase 2.5   Step 3: Character Dynamics (Resolve / Growth / Approach / MS)     (askuser; quick-ref §2-5 inline)
Phase 2.6   Step 4: Plot Dynamics (Driver / Limit / Outcome / Judgment)       (askuser; quick-ref §6-8 inline)
Phase 2.7   Step 5: Plot Story Points (static + driver + thematic)            (1-2 askuser; quick-ref §9 inline)
            ──── GATE 2 (classes + dynamics + story points) ────              (approve / edit-section)
Phase 2.8   Step 6: Crucial Element + IC partner + Resolve↔Element check      (askuser; quick-ref §10 inline)
Phase 2.9   Step 7: Signposts + Journeys (4 per throughline)                  (askuser; nav.py Type-Quad)
Phase 2.10  Step 8 (optional): Genre Mode                                     (askuser ONLY on request)
Phase 2.11  Validation pass (00-storyform-validation.md hard checks)          (silent — auto)
Phase 2.12  NCP Skeleton Write (delegate ncp-author)                          (silent — auto)
Phase 2.13  Render Architecture View (file-first)                             (silent — auto)
            ──── GATE 3 (final architecture) ────                             (approve / edit-step / loop-back)
Phase 2.14  Write architecture.yaml (approved=true) + present_files           (file + present_files)
```

**Best case:** 3 askuser turns (3 gates, alle first-try approved).
**Typical:** 5–8 turns (one edit per Gate + 1–2 in-flight clarifications).
**Cap:** 10 askuser turns across all gates (hard rule HR.A4) — exceeded
means the storyform is incoherent; loop back to Phase 1.

**Operational detail:** [`methods/storyform/worksheet-loop.md` §3](../../novel-architect-structure/methods/storyform/worksheet-loop.md#3-per-step-operational-detail)
walks each Step's askuser-shape, decision heuristic, and recovery path.

## §3 Gate-Details

### §3.1 Gate 1 — Storyform Shape + Throughlines (Worksheet Steps 0 + 1)

**Was wird approved:** Phase 1's `dramatica_storyform_count` confirmed,
and the 4 Throughline *names* (OS / MC / IC / SS) — not yet their Classes.

**Rendered status-view:** `phase2-architecture-status-view.md` with the
Step-1 worksheet table (4 rows × 3 columns: POV, question, author's answer).

**Approval-Optionen:**
- **Approve** → fortfahren zu Step 2.
- **Edit OS / MC / IC / SS** → re-ask the specific throughline only.
- **Switch storyform count** (single ↔ dual) → loop back to Step 0 with
  intent-change warning (surfaces a Phase 1 revisit candidate).

**Diagnostic exit:** if the author cannot name SS, the worksheet says
*"that's diagnosis #1. Don't fudge it; come back when you can."* Surface
in status-view; askuser whether to loop back to Phase 1 (re-write
`core_conflict_question`) or park and proceed with `ss.name = "<UNRESOLVED>"`.

### §3.2 Gate 2 — Classes + Dynamics + Story Points (Worksheet Steps 2–5)

Eine konsolidierte Approval-View mit **vier Sektionen**:

**A. Class-Assignment (Step 2):**
- OS Class (one of {Universe, Physics, Mind, Psychology}).
- SS, MC, IC fall out by dynamic-pair constraint (auto-derived; show the
  derivation in the status-view).
- Inline: [`decision-heuristic-quick-ref.md` §1](../../novel-architect-structure/assets/decision-heuristic-quick-ref.md#1-class-choice).

**B. Character Dynamics (Step 3):**
- MC Resolve: Change / Steadfast (quick-ref §2).
- MC Growth: Start / Stop (quick-ref §3).
- MC Approach: Do-er / Be-er (quick-ref §4).
- MC Mental Sex: Linear / Holistic (quick-ref §5).

**C. Plot Dynamics (Step 4):**
- Story Driver: Action / Decision (quick-ref §6).
- Story Limit: Timelock / Optionlock (quick-ref §7).
- Story Outcome: Success / Failure (quick-ref §8).
- Story Judgment: Good / Bad (quick-ref §8).
- **Auto-readout: Ending Type** (Triumph / Personal Triumph / Personal
  Tragedy / Tragedy) shown in the status-view as the single best Gate-2
  sanity-check.

**D. Plot Story Points (Step 5):**
- Static: `goal` (at Type level — quick-ref §9), `requirements`,
  `consequences`, `forewarnings`.
- Driver/passenger: `dividends`, `costs`, `prerequisites`, `preconditions`.
- Thematic (per throughline): `concern`, `issue`, `problem`, `solution`,
  `focus`, `direction`.

**Approval-Optionen:** Approve / Edit Classes / Edit Char-Dynamics / Edit
Plot-Dynamics / Edit Story-Points. Edits re-run only the chosen section.

### §3.3 Gate 3 — Final Architecture (Worksheet Steps 6 + 7 + Validation)

Komplette `architecture.yaml` zur Approval. User kann:

- **Approve** → write final (`approved: true`) + present_files → Phase 3.
- **Edit Step 6 (Crucial Element)** → loop zurück zu Phase 2.8.
- **Edit Step 7 (Signposts)** → loop zurück zu Phase 2.9.
- **Loop back to Gate 2** → re-evaluate a Class / Dynamic / Story Point.
- **Loop back to Phase 1** → Intent-Änderung nötig (e.g., the
  Resolve↔Crucial-Element check exposed an incoherent thematic argument).

**Mandatory Validation gates** (auto, BEFORE the askuser): alle 12 H-rules
**H1–H12** aus
[`dramatica-theory/references/00-storyform-validation.md`](../../dramatica-theory/references/00-storyform-validation.md)
(canonical source numbering). Die fünf besonders hervorgehobenen Rules
(H3, H4, H5, H7, H9) fangen den Großteil der Authoring-Defekte; alle 12
MÜSSEN passen vor Gate 3.

| H-rule | Bound to step | Auto-check |
|---|---|---|
| **H1** Exactly 4 throughlines | Step 1 | ✓ |
| **H2** Each Class used exactly once | Step 2 | ✓ |
| **H3** OS-SS and MC-IC complementary dynamic pairs | Step 2 | ✓ |
| **H4** Story Goal at Type level | Step 5 (`STORY_POINT_LEVEL_TOO_FINE` if violated) | ✓ |
| **H5** Crucial Element at Element level | Step 6 (`nav.py by-id` check) | ✓ |
| **H6** Crucial Element lives in OS | Step 6 (ontology lookup) | ✓ |
| **H7** MC Resolve ↔ Crucial Element role agree | Step 6 (Change↔problem, Steadfast↔solution) | ✓ |
| **H8** IC sits on dynamic-pair partner of Crucial Element | Step 6 (`nav.py by-pair`) | ✓ |
| **H9** No character carries both Elements of a dynamic pair | all steps | ✓ |
| **H10** Outcome × Judgment = one of 4 endings | Step 4 | ✓ |
| **H11** Story Driver consistent across act transitions | Step 4 + 7 | ✓ |
| **H12** All 4 Signposts of a throughline = the 4 Types of that Class | Step 7 | ✓ |

Failures surface in the status-view with the canonical H-rule ID; the
author can `Edit step N` to fix without re-running the whole gate.
Auto-check delegation: [`novel-architect-structure/methods/validation/hard-rules.md`](../../novel-architect-structure/methods/validation/hard-rules.md).

**Gate 3 askuser-Header (verbindlich):** Jeder Gate-3-Approval-Prompt MUST
mit der folgenden Status-Zeile öffnen, sodass der Author die
Validation-Bilanz vor jeder Entscheidung sieht:

```
Hard Rules: <pass>/12 pass    (failures: <H-ID list> | alle OK)
```

Wo `<pass>` die Anzahl der H-Rules mit `result == PASS` ist und
`<H-ID list>` die komma-separierte Liste verletzter H-rule-IDs (z. B.
`H2, H7`); bei vollständigem Pass renderiert die Komponente das wörtliche
`alle OK`. Die Zeile MUST oben im Status-View vor den Edit-Optionen
erscheinen — HR.P2.5 (Validation pass bestanden muss sein vor Gate-3-
Askuser). Renderer-Wiring: siehe [Task 087](../../../tasks/087-novel-architect-render-architecture-wiring/task.md) (`render_architecture.py` Phase 2.13 → JSON-Artefakt von Task 084's `tools/check-hard-rules.py`).

## §4 Delegations (verbindlich)

| Frage | Delegate to | Navigator |
|---|---|---|
| Why is this Class/Type/Variation correct? | `dramatica-theory` | (prose; `references/01-foundations.md`, `06-storyforming.md`) |
| Storyform diagnosis (does the storyform hold together?) | `dramatica-theory` | `references/00-storyform-validation.md` |
| Class choice (OS) | `decision-heuristic-quick-ref.md` §1 | (inline excerpt in askuser) |
| Change vs Steadfast (Step 3.a) | `decision-heuristic-quick-ref.md` §2 | (inline) |
| Action vs Decision Driver (Step 4.a) | `decision-heuristic-quick-ref.md` §6 | (inline) |
| Optionlock vs Timelock (Step 4.b) | `decision-heuristic-quick-ref.md` §7 | (inline) |
| Goal at Type level (Step 5) | `decision-heuristic-quick-ref.md` §9 | (inline) |
| Crucial Element coherence (Step 6) | `decision-heuristic-quick-ref.md` §10 | (inline) |
| Dynamic Pair check on Element | `dramatica-vocabulary` | `nav.py by-id <id> --include-pairs` |
| KTAD coherence (Knowledge/Thought/Ability/Desire) | `dramatica-vocabulary` | `nav.py by-ktad K\|T\|A\|D` |
| Element-Quad lookup (Step 7 Type-Quad enumeration) | `dramatica-vocabulary` | `nav.py by-quad quad.<class>-tp` |
| NCP enum string for Storypoint | `ncp-author` | `nav.py by-ncp '<string>'` |
| Schema-Validierung | `ncp-author` | `node skills/ncp-author/scripts/validate.js <file>` |

**AGENTS.md NO.2 Regel:** Dramatica-flavored Slots MUST resolve through
ontology before written into NCP. Use `nav.py by-id <ontology-id>` to
find the NCP enum string. **Never coin a free Class/Type/Variation/Element
name** — that is a Schema-drift defect (auto-reject in Phase 2.11
validation pass).

## §5 NCP-Skeleton Workflow (delegated to ncp-author, Phase 2.12)

Phase 2.12 ruft `ncp-author` auf mit:

1. **Input:** `architecture.yaml` (post-Validation).
2. **Operation:** Create empty NCP skeleton + populate Worksheet outputs.
3. **Template:** `skills/ncp-author/assets/template-empty.json` oder
   `template-storyform.json` (selectable on `storyform_count`).
4. **Output:** `canon/<slug>.ncp.json` mit:
   - `narratives[]` array (1 oder 2 depending on storyform_count).
   - Pro narrative: `subtext.perspectives[]` mit 4 throughlines (OS/MC/IC/SS)
     incl. `class_ref` (Step 2).
   - Pro narrative: `subtext.dynamics[]` mit 8 Dynamics (Steps 3 + 4).
   - Pro narrative: `subtext.storypoints[]` mit static + driver + thematic
     Story Points (Step 5), incl. `crucial_element` als `kind: "crucial_element"`
     mit `dynamic_pair_partner` (Step 6).
   - Pro narrative: `subtext.storybeats[]` mit 4 Signposts × 4 Throughlines
     + 3 Journeys × 4 Throughlines (Step 7).
   - Empty `players[]` (Phase 3 fills), `moments[]` (Phase 5 fills).
5. **Validation:** `node skills/ncp-author/scripts/validate.js canon/<slug>.ncp.json`.

NCP-Mutation läuft IMMER über `ncp-author` (AGENTS.md NO.2 + SKILL.md
"NCP-Mutation NUR via ncp-author"). Direkte Hand-Edits an `.ncp.json`
sind verboten — würden Schema-Drift erzeugen.

## §6 Hard Rules

- **HR.P2.1 — 8-Step Worksheet ist die SSoT.** Sub-Phase-Reihenfolge folgt
  `00-storyform-worksheet.md` strikt; Skip eines Schritts ist ein
  Audit-Defekt.
- **HR.P2.2 — 3 Approval Gates, keine monolithische Loop.** Edits in einem
  Gate re-run nur die spezifische Sektion (Class / Dynamic / Story-Point /
  Crucial-Element / Signposts), nicht den ganzen Gate.
- **HR.P2.3 — Approval ist File-Write-Trigger.** Silent state advancement
  bricht Audit-Trail. Jeder Gate-Approve schreibt `architecture.yaml` mit
  inkrementierten `gates.gate_N.edits` und (am Ende) `approved: true`.
- **HR.P2.4 — intent.yaml ist read-only in Phase 2.** Bei Edit-Wunsch
  zurück zu Phase 1 — surface in der status-view.
- **HR.P2.5 — Validation pass bestanden muss sein** vor Gate-3-Askuser.
  Alle 12 hard rules **H1–H12** aus
  [`dramatica-theory/references/00-storyform-validation.md`](../../dramatica-theory/references/00-storyform-validation.md)
  (canonical numbering) MÜSSEN passen — delegiert an Task 073's
  [`novel-architect-structure/methods/validation/hard-rules.md`](../../novel-architect-structure/methods/validation/hard-rules.md)
  auto-check pipeline. Failures surfacen mit canonical H-rule-ID.
- **HR.P2.6 — Bei dual storyform:** Throughline-für-Throughline durch
  BEIDE narratives simultan. Niemals A komplett vor B. Each worksheet
  step asks "what's the OS for A?" + "what's the OS for B?" together.
- **HR.P2.7 — Dramatica-Lookups über `nav.py`.** Niemals Element-Namen
  frei coinen — Ontology-IDs first.
- **HR.P2.8 — Decision heuristic inline (HR.M2.3).** Every Step 2–7
  askuser embeds a one-paragraph excerpt from
  [`decision-heuristic-quick-ref.md`](../../novel-architect-structure/assets/decision-heuristic-quick-ref.md)
  in the status-view body (not just a link).

## §7 Edge Cases

### §7.1 User wählt single, aber intent.yaml sagt dual

→ Surface in Gate 1 (Step 0 readout): *„intent.yaml sagt dual, du
wählst jetzt single. Intent-Change nötig?"*
→ Optionen: Update intent → Phase 1 / Continue single / Switch dual.

### §7.2 OS + MC in derselben Class (Step 2 constraint violation)

→ Dramatica-Constraint violated (OS+SS = Pair, MC+IC = Pair).
→ Surface in Gate 2, Section A: *„Constraint violated. Beide in Universe
ist invalid. Welche bleibt?"*
→ Quick-ref §1 inline (showing the pair-partner rule).

### §7.3 Step 1 SS leer („cannot name SS")

→ Worksheet diagnosis #1. Surface: *„Du kannst SS nicht benennen.
Premise / MC↔IC-Beziehung unklar?"*
→ Optionen: Loop back to Phase 1 (`core_conflict_question` rewrite) /
Park mit `ss.name = "<UNRESOLVED>"` (Gate 1 conditional approval).

### §7.4 Step 3 Resolve doesn't match Step 6 Element role

→ Validation hard check fail.
→ Surface in Gate 3: *„MC Resolve = Change, aber Crucial Element ist
markiert als 'solution'. Inkonsistent."*
→ Optionen: Edit Resolve / Edit Element / Loop back to Step 3.

### §7.5 Step 5 Goal at Variation or Element level

→ `STORY_POINT_LEVEL_TOO_FINE` (quick-ref §9).
→ Surface: *„Goal ist 'faith' — das ist ein Element. Goal muss auf
Type-Level sein."* + Type-list für die OS-Class inline.
→ Edit Goal → re-pick at Type level.

### §7.6 NCP-Validation failed (Phase 2.12)

→ Surface error from `ncp-author/scripts/validate.js` in status-view.
→ Show problematic slot, askuser to fix → loop zurück zur entsprechenden
Worksheet-Step.

### §7.7 dramatica-theory sagt Storyform hält nicht zusammen

→ Diagnostic-Report von dramatica-theory in status-view embedden.
→ askuser: Fix Dynamic / Switch Throughline / Re-check Intent.

### §7.8 Dual storyform: A vs B Dynamic-Conflict

→ Surface side-by-side in status-view: *„Storyform A sagt MC=Change;
Storyform B sagt MC=Change. 5D-Interferenz braucht Dynamic-Differenz."*
→ Reference: `methods/conflict/dual-storyform.md` für 5D-Interferenz-Regeln.

## §8 architecture.yaml Schema 2

Vollständig in [`assets/architecture-template.yaml`](../assets/architecture-template.yaml).
Hier die Key-Sektionen (Worksheet-aligned slot names in **bold**):

```yaml
schema_version: "1.0"
provenance: { ... }
architecture:
  storyform_count: single|dual
  narratives:
    - id: storyform_a
      # ── Step 1: Throughlines (names) ──
      throughlines:
        os: { name: <string>, class: <Universe|Physics|Mind|Psychology>, type: <PLACEHOLDER>, variation: <PLACEHOLDER>, element: <PLACEHOLDER> }
        mc: { name: <string>, class: <…>, type: <…>, variation: <…>, element: <…> }
        ic: { name: <string>, class: <…>, type: <…>, variation: <…>, element: <…> }
        ss: { name: <string>, class: <…>, type: <…>, variation: <…>, element: <…> }
      # ── Steps 3 + 4: Dynamics ──
      dynamics:
        mc_resolve:    <Change|Steadfast>
        mc_growth:     <Start|Stop>
        mc_approach:   <Doer|Beer>
        mc_mental_sex: <Linear|Holistic>
        plot_driver:   <Action|Decision>
        plot_limit:    <Timelock|Optionlock>
        outcome:       <Success|Failure>
        judgment:      <Good|Bad>
      ending_type:     <Triumph|PersonalTriumph|PersonalTragedy|Tragedy>  # auto-derived
      # ── Step 5: Story Points ──
      story_points:
        static:        { goal, requirements, consequences, forewarnings }
        driver:        { dividends, costs, prerequisites, preconditions }
        thematic:      { os: {…}, mc: {…}, ic: {…}, ss: {…} }
      # ── Step 6: Crucial Element ──
      crucial_element:
        element:               <ontology-id>
        dynamic_pair_partner:  <ontology-id>   # IC sits here
        role:                  <problem|solution>  # matches mc_resolve
      # ── Step 7: Signposts + Journeys ──
      signposts:
        os: [<sp1>, <sp2>, <sp3>, <sp4>]
        mc: [<sp1>, <sp2>, <sp3>, <sp4>]
        ic: [<sp1>, <sp2>, <sp3>, <sp4>]
        ss: [<sp1>, <sp2>, <sp3>, <sp4>]
      journeys:
        os: [<j1>, <j2>, <j3>]   # 3 transitions between 4 signposts
        mc: [<j1>, <j2>, <j3>]
        ic: [<j1>, <j2>, <j3>]
        ss: [<j1>, <j2>, <j3>]
      # ── Step 8 (optional) ──
      genre_mode:      <ontology-id|null>
ncp:
  skeleton_written: bool
  ncp_file: <path>
  validation_status: passed|failed|pending
gates:
  gate_1_storyform_shape: { approved: bool, edits: int }
  gate_2_classes_dynamics_storypoints: { approved: bool, edits: int }
  gate_3_final_architecture: { approved: bool, edits: int }
worksheet_audit:
  step_0_intent_loaded:           bool   # always true (precondition)
  step_1_throughlines_named:      bool
  step_2_classes_assigned:        bool
  step_3_character_dynamics_set:  bool
  step_4_plot_dynamics_set:       bool
  step_5_story_points_set:        bool
  step_6_crucial_element_set:     bool
  step_7_signposts_set:           bool
  step_8_genre_mode_set:          bool   # may stay false (optional step)
  validation_pass:                bool
approved: bool
revisions: []
```

## §9 Exit Gate

Phase 2 ist done, wenn:
- `architecture.yaml` mit `approved: true`.
- Alle 9 `worksheet_audit.step_*` Felder konsistent gesetzt (Step 8
  darf `false` bleiben, alle anderen MÜSSEN `true` sein).
- `worksheet_audit.validation_pass: true`.
- `canon/<slug>.ncp.json` existiert, NCP validation status `passed`.
- Alle 3 Gates approved (`gates.gate_*.approved: true`).
- `phase2-architecture-status-view.md` final geschrieben.
- `present_files` aufgerufen auf `architecture.yaml` + status-view +
  `<slug>.ncp.json`.

→ Übergang zu Phase 3 (Character Architecture).

## §10 /sc:-Mapping

| Worksheet-Step | /sc: Command (primary) | /sc: Command (secondary) |
|---|---|---|
| Step 1 — Throughlines | `sc:brainstorm` | `sc:design` |
| Step 2 — Classes | `sc:design` | `sc:explain` |
| Step 3 — Char Dynamics | `sc:analyze` | `sc:explain` |
| Step 4 — Plot Dynamics | `sc:analyze` | `sc:explain` |
| Step 5 — Story Points | `sc:design` | `sc:workflow` |
| Step 6 — Crucial Element | `sc:analyze` | `sc:explain` |
| Step 7 — Signposts | `sc:workflow` | `sc:design` |
| Validation pass | `sc:reflect` | `sc:analyze` |

## §11 Operational Reference (External)

For each Step's askuser-shape, decision heuristic, recovery path, and
NCP slot mapping, see:

- **[`methods/storyform/worksheet-loop.md`](../../novel-architect-structure/methods/storyform/worksheet-loop.md)** — operational walkthrough (§3 per-step detail, §4 worked example, §5 method-level hard rules).
- **[`assets/decision-heuristic-quick-ref.md`](../../novel-architect-structure/assets/decision-heuristic-quick-ref.md)** — inline-quotable heuristics for Steps 2–7 askuser calls.
- **[`dramatica-theory/references/00-storyform-worksheet.md`](../../dramatica-theory/references/00-storyform-worksheet.md)** — the worksheet itself (theory SSoT).
- **[`dramatica-theory/references/10-decision-heuristics.md`](../../dramatica-theory/references/10-decision-heuristics.md)** — full heuristics (the quick-ref is a condensation).
- **[`dramatica-theory/references/00-storyform-validation.md`](../../dramatica-theory/references/00-storyform-validation.md)** — the 12 hard rules H1–H12 run in Phase 2.11.
- **[`novel-architect-structure/methods/validation/hard-rules.md`](../../novel-architect-structure/methods/validation/hard-rules.md)** — Task 073's deterministic auto-check pipeline for H1–H12.

This Phase 2 file is the **gate-binding contract** (what gets asked, when,
and how it ladders into 3 Gates). The method file is the **operational
recipe** (the per-step askuser shapes). Both bind to the worksheet —
that is the immovable SSoT.
