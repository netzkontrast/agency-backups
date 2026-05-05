---
type: prompt
status: active
slug: agency-adr-governance-spec
summary: "Research-proposal prompt rendered by research-prompt-optimizer v3.2.0. Drives a Category-B extraction that produces an ADR-governance spec (lifecycle + token-efficient rule synthesis + tooling acceptance criteria) for the netzkontrast/agency repo. Verbatim-preserved; the renderer's two metadata blocks are kept inside a fenced ```yaml block below for traceability."
created: 2026-05-05
updated: 2026-05-05
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: any
prompt_relates_to_task: spec-subagent-subtask-prompt-format
---

# Research Prompt: ADR-governance spec for github.com/netzkontrast/agency

> **Verbatim preservation note.** The renderer (`research-prompt-optimizer v3.2.0`) emitted two YAML blocks ahead of its body. They are preserved verbatim inside a fenced `yaml` block immediately below so this file remains a single-frontmatter markdown document while the original render is fully recoverable. Do not edit the fenced block in place — re-render upstream and replace.

```yaml
---
schema_version: "3.1"
schema: research-prompt-render
provenance:
  created: "2026-05-05T09:09:18+00:00"
  skill_version: "3.3.1"
  phase: "phase3"
  slug: "agency-adr-governance-spec"
  output_filename: "research-prompt_agency-adr-governance-spec.md"
  category_signal: "B"
  selected_methods: ["M13", "M06", "M07", "M08", "M12"]
  selected_framework_structural: "risen"
  cross_pollination_pair: ["a-into-b", "c-into-b"]
  intent_ref: "intent_agency-adr-governance-spec.yaml"
  meta_prompt_ref: "meta-prompt_agency-adr-governance-spec.yaml"
language: "en"
target_agent: model-agnostic
---

---
topic: "ADR-governance spec for github.com/netzkontrast/agency (lifecycle + token-efficient rule synthesis + tooling acceptance criteria)"
slug: "agency-adr-governance-spec"
research_category: "B"
research_category_label: "Extraction"
critical_thinking_methods:
  - "M06 Source Triangulation"
  - "M07 Contradiction Log"
  - "M08 What Would Change My Mind"
  - "M12 Base-Rate Anchoring"
  - "M13 Adversarial Query Expansion"
prompt_engineering_framework_agentic_spine: "ReAct"
prompt_engineering_framework_structural: "RISEN"
cross_pollination:
  - source_category: "A"
    module: "a-into-b"
    title: "Exploration Sanity Pass (Hidden-items + Schema-gap)"
  - source_category: "C"
    module: "c-into-b"
    title: "World-Change Check (pre + mid-batch)"
constraint_blocks:
  - "0 — Reflection Baseline (Always Active)"
  - "1 — Source Priority Rules — Repo-First, Then Canon"
  - "2 — Temporal Scope"
  - "3 — Output Exclusions and Schema Conformance"
  - "4 — Privacy / Confidentiality"
language: "en"
target_agent: "model-agnostic"
created: "2026-05-05T09:09:14+00:00"
version: "1.0"
source_skill: "research-prompt-optimizer v3.2.0"
---
```

# Research Prompt: ADR-governance spec for github.com/netzkontrast/agency (lifecycle + token-efficient rule synthesis + tooling acceptance criteria)

> **For the executing AI:** This prompt is self-contained. Every
> method, framework, and constraint you need is defined inline below.
> You do not need external context, prior training on specific
> methodologies, or knowledge of the skill that generated this
> prompt. **Read the entire prompt before beginning.** Specifically,
> read the three layers in the Meta-Header below and verify you
> understand how they compose.



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
| [M06] | Source Triangulation            | —                                     |
| [M07] | Contradiction Log               | —                                     |
| [M08] | What Would Change My Mind       | —                                     |
| [M12] | Base-Rate Anchoring             | —                                     |
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

## CONSTRAINT BLOCK 0 — Reflection Baseline (Always Active)

Reflection is not a polish step. It is a **baseline operational
requirement** that runs in parallel to every other activity in this
research. You — the executing agent — perform targeted reflection at
every defined checkpoint, in writing, using the template below. A
checkpoint reached without a reflection entry is an incomplete
checkpoint; do not advance past it.

### Reflection Checkpoints (Minimum)

1. **Kickoff reflection** — immediately after restating the research
   objective and Constraint Blocks, before the first Reason phase.
2. **Mid-run reflection** — after the first batch of searches, once
   you have a tentative direction but before you commit to it.
3. **Post-Query-Expansion reflection** — after each Adversarial Query
   Expansion pass (Method M13).
4. **Pre-synthesis reflection** — immediately before the Pre-Synthesis
   Integrity Check (M4).
5. **Post-synthesis reflection** — after the draft synthesis, before
   delivery.

Additional checkpoints apply if the research category has its own
(e.g., per-session reflections in lifecycle research).

### Reflection Template — Use Verbatim Structure

Each reflection entry answers these five questions, in order, in
writing:

> **Q1. What do I actually believe right now, and how confident?**
> (One sentence. Use an explicit confidence band: low / medium / high.)
>
> **Q2. What is the strongest piece of evidence against my current
> belief?** (Name the specific source or the specific observation. If
> you cannot name one, that itself is the answer — and it is a warning.)
>
> **Q3. Where am I most likely wrong, and why?** (Not generic — name
> the specific claim, assumption, or inference that is weakest.)
>
> **Q4. What would I do differently if I restarted the research from
> scratch knowing what I know now?** (Forces de-anchoring from the
> path already taken.)
>
> **Q5. What is the single highest-value next action?** (Must be a
> concrete, executable next step — a specific search, a specific
> verification, a specific hypothesis branch to open or close.)

### Rules

- Reflections are **written**, not internal. They become part of the
  research notes and of the final output's Reflection History
  section in the Synthesis.
- Reflections may not be skipped "because the answer is obvious". If
  the answer feels obvious, write the obvious answer in one line and
  advance — but do not omit the entry.
- **Reflections on reflections are allowed but not required.** If a
  reflection surfaces a contradiction with an earlier reflection, log
  both in the Contradiction Log (Method M07) with a note that the
  disagreement is internal rather than inter-source.
- If a reflection produces an action item (Q5) that contradicts the
  current Step's plan, the action item **takes precedence**. Update
  the plan, note the change, and continue.

### Anti-Rationalization Guard

If you find yourself writing "N/A" or "nothing to reflect on" in a
reflection entry — stop and re-read the entry's five questions. At
least Q2 and Q3 always have a real answer. "N/A" is a signal that the
reflection is being skipped performatively; write the real answer
instead.

### CONSTRAINT BLOCK 1 — Source Priority Rules — Repo-First, Then Canon

AUTHORITATIVE-FIRST ORDERING — must be followed in this exact order:

1. **Repository root files of `https://github.com/netzkontrast/agency`** MUST be read FIRST, before any external search. Read at minimum: `README.md`, `AGENTS.md` (if present), `CLAUDE.md` (if present), `SKILL.md` (if present at root), the top-level directory listing, and any `docs/` subtree referenced from README. The produced spec's §0 (Status & Provenance) AND §2 (System-Level Conventions) MUST visibly cite content found in these repo files. If the repo is unreachable, the spec MUST declare this in §0 and §8 instead of fabricating context.

2. **Primary ADR canon:** Michael Nygard's 2011 post 'Documenting Architecture Decisions'; the MADR project (`adr.github.io`, `adr/madr` GitHub repo); Olaf Zimmermann's Y-Statements; ThoughtWorks Tech Radar entries on ADRs.

3. **Tooling repos (≥3 mandatory in §9 Source Index):** examples include `npryce/adr-tools`, `thomvaill/log4brains`, `adr/madr`, `joelparkerhenderson/architecture-decision-record`. If these are stale at search time, the agent MUST find current equivalents and document the lineage in §8.

4. **Research papers (≥2 mandatory where literature exists):** Zimmermann et al. on architectural decision capture; ICSE / ECSA / ICSA conference proceedings on architectural knowledge management; any peer-reviewed work on AI-agent-readable specifications. If literature is genuinely thin (esp. for the orthogonal lens), the agent MUST declare 'literature-thin' in §8 with a one-sentence explanation rather than fabricate sources.

5. **Aggregator / community sources** (Wikipedia, blog posts, podcasts) are admissible for discovery and triangulation only. They MUST NOT be the sole source for any normative MUST/SHOULD statement.

6. **URL reachability:** every URL in §9 MUST resolve at the time of writing. Paywalled-only sources MUST NOT be the sole source for any normative statement. Inline citations in §3–§7 MUST point to a §9 entry.

### CONSTRAINT BLOCK 2 — Temporal Scope

Research spans 2011-01-01 through 2026-05-05.

ADR fundamentals (concept, structure, lifecycle) are unbounded back to Nygard's 2011 post — these are stable and pre-2011 sources are not expected to exist for this topic.

Tooling, AI-agent rule-file patterns, token-efficient synthesis, and governance-as-code approaches: 2022-present (post-LLM-coding-agent era). Pre-2022 sources on these specific sub-topics MUST be treated as background context only, never as authoritative for normative statements about current practice.

Sources outside this window MUST NOT be cited unless they establish a baseline that is explicitly referenced from within the window.

### CONSTRAINT BLOCK 3 — Output Exclusions and Schema Conformance

The produced spec MUST NOT contain:
- Generic ADR template recommendations divorced from the agency repo's actual structure.
- General prompting best practices for AI agents — covered elsewhere in the user's skill ecosystem.
- Concrete ADR records — the spec governs HOW ADRs are made, not their content.
- Reference implementation source code — interface contracts (JSON-Schema sketches, CLI shape) yes, working code no.

SCHEMA CONFORMANCE (mandatory):
The produced spec MUST follow the §0–§9 structure demonstrated in the pasted 3-systems example:
  §0 Status & Provenance (with World-Change Annotation)
  §1 Normative Conventions:
    §1.1 RFC-2119 / BCP-14 Normative Keywords — REPRODUCE THE BINDING PARAGRAPH VERBATIM
    §1.2 Gherkin Syntax Binding
    §1.3 Style Guide for Normative Statements
  §2 System-Level Conventions
  §3 Aspect 1 — Explore
  §4 Aspect 2 — Plan
  §5 Aspect 3 — Implement
  §6 Aspect 4 — Review
  §7 Aspect 5 — Validate
  §8 Known Limitations & Open Questions
  §9 Source Index

Each §3–§7 aspect contains: (a) §X.1 Normative Statements (each one BCP-14 keyword per sentence, each with stable ID `<SpecLetter>.<AspectN>.<StmtN>`), (b) §X.2 Acceptance Criteria as Gherkin scenarios with `# anchor: <stable-id>` comments, (c) §X.3 Rationale (no all-caps BCP-14 keywords). Tooling acceptance criteria depth is BEHAVIOUR + INTERFACE: Gherkin scenarios + JSON-Schema sketches + CLI command shape. NO reference implementation source code.

### CONSTRAINT BLOCK 4 — Privacy / Confidentiality

Public OSS context. The agency repository is public. No confidential data. Standard reachable-URL discipline applies (see CB1).

## Critical-Thinking Methods (Always Active)

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

### Method: Base-Rate Anchoring

**What it is:** For every frequency, probability, or prevalence claim, you
anchor it against the **base rate** of the relevant reference population.
Specific cases are interpreted against general rates, not in isolation.

**Why it is in this prompt:** Representativeness bias causes research to
weight vivid specific examples over statistically-grounded base rates.
Anchoring reverses this by making the base rate primary.

**How to apply it — step by step:**
1. For every probability / frequency / "how common" claim, identify the
   **reference population** the claim is made against.
2. Find the base rate in that reference population.
3. State the specific claim **explicitly relative to** the base rate:
   "2x the base rate", "well below the base rate", "within the base-rate
   range".
4. If no base rate can be found, flag the claim as **unanchored**.

**When to stop / escape criterion:** Apply to every numerical frequency or
probability claim. Skip for purely qualitative observations.

**Example trigger in this research context:** "Company X had
[PLACEHOLDER] failures" is meaningless without the base rate: what is
the failure rate in comparable companies of similar size, industry,
and time period?

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
   is `['architecture decision records', 'ADR', 'governance', 'lifecycle', 'supersession', 'amendment', 'token-efficient synthesis', 'rules file', 'AI coding agent', 'netzkontrast/agency', 'skill ecosystem repo']` (extracted at composition time from the
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
     pre-specified by the user as: `Information-theoretic / compression — frame the ADR-corpus → rules-file synthesis as a minimum-description-length compression with semantic-fidelity bounds. Produces measurable acceptance criteria (compression ratio, fidelity floor) for the synthesis tooling.`.** Execute
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
`['architecture decision records', 'ADR', 'governance', 'lifecycle', 'supersession', 'amendment', 'token-efficient synthesis', 'rules file', 'AI coding agent', 'netzkontrast/agency', 'skill ecosystem repo']`. Your pre-specified orthogonal lens is
`Information-theoretic / compression — frame the ADR-corpus → rules-file synthesis as a minimum-description-length compression with semantic-fidelity bounds. Produces measurable acceptance criteria (compression ratio, fidelity floor) for the synthesis tooling.`. After the first search batch, you generate one
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

- **CONSTRAINT BLOCK 0 — Reflection Baseline (Always Active):** [Paste the full text of the block here. Do not paraphrase.]
- **CONSTRAINT BLOCK 1 — Source Priority Rules — Repo-First, Then Canon:** [Paste the full text of the block here. Do not paraphrase.]
- **CONSTRAINT BLOCK 2 — Temporal Scope:** [Paste the full text of the block here. Do not paraphrase.]
- **CONSTRAINT BLOCK 3 — Output Exclusions and Schema Conformance:** [Paste the full text of the block here. Do not paraphrase.]
- **CONSTRAINT BLOCK 4 — Privacy / Confidentiality:** [Paste the full text of the block here. Do not paraphrase.]

I also restate the currently-active critical-thinking methods:

- **Method: Adversarial Query Expansion** — [Paste the "How to apply" bullet list verbatim.]
- **Method: Source Triangulation** — [Paste the "How to apply" bullet list verbatim.]
- **Method: Contradiction Log** — [Paste the "How to apply" bullet list verbatim.]
- **Method: What Would Change My Mind** — [Paste the "How to apply" bullet list verbatim.]
- **Method: Base-Rate Anchoring** — [Paste the "How to apply" bullet list verbatim.]

I confirm these are active for the step below.

### {{step_or_iteration_label}} — {{step_title}}

{{step_content}}

### Batch Procedures

## BATCH PROCEDURE — per-aspect

You will execute the following procedure **exactly 5 times**,
once per item in this list:

[Aspect 1 — Explore, Aspect 2 — Plan, Aspect 3 — Implement, Aspect 4 — Review, Aspect 5 — Validate]

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

1. Draft ≤6 normative statements (one BCP-14 keyword per sentence)
2. Author ≥1 Gherkin scenario per statement (with `# anchor:` comment)
3. Write Rationale paragraph in lowercase prose
4. Append sources to §9 following CB1 priority
5. M06 triangulate every MUST/MUST NOT statement against ≥3 independent sources
6. M07 log any inter-source contradictions

**Iteration [i] Output Schema (fill all fields):**

{ aspect_id, aspect_name, normative_statements:[{id, keyword, statement, anchor}], gherkin_scenarios:[{anchor, feature, scenario_text}], rationale, sources_added:[{ref_number, citation, url, source_tier}] }
- Confidence: {{confidence_label}}

You may not proceed to Iteration [i+1] until Iteration [i]'s output
schema is fully populated.

### Cross-Pollination Steps

### Step [i.a] — Exploration Sanity Pass (cross-pollination from Category A)

This step imports one sanity pass from Category A (Exploration) because
even a well-scoped extraction can miss items that belong in the list
but were never named, or can lock on a schema that hides the real
variation.

Perform the following before finalizing any batch result:

1. **Hidden-items query.** Run one orthogonal search designed to find
   items that would belong in the list but were not in the original
   input. Phrase it as: *"[item type] that [trait that would make it
   qualify] but is rarely included in typical lists of [item type]"*.
   If the query returns a credible candidate, raise it as an
   **Out-of-Scope Candidate** in the Contradiction Log with the note:
   *"Item [NAME] appears to satisfy the inclusion criteria but is not
   in the input list."*

2. **Schema-gap hypothesis.** Write down one hypothesis of the form:
   *"The output schema as given may be missing the field [FIELD] because
   [REASON]."* Test it with one targeted search across the item set.
   If the hypothesis survives, raise it as an **Out-of-Scope Candidate
   Field** in the Contradiction Log.

3. **Do not hybridize.** These two checks are explicitly scoped. They
   produce candidates for the user to decide on, not silent changes to
   the input list or the schema. The extraction proceeds against the
   locked input + locked schema as before.

### Step [i.c] — World-Change Check (cross-pollination from Category C)

This step imports one lifecycle discipline from Category C because
a Category-B extraction implicitly treats every fact within the
temporal scope as static. For fast-moving domains (regulation, market
data, leadership, technology versions), facts harvested at the start
of a long batch may already be wrong by the end of the batch.

Perform the following at two points in the run:

1. **Pre-batch world-change scan.** Before starting the batch, run
   one targeted search for **state changes that occurred within the
   last [time-since-temporal-window-end] for each major item type
   in the input list**. Format: *"changes in [item type] [back-edge
   of temporal window]–today"*. The point is not to extend the
   temporal window, but to **flag items whose extracted values may
   already be stale** by the time the synthesis is delivered.

2. **Mid-batch world-change check.** At the halfway point of the
   batch (or every [N] iterations, whichever fires first), repeat the
   scan with focus on items already extracted. Any item whose state
   has measurably moved since its extraction goes into a
   **World-Change Annotation** column in the output schema, alongside
   the original extracted value.

3. **Annotate, do not retroactively edit.** A core B-discipline
   (Method M06 Source Triangulation) requires the extracted value at
   the moment of extraction to be preserved. World-Change Annotations
   are an additional layer; the original triangulated value remains
   the primary record, with the annotation flagging downstream caution.

4. **Do not hybridize.** This step does not turn the extraction into
   ongoing monitoring. It is a one- or two-pass check that surfaces
   staleness risk before the synthesis is delivered. If the user
   wants ongoing monitoring, route the next prompt as Category C.

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
      axis (`Information-theoretic / compression — frame the ADR-corpus → rules-file synthesis as a minimum-description-length compression with semantic-fidelity bounds. Produces measurable acceptance criteria (compression ratio, fidelity floor) for the synthesis tooling.`) was used [M] times."* If N=0 or M=0,
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

*End of research prompt — generated by research-prompt-optimizer v3.2.0 at 2026-05-05T09:09:14+00:00.*
