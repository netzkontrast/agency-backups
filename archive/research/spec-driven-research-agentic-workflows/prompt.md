---
topic: "Spec-Driven Best Practices for Designing and Governing Agentic Research Workflows"
slug: "spec-driven-research-agentic-workflows"
research_category: "B+C"
research_category_label: "Extraction + Lifecycle"
critical_thinking_methods:
  - "Source Triangulation"        # M06 — Cat-B default
  - "Contradiction Log"           # M07 — Cat-B default
  - "What Would Change My Mind"   # M08 — Cat-B default, Pre-Commitment pass
  - "Pre-Mortem"                  # M03 — Cat-C default, lifecycle failure-mode scan
  - "Steelmanning"                # M09 — Cat-C default, adversarial stress-test of normative claims
  - "Adversarial Query Expansion" # M13 — always present
prompt_engineering_framework_agentic_spine: "ReAct"
prompt_engineering_framework_structural: "RISE-DX"
bespoke_framework_provenance: |
  RISE-DX adapted from RISEN + TIDD-EC:
  R (Role), I (Input), S (Steps), E (Expectations), D (Do/Don't), X (eXamples).
  Chosen because the output requires both an explicit Do/Don't grammar layer
  (RFC-2119 keyword discipline enforced by CB4) and a worked-example layer
  (the existing Spec-A/B/C document serves as the canonical positive example).
cross_pollination:
  - source_category: "A"
    step_id: "S6.a"
    description: "Exploration Sanity Pass — Hidden-Aspects + Schema-Gap Hypothesis"
  - source_category: "C"
    step_id: "S7.c"
    description: "World-Change Scan (pre-batch + mid-batch) — detect drift in agent platform versions"
constraint_blocks:
  - "0 — Reflection Baseline"
  - "1 — Source Priority Rules"
  - "2 — Temporal Scope"
  - "3 — Output Exclusions"
  - "4 — Spec-Driven Output Grammar (RFC 2119 + Gherkin)"
  - "5 — Repository Linkage Protocol (Jules vs. Non-Jules bifurcation)"
prior_art_ref: "research/agent-prompt-specs-3-systems-sdd/output/SPEC.md"
language: "en"
target_agent: "model-agnostic"
created: "2026-05-02"
version: "1.0"
source_skill: "research-prompt-optimizer v3.0 + spec-skill v1.0"
---

# Research Prompt: Spec-Driven Best Practices for Designing and Governing Agentic Research Workflows

> **For the executing AI — read this block before doing anything else.**
>
> This prompt is **entirely self-contained**. Every framework, method, constraint, and
> example you need is defined inline below. You do not need external context, prior
> training on specific methodologies, or knowledge of any skill that generated this
> prompt. Read the full prompt before beginning any research or writing.
>
> Your output is **three Specs** — Spec-D, Spec-E, Spec-F — each defining normative
> best practices across the five standard aspects (Explore / Plan / Implement / Review /
> Validate), written in the Spec-Driven Development grammar defined in CONSTRAINT BLOCK 4.
>
> Before doing anything else, execute the **PRIOR ART BLOCK** immediately below.

---

## ⚡ PRIOR ART BLOCK — Execute Before Any Research

This task extends an existing research artefact. Your behaviour depends on which
agent platform you are running on.

### Branch A — If you are Google Jules (repo-resident agent)

You have filesystem access to the repository that contains this prompt.

**You MUST execute the following steps before proceeding to the research body:**

1. Read the file at `./research/agent-prompt-specs-3-systems-sdd/output/SPEC.md`.
   This document contains Spec-A (Google Jules), Spec-B (Claude Code), and
   Spec-C (Gemini Deep Research) — three normative specifications that your new
   output (Spec-D, Spec-E, Spec-F) will extend and cross-reference.
2. Read `./AGENTS.md`, `./RESEARCH.md`, `./FOLDERS.md`, and `./PRE_COMMIT.md`
   to understand the repository's governance protocols. Your output MUST be
   compatible with the folder structure defined in `RESEARCH.md`.
3. Initialize your working directory at:
   `./research/spec-driven-research-agentic-workflows/`
   following the exact subfolder structure in `RESEARCH.md §Directory Structure`.
4. Save this prompt verbatim to:
   `./research/spec-driven-research-agentic-workflows/prompt.md`
5. Then proceed to the **RESEARCH BODY** below.

**Cross-referencing convention for Jules:** When a new normative statement in
Spec-D/E/F directly supersedes, refines, or contradicts a statement in Spec-A/B/C,
annotate it inline: `[extends A.4.2]` or `[contradicts B.2.3 — see §8]`.

### Branch B — If you are an external research agent (Gemini Deep Research, Perplexity, Claude Research, GPT Deep Research, or any model without filesystem access)

You cannot read the existing repository directly.

**Your output MUST include a `## Repository Linking Manifest` section** (see OUTPUT
SPEC §5 below) that maps every output artefact you produce to its target path in the
repository. A human operator will use this manifest to integrate your findings.

**Prior art summary for non-Jules agents** (treat as authoritative ground truth):
The existing `SPEC.md` (Spec-A/B/C) established the following canonical positions,
which your new Specs MUST treat as confirmed priors:

| ID | Confirmed Prior |
|:---|:----------------|
| A.2.5 | Users MUST review and approve a Jules-generated plan before code execution |
| B.2.2 | A Claude Code repo MUST contain a `CLAUDE.md` instruction file |
| B.3.4 | Context rot occurs past ~300k tokens; wide reads SHOULD be delegated to subagents |
| B.4.4 | Planning phase and execution phase MUST NOT be merged into a single command |
| C.3.1 | Gemini Deep Research prompts MUST instruct the agent to use live Google Search grounding |
| C.4.2 | The planning prompt MUST define the expected structure of the final report |
| All  | Every spec MUST include §1 BCP-14 normative conventions paragraph verbatim |
| All  | Every Gherkin Scenario MUST carry a `# anchor: <ID>` comment line |

Do not re-research these priors. Build on them.

---

## R — Role

You are an **Autonomous Research Architect and Spec Author** with expertise in:

- Normative specification writing for long-horizon agentic systems (RFC-2119 / BCP-14)
- Agentic workflow orchestration patterns: ReAct, Plan-Execute, DAG pipelines, and
  dual-cognition orchestration (JANUS-style Planner-Executor separation)
- Repository-resident governance protocols: AGENTS.md, CLAUDE.md, RESEARCH.md patterns
- Spec-Driven Development (SDD) applied to AI research pipelines
- Long-context engineering: wiki-ingest, world-model synchronization, session handoff

You produce outputs that can be audited against their sources, contradict themselves
only explicitly (with resolution proposals), and can be operationalized by a downstream
agent without further clarification.

---

## I — Input

**Research Question (primary):**
What are the normative, specification-driven best practices for *designing*, *governing*,
and *executing* agentic research and coding workflows at the meta-level — covering the
mechanics of spec authorship, orchestration pattern selection, repository governance,
and world-model synchronization — such that any conformant agent can operate autonomously
across the full Explore → Plan → Implement → Review → Validate cycle without workflow drift?

**Research Question (unpacked — what this is NOT):**
This is not a survey of which agent tools exist (that is Spec-A/B/C). This is a
specification of *how* to design the spec-driven governance layer that sits above those
tools — the meta-level that answers: how do you write specs for agents that write specs?
How do you govern a repository that an agent will modify? How do you structure a research
workflow so that an agent can pick up a half-finished task without hallucinating the
missing context?

**Target systems covered (one Spec per system):**
- **Spec-D**: The Spec-Driven Research Workflow itself — how to author, version, and
  evolve normative specifications for agentic systems
- **Spec-E**: Agentic Orchestration Patterns — ReAct, Plan-Execute DAG, JANUS dual-cognition,
  and multi-agent handoff protocols
- **Spec-F**: Repository-Resident Agent Governance — the AGENTS.md / RESEARCH.md /
  FOLDERS.md / PRE_COMMIT.md pattern, decentralized documentation, and agent frustration
  feedback loops

**Audience:** Software architects and AI systems developers who are actively building
long-horizon agentic pipelines, familiar with RFC-2119 grammar and Gherkin syntax.

**Depth:** Exhaustive — every normative statement must survive at least one Pre-Commitment
counter-pass and one Steelmanning pass before being emitted as MUST.

**Success criterion:** The three Specs are self-contained, machine-readable, and
operationally complete — meaning a new agent reading only this document and the three
output Specs could begin executing a research task in the target repository without
asking for clarification.

---

## CONSTRAINT BLOCK 0 — Reflection Baseline

You MUST produce a **Reflection Entry** (minimum 5 questions answered) at each of the
following checkpoints. Log these entries under `## Reflection History` in the final
output. Do not skip any checkpoint, even if it feels redundant.

**Reflection template (5 questions, answer each in 2–4 sentences):**
1. What do I actually believe right now, and how confident am I?
2. What is the strongest piece of evidence against my current belief?
3. Where am I most likely wrong, and why?
4. What would I do differently if I restarted from scratch knowing what I know now?
5. What is the single highest-value next action?

**Required checkpoints:**
- Kickoff (before first search)
- After each Spec (post-D, post-E, post-F)
- Pre-Synthesis (before assembling the final document)
- Post-Synthesis (after assembly, before the pre-commit check)

---

## CONSTRAINT BLOCK 1 — Source Priority Rules

When researching, apply the following source hierarchy. Document your source tier
for every normative statement that cites evidence.

| Tier | Source Type | Trust Level |
|:-----|:------------|:------------|
| T1 | Vendor primary documentation (RFC text, official agent docs) | Highest |
| T2 | Peer-reviewed papers, official engineering blogs | High |
| T3 | Community reproductions, power-user write-ups, GitHub repos | Medium |
| T4 | Aggregators, secondary summaries, AI-generated overviews | Low — cite sparingly, annotate |

- A statement sourced only from T4 MUST be flagged `[Confidence: low (single-source)]`.
- A statement sourced from T1+T2 convergence MAY be emitted as MUST without caveat.
- If T1 and T3 contradict each other, log it in the **Contradiction Log** (see §Logs).

---

## CONSTRAINT BLOCK 2 — Temporal Scope

- **Primary window:** January 1, 2025 – May 2, 2026 (today)
- **Soft background window:** July 1, 2024 – December 31, 2024 (use for context only;
  do not cite as primary evidence)
- **Do NOT cite:** anything prior to July 2024 as current practice
- **Do NOT speculate** about capabilities not yet released or announced

Apply a **World-Change Scan** (Step S7.c) at two points: before beginning Spec-E
(orchestration patterns — rapidly evolving) and before beginning Spec-F (repository
governance — slower but shifting with new agent releases). Log results in `## World-Change Log`.

---

## CONSTRAINT BLOCK 3 — Output Exclusions

The following MUST NOT appear in any normative statement or Gherkin scenario:

- Pricing, quota limits, or rate-limit numbers (these change without notice)
- Model version strings as acceptance criteria (e.g., "MUST use Gemini 2.5 Pro")
- Comparative rankings of agents by quality ("Agent X is better than Agent Y")
- Unannounced or rumoured features
- UI surface details in MUST statements (button names, menu paths — these belong in Rationale)

---

## CONSTRAINT BLOCK 4 — Spec-Driven Output Grammar (RFC 2119 + Gherkin)

Every normative statement in every Spec MUST conform to the following grammar.
This is non-negotiable.

### BCP-14 Normative Keywords

> The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
> **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and
> **OPTIONAL** in every produced Spec are to be interpreted as described in BCP 14
> [RFC 2119] [RFC 8174] **when, and only when, they appear in all capitals**, as
> shown here.

Each produced Spec **MUST** include this paragraph verbatim in its §1.

### Statement discipline

- **One RFC-2119 keyword per statement.** No "and" clauses hiding a second requirement.
- **Specify the actor** in every statement: "The agent MUST…", "The user SHOULD…",
  "The repository MUST…"
- **Testable.** If a statement cannot be checked against a Gherkin scenario, rewrite it.
- **No all-caps keywords in rationale prose.** Lowercase "should" or "may" in prose is fine.
- **MUST inflation guard.** If you find yourself writing 5+ MUSTs in a single aspect,
  pause and apply a Steelmanning pass. At least two statements per aspect SHOULD be
  SHOULD-level or lower.

### Gherkin conventions

```gherkin
# anchor: <Spec-Letter>.<Aspect-Number>.<Statement-Number>
Feature: <short feature name>

  Background:            # OPTIONAL — only when ≥ 3 scenarios share setup
    Given ...

  Scenario: <imperative description>
    Given <pre-condition>
    When <action>
    Then <observable outcome>
    And <additional outcome>   # optional continuation
```

- Every aspect block MUST contain at least one Gherkin scenario.
- Every scenario MUST carry a `# anchor:` comment on the line immediately above `Scenario:`.
- `Background` sections are OPTIONAL but RECOMMENDED when ≥ 3 scenarios share setup steps.

### Stable identifiers

Each normative statement MUST be addressable by:
`<Spec-Letter>.<Aspect-Number>.<Statement-Number>`

- Spec-D: prefix `D`
- Spec-E: prefix `E`
- Spec-F: prefix `F`

---

## CONSTRAINT BLOCK 5 — Repository Linkage Protocol

### For Jules (repo-resident):
Your output artefacts MUST be written to the following paths, in this exact structure:

```
research/spec-driven-research-agentic-workflows/
├── readme.md
├── prompt.md                    ← this file, verbatim
├── workspace/
│   ├── readme.md
│   ├── session.log
│   └── integrity_check.md
├── synthesis/
│   ├── readme.md
│   ├── state.md
│   ├── methodology.md
│   ├── post-synthesis-log.md
│   └── tracks.md
├── reflection/
│   ├── readme.md
│   └── friction-log.md
└── output/
    ├── readme.md
    └── SPEC.md                  ← the three new Specs (D, E, F)
```

Every folder MUST contain a `readme.md` explaining its contents with relative Markdown links,
per `FOLDERS.md §Mandatory readme.md Rule`. The `friction-log.md` is MANDATORY even if FL0.
Run the full `PRE_COMMIT.md` checklist before invoking `git commit`.

### For non-Jules agents (output contains a Linking Manifest):
Your output `SPEC.md` MUST include a trailing section formatted exactly as follows.
A human operator will use it to place your output in the correct repository locations.

```markdown
## Repository Linking Manifest

| Artefact | Target Path in Repository | Action |
|:---------|:--------------------------|:-------|
| This SPEC.md | `research/spec-driven-research-agentic-workflows/output/SPEC.md` | CREATE |
| Spec-D normative statements | (inline in SPEC.md) | CONTAINED |
| Spec-E normative statements | (inline in SPEC.md) | CONTAINED |
| Spec-F normative statements | (inline in SPEC.md) | CONTAINED |
| friction-log.md | `research/spec-driven-research-agentic-workflows/reflection/friction-log.md` | CREATE |
| session.log | `research/spec-driven-research-agentic-workflows/workspace/session.log` | CREATE |
| state.md | `research/spec-driven-research-agentic-workflows/synthesis/state.md` | CREATE |
| Prior art cross-ref | `research/agent-prompt-specs-3-systems-sdd/output/SPEC.md` | READ-ONLY REFERENCE |
```

Fill in the `Action` column with CREATE / UPDATE / READ-ONLY REFERENCE as appropriate.
Add rows for any additional artefacts you produce. The operator will reconcile this
manifest against the repository structure before committing.

---

## S — Steps (ReAct Agentic Spine)

Execute in strict order. Each step is Thought → Action → Observation. Log actions
to `workspace/session.log` (Jules) or equivalent internal log (non-Jules).

---

### S0 — Kickoff Reflection

Write your Kickoff Reflection entry (5 questions per CB0 template).
Commit to your hypothesis for each target Spec before beginning research.

---

### S1 — Prior Art Ingestion

**Jules:** Read `./research/agent-prompt-specs-3-systems-sdd/output/SPEC.md` now.
Extract: (a) all cross-cutting conventions, (b) the three open questions from §8 of each
existing Spec, (c) the Contradiction Log, (d) the World-Change Log.

**Non-Jules:** Use the Prior Art Summary table in the PRIOR ART BLOCK above as your
ground truth. Do not re-research confirmed priors.

Log extracted prior-art findings under `## Prior Art Extraction` in your synthesis output.

---

### S2 — Seed Query Construction

For each target Spec, generate 3–5 seed queries. Queries MUST be specific, 3–8 words,
and distinct from each other. Avoid generic terms like "best practices" in isolation.

**Spec-D seed areas (Spec-Driven Research Workflow Governance):**
- RFC-2119 specification authoring for AI agents (T1 priority: RFC texts, ISO standards)
- Living specification patterns — versioning and evolution of normative documents
- Spec-Driven Development methodology — academic and practitioner literature (2025–2026)
- Gherkin BDD applied to agent acceptance criteria
- Pre-mortem and falsification discipline for normative spec authorship

**Spec-E seed areas (Agentic Orchestration Patterns):**
- ReAct agent loop: reasoning-acting interleave — original paper + 2025 implementations
- Plan-Execute DAG: task decomposition architectures (LangGraph, AutoGen, CrewAI)
- Dual-cognition architectures: System-1/System-2 LLM orchestration (JANUS-type)
- Multi-agent handoff protocols: context passing, state serialization, re-entry contracts
- Long-horizon context engineering: wiki-ingest, world-model synchronization

**Spec-F seed areas (Repository-Resident Agent Governance):**
- AGENTS.md convention — origin, adoption patterns across OSS projects (2025)
- Decentralized documentation protocol — readme.md adjacency requirements
- Pre-commit governance for agent commits — safety, integrity, rollback
- Agent frustration / friction feedback loops — meta-learning from agent self-reports
- Workflow drift prevention — how repositories detect and correct agentic assumption drift

---

### S3 — Research Execution (Source Triangulation, M06)

For each seed area, gather evidence from at least two independent sources.
Apply Tier classification (CB1) to every source.

**Triangulation requirement:** A normative statement MAY only be emitted as MUST when
at least two T1/T2 sources converge on the same behavioural requirement.

Log source titles, tiers, and the specific evidence extracted in `## Source Index`.

---

### S4 — Adversarial Query Expansion (M13 — Mandatory)

For each Spec, execute the following four query expansion axes. Log results under
`## Query Expansion Log`. Annotate whether each axis produced novel findings that
modified a tentative normative statement.

| Axis | Description |
|:-----|:------------|
| **Adjacent** | Neighbouring concepts that might surface hidden requirements |
| **Opposing** | Searches for failure cases, criticisms, known anti-patterns |
| **Abstraction** | Step up one level — what broader pattern does this instantiate? |
| **Orthogonal** | Completely lateral — what adjacent domain solved a similar problem? |

**Minimum:** 3 axes active per Spec. M13 MUST NOT be skipped. If an axis finds nothing
novel, log it explicitly as "no novel findings".

---

### S5 — Contradiction Log (M07)

As findings accumulate, actively maintain the Contradiction Log.

For every contradiction found:
1. State the two conflicting claims precisely
2. Name their sources and tiers
3. Hypothesize a cause (framing difference, temporal gap, audience mismatch)
4. State the evidence that would resolve it
5. Emit the normative statement at the *weaker* keyword level until resolved

Format:
```
### Contradiction [X]: <short title>
- Claim A: "…" (Source: …, Tier: T2)
- Claim B: "…" (Source: …, Tier: T3)
- Hypothesized cause: …
- Resolution evidence needed: …
- Interim statement level: SHOULD (weakened from MUST pending resolution)
```

---

### S6 — Spec Drafting (per Spec, repeat S6 three times)

For each Spec (D, E, F), fill the following schema. Each aspect block MUST contain:
- 4–6 normative statements (mixed MUST/SHOULD/MAY — see CB4 inflation guard)
- At least one Gherkin scenario with `# anchor:` comment
- A Rationale paragraph (no all-caps RFC-2119 keywords)

```
## Spec-<X>: <Subject System>

### §0. Status & Provenance
### §1. Normative Conventions         ← copy BCP-14 paragraph from CB4 verbatim
### §2. System-Level Conventions      (<X>.2.1 … <X>.2.N)
### §3. Aspect 1 — Explore
### §4. Aspect 2 — Plan / Develop Spec
### §5. Aspect 3 — Implement / Execute
### §6. Aspect 4 — Review
### §7. Aspect 5 — Validate / Verify
### §8. Known Limitations & Open Questions
### §9. Source Index
```

**S6.a — Exploration Sanity Pass (Cross-pollination from Category A):**
Before finalizing each Spec, run one pass asking: "What aspect of this system is
*not* captured by the five-aspect schema? Is there a hidden sixth dimension that the
schema forces underground?" Log candidates under `## Hidden Aspects`. If a candidate is
strong enough, surface it as a §10 section (Optional Extended Aspect).

**Reflection checkpoint after each Spec.**

---

### S7 — Pre-Synthesis Integrity Check (M4)

Before assembling the final document, run the following 6-item checklist.
Any ✗ blocks assembly and forces a self-correct loop.

```
☐ ReAct spine is present and every step has Thought → Action → Observation
☐ M0 reflection entries exist at every required checkpoint
☐ M13 (Adversarial Query Expansion) was applied to all three Specs
☐ CB1 Source Priority is documented for every MUST-level statement
☐ Cross-pollination steps S6.a and S7.c have been executed and logged
☐ No <UNFILLED> markers or placeholder text remains in normative statements
```

**S7.c — World-Change Scan (Cross-pollination from Category C):**
Before beginning Spec-E (orchestration patterns), check: have any major agentic
framework releases (LangGraph, AutoGen, CrewAI, OpenAI Assistants API) occurred in the
last 90 days that affect your tentative normative statements? Log results under
`## World-Change Log`. If yes, re-run the affected seed areas in S3.

---

### S8 — Final Assembly and Linking Manifest

Assemble `SPEC.md` in the following document order:

1. **Executive Summary** (≤300 words — what the three Specs collectively establish)
2. **Common Conventions Across Specs** (cross-cutting rules that apply to D, E, and F)
3. **Spec-D** (full schema)
4. **Spec-E** (full schema)
5. **Spec-F** (full schema)
6. **Cross-Spec Dependency Map** — a table showing which Spec-D/E/F statements build on or supersede Spec-A/B/C statements
7. **Contradiction Log** (all logged contradictions)
8. **World-Change Log**
9. **Query Expansion Log**
10. **Reflection History** (all reflection entries in chronological order)
11. **Source Index** (all sources, tiered, linked)
12. **Repository Linking Manifest** (non-Jules agents: MANDATORY; Jules: optional confirmation)

---

## E — Expectations

### What success looks like

A successful run produces a `SPEC.md` that:

1. Contains exactly three Specs (D, E, F), each with §§0–9 filled (and optional §10)
2. Every normative statement is addressable by stable ID (`D.4.3`, `E.2.1`, `F.7.2`)
3. Every Gherkin scenario has a `# anchor:` comment and conforms to the `Given/When/Then` contract
4. No rationale paragraph contains an all-caps RFC-2119 keyword
5. The M13 Adversarial Query Expansion Log has ≥ 9 entries (3 Specs × 3 axes minimum)
6. The Contradiction Log has at least 2 entries (these systems genuinely contradict each other)
7. The Reflection History has ≥ 5 entries (Kickoff + 3 post-Spec + Pre-Synthesis)
8. The `friction-log.md` declares an explicit Frustration Level (FL0–FL3)
9. If non-Jules: the Repository Linking Manifest is present and complete
10. If Jules: the output folder structure exactly matches `RESEARCH.md §Directory Structure`

### What failure looks like

- Normative statements in Rationale blocks (all-caps keywords in prose)
- MUST-level statements with no supporting T1/T2 source
- Gherkin scenarios missing `# anchor:` comment
- Reflection entries that are ≤ 2 sentences per question
- The Prior Art Block ignored — emitting statements that contradict confirmed Spec-A/B/C priors without explicit `[contradicts X.Y.Z]` annotation
- Friction log absent or empty

---

## D — Do / Don't

| DO | DON'T |
|:---|:------|
| Emit MUST only when T1/T2 sources converge | Emit MUST on a single T3/T4 source |
| Annotate single-source claims with `[Confidence: low]` | Silently emit low-confidence claims as MUST |
| Annotate cross-references to Spec-A/B/C | Re-research confirmed priors from scratch |
| Use SHOULD and MAY for genuinely optional/recommended behaviours | Default everything to MUST (MUST inflation) |
| Put vendor UI surface details in Rationale | Put UI details in normative statements |
| Run S7.c World-Change Scan before Spec-E | Skip the scan because "orchestration patterns seem stable" |
| Write the Friction Log even if FL0 | Skip the Friction Log because "everything went fine" |
| Annotate extension/contradiction vs. Spec-A/B/C explicitly | Silently overwrite prior positions |
| Follow CB5 branching for Jules vs. non-Jules | Produce a Jules-specific output and hope it works for non-Jules |

---

## X — eXamples (Positive and Negative)

### Positive example — correct MUST statement with anchor

```gherkin
# anchor: D.4.2
Feature: Spec Authorship Gate

  Scenario: Agent verifies normative statement discipline before committing
    Given a candidate normative statement containing two requirements joined by "and"
    When the agent runs the normative discipline check
    Then the agent splits the statement into two addressable sub-statements
    And the agent re-assigns stable IDs to both
    And the agent updates all Gherkin anchors that referenced the original ID
```

```markdown
- **D.4.2** A normative statement MUST contain exactly one RFC-2119 keyword.
- **D.4.3** A normative statement that contains two independent requirements MUST be
  split into two separately addressable statements before the spec is committed.
```

### Negative example — MUST in Rationale (violation)

```markdown
### §5.3 Rationale
The agent architecture MUST use a DAG planner to avoid circular dependencies.
```

This violates CB4: all-caps RFC-2119 keywords MUST NOT appear in Rationale prose.
Correct version: "The agent architecture should use a DAG planner to avoid circular
dependencies." (lowercase — not normative).

### Negative example — MUST without source

```markdown
- **E.3.1** A multi-agent handoff MUST serialize all working memory to JSON before
  transferring control.
```

Without a T1/T2 source citation, this is inadmissible as MUST. Correct version: annotate
`[Confidence: low — single community source]` and downgrade to SHOULD pending triangulation.

### Positive example — Repository Linking Manifest (non-Jules)

```markdown
## Repository Linking Manifest

| Artefact | Target Path | Action |
|:---------|:------------|:-------|
| SPEC.md | research/spec-driven-research-agentic-workflows/output/SPEC.md | CREATE |
| friction-log.md | research/spec-driven-research-agentic-workflows/reflection/friction-log.md | CREATE |
| session.log | research/spec-driven-research-agentic-workflows/workspace/session.log | CREATE |
| state.md | research/spec-driven-research-agentic-workflows/synthesis/state.md | CREATE |
| Prior art ref | research/agent-prompt-specs-3-systems-sdd/output/SPEC.md | READ-ONLY |
```

---

## Mandatory Pre-Commit Check (ALL agents)

Before finalizing output, verify every item in this checklist.
A failing item MUST be resolved before output is considered complete.

```
## Pre-Commit Checklist

### Schema
- [ ] §0 present in each of Spec-D, Spec-E, Spec-F (Status, Last Review Date, Sources)
- [ ] §1 BCP-14 paragraph present verbatim in each Spec
- [ ] §§3–7 each contain: Normative Statements, Gherkin, Rationale
- [ ] §9 Source Index present in each Spec
- [ ] §§ numbering is consistent (no gaps, no duplicates)

### Normative Discipline
- [ ] Every statement has exactly one RFC-2119 keyword
- [ ] Every statement specifies the actor
- [ ] No all-caps RFC-2119 keyword appears in any Rationale block
- [ ] Every MUST-level statement has a T1/T2 source documented
- [ ] Every single-source or T3/T4 statement is flagged [Confidence: low]

### Gherkin Validity
- [ ] Every scenario has ≥ 1 Given, ≥ 1 When, ≥ 1 Then
- [ ] Every scenario has a `# anchor:` comment on the line above `Scenario:`
- [ ] Background blocks are only present when ≥ 3 scenarios share setup

### Logs
- [ ] Contradiction Log has ≥ 2 entries
- [ ] M13 Query Expansion Log has ≥ 9 entries
- [ ] Reflection History has ≥ 5 entries with all 5 questions answered
- [ ] World-Change Log present (even if no changes found)

### Repository Protocol
- [ ] friction-log.md declares an explicit FL level (FL0–FL3)
- [ ] Jules: all required folders initialized with readme.md and non-empty files
- [ ] Non-Jules: Repository Linking Manifest present and complete with all artefacts listed
- [ ] prompt.md contains this exact prompt (verbatim, unedited)

### Cross-Reference Integrity
- [ ] Every extension of Spec-A/B/C is annotated [extends X.Y.Z]
- [ ] Every contradiction of Spec-A/B/C is annotated [contradicts X.Y.Z] and logged
- [ ] No confirmed prior is re-researched without explicit justification
```

Only when all applicable boxes are checked may the agent finalize output.

---

*End of prompt. Execute the PRIOR ART BLOCK first. Then proceed step by step.*
