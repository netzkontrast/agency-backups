# Method: Storyform Worksheet-Loop (8-step Dramatica build)

> **Category:** Storyform (Phase 2 of `novel-architect`)
> **Load when:** Phase 2.1 selects methods *and* the project uses the default
> Dramatica-native architecture build (any `intent.methods_preference.structure`
> containing `dramatica-quad`, or unset).
> **Source spec:** [`dramatica-theory/references/00-storyform-worksheet.md`](../../../dramatica-theory/references/00-storyform-worksheet.md)
> **Inline ask asset:** [`assets/decision-heuristic-quick-ref.md`](../../assets/decision-heuristic-quick-ref.md)
> **Anti-patterns to surface mid-loop:** [`dramatica-theory/references/11-anti-patterns.md`](../../../dramatica-theory/references/11-anti-patterns.md)

---

## §0 Why this method exists

v1.0.0's Phase 2 said *"auto + consult dramatica-theory"* for every sub-phase.
That is **declarative** — it tells you the slots exist, but does not walk
the author through filling them. Authors with no Dramatica background cannot
follow "consult dramatica-theory"; they need an operational loop that asks
the right question, in the right order, with the right decision heuristic
inlined.

This method is the operational answer: an 8-step worksheet borrowed
verbatim from [`00-storyform-worksheet.md`](../../../dramatica-theory/references/00-storyform-worksheet.md),
mapped onto `novel-architect`'s 3-Gate Approval discipline.

---

## §1 The 8 Worksheet Steps (canonical order)

The order below is the **recommended decision order**. Revisit earlier
steps when later ones expose contradictions — that is not a loop violation,
it is the worksheet's own rule (`00-storyform-worksheet.md` §opening note).

| Step | Worksheet title | What it fills | Gate |
|------|-----------------|---------------|------|
| **0** | Author's Intent / Premise | (read from `intent.yaml` — already done in Phase 1) | — (precondition) |
| **1** | Identify the Four Throughlines (OS / MC / IC / SS) | `architecture.narratives[].throughlines.{os,mc,ic,ss}` (name fields) | **Gate 1** |
| **2** | Assign each Throughline to a Class | `architecture.narratives[].throughlines.*.class` | **Gate 2** |
| **3** | Character Dynamics (4 binary choices) | `architecture.narratives[].dynamics.{mc_resolve,mc_growth,mc_approach,mc_mental_sex}` | **Gate 2** |
| **4** | Plot Dynamics (4 binary choices) | `architecture.narratives[].dynamics.{plot_driver,plot_limit,outcome,judgment}` | **Gate 2** |
| **5** | Plot Story Points (static + driver + thematic) | `architecture.narratives[].story_points.*` | **Gate 2** |
| **6** | The Crucial Element | `architecture.narratives[].crucial_element` (+ IC partner) | **Gate 3** |
| **7** | Signposts and Journeys | `architecture.narratives[].signposts[][]` (4 per throughline) | **Gate 3** |
| (8) | *Optional: Genre Mode* | `architecture.narratives[].genre_mode` | **Gate 3** (skip when blank) |
| **V** | Validation pass | run [`00-storyform-validation.md`](../../../dramatica-theory/references/00-storyform-validation.md) hard checks | **Gate 3** |

The Gate alignment is the **only** difference between this workflow and the
raw worksheet. Three gates remain (preserving the `research-prompt-optimizer`
3-Gate discipline), and they bind the worksheet's natural seams:

- **Gate 1 = Steps 0 + 1.** Storyform shape + Throughline names. Cheapest
  to revise; an OS/MC mis-identification cascades everywhere downstream.
- **Gate 2 = Steps 2 + 3 + 4 + 5.** Classes + Dynamics + Story Points. All
  16 binary-ish decisions land together so the author sees the storyform's
  *shape* before sinking effort into Step 6/7 specifics.
- **Gate 3 = Steps 6 + 7 (+ 8) + Validation.** Crucial Element + Signposts +
  optional Genre Mode + the worksheet's validation pass. Failures here
  loop back to the specific earlier step — *not* the whole gate.

---

## §2 Sub-Phase Pseudocode (Phase 2.1 – 2.10)

```
Phase 2.1  Load intent.yaml + select methods                            (silent)
Phase 2.2  Step 0: read Author's Intent from intent.yaml                (silent — no askuser)
Phase 2.3  Step 1: name the 4 Throughlines (OS / MC / IC / SS)          (1 askuser, ≤3 slots/turn)
           ──── GATE 1 (storyform shape + throughlines) ────            (approve / edit-N)
Phase 2.4  Step 2: assign each Throughline to a Class                   (1 askuser; pair constraint enforced)
Phase 2.5  Step 3: Character Dynamics (4 binaries)                      (1 askuser; AskUserQuestion 4-option)
Phase 2.6  Step 4: Plot Dynamics (4 binaries)                           (1 askuser; AskUserQuestion 4-option)
Phase 2.7  Step 5: Plot Story Points (static + driver + thematic)       (1–2 askuser; Goal at Type level)
           ──── GATE 2 (classes + dynamics + story points) ────         (approve / edit-section)
Phase 2.8  Step 6: Crucial Element + IC partner + consistency check     (1 askuser; dynamic-pair lookup)
Phase 2.9  Step 7: Signposts and Journeys (4 per throughline)           (1 askuser; Type-Quad enumeration)
Phase 2.10 Step 8 (optional): Genre Mode                                (skip on default; 1 askuser if requested)
Phase 2.11 Validation pass (00-storyform-validation.md hard checks)     (silent — auto)
Phase 2.12 NCP Skeleton Write (delegate ncp-author)                     (silent — auto)
Phase 2.13 Render Architecture View (file-first)                        (silent — auto)
           ──── GATE 3 (final architecture) ────                        (approve / edit-step / loop-back)
Phase 2.14 Write architecture.yaml (approved) + present_files           (file + present_files)
```

**Best case:** 3 askuser turns at the three Gates (all first-try approved).
**Typical:** 5–8 turns (one edit per Gate + 1–2 in-flight clarifications).
**Cap:** 10 askuser turns across all gates (hard rule HR.A4 in
`AGENTS.md` — exceeded means storyform is incoherent; loop back to Phase 1).

---

## §3 Per-Step Operational Detail

### §3.1 Step 1 — Identify the Four Throughlines

**What you write:** one *name* per throughline. Not a Class yet (that's
Step 2). The name answers a perspective question:

| Throughline | POV question | Output shape |
|---|---|---|
| OS | What's the objective conflict everyone is involved in? | short noun phrase |
| MC | Whose personal struggle do we live inside? | character name + 1-line frame |
| IC | Who keeps challenging the MC's worldview by their existence? | character name + 1-line frame |
| SS | What's the MC↔IC relationship, treated as its own story? | relationship noun phrase |

**AskUserQuestion shape (turn 1):** 4 throughlines as separate sub-questions
on the same form — but only 3 fit per HR.A1, so split if SS needs disambiguation.

**Diagnostic exit:** if the author cannot name SS, **stop**. Per the
worksheet: *"If you can't name one — most often the SS — that's diagnosis #1.
Don't fudge it; come back when you can."* Surface in status-view and
askuser whether to loop back to Phase 1 (`core_conflict_question` rewrite)
or park and proceed.

### §3.2 Step 2 — Class Assignment

**Constraint:** OS+SS form one dynamic pair, MC+IC form the other. Pairs are
**Universe ↔ Mind** (state pair) and **Physics ↔ Psychology** (process pair).

Pick one Class for OS; the other three are *constrained*:

```
OS = Universe  →  SS = Mind,        MC ∈ {Physics, Psychology}, IC = MC's pair partner
OS = Physics   →  SS = Psychology,  MC ∈ {Universe, Mind},      IC = MC's pair partner
OS = Mind      →  SS = Universe,    MC ∈ {Physics, Psychology}, IC = MC's pair partner
OS = Psychology→  SS = Physics,     MC ∈ {Universe, Mind},      IC = MC's pair partner
```

**Decision heuristic:** [`decision-heuristic-quick-ref.md` §1](../../assets/decision-heuristic-quick-ref.md#1-class-choice).
**AskUserQuestion shape:** 2 slots — Class for OS, Class for MC. SS and IC fall out by constraint.
**Validation:** use `tools/dramatica-nav/nav.py by-id concept.dynamic-pair`
to confirm the pair lookup.

### §3.3 Step 3 — Character Dynamics (4 binaries)

| Dynamic | Options | Heuristic anchor |
|---|---|---|
| MC Resolve | Change / Steadfast | `decision-heuristic-quick-ref.md` §2 |
| MC Growth | Start / Stop | §3 |
| MC Approach | Do-er / Be-er | §4 |
| MC Mental Sex | Linear / Holistic | §5 |

**AskUserQuestion shape:** one form, 4 binary sub-questions (within HR.A1
cap of 3 — split into 2 turns: Resolve+Growth, Approach+MentalSex).
**Anti-pattern:** *"MC is logical, so must be Linear"* — Logic vs Feeling
is a different distinction (Motivation Elements). Linear/Holistic is
*reasoning strategy*. See [`10-decision-heuristics.md` "Linear vs Holistic — Anti-indicator"](../../../dramatica-theory/references/10-decision-heuristics.md).

### §3.4 Step 4 — Plot Dynamics (4 binaries)

| Dynamic | Options | Heuristic anchor |
|---|---|---|
| Story Driver | Action / Decision | `decision-heuristic-quick-ref.md` §6 |
| Story Limit | Timelock / Optionlock | §7 |
| Story Outcome | Success / Failure | §8 |
| Story Judgment | Good / Bad | §8 |

**Ending Type readout (auto from Outcome × Judgment):**

| | Outcome: Success | Outcome: Failure |
|---|---|---|
| **Judgment: Good** | Triumph | Personal Triumph |
| **Judgment: Bad** | Personal Tragedy | Tragedy |

Render the ending-type label in the Gate 2 status-view so the author sees
the *shape of the ending* immediately after the Dynamics commit. This is
the single best Gate 2 sanity-check.

### §3.5 Step 5 — Plot Story Points

Three sub-sets, written into `architecture.narratives[].story_points`:

1. **Static (must be set):** `goal`, `requirements`, `consequences`, `forewarnings`.
   The Goal MUST be at *Type* level (one of the 16) — see
   `decision-heuristic-quick-ref.md` §9. Goals at Variation or Element
   level are a hard-fail; surface in status-view as `STORY_POINT_LEVEL_TOO_FINE`.

2. **Driver / passenger (often set):** `dividends`, `costs`, `prerequisites`, `preconditions`.

3. **Thematic (per throughline — 6 slots × 4 throughlines = 24 slots):**
   `concern`, `issue`, `problem`, `solution`, `focus`, `direction`. Mostly
   auto-derivable from the worksheet's Quad math; surface unfilled ones in
   the Gate 2 status-view and ask only the ambiguous ones.

**AskUserQuestion shape:** ≤3 slots per turn. Goal first (constrains
everything else). Thematic per-throughline only if the author requests
explicit input — otherwise auto-fill and surface for confirmation.

### §3.6 Step 6 — The Crucial Element

The Crucial Element is **one of the 64 OS Character Elements**. The MC
sits on it; the IC sits on its dynamic-pair partner.

- If MC Resolve = **Change**, the Crucial Element is the *problem* and
  the MC must give it up at the climax.
- If MC Resolve = **Steadfast**, the Crucial Element is the *solution*
  and the MC must hold to it.

**Consistency check (mandatory before Gate 3):**
- Change MC + Element-as-problem ✓
- Steadfast MC + Element-as-solution ✓
- Any other combination → loop back to Step 3 or this Step.

**Worksheet example:** *To Kill A Mockingbird* — Crucial Element is
**INEQUITY**. Scout (MC) is Change, so Inequity is the problem she
gives up (her prejudice against Boo Radley).

**Tooling:** look up the Element + its dynamic-pair partner via
`tools/dramatica-nav/nav.py by-id <element-id> --include-pairs` (AGENTS.md
NO.2 — never coin a free Element name).

### §3.7 Step 7 — Signposts and Journeys

Each throughline progresses through **4 Signposts** (one per Act, at the
throughline's Type level) connected by **3 Journeys** (transitions).
The 4 Signposts MUST be the 4 Types of the throughline's Class.

| Throughline | Sgnpst 1 | Jrny 1→2 | Sgnpst 2 | Jrny 2→3 | Sgnpst 3 | Jrny 3→4 | Sgnpst 4 |
|---|---|---|---|---|---|---|---|
| OS | … | … | … | … | … | … | … |
| MC | … | … | … | … | … | … | … |
| IC | … | … | … | … | … | … | … |
| SS | … | … | … | … | … | … | … |

**Constraint:** order matters and is constrained by other choices, but the
four Signposts must be the four Types of that Class (Type-Quad — see
`dramatica-vocabulary/nav.py by-quad quad.<class>-tp`).

**Detail reference:** `dramatica-theory/references/07-storyencoding.md` for
the full ordering rules.

### §3.8 Step 8 — Optional Genre Mode

Dramatica genre = *Mode of Expression*, not marketing label. Skip on
default; ask only if author requests genre-encoding work. See
`dramatica-theory/references/05-plot-genre.md`.

### §3.9 Validation Pass

Run [`00-storyform-validation.md`](../../../dramatica-theory/references/00-storyform-validation.md)
hard checks. The minimum five:

1. **Dynamic-pair complementarity** — OS+SS are partners; MC+IC are partners.
2. **No character carries both elements of a dynamic pair.**
3. **Goal is at Type level.**
4. **Crucial Element is at Element level.**
5. **MC Resolve ↔ Crucial Element coherence** (Change + problem, or Steadfast + solution).

Validation failures surface in the Gate 3 status-view with their
`00-storyform-validation.md` rule ID; the author can `Edit step N` to
loop back to the violating step *without re-running the whole gate*.

---

## §4 Worked Example — `consciousness-novel` (Hard-SF)

Drop-in walkthrough from Phase 1 → Gate 3. Demonstrates the 8 steps with
the example project `consciousness-novel` (Hard-SF, philosophical horror
overtones, single storyform).

### Phase 2.2 — Step 0 (silent: read intent.yaml)

```yaml
intent.genre: hard_sf
intent.subgenre_modifiers: "Philosophical Horror, Consciousness-First"
intent.core_conflict_question: "Kann ein fragmentiertes Bewusstsein authentisch sein?"
intent.dramatica_storyform_count: single
```

### Phase 2.3 — Step 1 (askuser turn 1)

| Throughline | Author's answer |
|---|---|
| OS | "The community of fragmented minds trying to reach consensus on what counts as a self" |
| MC | "Lena — a consciousness-researcher who herself begins to fragment" |
| IC | "Dr. Vey — Lena's former mentor, who insists fragmentation is liberation" |
| SS | "Lena ↔ Vey — the teacher-becomes-the-mirror relationship" |

→ **Gate 1: Approve** (storyform shape = single + all 4 throughlines named).

### Phase 2.4 — Step 2 (askuser turn 2)

- **OS = Mind.** ("the community's *frozen attitude* about selfhood" — quick-ref §1, Mind row.)
- SS = Universe (pair partner).
- **MC = Psychology.** ("Lena's *shifting* internal manipulation — self-deception, scheming with her own fragments" — quick-ref §1, Psychology row.)
- IC = Physics (pair partner — Vey *does things to* Lena, not *believes* against her).

### Phase 2.5 — Step 3 (askuser turn 3, 4 binaries split)

- **MC Resolve = Change.** (Lena abandons her core driving Element.)
- **MC Growth = Start.** (Growing *into* something she lacks: integration.)
- **MC Approach = Be-er.** (Adapts herself to the world; doesn't act on it.)
- **MC Mental Sex = Holistic.** (Pattern-relational, multiple threads at once.)

### Phase 2.6 — Step 4 (askuser turn 4)

- **Story Driver = Decision.** (Lena's *choices about which fragment to trust* force the actions, not the other way around.)
- **Story Limit = Optionlock.** (Finite set of possible integrations; story ends when the last one fails or holds.)
- **Story Outcome = Failure.** (The OS Goal — community consensus — is not achieved.)
- **Story Judgment = Good.** (Lena lands in a satisfied internal state regardless.)

→ Ending type readout: **Personal Triumph**.

### Phase 2.7 — Step 5 (askuser turn 5)

- **Goal (Type-level, OS=Mind):** *Memory* — the community's struggle is to remember what selfhood once was.
- **Requirements:** "Each fragment must witness another fragment's experience."
- **Consequences:** "The community accepts permanent dissolution as the new baseline."
- **Forewarnings:** "Early-act consensus failures."
- Thematic per-throughline auto-filled from Quad math (Lena's MC issue: *Confidence*; Vey's IC issue: *Worry*; etc.).

→ **Gate 2: Approve** (Classes + Dynamics + Story Points all coherent).

### Phase 2.8 — Step 6 (askuser turn 6)

- **Crucial Element: SELF-INTEREST.** (OS=Mind → look up Mind's 64 Elements via `nav.py`.) Lena (Change MC) must give it up.
- **IC's opposing Element (dynamic-pair partner): MORALITY.** Vey holds it.
- **Consistency check:** Change MC + Element-as-problem ✓.

### Phase 2.9 — Step 7 (askuser turn 7)

Type-Quad for Mind = {Memory, Preconscious, Conscious, Subconscious}.

| | Sgnpst 1 | Sgnpst 2 | Sgnpst 3 | Sgnpst 4 |
|---|---|---|---|---|
| OS (Mind) | Memory | Preconscious | Conscious | Subconscious |
| MC (Psychology) | Conceiving | Being | Becoming | Conceptualizing |
| IC (Physics) | Understanding | Doing | Learning | Obtaining |
| SS (Universe) | Past | Progress | Present | Future |

### Phase 2.11 — Validation pass (silent)

All five hard checks pass. → **Gate 3: Approve**.

### Phase 2.14 — Write architecture.yaml + NCP skeleton

`architecture.yaml` written with `approved: true`. `canon/consciousness-novel.ncp.json`
written via `ncp-author`. Total askuser turns: **7** (within the 10-turn cap).

---

## §5 Hard Rules (this method)

- **HR.M2.1 — One step per turn.** Each askuser commits one worksheet
  step's slots (or fewer if HR.A1's 3-slot cap forces splitting). Never
  ask Step 3 + Step 4 + Step 5 in one form.
- **HR.M2.2 — Backtrack on contradiction.** If a later step exposes a
  contradiction in an earlier one, surface in status-view as
  `WORKSHEET_BACKTRACK_<step>` and ask the author to revise. Do not
  silently *fix* the earlier step.
- **HR.M2.3 — Decision heuristics inline.** Every Step 2–7 askuser MUST
  include a one-paragraph excerpt from `decision-heuristic-quick-ref.md`
  in the status-view, not just a link. Authors with no Dramatica background
  cannot follow "consult dramatica-theory".
- **HR.M2.4 — Ontology-first for all named slots.** Class, Type,
  Variation, Element, and Type-Quad names go through
  `tools/dramatica-nav/nav.py` (AGENTS.md **NO.2**). Free-coined names
  are a Schema-drift defect — auto-reject in status-view.
- **HR.M2.5 — Validation pass is mandatory.** Gate 3 cannot approve
  until all 5 `00-storyform-validation.md` hard checks pass. Failures
  loop back to the violating step.

---

## §6 Anti-Patterns Specific to This Method

| Anti-pattern | Why it fails | Detection |
|---|---|---|
| Skip Step 0 (read `intent.yaml`) | Premise/thematic argument missing → Step 5 Goal is ungrounded | Status-view shows empty premise → fail Gate 1 |
| Pick Class for MC *before* OS | Constraint reversed; MC's options should narrow *to* 2 once OS is fixed | quick-ref §1 |
| Conflate Outcome with Judgment | Collapses "happy ending vs sad ending"; loses Personal Triumph / Personal Tragedy | quick-ref §8 anti-indicator |
| Coin a Crucial Element name | NCP schema-drift; ontology-lookup fails at validation | HR.M2.4 |
| "Mostly Decision Driver, some Action" | Driver is a constant across the storyform, not a mix | quick-ref §6 anti-indicator |

Cross-reference: `dramatica-theory/references/11-anti-patterns.md` for
the full theoretical anti-pattern set.

---

## §7 NCP Slot Mapping (what each Worksheet step writes)

| Worksheet step | NCP path | Writer |
|---|---|---|
| 1 — Throughlines (names) | `narratives[].subtext.perspectives[]` (4 entries: OS/MC/IC/SS, name only) | Phase 2.3 → ncp-author |
| 2 — Classes | `narratives[].subtext.perspectives[].class_ref` | Phase 2.4 → ncp-author |
| 3 + 4 — Dynamics | `narratives[].subtext.dynamics[]` (8 entries) | Phase 2.5 + 2.6 → ncp-author |
| 5 — Story Points (static + thematic) | `narratives[].subtext.storypoints[]` | Phase 2.7 → ncp-author |
| 6 — Crucial Element | `narratives[].subtext.storypoints[].kind == "crucial_element"` + `dynamic_pair_partner` | Phase 2.8 → ncp-author |
| 7 — Signposts/Journeys | `narratives[].subtext.storybeats[]` (16 signposts + 12 journeys per single storyform) | Phase 2.9 → ncp-author |

NCP validation runs after each Gate's writes, not at the end —
fail-loud per Phase 2.6 / 2.7.

---

## §8 Failure Modes & Recovery

| Symptom | Likely cause | Recovery |
|---|---|---|
| Can't name SS in Step 1 | Premise unclear → MC↔IC relationship undefined | Loop back to Phase 1, rewrite `core_conflict_question` |
| Class pair constraint violated in Step 2 | OS+MC both in Universe (or both in Mind/Physics/Psychology) | Surface in status-view; force pick which one stays |
| MC Resolve doesn't match Crucial Element in Step 6 | Step 3 or Step 6 wrong | Loop back: re-evaluate Resolve *or* re-pick Element |
| Goal at Variation/Element level in Step 5 | Author zoomed past Type | Surface `STORY_POINT_LEVEL_TOO_FINE`; show quick-ref §9 |
| Signpost Types don't match Class in Step 7 | Free-coined Type names instead of nav.py lookup | Reject; force `nav.py by-quad quad.<class>-tp` |

---

## §9 Bilingual Contract

Method **prose** is German (DE) per [SKILL.md "Bilingual Contract (DE/EN)"](../../SKILL.md);
**schema, slot names, NCP enum strings, and code identifiers** are English (EN).
The Worksheet uses English term names (Class, Throughline, Crucial Element,
Optionlock, …) because they are NCP enum strings — translating them would
break schema lookup. Quick-ref headings (§1 Class Choice, §2 Change vs
Steadfast, …) follow the worksheet term, not a German calque.

---

## §10 Versioning

- **v1.0.0** (this file, Task 072) — initial 8-step Worksheet-Loop method
  for `novel-architect@1.0.0` Phase 2. Sub-Phase numbering 2.1–2.14
  matches `phases/phase2-narrative-architecture.md` §2.
- **Forward-compat:** when Task 071 lands (`novel-architect-structure/`
  sub-skill split), this file will `git mv` to
  `skills/novel-architect-structure/methods/storyform/worksheet-workflow.md`
  unchanged. All links above are relative; the move preserves them.
