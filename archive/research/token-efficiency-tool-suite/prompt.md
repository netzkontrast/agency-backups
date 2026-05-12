---
type: prompt
status: active
slug: token-efficiency-tool-suite
summary: "Research prompt: survey public GitHub repos tackling token efficiency via mandatory tool calling; synthesise findings into a Token Efficiency Tool Suite spec for this repository."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: "token-efficiency-tool-suite"
prompt_spawned_from_research: ""
---

# Token Efficiency Tool Suite — Research Proposal

## Framework

**RISEN + ReAct.** This is a multi-step, evidence-gathering task that requires iterative search, observation, and reflection before synthesis. RISEN provides the structural skeleton (Role, Input, Steps, Expectations, Constraints); ReAct governs the inner execution loop (Thought → Action → Observation cycles inside §Steps).

---

## § RFC 2119

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

---

## R — Role

You are a senior research engineer specialising in LLM agent efficiency. Your task is to survey the public GitHub ecosystem for repositories that enforce or strongly encourage **token efficiency via mandatory tool calling** — architectures where agents are structurally required to invoke tools (rather than generating from context) as a mechanism for controlling token spend. You will synthesise your findings into a formal specification for a Token Efficiency Tool Suite to be built into this repository.

---

## I — Input

Read the following files before beginning:

1. `/maintenance/language-spec.md` — canonical RFC 2119 and Gherkin definitions you MUST apply in the output spec.
2. `/RESEARCH.md` — directory structure, workflow, and pre-commit checks you MUST satisfy.
3. `/TASK.md §3` — Frontmatter Ontology; every file you create MUST carry conforming frontmatter.
4. `/AGENTS.md §Spec Language Reference` — quick-reference summary of the language spec.
5. (Context) The `RTK` tool (Rust Token Killer) is already active in this environment as a transparent proxy that filters command output to reduce token consumption. Your spec SHOULD complement, not duplicate, RTK.

---

## S — Steps

Execute the following steps. Each step is a ReAct cycle: state your **Thought**, take the **Action**, record the **Observation**, then proceed.

### Step 1 — Seed Query Design

You MUST design at least four search query axes before issuing any GitHub search:

- **Axis A — Mandatory tool calling:** repos where agents *cannot* answer without invoking a tool (e.g., "forced tool use", "tool-only agent", "no hallucination via tool constraint").
- **Axis B — Token budget enforcement:** repos that explicitly budget, meter, or cap token usage at runtime (e.g., "token budget", "context compression", "token-aware agent").
- **Axis C — Structured output coercion:** repos using strict schemas, grammars, or output validators to prevent verbose free-form generation (e.g., "structured output LLM", "grammar-constrained generation", "json-mode agent").
- **Axis D — Context window management tooling:** repos providing utilities to trim, compress, or prioritise context before it reaches the model (e.g., "context pruning", "context manager LLM", "token-efficient RAG").

Log your seed queries in `workspace/session.log`.

### Step 2 — GitHub Search Execution

For each axis, you MUST execute at least two GitHub searches. For each search result:

1. Record the repo name, star count, last-commit date, and a one-sentence description in `workspace/session.log`.
2. Flag any repo where mandatory tool calling is *structural* (enforced by the framework architecture, not just documented as a best practice). These are **high-relevance** candidates.
3. Flag any repo where token budget enforcement occurs at the *invocation layer* (before the LLM is called), not post-hoc. These are **high-relevance** candidates.

You MUST collect at least 10 distinct repositories across all axes before proceeding to Step 3. You SHOULD collect up to 25.

### Step 3 — Deep Dive (High-Relevance Repos)

For each high-relevance repo identified in Step 2, you MUST:

1. Read the repository's README and any `AGENTS.md`, `CLAUDE.md`, or architecture docs.
2. Identify the specific mechanism by which token efficiency is enforced (schema, hook, middleware, grammar, budget decorator, etc.).
3. Note any reusable patterns, abstractions, or primitives that could be adapted for this repository.
4. Record findings in `workspace/repo-<slug>.md` (one file per repo).

### Step 4 — Adversarial Query Expansion (M13)

Apply M13 Adversarial Query Expansion across four axes. For each axis, issue at least one additional search query and record whether it produced novel findings:

- **Adjacent axis:** broaden the search scope slightly (e.g., from "mandatory tool calling" to "tool-first agent architecture").
- **Opposing axis:** search for the failure mode (e.g., "token overrun agent", "context overflow LLM crash").
- **Abstraction axis:** search for the concept generalised (e.g., "constraint-driven LLM inference", "bounded generation").
- **Orthogonal axis:** search for analogous solutions in other domains (e.g., "budget-constrained query planning SQL", "memory-bounded inference").

Log each axis and whether it modified the candidate repo list.

### Step 5 — Contradiction Log (M07)

Identify and document at least one genuine contradiction or tension across the surveyed repos. Examples: "Repo X claims mandatory tool calling reduces tokens; Repo Y shows it increases overhead for simple queries." Each contradiction MUST be written as:

```
Contradiction: <short label>
Claim A: <what one source says>
Claim B: <what another source says>
Hypothesised cause: <why they might both be right>
Evidence to resolve: <what would settle it>
```

### Step 6 — Synthesis

Populate `/synthesis/` per `RESEARCH.md §2`:

- `methodology.md` — describe which methods were applied (M01, M06, M07, M13) and what each produced.
- `tracks.md` — one entry per search axis (A, B, C, D + M13 expansions).
- `state.md` — checklist of every synthesis step; mark each `[x]` as completed.
- `post-synthesis-log.md` — chronological merge log: what evidence was combined and in what order.

You MUST complete all `state.md` checklist items before proceeding to Step 7.

### Step 7 — Reflection (Five Milestones)

Write five reflection files in `/reflection/`, one per milestone. Each file MUST answer the five standard questions:

1. What do I actually believe right now, and how confident?
2. What is the strongest piece of evidence against my current belief?
3. Where am I most likely wrong, and why?
4. What would I do differently if restarting from scratch with current knowledge?
5. What is the single highest-value next action?

Milestones: `M00-kickoff.md`, `M00-midrun.md`, `M00-post-query.md`, `M00-pre-synthesis.md`, `M00-post-synthesis.md`.

You MUST also write `friction-log.md` with the highest FL level experienced (FL0–FL3), per `FRUSTRATED.md`.

### Step 8 — Draft the Spec

Write `/output/SPEC.md` with the following mandatory sections, in order:

1. **Executive Summary** — 150 words max. What was found and what the spec recommends.
2. **Landscape Map** — table of all surveyed repos: name, axis, star count, enforcement mechanism, relevance (high/medium/low).
3. **Design Hypotheses** — H1…Hn. Each hypothesis MUST be falsifiable and annotated with supporting evidence.
4. **Surviving Architecture** — which hypothesis survives falsification tests, and why. MUST include at least one ASCII diagram showing the proposed tool suite architecture.
5. **Normative Specification** — RFC 2119 clauses for the tool suite, structured as:
   - `§ Tool Suite Roles` — what each tool in the suite does.
   - `§ Mandatory Invocation Points` — where in the agent workflow each tool MUST be called.
   - `§ Token Budget Rules` — how tools enforce or report token consumption.
   - `§ Integration with existing repo hooks` — how the suite connects to `.githooks/`, `PRE_COMMIT.md`, and the RTK proxy.
6. **Gherkin Acceptance Criteria** — at least 4 Scenario blocks covering the primary tool suite behaviours. Each MUST carry a `# anchor:` comment.
7. **Contradiction Log** — from Step 5.
8. **Open Questions / Unresolved** — any question the research could not answer.
9. **Sources** — indexed list with tier (Primary, Reproduction, Aggregator).
10. **Methodology Note** — which methods were applied and what pre-commitments were made.

The spec MUST carry L1 + Research-namespace frontmatter:

```yaml
---
type: research
status: active
slug: token-efficiency-tool-suite
summary: "..."
created: 2026-05-04
updated: YYYY-MM-DD
research_phase: complete
research_executes_prompt: token-efficiency-tool-suite
research_friction_level: FL0 | FL1 | FL2 | FL3
---
```

### Step 9 — Open Questions Routing

For every unresolved question in §8 of the spec, you MUST file a new prompt under `/prompts/<follow-up-slug>/prompt.md` with `prompt_kind: follow-up` and `prompt_spawned_from_research: token-efficiency-tool-suite`. List all created follow-up slugs in `readme.md` under "Open Questions Surfaced".

### Step 10 — Pre-Commit Verification

Before committing, verify all checks from `RESEARCH.md §5`:

- [ ] `prompt.md` snapshot exists and matches the run-start prompt.
- [ ] `research_executes_prompt` resolves to `/prompts/token-efficiency-tool-suite/`.
- [ ] No execution scripts (`.py`, `.sh`) remain in `/workspace/`.
- [ ] No required file is 0 bytes.
- [ ] Every touched folder has an updated `readme.md`.
- [ ] `/workspace/session.log` is populated and chronological.
- [ ] All `state.md` steps are `[x]`.
- [ ] `/output/SPEC.md` has required frontmatter.
- [ ] `friction-log.md` declares the highest FL.
- [ ] Every open question has a follow-up prompt file.

---

## E — Expectations

| Deliverable | Path | Format |
|---|---|---|
| Session log | `research/token-efficiency-tool-suite/workspace/session.log` | Chronological plain text |
| Per-repo notes | `research/token-efficiency-tool-suite/workspace/repo-<slug>.md` | Markdown, one file per high-relevance repo |
| Methodology log | `research/token-efficiency-tool-suite/synthesis/methodology.md` | Markdown |
| Synthesis tracks | `research/token-efficiency-tool-suite/synthesis/tracks.md` | Markdown |
| Synthesis state | `research/token-efficiency-tool-suite/synthesis/state.md` | GitHub-style checklist |
| Post-synthesis log | `research/token-efficiency-tool-suite/synthesis/post-synthesis-log.md` | Markdown |
| Reflection files (×5) | `research/token-efficiency-tool-suite/reflection/M00-*.md` | Markdown |
| Friction log | `research/token-efficiency-tool-suite/reflection/friction-log.md` | Markdown, FL declared at top |
| **Final spec** | `research/token-efficiency-tool-suite/output/SPEC.md` | Markdown with frontmatter, RFC 2119, Gherkin |
| Follow-up prompts | `/prompts/<follow-up-slug>/` | Per `PROMPT.md` |

---

## Constraints

1. **Scope:** You MUST focus on mechanisms that enforce token efficiency *structurally* (tool schemas, budget decorators, mandatory invocation hooks). General prompting tips about "be concise" are out of scope.
2. **Self-containedness:** The output spec MUST be usable by a future agent with no prior context beyond the files named in §I.
3. **No fabrication:** You MUST NOT invent repository names, star counts, or feature claims. If a search returns no results on an axis, log that fact.
4. **RTK Compatibility:** The proposed tool suite MUST NOT conflict with the RTK proxy already active in this environment. It SHOULD extend RTK's approach rather than replace it.
5. **Repository scope:** Only survey public GitHub repositories. Private or paywalled sources are out of scope.
6. **Failure handling:** If GitHub search is rate-limited or unavailable, you MUST log the blockage in `session.log`, skip that search axis, and note it as a gap in the spec's "Open Questions" section. You MUST NOT fabricate search results to fill the gap.
7. **Single RFC 2119 keyword per sentence:** Every normative sentence in the output spec MUST contain exactly one keyword.
8. **Gherkin validity:** Every Scenario in the output spec MUST satisfy G1–G6 from `/maintenance/language-spec.md §3.3`.
