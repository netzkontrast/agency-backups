---
topic: "Agentic Long-Horizon Context Continuity: Normative Specification for Context Engineering, Memory Persistence, and Cross-Session World-Model Synchronization"
slug: "agentic-session-continuity-spec"
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
  (RFC-2119 keyword discipline, enforced by CB4) and a worked-example layer
  to illustrate correct vs. incorrect context engineering patterns as positive
  and negative Gherkin examples.
cross_pollination:
  - source_category: "A"
    step_id: "S6.a"
    description: "Exploration Sanity Pass — Hidden-Aspects + Schema-Gap Hypothesis: identify context-lifecycle dimensions that the five-aspect schema (Explore/Plan/Implement/Review/Validate) forces underground"
  - source_category: "C"
    step_id: "S7.c"
    description: "World-Change Scan — memory/compaction APIs and cross-framework handoff protocols (Google A2A, LangGraph checkpointing, Anthropic Managed Agents) evolve rapidly; verify tentative normative statements before finalizing Spec-H and Spec-I"
constraint_blocks:
  - "0 — Reflection Baseline"
  - "1 — Source Priority Rules"
  - "2 — Temporal Scope"
  - "3 — Output Exclusions"
  - "4 — Spec-Driven Output Grammar (RFC 2119 + Gherkin)"
  - "5 — Repository Linkage Protocol (Jules vs. Non-Jules bifurcation)"
prior_art_refs:
  - "research/agent-prompt-specs-3-systems-sdd/output/SPEC.md — Spec-A/B/C"
  - "research/spec-driven-research-agentic-workflows/output/SPEC.md — Spec-D/E/F"
language: "en"
target_agent: "model-agnostic"
created: "2026-05-03"
version: "1.0"
source_skill: "research-prompt-optimizer v3.1 + spec-skill v1.0"
status: "PROPOSED — awaiting execution"
---

# Research Prompt: Agentic Long-Horizon Context Continuity

> **For the executing AI — read this block before doing anything else.**
>
> This prompt is **entirely self-contained**. Every framework, method, constraint, and
> example you need is defined inline below. You do not need external context, prior
> conversation history, or knowledge of any skill that generated this prompt. Read the
> full prompt before beginning any research or writing.
>
> Your output is **three Specs** — Spec-G, Spec-H, Spec-I — each defining normative
> best practices across the five standard aspects (Explore / Plan / Implement / Review /
> Validate), written in the Spec-Driven Development grammar defined in CONSTRAINT BLOCK 4.
>
> Before doing anything else, execute the **PRIOR ART BLOCK** immediately below.

---

## ⚡ PRIOR ART BLOCK — Execute Before Any Research

This task extends two existing research artefacts. Your behaviour depends on which
agent platform you are running on.

### Branch A — If you are Google Jules (repo-resident agent)

You have filesystem access to the repository that contains this prompt.

**You MUST execute the following steps before proceeding to the research body:**

1. Read the file at `./research/agent-prompt-specs-3-systems-sdd/output/SPEC.md`.
   This document contains Spec-A (Google Jules), Spec-B (Claude Code), and
   Spec-C (Gemini Deep Research). Your output MUST treat their confirmed priors
   as ground truth (do not re-research them).
2. Read the file at `./research/spec-driven-research-agentic-workflows/output/SPEC.md`.
   This document contains Spec-D (Spec-Driven Workflow Governance), Spec-E (Agentic
   Orchestration Patterns), and Spec-F (Repository-Resident Agent Governance). Your
   new Specs G/H/I extend this trilogy at the context-lifecycle layer.
3. Read `./AGENTS.md`, `./RESEARCH.md`, `./FOLDERS.md`, and `./PRE_COMMIT.md`
   to understand the repository's governance protocols.
4. Initialize your working directory at:
   `./research/agentic-session-continuity-spec/`
   following the exact subfolder structure in `RESEARCH.md §Directory Structure`.
5. Save this prompt verbatim to:
   `./research/agentic-session-continuity-spec/prompt.md`
   (it may already exist; do not alter it — verify the content is intact)
6. Then proceed to the **RESEARCH BODY** below.

**Cross-referencing convention for Jules:** When a new normative statement in
Spec-G/H/I directly supersedes, refines, or contradicts a statement in Spec-A through F,
annotate it inline: `[extends B.3.4]` or `[contradicts E.3.2 — see §8]`.

### Branch B — If you are an external research agent

You cannot read the existing repository directly.

**Your output MUST include a `## Repository Linking Manifest` section** (see OUTPUT
SPEC §5 below) that maps every output artefact you produce to its target path in the
repository. A human operator will use this manifest to integrate your findings.

**Prior art summary for non-Jules agents** (treat as authoritative ground truth):

| ID | Confirmed Prior |
|:---|:----------------|
| B.3.4 | Context rot occurs past ~300k tokens; wide reads SHOULD be delegated to subagents |
| B.4.4 | Planning phase and execution phase MUST NOT be merged into a single command |
| D.2.2 | Spec authors MUST chunk a specification into separate files if it exceeds standard agent context windows |
| E.2.1 | A multi-agent orchestrator MUST separate the Planning Agent from the Execution Agent |
| E.3.2 | A ReAct agent MUST externalize its Observation log to a persistent artifact before any context compaction event |
| F.2.1 | A repository-resident agent MUST read AGENTS.md before modifying any file |
| F.3.1 | Every folder touched by an agent MUST contain a readme.md with relative Markdown links |
| All   | Every spec MUST include §1 BCP-14 normative conventions paragraph verbatim |
| All   | Every Gherkin Scenario MUST carry a `# anchor: <ID>` comment line |

Do not re-research these priors. Build on them.

---

## R — Role

You are an **Agentic Systems Architect and Specification Author** with deep expertise in:

- Long-context LLM engineering: context window management, compaction strategies,
  attention dilution mechanisms, and context rot detection
- Agent memory architectures: short-term working memory, episodic memory, semantic
  long-term memory, procedural memory, and graph-enhanced hybrid stores
- Cross-session continuity protocols: session serialization, world-model checkpointing,
  staleness detection, and re-entry contracts for interrupted agentic tasks
- Multi-agent context transfer: state serialization formats, handoff contracts,
  cross-framework interoperability (LangGraph, AutoGen, Google A2A, OpenAI Swarm)
- Anthropic-specific context engineering: Claude context compaction, Managed Agents
  session log model, `getEvents()` event stream interface

You produce outputs that are grounded in vendor documentation, peer-reviewed research,
and production deployment patterns. Every normative statement you emit as MUST has
survived at least two independent T1/T2 source confirmations and one Steelmanning pass.

---

## I — Input

**Research Question (primary):**
What are the normative, specification-driven best practices for preserving agent epistemic
continuity across context window boundaries, multi-session gaps, and cross-agent handoffs —
such that any conformant agent operating on a long-horizon task (>24 hours, >500k tokens,
or across multiple specialized sub-agents) can resume work at any checkpoint without
observable degradation in decision quality, constraint compliance, or world-model accuracy?

**Research Question (decomposed — the three target dimensions):**

1. **Context Engineering Layer (Spec-G):** What are the normative patterns for the
   four core context engineering strategies — Write Context (externalize), Select Context
   (retrieve), Compress Context (compact/summarize), and Isolate Context (delegate to
   subagents) — and when MUST each be applied vs. SHOULD vs. MAY?

2. **Agent Memory Architecture (Spec-H):** What are the normative requirements for a
   multi-tiered agent memory system (STM / MTM / LTM / Graph) that prevents memory
   contamination, supports write isolation, and enables efficient cross-session retrieval
   without full-context reload?

3. **Cross-Session Continuity Protocol (Spec-I):** What MUST a session serialization
   artifact contain to enable a re-entering agent (same or different instance) to resume
   a long-horizon task without hallucinating the missing context? What triggers MUST cause
   an agent to verify world-model staleness before proceeding?

**Why this research is needed now (context for the executing agent):**

The existing Spec-E (Agentic Orchestration Patterns) addresses multi-agent coordination at
the structural level — which agent does what, in what order. It does not address the
*epistemic lifecycle* of an individual agent's understanding: how context is born, grows,
compresses, externalizes, and is reconstituted. This gap has become critical as production
deployments regularly exceed 100k–1M token context windows and as studies have confirmed
>50% performance degradation at those scales. The present research fills that gap by
defining the Context Engineering Layer as a first-class architectural concern.

**Target systems covered (one Spec per dimension):**
- **Spec-G**: Context Engineering Layer — Write/Select/Compress/Isolate strategy patterns
- **Spec-H**: Agent Memory Architecture — STM/MTM/LTM/Graph hierarchy with contamination prevention
- **Spec-I**: Cross-Session Continuity Protocol — session handoff contracts, staleness detection,
  re-entry verification

**Audience:** Software architects and AI systems developers building production long-horizon
agentic pipelines (>24h tasks, multi-session research, novel writing, software development),
familiar with RFC-2119 grammar, Gherkin syntax, and the existing Spec-A through Spec-F
corpus in this repository.

**Depth:** Exhaustive. Every normative statement MUST survive at least one Pre-Commitment
counter-pass and one Steelmanning pass before being emitted as MUST.

**Success criterion:** The three Specs are self-contained, machine-readable, and
operationally complete — a new agent reading only these three Specs and the confirmed
priors table above could implement a compliant context management system without asking
for clarification.

---

## CONSTRAINT BLOCK 0 — Reflection Baseline

You MUST produce a **Reflection Entry** (minimum 5 questions answered) at each of the
following checkpoints. Log these entries under `## Reflection History` in the final
output. Do not skip any checkpoint even if it feels redundant.

**Reflection template (5 questions, answer each in 2–4 sentences):**
1. What do I actually believe right now, and how confident am I?
2. What is the strongest piece of evidence against my current belief?
3. Where am I most likely wrong, and why?
4. What would I do differently if I restarted from scratch knowing what I know now?
5. What is the single highest-value next action?

**Required checkpoints:**
- Kickoff (before first search)
- After each Spec (post-G, post-H, post-I)
- Pre-Synthesis (before assembling the final document)
- Post-Synthesis (after assembly, before the pre-commit check)

---

## CONSTRAINT BLOCK 1 — Source Priority Rules

When researching, apply the following source hierarchy. Document your source tier
for every normative statement that cites evidence.

| Tier | Source Type | Trust Level |
|:-----|:------------|:------------|
| T1 | Vendor primary documentation (Anthropic engineering blog, LangGraph docs, official SDK docs, RFC text) | Highest |
| T2 | Peer-reviewed papers, official engineering blogs, IJCAI/NeurIPS/ICML proceedings | High |
| T3 | Community reproductions, power-user write-ups, GitHub repos with production evidence | Medium |
| T4 | Aggregators, secondary summaries, AI-generated overviews | Low — cite sparingly, annotate |

- A statement sourced only from T4 MUST be flagged `[Confidence: low (single-source)]`.
- A statement sourced from T1+T2 convergence MAY be emitted as MUST without caveat.
- If T1 and T3 contradict each other, log it in the **Contradiction Log** (§Logs).

**Priority sources for this research (pre-identified T1/T2):**

| Source | Tier | Relevance |
|:-------|:-----|:----------|
| Anthropic engineering blog: "Effective context engineering for AI agents" | T1 | Write/Select/Compress/Isolate framework |
| Anthropic Managed Agents documentation | T1 | Session log model, `getEvents()` interface |
| Anthropic Claude context compaction cookbook | T1 | Compaction trigger mechanics |
| LangGraph checkpointing documentation | T1 | State persistence and time-travel |
| Google A2A protocol specification | T1 | Cross-framework handoff standard |
| arxiv:2603.29194 — Multi-Layered Memory Architectures for LLM Agents | T2 | STM/MTM/LTM experimental evaluation |
| arxiv:2601.01885 — Agentic Memory: Unified LTM/STM Management | T2 | Memory policy as agent tool actions |
| arxiv:2601.03236 — MAGMA: Multi-Graph Agentic Memory Architecture | T2 | Graph-enhanced memory production patterns |
| Chroma Research: Context Rot study | T2 | Quantitative context degradation evidence |
| mem0.ai: State of AI Agent Memory 2026 | T2 | Production deployment patterns |

---

## CONSTRAINT BLOCK 2 — Temporal Scope

- **Primary window:** January 1, 2025 – May 3, 2026 (today)
- **Soft background window:** July 1, 2024 – December 31, 2024 (use for context only;
  do not cite as primary evidence for normative statements)
- **Do NOT cite:** anything prior to July 2024 as current practice for memory architectures
  (the field moved rapidly in 2024–2025)
- **Foundational exceptions:** RFC 2119, BCP 14, Gherkin specification, and the original
  ReAct paper (Yao et al., 2022) may be cited regardless of date

Apply a **World-Change Scan** (Step S7.c) at two points:
1. Before beginning Spec-H (memory architectures — rapidly evolving with new releases)
2. Before beginning Spec-I (cross-session protocols — shifting with Google A2A, Anthropic
   Managed Agents API updates). Log results in `## World-Change Log`.

---

## CONSTRAINT BLOCK 3 — Output Exclusions

The following MUST NOT appear in any normative statement or Gherkin scenario:

- Specific token count thresholds as hard acceptance criteria (use relative terms:
  "approaching context limit", "exceeding N% of declared context budget")
- Pricing, quota limits, or rate-limit numbers
- Model version strings as acceptance criteria (e.g., "MUST use claude-sonnet-4-6")
- Comparative rankings of memory frameworks by quality
- Unannounced or rumoured features
- UI surface details in MUST statements (button names, menu paths — these belong in Rationale)

**Exception:** Empirical findings (e.g., ">50% performance degradation at 1M tokens" from
the Chroma study) MAY appear in Rationale sections as motivating evidence, not as
normative thresholds.

---

## CONSTRAINT BLOCK 4 — Spec-Driven Output Grammar (RFC 2119 + Gherkin)

Every normative statement in every Spec MUST conform to the following grammar.

### BCP-14 Normative Keywords

> The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
> **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and
> **OPTIONAL** in every produced Spec are to be interpreted as described in BCP 14
> [RFC 2119] [RFC 8174] **when, and only when, they appear in all capitals**, as
> shown here.

Each produced Spec **MUST** include this paragraph verbatim in its §1.

### Statement discipline

- **One RFC-2119 keyword per statement.** No "and" clauses hiding a second requirement.
- **Specify the actor** in every statement: "The agent MUST…", "The orchestrator SHOULD…",
  "The memory store MUST…"
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

- Spec-G: prefix `G`
- Spec-H: prefix `H`
- Spec-I: prefix `I`

---

## CONSTRAINT BLOCK 5 — Repository Linkage Protocol

### For Jules (repo-resident):

Your output artefacts MUST be written to the following paths:

```
research/agentic-session-continuity-spec/
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
    └── SPEC.md                  ← the three new Specs (G, H, I)
```

Every folder MUST contain a `readme.md` per `FOLDERS.md §Mandatory readme.md Rule`.
Run the full `PRE_COMMIT.md` checklist before invoking `git commit`.

### For non-Jules agents:

Your output `SPEC.md` MUST include a trailing `## Repository Linking Manifest` section:

```markdown
## Repository Linking Manifest

| Artefact | Target Path in Repository | Action |
|:---------|:--------------------------|:-------|
| This SPEC.md | research/agentic-session-continuity-spec/output/SPEC.md | CREATE |
| Spec-G normative statements | (inline in SPEC.md) | CONTAINED |
| Spec-H normative statements | (inline in SPEC.md) | CONTAINED |
| Spec-I normative statements | (inline in SPEC.md) | CONTAINED |
| friction-log.md | research/agentic-session-continuity-spec/reflection/friction-log.md | CREATE |
| session.log | research/agentic-session-continuity-spec/workspace/session.log | CREATE |
| state.md | research/agentic-session-continuity-spec/synthesis/state.md | CREATE |
| Prior art cross-ref (Spec-A/B/C) | research/agent-prompt-specs-3-systems-sdd/output/SPEC.md | READ-ONLY |
| Prior art cross-ref (Spec-D/E/F) | research/spec-driven-research-agentic-workflows/output/SPEC.md | READ-ONLY |
```

---

## S — Steps (ReAct Agentic Spine)

Execute in strict order. Each step is Thought → Action → Observation. Log actions
to `workspace/session.log` (Jules) or equivalent internal log (non-Jules).

---

### S0 — Kickoff Reflection

Write your Kickoff Reflection entry (5 questions per CB0 template).
Commit to your hypothesis for each target Spec before beginning research.

**Hypothesis scaffolding (answer before first search):**

- **G-H0:** The four-strategy framework (Write/Select/Compress/Isolate) from Anthropic's
  engineering blog is T1 and likely already operationally complete — the gap is the
  normative triggering conditions (when MUST each strategy fire, not just that it exists).
- **H-H0:** Memory contamination (semantic drift from naive append) is the primary
  failure mode of current production memory systems, and write isolation is the
  underpublicized fix that lacks normative specification.
- **I-H0:** Cross-session handoff contracts are framework-specific (LangGraph vs. AutoGen
  vs. Anthropic) and no cross-framework normative standard exists yet — meaning Spec-I
  must derive from first principles and annotate framework-specific deviations rather
  than codifying a single standard.

---

### S1 — Prior Art Ingestion

**Jules:** Read the two prior-art files identified in the PRIOR ART BLOCK above.
Extract: (a) all context-management-related normative statements, (b) open questions
deferred to future research, (c) all entries in the Contradiction Log and World-Change Log.

**Non-Jules:** Use the Confirmed Priors table in the PRIOR ART BLOCK as ground truth.

Log extracted prior-art findings under `## Prior Art Extraction` in your synthesis output.

**Specific statements to track (these are the seeds for extension):**

| Statement | Source | What to extend |
|:----------|:-------|:---------------|
| B.3.4: context rot past ~300k tokens → delegate to subagents | Spec-B | When exactly? What observable signals? |
| E.3.2: ReAct agent MUST externalize Observation log before compaction | Spec-E | Define the schema of that externalization |
| D.2.2: chunk spec if it exceeds context window | Spec-D | Chunking strategy for non-spec content too |

---

### S2 — Seed Query Construction

For each target Spec, generate 3–5 seed queries.

**Spec-G (Context Engineering Layer):**
- Anthropic context engineering Write Select Compress Isolate agent 2025
- LLM agent context budget management proactive reactive compaction
- Context rot threshold detection signals agentic systems
- Agent context window eviction strategy priority scoring
- Anthropic Managed Agents session log getEvents interface

**Spec-H (Agent Memory Architecture):**
- Multi-tiered LLM agent memory STM MTM LTM graph 2025 2026
- Memory contamination semantic drift write isolation agent memory
- Graph-enhanced agent memory Mem0 MAGMA production 2026
- Agent memory retrieval selective vs full-context reload performance
- Memory decay forgetting curve LLM agent normative policy

**Spec-I (Cross-Session Continuity Protocol):**
- Agent session serialization artifact schema checkpoint 2025
- LangGraph checkpoint time-travel state persistence agent handoff
- Google A2A agent-to-agent protocol cross-framework handoff
- World-model staleness detection agent re-entry verification
- Long-horizon agent task resume context reconstruction

---

### S3 — Research Execution (Source Triangulation, M06)

For each seed area, gather evidence from at least two independent sources.
Apply Tier classification (CB1) to every source.

**Triangulation requirement:** A normative statement MAY only be emitted as MUST when
at least two T1/T2 sources converge on the same behavioural requirement.

**Specific triangulation targets for this research:**

1. **Compaction trigger conditions**: Find at least one T1 source (Anthropic docs or
   LangGraph docs) and one T2 source (research paper or engineering blog) that specify
   observable signals for when compaction MUST be triggered.

2. **Write isolation requirement**: Find at least two independent sources that identify
   "memory contamination" or "semantic drift from naive append" as a production failure
   mode requiring architectural mitigation.

3. **Session serialization minimum viable set**: Find at least two sources specifying
   what a session handoff artifact MUST contain. Document differences (these will generate
   Contradiction Log entries).

4. **Staleness detection**: Find evidence for how agents detect that their world-model
   has drifted from ground truth (e.g., world-change scan, version hash comparison,
   timestamp checking). Even one T1 source suffices for a SHOULD-level statement.

Log all source titles, tiers, and extracted evidence in `## Source Index`.

---

### S4 — Adversarial Query Expansion (M13 — Mandatory)

For each Spec, execute the following four query expansion axes. Log results under
`## Query Expansion Log`.

| Axis | Spec-G | Spec-H | Spec-I |
|:-----|:-------|:-------|:-------|
| **Adjacent** | "context window scheduling", "token budget allocation agent" | "episodic memory LLM vector graph hybrid" | "distributed system checkpoint protocol", "saga pattern long-running transaction" |
| **Opposing** | "against context compaction — what fails", "compaction information loss risk" | "single flat memory vs tiered memory agent tradeoffs" | "stateless agent better than stateful", "against session serialization overhead" |
| **Abstraction** | "operating system memory paging analogy agent" | "cognitive architecture working memory model AI" | "version control as state management analogy" |
| **Orthogonal** | "database transaction isolation levels as analogy for context isolation" | "library science document taxonomy as memory schema" | "theatrical production prompt book as session continuity artifact" |

**Minimum:** 3 axes active per Spec. M13 MUST NOT be skipped.
Annotate whether each axis produced novel findings.

---

### S5 — Contradiction Log (M07)

Actively maintain the Contradiction Log as findings accumulate.

For every contradiction:
1. State the two conflicting claims precisely
2. Name their sources and tiers
3. Hypothesize a cause
4. State the evidence that would resolve it
5. Emit the normative statement at the *weaker* keyword level until resolved

**Pre-seeded contradiction candidates** (based on the research landscape):

- **Candidate C1**: Anthropic recommends proactive compaction (triggered by context budget);
  some research recommends reactive compaction (triggered only at failure signals). These
  may be two valid strategies for different task types rather than a true contradiction.

- **Candidate C2**: LangGraph's checkpointing stores full state (all messages + tool outputs);
  Anthropic's Managed Agents model externalizes only a curated event stream. One implies
  "save everything", the other implies "save what matters". Resolve: are these different
  audiences (debug/audit vs. production efficiency)?

- **Candidate C3**: Some memory architecture papers argue STM→LTM transfer should be
  automatic (policy-driven); others argue it must be explicit (agent-tool-driven). The
  resolution likely depends on whether the agent is in a supervised or autonomous context.

---

### S6 — Spec Drafting (repeat S6 three times: G, H, I)

For each Spec, fill the following schema. Each aspect block MUST contain:
- 4–6 normative statements (mixed MUST/SHOULD/MAY — see CB4 inflation guard)
- At least one Gherkin scenario with `# anchor:` comment
- A Rationale paragraph (no all-caps RFC-2119 keywords)

```
## Spec-<X>: <Subject>

### §0. Status & Provenance
### §1. Normative Conventions         ← copy BCP-14 paragraph from CB4 verbatim
### §2. System-Level Conventions      (<X>.2.1 … <X>.2.N)
### §3. Aspect 1 — Explore
### §4. Aspect 2 — Plan / Develop Context Strategy
### §5. Aspect 3 — Implement / Execute
### §6. Aspect 4 — Review
### §7. Aspect 5 — Validate / Verify
### §8. Known Limitations & Open Questions
### §9. Source Index
```

**S6.a — Exploration Sanity Pass (Cross-pollination from Category A):**
Before finalizing each Spec, ask: "What aspect of this system is *not* captured by
the five-aspect schema? Is there a hidden sixth dimension the schema forces underground?"

For this research, three candidate hidden dimensions are pre-identified:

| Candidate | Spec | Hidden Dimension |
|:----------|:-----|:----------------|
| Emergency Recovery | Spec-G | What happens when the agent loses its compacted summary? What's the recovery path? |
| Memory Governance / Forgetting Rights | Spec-H | Who can delete or modify agent memory? What normative rules govern intentional forgetting? |
| Trust Anchoring | Spec-I | When a re-entering agent reconstitutes context from a serialized artifact, how does it verify the artifact has not been tampered with? |

Surface strong candidates as §10 Optional Extended Aspect.

**Reflection checkpoint after each Spec.**

---

### S7 — Pre-Synthesis Integrity Check

Before assembling the final document, run the following checklist.
Any ✗ blocks assembly and forces a self-correct loop.

```
☐ ReAct spine present: every step has Thought → Action → Observation
☐ CB0 reflection entries exist at every required checkpoint
☐ M13 Adversarial Query Expansion applied to all three Specs
☐ CB1 Source Priority documented for every MUST-level statement
☐ Cross-pollination steps S6.a and S7.c executed and logged
☐ No <UNFILLED> markers or placeholder text in normative statements
☐ Confirmed priors not re-researched (treated as ground truth)
```

**S7.c — World-Change Scan (Cross-pollination from Category C):**
Before beginning Spec-H, check: have any major memory framework releases (Mem0, LangGraph
memory nodes, Anthropic context APIs, Google A2A updates) occurred in the last 90 days
that affect tentative normative statements? Log results under `## World-Change Log`.
If yes, re-run the affected seed areas in S3.

---

### S8 — Final Assembly

Assemble `SPEC.md` in the following document order:

1. **Executive Summary** (≤300 words)
2. **Common Conventions Across Specs** (cross-cutting rules for G, H, I)
3. **Spec-G** (full schema, §§0–9, optional §10)
4. **Spec-H** (full schema, §§0–9, optional §10)
5. **Spec-I** (full schema, §§0–9, optional §10)
6. **Cross-Spec Dependency Map** — which G/H/I statements build on or supersede A–F
7. **Contradiction Log**
8. **World-Change Log**
9. **Query Expansion Log**
10. **Reflection History**
11. **Source Index**
12. **Repository Linking Manifest** (non-Jules: MANDATORY; Jules: optional confirmation)

---

## E — Expectations

### What success looks like

A successful run produces a `SPEC.md` that:

1. Contains exactly three Specs (G, H, I), each with §§0–9 filled
2. Every normative statement is addressable by stable ID (`G.4.2`, `H.3.1`, `I.7.3`)
3. Every Gherkin scenario has a `# anchor:` comment and `Given/When/Then` structure
4. No Rationale paragraph contains an all-caps RFC-2119 keyword
5. The M13 Query Expansion Log has ≥ 9 entries (3 Specs × 3 axes minimum)
6. The Contradiction Log has at least 3 entries (C1, C2, C3 pre-seeded above)
7. The Reflection History has ≥ 5 entries (Kickoff + 3 post-Spec + Pre-Synthesis)
8. The `friction-log.md` declares an explicit Frustration Level (FL0–FL3)
9. The Cross-Spec Dependency Map explicitly links G/H/I extensions to B.3.4, E.3.2, D.2.2
10. If Jules: output folder structure exactly matches `RESEARCH.md §Directory Structure`
11. If non-Jules: Repository Linking Manifest is present and complete

### What failure looks like

- Normative statements in Rationale blocks (all-caps keywords in prose)
- MUST-level statements with no T1/T2 source citation
- Gherkin scenarios missing `# anchor:` comment
- Reflection entries that are ≤ 2 sentences per question
- Re-researching confirmed priors without annotation `[confirmed prior — re-verified]`
- Contradiction Log empty or pre-seeded contradictions (C1/C2/C3) not investigated
- Spec-I missing cross-framework comparison (LangGraph vs. AutoGen vs. Anthropic approach)

---

## D — Do / Don't

| DO | DON'T |
|:---|:------|
| Emit MUST only when T1/T2 sources converge | Emit MUST on a single T3/T4 source |
| Annotate single-source claims `[Confidence: low]` | Silently emit low-confidence claims as MUST |
| Extend confirmed priors with `[extends B.3.4]` | Re-research confirmed priors from scratch |
| Use SHOULD and MAY for genuinely optional behaviours | Default everything to MUST (MUST inflation) |
| Put empirical numbers (token counts) in Rationale | Put them in normative statements as hard thresholds |
| Run S7.c World-Change Scan before Spec-H | Skip because "memory APIs seem stable" |
| Investigate all three pre-seeded contradictions (C1/C2/C3) | Skip them because they seem obvious |
| Write the Friction Log even if FL0 | Skip the Friction Log because "everything went fine" |
| Annotate extension/contradiction vs. Spec-A through F | Silently overwrite prior positions |
| Surface hidden dimensions (S6.a) for each Spec | Treat the five-aspect schema as exhaustive |
| Follow CB5 branching for Jules vs. non-Jules | Produce Jules-specific output and hope it works externally |

---

## X — eXamples (Positive and Negative)

### Positive example — correct MUST statement for Spec-G with anchor

```gherkin
# anchor: G.5.2
Feature: Context Compaction Gate

  Scenario: Agent triggers compaction before context limit
    Given an agent whose active context has exceeded its declared budget threshold
    When the agent begins a new reasoning step
    Then the agent MUST pause execution and invoke the context compaction procedure
    And the agent writes the compaction summary to the external memory store
    And the agent resumes execution with the compacted context plus the raw tail
```

```markdown
- **G.5.2** The agent MUST trigger compaction before beginning any new reasoning step
  when the active context exceeds the declared context budget threshold.
  [extends B.3.4] [Source: Anthropic context compaction cookbook, T1]
- **G.5.3** The agent MUST write the compaction summary to the persistent external store
  before discarding the raw context segments being replaced.
  [Source: Anthropic Managed Agents session log model, T1]
```

### Negative example — MUST in Rationale (violation)

```markdown
### §5.3 Rationale
The agent MUST always compress context before the window fills. Failure to do so
causes context rot and performance degradation.
```

This violates CB4. Correct version: move the normative statement to the statement list;
in the Rationale block write: "Compaction before the window fills prevents the 'lost-in-the-middle'
phenomenon documented in the Chroma context rot study, where performance drops sharply
as critical constraints get buried by accumulated tool output."

### Negative example — MUST with no source (violation)

```markdown
- **H.3.1** A long-term memory store MUST use a graph structure rather than a vector store.
```

Neither T1 nor T2 sources establish graph as categorically required over vector. Correct
version: `[Confidence: low — single community source]` and downgrade to SHOULD, or
rephrase: "A long-term memory store SHOULD supplement vector retrieval with a graph index
when the agent's tasks require multi-hop relationship traversal." [Source: MAGMA paper, T2]

### Positive example — Cross-Spec Dependency Map entry

```markdown
## Cross-Spec Dependency Map

| New Statement | Extends / Supersedes | Relationship |
|:--------------|:---------------------|:-------------|
| G.5.2 | B.3.4 | Extends: B.3.4 identifies context rot threshold; G.5.2 specifies the triggering mechanic |
| H.3.2 | E.3.2 | Extends: E.3.2 mandates externalizing Observation log; H.3.2 specifies the schema of that externalization |
| I.4.1 | E.2.1 | Refines: E.2.1 mandates Planning/Execution separation; I.4.1 adds the handoff contract requirement |
```

---

## Mandatory Pre-Commit Check (ALL agents)

```
## Pre-Commit Checklist

### Schema
- [ ] §0 present in each of Spec-G, Spec-H, Spec-I (Status, Last Review Date, Sources)
- [ ] §1 BCP-14 paragraph present verbatim in each Spec
- [ ] §§3–7 each contain: Normative Statements, Gherkin, Rationale
- [ ] §9 Source Index present in each Spec
- [ ] §§ numbering consistent (no gaps, no duplicates)

### Normative Discipline
- [ ] Every statement has exactly one RFC-2119 keyword
- [ ] Every statement specifies the actor
- [ ] No all-caps RFC-2119 keyword appears in any Rationale block
- [ ] Every MUST-level statement has a T1/T2 source documented
- [ ] Every single-source or T3/T4 statement is flagged [Confidence: low]

### Gherkin Validity
- [ ] Every scenario has ≥ 1 Given, ≥ 1 When, ≥ 1 Then
- [ ] Every scenario has a `# anchor:` comment on the line above `Scenario:`
- [ ] Background blocks only when ≥ 3 scenarios share setup

### Logs
- [ ] Contradiction Log has ≥ 3 entries (C1/C2/C3 pre-seeded above investigated)
- [ ] M13 Query Expansion Log has ≥ 9 entries
- [ ] Reflection History has ≥ 5 entries with all 5 questions answered
- [ ] World-Change Log present (even if no changes found)

### Repository Protocol
- [ ] friction-log.md declares an explicit FL level (FL0–FL3)
- [ ] Jules: all required folders initialized with readme.md and non-empty files
- [ ] Non-Jules: Repository Linking Manifest present and complete
- [ ] prompt.md contains this exact prompt (verbatim, unedited)

### Cross-Reference Integrity
- [ ] Every extension of Spec-A through F annotated [extends X.Y.Z]
- [ ] Every contradiction of Spec-A through F annotated [contradicts X.Y.Z]
- [ ] Cross-Spec Dependency Map present and complete
- [ ] Pre-seeded contradictions C1, C2, C3 all investigated and logged
```

Only when all applicable boxes are checked may the agent finalize output.

---

*End of prompt. Execute the PRIOR ART BLOCK first. Then proceed step by step.*
