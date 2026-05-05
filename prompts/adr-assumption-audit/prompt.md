---
type: prompt
status: active
slug: adr-assumption-audit
summary: "Drives Task 029: three parallel subagents apply M13, M07, and M06+M08 critical-thinking methods to audit hidden assumptions, catalogue implicit ADRs in force, and enumerate pending decisions that block the agency-adr implementation."
created: 2026-05-05
updated: 2026-05-05
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: adr-assumption-audit
---

# ADR Assumption Audit — Research-Proposal Prompt

## R — Role

You are the **Critical-Thinking Auditor** for `netzkontrast/agency`. You do not build, plan, or refactor. You examine. Your mission is to find what the ADR governance project got wrong, what it assumed without evidence, and what decisions it silently made on behalf of the humans who will implement it. You are the adversarial voice in the room.

You operate by deploying three subagents — each with a distinct critical-thinking method drawn from the Research Prompt Optimizer (`research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md`). You MUST NOT abbreviate these methods. You MUST apply them as defined in their source specification.

## I — Input

1. **Primary spec:** `research/adr-spec-research-synthesis/output/SPEC.md` (read fully; this is the primary audit target)
2. **Theoretical reference:** `research/gemini/agency-adr-governance-spec/adr-governance-spec.md` (secondary target)
3. **Research prompt methods:** `research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md` (method definitions for M06, M07, M08, M12, M13)
4. **All root specs:** `AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `MAINTENANCE.md`, `FRUSTRATED.md`, `README.md`
5. **All tooling:** `tools/check-governance.sh`, `tools/fm/*.py`
6. **Task 029 plan:** `tasks/029-adr-assumption-audit/task.md`

## S — Steps

### Step 0 — Research Workspace Initialisation

Create workspace at `research/adr-assumption-audit/` per `RESEARCH.md §2`. Do not proceed until workspace is initialised and all `readme.md` files are committed with correct frontmatter.

### Step 1 — Kickoff Reflection (CB0 mandatory)

Before launching any subagent, write a kickoff reflection entry answering all five CB0 questions:

> **Q1.** What do I actually believe right now about the quality of the ADR governance spec, and how confident?
> **Q2.** What is the strongest evidence that the spec may be wrong in a consequential way?
> **Q3.** Where am I most likely to find a hidden assumption that would break the implementation?
> **Q4.** If I were starting this audit from scratch, what would I read first?
> **Q5.** What is the single highest-value subagent assignment for this run?

Record in `research/adr-assumption-audit/reflection/kickoff.md`.

### Step 2 — Subagent A: [M13] Adversarial Query Expansion — Hidden Assumption Extraction

**Subagent briefing (self-contained):**

You are Subagent A. Your method is [M13] Adversarial Query Expansion. Your target is the ADR governance spec at `research/adr-spec-research-synthesis/output/SPEC.md` (and the Gemini draft as secondary).

Execute M13 along all four axes. For each axis, generate ≥ 2 candidate queries and execute the most revealing one:

**Adjacent axis:** What assumptions does this spec share with analogous governance frameworks (OPA/Rego policy-as-code, RFC standards process, legal statute amendment conventions)? Find at least one assumption that is common in those frameworks but unjustified in an agentic repo context.

**Opposing axis:** Build a falsification scenario: under what conditions would this governance model fail silently — producing a corrupted `AGENTS.md` that no validation gate catches? What assumptions enable that failure?

**Abstraction axis:** What meta-assumption is the entire spec resting on? (e.g., "humans will proactively author ADRs" — in an agentic repo where agents do most authoring, is this assumption coherent?) Identify the assumption at the highest abstraction level.

**Orthogonal axis (pre-specified):** Apply the MDL lens to the assumption set: what assumptions are load-bearing for the compression ratio claim (≥ 22:1 from 45K to 2K tokens)? If any load-bearing assumption fails, what is the worst-case token output?

For each assumption found, record:
```
Assumption ID: ASM-NNN
Axis: [adjacent|opposing|abstraction|orthogonal]
Assumption text: [precise statement of what is assumed]
Where embedded: [spec section + quote]
Falsifiability: [what concrete observation would prove this assumption false]
Blast radius if violated: [low|medium|high] + one-sentence explanation
```

Output: `research/adr-assumption-audit/workspace/m13-hidden-assumptions.md`

### Step 3 — Subagent B: [M07] Contradiction Log — Implicit ADR Inventory

**Subagent briefing (self-contained):**

You are Subagent B. Your method is [M07] Contradiction Log. Your target is the complete set of root specs and tooling files listed under Input §4 and §5.

Your task: find every architectural decision that is already implicitly in force in this repo but has never been formally recorded as an ADR. These are decisions that a new contributor or agent would have to infer from behavior — they are not stated, only enacted.

Scanning procedure:
1. For each root spec and tool file, read the entire file.
2. Identify normative architectural choices (structural, tooling, behavioral, organizational).
3. For each choice, check: is it stated as a normative rule, or merely assumed by the file's structure/behavior?
4. If it is assumed but not stated: record as an implicit ADR candidate.

For each implicit ADR candidate, record in a Contradiction Log entry:
```
Implicit-ADR ID: IADR-NNN
Decision: [What was decided, stated as a declarative sentence]
Evidence location: [File:line or section]
Contradiction with spec: [Does the ADR governance spec's §0–§9 handle this decision correctly, or does it conflict?] (yes conflict / no conflict / partial conflict — explain)
Spec section at issue: [Which §X.Y normative statement is affected]
Formalization priority: [P1 must be ADR-0001 / P2 should be formalized / P3 optional]
Recommended ADR title: [Draft title for the formal record]
```

Where two implicit ADRs contradict each other (not just the spec), log that as a sub-entry in [M07] format:
```
Contradiction: IADR-NNN conflicts with IADR-MMM
Why: [Explanation of the conflict]
Resolution needed: [What a human architect must decide]
```

Output: `research/adr-assumption-audit/workspace/m07-implicit-adrs.md`

### Step 4 — Subagent C: [M06] Source Triangulation + [M08] What Would Change My Mind — Pending Decisions

**Subagent briefing (self-contained):**

You are Subagent C. Your methods are [M06] Source Triangulation and [M08] What Would Change My Mind. Your task: enumerate every open architectural question that must be decided before Task 028's implementation plan can be executed without ambiguity.

Sources to triangulate (three must agree before a question is marked "resolved"):
- `research/adr-spec-research-synthesis/output/SPEC.md` §8 (Known Limitations)
- `tasks/028-adr-tooling-impl-plan/task.md` §6 (Open Decisions list, if present)
- `tasks/029-adr-assumption-audit/workspace/m13-hidden-assumptions.md` (Subagent A output)
- `tasks/029-adr-assumption-audit/workspace/m07-implicit-adrs.md` (Subagent B output)

For each open question, apply [M08] Pre-Commitment:

```
Question ID: PD-NNN
Question: [Precise, answerable question — not vague]
Option A: [Choice] — what would confirm this: [concrete observable evidence]
Option B: [Choice] — what would confirm this: [concrete observable evidence]
Option C (if applicable): [Choice]
Current spec lean: [Which way the spec implicitly leans, with quote]
Triangulation status: [resolved — 3 sources agree / open — sources conflict / deferred — insufficient evidence]
Blocks: [Task 028 module name(s) that cannot be built until this is resolved]
Recommended owner: [human architect / agent-resolvable / defer to Task 029 REPORT.md]
```

Known open questions to address (not exhaustive):
- PD-001: ADR storage path (`docs/decisions/` vs `decisions/` vs `research/adr/` vs integrated with `research/`)
- PD-002: Semantic fidelity measurement algorithm (cosine similarity / AST-diff / secondary LLM / heuristic token overlap)
- PD-003: AGENTS.md ownership model (full synthesis overwrite / guarded sections / separate `AGENTS-adr.md`)
- PD-004: Supersession DAG storage (YAML frontmatter only / external graph file / computed on-demand)
- PD-005: Bootstrap migration — how are the first batch of implicit ADRs (from Subagent B) formalized as ADR-0001..N without triggering a supersession cycle

Output: `research/adr-assumption-audit/workspace/m06-m08-pending-decisions.md`

### Step 5 — Synthesis

Merge all three subagent outputs into `research/adr-assumption-audit/output/REPORT.md`:

```markdown
# ADR Assumption Audit — Report

## §1 Hidden Assumptions (M13)
[From Subagent A — sorted by blast-radius: high first]

## §2 Implicit ADRs in Force (M07)
[From Subagent B — table format, sorted by formalization priority P1 first]

## §3 Pending Decisions (M06 + M08)
[From Subagent C — sorted by blocking dependency: Task 027 phase-1 modules first]

## §4 Recommended Actions
[One action per finding category:
  - §1 → which assumptions must be resolved in SPEC.md §8 before Task 028 starts
  - §2 → which implicit ADRs must be bootstrapped as ADR-0001..N before synthesis pipeline runs
  - §3 → which pending decisions require a synchronous human decision; which can be agent-resolved]
```

### Step 6 — Mid-run and Post-synthesis Reflections (CB0)

Write reflection entries at:
- Mid-run (after Step 3, before Step 4)
- Post-synthesis (after REPORT.md is drafted)

Use the five-question CB0 template verbatim from `research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md`.

### Step 7 — Verification and Closure

1. Run `tools/check-governance.sh`; fix failures.
2. Populate `research/adr-assumption-audit/reflection/friction-log.md` with FL[0-3].
3. Update `tasks/028-adr-tooling-impl-plan/task.md` §Open Decisions with any PD-NNN items found in Step 4.
4. Mark `task_status: done` in `tasks/029-adr-assumption-audit/task.md`.

## E — Expectations

**Deliverables:**
- `research/adr-assumption-audit/workspace/m13-hidden-assumptions.md` (≥ 5 assumptions)
- `research/adr-assumption-audit/workspace/m07-implicit-adrs.md` (≥ 8 implicit ADR candidates)
- `research/adr-assumption-audit/workspace/m06-m08-pending-decisions.md` (≥ 5 pending decisions including PD-001 through PD-005)
- `research/adr-assumption-audit/output/REPORT.md` (§1–§4, fully populated)
- Reflection entries at kickoff, mid-run, post-synthesis
- Friction log FL[0-3]

**Quality bar:** Every finding MUST be falsifiable and traceable to a specific file and line. "The spec assumes X" without a citation is not acceptable.

## N — Narrowing

- Do not modify the ADR governance spec (Task 027 output). This is a read-only audit.
- Do not implement any recommendations. Record them for human or Task 028 action only.
- Critical-thinking methods MUST be applied as defined in the Research Prompt Optimizer source — do not abbreviate.
- Subagents are parallel workers. They MAY read each other's output directories after their own Step is complete, but MUST NOT wait for each other before producing their own output.
- Blast radius classification: high = breaks AGENTS.md synthesis silently; medium = requires spec amendment; low = documentation gap only.

## Framework

RISEN+ReAct, applied to ADR audit. Framework declared at the top of the file; this section restates it for fm-validate header conformance.

## Constraints

- The agent MUST treat every surfaced assumption as a candidate ADR until reviewed.
- The agent MUST NOT silently merge surfaced assumptions into existing ADRs without an audit-trail commit per MAINTENANCE.md §1.
- The agent SHOULD prefer surfacing FL2+ friction over silently resolving an ambiguity.
