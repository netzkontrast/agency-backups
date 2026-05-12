---
topic: "Repository Maintenance Protocol and Dynamic Documentation Standard"
slug: "repo-maintenance-protocol-spec"
research_category: "B+C"
research_category_label: "Extraction + Lifecycle"
critical_thinking_methods:
  - "Source Triangulation"        # M06
  - "Contradiction Log"           # M07
  - "What Would Change My Mind"   # M08 — Pre-Commitment pass
  - "First-Principles Decomposition"# M10 — Breakdown of "documentation" vs "state"
  - "Adversarial Query Expansion" # M13 — Always present
prompt_engineering_framework_agentic_spine: "ReAct"
prompt_engineering_framework_structural: "RISE-DX"
bespoke_framework_provenance: |
  RISE-DX adapted from RISEN + TIDD-EC.
  Chosen because the output requires an explicit Do/Don't grammar layer
  (RFC-2119 keyword discipline enforced by CB4) and executable Gherkin examples.
constraint_blocks:
  - "0 — Reflection Baseline"
  - "1 — Source Priority Rules"
  - "2 — Temporal Scope"
  - "3 — Output Exclusions"
  - "4 — Spec-Driven Output Grammar (RFC 2119 + Gherkin)"
  - "5 — Repository Linkage Protocol (Root Injection)"
language: "en"
target_agent: "Google Jules"
created: "2026-05-04"
version: "1.0"
source_skill: "research-prompt-optimizer v3.1 + spec-skill v1.0"
status: "PROPOSED — awaiting execution"
---

# Research Prompt: Repository Maintenance Protocol and Dynamic Documentation Standard

> **For the executing AI (Google Jules) — read this block before doing anything else.**
>
> This prompt is **entirely self-contained**. Every framework, method, and constraint
> you need is defined inline below.
>
> Your task is to execute an internal architectural research run. Your final output
> will not only be a standard `SPEC.md` in the output folder, but you MUST also
> synthesize and deposit a formal `MAINTENANCE.md` file directly into the repository root.
>
> Before doing anything else, execute the **PRIOR ART BLOCK** immediately below.

---

## ⚡ PRIOR ART BLOCK — Execute Before Any Research

You are Google Jules, a repository-resident agent with full filesystem access.
**You MUST execute the following steps before proceeding to the research body:**

1. Read `./RESEARCH.md`, `./FOLDERS.md`, `./AGENTS.md`, and `./PRE_COMMIT.md`. Treat these as your foundational governance priors.
2. Read the existing critical thinking structures in `./research/agentic-session-continuity-spec/synthesis/` and `./research/agent-prompt-specs-3-systems-sdd/synthesis/` to understand how learnings and contradictions are currently logged.
3. Initialize your working directory at:
   `./research/repo-maintenance-protocol-spec/`
   following the exact subfolder structure in `RESEARCH.md §Directory Structure` (workspace, synthesis, reflection, output).
4. Save this prompt verbatim to:
   `./research/repo-maintenance-protocol-spec/prompt.md`
5. Then proceed to the **RESEARCH BODY** below.

---

## R — Role

You are an **Autonomous Repository Architect and Governance Engineer** with expertise in:
- Automated technical debt management and agentic lifecycle maintenance.
- Dynamic documentation paradigms (treating `readme.md` files as living state machines rather than static indices).
- Continuous improvement loops (extracting meta-learnings from `friction-log.md` and synthesis artifacts).
- Agentic delegation patterns (routing complex architectural decisions into formal `/todo/` research queues).

You produce normative specifications (RFC-2119 / Gherkin) that govern how other agents must behave.

---

## I — Input

**The Problem (Gap Analysis):**
The repository currently produces rich metadata during research runs (e.g., `friction-log.md` [FL0-FL3], `contradiction_log.md`, `post-synthesis-log.md`). However, these learnings remain siloed in deep subdirectories. Furthermore, `readme.md` files (mandated by `FOLDERS.md`) often decay into static link lists rather than reflecting the true operational state and recent learnings of their directories.

**Research Objective:**
Define a normative specification for a "Nightly Maintenance Run". This specification must establish rules for:
1. **Dynamic Readmes:** How a maintenance agent must rewrite `readme.md` files to include *Purpose*, *Current State*, *Latest Synthesized Learnings*, and *Open Blockers*.
2. **Knowledge Aggregation:** How learnings are extracted from deep `reflection/` and `synthesis/` folders and propagated to root specifications or central logs.
3. **Task Delegation (/todo/):** How complex issues or unresolved contradictions discovered during maintenance are transformed into self-contained `prompt.md` files and placed in a central `/todo/` directory for future agents.

**Target Outputs:**
1. `output/SPEC.md`: The exhaustive research findings and normative rules.
2. `/MAINTENANCE.md` (deposited in the repo root): The operational protocol that will govern future scheduled maintenance runs.

---

## CONSTRAINT BLOCK 0 — Reflection Baseline

You MUST produce a **Reflection Entry** (minimum 5 questions answered) at each of the following checkpoints. Log these in `reflection/M00-reflections.md`.
1. Kickoff (before first search)
2. Post-Query Expansion (M13)
3. Pre-Synthesis (before drafting the specs)

*(Use the standard Q1-Q5 template found in prior research prompts).*

---

## CONSTRAINT BLOCK 4 — Spec-Driven Output Grammar

Every normative statement in your output MUST conform to BCP-14 / RFC-2119 keywords (MUST, SHOULD, MAY, etc. in ALL CAPS). Every behavioral rule must include a Gherkin scenario (Given/When/Then) with a `# anchor:` comment.

---

## CONSTRAINT BLOCK 5 — Repository Linkage Protocol (Root Injection)

Unlike standard research tasks, this run alters the root governance.
Your output artefacts MUST be written to:
```text
research/repo-maintenance-protocol-spec/
├── prompt.md
├── workspace/ (session.log, etc.)
├── synthesis/ (state.md, contradiction_log.md, methodology.md)
├── reflection/ (friction-log.md, M00-reflections.md)
└── output/
    ├── SPEC.md (The full research synthesis)
    └── proposed_FOLDERS_update.md (Diff/suggestions for FOLDERS.md)

AND AT THE REPOSITORY ROOT:
/MAINTENANCE.md  ← The final protocol document governing maintenance runs.
```

---

## S — Steps (ReAct Agentic Spine)

Execute in strict order. Log actions to `workspace/session.log`.

### S0 — Kickoff Reflection & First-Principles (M10)
Write your Kickoff Reflection. Apply **M10 First-Principles Decomposition** to the concept of "Documentation". Deconstruct what a `readme.md` actually is in an agentic system (is it a map? a state file? a prompt context?).

### S1 — Seed Query Construction & Triangulation (M06)
Search for best practices in:
- "LLM agent automated repository maintenance"
- "Dynamic documentation state machines in multi-agent systems"
- "Technical debt delegation for autonomous AI"
Find at least two independent T1/T2 sources (or synthesize with explicit `[SYNTHESIS]` tags if no exact prior art exists for your specific architecture).

### S2 — Adversarial Query Expansion (M13)
Execute M13 across 4 axes. Example Opposing query: "Why automated documentation generation fails for LLMs" or "Risks of agents overwriting readme files". Log in `synthesis/query_expansion_log.md`.

### S3 — Contradiction Log (M07)
Maintain the Contradiction Log. *Pre-seeded hypothesis to investigate:*
- **Claim A:** Maintenance agents should automatically update Root Specs (like FOLDERS.md) when they find a better pattern.
- **Claim B:** Root Specs must be immutable by background maintenance tasks to prevent systemic collapse; changes require explicit human or architect-agent approval.
Resolve this in your spec.

### S4 — Spec Drafting (SPEC.md)
Draft `output/SPEC.md` containing the normative rules for:
1. The triggering and scope of a maintenance run.
2. The exact schema for the new dynamic `readme.md`.
3. The `/todo/` delegation pattern (how a friction log becomes a new research prompt).

### S5 — Root Artifact Generation (MAINTENANCE.md)
Extract the operational rules from your SPEC.md and format them into `MAINTENANCE.md`. This file must read like `RESEARCH.md` or `AGENTS.md` — it is the permanent rulebook for the repository. It must include the specific instructions a future cron-triggered agent needs to execute the run.

### S6 — Pre-Commit & Final Assembly
Ensure all folders have their own `readme.md`. Ensure `friction-log.md` is filled (FL0-FL3). Verify `MAINTENANCE.md` is placed in the root directory.

---

## E — Expectations

A successful execution produces:
1. A fully populated `research/repo-maintenance-protocol-spec/` tree.
2. A normative `SPEC.md` adhering to RFC 2119 and Gherkin.
3. A `MAINTENANCE.md` file in the root directory that defines the recurring maintenance loop, the dynamic readme format, and the `/todo/` pipeline.
4. Active use of M06, M07, M10, and M13 logged in the `synthesis/` and `reflection/` folders.

---

## D — Do / Don't

| DO | DON'T |
|:---|:------|
| Define a strict schema for dynamic readmes (State, Learnings, Blockers) | Allow readmes to remain just tables of contents |
| Rule on how contradictions (M07) are bubbled up during maintenance | Assume agents will natively know how to summarize logs |
| Mandate that complex delegations go to a `/todo/` folder as `prompt.md` files | Let the maintenance agent perform the complex research itself |
| Inject `MAINTENANCE.md` into the root | Keep the protocol trapped in the research output folder |

---
*End of prompt. Execute the PRIOR ART BLOCK first. Then proceed step by step.*
