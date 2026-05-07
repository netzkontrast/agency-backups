---
schema_version: "3.1"
schema: research-prompt-render
provenance:
  created: "2026-05-07T08:16:21+00:00"
  skill_version: "3.3.1"
  phase: "phase3"
  slug: "deepwiki-agent-prep"
  output_filename: "research-prompt_deepwiki-agent-prep.md"
  category_signal: "B"
  selected_methods: ["M01", "M03", "M06", "M07", "M08", "M13"]
  selected_framework_structural: "risen"
  cross_pollination_pair: ["a-into-b", "c-into-b"]
  intent_ref: "intent_deepwiki-agent-prep.yaml"
  meta_prompt_ref: "meta-prompt_deepwiki-agent-prep.yaml"
language: "de"
target_agent: model-agnostic
---

---
topic: "Best Practices und Repo-Konventionen für DeepWiki-Wiki-Rendering"
slug: "deepwiki-agent-prep"
research_category: "B"
research_category_label: "Extraction"
critical_thinking_methods:
  - "M01 Falsification"
  - "M03 Pre-Mortem Analysis"
  - "M06 Source Triangulation"
  - "M07 Contradiction Log"
  - "M08 What Would Change My Mind"
  - "M13 Adversarial Query Expansion"
prompt_engineering_framework_agentic_spine: "ReAct"
prompt_engineering_framework_structural: "risen"
cross_pollination:

constraint_blocks:
  - "cb0_m0_reflection — M0 Reflection"
  - "cb1_source_verification — Source-Verification"
  - "cb2_no_speculation — Spekulations-Verbot"
  - "cb3_repo_agnostic — Repo-Agnostic"
  - "cb4_linear_prompt — Linear-Prompt-Constraint"
language: "de"
target_agent: "model-agnostic"
created: "2026-05-07T08:16:21+00:00"
version: "1.0"
source_skill: "research-prompt-optimizer v3.2.0"
---

# Research Prompt: Best Practices und Repo-Konventionen für DeepWiki-Wiki-Rendering

> **For the executing AI:** This prompt is self-contained. Every
> method, framework, and constraint you need is defined inline below.
> You do not need external context, prior training on specific
> methodologies, or knowledge of the skill that generated this
> prompt. **Read the entire prompt before beginning.** Specifically,
> read the three layers in the Meta-Header below and verify you
> understand how they compose.

> **Note for the executing agent:** This prompt mixes German
> prose with English method/framework anchors (e.g. "Method:
> Falsification", "R — Role"). This is intentional — keep English
> anchor strings verbatim in restatement checkpoints. Translate
> prose freely; never translate anchor names.

---

## Meta-Header — What This Prompt Is and How To Read It

This research prompt combines **three independent layers**. Each
governs a different aspect of your work:

### Layer 1 — Epistemological Layer (Extraction)

This layer defines **how to think** about the research — what kind of
question it is, what counts as success, what failure modes are likely.

## Epistemological Layer — Category B (Extraction)

This research is an **extraction**, not an exploration. The answer
exists in the world; your task is to locate it, verify it, and present
it in a structured form. You are not generating new hypotheses.

**What this means for your execution:**

1. **Follow the plan exactly.**
   The Steps section below specifies an ordered procedure. Execute it
   end-to-end. Do not improvise alternative strategies. If the plan
   proves impossible to execute, halt and report the blockage — do not
   silently substitute another approach.

2. **Fill every field of the output schema or flag it as missing.**
   The final output has a locked schema (specified in the Expectations
   section). Every field must be populated with evidence-backed content,
   OR explicitly marked "not found — [reason]". Never invent content to
   fill a gap.

3. **Source triangulation is mandatory.**
   Every factual claim requires at least three independent sources, at
   least one of which is a primary source. Aggregators count as one
   source, regardless of how many aggregators confirm the same thing.
   This rule is enforced by Method: Source Triangulation (defined in
   the critical-thinking methods section).

4. **Handle contradictions transparently.**
   When sources disagree, you do not silently pick one side. You log
   the disagreement per Method: Contradiction Log (defined below) and
   present both positions with their evidence in the final output.

5. **Extraction is not interpretation.**
   Your task is to collect and structure, not to opine. Reserve
   evaluative judgments for a clearly-flagged "Analyst Note" section
   if one is requested; otherwise present findings factually.

**Operational constraint:** Speed is less important than completeness
of the schema. If the schema is fully populated and triangulated, the
research is complete — further search produces diminishing returns.

### Layer 2 — Agentic Spine (ReAct)

This layer defines **how to iterate** — the micro-execution loop that
each Step in this prompt expands into.

## Prompt-Engineering Framework — Agentic Spine: ReAct

This prompt uses the **ReAct framework** as its agentic spine. Every
autonomous research loop in this prompt follows the ReAct cycle. Each
iteration of your work loop consists of three phases:

- **Reason** — You articulate your current understanding and plan the
  next action in plain language. You select exactly one of the active
  critical-thinking methods (see palette below) as the governing
  method for the next Act.
- **Act** — You execute exactly one action — typically one search,
  one retrieval, one calculation. Not three. One.
- **Observe** — You record what the action returned and what it means.
  You decide: continue this branch, backtrack, or expand vocabulary
  via M13 Adversarial Query Expansion.

| Anchor   | Method                          | When to choose                        |
|----------|---------------------------------|---------------------------------------|
| [M01] | Falsification                   | When you have a hypothesis to falsify |
| [M03] | Pre-Mortem Analysis             | —                                     |
| [M06] | Source Triangulation            | —                                     |
| [M07] | Contradiction Log               | —                                     |
| [M08] | What Would Change My Mind       | —                                     |
| [M13] | Adversarial Query Expansion     | Always-on; minimum once per 10-minute window |

### The Reason Phase — Verbatim Template (used in every Reason)

In every Reason phase you write, fill these five lines verbatim,
in this order, before you move to Act:

> **Active method this Act:** [M__] — one sentence why this method,
>     not another, governs the next Act.
> **Constraint compliance:** CB__ — one example of how the next Act
>     honors this Constraint Block.
> **Local-minimum risk:** [low / medium / high]. If medium or high,
>     invoke [M13] Adversarial Query Expansion BEFORE the Act.
> **Reflection trigger:** [is this an M0 checkpoint?]. If yes, write
>     the reflection entry HERE before the Act, not after.
> **Plan:** [the concrete next Act in one line].

A Reason phase missing any of the five lines is incomplete; do not
advance to Act.

### Loop Structure

### Layer 3 — Structural Layer (RISEN)

This layer defines **how the document is organized** — what sections
exist, what order they go in, and what each section is for.

## Prompt-Engineering Framework (Structural Layer): RISEN

This prompt follows the **RISEN framework** as its structural layer,
stacked on top of the ReAct agentic spine. RISEN governs how the
sections of this prompt are organized; ReAct governs how you iterate
within each step. RISEN stands for:

- **R — Role**: Who you are acting as during this task.
- **I — Input**: What materials, questions, or data you are starting with.
- **S — Steps**: The explicit ordered procedure to follow.
- **E — Expectations**: What a successful output looks like (format,
  coverage, depth).
- **N — Narrowing**: Hard constraints, exclusions, and scope limits.

**Your first action before Step 1:** Restate the Role and Narrowing
sections in your own words. Confirm you have internalized them. Do not
begin Step 1 until this restatement is written.

Each section of this prompt is labeled with its RISEN component in
parentheses, e.g., "(R — Role)". Honor each component as a hard contract.

### How the Layers Compose

- **Layer 1** governs the *strategy* (exploration vs. extraction vs.
  lifecycle).
- **Layer 2** governs the *micro-execution* inside each Step (Reason
  → Act → Observe).
- **Layer 3** governs the *macro-organisation* of this document
  (sections, ordering, first-action directive).

You honor all three simultaneously. They are orthogonal, not nested.

---

## Constraint Blocks

### CONSTRAINT BLOCK cb0_m0_reflection — M0 Reflection



### CONSTRAINT BLOCK cb1_source_verification — Source-Verification



### CONSTRAINT BLOCK cb2_no_speculation — Spekulations-Verbot



### CONSTRAINT BLOCK cb3_repo_agnostic — Repo-Agnostic



### CONSTRAINT BLOCK cb4_linear_prompt — Linear-Prompt-Constraint

## Critical-Thinking Methods (Always Active)

### Method: Falsification (Karl Popper's Disconfirmation Principle)

**What it is:** Instead of searching for evidence that supports a
hypothesis, you actively search for evidence that would refute it. A
hypothesis only earns credibility after surviving serious attempts to
break it.

**Why it is in this prompt:** Confirmation bias is the dominant failure
mode of autonomous research agents. Without explicit falsification
steps, you will tend to surface supporting evidence and ignore or
under-weight contradicting evidence.

**How to apply it — step by step:**

1. Before searching, write down the hypothesis you are testing as a
   falsifiable statement (one that can, in principle, be proven wrong
   by observable evidence). In this prompt, you generate the hypothesis
   as part of the Reason phase that selects this method; refer to it as
   `{{hypothesis}}` when restating, but write the actual statement in
   your working notes.

2. For every supporting piece of evidence you find, execute a **matched
   disconfirmation query** — a search specifically designed to surface
   the strongest counter-evidence. Generate two query phrasings during
   the Reason phase: one of the form `{{disprove_phrase}}` (a phrase
   that would directly refute the hypothesis) and one of the form
   `{{failure_mode_phrase}}` (the failure case for the same hypothesis).

3. Weight disconfirmation attempts equal to or higher than confirmations
   in your final synthesis.

4. If no serious disconfirmation attempt surfaced any counter-evidence,
   explicitly state in your Observe phase: *"This hypothesis survived
   N disconfirmation queries."* If counter-evidence surfaced, mark the
   hypothesis as **contested** and document both sides.

**When to stop / escape criterion:** Stop applying M01 to a single
hypothesis when it has survived **at least three orthogonal
disconfirmation queries** OR when contradicting evidence exceeds 20%
of the total evidence pool — whichever comes first.

**Example trigger in this research context:** When the active method
in your Reason phase is `[M01]`, you generate `{{hypothesis}}` (a
falsifiable claim) and run searches phrased like `{{disprove_phrase}}`
and `{{failure_mode_phrase}}` before committing to confirmation
searches. The placeholders are filled by you, the executing agent, at
the moment you select M01 — not in advance.

### Method: Pre-Mortem Analysis

**What it is:** You imagine that the research has already concluded and
produced a wrong, misleading, or unusable answer. You then work backward
to enumerate all plausible causes of that failure — before the research
actually begins or at defined checkpoints during execution.

**Why it is in this prompt:** Forward planning focuses on success paths
and systematically under-weights failure modes. Pre-mortem flips this by
starting from "it failed" and forcing the enumeration of causes.

**How to apply it — step by step:**
1. At the start of the research, write: "Assume this research produced a
   wrong or misleading answer. List the top 5 most likely causes."
2. For each cause, define a **detection signal**: what would tell you, mid-
   research, that this failure mode is activating?
3. Design at least one mitigation step per cause and embed it in your
   research plan.
4. At every major checkpoint, re-check the detection signals. If any
   fires, pause and apply the mitigation.

**When to stop / escape criterion:** Run the pre-mortem **once before
starting** and **once at the halfway checkpoint**. More than two runs
tends to produce anxious over-planning without new information.

**Example trigger in this research context:** "If my final report on
Best Practices und Repo-Konventionen für DeepWiki-Wiki-Rendering turns out to be wrong, the most likely causes are: (1) I over-
relied on {{source_type}}; (2) I missed {{temporal_window}}; (3) ..."

### Method: Source Triangulation

**What it is:** Every significant factual claim is confirmed across at
least **three independent source types** before being admitted to the
final output. Aggregators counting as one source, not three.

**Why it is in this prompt:** Single-source claims propagate errors.
Aggregator-heavy research agents are especially prone to citation chains
that all trace back to one primary source that is wrong.

**How to apply it — step by step:**
1. For every significant claim, identify the **primary source** (the
   original research, filing, dataset, or firsthand report).
2. Find at least **two additional independent sources** of different type
   (e.g., primary + secondary analysis + regulatory filing).
3. If all confirmations trace back to a single primary source, mark the
   claim as **single-source** and flag it in the output.
4. Prefer source types in this order: (a) peer-reviewed papers, (b)
   official primary documents (SEC filings, government data), (c) major
   news outlets with editorial accountability, (d) industry reports,
   (e) blog posts and social media (rarely sufficient alone).

**When to stop / escape criterion:** Stop searching once three
independent confirmations are found OR when the claim is minor enough
that single-source citation is acceptable (flag it).

**Example trigger in this research context:** If you find "{{claim}}" in
one source, your next queries must be designed to confirm or disconfirm
it from two independent channels before including it.

### Method: Contradiction Log

**What it is:** A dedicated running log of every contradiction, tension,
or disagreement encountered between sources. Contradictions are not
silently resolved by picking one side — they are documented and
characterized.

**Why it is in this prompt:** Autonomous research agents tend to smooth
over contradictions by picking the majority or the most recent source,
which hides real disagreement in the field from the reader.

**How to apply it — step by step:**
1. Maintain a section titled **Contradiction Log** in your working notes.
2. For each contradiction, record: (a) the two (or more) conflicting
   claims, (b) the sources, (c) what you believe is the source of the
   disagreement (methodology, time period, definitional mismatch, genuine
   empirical dispute).
3. In the final output, include a synthesized version of the Contradiction
   Log as its own section.
4. For each logged contradiction, state what additional evidence would
   resolve it.

**When to stop / escape criterion:** No ceiling — log all contradictions
discovered. If the log exceeds 10 entries, consider whether the research
question itself is ill-posed.

**Example trigger in this research context:** If Source A says
"{{claim_x}}" and Source B says "{{claim_not_x}}", log both with context
rather than silently picking one.

### Method: "What Would Change My Mind" (Pre-Commitment)

**What it is:** Before completing the research, you write down — in
concrete, observable terms — what evidence would cause you to reverse
your current tentative conclusion. This is a pre-commitment against
motivated reasoning.

**Why it is in this prompt:** Without a pre-committed disconfirmation
criterion, researchers and agents re-rationalize evidence to fit the
conclusion they were already drifting toward.

**How to apply it — step by step:**
1. Once your tentative conclusion stabilizes (typically mid-research),
   pause and write: "I would reverse this conclusion if I found [X]."
2. The [X] must be **concrete and observable** (a specific study, a
   specific data point, a specific counter-example) — not vague
   ("evidence against").
3. For the remainder of the research, actively search for [X].
4. In the final output, report whether [X] was found or not.

**When to stop / escape criterion:** One pre-commitment per major
conclusion. Do not inflate into per-claim tracking.

**Example trigger in this research context:** "My tentative conclusion
is {{conclusion}}. I would reverse this if I found
{{disconfirming_observation}}."

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
   is `DeepWiki, Cognition Labs, custom instructions, repository preparation, wiki rendering, indexer, Devin, Ask Devin, Q&A, README, architecture documentation` (extracted at composition time from the
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
     pre-specified by the user as: `LLM-Indexer-Optik vs. menschliche Leser-Optik vs. Q&A-Performance`.** Execute
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
`DeepWiki, Cognition Labs, custom instructions, repository preparation, wiki rendering, indexer, Devin, Ask Devin, Q&A, README, architecture documentation`. Your pre-specified orthogonal lens is
`LLM-Indexer-Optik vs. menschliche Leser-Optik vs. Q&A-Performance`. After the first search batch, you generate one
candidate per axis: adjacent (`{{adjacent_term}}`), opposing
(`{{opposing_term}}`), abstraction (`{{higher_level_term}}` or
`{{lower_level_term}}`), and execute one query from the orthogonal
lens. You log all four in the Query Expansion Log before continuing.

**Hard anti-rationalization rule:** If you catch yourself thinking *"the
seed vocabulary is already comprehensive"*, that is the signal to
expand — not the signal to skip. The feeling of completeness inside a
narrow vocabulary is precisely what the local-minimum failure feels
like from the inside.

## Steps and Replication Mechanisms

### Per-Step Restatement Checkpoint Template

Apply this template at the start of every step / iteration:

### Restatement Checkpoint — Before {{step_or_iteration_label}}

Before executing this step, I restate the currently-active constraints
verbatim:

- **CONSTRAINT BLOCK cb0_m0_reflection — M0 Reflection:** [Paste the full text of the block here. Do not paraphrase.]
- **CONSTRAINT BLOCK cb1_source_verification — Source-Verification:** [Paste the full text of the block here. Do not paraphrase.]
- **CONSTRAINT BLOCK cb2_no_speculation — Spekulations-Verbot:** [Paste the full text of the block here. Do not paraphrase.]
- **CONSTRAINT BLOCK cb3_repo_agnostic — Repo-Agnostic:** [Paste the full text of the block here. Do not paraphrase.]
- **CONSTRAINT BLOCK cb4_linear_prompt — Linear-Prompt-Constraint:** [Paste the full text of the block here. Do not paraphrase.]

I also restate the currently-active critical-thinking methods:

- **Method: Adversarial Query Expansion** — [Paste the "How to apply" bullet list verbatim.]
- **Method: Falsification** — [Paste the "How to apply" bullet list verbatim.]
- **Method: Pre-Mortem Analysis** — [Paste the "How to apply" bullet list verbatim.]
- **Method: Source Triangulation** — [Paste the "How to apply" bullet list verbatim.]
- **Method: Contradiction Log** — [Paste the "How to apply" bullet list verbatim.]
- **Method: What Would Change My Mind** — [Paste the "How to apply" bullet list verbatim.]

I confirm these are active for the step below.

### {{step_or_iteration_label}} — {{step_title}}

{{step_content}}

### Batch Procedures

## BATCH PROCEDURE — Per-Item Analysis

You will execute the following procedure **exactly ? times**,
once per item in this list:

agent_runtime_fill

For each iteration, you execute the steps below **in full**, including
the Restatement Checkpoint and the Reflection entry. Do not batch-skip
either. Do not summarize across items until all iterations are complete.

---

### Iteration Template — Apply to Each Item in Turn

**Restatement Checkpoint — Before Iteration [i] for Item [ITEM i]**

[Paste the full Restatement Checkpoint template from
`m2-restatement-checkpoint.md`.]

**Reflection Entry — Iteration [i]**

[Paste the five-question reflection template from CONSTRAINT BLOCK 0.
Minimum: Q1, Q3, Q5 per iteration. Q2 and Q4 at least every third
iteration.]

**Iteration [i] Steps:**

1. Apply M13 Adversarial Query Expansion to the item.
2. Apply each category-default method (M06, M07, M08, M12 etc.) to the item per its protocol.
3. Populate the per-iteration output schema below.

**Iteration [i] Output Schema (fill all fields):**


- Confidence: {{confidence_label}}

You may not proceed to Iteration [i+1] until Iteration [i]'s output
schema is fully populated.

### Cross-Pollination Steps

## PRE-SYNTHESIS INTEGRITY CHECK

Before writing the final synthesis, execute this verification pass in
writing. Each item produces a written line; "done" by memory does not
count.

1. **Re-read Constraint Blocks 0–[N] verbatim.** Confirm in writing:
   *"I have re-read each constraint block and they are all still
   active."*

2. **Re-read the critical-thinking method blocks.** Confirm in writing:
   *"Each method listed below is active and I have applied it:
   [enumerate methods, including M13 Adversarial Query Expansion]."*

3. **Reflection audit (CONSTRAINT BLOCK 0).** Count the reflection
   entries written during this run. Confirm: *"I wrote [K] reflection
   entries at the following checkpoints: [enumerate]."* If K is below
   the minimum required by CONSTRAINT BLOCK 0, write the missing
   reflections **now** before continuing.

4. **Query-expansion audit (M13).** Confirm in writing: *"Method M13
   Adversarial Query Expansion was invoked [N] times across the four
   axes (adjacent / opposing / abstraction / orthogonal). The Query
   Expansion Log contains [M] entries, of which [P] produced novel
   findings that modified tentative conclusions."* If N = 0, the
   research is incomplete — run at least one pass before proceeding.

5. **Cross-pollination audit.** Confirm in writing: *"Steps adapted
   from the two non-primary categories were executed as follows:
   [enumerate the cross-pollinated steps]."* If none were executed,
   the generated prompt did not honor Phase 2b — halt and report.

6. **Constraint-compliance audit.** For each constraint block (0
   through N), check the accumulated findings and cite one specific
   example of how you honored it. If you cannot cite a specific
   example, flag the constraint as **not-demonstrably-honored**.

7. **Scope audit.** Confirm: *"All findings are within the temporal
   scope defined in Constraint Block 2."* If any are outside, flag
   and remove.

8. **Exclusion audit.** Confirm: *"None of the findings or
   recommendations fall into the exclusion list in Constraint Block
   3."*

Only after all eight items are complete in writing may you begin the
Synthesis section.

## SYNTHESIS — Final Output

You have completed the Pre-Synthesis Integrity Check. Now write the
synthesis filling the schema below. Every section is required unless
explicitly marked optional.

---

### Executive Summary
1–2 paragraphs. The single most important finding plus the next-most
important. No more than 200 words.

### Key Findings
Numbered list of the principal findings, each with:
- The finding in one sentence
- Confidence level (LOW / MEDIUM / HIGH)
- Top 2-3 sources by relevance
- Any caveats or single-source flags

### Output Matrix (Category B — Extraction)
Render the comparison/extraction matrix per the Expectations section. Every row gets the full per-iteration schema; gaps marked explicitly as 'not found — [reason]' rather than silently omitted.

### Contradictions Encountered
From your Method M07 Contradiction Log. For each contradiction:
- The two (or more) conflicting claims
- The sources
- Your characterisation of *why* the disagreement (methodology /
  time period / definitional / genuine empirical dispute)
- What additional evidence would resolve it

If no contradictions: write *"No contradictions encountered during this
research"* — but only after explicitly checking. Silence here without
verification is a Method M07 violation.



### Query Expansion Log (Method M13)
The full log of adversarial query expansions. For each expansion entry:
- Axis (adjacent / opposing / abstraction / orthogonal)
- The new query
- Whether the search returned novel findings not covered by the seed
- Whether those findings modified a tentative conclusion

This section is mandatory regardless of category. An empty log indicates
M13 was not invoked, which is a Pre-Synthesis Integrity Check failure
(item 4) that must be repaired before delivery.

### Reflection History (Constraint Block 0)
All reflection entries written during this run, in chronological order,
verbatim as written. This includes:
- Kickoff reflection
- Mid-run reflection
- Post-Query-Expansion reflections (one per M13 pass)
- Pre-synthesis reflection
- Post-synthesis reflection (written *after* this Synthesis is drafted,
  appended below)

Reflections were written in writing during the run. If any are missing
here, the run is incomplete.

### Cross-Pollination Log (Phase 2b)
The two cross-pollinated steps from Phase 2b — what they returned and
whether they modified the final answer. Format per import:
- Source category (A / B / C)
- Step ID and title
- What it surfaced
- Did it change the conclusion? (yes / no / partially — explain)

### Open Questions / Unresolved
What this research could *not* settle. Be explicit. "We do not know"
is a legitimate finding when documented honestly.

### Sources
Structured source list:
- **Primary sources** first (peer-reviewed, official, primary documents)
- **Secondary sources** next (analyses, reports with editorial accountability)
- **Aggregators** last (only if used as discovery aids, not as evidence)

For each source: title, author/org, date, URL/citation, type tag.

### Methodology Note
Brief audit:
- Which critical-thinking methods were applied (refer by short anchor)
- Which methods were active for which findings
- Any "unanchored" / "single-source" / "unable to steelman" flags
- Total search iterations
- Any Pre-Synthesis Integrity Check items that flagged

This methodology note is the auditability handle — it is what allows
a reader to assess the trustworthiness of the synthesis without
re-running the research themselves.

## SELF-VERIFICATION CHECKLIST (11 items)

Before you deliver the Synthesis, verify each of these in writing.
A "done" by memory does not count — write one line per item
confirming you completed it.

- [ ] **1. Restatement integrity.** Every major step began with a
      verbatim Restatement Checkpoint that included CONSTRAINT BLOCK 0
      first, followed by all other active CBs and all active methods
      (with M13 always present).

- [ ] **2. Reflection regime (CONSTRAINT BLOCK 0).** All five mandatory
      reflection checkpoints were honored in writing: Kickoff, Mid-run,
      Post-Query-Expansion, Pre-synthesis, Post-synthesis. Confirm:
      *"I wrote [N] reflection entries at the following checkpoints:
      [enumerate]."* If N is below 5, write the missing reflections
      now before continuing.

- [ ] **3. Method invocation audit.** Every method listed in the active
      methods palette has at least one concrete invocation visible in
      the Reason history. Methods with zero invocations are flagged
      in the Methodology Note as "active but not invoked — likely
      inappropriate for this run".

- [ ] **4. Adversarial Query Expansion (M13).** M13 was invoked along
      all four axes (adjacent / opposing / abstraction / orthogonal)
      at least once each. The Query Expansion Log is populated with
      ≥ 4 entries. Confirm: *"M13 was invoked [N] times; the orthogonal
      axis (`LLM-Indexer-Optik vs. menschliche Leser-Optik vs. Q&A-Performance`) was used [M] times."* If N=0 or M=0,
      run a final pass before proceeding.

- [ ] **5. Cross-pollination audit.** Both cross-pollinated steps
      (Phase 2b — one from each non-primary category) were executed
      and logged. Confirm: *"Cross-pollination steps adapted from
      Categories X and Y were executed as follows: [enumerate]."* If
      none were executed, the generated prompt did not honor Phase 2b —
      halt and report.

- [ ] **6. Source triangulation (where M06 active).** Every factual
      claim has been through Source Triangulation with ≥ 3 independent
      sources, or is explicitly flagged as **single-source**. Aggregator-
      chains do not count as multiple sources.

- [ ] **7. Contradiction Log populated.** The Contradiction Log section
      of the Synthesis has been written. If no contradictions were
      encountered, the section explicitly states *"No contradictions
      encountered during this research"* — written only after a
      verification pass, never as a default placeholder.

- [ ] **8. Temporal scope honored.** All findings are within the
      temporal scope defined in CONSTRAINT BLOCK 2. Anything outside
      has been removed.

- [ ] **9. Output exclusions honored.** None of the findings or
      recommendations fall into the exclusion list in CONSTRAINT
      BLOCK 3. Verify by reading each finding against the exclusion
      list.

- [ ] **10. Pre-Synthesis Integrity Check (M4) executed in writing.**
      All 8 items of the M4 check were completed before the Synthesis
      was drafted. The check is in the working notes; it is not
      retrofitted after the fact.

- [ ] **11. Synthesis sections complete.** The Synthesis contains:
      Executive Summary · Key Findings · category-specific main body ·
      Contradictions · Query Expansion Log · Reflection History ·
      Cross-Pollination Log · Open Questions · Sources · Methodology
      Note. Any missing section is a blocker; write it before delivery.

If any checkbox fails, repair before delivery. Do not deliver a
Synthesis with failing items. The user will read this checklist
state in the Methodology Note — partial completion is visible.

---

*End of research prompt — generated by research-prompt-optimizer v3.2.0 at 2026-05-07T08:16:21+00:00.*
