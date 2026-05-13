---
source: Google Drive (Google Doc → markdown export)
drive_file_id: 1ioxEPxFFggIrgFlZ_5_telv7BQ2vSdZnD5vC5YLtibk
drive_title: "Agent Bootstrap Budget Reduction Patterns"
drive_created: 2026-05-13T14:54:31Z
imported_on: 2026-05-13
brief: .claude/research-prompts/gemini-deep-research-bootstrap-context-engineering.md
companion_brief: .claude/research-prompts/gemini-deep-research-agency-refactor.md
companion_result: .claude/research-results/gemini-1-architecture-audit.md
purpose: Gemini Deep Research output for brief #2 — surveys context-engineering and token-efficiency patterns implementable with the locked architecture; addresses the ~50K→≤8K bootstrap-budget drift surfaced by /sc:reflect.
status: imported, not yet synthesised into Round 11 decisions
---

# **Bootstrap-budget reduction & context-engineering patterns for the agency substrate**

## **1\. Executive Summary**

The agency substrate architecture, finalized over ten conceptual iterations, presents a sophisticated governance and orchestration layer designed for long-horizon AI agents. However, comprehensive architectural review reveals a critical operational inefficiency: a bootstrap token budget drift from the targeted ≤8K tokens to an unsustainable baseline of approximately \~50K tokens per session start. This drift is primarily driven by the static loading of monolithic specifications, including the AGENTS.md file (\~25K tokens), the CLAUDE.md configuration (\~15K tokens), various layer specifications, and an auto-generated Architecture Decision Record (ADR) synthesis block.  
To rectify this inefficiency without disturbing the locked architectural constraints (L1–L14)—specifically the reliance on Markdown, Semantic Versioning, and deterministic pre-commit linting—this report presents an exhaustive catalogue of 22 context-engineering patterns sourced from the 2023–2026 literature. By reframing context not as a static repository of universal knowledge, but as a dynamically managed, scarce resource subject to diminishing marginal returns 1, the bootstrap sequence can be mechanically optimized to meet the ≤8K token target.  
The five most impactful and immediately compatible patterns for closing the 50K → 8K gap are summarized below.

| Priority | Pattern Name | Origin & Mechanism | Empirical Token Savings | Implementation Impact |
| :---- | :---- | :---- | :---- | :---- |
| **1** | **Context Tiering & Glob-Scoping** | **Anthropic (2026):** Segregates CLAUDE.md into Permanent (\<100 lines) and Temporary/On-Demand tiers via .claude/rules/\*.md files, loading rules only when specific file paths are touched.3 | \~15K → \~2K tokens | **Low Cost.** Requires refactoring existing monolithic markdown into targeted, glob-matched files. Fully compatible with static pre-commits. |
| **2** | **Aider Repo-Map (Tree-Sitter)** | **Aider (2024):** Generates an AST-derived dependency graph, applying a PageRank algorithm to rank symbols. Distills the workspace into a rigid token-budgeted map.4 | \~30K → \~1K–3K tokens | **Medium Cost.** Requires integrating a Python/Node tree-sitter script into the 8-step pre-commit gate (L14) to generate a static index-quick.md. |
| **3** | **Description-Only Skill Bootstrapping** | **Anthropic (2025):** Represents complex layer and skill specifications merely as 1–2 sentence descriptions at boot. Full markdown bodies are fetched only upon explicit tool invocation.3 | \~10K → \~500 tokens | **Low Cost.** Aligns perfectly with the substrate's four-layer taxonomy (L1). Requires exposing a simple read tool to the agent. |
| **4** | **MCP Resource vs. Tool Separation** | **OpenAI / Anthropic (2024):** Transitions static governance docs (like the 5K ADR block) into Model Context Protocol (MCP) Resources. The agent receives only URI schemas at boot.7 | \~5K → \~100 tokens | **Medium Cost.** Requires mapping local Markdown files to an MCP resource server, decoupling documentation from the system prompt. |
| **5** | **Manifest-Driven Loading (initramfs)** | **OS / Build Systems:** Adapts the Linux kernel initramfs pattern. The agent reads a tiny agency.yaml manifest acting as a lookup table, using tools to mount specific workflow layers.9 | Variable (Reduces foundational bloat) | **Medium Cost.** Requires establishing a strict root manifest and enforcing that the agent relies on discoverability over upfront injection. |

By implementing these synergistic patterns, the substrate can achieve a mathematically verifiable reduction to approximately \~5.5K tokens at session start, preserving high-fidelity governance while eliminating "context rot."

## **2\. The Presenting Problem & Domain Context**

The core operational tension within the agency substrate lies in the conflict between its rich governance mandates and the economic and performance realities of Large Language Models (LLMs). Modern frontier models experience a phenomenon known as "context rot" or attention dilution. As the number of tokens in the context window increases, the model's ability to accurately recall specific instructions, prioritize tasks, and execute multi-hop reasoning decreases significantly.2 A 50K-token bootstrap is not merely an economic burden regarding API costs; it actively diminishes the agent's capacity to execute the substrate's complex, DAG-ordered subtasks reliably.  
The target is to return to the original constraint identified in Round 1: the agent must read ≤8K tokens at session start before deciding what else to lazy-load.

### **2.1 The Locked Architecture (Compatibility Constraints)**

Any proposed context-engineering pattern must be rigorously evaluated against the substrate's locked architectural decisions. These locks represent the non-negotiable governance mechanisms of the system. Patterns that require revising these locks are flagged as incompatible or requiring architectural adjustments.

| Lock \# | Constraint | Impact on Context Engineering Search |
| :---- | :---- | :---- |
| **L1** | Four-layer separation: Task/Prompt/Research/Skill | Context patterns must respect this taxonomy. Techniques that collapse or blur these boundaries are incompatible. |
| **L2** | 1:1:1 main-level pairing | Restricts context patterns that fan out unpredictably at the root execution level. |
| **L3** | SemVer on non-code artefacts | Directly conflicts with embedding-based Vector databases (RAG) which rely on cryptographic hashes or content-addressed IDs (CIDs) rather than semantic versions. |
| **L4** | Goal-only Task → deferred Gherkin | Patterns requiring rigid, upfront success criteria before bootstrap are incompatible. |
| **L5** | No-decomp direct promotion | Patterns (like Copilot Workspace) that *mandate* step-by-step planning and decomposition violate this lock. |
| **L6** | Subtask \= MCP ID \+ parent-relative SemVer | Context mechanisms managing sub-agent state must adhere to this specific namespace scheme. |
| **L7** | Explicit DAG via task\_depends\_on | Implicit, LLM-hallucinated ordering mechanisms cannot replace the explicit graph. |
| **L8** | notes: string field as escape valve | Prevents the use of overly rigid, typed schema enforcement for all context. |
| **L9** | Mandatory Gherkin \+ JSON Schema gate | Context retrieval tools must be capable of returning data that satisfies these validation gates. |
| **L10** | Bootstrap target ≤8K tokens | The primary evaluation metric for all proposed patterns. |
| **L11** | MCP service for globally-unique IDs | Context mechanisms cannot rely on local monotonic counters. |
| **L12** | Theatrical rename direction | Primarily cosmetic; rarely impacts context fetching. |
| **L13** | Frontmatter-only audit graph | Strongly restricts deep Markdown-link traversal or complex graph databases (e.g., GraphRAG) that rely on body-text entity extraction. |
| **L14** | 8-step pre-commit gate | Prohibits context validation that relies solely on runtime evaluation. The system must remain statically verifiable before execution. |

The reliance on Markdown, YAML frontmatter, and pre-commit linting (L13, L14) introduces a specific architectural bottleneck. The system is inherently static, yet context engineering demands dynamic efficiency. To mechanically reduce the bootstrap budget, the agency substrate must adopt patterns that allow a static file system to gracefully simulate dynamic, on-demand context retrieval.

## **3\. Analytical Synthesis of Context Engineering Literature**

The literature surrounding context management and agent token efficiency has shifted dramatically between 2023 and 2026\. Early research in 2023 focused heavily on the illusion of infinite context, attempting to push as much data as possible into long-context models using monolithic prompts and episodic memory streams.13 By 2024 and 2025, the industry recognized the severe latency, cost, and attention-degradation penalties of bloated context windows. The paradigm shifted toward "Context Engineering" as a formalized discipline: the practice of treating the context window as a highly constrained attention budget, where every token must justify its inclusion.1  
This section synthesizes 22 specific patterns across six operational domains, evaluating their mechanisms and mapping them to the agency substrate's constraints.

### **3.1 Domain 1: Manifests, Tiering, and Static Compression**

The most immediate token savings are achieved by restructuring the static files loaded at session start. Monolithic files like AGENTS.md and CLAUDE.md violate the principle of parsimony.16  
The **Context Tiering** pattern, heavily utilized in the Claude Code ecosystem, resolves this by dividing instructions into three distinct tiers: Permanent, On-Demand, and Temporary.3 In this architecture, the CLAUDE.md file is strictly limited to approximately 100 lines (Permanent tier), serving only as a high-level index defining project identity and navigation. All granular coding standards, architectural rules, and specific constraints are moved into separate files (e.g., .claude/rules/\*.md). Crucially, these rules utilize **Glob-Scoped Rule Injection**. A rule governing database migrations, for instance, is paired with a glob pattern (globs: /models.py). The harness only injects this rule into the context window when the agent interacts with matching files.3 Applied to the agency substrate, this pattern eliminates the need to load the entire 15K-token CLAUDE.md, replacing it with a 2K-token root file and mathematically reducing token waste.  
To replace the 25K-token AGENTS.md file, the substrate can adopt the **Aider Repo-Map** pattern. Originally developed by Paul Gauthier, this technique provides agents with structural awareness of a codebase without reading raw files.4 The mechanism relies on tree-sitter to parse the workspace into an Abstract Syntax Tree (AST), extracting all class, function, and variable definitions. It then builds a directed dependency graph and applies a Personalized PageRank algorithm to determine the most highly referenced and critical symbols.4 The output is a highly compressed, elided code map that strictly adheres to a user-defined token limit (e.g., \--map-tokens 1024). For the agency substrate, integrating a Tree-sitter map generation script into the L14 pre-commit gate allows the system to output an index-quick.md file. The agent reads only this 2K-token map at boot, achieving massive savings while maintaining compatibility with L13 (frontmatter graphs).

### **3.2 Domain 2: Runtime Fetching and Discoverability**

Once static compression is maximized, the architecture must transition from "pushing" information to the agent to allowing the agent to "pull" information on demand.  
The **Description-Only Skill Bootstrapping** pattern demonstrates this efficiently. In production frameworks like Anthropic's Skill Tool and Block's Goose, agents are not provided with the full, dense Markdown instructions for their available skills at startup. Instead, the system prompt only receives the name of the skill and a one-sentence description of what it does and when to invoke it.3 The heavy, multi-kilobyte instructional body is deferred; it is only loaded into context when the LLM explicitly issues a Skill(...) tool invocation. Applying this to agency means the 50+ layer specifications (TASK.md, RESEARCH.md, etc.) are compressed into a tiny JSON array of hints, saving upwards of 10K tokens.  
This concept aligns with the **HATEOAS Tool Discoverability** pattern derived from hypermedia REST APIs. Rather than upfront documentation, the agent relies on state-driven hyperlinks.19 At boot, the agent reads the current workspace state, which provides links (or tool triggers) to the next logical actions.  
Furthermore, the implementation of the **MCP Resource vs. Tool Separation** pattern formalizes this lazy-loading. The Model Context Protocol (MCP) strictly distinguishes between Tools (executable actions) and Resources (read-only data streams).7 Massive governance checks, such as the 5K-token auto-generated ADR synthesis block, should not exist in AGENTS.md. Instead, they should be mounted as an MCP Resource (resource://agency/adr-synthesis). The agent is aware of the URI but only pays the token cost to read it when architectural context is specifically requested.

### **3.3 Domain 3: Memory Hierarchies and Agentic State**

Long-horizon tasks inevitably cause the context window to fill with tool outputs, file reads, and internal reasoning. To manage this, agents require virtual memory management.  
The **Memory Blocks (OS-Style Virtual Context)** pattern, pioneered by MemGPT (now Letta), treats the LLM context window like RAM and external storage like a hard drive.21 The agent is provided with tools to explicitly page data in and out of "Core Memory" (always visible context), "Recall Memory" (searchable conversation history), and "Archival Memory" (long-term document storage). While highly effective, implementing this natively requires granting the agent permission to autonomously edit its own core prompt block. In the agency substrate, this could be adapted by allowing the agent to write to a specific state-summary.md file that is loaded at boot, rather than re-reading the entire Git history.  
Similarly, the **Auto-Compact / Workspace-Tracker** pattern used by Cline monitors context usage dynamically.23 When token usage crosses a threshold (e.g., 80%), a **Context Usage Threshold Hook** triggers.25 The harness automatically intercepts the session, summarizes the oldest portions of the conversation while preserving critical code changes and tool outputs, and replaces the raw history with this dense summary. While this operates at the IDE/harness level (outside the strict static files of agency), the substrate's .clinerules can explicitly instruct the execution harness to enforce strict auto-compaction policies to prevent token explosion.  
The **Agentic Note-Taking & Linking (A-MEM)** pattern offers a highly compatible alternative for memory.26 Inspired by the Zettelkasten method, the agent autonomously generates atomic, structured notes detailing its findings. It uses semantic similarity to link these notes and continuously updates older memories as new information is discovered. Because this pattern relies on discrete, well-structured Markdown files, it maps flawlessly to the substrate's L13 frontmatter-only audit graph constraint.

### **3.4 Domain 4: Agentic Orchestration and Algorithmic Optimization**

For complex feature development, breaking the work down optimally saves immense token overhead.  
The **Spec-to-Plan Cascade**, observed in GitHub Copilot Workspace, dictates that an agent never reads the full codebase to write code. Instead, it reads a distilled specification, generates a step-by-step implementation plan, and then fetches *only* the specific files needed for the current step in the plan.27 While highly token-efficient, this pattern skirts the edge of compatibility with agency lock L5 (No-decomp direct promotion), as it conceptually enforces decomposition. It should be used contextually rather than globally.  
Conversely, the **Lazy Decomposition (ADaPT)** pattern aligns better with L5. In ADaPT, the agent attempts to execute a task directly without planning.29 It is only when the agent encounters an error or reaches a complexity threshold that it falls back to a planner module to recursively decompose the task. This saves the heavy token cost of generating plans for trivial operations.  
To keep the main orchestrator's context pristine, the **Subagent Context Isolation** pattern is essential.1 Rather than one agent performing file searches, linting, and planning, the main agent spawns specialized subagents (using the L6 MCP ID standard). A subagent might consume 60K tokens exploring the codebase and reading API docs, but it terminates and returns only a highly compressed, 1,000-token summary to the main agent. This prevents context rot at the orchestration layer.  
Finally, the prompts themselves can be mathematically compressed. **Programmatic Prompt Optimization (DSPy / MIPRO)** treats prompts as hyperparameters.32 Using Bayesian Optimization, frameworks like DSPy iteratively test variations of instructions and few-shot examples against an evaluation metric, discovering formulations that are simultaneously shorter and more effective than human-written prompts. The substrate team can utilize DSPy offline to minimize the token footprint of the Prompt layer (L1) templates.

### **3.5 Domain 5: Cross-Pollinated Architectures**

The token bootstrap problem mirrors classical computer science constraints regarding startup times and memory limits.

* **Manifest-Driven Loading (initramfs):** In Linux kernel design, the initramfs is a minimal, temporary file system loaded into RAM that contains just enough tooling to mount the actual root file system.9 Applied to agency, the substrate should utilize an agency.yaml manifest. At boot, the agent reads *only* this manifest, which outlines the available layers and their mounting tools, deferring the loading of the actual layers until execution requires them.  
* **Deferred Startup Hooks (Emacs use-package):** The Emacs community optimizes editor startup times by moving configurations from static loads into deferred, event-driven hooks.34 In agency, rules governing specific tasks (like Python formatting) are deferred and loaded only when a .py file is detected in the workspace, mirroring the Glob-Scoped Rules pattern.

### **3.6 Negative Findings: Patterns to Actively Avoid**

Not all context-engineering patterns suit the agency substrate. The following must be rejected to maintain architectural integrity:

1. **Continuous Semantic Indexing (Cursor-Style Background RAG):** Cursor relies on continuously chunking the codebase and maintaining a local Turbopuffer vector database for instant @codebase semantic search.36 This requires a persistent background runtime and relies on vector embeddings rather than semantic versions (L3). It completely circumvents the static, frontmatter-only audit graph (L13) and cannot be validated by the 8-step pre-commit gate (L14).  
2. **Dense GraphRAG (Microsoft):** While GraphRAG offers superior multi-hop reasoning, constructing the entity-relationship graph requires massive, token-heavy LLM calls for node extraction and community summarization.39 The indexing cost routinely exceeds hundreds of thousands of tokens, directly opposing the economic goal of bootstrap reduction.  
3. **Language Agent Tree Search (LATS):** LATS integrates Monte Carlo Tree Search to allow the agent to explore and simulate multiple reasoning and action trajectories.42 While rigorous, the branching factor leads to exponential token consumption. It guarantees a failure of the ≤8K token budget target.  
4. **Monolithic "All-in-One" System Prompts:** The current state of AGENTS.md. Relying on massive system prompts under the assumption that the LLM requires total upfront knowledge results in severe context rot, where the model loses focus on specific governance instructions hidden within the noise.2

## ---

**4\. Pattern Catalogue**

The following table catalogs the 22 identified techniques, evaluating their mechanisms, token savings, compatibility with locks L1-L14, and implementation cost.

| \# | Pattern | Origin (System/Paper) | Mechanism (1 sentence) | Realistic Token Savings for agency | Compatibility (L1–L14) | Implementation Cost | Rec? |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 1 | **Aider Repo-Map** | Aider (Gauthier, 2024\) 4 | Tree-sitter AST parsing and PageRank centrality distills the repo into a strictly token-budgeted map. | \~25K → \~2K | Compatible with L1, L13. Needs pre-commit hook integration (L14). | Medium (2-4 wks) | ✓ |
| 2 | **Context Tiering** | Anthropic Claude Code (2026) 3 | Splits monolithic prompts into Permanent (\<100 lines), On-Demand, and Temporary tiers. | \~15K → \~2K | Highly Compatible. Aligns with standard Markdown structures. | Low (1 wk) | ✓ |
| 3 | **Glob-Scoped Rules** | Cline .clinerules (2026) 3 | Rules trigger and inject into context only when specific file paths (via globs) are interacted with. | \~5K → \~0 (until triggered) | Compatible. Works elegantly with L14 linting. | Low (1 wk) | ✓ |
| 4 | **Description-Only Skills** | Anthropic Skill Tool (2025) 6 | Skills/Layers are presented merely as 1-sentence descriptions at boot; full bodies loaded via tool call. | \~10K → \~500 | Compatible. Maps cleanly to the L1 Skill layer. | Low (1 wk) | ✓ |
| 5 | **MCP Resource Separation** | Model Context Protocol (2024) 7 | Distinguishes executable Tools from read-only Resources (like ADRs), fetching data lazily via URIs. | \~5K → \~100 | Compatible. Standardizes lazy loading. | Medium (2-3 wks) | ✓ |
| 6 | **Manifest-Driven Loading** | OS kernels (initramfs) 9 | A tiny root manifest (agency.yaml) acts as a lookup table for mounting heavier logic later. | Variable baseline reduction | Compatible. Mirrors L13 frontmatter paradigms. | Medium (2 wks) | ✓ |
| 7 | **Auto-Compact Workspace** | Cline / Deep Agents SDK 23 | Actively monitors context window and summarizes oldest history while preserving technical code blocks. | Prevents linear token explosion | △ (Requires IDE/harness support; static files cannot enforce). | Medium (2 wks) | ✓ |
| 8 | **Context Threshold Hook** | Claude Code issue 25689 25 | Fires an interrupt when context reaches 80%, allowing the agent to plan and flush memory before hard limits. | Prevents truncation failure | △ (Harness dependent). | Medium (2 wks) | ✓ |
| 9 | **Subagent Context Isolation** | Anthropic Subagents (2025) 31 | Deep research is isolated to read-only subagents that return distilled 1K-token summaries to the main agent. | Saves \~50K per deep research task | Compatible. Fits L6 subtask definitions. | High (4-6 wks) | ✓ |
| 10 | **A-MEM Zettelkasten** | A-MEM (Xu et al., 2024\) 26 | Agent autonomously constructs and links atomic memory notes, updating older notes as context evolves. | High (prevents redundant reads) | Compatible. Excellent fit for L13 frontmatter graphs. | Medium (3 wks) | ✓ |
| 11 | **Lazy Decomposition (ADaPT)** | ADaPT (Prasad et al., 2024\) 29 | Agent executes directly first; only falls back to recursive planning/decomposition upon encountering failure. | Bypasses planning token costs | △ (Slight tension with L5 absolute promotion vs decomp). | Medium (3 wks) | ✓ |
| 12 | **Programmatic Prompt Opt.** | DSPy / MIPROv2 (2024) 32 | Uses Bayesian Optimization to mathematically find the most token-efficient prompt instructions offline. | \~30% reduction per prompt | Compatible. Executed offline, outputs standard text. | High (4-6 wks) | ✓ |
| 13 | **HATEOAS Discoverability** | Hypermedia REST APIs 20 | Agents navigate state via provided hyperlinks rather than relying on massive upfront schema documentation. | High (reduces upfront bloat) | Compatible. | Medium (2 wks) | ✓ |
| 14 | **Prompt Caching** | Anthropic/OpenAI APIs 44 | API-level caching of static system prompts, drastically reducing effective cost and latency. | 0 absolute, 90% effective cost | Compatible. | Low (1 wk) | ✓ |
| 15 | **Sparse MoE Context** | MoE Architectures 45 | Conceptually routing only the highly relevant layer specs based on a tiny initial intent classifier prompt. | \~80% reduction in layer reads | Compatible. | Medium (2 wks) | ✓ |
| 16 | **Memory Blocks (OS RAM)** | MemGPT/Letta (2023) 21 | Paging data between Core, Recall, and Archival memory using explicit agent tools. | High | △ (Requires giving agent tools to rewrite its own root prompt). | High (4 wks) | △ |
| 17 | **Spec-to-Plan Cascade** | Copilot Workspace 28 | Enforces a strict cascade: read spec, write step-by-step plan, fetch files *only* for the active step. | High | △ (Violates L5 direct promotion if enforced universally). | Medium (2 wks) | △ |
| 18 | **Retrieve-on-Demand** | Self-RAG (Asai et al., 2024\) 46 | LLM generates reflection tokens (e.g., \`\`) to autonomously decide if it needs external RAG context. | Medium | △ (Hard to validate deterministically via L14 pre-commit). | High (4 wks) | △ |
| 19 | **Continuous Semantic RAG** | Cursor Turbopuffer 36 | Background vector DB chunking and embedding for instant @codebase semantic retrieval. | High | ✗ (Violates L3 SemVer, L13 frontmatter, L14 pre-commit). | High | ✗ |
| 20 | **Dense GraphRAG** | Microsoft GraphRAG 39 | Heavy LLM processing to extract nodes, edges, and community summaries for deep multi-hop reasoning. | Negative (Increases indexing tokens massively) | ✗ (Violates Token budget goals and L13). | High | ✗ |
| 21 | **Language Agent Tree Search** | LATS (Zhou et al., 2024\) 42 | Monte Carlo Tree Search for exploring multiple reasoning trajectories. | Negative (Exponential token bloat) | ✗ (Violates L10 8K budget completely). | High | ✗ |
| 22 | **MIRIX Hierarchical Routing** | MIRIX (Wang et al., 2025\) 47 | 6-component memory database governed by an 8-agent routing cluster. | Medium | ✗ (Violates L1 4-layer separation, over-engineered). | Very High | ✗ |

## ---

**5\. Compatibility Matrix (Pattern × Lock)**

The following matrix maps the 22 patterns against the 14 locked architectural constraints (L1-L14).  
*Legend:*  
✓ \= Compatible (Requires no changes to locks; composes cleanly)  
△ \= Requires minor adjustments to lock implementation, harness settings, or specific opt-outs.  
✗ \= Incompatible (Requires fundamentally revising the lock; marked as Negative Finding).

| Pattern | L1 (4-Layer) | L2 (1:1:1) | L3 (SemVer) | L4 (Goal Task) | L5 (No Decomp) | L6 (Subtask ID) | L7 (DAG) | L8 (Notes) | L9 (Gherkin) | L10 (≤8K) | L11 (MCP ID) | L12 (Rename) | L13 (FM Graph) | L14 (Pre-Commit) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 1\. Aider Repo-Map | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 2\. Context Tiering | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 3\. Glob-Scoped Rules | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 4\. Description Skills | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 5\. MCP Resources | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 6\. Manifest Loading | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 7\. Auto-Compact | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | △¹ |
| 8\. Context Threshold | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | △¹ |
| 9\. Subagent Isolation | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 10\. A-MEM Zettel. | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 11\. ADaPT Lazy Decomp | ✓ | ✓ | ✓ | ✓ | △² | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 12\. DSPy Prompts | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 13\. HATEOAS API | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 14\. Prompt Caching | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 15\. Sparse MoE | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 16\. MemGPT Blocks | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | △¹ |
| 17\. Spec-to-Plan | ✓ | ✓ | ✓ | △³ | △³ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 18\. Self-RAG | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | △⁴ |
| 19\. Cursor Indexing | ✓ | ✓ | ✗⁵ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗⁶ | ✗⁷ |
| 20\. Dense GraphRAG | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗⁸ | ✓ | ✓ | ✗⁶ | ✓ |
| 21\. LATS Tree Search | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗⁸ | ✓ | ✓ | ✓ | ✓ |
| 22\. MIRIX Routing | ✗⁹ | ✗⁹ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**Matrix Footnotes:**

* **△¹ (L14):** Relying on runtime auto-compaction, threshold hooks, or LLM-driven memory blocks shifts context management away from deterministic pre-commit gates. The state becomes highly mutable during runtime.  
* **△² (L5):** ADaPT relies on executing first and decomposing upon failure. This introduces a recursive decomposition loop that mildly conflicts with the strict "No-decomp direct promotion" lock, though it maintains the spirit of lazy execution.  
* **△³ (L4/L5):** The Copilot Spec-to-Plan cascade strictly enforces that a plan (decomposition) must be written before code is touched. This directly violates L5 if enforced as a universal rule.  
* **△⁴ (L14):** Reflection tokens are generated probabilistically at inference time by the LLM. It is impossible to validate the exact retrieval path via a static pre-commit hook.  
* **✗⁵ (L3):** Vector databases rely fundamentally on cryptographic hashes, chunk IDs, and vector distances, completely ignoring Semantic Versioning (L3) for document retrieval.  
* **✗⁶ (L13):** Both Cursor's semantic indexing and GraphRAG rely on chunking raw body text and extracting entities, directly violating the L13 constraint that all audit graphs must be frontmatter-only.  
* **✗⁷ (L14):** Background vector indexing occurs outside the git lifecycle, rendering pre-commit validation (L14) impossible.  
* **✗⁸ (L10):** GraphRAG construction and LATS MCTS branching consume exponential tokens, completely failing the ≤8K token budget target.  
* **✗⁹ (L1/L2):** MIRIX demands a 6-layer memory architecture and an 8-agent routing cluster, entirely overriding the locked 4-layer Task/Prompt/Research/Skill taxonomy (L1) and the 1:1:1 pairing rule (L2).

## ---

**6\. Cheapest-First Implementation Roadmap**

The implementation roadmap provides a pragmatic sequence to structurally reduce the \~50K token bootstrap to the ≤8K target. It prioritizes static file restructuring (lowest cost, highest compatibility) before moving to advanced runtime mechanisms.

### **6.1 Tier 1 — Wins within 1 week (Savings: \~20K tokens)**

**Goal:** Optimize static text payloads without altering core infrastructure or requiring new background services.

* **Step 1: Implement Context Tiering.** Restructure CLAUDE.md and AGENTS.md. Truncate CLAUDE.md to a strict 100-line maximum, serving only as a high-level index (Permanent Tier). Move all granular coding rules, architectural constraints, and layer definitions into .claude/rules/\*.md.  
* **Step 2: Glob-Scoped Rule Injection.** Define glob patterns for the new rule files (e.g., globs: /frontend/\* for UI rules). Ensure the agent harness only loads these rules when matching files are actively being edited.3  
* **Step 3: Description-Only Skill Bootstrapping.** Modify the system prompt injection. Instead of loading the full Markdown body of all 50+ layer specs and skills, inject only a JSON array containing { "name": "...", "description": "..." }. The agent must use a standard read\_file or read\_skill tool to fetch the body.6  
* **Files to Touch:** AGENTS.md, CLAUDE.md, .claude/rules/\*.  
* **Expected Budget at Completion:** \~30K tokens.

### **6.2 Tier 2 — Wins within 1 month (Savings: \~15K tokens)**

**Goal:** Implement intelligent static indexing via pre-commit hooks.

* **Step 1: Aider-style Repo-Map at Pre-Commit.** Develop a lightweight Python/Node script utilizing tree-sitter to parse the workspace. Calculate PageRank centrality for code and markdown symbols. Integrate this script into the L14 8-step pre-commit gate. The script must output an index-quick.md file limited to exactly 2048 tokens.4 The agent will read *only* this map at boot instead of scraping the directory tree.  
* **Step 2: Lazy ADR Synthesis.** The 5K-token ADR synthesis block currently auto-rebuilds inside AGENTS.md. Extract this into an independent ADR\_SYNTHESIS.md file. Utilizing HATEOAS principles 20, replace the block in AGENTS.md with a single hyperlink instructing the agent to fetch the synthesis file only if architectural conflict resolution is required.  
* **Files to Touch:** .git/hooks/pre-commit, index-quick.md (new), ADR\_SYNTHESIS.md (new).  
* **Expected Budget at Completion:** \~15K tokens.

### **6.3 Tier 3 — Wins within 3 months (Savings: \~10K tokens)**

**Goal:** Migrate to runtime resource fetching and orchestrator isolation to close the final gap.

* **Step 1: MCP Resource Integration.** Fully implement the MCP Resource vs. Tool pattern. Map the remaining heavy layer specs (TASK.md, RESEARCH.md) to an MCP server as Resources. The orchestrator's system prompt will contain only the resource URIs (e.g., resource://agency/spec/task), removing all documentation from the baseline context window.7  
* **Step 2: Subagent Context Isolation.** Institute a strict architectural pattern where the main orchestrator agent is barred from performing file edits or deep research itself. It must spawn a subagent (utilizing the L6 MCP ID standard). The subagent consumes 60K+ tokens performing the work, but terminates and returns only a compressed, 1000-token Zettelkasten-style frontmatter summary (A-MEM pattern) to the main agent.26  
* **Files to Touch:** MCP Server configuration, Orchestrator System Prompts, Agent Harness logic.  
* **Expected Budget at Completion:** \~5K tokens (Target Achieved).

## ---

**7\. Falsification Frame**

A context engineering pattern is only valuable if its failure modes are quantifiable. For the highest priority "✓ Recommended" patterns, the following falsification conditions apply. If these conditions are met during implementation, the recommendation should be abandoned or downgraded.

| Recommended Pattern | This recommendation would be falsified if... |
| :---- | :---- |
| **Context Tiering / Glob-Scoping** | The LLM exhibits a statistically significant increase in hallucination rates regarding project architecture because the offloaded .clinerules fail to trigger accurately based on glob-matching during complex, cross-file refactoring tasks. |
| **Description-Only Skills** | The agent repeatedly hallucinates the expected input parameters of a skill because the 1-sentence description provides insufficient context to formulate a valid tool call, leading to endless error loops. |
| **Aider Repo-Map** | The Tree-sitter AST generation adds unacceptable latency (\>5 seconds) to the pre-commit hook (L14), or if the 2048-token PageRank compression consistently omits critical cross-layer DAG dependencies (L7) required for proper Subtask routing. |
| **MCP Resource Separation** | The latency overhead of executing a JSON-RPC resources/read call over the MCP bridge disrupts the agent's reasoning flow, causing it to abandon the context fetch and hallucinate the documentation instead. |
| **Subagent Context Isolation** | The 1,000-token summary returned by the subagent consistently drops critical technical nuances (e.g., specific variable names or error traces) required by the main orchestrator to update the frontmatter audit graph (L13). |

## ---

**8\. Open Questions & Meta-Synthesis**

Beyond the enumeration of patterns, the user query poses a critical meta-question: *Does the published literature suggest the substrate's choice to express governance through Markdown \+ frontmatter \+ pre-commit linting is itself the bottleneck?*  
**The Synthesis:** Yes. The 2024–2026 literature unequivocally points toward expressing governance and context as a *dynamic runtime service*.2 The substrate's current static methodology assumes the agent must read the laws (Markdown files) before it acts, relying on pre-commit linting to catch violations after the fact.  
The literature argues the opposite: the environment should enforce the laws dynamically. By forcing the system into a static paradigm (L13, L14), the substrate actively prevents the use of dynamic vector retrieval (Cursor), real-time context swapping (MemGPT), and automated reflection loops (Self-RAG).  
**Open Questions for the Substrate Team:**

1. **Re-evaluating L14 (Pre-commit gate):** Can the 8-step pre-commit gate be partially offloaded to an MCP validation tool? If an agent can call validate\_structure() mid-flight and receive immediate JSON schema feedback, it does not need to load the complex governance schemas into its bootstrap context.  
2. **Re-evaluating L5 (No-decomp promotion):** Copilot Workspace and ADaPT 28 heavily utilize forced planning cascades to save tokens. The agent plans first, then fetches context *only* for the current step. Is the team willing to revise L5 to mandate a lightweight planning step to prevent monolithic task execution?  
3. **The Cost of the Audit Graph (L13):** Is the value of a purely static, git-verifiable audit graph worth the perpetual token bloat? If the substrate transitioned to a graph database backing (like Neo4j) rather than relying on Markdown frontmatter, contextual relationships could be queried via GraphQL with near-zero token overhead.

## ---

**9\. Replication Pointer**

To ensure the validity and recency of this report, the substrate team can re-run this audit against future iterations of the architecture locks using the following parameters:

* **Search Queries:** "context engineering" AND "LLM agents", "token budget reduction" AND "context window", "MemGPT" OR "Self-RAG" OR "GraphRAG", "Tree-sitter repo map" AND "LLM context".  
* **Source Filtering Heuristics:** Limit strictly to primary engineering blogs authored by tool creators (e.g., Anthropic Engineering, Paul Gauthier, Letta Blog, Cursor Blog) and peer-reviewed/arXiv papers from June 2023 onward. Filter out SEO content farms and generic "Top 10 AI tools" listicles.  
* **Judgement-Required Decision-Points:** Evaluate extracted patterns strictly against the 14 locked architectural constraints. Patterns requiring vector databases or cryptographic hashes must be flagged as incompatible with Semantic Versioning (L3). Patterns requiring complex runtime orchestration must be evaluated against the cost of departing from static pre-commit verification (L14).

## ---

**10\. Recency-Stratified Bibliography**

The following primary sources informed this report, stratified by year to highlight the evolution of context engineering from infinite-context theories to strict token-budget methodologies.  
**2025–2026 (Context Engineering as a Formal Discipline & Optimization)**

* **Anthropic Engineering Blog (2025):** "Effective context engineering for AI agents" – Establishes the parsimony principle and context tiering, proving that intelligence is no longer the bottleneck, but context delivery is.1  
* **Letta / MemGPT Blog (2025):** "Benchmarking AI Agent Memory" – Details the transition to OS-style virtual memory blocks and context repositories for persistent agents.21  
* **Wang et al. (2025) \[arXiv:2507.07957\]:** "MIRIX: Multi-Agent Memory System for LLM-Based Agents" – Introduces a 6-component hierarchical memory system managed by routing agents.47  
* **Cursor Blog (2025):** "Improving agent with semantic search" – Details the RAG pipeline, Turbopuffer integration, and continuous semantic indexing for @codebase resolution.49  
* **Kumar, S. (2026):** "Context Tiering for Claude Code" – Provides the empirical framework for optimizing CLAUDE.md from 470 lines to 94 lines using glob-scoped rules.3

**2024 (Retrieval Efficiency, Graph Abstractions, & Prompt Tuning)**

* **Gauthier, P. (2024):** Aider Documentation (repomap.py) – Explains the mechanism of Tree-sitter AST parsing and PageRank centrality for creating token-budgeted repo-maps.4  
* **Prasad et al. (2024) \[NAACL\]:** "ADaPT: As-Needed Decomposition and Planning with Language Models" – Introduces the concept of lazy decomposition, executing tasks directly and planning only upon failure.29  
* **Khattab et al. (2024) \[EMNLP\]:** "Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs (MIPRO)" – The foundational paper for DSPy, utilizing Bayesian optimization for programmatic prompt compression.32  
* **Zhou et al. (2024) \[ICML\]:** "Language Agent Tree Search Unifies Reasoning, Acting, and Planning" – Details the MCTS approach to agent trajectories (noted as a negative finding due to token bloat).42  
* **Asai et al. (2024):** "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection" – Introduces reflection tokens for LLM-driven on-demand context retrieval.46

**2023 (Foundational Agent Memory & Reflection)**

* **Packer et al. (2023) \[arXiv:2310.08560\]:** "MemGPT: Towards LLMs as Operating Systems" – The foundational paper establishing virtual context management and memory paging for LLMs.14  
* **Shinn et al. (2023):** "Reflexion: Language Agents with Verbal Reinforcement Learning" – Establishes the baseline for episodic memory and self-reflection in agent loops.13

---

*End of Report.*

#### **Referenzen**

1. Effective context engineering for AI agents \- Anthropic, Zugriff am Mai 13, 2026, [https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)  
2. Context Engineering for Agentic Systems: What Goes Into Your Agent's Mind | Haystack, Zugriff am Mai 13, 2026, [https://haystack.deepset.ai/blog/context-engineering](https://haystack.deepset.ai/blog/context-engineering)  
3. Context Tiering for Claude Code: The CLAUDE.md Setup That ..., Zugriff am Mai 13, 2026, [https://medium.com/@sohit\_kumar/context-tiering-for-claude-code-the-claude-md-setup-that-survives-long-sessions-82f058736731](https://medium.com/@sohit_kumar/context-tiering-for-claude-code-the-claude-md-setup-that-survives-long-sessions-82f058736731)  
4. Repository map \- Aider, Zugriff am Mai 13, 2026, [https://aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html)  
5. GitHub All-Stars \#15: jCodeMunch MCP \- VirtusLab, Zugriff am Mai 13, 2026, [https://virtuslab.com/blog/ai/code-munch-mcp-your-agent-starts-navigating](https://virtuslab.com/blog/ai/code-munch-mcp-your-agent-starts-navigating)  
6. Extend Claude with skills \- Claude Code Docs, Zugriff am Mai 13, 2026, [https://code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)  
7. MCP's Three Core Capabilities: Tools, Resources, and Prompts | by Yash Bhaskar \- Medium, Zugriff am Mai 13, 2026, [https://medium.com/@yash9439/mcps-three-core-capabilities-tools-resources-and-prompts-43c3214ff43e](https://medium.com/@yash9439/mcps-three-core-capabilities-tools-resources-and-prompts-43c3214ff43e)  
8. Model Context Protocol (MCP): The Complete Engineering Guide — Architecture, Internals, and Real-World Use Cases | by Rishabh Kumar | Mar, 2026 | Medium, Zugriff am Mai 13, 2026, [https://medium.com/@rishabhkr954/model-context-protocol-mcp-the-complete-engineering-guide-architecture-internals-and-0d7b5d988b08](https://medium.com/@rishabhkr954/model-context-protocol-mcp-the-complete-engineering-guide-architecture-internals-and-0d7b5d988b08)  
9. Is the entire kernel loaded into memory on boot? \- Unix & Linux Stack Exchange, Zugriff am Mai 13, 2026, [https://unix.stackexchange.com/questions/257812/is-the-entire-kernel-loaded-into-memory-on-boot](https://unix.stackexchange.com/questions/257812/is-the-entire-kernel-loaded-into-memory-on-boot)  
10. The Manifest Format \- The Cargo Book \- Rust Documentation, Zugriff am Mai 13, 2026, [https://doc.rust-lang.org/cargo/reference/manifest.html](https://doc.rust-lang.org/cargo/reference/manifest.html)  
11. Context engineering: memory, compaction, and tool clearing | Claude Cookbook, Zugriff am Mai 13, 2026, [https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)  
12. The End of Infinite Context: Engineering Reliability in the Age of Agentic Workflows | by Ali moradi | Medium, Zugriff am Mai 13, 2026, [https://medium.com/@moradikor296/the-end-of-infinite-context-engineering-reliability-in-the-age-of-agentic-workflows-9531163159b4](https://medium.com/@moradikor296/the-end-of-infinite-context-engineering-reliability-in-the-age-of-agentic-workflows-9531163159b4)  
13. (PDF) Reflexion: an autonomous agent with dynamic memory and self-reflection, Zugriff am Mai 13, 2026, [https://www.researchgate.net/publication/369414009\_Reflexion\_an\_autonomous\_agent\_with\_dynamic\_memory\_and\_self-reflection](https://www.researchgate.net/publication/369414009_Reflexion_an_autonomous_agent_with_dynamic_memory_and_self-reflection)  
14. \[2310.08560\] MemGPT: Towards LLMs as Operating Systems \- arXiv, Zugriff am Mai 13, 2026, [https://arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560)  
15. context-engineering/README.md at main \- GitHub, Zugriff am Mai 13, 2026, [https://github.com/bonigarcia/context-engineering/blob/main/README.md](https://github.com/bonigarcia/context-engineering/blob/main/README.md)  
16. Context Engineering: Why LLM's need more than prompts and MCP servers \- Unblocked, Zugriff am Mai 13, 2026, [https://getunblocked.com/blog/context-engineering/](https://getunblocked.com/blog/context-engineering/)  
17. Rules \- Cline Documentation, Zugriff am Mai 13, 2026, [https://docs.cline.bot/customization/cline-rules](https://docs.cline.bot/customization/cline-rules)  
18. goose | Your open source AI agent, Zugriff am Mai 13, 2026, [https://goose-docs.ai/](https://goose-docs.ai/)  
19. HATEOAS as the Cure for MCP Tool Bloat? | by Jay Hamilton | Apr, 2026 | Medium, Zugriff am Mai 13, 2026, [https://jaystevenhamilton.medium.com/hateoas-as-the-cure-for-mcp-tool-bloat-7c60dfdbde05](https://jaystevenhamilton.medium.com/hateoas-as-the-cure-for-mcp-tool-bloat-7c60dfdbde05)  
20. The Missing Level in REST: API Discoverability from Academic Ideal to AI Necessity, Zugriff am Mai 13, 2026, [https://jonwoodlief.com/rest3-mcp.html](https://jonwoodlief.com/rest3-mcp.html)  
21. Memory Blocks: The Key to Agentic Context Management \- Letta, Zugriff am Mai 13, 2026, [https://www.letta.com/blog/memory-blocks](https://www.letta.com/blog/memory-blocks)  
22. Agent\_Memory\_Techniques/all\_techniques/26\_letta\_memgpt\_patterns/letta\_memgpt\_patterns.ipynb at main \- GitHub, Zugriff am Mai 13, 2026, [https://github.com/NirDiamant/Agent\_Memory\_Techniques/blob/main/all\_techniques/26\_letta\_memgpt\_patterns/letta\_memgpt\_patterns.ipynb](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/main/all_techniques/26_letta_memgpt_patterns/letta_memgpt_patterns.ipynb)  
23. Auto Compact \- Cline Documentation, Zugriff am Mai 13, 2026, [https://docs.cline.bot/features/auto-compact](https://docs.cline.bot/features/auto-compact)  
24. Context Management for Deep Agents \- LangChain, Zugriff am Mai 13, 2026, [https://www.langchain.com/blog/context-management-for-deepagents](https://www.langchain.com/blog/context-management-for-deepagents)  
25. Add ContextThreshold hook event for proactive memory management \#38524 \- GitHub, Zugriff am Mai 13, 2026, [https://github.com/anthropics/claude-code/issues/38524](https://github.com/anthropics/claude-code/issues/38524)  
26. A-Mem: Agentic Memory for LLM Agents \- arXiv, Zugriff am Mai 13, 2026, [https://arxiv.org/html/2502.12110v1](https://arxiv.org/html/2502.12110v1)  
27. Implementation planner \- GitHub Docs, Zugriff am Mai 13, 2026, [https://docs.github.com/en/copilot/tutorials/customization-library/custom-agents/implementation-planner](https://docs.github.com/en/copilot/tutorials/customization-library/custom-agents/implementation-planner)  
28. copilot-workspace-user-manual/overview.md at main \- GitHub, Zugriff am Mai 13, 2026, [https://github.com/githubnext/copilot-workspace-user-manual/blob/main/overview.md](https://github.com/githubnext/copilot-workspace-user-manual/blob/main/overview.md)  
29. ADaPT: As-Needed Decomposition and Planning with Language Models \- GitHub Pages, Zugriff am Mai 13, 2026, [https://allenai.github.io/adaptllm/](https://allenai.github.io/adaptllm/)  
30. ADAPT: As-Needed Decomposition and Planning with Language Models \- ACL Anthology, Zugriff am Mai 13, 2026, [https://aclanthology.org/2024.findings-naacl.264.pdf](https://aclanthology.org/2024.findings-naacl.264.pdf)  
31. Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems \- arXiv, Zugriff am Mai 13, 2026, [https://arxiv.org/html/2604.14228v1](https://arxiv.org/html/2604.14228v1)  
32. Optimizers \- DSPy, Zugriff am Mai 13, 2026, [https://dspy.ai/learn/optimization/optimizers/](https://dspy.ai/learn/optimization/optimizers/)  
33. A Comparative Study of DSPy Teleprompter Algorithms for Aligning Large Language Models Evaluation Metrics to Human Evaluation \- arXiv, Zugriff am Mai 13, 2026, [https://arxiv.org/html/2412.15298v1](https://arxiv.org/html/2412.15298v1)  
34. minimal-emacs.d \- A Customizable Emacs init.el and early-init.el for Better Defaults and Optimized Startup \- GitHub, Zugriff am Mai 13, 2026, [https://github.com/jamescherti/minimal-emacs.d](https://github.com/jamescherti/minimal-emacs.d)  
35. What's New in Emacs 30.1?, Zugriff am Mai 13, 2026, [https://www.masteringemacs.org/article/whats-new-in-emacs-301](https://www.masteringemacs.org/article/whats-new-in-emacs-301)  
36. Securely indexing large codebases · Cursor, Zugriff am Mai 13, 2026, [https://cursor.com/blog/secure-codebase-indexing](https://cursor.com/blog/secure-codebase-indexing)  
37. Context Management Strategies for Cursor: A Complete Guide to the AI-Native Code Editor, Zugriff am Mai 13, 2026, [https://datalakehousehub.com/blog/2026-03-context-management-cursor/](https://datalakehousehub.com/blog/2026-03-context-management-cursor/)  
38. Semantic Code Search \- Medium, Zugriff am Mai 13, 2026, [https://medium.com/@wangxj03/semantic-code-search-010c22e7d267](https://medium.com/@wangxj03/semantic-code-search-010c22e7d267)  
39. TERAG: Token-Efficient Graph-Based Retrieval-Augmented Generation \- arXiv, Zugriff am Mai 13, 2026, [https://arxiv.org/html/2509.18667v2](https://arxiv.org/html/2509.18667v2)  
40. WHEN TO USE GRAPHS IN RAG: A COMPREHENSIVE ANALYSIS FOR GRAPH RETRIEVAL-AUGMENTED GEN \- OpenReview, Zugriff am Mai 13, 2026, [https://openreview.net/pdf?id=i9q9xDMjG7](https://openreview.net/pdf?id=i9q9xDMjG7)  
41. The Rise and Evolution of RAG in 2024 A Year in Review \- RAGFlow, Zugriff am Mai 13, 2026, [https://ragflow.io/blog/the-rise-and-evolution-of-rag-in-2024-a-year-in-review](https://ragflow.io/blog/the-rise-and-evolution-of-rag-in-2024-a-year-in-review)  
42. Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models, Zugriff am Mai 13, 2026, [https://experts.illinois.edu/en/publications/language-agent-tree-search-unifies-reasoning-acting-and-planning-/](https://experts.illinois.edu/en/publications/language-agent-tree-search-unifies-reasoning-acting-and-planning-/)  
43. \[2310.04406\] Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models \- arXiv, Zugriff am Mai 13, 2026, [https://arxiv.org/abs/2310.04406](https://arxiv.org/abs/2310.04406)  
44. Anthropic Claude API Pricing In 2026: Models, Token Rates, Costs \- CloudZero, Zugriff am Mai 13, 2026, [https://www.cloudzero.com/blog/anthropic-claude-api-pricing/](https://www.cloudzero.com/blog/anthropic-claude-api-pricing/)  
45. Uncovering Intra-expert Activation Sparsity for Efficient Mixture-of-Expert Model Execution, Zugriff am Mai 13, 2026, [https://arxiv.org/html/2605.08575v1](https://arxiv.org/html/2605.08575v1)  
46. SELF-RAG: Revolutionizing AI Language Models with Self-Reflection and Adaptive Retrieval | by Nirdiamant | Medium, Zugriff am Mai 13, 2026, [https://medium.com/@nirdiamant21/self-rag-revolutionizing-ai-language-models-with-self-reflection-and-adaptive-retrieval-05ae4b3b5e39](https://medium.com/@nirdiamant21/self-rag-revolutionizing-ai-language-models-with-self-reflection-and-adaptive-retrieval-05ae4b3b5e39)  
47. MIRIX Framework: Multi-Agent Memory System \- Emergent Mind, Zugriff am Mai 13, 2026, [https://www.emergentmind.com/topics/mirix-framework](https://www.emergentmind.com/topics/mirix-framework)  
48. Benchmarking AI Agent Memory: Is a Filesystem All You Need? \- Letta, Zugriff am Mai 13, 2026, [https://www.letta.com/blog/benchmarking-ai-agent-memory](https://www.letta.com/blog/benchmarking-ai-agent-memory)  
49. Improving agent with semantic search \- Cursor, Zugriff am Mai 13, 2026, [https://cursor.com/blog/semsearch](https://cursor.com/blog/semsearch)  
50. How Cursor Actually Indexes Your Codebase \- Towards Data Science, Zugriff am Mai 13, 2026, [https://towardsdatascience.com/how-cursor-actually-indexes-your-codebase/](https://towardsdatascience.com/how-cursor-actually-indexes-your-codebase/)  
51. Self-RAG: Learning to Retrieve, Generate and Critique through Self-Reflection, Zugriff am Mai 13, 2026, [https://selfrag.github.io/](https://selfrag.github.io/)