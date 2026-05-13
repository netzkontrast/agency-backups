---
title: "Bootstrap-budget reduction & context-engineering patterns for the `agency` substrate — a Gemini Deep Research brief (companion #2)"
purpose: Surface implementable token-efficiency and context-engineering patterns that COMPOSE with the architectural decisions locked across rounds 1–10. Address the bootstrap-budget drift (~50K → ≤8K target) identified by /sc:reflect.
audience: Gemini Deep Research (autonomous agent) → results consumed by a small team brainstorming the refactor.
output_format: Pattern catalogue (≥20 named techniques) + decision matrix (pattern × locked-decision compatibility) + implementation roadmap (cheapest-first).
temporal_scope: 2023-06 through 2026-05. The state of the art moves fast here; older sources only when foundational.
depth: exhaustive
language: en
success_criterion: The report delivers (a) ≥20 named, externally-cited context-engineering / token-efficiency patterns; (b) a compatibility matrix showing which patterns compose cleanly with the 30 already-locked decisions vs. which would require revising a lock; (c) a cheapest-first implementation roadmap with concrete token-budget estimates; (d) explicit identification of patterns NOT to adopt (negative findings).
provenance:
  companion_to: gemini-deep-research-agency-refactor.md
  generated_by: assistant (sidequest after /sc:reflect drift analysis)
  generated_on: 2026-05-13
  source_repo: netzkontrast/agency
  source_branch: claude/repo-refactoring-plan-CfLY5
  context_doc: .claude/plans/agency-refactor-plan.md (rounds 1–10) + .claude/plans/round-10-additions.md
schema_version: 3.3-lite
---

# Bootstrap-budget reduction & context-engineering patterns for the `agency` substrate

> **You are Gemini Deep Research.** This is companion brief #2. The first brief (filename above) audits the substrate's 14 architectural decisions for *correctness*. This brief asks a different question: **given those decisions stand**, what implementable token-efficiency and context-engineering patterns from the 2023–2026 literature can close the bootstrap-budget gap?

## 1. The presenting problem

The `agency` substrate is a governance/orchestration layer for long-horizon AI agents. The architecture has been iteratively designed across 10 rounds of brainstorming (see provenance). A `/sc:reflect` pass at end of Round 10 surfaced a **drift**:

- **Original constraint (Round 1):** the agent must read ≤8K tokens at session start before deciding what else to lazy-load. Current real bootstrap is ~50K tokens (AGENTS.md + CLAUDE.md + layer specs + ADR synthesis block + governance check output + frontmatter schemas + skill index + …).
- **What rounds 2–10 produced:** rich architectural machinery (four-layer separation, SemVer for artefacts, MCP ID dispenser, deferred-Gherkin decomposition workflow, DAG-ordered subtasks, mandatory gate-tooling, theatrical rename, frontmatter-only audit graph, 8-step pre-commit gate).
- **What rounds 2–10 did NOT produce:** any mechanism that mechanically reduces the bootstrap budget.

The substrate is now feature-rich but the original constraint is unmet. **This brief asks Gemini to close that gap using the published literature on context engineering and token-efficient agent design.**

Critically, the architecture is mostly locked. The brief is about *forward-compatible* patterns — what plugs in without revising the locks. Patterns that would require revising a lock should be flagged separately with explicit identification of which lock(s) they'd disturb.

## 2. Domain context — the locked architecture (compatibility constraints)

Patterns proposed by Gemini MUST be evaluated against the following constraints (these are the locks; revising any of them is "expensive"):

| Lock # | Constraint | Why it constrains the search |
|---|---|---|
| L1 | Four-layer separation: Task/Prompt/Research/Skill | Patterns must respect this taxonomy — a "pattern" that collapses Task into Prompt would require revising L1 |
| L2 | 1:1:1 main-level pairing | Patterns that fan out at the main level need revision |
| L3 | SemVer on non-code artefacts (`1.0.0` / `1.0.1` / `1.1.0` / `2.0.0`) | Patterns that use content-addressed versioning (CIDs, hashes) disturb L3 |
| L4 | Goal-only Task → deferred Gherkin (synthesis writes it) | Patterns that require criteria upfront disturb L4 |
| L5 | No-decomp direct promotion to ready-to-execute | Patterns that mandate decomposition disturb L5 |
| L6 | Subtask = MCP ID + parent-relative SemVer | Patterns using URN/URI schemes disturb L6 |
| L7 | Explicit DAG via `task_depends_on` | Patterns using implicit ordering disturb L7 |
| L8 | `notes:` string field as escape valve | Patterns mandating strict typed schemas disturb L8 |
| L9 | Mandatory Gherkin + JSON Schema gate-tooling | Patterns that gate on different artefacts disturb L9 |
| L10 | Bootstrap target ≤8K tokens | **This is the target, not a constraint** — patterns are scored against it |
| L11 | MCP service for globally-unique IDs | Patterns using local-monotonic counters disturb L11 |
| L12 | Theatrical rename direction (deferred execution) | Cosmetic; rarely disturbed |
| L13 | Frontmatter-only audit graph; depth ≤ 1, kebab-case | Patterns using body-link graphs or deep YAML disturb L13 |
| L14 | 8-step pre-commit gate (frontmatter, structure, runlog, ADR, polarity, index-diff, hooks, dramatica) | Patterns that defer validation to runtime disturb L14 |

## 3. What to investigate

### 3.1 Patterns from production agentic systems

Survey the bootstrap and context-management strategies of these systems. For each, name the technique, cite the source (blog post / docs / paper / commit), and report the typical bootstrap-token figure if disclosed.

| System | What to extract |
|---|---|
| **Aider** (Paul Gauthier) | `repo-map` algorithm; tree-sitter symbol ranking; `--map-tokens` flag; how the map degrades when token budget shrinks |
| **Cursor** | Codebase indexing pipeline; semantic search at @-mention; symbol resolution |
| **Continue** | `@-mention` model; context providers (file, code, docs, problems); the auto-context heuristic |
| **Cline** (formerly Claude-Dev) | Auto-context selection; environment-details injection; the workspace-tracker pattern |
| **Sweep** | Repository graph; entity extraction; chunk-level retrieval |
| **Devin** | Planning step; workspace snapshotting; long-horizon memory |
| **OpenHands** (formerly OpenDevin) | Event-stream + condenser; the agent skill abstraction; AgentDelegate pattern |
| **Roo Code / Cline forks** | "Modes" as context-scoping; orchestrator mode delegation |
| **Goose** (Block, formerly Square) | Tool descriptions as the bootstrap surface; profile system; recipe pattern |
| **Aider's `/architect` mode** | Plan-then-edit split; how it reduces edit-time tokens |
| **Codex** (OpenAI) | `codex.md` / `AGENTS.md` discovery; nested project files; auto-loaded context |
| **Claude Code** | `CLAUDE.md` discovery + nesting; Skill tool semantics; hook events; the `Skill` invocation model |
| **GitHub Copilot Workspace** | Task → spec → plan → implementation cascade; spec-as-bootstrap |
| **LangGraph** | State-machine-as-context-budget; checkpointing; the `StateGraph` pattern |
| **CrewAI** | Crew-level shared memory; task delegation context |
| **AutoGen v0.4** | Topic-based pub/sub; context-isolation between agents |
| **Letta / MemGPT** | Memory hierarchy (core, conversational, archival); the recall/compression cycle |
| **A-MEM** (Xu et al., 2024) | Agentic memory with note-taking + linking |
| **MIRIX** (Wang et al., 2025) | Memory-centric agent architecture |

For each: which technique would compose cleanly with L1–L14? Which would disturb a lock?

### 3.2 Patterns from the published literature

Survey the 2023–2026 papers on context engineering. Include but don't limit to:

| Paper / technique | What to extract |
|---|---|
| **Anthropic "Context Engineering"** (Anthropic blog series, 2024–2025) | The framing of "context as scarce resource"; the layered context model |
| **Anthropic "Skill Tool"** (claude.com docs + announcement 2025) | The Skill abstraction; SHA-pinned skill corpora; description-only at boot |
| **Anthropic "Computer Use" / "Tool Use"** | Tool description economics; tool-result compression |
| **Anthropic "Sub-agents"** (2025) | Subagent context isolation; result-only return pattern |
| **OpenAI MCP** (2024 spec) | Resource vs. Prompt vs. Tool; lazy resource fetch |
| **MetaGPT** (Hong et al., 2023) | SOP-as-context; role-specific context windows |
| **CAMEL** (Li et al., 2023) | Role-playing as context-shaping |
| **Reflexion** (Shinn et al., 2023) | Reflection as compressed long-horizon memory |
| **MemGPT / Letta** (Packer et al., 2023) | OS-style virtual context |
| **A-MEM** (Xu et al., 2024) | Agentic memory with structured notes |
| **Generative Agents** (Park et al., 2023) | Memory stream + reflection + retrieval |
| **HippoRAG** (Gutiérrez et al., 2024) | PageRank-style retrieval over knowledge graph |
| **GraphRAG** (Microsoft Research, 2024) | Community summaries + hierarchical retrieval |
| **LightRAG** (Guo et al., 2024) | Dual-level retrieval with low-overhead graphs |
| **Self-RAG** (Asai et al., 2024) | Retrieve-on-demand with reflection tokens |
| **Plan-and-Solve** (Wang et al., 2023) | Plan-first decomposition |
| **Tree-of-Thoughts** (Yao et al., 2023) | Search-tree over reasoning steps |
| **ADaPT** (Prasad et al., 2024) | Decompose-as-needed (lazy decomposition) |
| **LATS** (Zhou et al., 2024) | Language Agent Tree Search |
| **MIPRO / DSPy** (Khattab et al., 2024) | Programmatic prompt optimization |
| **GEPA / Reflexion-style optimization** | Compositional prompt evolution |
| **Long-context vs. RAG** debate (Anthropic, Google "Long context vs. RAG" 2024; Databricks paper 2024) | When long context wins; when RAG wins; the hybrid |
| **Context caching** (Anthropic, OpenAI, Google 2024) | Prompt-caching for static system prompts; cost / latency profile |
| **Skill / Tool-of-thought** literature (2024–2025) | Treating tool descriptions as the bootstrap surface |

For each: extract the *mechanism*, not just the headline. Report whether the mechanism is implementable in a Markdown-+-frontmatter substrate with pre-commit linting (i.e., the `agency` shape), or whether it requires a runtime.

### 3.3 Patterns from adjacent fields

Cross-pollinate. The bootstrap-budget problem is not unique to agents:

- **Operating-system kernels** — minimal init, lazy module load, `initramfs` pattern.
- **Smalltalk / Lisp images** — image-based persistence; "the world is the bootstrap".
- **Emacs / Vim startup-tuning** — `vim-plug` lazy-load, `package-quickstart`, `early-init.el`.
- **Browser DOMContentLoaded vs. load** — staged readiness.
- **Compiler driver tables** — lookup-table-as-bootstrap.
- **Library catalogues / Dewey Decimal** — hierarchical retrieval-on-demand.
- **Hypercard stacks** — the manifest-of-cards pattern.
- **Hypermedia (HATEOAS)** — discoverability over upfront-knowledge.
- **GraphQL schema introspection** — schema-as-discovery-surface.

Surface ≥3 cross-pollinated techniques from this list that map onto the agent-bootstrap problem.

### 3.4 The specific gap: how to reduce ~50K → ≤8K bootstrap

The current `agency` bootstrap (~50K tokens) consists of:
- `AGENTS.md` (~25K) — the canonical agent specification
- `CLAUDE.md` (~15K) — the project-level entry point
- Layer specs (TASK.md, PROMPT.md, RESEARCH.md, SKILLS.md, FOLDERS.md, PRE_COMMIT.md, FRUSTRATED.md, MAINTENANCE.md) — ~50K combined; only some are read every session
- ADR synthesis block (auto-generated, ~5K)
- Governance check output, frontmatter schemas, skill index — variable

The target is ≤8K. Mechanically, this requires: (a) deferring most reads, (b) summarising or indexing the deferred content, (c) on-demand retrieval. Investigate the **engineering patterns** that make this work in practice, not just in theory:

1. **Manifest-driven loading.** What does a good manifest look like? (Compare: `package.json` engines, `Cargo.toml`, `pyproject.toml`, `npm shrinkwrap`, `composer.lock`, `flake.lock`, Bazel `WORKSPACE`.)
2. **Index-as-bootstrap.** Aider's repo-map is the most-cited example. What's the algorithm? What's the token cost of the index itself relative to the substrate it indexes?
3. **Hint-based context.** Claude Code's `CLAUDE.md` pattern; Cline's `.clinerules`; Cursor's `.cursor/rules`. What's the empirical bootstrap savings? How are these files kept fresh?
4. **Sparse activation / mixture-of-experts at session level.** Loading only the layer specs relevant to the kind of work the session is about to do. How is "kind of work" detected upfront?
5. **Spec-as-tool-description.** Reframing the layer specs as *tool descriptions* the agent retrieves on demand via a `getSpec(layer)` tool. Compare Claude's tool descriptions, MCP's `Resource` spec.
6. **Prompt caching for static bootstrap.** Anthropic / OpenAI / Google all support prompt caching. What's the cost / cache-hit profile for a stable system prompt?
7. **Lazy ADR synthesis.** The ADR `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` block (~5K) is currently in AGENTS.md and auto-rebuilt. What if it lived in a separate file fetched only when "ADR relevant" intent is detected?
8. **Frontmatter as the only mandatory read.** What if the bootstrap is *only* the YAML frontmatter of root files, summarised into a single index file?
9. **Compression via summary specs.** Each layer spec produces a 100-line `*-quick.md` digest; full spec lazy-loaded only when needed. Risk: drift between digest and full spec.
10. **Skill descriptions as the bootstrap surface.** The Skill tool already injects 50+ skill descriptions at session start. If the agent's primary capability is skill-invocation, are the layer specs partially redundant?
11. **JIT spec loading via a `consultSpec(layer)` tool.** The agent has access to a tool that returns the relevant section of a spec on demand.
12. **Embedding-based retrieval at session start.** A `.agent_cache/` directory of pre-computed embeddings; the agent retrieves only the chunks relevant to its first message. Risk: cache invalidation, retrieval accuracy.
13. **Multi-pass bootstrap.** Pass 1 (1K tokens): read a manifest. Pass 2 (≤7K tokens): read the layers the manifest pointed at.
14. **Context-window budget enforcement at the harness level.** Pre-commit hook fails if `git diff` indicates `AGENTS.md` grew past a token threshold. What's a sensible threshold?

For each of these 14 micro-patterns, Gemini should: (a) name ≥2 production systems that implement it, (b) cite the published rationale, (c) estimate the realistic token-savings if applied to `agency`, (d) assess compatibility with L1–L14.

## 4. Required deliverable shape

### 4.1 Executive summary (≤ 600 words)

The five most impactful patterns for closing the 50K→8K gap, ranked by (token-savings × forward-compatibility-with-locks) / implementation-cost. Each pattern named, sourced, and quantified.

### 4.2 Pattern catalogue (≥20 named techniques)

A Markdown table:

| # | Pattern | Origin (system / paper / RFC) | Mechanism (1 sentence) | Realistic token savings for `agency` | Compatibility with L1–L14 | Implementation cost | Recommended? |
|---|---|---|---|---|---|---|---|
| 1 | Aider repo-map | github.com/Aider-AI/aider + paulgauthier.com blog (2024) | tree-sitter symbol ranking distils repo into a token-budgeted map | ~30K → ~3K | Compatible with L1, L13; needs `task.md` to be tree-sitter-indexable | Medium (2–4 wks) | ✓ |
| 2 | Anthropic Skill tool | claude.com docs (2025) | Skills are description-only at boot; body loaded on `Skill(...)` invocation | … | L1 (skill layer maps cleanly); L14 (precommit can validate manifest) | Low (1 wk) | ✓ |
| … | … | … | … | … | … | … | … |
| 20+ | … | … | … | … | … | … | … |

### 4.3 Compatibility matrix (pattern × lock)

A heat-map-style table. Rows = the ≥20 patterns. Columns = L1–L14. Cell values: `✓ compatible` | `△ requires minor adjustment to lock` | `✗ requires revising lock`. For every `△` or `✗`, a footnote explains.

### 4.4 Cheapest-first implementation roadmap

Three tiers:
- **Tier 1 — wins within 1 week**, no architecture changes, savings ≥10K tokens.
- **Tier 2 — wins within 1 month**, minor architecture touch-ups, savings ≥20K tokens.
- **Tier 3 — wins within 3 months**, may require revising 1–2 locks, savings ≥35K tokens (closes the gap).

For each tier: concrete steps, files to touch, expected token-budget at completion.

### 4.5 Negative findings

Patterns that look attractive but should NOT be adopted. Common candidates: full RAG-based bootstrap (latency + accuracy issues for a small substrate); embedding cache (invalidation pain); deep markdown-link graph traversal (slow); fancy MoE-style skill routing (over-engineering for ≤100 skills).

### 4.6 Open questions for the substrate team

Things Gemini noticed that the team has not yet asked. Especially: where does the architecture assume something that the literature contradicts?

### 4.7 Recency-stratified bibliography

Sources stratified by year, with one-sentence relevance per entry.

## 5. Evaluation rubric (per claim)

Same as companion brief #1:

| Dimension | What it means |
|---|---|
| Named anchoring | Every assertion cites a tool/paper/repo/talk/case study by name |
| Recency | Strong preference for 2023-06 onwards |
| Evidence vs. opinion | Token-savings figures are evidence-backed (cite the source); architectural recommendations may be opinion (flag as such) |
| Counter-evidence | Every "✓ Recommended" surfaces a counter-case from a practitioner who didn't adopt it |
| Confidence calibration | High confidence requires ≥3 independent converging sources |
| Scope discipline | Stay within "engineering patterns implementable in a Markdown-+-frontmatter governance substrate" |

## 6. Constraint blocks

**CB0 — Source quality.**
- MUST cite at least one primary source per pattern.
- SHOULD prefer engineering blog posts by tool authors (Paul Gauthier, Anthropic engineering, OpenAI engineering, Microsoft GraphRAG team, the Letta team) as primary for production systems.
- MAY cite arXiv preprints for academic patterns.
- MUST NOT cite content farms, "Top 10 AI tools" listicles, marketing material.

**CB1 — Scope.**
- IN scope: agent bootstrap budgets, context-window engineering, lazy-loading, manifest design, skill/tool description economics, prompt caching, RAG architectures, memory hierarchies, sparse activation, embedding-based retrieval at session start.
- OUT of scope: model training, alignment debates, AGI predictions, model selection (Opus vs. Sonnet), parameter tuning unrelated to context.

**CB2 — Quantification.**
- Where a source reports token figures, cite them.
- Where the substrate team will need to make a reasonable estimate, mark the figure as `(est)` and show the math.
- Avoid percentages without absolute numbers ("50% reduction" is useless without the baseline).

**CB3 — Negative findings welcome.**
- If a popular pattern (e.g. RAG-everywhere) doesn't fit `agency`, say so plainly with named sources.

**CB4 — Output discipline.**
- One Markdown file; no annexes.
- All tables in Markdown.
- All citations inline or as `[ref-N]` footnotes.
- Length 6000–12000 words.

## 7. Methods (how to approach this research)

Same ReAct-style loop as companion brief #1, with two adjustments specific to this brief:

1. **Quantify whenever possible.** This brief produces an implementation roadmap; un-quantified recommendations are not actionable. Token figures, latency figures, cache-hit rates — cite them.
2. **Steel-man "do nothing".** For each pattern, ask: "What's the strongest argument for NOT adopting this and keeping the 50K bootstrap?" If the argument is strong, surface it.

Cross-pollinate from at least **two** of the following:
- **Operating-system minimal-init design** (Linux initramfs, NixOS module system).
- **Build-system manifests** (Bazel, Nix, Cargo, pnpm).
- **Library cataloguing** (Dewey, MARC, FRBR).
- **Hypermedia / HATEOAS** as discoverability.

## 8. Falsification frame

For each "✓ Recommended" verdict, complete: *"This recommendation would be falsified if …"*. A recommendation that cannot be falsified should be downgraded.

## 9. Replication pointer

A section labelled **"How to re-run this audit"** enumerating: search queries used, source-filtering heuristics, judgement-required decision-points. The substrate team will re-run this brief against the next iteration of locks.

## 10. Self-verification checklist

Before returning the report, confirm:

- [ ] ≥20 named patterns catalogued, each with origin + mechanism + token estimate + compatibility + cost + recommendation.
- [ ] Compatibility matrix is filled (no empty cells); every `△`/`✗` is footnoted.
- [ ] Cheapest-first roadmap names concrete files to touch and target token budgets per tier.
- [ ] Negative findings section names ≥3 patterns NOT to adopt.
- [ ] All token figures are either cited or marked `(est)`.
- [ ] Each "✓ Recommended" has a falsification clause.
- [ ] Bibliography is stratified by year.
- [ ] Length 6000–12000 words.

## 11. Final word — the meta-question

Beyond pattern enumeration, the brief invites one synthesis: **does the published literature suggest the substrate's choice to express governance through Markdown + frontmatter + pre-commit linting is itself the bottleneck**, or is it merely under-optimised? If the literature points toward "express governance as a runtime service" (i.e., the agent calls `getSpec()`, `validateTask()`, `dispenseId()` tools rather than reading files), that's a reframing the team needs to hear.

---

*End of Gemini Deep Research brief, companion #2. Begin research now.*
