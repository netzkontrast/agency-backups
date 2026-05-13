---
title: "Stress-testing the architectural decisions of the `agency` repository — a Gemini Deep Research brief"
purpose: External, literature-grounded critique of 14 in-progress architectural decisions for an AI-agent governance/orchestration substrate.
audience: Gemini Deep Research (autonomous agent) → results consumed by a small team brainstorming the refactor.
output_format: Per-decision verdict table + executive summary + per-investigation-area memo.
temporal_scope: Sources from 2018-01 through 2026-05, with strong preference for 2022-01 onwards (post-LLM-agent era).
depth: exhaustive
language: en
success_criterion: For each of the 14 decisions, the report delivers (a) at least 2 named external precedents (named tool, paper, repo, talk, or production case study), (b) at least 1 documented failure mode or critique, (c) a verdict in {keep, revise, replace, defer}, (d) a confidence score in [low, medium, high] with the evidence backing it.
provenance:
  generated_by: research-prompt-optimizer (skill ceremony waived — user override; rendered directly from context)
  generated_on: 2026-05-13
  source_repo: netzkontrast/agency
  source_branch: claude/repo-refactoring-plan-CfLY5
  context_doc: .claude/plans/agency-refactor-plan.md (rounds 1–10)
schema_version: 3.3-lite
---

# Stress-testing the architectural decisions of the `agency` repository

> **You are Gemini Deep Research.** You have no access to the originating conversation, the repository, or any prior context beyond this prompt. Treat every numbered decision below as a *hypothesis on trial*; your job is to surface the strongest external evidence FOR and AGAINST it from the published literature, production case studies, and open-source codebases.

## 1. Objective

The `agency` repository is a **governance and orchestration substrate** for long-horizon work performed by autonomous AI agents. It is not an application; it is the meta-layer where Tasks, Prompts, Research workspaces, and reusable Skills are coordinated through filesystem conventions, frontmatter schemas, pre-commit linters, and an ADR ledger.

A small team has been brainstorming a refactor of this substrate. They have made **14 architectural decisions** that need external stress-testing before they harden. Your job is to produce a literature-grounded critique of each decision: prior art, counter-examples, known failure modes, competing patterns, and a recommended verdict.

This is **not** a request for general AI-agent commentary. It is a targeted audit. Every claim you make must be anchored to a **named** source (paper title + venue + year, repository URL + commit, blog post + author + date, conference talk + speaker + venue, or a production case study with a citable artefact). Anonymous folklore, "common knowledge", or unsourced reasoning are explicitly out of scope and should be flagged.

## 2. Domain context — what the substrate is

The repository enforces a **four-way separation of concerns** through filesystem layout, frontmatter, and pre-commit linting:

| Layer | Question it answers | Directory | Contents |
|---|---|---|---|
| **TASK** | *What should be done?* | `/tasks/<NNN>-<slug>/task.md` | Goal + acceptance criteria (Gherkin scenarios) + gate-tooling |
| **PROMPT** | *What is the agent told to do?* | `/prompts/<slug>/prompt.md` | Executable instruction set + session traces (tool-calls, hook telemetry) |
| **RESEARCH** | *What did running it produce?* | `/research/<slug>/{workspace,synthesis,reflection,output}/` | Output + synthesis + reflection-on-task |
| **SKILL** | *What does the agent know how to do?* | `/skills/<slug>/SKILL.md` | Reusable agent capability (description + body + assets) |

Cross-layer linkage flows through **YAML frontmatter only** (`task_uses_prompts`, `task_spawns_research`, `prompt_relates_to_task`, `research_executes_prompt`). Body Markdown links are for humans; the linker reads frontmatter. Every operational file MUST carry L1 Vault Core frontmatter (`type`, `status`, `slug`, `summary`, `created`, `updated`) and an L2 domain namespace (`task_*`, `prompt_*`, `research_*`, `skill_*`).

The repository ships a pre-commit hook that runs 8 linter steps including frontmatter validation, structural completeness, runlog format, ADR validation, RFC 2119 polarity, hook consistency, and index-diff. Acceptance criteria are written as **Gherkin scenarios** (Given / When / Then), and every normative clause uses **RFC 2119 keywords** (MUST, MUST NOT, SHOULD, MAY).

The refactor introduces several new mechanisms (SemVer for non-code artefacts, MCP-dispensed IDs, deferred Gherkin, decomposition prompts as a distinct kind, schema escape hatches, a theatrical rename, and a bootstrap budget). These are what need stress-testing.

## 3. The 14 decisions under audit

For each decision, identify: (a) ≥2 named external precedents (tools, papers, production systems); (b) ≥1 documented failure mode or critique; (c) verdict ∈ {keep, revise, replace, defer}; (d) confidence in {low, medium, high}.

### Decision 1 — Four-layer separation as THE decomposition

The substrate claims `Task | Prompt | Research | Skill` is the right four-way decomposition for agentic governance. Subject to audit: is this novel? does it generalise? what gets pushed into the "skill" bucket that doesn't belong? does the literature show convergence toward this shape or away from it?

### Decision 2 — Tasks/Prompts/Research paired 1:1:1 at the main level

The canonical level has one Task, one Prompt, one Research workspace, paired identically. Subtasks and amendments are sub-numbered children of the main triple, never replacements. Subject to audit: is paired-cardinality coherent or restrictive? does production agentic work tend toward 1:N (one Task → many Prompts) or N:1 (many Tasks → one Prompt)?

### Decision 3 — SemVer applied to non-code artefacts

Tasks, Prompts, Research workspaces are versioned with `MAJOR.MINOR.PATCH`. `MAJOR` = breaking redesign; `MINOR` = new subtask added; `PATCH` = in-place amendment. Subject to audit: is SemVer well-fitted to non-code artefacts? Examples and counter-examples (ontologies, datasets, API contracts, knowledge bases). Known failure modes (semver-ish drift, cherry-picking, "is this minor or major?" perennial disputes). Is calendar-versioning (CalVer) or content-addressed versioning a stronger fit for research artefacts?

### Decision 4 — Goal-only initial Tasks with deferred Gherkin

A new Task may start with ONLY a goal (no acceptance criteria). The first Prompt is a `prompt_kind: decomposition` prompt whose job is to propose subtasks. The Research synthesis step then **writes the parent's Gherkin retroactively** after subtasks are spawned. Subject to audit: is "synthesis writes the parent's criteria retroactively" a known pattern (cf. TDD discovery tests, BDD outside-in, hypothesis-driven design, lean startup's "build-measure-learn")? What are the documented risks of retroactive criteria (criterion-fitting, hindsight bias, gameable PASS)?

### Decision 5 — No-decomposition-needed direct promotion

If decomposition concludes the goal is a single concrete unit (no subtasks needed), the parent Task transitions directly from `task_phase: undecomposed` to `task_phase: ready-to-execute`, skipping the `decomposed` phase. Synthesis writes Gherkin + gate-tooling for the goal itself. Subject to audit: is the four-state phase machine (`undecomposed → decomposed | ready-to-execute → closed`) better or worse than a strict three-state (`undecomposed → decomposed → closed`)? Does the bypass risk producing under-decomposed Tasks?

### Decision 6 — Subtask addressing: full MCP ID + parent-relative SemVer

Every subtask receives both (a) a globally unique MCP-dispensed Task ID (e.g. `Task 087`) AND (b) a parent-relative SemVer coordinate (`task_parent_semver: 042/1.1.0`). Both are queryable. Subject to audit: is dual addressing redundant or load-bearing? What do hierarchical issue-tracker systems (JIRA epics/stories, Linear cycles, GitHub project boards) do? When does the hierarchy strain?

### Decision 7 — Explicit DAG for subtask ordering

Subtasks declare dependencies via `task_depends_on: [<id>, ...]` in frontmatter. Gate-tooling evaluates partial PASS in topological order. Linter rejects cycles. Subject to audit: how do scientific-workflow tools (Snakemake, Nextflow, Airflow, Prefect, Argo Workflows, Dagster) handle dependency declaration? Is frontmatter-as-DAG-encoding a known pattern or anti-pattern? When does the DAG model fail (long-running tasks, conditional branches, dynamic spawning)?

### Decision 8 — Schema escape hatch: reserved `notes:` field

Every schema reserves a top-level `notes:` string field as a **permanent escape valve** — free prose for information that doesn't fit the canonical schema yet. Meta-runs harvest recurring `notes:` patterns to propose schema upgrades. Subject to audit: is `notes:` a known anti-pattern (cf. catch-all `metadata: {}` blobs in YAML, "other" columns in relational schemas, EAV in databases)? When do escape valves harden into shadow schemas? What does the literature say about strict schema + explicit schema-evolution workflow vs. permissive schema?

### Decision 9 — Gate-tooling matrix is mandatory

Every Task carries (a) Gherkin acceptance criteria, (b) JSON Schema for artefact shape, (c) optionally custom validator scripts (only for meta-initialised maintenance Tasks), (d) optionally a reviewer subagent for ungateable outputs (code, prose). Subject to audit: is mandatory dual-gate (Gherkin + JSON Schema) appropriate for AI-agent outputs, or does it generate bureaucratic drag? What's the empirical evidence from spec-driven shops (Stripe, GitLab, Google) when AI agents are the primary authors? When does gate-tooling improve agent quality vs. degrade it?

### Decision 10 — Bootstrap budget: ≤8K tokens before deferring

The agent should read ≤8K tokens at session start before deciding what else to lazy-load. Current real bootstrap is ~50K tokens; target hits 0/10 on this dimension. Subject to audit: how do other agentic systems hold an agent to a context budget at session start? Compare Aider's repo-map, Continue's @-mention model, Cursor's indexed-codebase, RAG-based scaffolding, LangGraph's state machines, Sweep's repo-graph, Codex's project-config, Claude Code's `CLAUDE.md`, Cline's auto-context. What budget figure shows up across these tools?

### Decision 11 — MCP service for globally-unique IDs

A centralised MCP (Model Context Protocol) service issues globally-unique IDs to prevent collision across parallel agent sessions. Subject to audit: when does a centralised dispenser become a bottleneck? Compare distributed ID generation patterns: Snowflake IDs (Twitter), UUID v7 (RFC 9562), KSUID (Segment), ULID, Sonyflake, NanoID, BSON ObjectId. What are the failure modes of centralised dispensers under high agent-parallelism (10 / 100 / 1000 concurrent agents)?

### Decision 12 — Theatrical rename direction (deferred execution)

Rename direction is locked (execution timing still deferred): `prompts/ → enactments/`, `research/ → witness/`, with verbs "Actor enacts" and "Space witnesses". Subject to audit: when does a domain-specific lexicon (ubiquitous-language in DDD, theatrical/dramaturgical in narrative systems) help vs. hurt? Compare DDD case studies, Hibernate's persistence terminology, RxJS's reactive vocabulary, Akka's actor model. Quantifiable evidence on onboarding cost, developer mental model, search/grep-ability?

### Decision 13 — Frontmatter-only audit graph

Cross-layer links flow through YAML frontmatter (`task_uses_prompts: [...]`), not body Markdown. Depth ≤ 1, kebab-case slugs, RFC 2119 + Gherkin in body. Subject to audit: failure modes (orphaned references, link rot, schema drift between body and frontmatter, frontmatter-vs-body inconsistency). How do tools like Roam's bidirectional links, Logseq's properties, Obsidian's frontmatter + Dataview, Foam's graph, Notion's relations, and RDF/ontology projects (Wikidata, DBpedia) handle the same problem? What is the empirical cost of frontmatter-as-source-of-truth?

### Decision 14 — Pre-commit-gated governance (8 linter steps)

Pre-commit hook runs 8 linter steps; commit blocked unless errors are addressed or covered by an open maintenance Task. Subject to audit: empirical evidence on pre-commit governance for AI-agent output. What's the cost/benefit shape from spec-driven shops (Stripe, Google, Shopify) when AI agents are the primary authors? When does pre-commit gating help productivity vs. drive agents into workarounds (`--no-verify`, dummy fixes, gaming the linter)? Compare to test-gated CI vs. lint-gated commit.

## 4. Cross-cutting investigation areas (A–J)

In addition to the per-decision audits, address these ten cross-cutting questions. Each question is a literature-survey lens that touches multiple decisions.

| ID | Lens | What to surface |
|---|---|---|
| **A** | Prior art for four-way Task/Prompt/Research/Skill separation | Have OS theory, knowledge-management systems (Roam, Notion, Obsidian, Logseq), scientific-workflow tools (Snakemake, Nextflow, Airflow, Prefect, Dagster, Argo), or agentic frameworks (CrewAI, LangGraph, AutoGen, MetaGPT, BabyAGI, AutoGPT, OpenAI Swarm) ratified or rejected this exact decomposition? Where does it strain in production reports? |
| **B** | SemVer on non-code artefacts | Named precedents: OWL/RDF ontology versioning (PURL.org practices), DataCite + Zenodo dataset versioning, OpenAPI/AsyncAPI contract versioning, schema.org versioning, Wikidata edit-history, DVC dataset versioning, MLflow model versioning. Known failure modes from these communities. Calendar-versioning (CalVer) and content-addressed (IPFS/CID, Git SHA, Merkle DAG) comparison. |
| **C** | Deferred / retroactive acceptance criteria | TDD discovery tests (Beck, "Test-Driven Development by Example", 2002); BDD outside-in (Adzic, "Specification by Example", 2011); hypothesis-driven design at IDEO; "build-measure-learn" (Ries, "The Lean Startup", 2011); "Done is better than perfect" anti-pattern critique; example-mapping (Wynne). Risks: criterion-fitting bias, gameable PASS, hindsight rationalisation. |
| **D** | Schema escape hatches (`notes:` / `metadata: {}` / "other") | When permissive escape valves become shadow schemas. Compare YAML "extras" fields in Kubernetes CRDs, "metadata" blobs in OpenAPI extensions (`x-*`), EAV anti-pattern in RDBMS (Karwin, "SQL Antipatterns", 2010), "Other" column in survey databases, JSONB columns in PostgreSQL (Celko, et al.). Counter-design: strict schema + explicit "evolve-schema" Task. |
| **E** | Decomposition prompts as first-class artefacts | Plan-and-solve (Wang et al., 2023); ReAct (Yao et al., 2022); Tree-of-Thoughts (Yao et al., 2023); ADaPT (Prasad et al., 2024); LATS (Zhou et al., 2024); Reflexion (Shinn et al., 2023); HuggingGPT / Hugging-Face Agents; AutoGPT/BabyAGI's task-agent architecture. Is the decomposition/execution distinction durable, or are modern agentic frameworks collapsing it back? |
| **F** | Frontmatter-as-graph | Roam Research bidirectional links; Logseq block properties + queries; Obsidian frontmatter + Dataview + Bases; Foam's graph; Notion relations + rollups; Foam vs. Dendron property models; ZIM Wiki; semantic-wiki precedents (Semantic MediaWiki); RDF/Turtle ontologies; Wikidata QID linkage. Documented failure modes: orphaned refs, link rot, schema drift, frontmatter-body inconsistency. |
| **G** | Pre-commit governance for AI-agent output | Spec-driven shops with AI agents in the loop: GitHub's experiments with Copilot Workspace, Stripe's spec discipline + AI usage, Sourcegraph's Cody + spec linting, Google's internal monorepo + Glob/Critique + AI-assisted patches, Shopify's spec-first AI workflows. Quantifiable productivity impact of pre-commit gating on agent output. Workarounds agents develop (the `--no-verify` problem). |
| **H** | Bootstrap-budget mechanisms | Aider's repo-map (Paul Gauthier blog posts); Cursor's indexed-codebase + @-mentions; Continue's auto-context + @-mentions; Codex's project-config; Claude Code's `CLAUDE.md`; Cline's auto-context; Sweep's repo-graph; Devin's planning step; Tabby's IDE context; OpenHands' workspace context; LangGraph's state-machine context; RAG-based bootstrap (Llamaindex's project-aware indexing). Token-budget figures reported across these. |
| **I** | Centralised ID dispenser vs. distributed | Snowflake IDs (Twitter, 2010); UUID v7 (RFC 9562, 2024); KSUID (Segment, 2017); ULID (Buckley, 2016); Sonyflake (Sony, 2017); NanoID; MongoDB ObjectId; AWS request-IDs; CockroachDB's HLC-based IDs. When centralised dispensers bottleneck and how distributed schemes avoid it. Is MCP-as-dispenser an over-engineering choice for the agent-parallelism this substrate is likely to see (1s–10s of concurrent agents, not 1000s)? |
| **J** | Domain-specific lexicon (theatrical metaphor) | DDD ubiquitous-language case studies (Evans, "Domain-Driven Design", 2003; Vernon, "Implementing DDD", 2013); Akka's actor model (Hewitt, 1973; Lightbend case studies); Hibernate's "session/persistence-context"; RxJS's "observable/observer/subscription"; Apache Kafka's "topic/partition/consumer-group". When ubiquitous-language is a clear net win and when it produces cognitive overhead, grep-failure, and onboarding friction. |

## 5. Required deliverable shape

Produce a single Markdown report with the following structure. **Every section is mandatory.**

### 5.1 Executive summary (≤ 600 words)

Five-bullet TL;DR per audited decision class. Highlight the 3 most contested decisions, the 3 strongest precedents, and the 3 most-overlooked risks.

### 5.2 Per-decision verdict table

A single Markdown table with columns:

| # | Decision (short) | ≥2 Named precedents | ≥1 Failure mode | Verdict | Confidence | Strongest evidence |
|---|---|---|---|---|---|---|
| 1 | Four-layer Task/Prompt/Research/Skill | … | … | keep/revise/replace/defer | low/medium/high | citation |
| 2 | 1:1:1 main pairing | … | … | … | … | … |
| … | … | … | … | … | … | … |
| 14 | Pre-commit 8-step gate | … | … | … | … | … |

Each cell that says "…" in this template must be filled with concrete content (no placeholders in the final report).

### 5.3 Per-investigation-area memo (A–J)

For each of the 10 cross-cutting areas (A–J above), write a ~400-word memo covering:
- **Strongest 2–3 precedents** (named + dated + cited).
- **Strongest 2–3 critiques / failure modes** (named + dated + cited).
- **Pattern-of-patterns observation** — what do the precedents converge or diverge on?
- **Recommended verdict** for the related decisions, with confidence.

### 5.4 Composite recommendation table

A single table indicating which decisions reinforce or undermine each other. Example: if Decision 3 (SemVer) is fragile but Decision 7 (DAG) is solid, the SemVer-encoded amendment-folder names (which conflate semantic versioning with topological position) might be the weak seam — flag that.

### 5.5 Recency-stratified source list

A bibliography stratified by year (2024–2026, 2021–2023, 2018–2020, ≤2017). For each source: title, author(s), year, venue/URL, one-sentence relevance.

### 5.6 Open questions for the substrate team

Any questions you encountered that the substrate team has not yet asked themselves. These become the next-round agenda.

## 6. Evaluation rubric (per claim)

When you state a claim about any of the 14 decisions or 10 investigation areas, your claim is judged on:

| Dimension | What it means | What gets you marked down |
|---|---|---|
| **Named anchoring** | Every assertion cites a tool/paper/repo/talk/case study by name | "It is widely believed …" / "Most agentic systems …" |
| **Recency** | Sources are dated; preference for 2022-01 onwards | Citing a 2009 paper as state-of-the-art without acknowledging it's foundational, not current |
| **Evidence vs. opinion** | Claims marked as "evidence-backed" cite measurable results; claims marked as "opinion / community consensus" are flagged separately | Conflating opinion with evidence |
| **Counter-evidence** | Every "keep" or "replace" verdict surfaces at least one strong counter-case | One-sided arguments |
| **Confidence calibration** | "High confidence" requires ≥3 independent named sources converging; "low" is fine with 1 weak source but must be marked low | Overclaiming on thin evidence |
| **Scope discipline** | Claims stay within the substrate's domain (agent governance + multi-agent orchestration + AI-generated content gating); don't drift into "AI safety generally" or "software engineering generally" | Generic AI/SWE platitudes |

## 7. Constraint blocks

**CB0 — Source quality.**
- MUST cite at least one primary source (paper, RFC, original blog post by tool author) per claim.
- SHOULD prefer arXiv / ACM / IEEE / USENIX / venue proceedings over second-order summaries.
- MAY cite high-signal blog posts from tool authors (Paul Gauthier on Aider; Andrej Karpathy on LLM agents; Simon Willison on prompt engineering) as primary.
- MUST NOT cite content-farm articles, generic "Top 10 AI agent frameworks" listicles, or marketing pages.

**CB1 — Scope.**
- IN scope: AI-agent orchestration, agentic frameworks, spec-driven development with AI, scientific-workflow management, knowledge-management systems, distributed ID generation, schema design, governance/lint tooling, ubiquitous-language case studies.
- OUT of scope: AI safety in the abstract, alignment debates, AGI predictions, general LLM benchmarking, training-data ethics.

**CB2 — Recency.**
- 2024–2026 sources preferred where the topic is fast-moving (agentic frameworks, LLM-context budgeting, MCP / tool-calling).
- 2018–2023 sources welcome for foundational topics (SemVer, DDD ubiquitous-language, BDD, TDD).
- ≤2017 sources welcome only as foundational anchors (e.g. Evans 2003 for DDD).

**CB3 — Negative findings welcome.**
- If a decision is solid, say so plainly. If a decision is broken, say so plainly with named sources.
- Equivocation ("on the one hand … on the other hand …") without a final verdict is failure.

**CB4 — Output discipline.**
- One Markdown file; no separate annexes.
- All tables are Markdown tables (not images).
- All citations are inline links or `[ref-N]` footnotes resolved at the bottom.
- Total length 6000–12000 words. Below 6000: insufficient evidence; above 12000: bloat.

## 8. Methods (how to approach the research)

This research is best approached with a **ReAct-style loop**:

1. **Decompose** each of the 14 decisions into 2–3 sub-claims you can search against.
2. **Search** for named precedents and counter-examples — across both the academic literature (Google Scholar, Semantic Scholar, arXiv) and the practitioner literature (GitHub repos, tool documentation, conference talks, engineering blogs).
3. **Triangulate** — never rest on a single source for "high confidence". Three independent sources converging is the bar.
4. **Steelman the opposing view** — for every decision you would "keep", find the strongest case for "replace". For every "replace", find the strongest case for "keep".
5. **Reflect** — after each decision is audited, ask: "What would I have to learn next to flip this verdict?" Record that as an open question.

Cross-pollinate from at least **two** of the following adjacent domains, even if not directly cited in the decisions list:
- **Scientific-workflow management** (Snakemake, Nextflow, Airflow, Prefect, Dagster) — they have decades of dependency-DAG-as-source-of-truth experience.
- **Spec-driven development** with AI in the loop (Stripe, Google's Critique, Shopify) — they have empirical productivity data.
- **Knowledge-management systems** (Roam, Logseq, Obsidian, Notion) — they have user studies on frontmatter-as-graph friction.
- **Ontology engineering** (OWL, RDF, Wikidata, schema.org) — they have versioning experience for non-code artefacts.

## 9. Falsification frame (Popper-style)

For each verdict you produce, complete this sentence: *"This verdict would be falsified by …"* Include at least one falsification clause per verdict. A verdict that cannot be falsified is suspicious and should be downgraded.

## 10. Replication pointer

The user can re-run this research prompt against any future iteration of the substrate's decisions list. Your report SHOULD include a section labelled **"How to re-run this audit"** that enumerates the search queries you used, the source-filtering heuristics you applied, and the decision-points that required human judgement.

## 11. Final verification checklist (self-applied before submission)

Before you return your report, confirm:

- [ ] Every one of the 14 decisions has a verdict + confidence + ≥2 named precedents + ≥1 failure mode.
- [ ] Every one of the 10 investigation areas (A–J) has a memo (~400 words each).
- [ ] The executive summary names the 3 most contested decisions.
- [ ] The composite recommendation table shows which decisions reinforce or undermine each other.
- [ ] The source list is stratified by year.
- [ ] Every claim is named-anchored; no folkloric assertions.
- [ ] Every verdict has a falsification clause.
- [ ] Negative findings are stated plainly.
- [ ] Total length is between 6000 and 12000 words.

## 12. Output

Return a single Markdown document with the sections enumerated in §5, conforming to the rubric in §6, respecting the constraints in §7, applying the methods in §8, the falsification frame in §9, and the verification checklist in §11.

---

*End of Gemini Deep Research brief. Begin research now.*
