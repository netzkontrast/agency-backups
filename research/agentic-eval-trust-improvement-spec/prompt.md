---
topic: "Agentic Output Evaluation, Human-Agent Trust Calibration, and Governance Improvement Loop Formalization"
slug: "agentic-eval-trust-improvement-spec"
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
  (existing Spec-A through Spec-F serve as canonical positive examples).
cross_pollination:
  - source_category: "A"
    step_id: "S6.a"
    description: "Exploration Sanity Pass — Hidden-Aspects + Schema-Gap Hypothesis: identify evaluation dimensions that the five-aspect schema forces underground (e.g., temporal decay of trust calibration, error amplification risk in feedback loops)"
  - source_category: "C"
    step_id: "S7.c"
    description: "World-Change Scan — agentic governance standards (OWASP Agentic AI Top 10, EU AI Act enforcement timelines, Microsoft Agent Governance Toolkit updates) and evaluation benchmarks evolve rapidly; verify tentative normative statements before finalizing each Spec"
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
  - "research/agentic-session-continuity-spec/prompt.md — Spec-G/H/I (PROPOSED — verify execution status)"
language: "en"
target_agent: "model-agnostic"
created: "2026-05-04"
version: "1.0"
source_skill: "research-prompt-optimizer v3.1 + spec-skill v1.0"
status: "PROPOSED — awaiting execution"
---

# Research Prompt: Agentic Output Evaluation, Trust Calibration, and Governance Improvement Loops

> **For the executing AI — read this block before doing anything else.**
>
> This prompt is **entirely self-contained**. Every framework, method, constraint, and
> example you need is defined inline below. You do not need external context, prior
> conversation history, or knowledge of any skill that generated this prompt. Read the
> full prompt before beginning any research or writing.
>
> Your output is **three Specs** — Spec-J, Spec-K, Spec-L — each defining normative
> best practices across the five standard aspects (Explore / Plan / Implement / Review /
> Validate), written in the Spec-Driven Development grammar defined in CONSTRAINT BLOCK 4.
>
> Before doing anything else, execute the **PRIOR ART BLOCK** immediately below.

---

## ⚡ PRIOR ART BLOCK — Execute Before Any Research

This task extends up to three existing research artefacts. Your behaviour depends on
which agent platform you are running on.

### Branch A — If you are Google Jules (repo-resident agent)

You have filesystem access to the repository that contains this prompt.

**You MUST execute the following steps before proceeding to the research body:**

1. Read `./research/agent-prompt-specs-3-systems-sdd/output/SPEC.md`.
   This contains Spec-A (Google Jules), Spec-B (Claude Code), Spec-C (Gemini Deep
   Research). Treat their confirmed priors as ground truth; do not re-research them.
2. Read `./research/spec-driven-research-agentic-workflows/output/SPEC.md`.
   This contains Spec-D (Spec-Driven Workflow Governance), Spec-E (Agentic Orchestration
   Patterns), Spec-F (Repository-Resident Agent Governance).
3. Check whether `./research/agentic-session-continuity-spec/output/SPEC.md` exists.
   - If it exists: read it. It contains Spec-G (Context Engineering), Spec-H (Agent
     Memory Architecture), Spec-I (Cross-Session Continuity). Treat as confirmed priors.
   - If it does not exist: the Spec-G/H/I research has not been executed yet. Note this
     in your `workspace/session.log` and proceed without Spec-G/H/I priors.
4. Read `./AGENTS.md`, `./RESEARCH.md`, `./FOLDERS.md`, and `./PRE_COMMIT.md`.
5. Initialize your working directory at:
   `./research/agentic-eval-trust-improvement-spec/`
   following the exact subfolder structure in `RESEARCH.md §Directory Structure`.
6. Save this prompt verbatim to:
   `./research/agentic-eval-trust-improvement-spec/prompt.md`
7. Then proceed to the **RESEARCH BODY** below.

**Cross-referencing convention for Jules:** When a new normative statement in Spec-J/K/L
directly supersedes, refines, or contradicts a statement in Spec-A through Spec-I,
annotate it inline: `[extends F.4.2]` or `[contradicts B.3.4 — see §8]`.

### Branch B — If you are an external research agent

You cannot read the repository directly.

**Your output MUST include a `## Repository Linking Manifest` section** (see CONSTRAINT
BLOCK 5) that maps every artefact you produce to its target path in the repository.

**Prior art summary for non-Jules agents** (treat as authoritative ground truth):

| ID | Confirmed Prior |
|:---|:----------------|
| A.2.5 | Users MUST review and approve a Jules-generated plan before code execution |
| B.2.2 | A Claude Code repo MUST contain a `CLAUDE.md` instruction file |
| B.3.4 | Context rot occurs past ~300k tokens; wide reads SHOULD be delegated to subagents |
| B.4.4 | Planning phase and execution phase MUST NOT be merged into a single command |
| C.3.1 | Gemini Deep Research prompts MUST instruct the agent to use live Google Search grounding |
| D.4.2 | A normative statement MUST contain exactly one RFC-2119 keyword |
| E.3.x | ReAct, Plan-Execute DAG, and JANUS dual-cognition are the three canonical orchestration patterns |
| F.2.x | Every repository that an agent will modify MUST contain governance files (AGENTS.md equivalent) |
| F.4.x | Agent friction SHOULD be reported via a structured frustration-level taxonomy (FL0–FL3) |
| All  | Every spec MUST include §1 BCP-14 normative conventions paragraph verbatim |
| All  | Every Gherkin Scenario MUST carry a `# anchor: <ID>` comment line |

Do not re-research these priors. Build on them.

**Spec-G/H/I status for non-Jules agents:** The Agentic Session Continuity Spec
(Spec-G/H/I) covers Context Engineering Layer, Agent Memory Architecture, and
Cross-Session Continuity Protocol. At the time this prompt was written, it was PROPOSED
but not executed. If you have access to information about Spec-G/H/I, treat it as prior
art. If not, note that gap in your `§8 Known Limitations` sections and proceed.

---

## R — Role

You are an **Autonomous Research Architect and Spec Author** with expertise in:

- Agentic output quality evaluation: multi-dimensional frameworks (CLEAR, Agent-as-a-Judge,
  Beyond Task Completion), trajectory-level process assessment, and normative correctness rubrics
- Human-agent trust calibration: autonomy level taxonomies, risk-tiered approval gates,
  production trust data, and credentialing/certification frameworks for autonomous agents
- Agentic feedback loop formalization: verbal reinforcement learning (Reflexion, ExpeL),
  automatic prompt optimization (DSPy, TextGrad), iterative refinement architectures,
  and the specific gap between task-performance improvement loops and governance-protocol
  improvement loops
- Multi-agent conflict resolution: voting vs. consensus protocols, three-tier escalation
  hierarchies, and artifact-level merge strategies for agentic outputs
- Normative specification writing: RFC-2119 / BCP-14, Gherkin BDD, Spec-Driven Development

You produce outputs that can be audited against their sources, contradict themselves only
explicitly (with resolution proposals), and can be operationalized by a downstream agent
without further clarification.

---

## I — Input

**Research Question (primary):**
What are the normative, specification-driven best practices for (a) *evaluating* the
quality and correctness of agentic outputs beyond task-completion metrics; (b)
*calibrating* the level of human oversight granted to agents based on evidence-based
autonomy levels and risk profiles; and (c) *formalizing* the closed-loop process by
which agent friction signals, self-reports, and failure trajectories feed back into
improved prompts and governance protocols — such that any conformant agent or system
can implement all three layers without ambiguity?

**Research Question (unpacked — what this is NOT):**
This is not a survey of what agents can do (Spec-A/B/C did that). This is not a
governance framework for how agents interact with repositories (Spec-D/E/F). This is not
about context continuity across sessions (Spec-G/H/I). This is the *closing layer* of
the governance pyramid: how do you know if the system is working, how do you decide when
to trust it, and how do you make it get better?

**Target systems covered (one Spec per system):**

- **Spec-J**: Agentic Output Quality Evaluation — a normative framework for multi-dimensional
  quality assessment of agent-produced artifacts (specs, code, plans), covering: trajectory-level
  process evaluation, normative correctness rubrics for spec outputs, LLM-as-Judge and
  Agent-as-a-Judge calibration standards, and the failure modes of task-only benchmarks
- **Spec-K**: Human-Agent Trust Calibration — normative standards for evidence-based autonomy
  level assignment, covering: the five-level autonomy taxonomy, promotion criteria and
  demotion triggers, risk-tier classification of agent actions, multi-agent trust hierarchies,
  and runtime governance gate specifications
- **Spec-L**: Governance Improvement Loop Formalization — normative standards for closing the
  loop from agent friction/failure signals back to improved governance protocols, covering:
  friction taxonomy formalization (extending FL0–FL3), failure trajectory analysis patterns,
  the distinction between task-performance improvement and governance-protocol improvement,
  error amplification risk mitigation, and multi-agent conflict resolution at the artifact level

**Audience:** Software architects and AI systems developers actively building long-horizon
agentic pipelines. Familiar with RFC-2119 grammar, Gherkin syntax, and the prior Spec-A
through Spec-F outputs in this series.

**Depth:** Exhaustive — every normative statement must survive at least one Pre-Commitment
counter-pass and one Steelmanning pass before being emitted as MUST.

**Success criterion:** The three Specs are self-contained, machine-readable, and
operationally complete — a new agent reading only Spec-J/K/L (and the confirmed priors
table above) could instrument an agentic system with quality evaluation, trust gates, and
an improvement loop without asking for clarification.

---

## ⚡ PRE-SEEDED CONTRADICTION BLOCK

The following three contradictions were identified during prompt authoring. You MUST
investigate and attempt to resolve each one. Treat these as hypotheses, not conclusions.

### Pre-Seeded Contradiction C1: Self-Rewarding Loops — Improvement vs. Error Amplification

- **Claim A:** Self-rewarding language models (Meta/NYU, 2024, T2) that use LLM-as-Judge
  to evaluate their own outputs via iterative DPO introduce documented risk of error
  amplification — miscalibrated self-evaluation can compound rather than correct errors
  over time.
- **Claim B:** Multi-AI Iterative Refinement systems (arxiv 2412.17149, Dec 2024, T2) that
  use a separate Evaluation Agent (not the producing agent itself) to assess outputs
  consistently achieve near-0.9+ scores across diverse domains.
- **Hypothesized cause:** The distinction may be self-evaluation (same agent judges own
  output — risk of confirmation bias and error amplification) vs. agent-evaluation (a
  separate judge agent — provides independence, reduces amplification risk).
- **Resolution evidence needed:** A controlled study comparing self-evaluating loops against
  separate-evaluator loops on the same tasks, with the same base model, measuring both
  final quality and error trajectory across iterations.
- **Interim statement level:** SHOULD (weakened from MUST pending resolution)

### Pre-Seeded Contradiction C2: Voting vs. Consensus for Multi-Agent Agreement

- **Claim A:** Voting outperforms consensus by 13.2% on reasoning tasks (arxiv 2502.19130,
  Feb 2025, T2) because it preserves multiple independent reasoning paths.
- **Claim B:** Consensus outperforms voting by 2.8% on knowledge tasks (same source) because
  requiring agreement catches individual factual errors.
- **Hypothesized cause:** Task type is the moderating variable — not a genuine contradiction
  but a conditioning relationship that is often collapsed into a single recommendation.
- **Resolution evidence needed:** A task-type classification rubric that determines which
  protocol to apply before the fact, not post-hoc.
- **Interim statement level:** SHOULD with explicit task-type conditioning

### Pre-Seeded Contradiction C3: CLEAR Framework Correlation Claim

- **Claim A:** CLEAR Framework (arxiv 2511.14136, Nov 2025, T2) reports 0.83 Pearson
  correlation with deployment readiness vs. 0.41 for accuracy-only metrics, validated
  against 15 enterprise leaders and 300 tasks.
- **Claim B:** The sample size (N=15 enterprise leaders, 300 tasks) is insufficient to
  generalize this correlation to the full range of agentic deployment contexts.
- **Hypothesized cause:** CLEAR is a strong framework but its headline statistic is based
  on a convenience sample that may not represent low-resource or domain-specific deployments.
- **Resolution evidence needed:** Replication by an independent research group across a more
  diverse enterprise sample, or a meta-analysis of CLEAR adoption outcomes by early 2027.
- **Interim statement level:** SHOULD (cite CLEAR but caveat N=15 sample)

---

## CONSTRAINT BLOCK 0 — Reflection Baseline

You MUST produce a **Reflection Entry** (minimum 5 questions answered) at each of the
following checkpoints. Log these entries under `## Reflection History` in the final output.
Do not skip any checkpoint, even if it feels redundant.

**Reflection template (5 questions, answer each in 2–4 sentences):**
1. What do I actually believe right now, and how confident am I?
2. What is the strongest piece of evidence against my current belief?
3. Where am I most likely wrong, and why?
4. What would I do differently if I restarted from scratch knowing what I know now?
5. What is the single highest-value next action?

**Required checkpoints:**
- Kickoff (before first search)
- After each Spec (post-J, post-K, post-L)
- Pre-Synthesis (before assembling the final document)
- Post-Synthesis (after assembly, before the pre-commit check)

---

## CONSTRAINT BLOCK 1 — Source Priority Rules

When researching, apply the following source hierarchy. Document the source tier for
every normative statement that cites evidence.

| Tier | Source Type | Trust Level |
|:-----|:------------|:------------|
| T1 | Vendor primary documentation (RFC text, official agent docs) | Highest |
| T2 | Peer-reviewed papers, official engineering blogs | High |
| T3 | Community reproductions, power-user write-ups, GitHub repos | Medium |
| T4 | Aggregators, secondary summaries, AI-generated overviews | Low — cite sparingly, annotate |

- A statement sourced only from T4 MUST be flagged `[Confidence: low (single-source)]`.
- A statement sourced from T1+T2 convergence MAY be emitted as MUST without caveat.
- If T1 and T3 contradict each other, log it in the **Contradiction Log** (see §Logs).

**Key sources identified during prompt authoring (verify and extend):**

| Source | Tier | Topic |
|:-------|:-----|:------|
| arxiv 2511.14136 (CLEAR Framework) | T2 | Spec-J — multi-dimensional evaluation |
| arxiv 2512.12791 (Beyond Task Completion) | T2 | Spec-J — process vs. outcome |
| arxiv 2508.02994 (Agent-as-a-Judge) | T2 | Spec-J — trajectory-level evaluation |
| arxiv 2506.12469 (Levels of Autonomy) | T2 | Spec-K — autonomy taxonomy |
| anthropic.com/research/measuring-agent-autonomy (Jan 2026) | T1 | Spec-K — empirical trust data |
| Microsoft Agent Governance Toolkit (April 2026) | T1 | Spec-K — runtime governance gates |
| arxiv 2506.04133 (TRiSM) | T2 | Spec-K — hierarchical monitoring |
| Cloud Security Alliance Agentic Trust Framework (Feb 2026) | T3 | Spec-K — zero-trust maturity |
| arxiv 2303.11366 (Reflexion, NeurIPS 2023) | T2 | Spec-L — verbal RL |
| arxiv 2512.20845 (Multi-Agent Reflexion) | T2 | Spec-L — failure-derived heuristics |
| arxiv 2412.17149 (Multi-AI Iterative Refinement) | T2 | Spec-L — iterative refinement |
| arxiv 2503.12434 (LLM Agent Optimization Survey) | T2 | Spec-L — feedback taxonomy |
| arxiv 2502.19130 (Voting vs. Consensus) | T2 | Spec-L — conflict resolution |
| Google A2A Protocol (April 2025) | T1 | Spec-L — agent communication (not resolution) |
| EU AI Act (Aug 2024, enforcement Aug 2026) | T1 | Spec-K — regulatory floor |
| OWASP Agentic AI Top 10 (Dec 2025) | T3 | Spec-K — risk taxonomy |

---

## CONSTRAINT BLOCK 2 — Temporal Scope

- **Primary window:** January 1, 2025 – May 4, 2026 (today)
- **Soft background window:** July 1, 2024 – December 31, 2024 (use for context only;
  do not cite as primary evidence for current practice)
- **Do NOT cite:** anything prior to July 2024 as current practice; exception: foundational
  frameworks cited in the prompt authoring list (Reflexion 2023, Constitutional AI 2022)
  may be cited as foundational T2 with explicit date caveat
- **Do NOT speculate** about capabilities not yet released or announced

Apply a **World-Change Scan** (Step S7.c) at two points:
1. Before beginning Spec-K (trust calibration — regulatory and vendor policy shift rapidly;
   EU AI Act enforcement starts August 2026)
2. Before beginning Spec-L (feedback loops — DSPy, TextGrad, and related automatic prompt
   optimization frameworks are updated frequently)
Log results in `## World-Change Log`.

---

## CONSTRAINT BLOCK 3 — Output Exclusions

The following MUST NOT appear in any normative statement or Gherkin scenario:

- Pricing, quota limits, or rate-limit numbers
- Model version strings as acceptance criteria (e.g., "MUST use Claude Sonnet 4.6")
- Comparative rankings of agents by quality
- Unannounced or rumoured features
- UI surface details in MUST statements (button names, menu paths — Rationale only)
- Specific benchmark pass-rate numbers as acceptance criteria (e.g., "MUST achieve 0.83
  on the CLEAR correlation metric") — these belong in Rationale, not normative statements

---

## CONSTRAINT BLOCK 4 — Spec-Driven Output Grammar (RFC 2119 + Gherkin)

Every normative statement in every Spec MUST conform to the following grammar.

### BCP-14 Normative Keywords

> The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
> **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and
> **OPTIONAL** in every produced Spec are to be interpreted as described in BCP 14
> [RFC 2119] [RFC 8174] **when, and only when, they appear in all capitals**, as shown here.

Each produced Spec **MUST** include this paragraph verbatim in its §1.

### Statement discipline

- **One RFC-2119 keyword per statement.** No "and" clauses hiding a second requirement.
- **Specify the actor** in every statement: "The evaluation agent MUST…", "The operator SHOULD…"
- **Testable.** If a statement cannot be checked against a Gherkin scenario, rewrite it.
- **No all-caps keywords in rationale prose.** Lowercase in rationale is fine.
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

- Spec-J: prefix `J`
- Spec-K: prefix `K`
- Spec-L: prefix `L`

---

## CONSTRAINT BLOCK 5 — Repository Linkage Protocol

### For Jules (repo-resident):

Your output artefacts MUST be written to the following paths:

```
research/agentic-eval-trust-improvement-spec/
├── readme.md
├── prompt.md                    ← this file, verbatim
├── workspace/
│   ├── readme.md
│   ├── session.log
│   └── (other scratchpad notes — delete execution scripts before commit)
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
    └── SPEC.md                  ← Spec-J, Spec-K, Spec-L
```

Every folder MUST contain a `readme.md` per `FOLDERS.md §Mandatory readme.md Rule`.
Run the full `PRE_COMMIT.md` checklist before invoking `git commit`.

### For non-Jules agents:

Your output `SPEC.md` MUST include a trailing `## Repository Linking Manifest` section:

```markdown
## Repository Linking Manifest

| Artefact | Target Path in Repository | Action |
|:---------|:--------------------------|:-------|
| This SPEC.md | research/agentic-eval-trust-improvement-spec/output/SPEC.md | CREATE |
| Spec-J normative statements | (inline in SPEC.md) | CONTAINED |
| Spec-K normative statements | (inline in SPEC.md) | CONTAINED |
| Spec-L normative statements | (inline in SPEC.md) | CONTAINED |
| friction-log.md | research/agentic-eval-trust-improvement-spec/reflection/friction-log.md | CREATE |
| session.log | research/agentic-eval-trust-improvement-spec/workspace/session.log | CREATE |
| state.md | research/agentic-eval-trust-improvement-spec/synthesis/state.md | CREATE |
| Prior art ref (Spec-A/B/C) | research/agent-prompt-specs-3-systems-sdd/output/SPEC.md | READ-ONLY REFERENCE |
| Prior art ref (Spec-D/E/F) | research/spec-driven-research-agentic-workflows/output/SPEC.md | READ-ONLY REFERENCE |
| Prior art ref (Spec-G/H/I) | research/agentic-session-continuity-spec/output/SPEC.md | READ-ONLY REFERENCE (if exists) |
```

---

## S — Steps (ReAct Agentic Spine)

Execute in strict order. Each step is Thought → Action → Observation. Log actions to
`workspace/session.log` (Jules) or equivalent internal log (non-Jules).

---

### S0 — Kickoff Reflection

Write your Kickoff Reflection entry (5 questions per CB0 template). Commit to your
hypothesis for each target Spec before beginning research. State explicitly whether
Spec-G/H/I has been executed (based on Branch A filesystem check or Branch B knowledge).

---

### S1 — Prior Art Ingestion

**Jules:** Read the files listed in PRIOR ART BLOCK §Branch A steps 1–3. Extract:
(a) all cross-cutting conventions applicable to J/K/L; (b) any open questions from §8
of each existing Spec that directly motivate J/K/L; (c) the Contradiction Log from
Spec-D/E/F; (d) any friction-log items from existing research that flagged evaluation
or trust gaps.

**Non-Jules:** Use the Prior Art Summary table in the PRIOR ART BLOCK as ground truth.
Additionally, treat the three Pre-Seeded Contradictions (C1, C2, C3) as hypothesis
entries already in your Contradiction Log — investigate and attempt to resolve them.

Log extracted prior-art findings under `## Prior Art Extraction` in your synthesis output.

---

### S2 — Seed Query Construction

For each target Spec, generate 3–5 seed queries. Queries MUST be specific, 3–8 words,
and distinct from each other.

**Spec-J seed areas (Agentic Output Quality Evaluation):**
- Multi-dimensional agentic evaluation beyond task completion (CLEAR, Beyond Task Completion)
- Agent-as-a-Judge trajectory evaluation — process quality vs. terminal output
- Normative correctness evaluation for AI-generated specifications and documents
- Constitutional AI self-critique adapted for quality (not safety) domains
- Reward hacking and benchmark gaming in agentic evaluation settings

**Spec-K seed areas (Human-Agent Trust Calibration):**
- Five-level autonomy taxonomy for AI agents — operationalization and promotion criteria
- Empirical trust calibration in production agentic systems (Anthropic, Google Jules data)
- Runtime governance gate design — multi-stage policy pipelines for agent actions
- OWASP Agentic AI Top 10 — risk taxonomy and mitigation mapping
- EU AI Act high-risk AI obligations — human oversight requirements for autonomous agents
- Multi-agent trust hierarchies — trusting orchestrators to oversee sub-agents

**Spec-L seed areas (Governance Improvement Loop Formalization):**
- Reflexion and failure-derived heuristics — verbal RL for agentic improvement
- DSPy and TextGrad — automatic prompt optimization from agent failure trajectories
- Multi-AI iterative refinement — evaluation-agent-driven improvement cycle
- Error amplification risk in self-rewarding agentic loops — mitigation protocols
- Governance protocol improvement from agent self-reports — the missing loop
- Multi-agent conflict resolution at artifact level — beyond voting/consensus to merge protocols

---

### S3 — Research Execution (Source Triangulation, M06)

For each seed area, gather evidence from at least two independent sources. Apply Tier
classification (CB1) to every source.

**Triangulation requirement:** A normative statement MAY only be emitted as MUST when
at least two T1/T2 sources converge on the same behavioural requirement.

**Priority note:** The following gaps were confirmed as open research problems during
prompt authoring. If you find sources that fill these gaps, they represent novel
findings that MUST be foregrounded in the relevant Spec:

1. No published rubric evaluates normative correctness of agentic spec documents
   (distinct from code correctness or safety compliance). If found → Spec-J §6.
2. No validated algorithm exists for recommending when to promote an agent to a higher
   autonomy level. If found → Spec-K §5.
3. No production agentic system publishes a formalized mechanism for feeding friction
   signals back into governance protocol improvements (as opposed to task-performance).
   If found → Spec-L §4 or §5.
4. No artifact-level conflict resolution protocol exists for two agents producing
   divergent versions of the same document. If found → Spec-L §6.

Log source titles, tiers, and specific evidence extracted in `## Source Index`.

---

### S4 — Adversarial Query Expansion (M13 — Mandatory)

For each Spec, execute the following four query expansion axes. Log results under
`## Query Expansion Log`. Annotate whether each axis produced novel findings.

| Axis | Description |
|:-----|:------------|
| **Adjacent** | Neighbouring concepts that might surface hidden requirements |
| **Opposing** | Searches for failure cases, criticisms, known anti-patterns |
| **Abstraction** | Step up one level — what broader pattern does this instantiate? |
| **Orthogonal** | Completely lateral — what adjacent domain solved a similar problem? |

**Minimum:** 3 axes active per Spec. M13 MUST NOT be skipped. If an axis finds nothing
novel, log it explicitly as "no novel findings".

**Suggested orthogonal domains for inspiration:**
- Spec-J (Evaluation): Software quality assurance standards (ISO/IEC 25010); clinical
  trial evaluation protocols; aviation safety auditing (DO-178C)
- Spec-K (Trust Calibration): Medical device autonomy levels (FDA AI/ML Software as
  Medical Device); nuclear safety human-machine interface standards; aircraft autopilot
  certification levels
- Spec-L (Improvement Loops): ISO 9001 continual improvement cycle; software retrospective
  frameworks (blameless post-mortems); academic peer review improvement processes

---

### S5 — Contradiction Log (M07)

Maintain an active Contradiction Log throughout the research. The three Pre-Seeded
Contradictions (C1, C2, C3 in the PRIOR ART BLOCK above) MUST be the first three entries.
Add additional contradictions as they emerge.

For every contradiction (new or pre-seeded):
1. State the two conflicting claims precisely
2. Name their sources and tiers
3. Hypothesize a cause (framing difference, temporal gap, audience mismatch)
4. State the evidence that would resolve it
5. Emit the normative statement at the *weaker* keyword level until resolved

---

### S6 — Spec Drafting (per Spec, repeat S6 three times)

For each Spec (J, K, L), fill the following schema. Each aspect block MUST contain:
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
Before finalizing each Spec, ask: "What aspect of this system is *not* captured by the
five-aspect schema? Is there a hidden sixth dimension the schema forces underground?"

Suggested hidden-aspect hypotheses to investigate:
- Spec-J: Does the schema adequately capture *temporal decay* of evaluation validity
  (an output deemed high-quality today may be outdated/wrong next quarter)?
- Spec-K: Does the schema capture *multi-agent trust transitivity* (if A trusts B and
  B trusts C, does A transitively trust C, and should it)?
- Spec-L: Does the schema capture *improvement loop termination criteria* — when does
  a governance improvement loop converge, and how do you know to stop?

Log candidates under `## Hidden Aspects`. Surface strong candidates as §10 sections.

**Reflection checkpoint after each Spec.**

---

### S7 — Pre-Synthesis Integrity Check

Before assembling the final document, run the following 7-item checklist.
Any ✗ blocks assembly and forces a self-correct loop.

```
☐ ReAct spine is present and every step has Thought → Action → Observation
☐ CB0 reflection entries exist at every required checkpoint
☐ M13 Adversarial Query Expansion was applied to all three Specs
☐ CB1 Source Priority is documented for every MUST-level statement
☐ Pre-Seeded Contradictions C1, C2, C3 are in the Contradiction Log with investigation notes
☐ Cross-pollination steps S6.a and S7.c have been executed and logged
☐ No <UNFILLED> markers or placeholder text remains in normative statements
```

**S7.c — World-Change Scan (Cross-pollination from Category C):**
Before beginning Spec-K, check: have any major regulatory changes (EU AI Act enforcement,
new OWASP Agentic AI guidance, new vendor governance toolkit releases) occurred in the
last 90 days that affect tentative normative statements? Before beginning Spec-L, check:
have any major updates to DSPy, TextGrad, or Reflexion occurred that change their
applicability recommendations? Log results under `## World-Change Log`.

---

### S8 — Final Assembly and Linking Manifest

Assemble `SPEC.md` in the following document order:

1. **Executive Summary** (≤300 words — what Spec-J/K/L collectively establish)
2. **Common Conventions Across Specs** (cross-cutting rules for J, K, and L)
3. **Spec-J** (full schema §0–§9, optional §10)
4. **Spec-K** (full schema §0–§9, optional §10)
5. **Spec-L** (full schema §0–§9, optional §10)
6. **Cross-Spec Dependency Map** — table mapping J/K/L statements to prior Spec-A through
   Spec-I statements they extend, refine, or contradict
7. **Contradiction Log** (all entries including C1/C2/C3 with resolution status)
8. **World-Change Log**
9. **Query Expansion Log** (M13 results for all three Specs)
10. **Reflection History** (all checkpoint entries in chronological order)
11. **Source Index** (all sources, tiered, linked)
12. **Repository Linking Manifest** (non-Jules agents: MANDATORY; Jules: optional confirmation)

---

## E — Expectations

### What success looks like

A successful run produces a `SPEC.md` that:

1. Contains exactly three Specs (J, K, L), each with §§0–9 filled (and optional §10)
2. Every normative statement is addressable by stable ID (`J.4.3`, `K.2.1`, `L.7.2`)
3. Every Gherkin scenario has a `# anchor:` comment and conforms to `Given/When/Then`
4. No rationale paragraph contains an all-caps RFC-2119 keyword
5. The M13 Adversarial Query Expansion Log has ≥ 9 entries (3 Specs × 3 axes minimum)
6. The Contradiction Log has at least 5 entries (C1/C2/C3 pre-seeded + ≥ 2 discovered)
7. The Reflection History has ≥ 5 entries (Kickoff + 3 post-Spec + Pre-Synthesis)
8. The `friction-log.md` declares an explicit Frustration Level (FL0–FL3)
9. Each of the four confirmed open research problems (§S3 priority note) is addressed
   — either by citing a newly found source, or by explicitly marking `[NOT-FOUND — reason]`
10. If non-Jules: Repository Linking Manifest is present and complete
11. If Jules: the output folder structure exactly matches `RESEARCH.md §Directory Structure`

### What failure looks like

- Normative statements in Rationale blocks (all-caps keywords in prose)
- MUST-level statements with no T1/T2 source citation
- Gherkin scenarios missing `# anchor:` comment
- Reflection entries ≤ 2 sentences per question
- Pre-Seeded Contradictions C1/C2/C3 not appearing in the Contradiction Log
- Ignoring the confirmed open research problems in §S3 without explicit `[NOT-FOUND]` markers
- Friction log absent or empty

---

## D — Do / Don't

| DO | DON'T |
|:---|:------|
| Emit MUST only when T1/T2 sources converge | Emit MUST on a single T3/T4 source |
| Annotate single-source claims with `[Confidence: low]` | Silently emit low-confidence claims as MUST |
| Annotate cross-references to Spec-A through Spec-I | Re-research confirmed priors from scratch |
| Use SHOULD/MAY for genuinely optional behaviours | Default everything to MUST (MUST inflation) |
| Distinguish self-evaluation loops from separate-evaluator loops (C1 distinction) | Treat all feedback loops as equivalent |
| Condition voting vs. consensus recommendation on task type (C2 resolution) | Make a blanket recommendation for one protocol |
| Caveat CLEAR correlation claim with sample size note (C3) | Emit CLEAR's 0.83 figure as a hard normative criterion |
| Mark open problems `[NOT-FOUND — reason]` and continue | Invent data to fill gaps |
| Run S7.c World-Change Scan before Spec-K (regulatory) and Spec-L (tooling) | Skip the scan |
| Write the Friction Log even if FL0 | Skip the Friction Log |
| Annotate extension/contradiction vs. Spec-A through Spec-I explicitly | Silently overwrite prior positions |

---

## X — eXamples (Positive and Negative)

### Positive example — Spec-J evaluation criterion with anchor

```gherkin
# anchor: J.5.2
Feature: Agent Output Quality Gate

  Scenario: Evaluation agent assesses agentic spec for normative completeness
    Given a candidate spec document produced by an executing agent
    When the evaluation agent applies the multi-dimensional quality rubric
    Then the evaluation agent MUST produce scores across at least four dimensions:
         process compliance, normative statement discipline, source traceability,
         and Gherkin scenario coverage
    And the evaluation agent MUST flag any dimension scoring below the defined
        threshold as a blocking defect before the spec is committed
```

```markdown
- **J.5.2** The evaluation agent MUST assess agentic spec outputs across at least
  four quality dimensions: process compliance, normative statement discipline,
  source traceability, and Gherkin scenario coverage.
- **J.5.3** The evaluation agent MUST treat any dimension scoring below its defined
  threshold as a blocking defect.
```

### Negative example — MUST without source

```markdown
- **K.3.1** A deployed agent MUST NOT be granted Level 4 autonomy until it has
  completed 500 tasks without a human-overridden error.
```

Without a T1/T2 source for the "500 tasks" threshold, this is inadmissible as MUST.
Correct version: downgrade to SHOULD, or replace the specific number with a
verifiable criterion derived from a source, and annotate source tier.

### Negative example — MUST in Rationale (CB4 violation)

```markdown
### §5.3 Rationale
The system MUST use a separate Evaluation Agent (not the producing agent) to avoid
the error amplification risk documented in self-rewarding loops.
```

Correct version: move this to a normative statement with an anchor, or rewrite Rationale
in lowercase: "Using a separate evaluation agent is recommended to avoid the error
amplification risk documented in self-rewarding loops (see C1 Contradiction Log)."

### Positive example — handling an open research problem

```markdown
#### §6.3 — Normative Correctness Evaluation for Spec Documents

No published framework was identified that addresses normative correctness evaluation
for AI-generated specification documents distinct from code correctness or safety
compliance.
[NOT-FOUND — no T1/T2 source found for spec-document normative correctness rubrics;
see §8 Open Questions for recommendations on filling this gap]

- **J.6.3** The evaluation agent SHOULD apply the normative statement discipline
  criteria from CB4 (RFC 2119 keyword count, actor specification, Gherkin anchor
  presence) as a proxy normative correctness rubric until a formal standard is published.
  [Confidence: low — derived from CB4 of this specification series, not an external standard]
```

---

## Mandatory Pre-Commit Check (ALL agents)

Before finalizing output, verify every item in this checklist.
A failing item MUST be resolved before output is considered complete.

```
## Pre-Commit Checklist

### Schema
- [ ] §0 present in each of Spec-J, Spec-K, Spec-L (Status, Last Review Date, Sources)
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
- [ ] Contradiction Log has ≥ 5 entries (C1/C2/C3 pre-seeded + ≥ 2 discovered)
- [ ] Pre-Seeded C1, C2, C3 each have investigation notes (not just copied hypothesis)
- [ ] M13 Query Expansion Log has ≥ 9 entries
- [ ] Reflection History has ≥ 5 entries with all 5 questions answered
- [ ] World-Change Log present (two entries: pre-Spec-K and pre-Spec-L scans)

### Open Research Problems
- [ ] All four confirmed open problems (§S3 priority note) have a resolution note or
      explicit [NOT-FOUND — reason] marker in the relevant Spec section
- [ ] Any [NOT-FOUND] item has a §8 open question entry and a suggested future research path

### Repository Protocol
- [ ] friction-log.md declares an explicit FL level (FL0–FL3)
- [ ] Jules: all required folders initialized with readme.md and non-empty files
- [ ] Non-Jules: Repository Linking Manifest present and complete
- [ ] prompt.md contains this exact prompt (verbatim, unedited)

### Cross-Reference Integrity
- [ ] Every extension of Spec-A through Spec-I is annotated [extends X.Y.Z]
- [ ] Every contradiction of prior Specs is annotated [contradicts X.Y.Z] and logged
- [ ] No confirmed prior is re-researched without explicit justification
- [ ] Spec-G/H/I status (executed or not) is documented in §0 of each new Spec
```

Only when all applicable boxes are checked may the agent finalize output.

---

*End of prompt. Execute the PRIOR ART BLOCK first. Then proceed step by step.*
