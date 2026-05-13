# Synthesis: Gemini Deep Research briefs #1 + #2

> **Frame.** Read fresh against the ORIGINAL refactor goal, not against the 14 locks accumulated in rounds 1–10. The goal as originally stated (Round 1, before any architectural decisions):
>
> 1. **Bootstrap cost** — every session is forced to read AGENTS.md plus several layer specs (~50K tokens) before doing anything. Target: ≤ 8K tokens at session start, with the rest deferred / on-demand.
> 2. **Parallel-work numbering collision** — filesystem-derived `NNN-slug` numbering collides when multiple agents create artefacts on parallel branches. Need global, monotonic, collision-free IDs.
> 3. **Layer-content drift** — the Task / Prompt / Research / Skill separation is correct in spirit, but the *contents* of each layer have drifted (prompts contain task framing, tasks contain prompt body, research workspaces accumulate follow-up prompts). Need re-pinned, enforceable layer contents.
>
> What follows reads both Gemini papers as ONE corpus answering: *what does the published 2023–2026 literature suggest a substrate like this should look like?* — irrespective of what was decided in rounds 1–10.

---

## 1. The convergent thesis (where both briefs agree)

### 1.1 Context is the bottleneck, not capability
Both briefs land on the same Anthropic / Praetorian framing: modern frontier models are not bottlenecked by reasoning, they are bottlenecked by **attention dilution under bloated context** ("context rot", "context-capability paradox"). Up to **80 % of tokens** in a 200K-window agent are wasted on orientation (brief #2 §2; brief #1 Memo H). Therefore the goal of bootstrap reduction is not cost-driven, it is **quality-driven**. Smaller, denser context produces better agents. This validates the original Round-1 ≤ 8K target on independent grounds.

### 1.2 The four-layer separation is the right primitive
Both briefs ratify the **Task / Prompt / Research / Skill** decomposition (brief #1 Decision 1 KEEP-high; brief #2 §3.2). The named anchors are Anthropic Agent Skills (progressive disclosure), Praetorian's deterministic orchestration platform, and LangGraph's state-graph architecture. Across the literature, **monolithic mega-prompts are uniformly being replaced by isolated procedural-memory layers** loaded on demand. Brief #2 specifically calls out that "**Description-Only Skill Bootstrapping**" — show the agent only `{name, description}` at boot, fetch the body on `Skill(...)` invocation — is the production pattern (Anthropic Skills, Block Goose). Anthropic, in other words, is already doing what the substrate needs to do for its own layer specs.

### 1.3 Spec-driven + pre-commit governance is the strongest decision in the design
Both briefs strongly ratify the **mandatory Gherkin + JSON-Schema gate matrix** (brief #1 Decision 9 KEEP-high; brief #2 Lock 9 fully compatible with everything). The named anchors are GitHub Spec Kit, Stripe's spec-driven AI work, Checkmarx Shadow-AI work. The thesis is that JSON-Schema terminates **tool-argument rot** and Gherkin terminates **logic drift**, and that pre-commit gating creates the tight feedback loop that probabilistic models need. The 8-step pre-commit governance model itself is rated KEEP-high (Decision 14).

### 1.4 Explicit DAG for ordering is the gold standard
Apache Airflow and Snakemake are cited as the undisputed precedent for DAG-ordered execution. Brief #1 Decision 7 is KEEP-high; brief #2 finds explicit DAGs fully compatible with every proposed efficiency pattern. **No published agent framework prefers implicit / LLM-hallucinated ordering** over an explicit `depends_on` graph.

### 1.5 The bootstrap-budget gap is closable with named, low-cost patterns
Brief #2's Tier-1 roadmap is the actionable core. **A single week of work** — Context Tiering + Glob-Scoped Rules + Description-Only Skill Bootstrapping — gets the substrate from ~50K → ~30K tokens, with **no architecture changes**. Tier 2 (Aider-style repo-map at pre-commit, lazy ADR synthesis) closes another ~15K. Tier 3 (MCP Resources, Subagent Context Isolation) closes the final gap to ~5K. **Each tier is independently shippable**, and none of the Tier-1 patterns disturb any existing decision class.

---

## 2. The divergent / contested findings (where one brief modulates the other)

### 2.1 SemVer for non-code artefacts — both reject, but in different ways
Brief #1 Decision 3 says **REPLACE** with Calendar Versioning + Content-Addressed (Git SHA / Merkle) hashes, on the basis that even Maven/NPM developers can't agree on what constitutes a "breaking" change (Lynch 2020; Maven empirical study). Brief #2 doesn't audit SemVer directly but flags that any vector / RAG / embedding pattern requires content-addressed IDs (CIDs), not SemVer — i.e. **SemVer actively blocks the most powerful retrieval techniques** (briefly: Cursor, GraphRAG, Self-RAG all want hashes, not semantic versions). The synthesis verdict is strong: **the SemVer choice is the single most consequential lock to revisit**, because it gates the entire dynamic-context branch of the design space.

### 2.2 Centralised MCP ID dispenser — both reject, but the replacement differs
Brief #1 Decision 11 says **REPLACE** with UUIDv7 or ULID — uncoordinated, time-sortable, decentralised; no network coordination. Brief #2 implicitly endorses this by treating "MCP ID" as a namespace scheme rather than a coordinator service. The convergent answer: **drop the central dispenser, adopt UUIDv7 or ULID locally**, and let agents generate IDs without network calls. The literature is unambiguous here — RFC 9562 (UUIDv7) is the standard, Twitter Snowflake is the precedent.

### 2.3 Frontmatter-only audit graph — both flag link-rot, but disagree on the fix
Brief #1 Decision 13 says **REVISE**: keep frontmatter as the declarative surface, but **compile to embedded SQLite** in the pre-commit step to enforce referential integrity. The named anchor is Logseq's actual migration history — Logseq was forced to move from pure markdown to SQLite to maintain integrity at scale. Brief #2 §3.3 offers a softer alternative: **A-MEM Zettelkasten** — atomic markdown notes with semantic linking — which avoids the SQLite step. Synthesis: **a compiled relational index at pre-commit is necessary above ~10K artefacts**; A-MEM is a complementary content pattern, not a replacement for the integrity layer.

### 2.4 Goal-only Task with deferred Gherkin — brief #1 says NO, brief #2 says CAUTIOUSLY
Brief #1 Decision 4 is **REVISE with high confidence**: retroactive criteria introduces **hindsight bias** (named anchor: Shah 2025 on TDD-in-the-AI-age). An agent that writes its own tests after producing output will inevitably write tests that fit its (potentially flawed) output. The fix: **Gherkin must be written and frozen BEFORE execution** — by the decomposition agent, not the execution agent. Brief #2 §3.4 echoes this softly: spec-to-plan cascade (Copilot Workspace) requires the plan FIRST. The synthesis verdict: **the "decomposition-synthesis writes the parent Gherkin afterwards" idea is the second most consequential lock to revisit**.

### 2.5 Schema escape hatch `notes:` — both reject
Brief #1 Decision 8 is **REVISE-high**: catch-all string fields are the EAV anti-pattern reborn; agents will dump malformed JSON into `notes:` to bypass linters; this is the proximate cause of "tool argument rot" in production (Lanham 2025). Brief #2 treats `notes:` as a substrate-specific lock (L8) that *can* be accommodated but flags it as a hedge against rigid schemas, not a feature. Synthesis: **remove `notes:` entirely; replace with an explicit "propose a schema upgrade" Task subtype** so that schema evolution is a first-class operation.

### 2.6 Theatrical rename — brief #1 strongly rejects, brief #2 dismisses as cosmetic
Brief #1 Decision 12 is **REPLACE-high**: the theatrical metaphor violates DDD's "ubiquitous language" principle (Evans), breaks repository grep-ability, and creates a steep onboarding curve. Brief #2 marks L12 as "primarily cosmetic; rarely impacts context fetching." Synthesis: **drop the rename**. It serves no engineering purpose, and the brainstorm's energy is better spent elsewhere.

### 2.7 1:1:1 main-level pairing of Task / Prompt / Research — brief #1 strongly rejects
This is the strongest dissent of brief #1 (Decision 2, REVISE-medium). The literature on real orchestration (CrewAI, LangGraph, MetaGPT) shows agents naturally fan out: one Task → many Prompts (planner, researcher, synthesiser, validator) → fragmented Research artefacts. Forcing 1:1:1 produces "prompt spaghetti" — distinct personas merged into one bloated string to fit the filesystem. Synthesis: **drop the strict 1:1:1 lock**. Adopt 1:N (one Task → many Prompts) at the main level; constrain to 1:1:1 only at the *amendment* level if needed.

---

## 3. The big-picture finding (synthesis-level)

The two briefs, read together, produce a coherent thesis that the substrate's current trajectory partially fights:

**The 2023–2026 literature says a long-horizon governance substrate should be a *manifest-routed, description-only, hash-addressed, plan-first* environment with explicit DAGs and a relational integrity layer.**

Concretely, the literature-prescribed substrate is:

1. **A tiny root manifest** (`agency.yaml`, ~1K tokens) that the agent reads first. Lists available layers and how to fetch them. Linux `initramfs` pattern.
2. **A description-only skill / layer index** (~500 tokens). Each layer spec presented as `{name, description, fetch-tool}`. Body loaded on demand.
3. **A repo-map** (~2K tokens), generated by tree-sitter at pre-commit time, listing the most-referenced symbols across `tasks/`, `prompts/`, `research/`, `skills/`. Aider's PageRank pattern.
4. **Glob-scoped rules** that inject only when the agent touches matching files. Anthropic's `.claude/rules/*.md` pattern.
5. **Hash-addressed artefacts** (UUIDv7 or ULID) generated locally by agents, no network round-trip.
6. **A relational integrity layer** (embedded SQLite, compiled from frontmatter at pre-commit) that maintains the DAG of `task_depends_on`, `task_uses_prompts`, etc.
7. **Pre-commit gates** for JSON-Schema, Gherkin, and DAG-acyclicity. The 8-step gate is correctly oriented.
8. **Plan-first decomposition** — Gherkin and DAG are written by the planner agent BEFORE the executor agent runs. No retroactive criteria.
9. **Subagent context isolation** — orchestrator never reads raw code; spawns subagents that consume 60K+ tokens and return a 1K summary.
10. **MCP resources for static governance docs** (ADR synthesis, full layer specs). Agent has the URIs at boot, fetches on demand.

This is **strictly mechanically compatible** with the original four-layer model. The four-way separation Task / Prompt / Research / Skill is preserved. What changes is **how each layer is materialised**: less monolithic markdown, more tooled fetches; less SemVer + central dispenser, more hashes + local generation; less retroactive synthesis, more plan-first DAG.

---

## 4. The five strongest external precedents (named, verifiable)

1. **Anthropic Agent Skills (2025)** — description-only at boot, body loaded on `Skill()` invocation. Already the model the user's substrate is plugged into via `.claude/skills/`. Brief #2 §3.2.
2. **Aider Repo-Map (Paul Gauthier, 2024)** — tree-sitter AST + PageRank, token-budgeted (default 1K–8K). The canonical bootstrap-budget mechanism. Brief #1 Memo H + brief #2 §3.1.
3. **GitHub Spec Kit (Microsoft, 2025–2026)** — spec-driven development with pre-commit governance. Validates the entire gate-tooling matrix. Brief #1 Memos C + G.
4. **Apache Airflow / Snakemake DAGs** — explicit dependency declaration as workflow orchestration standard. Validates Decision 7. Brief #1 Memo F.
5. **UUIDv7 (RFC 9562, 2024)** — decentralised time-sortable IDs replacing centralised dispensers. Validates the ID-replacement verdict. Brief #1 Memo I.

## 5. The five sharpest warnings (named, verifiable failure modes)

1. **Silent link rot in flat-file frontmatter graphs** — documented in Obsidian / Logseq forums; Logseq itself migrated to SQLite. The substrate will hit this above ~10K artefacts. Brief #1 Memo F.
2. **Hindsight bias in retroactive Gherkin** — Shah 2025; if the agent writes its own tests after producing output, the gate is rigged. Brief #1 Memo C.
3. **Shadow schemas in `notes:` escape hatches** — Lanham 2025; the proximate cause of tool-argument rot. The agent will dump malformed JSON into `notes:` to bypass linters. Brief #1 Memo D.
4. **Theatrical metaphor breaks grep-ability** — Wilshire 1977 + Evans DDD; substrate-grep will silently miss any agent that references the literal terms. Brief #1 Memo J.
5. **Central ID dispensers as single point of failure** — Praetorian / Authgear; network round-trip on every artefact creation is both slow and brittle. Brief #1 Memo I.

## 6. Synthesis-level open questions (independent of prior rounds)

These are the questions the literature DOES NOT settle, and that the substrate team must decide:

1. **Where does dynamic context-fetching cross the line into runtime opacity?** The Tier-1 patterns (Context Tiering, Glob-Scoped Rules) are still git-verifiable. The Tier-3 patterns (MCP Resources, Subagent Isolation) shift state into runtime. **How much runtime state is acceptable** before pre-commit governance loses its grip? Brief #2 §8 calls this out explicitly as the meta-question.

2. **Markdown + frontmatter + pre-commit IS the bottleneck, or just under-optimised?** Brief #2 frames this as the literature's bias against static-file governance. Migrating to a graph database (Neo4j) or MCP-validation-as-tool would close the bootstrap gap definitively but **change the substrate's identity**. The team's call.

3. **Plan-first or plan-as-needed?** Brief #1 wants Gherkin frozen before execution. Brief #2's ADaPT pattern wants the agent to try executing directly and only decompose on failure. These are different *philosophical* answers to the same operational pressure (token budget). The substrate must pick.

4. **Local UUIDv7 IDs vs. parent-relative addresses** — once IDs are decentralised, what becomes of the parent-child relationship? Brief #1 Decision 6 says drop the dual-address scheme; use flat IDs + relational edges. But the substrate has been treating SemVer-on-amendment as a feature. **Pick one address space.**

5. **What does the integrity layer look like?** Embedded SQLite compiled at pre-commit (brief #1 preferred) vs. A-MEM Zettelkasten markdown notes (brief #2 alternative) vs. nothing yet (current state). The bigger question: at what artefact count does this become mandatory?

---

## 7. What the synthesis does NOT settle

- **Migration of existing artefacts** (96 tasks / 77 prompts / 30 research) — not addressed by either brief, since both briefs are forward-looking.
- **Repo-name lexicon** (theatrical rename) — both briefs say drop it; that's settled. But what replaces it? The literal current names (`tasks/`, `prompts/`, `research/`, `skills/`) are fine per DDD.
- **Initial seed `task_kind: goal` parents** — neither brief weighs in.
- **The role of `meta/`** — neither brief addresses repository-internal maintenance workflows.
- **Decomposition-prompts as a SKILL** — neither brief addresses the specific question of whether `decompose-goal` should be a first-class skill artefact.

These remain in scope for the next iteration of the plan; they are not blocked by the briefs' findings.

---

*End of synthesis. Prepared 2026-05-13. Lives at `.claude/plans/synthesis-gemini-1-2.md`; companion: [`plan-rethink-overview.md`](./plan-rethink-overview.md).*
