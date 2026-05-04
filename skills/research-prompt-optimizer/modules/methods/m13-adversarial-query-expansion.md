---
id: M13
type: method
file: "modules/methods/m13-adversarial-query-expansion.md"
full_name: "Adversarial Query Expansion"
short_anchor: "M13-AdversarialQueryExpansion"
mandatory: true
applies_to_categories: [A, B, C]
default_for: [A, B, C]
triggered_by_signals: []
pairs_well_with: []
escape_criterion: "Stop expanding an axis when 2 consecutive expansions produce no novel findings; full method terminates only at Pre-Synthesis Integrity Check"
when_to_choose_short: "Always-on; minimum once per 10-minute window"
self_applied_phase2:
  sub_phase: "4.6"
  hook_role: "Before auto-generating adjacent/opposing/abstraction axes, reflect on the conceptual direction the initial seed-vocabulary pushes toward. Adjust auto-axes before bundled askuser. Without this hook, all 4 axes drift to local minimum."
  depth_active: ["standard", "exhaustive"]
slots:
  seed_vocabulary:
    type: phase2_fill
    description: "Initial query vocabulary the agent expands from"
    required: true
    fill_from_intent: "intent.research_question"
    fill_from_intent_strategy: "extract_keywords"
  orthogonal_lens:
    type: phase2_fill
    description: "A lens not present in the framing — the highest-leverage axis"
    required: true
    fill_from_intent: null
    ask_user_if_missing:
      question: "Welche orthogonale Linse hat in deiner Frage bisher niemand angesetzt?"
      type: single_select_with_other
      phase: "2.6_bundled"
  adjacent_term:
    type: agent_runtime_fill
    description: "Synonyms / neighbouring sub-fields the agent expands during run"
  opposing_term:
    type: agent_runtime_fill
    description: "Failure cases / opposite school the agent expands"
  higher_level_term:
    type: agent_runtime_fill
    description: "Up-abstraction term the agent expands"
  lower_level_term:
    type: agent_runtime_fill
    description: "Down-abstraction term the agent expands"
---

# M13 — Adversarial Query Expansion (MANDATORY in every prompt)

> **v3.0 sample module.** This method shows the **mixed slot pattern**:
> two `phase2_fill` slots (filled at composition time, one from intent,
> one from the bundled askuser in Phase 2.6) plus four
> `agent_runtime_fill` slots (the agent expands these during the run).
>
> M13 is the only mandatory critical-thinking method — it is in
> every generated prompt regardless of category.

## Rendered Block (composed into the research prompt)

```markdown
### Method: Adversarial Query Expansion

**What it is:** A standing directive that requires you — the executing
agent — to **autonomously expand the search vocabulary** at defined
checkpoints during the run. You are not bound to the query terms given
in the initial prompt; you are obligated to outgrow them. The purpose
is to prevent **local-minimum lock-in**, where the agent iterates within
a narrow semantic neighborhood of the user's phrasing and misses the
adjacent, opposing, or higher-abstraction evidence that would change
the answer.

**Why it is in this prompt:** The initial query vocabulary carries the
user's framing — including the user's blind spots. If your search stays
inside that vocabulary, your conclusions will be shaped by the same
blind spots. Critical thinking requires the queries themselves to be
critically expanded, not just the findings critically evaluated.

**How to apply it — step by step:**

1. **Build a Seed Query Set.** Your starting vocabulary for this run
   is `{{seed_vocabulary}}` (extracted at composition time from the
   research question). Begin from this set; do not narrow it further.

2. **Expand along four axes at every major checkpoint.** After every
   batch of searches (or every 10 minutes of agentic time, whichever
   is sooner), generate new queries along each of these axes and
   execute the most promising one per axis:

   - **Adjacent axis** — synonyms, related sub-fields, neighbouring
     disciplines, equivalent industry terms, other-language terms.
     You generate `{{adjacent_term}}` candidates during the run.
     Example: "AI Act compliance" → "Rechtssicherheit KI",
     "algorithmic accountability".

   - **Opposing axis** — the negation, the failure case, the opposite
     school of thought, the "X doesn't work" literature. You generate
     `{{opposing_term}}` candidates during the run. Example: "benefits
     of microservices" → "microservices failure modes".

   - **Abstraction axis** — step one level up or down. Up: the category
     the topic belongs to. Down: a concrete sub-case. You generate
     `{{higher_level_term}}` and/or `{{lower_level_term}}` during the
     run. Example: "ChatGPT enterprise adoption" ↑ "LLM enterprise
     adoption"; ↓ "ChatGPT in pharmaceutical R&D".

   - **Orthogonal axis** — an angle the original framing did not
     consider at all. **For this run, the orthogonal lens is
     pre-specified by the user as: `{{orthogonal_lens}}`.** Execute
     queries from that lens. (Other orthogonal lenses may also surface
     during the run; log them, but the pre-specified lens is the one
     you must invoke at minimum.)

3. **Log every expansion.** Maintain a **Query Expansion Log** in your
   working notes: for each expansion, record (a) the axis, (b) the new
   query, (c) whether the search returned novel findings not covered
   by the seed set, (d) whether those findings modified a tentative
   conclusion. This log is included in the final output's Synthesis
   section.

4. **Feed expansions back into hypotheses / schema fields.** If an
   expansion surfaces a finding that contradicts or enlarges the
   current working answer, treat it as a first-class input: re-run the
   relevant Restatement Checkpoint, update the Contradiction Log,
   consider whether it merits a new hypothesis branch (Category A),
   a new schema row (Category B), or a World-Change Log entry
   (Category C).

5. **Drive the expansion by reflection, not by token budget.** Before
   each expansion pass, pause and write one sentence answering:
   *"What am I most likely missing right now, and why?"* The answer
   selects which of the four axes to prioritize this pass.

**When to stop / escape criterion:** Stop expanding a single axis when
two consecutive expansions along that axis produce no novel findings.
Do not stop the method as a whole until every axis has been exhausted
in this sense. The full method only terminates at the Pre-Synthesis
Integrity Check.

**Example trigger in this research context:** Your seed vocabulary is
`{{seed_vocabulary}}`. Your pre-specified orthogonal lens is
`{{orthogonal_lens}}`. After the first search batch, you generate one
candidate per axis: adjacent (`{{adjacent_term}}`), opposing
(`{{opposing_term}}`), abstraction (`{{higher_level_term}}` or
`{{lower_level_term}}`), and execute one query from the orthogonal
lens. You log all four in the Query Expansion Log before continuing.

**Hard anti-rationalization rule:** If you catch yourself thinking *"the
seed vocabulary is already comprehensive"*, that is the signal to
expand — not the signal to skip. The feeling of completeness inside a
narrow vocabulary is precisely what the local-minimum failure feels
like from the inside.
```

---

## Notes on the Slot Treatment (v3.0)

The two `phase2_fill` slots are filled at composition time:

- **`seed_vocabulary`** — Phase 2 extracts the salient noun-phrases
  from `intent.research_question` (typically 3-6 keywords). This is the
  "starting vocabulary" the agent expands from.

- **`orthogonal_lens`** — Phase 2 collects this in the bundled
  Phase 2.6 askuser. The user names a lens (economic / historical /
  legal / ...) that the original framing did not cover. This is the
  highest-leverage M13 axis and the one most prone to local-minimum
  lock-in if Claude generates it alone.

The four `agent_runtime_fill` slots stay as placeholders in the rendered
prompt. The agent generates them during execution.

## Phase 2 Behaviour

When M13 is selected (always — mandatory), Phase 2:

- Adds M13 to `selected_methods` (always last in the list)
- Extracts seed vocabulary from `intent.research_question`
- Asks the user for orthogonal lens in the Phase 2.6 bundled turn
  (together with seed query confirmation)
- Populates `slot_fills.M13.seed_vocabulary` and
  `slot_fills.M13.orthogonal_lens`

The rendered block above goes into the research prompt with the two
`phase2_fill` slots substituted; the four `agent_runtime_fill` slots
remain as `{{placeholder}}` text.
