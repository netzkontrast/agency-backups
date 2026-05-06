---
type: research
status: completed
slug: superclaude-agency-orchestration-spec-doc
summary: "Verbatim Gemini Deep Research output — SuperClaude Orchestration & Meta-Governance Specification. RAW external content; binding status decided by Task 040."
created: 2026-05-06
updated: 2026-05-06
research_phase: complete
research_executes_prompt: superclaude-agency-orchestration-spec
research_friction_level: FL0
---

# SuperClaude Orchestration and Meta-Governance Specification

> **Provenance:** Verbatim output of a Gemini Deep Research run delivered 2026-05-06.
> Stored under `/research/gemini/<slug>/` per `RESEARCH.md §6.1`.
> **Not normative until evaluated by [Task 040](../../../tasks/040-superclaude-spec-evaluation/task.md).**
> The "binding / IN-FORCE" claim in §0 is the document's self-assertion, not an
> ingestion verdict.

---

**Type/Status:** Research / Active
**Slug:** superclaude-agency-orchestration-spec
**Summary:** This comprehensive architectural specification defines the repo-native governance model for integrating the SuperClaude Framework (v4.3.0) within the netzkontrast/agency repository ecosystem. It delineates exhaustive operational protocols, normative behavioral rules, and explicit Gherkin acceptance scenarios governing the utilization of all thirty `/sc:` commands, behavioral modification flags, and Model Context Protocol (MCP) servers across the project's markdown-driven workspaces.
**Dates:** Created and updated on May 6, 2026.
**Research Metrics:** Phase is complete, synthesized against the SuperClaude documentation index, command execution references, advanced MCP tooling capabilities, and the topological map of the netzkontrast/agency specification model.

## §0 System-Level Architecture and Provenance

The protocols documented herein represent the binding, IN-FORCE governance model for the netzkontrast/agency repository. This specification is the synthesized output of exhaustive architectural analysis concerning the SuperClaude Framework and its optimal deployment within a highly structured, spec-driven development environment. Artificial intelligence coding agents, when operating autonomously over extended durations, are inherently susceptible to context dilution, execution drift, and hallucinated architectural paradigms. To mitigate these failure modes, the netzkontrast/agency system relies on a deterministic, markdown-governed file topology. This topology forces agents into a predictable computational loop, reading and writing to specific state files including AGENTS.md, TASK.md, PROMPT.md, RESEARCH.md, FOLDERS.md, PRE_COMMIT.md, FRUSTRATED.md, and MAINTENANCE.md.

The SuperClaude Framework functions as a meta-programming configuration layer that injects behavioral instructions and orchestrates components, providing 30 distinct slash commands (`/sc:`), 20 specialized personas, and 8 integrated MCP servers. To prevent overlapping tool boundaries and ensure strict repository coherence, it is absolutely mandatory that all system agents and human operators conform to this specification when invoking SuperClaude operations. This specification supersedes all prior uncodified usage patterns for Claude Code, establishing a directed acyclic graph (DAG) of execution. The foundational principle of this DAG is the strict separation of planning and execution: discovery commands must never implement operational code, and implementation commands must never bypass prior architectural analysis.

The SuperClaude command namespace is strictly partitioned into eight functional categories, mapping directly to the physical topography of the repository workspaces.

| Repository Workspace | Governing SuperClaude Commands | Integrated MCP Servers | Core Operational Mandate |
|---|---|---|---|
| `AGENTS.md` | `/sc:pm`, `/sc:agent` | Serena | Defines specialized personas, global execution constraints, and contextual baselines. |
| `TASK.md` | `/sc:spawn`, `/sc:task` | Sequential | Orchestrates task hierarchies, dependency mapping, and parallel queue management. |
| `PROMPT.md` | `/sc:workflow`, `/sc:brainstorm` | Context7 | Transforms vague requirements into highly structured, actionable implementation plans. |
| `RESEARCH.md` | `/sc:research`, `/sc:spec-panel`, `/sc:business-panel` | Tavily, Playwright | Drives autonomous web discovery, competitive analysis, and multi-expert architectural scoring. |
| `FOLDERS.md` | `/sc:index-repo`, `/sc:load`, `/sc:save` | Serena | Manages topological indexing, context priming, and project memory persistence. |
| `PRE_COMMIT.md` | `/sc:reflect`, `/sc:git`, `/sc:analyze` | Context7, Sequential | Enforces quality checkpoints, task reflection, security audits, and smart version control. |
| `FRUSTRATED.md` | `/sc:troubleshoot`, `sc-document` | Chrome DevTools | Facilitates friction logging, root-cause diagnostic reports, and meta-cognitive self-correction. |
| `MAINTENANCE.md` | `/sc:improve`, `/sc:cleanup`, `/sc:build` | MorphLLM | Executes continuous systemic refactoring, dead code elimination, and dependency harmonization. |

### §0.1 Normative Vocabulary and Syntax

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" throughout this specification are to be interpreted as described in RFC 2119 / BCP 14. This strict terminology is not mere stylistic preference; it guarantees that automated agents parsing this specification can distinctively map commands to execution constraints without semantic ambiguity. Every behavioral requirement and automated acceptance scenario for a SuperClaude command is articulated using standard Gherkin syntax, carrying a stable identifier anchor in the format `SC.CMD.<aspect>.<statement>`. This convention allows external validation tools and Git pre-commit hooks to programmatically verify system compliance before repository state changes are pushed to remote origin.

## §1 Aspect 1: Global Orchestration, Initialization, and Memory Management

The foundational layer of the netzkontrast/agency implementation relies entirely on establishing a highly accurate, contextually rich environment before any code generation is attempted. If an agent begins execution without fully comprehending the rules defined in `AGENTS.md` and the structural map in `FOLDERS.md`, the probability of architectural hallucination approaches certainty. SuperClaude mitigates this through its Project Manager subsystem and dedicated memory persistence servers.

### §1.1 The Project Manager Subsystem (`/sc:pm`)

The `/sc:pm` command functions as an omnipresent background orchestrator. While it requires no explicit invocation by the user, its underlying algorithms continuously monitor the agent's interaction with the repository. The PM subsystem is responsible for restoring context from previous, disconnected sessions, delegating sub-tasks to highly specialized personas (such as `@agent-security` or `@agent-frontend-architect`), and driving the continuous Plan-Do-Check-Act (PDCA) lifecycle.

The behavior of the `/sc:pm` orchestrator is heavily customized by the contents of the `AGENTS.md` file located at the repository root. This file serves as the singular source of truth for coding standards, environment setup, and subsystem detection. The PM agent reads this file to understand whether the repository uses specific linting rules, continuous integration pipelines, or domain-driven design principles, mapping these rules directly into the active prompt context.

| Normative ID | Keyword Constraint | Operational Directive for Initialization |
|---|---|---|
| SC.CMD.1.1 | MUST | The system MUST prioritize `AGENTS.md` as the supreme configuration layer for the `/sc:pm` background process upon any new session initialization. |
| SC.CMD.1.2 | MUST | The `/sc:pm` orchestrator MUST utilize the Serena Model Context Protocol (MCP) server to achieve session persistence, ensuring continuous memory retrieval across disparate execution contexts. |
| SC.CMD.1.3 | SHOULD NOT | Explicit human invocation of the `/sc:pm` command SHOULD NOT occur unless a catastrophic context collapse necessitates a manual reset of the PDCA cycle. |

| Scenario ID | Gherkin Acceptance Criteria for PM Initialization |
|---|---|
| SC.CMD.1.A.1 | Given a new autonomous coding session initializes within the terminal interface, When the SuperClaude `/sc:pm` background layer loads into operational memory, Then it MUST automatically execute a read operation against `AGENTS.md` directives before accepting or executing any subsequent task prompt. |

### §1.2 Topological Indexing and Context Priming (`/sc:index-repo`, `/sc:load`, `/sc:save`)

To effectively navigate a repository, an agent must possess a complete mental map of its file topography. Relying solely on real-time directory traversal consumes excessive token bandwidth and leads to incomplete context windows. The `FOLDERS.md` specification dictates the naming conventions and architectural zoning of the project. The SuperClaude framework interfaces with this spec via the `/sc:index-repo` (alias `/sc:index`) command, which physically ingests the repository structure to optimize context.

When shifting between highly complex, multi-agent workflows, context must be deliberately passed. The `/sc:save` command writes the current analytical state to the Serena MCP server, and `/sc:load` proactively retrieves this overview, providing Claude with a "warm start".

| Normative ID | Keyword Constraint | Operational Directive for Indexing |
|---|---|---|
| SC.CMD.1.4 | MUST | Any major structural shift documented within `FOLDERS.md` or significant branch migration MUST trigger the `/sc:index-repo` command utilizing the `mode=update` parameter to forcefully synchronize Serena's internal memory stores. |
| SC.CMD.1.5 | MUST | The `--load` flag MUST be appended to commands when executing a handoff between specialized agent personas to ensure uninterrupted contextual flow. |
| SC.CMD.1.6 | MUST | Upon session termination, the orchestrator MUST trigger `/sc:save` to serialize active memory states, preventing context loss during prolonged periods of inactivity. |

| Scenario ID | Gherkin Acceptance Criteria for Topological Handoff |
|---|---|
| SC.CMD.1.A.2 | Given a newly cloned repository environment or a significant git branch switch, When an agent persona initiates a task execution sequence, Then the agent MUST independently run `/sc:index-repo` to build the semantic map before calling any implementation or analysis routines. |

## §2 Aspect 2: Task Orchestration, Decomposition, and Queue Management

Humans conceptualize architectures faster than agents can implement them. If a human operator dumps a massive, multi-tiered feature request into an active prompt, the agent will inevitably suffer from attention degradation, skipping critical security validations and hallucinating implementation details. The netzkontrast/agency architecture solves this by mandating a strict task queue buffer residing in `TASK.md`. The SuperClaude framework manages this queue utilizing highly specific triage mechanics: `/sc:spawn`, `/sc:task`, and `/sc:workflow`.

### §2.1 Epic Decomposition via The Planner (`/sc:spawn`)

The `/sc:spawn` command functions as the meta-system "Planner." It is strictly forbidden from writing source code. Its sole purpose is to parse a massive "Epic", decompose it into a hierarchy (Epic → Story → Task → Subtask), and coordinate dependencies. This command analyzes the request, establishes prerequisites (e.g., database schema creation must precede API endpoint implementation), and pushes the resulting nodes into the `TASK.md` file using standard Markdown checkbox syntax (`- [ ]`).

A critical component of `/sc:spawn` is its strategy execution engine. It supports `--strategy sequential`, `--strategy parallel`, and `--strategy adaptive`. By utilizing the `--parallel` flag, SuperClaude can execute multiple independent tasks concurrently across separate agent threads, radically accelerating development timelines.

| Normative ID | Keyword Constraint | Operational Directive for Spawning |
|---|---|---|
| SC.CMD.2.1 | MUST | Any human request estimated to exceed 4 hours of standard development effort MUST be parsed through `/sc:spawn` before any implementation command is authorized. |
| SC.CMD.2.2 | MUST | The orchestrator MUST append all decomposed subtasks to the `TASK.md` file, strictly adhering to the mandated Markdown task list formatting, including dependency identifiers. |
| SC.CMD.2.3 | SHOULD | The `--parallel` flag SHOULD be utilized when spawned subtasks share no blocking dependencies, enabling multi-agent concurrent processing. |

| Scenario ID | Gherkin Acceptance Criteria for Epic Breakdown |
|---|---|
| SC.CMD.2.A.1 | Given a complex feature request to "migrate legacy monolith authentication to a microservices architecture", When the human operator inputs `/sc:spawn "migrate legacy monolith authentication" --strategy adaptive --depth deep`, Then the system MUST generate a structured dependency graph, append the resulting items to `TASK.md`, and MUST NOT alter any existing executable source code. |

### §2.2 Execution Orchestration via The Tech Lead (`/sc:task`)

While the planner decomposes, `/sc:task` acts as "The Tech Lead", coordinating necessary MCP servers and activating domain-specific personas to execute a granular item extracted from `TASK.md`. It handles cross-session execution persistence for long-running processes.

When `/sc:task` picks up an item, it analyzes the requirements and dynamically loads the required persona. For example, a database migration task might load the `@agent-backend-architect`, while an interface adjustment loads the `@agent-frontend-architect`. This ensures domain expertise is applied precisely where needed.

| Normative ID | Keyword Constraint | Operational Directive for Task Execution |
|---|---|---|
| SC.CMD.2.4 | MUST | The `/sc:task` command MUST be the exclusive mechanism used to pick up and process individual nodes defined within the `TASK.md` queue. |
| SC.CMD.2.5 | MUST | When encountering highly complex or specialized domain requirements, the command MUST utilize the `--delegate` flag to force the orchestrator to assign specialized sub-agents. |

| Scenario ID | Gherkin Acceptance Criteria for Task Delegation |
|---|---|
| SC.CMD.2.A.2 | Given an unresolved specific task node in `TASK.md` titled `auth-fix-jwt`, When the command `/sc:task execute "auth-fix-jwt" --delegate` is invoked, Then the system MUST dynamically assign the `@agent-security` persona to handle the JWT refresh implementation, inheriting all security-specific constraints. |

### §2.3 Implementation Workflow Generation (`/sc:workflow`)

The `/sc:workflow` command serves as the intellectual bridge between raw Product Requirements Documents (PRDs) and actionable, step-by-step engineering plans. It ingests business logic and outputs technical roadmaps.

| Normative ID | Keyword Constraint | Operational Directive for Workflow Generation |
|---|---|---|
| SC.CMD.2.6 | MUST | When processing a newly introduced feature specification located in `PROMPT.md`, the system MUST execute `/sc:workflow` to generate a roadmap prior to writing code. |
| SC.CMD.2.7 | MUST | The system MUST accept and enforce methodology flags, explicitly `--strategy systematic` (and similar). |

## §3 Aspect 3: Discovery, Socratic Ideation, and Deep Research

Before execution can occur, the conceptual problem space must be comprehensively mapped. Jumping straight into coding from a vague, half-formed user prompt inevitably leads to refactoring loops and wasted computational resources. The `PROMPT.md` and `RESEARCH.md` environments are exclusively governed by SuperClaude's discovery and research commands, ensuring high-fidelity requirement elicitation.

### §3.1 Requirements Brainstorming (`/sc:brainstorm`)

The `/sc:brainstorm` command initiates interactive project discovery and technical feasibility analysis. Rather than passively accepting vague instructions, this command triggers a Socratic dialogue, forcing the human operator to clarify edge cases, define security boundaries, and explicitly state UI/UX assumptions.

| Normative ID | Keyword Constraint | Operational Directive for Brainstorming |
|---|---|---|
| SC.CMD.3.1 | MUST | Vague, single-sentence feature requests MUST be routed through `/sc:brainstorm` to extract latent requirements before they are permitted to enter the execution queue. |
| SC.CMD.3.2 | MUST NOT | The output of the `/sc:brainstorm` dialogue MUST result strictly in an updated `PROMPT.md` or a formal specification document; it MUST NOT write functional, executable software. |

| Scenario ID | Gherkin Acceptance Criteria for Socratic Discovery |
|---|---|
| SC.CMD.3.A.1 | Given a user inputs an ambiguous command like "build a productivity app for remote teams", When the system parses the request, Then it MUST execute `/sc:brainstorm "productivity app for remote teams"`, presenting a prioritized list of clarification questions regarding data storage, real-time collaboration requirements, and user authentication constraints. |

### §3.2 Autonomous Deep Web Research (`/sc:research`)

In an ecosystem where third-party APIs evolve rapidly and dependencies deprecate without warning, static LLM training data is insufficient. The `/sc:research` command leverages a powerful combination of MCP servers to execute autonomous web discovery. It utilizes the Tavily MCP server for primary search indexing, the Playwright MCP for bypassing complex dynamic web interfaces to extract content, and the Sequential MCP for reasoning and synthesizing the findings. This command maps directly to the workflows expected in the `RESEARCH.md` spec workspace.

When conducting research, agents are inherently prone to generating massive, redundant documents that overflow token limits. The specification dictates strict compression algorithms for research management.

| Normative ID | Keyword Constraint | Operational Directive for Autonomous Research |
|---|---|---|
| SC.CMD.3.3 | MUST | When confronting unknown external APIs, evolving cryptographic standards, or third-party documentation gaps, the system MUST pause execution and utilize `/sc:research`. |
| SC.CMD.3.4 | MUST | The agent MUST consolidate redundant findings, delete superseded or deprecated information immediately, and maintain a highly compressed synthesis in the target `RESEARCH.md` file to preserve context window capacity. |
| SC.CMD.3.5 | MUST | For complex architectural investigations requiring multi-step deduction, the agent MUST append the `--think` flag to enable advanced reasoning paradigms. |

| Scenario ID | Gherkin Acceptance Criteria for External API Discovery |
|---|---|
| SC.CMD.3.A.2 | Given an objective to implement a newly released, undocumented payment gateway feature, When the agent executes `/sc:research "Latest Stripe API integration best practices"`, Then the system MUST invoke Tavily to fetch current developer docs, use Playwright to scrape code examples, use Sequential to synthesize the findings, and write the strictly formatted output directly to the designated `RESEARCH.md` execution workspace. |

### §3.3 Multi-Expert Strategic Analysis Panels (`/sc:spec-panel` & `/sc:business-panel`)

SuperClaude introduces the sophisticated concept of multi-expert analysis panels. Relying on a single generalized LLM persona to evaluate complex enterprise architecture introduces blind spots. The `/sc:spec-panel` command evaluates technical specifications by simultaneously applying multiple established engineering frameworks (e.g., Wiegers, Fowler), while `/sc:business-panel` analyzes the strategic business value using frameworks like Porter or Drucker.

These panels act as critical scoring gates. They review proposed architectures and output a numerical score based on scalability, security, and maintainability.

| Normative ID | Keyword Constraint | Operational Directive for Expert Panels |
|---|---|---|
| SC.CMD.3.6 | MUST | Any architectural design document exceeding 1000 lines, or any module involving critical authentication infrastructure, MUST be evaluated by `/sc:spec-panel` prior to entering the implementation phase. |
| SC.CMD.3.7 | MUST NOT | If the spec-panel outputs a scoring gate value below the acceptable threshold (e.g., less than 7.0), implementation execution MUST NOT proceed, and the system MUST loop back to `/sc:brainstorm` for remediation. |

## §4 Aspect 4: Engineering Implementation Mechanics

The transition from theoretical planning to operational action involves the `/sc:implement` and `/sc:design` commands. This aspect defines the exact mechanics of how agents manipulate the repository file system, write code, and optimize their token expenditure.

### §4.1 Architectural Modeling and System Design (`/sc:design`)

The `/sc:design` command is utilized strictly for defining API contracts, establishing database schemas, and generating architectural blueprints. It precedes actual logic coding, ensuring that data structures are sound before state manipulation occurs.

| Normative ID | Keyword Constraint | Operational Directive for System Design |
|---|---|---|
| SC.CMD.4.1 | MUST | Complex relational data models MUST be thoroughly mapped using `/sc:design` before backend routing logic is constructed. |
| SC.CMD.4.2 | MAY | The command MAY utilize specific architectural flags such as `--ddd` (Domain-Driven Design) to forcefully enforce bounded contexts and specific architectural paradigms. |

### §4.2 Feature Implementation and Code Construction (`/sc:implement`)

The `/sc:implement` command embodies "The Developer" persona, responsible for writing production-ready code components that adhere strictly to security and quality standards. Because it alters system state and introduces potential vulnerabilities, its usage is heavily regulated by explicit syntax and MCP server integration.

When `/sc:implement` is called, it automatically invokes the Magic MCP server for UI component generation and the Context7 MCP server to validate implementation syntax against official framework documentation. This prevents the agent from hallucinating outdated library methods.

| Normative ID | Keyword Constraint | Operational Directive for Implementation |
|---|---|---|
| SC.CMD.4.3 | MUST | The syntax for execution MUST explicitly define the target, component type, and framework constraints (e.g., `/sc:implement user login form --type component --framework react --with-tests`). |
| SC.CMD.4.4 | MUST | To conserve tokens and eliminate processing latency on lightweight, isolated tasks, the agent MUST append the `--no-mcp` flag, disabling external server calls and preventing unintended side-effects. |
| SC.CMD.4.5 | SHOULD | When speed and operational efficiency are paramount, the `--lean` flag SHOULD be utilized to eliminate verbose explanatory output, focusing the agent entirely on delivering the raw code delta. |
| SC.CMD.4.6 | MUST | To enforce strict version control best practices, the `--git` flag MUST be appended to implementation commands to automatically stage and snapshot atomic changes as they are constructed. |

| Scenario ID | Gherkin Acceptance Criteria for Full-Stack Implementation |
|---|---|
| SC.CMD.4.A.1 | Given a validated, panel-approved specification for a JWT authentication module, When the agent executes `/sc:implement "user authentication with JWT and rate limiting"`, Then the system MUST deliver a complete implementation following OWASP security standards, automatically include unit tests, and MUST NOT halt to prompt the human user for intermediate, trivial sub-steps. |

### §4.3 Algorithmic Estimation (`/sc:estimate`)

Before allocating sprint capacity, project management requires operational baselines. The `/sc:estimate` command provides algorithmic time, effort, and complexity projections.

| Normative ID | Keyword Constraint | Operational Directive for Estimation |
|---|---|---|
| SC.CMD.4.7 | OPTIONAL | The orchestrator MAY invoke `/sc:estimate [target] --type time` (and similar). |

## §5 Aspect 5: Quality Assurance, Diagnostics, and Security Gating

Code generation is only half the lifecycle; relentless validation ensures survivability. Quality within the netzkontrast/agency ecosystem is strictly governed by the `/sc:analyze`, `/sc:test`, and `/sc:troubleshoot` commands. These commands are fundamentally destructive to bad logic; they do not construct new features but ensure existing implementations adhere to rigorous safety, performance, and formatting standards.

### §5.1 Static Code Analysis and Security Auditing (`/sc:analyze`)

The `/sc:analyze` command provides comprehensive audits of the existing codebase. It relies heavily on the Context7 and Sequential MCP servers to cross-reference local code against global vulnerability databases.

| Normative ID | Keyword Constraint | Operational Directive for Code Analysis |
|---|---|---|
| SC.CMD.5.1 | MUST | All newly implemented features MUST undergo an `/sc:analyze` pass prior to any merge operation. |
| SC.CMD.5.2 | MUST | The analysis invocation MUST explicitly specify a constrained focus area utilizing the `--focus` flag. Valid arguments are restricted to `quality`, `security`, `performance`, or `architecture`. |
| SC.CMD.5.3 | MUST | For deep security audits requiring advanced vulnerability deduction, the agent MUST append the `--think` or `--think-hard` flags to enable latent multi-step reasoning models, sacrificing speed for accuracy. |
| SC.CMD.5.4 | SHOULD | Output formats SHOULD be strictly controlled using the `--format text` (and similar) flag. |

| Scenario ID | Gherkin Acceptance Criteria for Security Audits |
|---|---|
| SC.CMD.5.A.1 | Given a newly committed data storage directory (`src/storage`), When the command `/sc:analyze src/storage --focus security --depth deep` is executed, Then the system MUST yield a structured vulnerability report detailing hardcoded keys, injection risks, and insecure SharedPreferences without altering the underlying code. |

### §5.2 Root-Cause Diagnostics and Troubleshooting (`/sc:troubleshoot`)

When automated test suites fail, continuous integration pipelines break, or regressions are reported, the `/sc:troubleshoot` command initiates a systematic root-cause diagnostic process. Unlike generic chatbots that immediately suggest destructive code changes based on error logs, this command forces a structured investigation.

| Normative ID | Keyword Constraint | Operational Directive for Diagnostics |
|---|---|---|
| SC.CMD.5.5 | MUST | By default, the `/sc:troubleshoot` command MUST operate in a strictly diagnostic, `--readonly` mode, preventing accidental modification of state. |
| SC.CMD.5.6 | MUST NOT | The system MUST NOT apply code patches automatically during a troubleshooting session unless the `--fix` flag is explicitly provided and subsequently confirmed by a human operator. |
| SC.CMD.5.7 | SHOULD | For complex environment variables, UI rendering issues, or CI container failures, the Chrome DevTools MCP server SHOULD be engaged to analyze live browser performance bottlenecks. |

| Scenario ID | Gherkin Acceptance Criteria for Diagnostic Halt |
|---|---|
| SC.CMD.5.A.2 | Given a backend API intermittently returning a 500 internal server error during load tests, When the agent invokes `/sc:troubleshoot "API returns 500 error on user login"`, Then it MUST output a ranked list of potential root causes, suggest remediation pathways, and MUST strictly halt execution before applying any patches. |

### §5.3 Automated Testing Suites (`/sc:test`)

The framework automates the generation of coverage suites to prevent regression.

| Normative ID | Keyword Constraint | Operational Directive for Testing Generation |
|---|---|---|
| SC.CMD.5.8 | MUST | The `/sc:test` command MUST dynamically integrate the Playwright MCP server when end-to-end (E2E) cross-browser testing generation is required. |
| SC.CMD.5.9 | MUST | The system MUST automatically generate unit, integration, and E2E coverage reports when `/sc:test --focus quality` is executed against a targeted component directory. |

## §6 Aspect 6: Task Validation, Pre-Commit Protocols, and Git Operations

Before any computational modification leaves the agent's localized workspace, it must pass through the reflection and version control gating mechanisms explicitly defined within the repository's `PRE_COMMIT.md` spec. This acts as the final firewall against contextual drift.

### §6.1 Semantic Task Reflection (`/sc:reflect`)

Reflection acts as the semantic validation layer. It guarantees that the physical code implemented matches the theoretical requirements demanded by the specification. The agent must step back and critique its own work.

| Normative ID | Keyword Constraint | Operational Directive for Task Reflection |
|---|---|---|
| SC.CMD.6.1 | MUST | Before checking off any node in the `TASK.md` queue as fully complete, the agent MUST execute `/sc:reflect --type task --analyze`. |
| SC.CMD.6.2 | MUST | The reflection algorithm MUST cross-reference the current implementation delta against the original PRD located in `PROMPT.md`, aggressively flagging any missing components, unhandled edge cases, or unchecked architectural assumptions. |

| Scenario ID | Gherkin Acceptance Criteria for Verification Gating |
|---|---|
| SC.CMD.6.A.1 | Given an agent concludes writing the logic for a designated feature, When it executes `/sc:reflect --validate` prior to commit, Then the system MUST compare the code against the `PRE_COMMIT.md` checklist and unconditionally block the commit action if mandatory constraints (e.g., missing unit tests) are absent. |

### §6.2 Version Control Operations (`/sc:git`)

| Normative ID | Keyword Constraint | Operational Directive for Git Mechanics |
|---|---|---|
| SC.CMD.6.3 | MUST | All codebase commits generated by autonomous systems MUST be processed through the `/sc:git` wrapper to ensure the generation of context-aware, highly structured "smart" commit messages. |

## §7 Aspect 7: Meta-Cognition, Friction Logging, and Continuous Learning

The most advanced and critical capability of the netzkontrast/agency implementation is its capacity for continuous self-improvement across sessions. Without meta-cognition, AI agents are doomed to repeat the same API integration failures and architectural missteps endlessly. The `FRUSTRATED.md` file tracks friction levels spanning from FL0 (minor annoyance) to FL3 (catastrophic blocking failure). The SuperClaude framework interfaces with this spec via specialized skills, notably the `sc-document` skill and the `ReflexionPattern` mechanism.

### §7.1 The Documentation and Reflexion Loop (`sc-document`)

The `sc-document` skill acts as the agent's meta-cognitive diary. It captures learnings, execution errors, and human corrections, storing them permanently. This eliminates recurring failure modes.

| Normative ID | Keyword Constraint | Operational Directive for Meta-Learning |
|---|---|---|
| SC.CMD.7.1 | MUST | The agent MUST invoke the `sc-document` skill automatically and immediately whenever any command or external operation fails unexpectedly (triggering a Friction Level 1 event). |
| SC.CMD.7.2 | MUST | If a human operator issues a hard correction via prompt (e.g., "No, that's wrong...", "Actually, the API changed..."), the system MUST log this delta in `FRUSTRATED.md` and synthesize the corrected approach into its persistent Serena memory to alter future behavior. |
| SC.CMD.7.3 | MUST | When the system mathematically recognizes its own internal knowledge or library assumptions are outdated, it MUST unconditionally halt execution, execute an `/sc:research` pass, and document the newly discovered paradigm. |

| Scenario ID | Gherkin Acceptance Criteria for Reflexive Error Correction |
|---|---|
| SC.CMD.7.A.1 | Given an external API integration attempt fails due to encountering an undocumented rate limit constraint, When the agent processes the HTTP 429 Too Many Requests response, Then it MUST immediately trigger the Reflexion pattern, update `FRUSTRATED.md` with the failure mode, and record the discovery of the rate limit to mathematically prevent future rapid, immediate retries in subsequent sessions. |

### §7.2 Confidence Checking Protocols (`confidence-check`)

An autonomous agent must possess the capacity to doubt its own competence. The internal `confidence.py` (ConfidenceChecker) skill serves this function.

| Normative ID | Keyword Constraint | Operational Directive for Confidence Gating |
|---|---|---|
| SC.CMD.7.4 | MUST | The `confidence-check` skill MUST execute silently prior to initiating any critical state changes or destructive refactoring. If the calculated confidence metric is low, the agent MUST pause execution, emit a warning, and request explicit human validation rather than hallucinating an implementation. |

### §7.3 Explanatory Generation (`/sc:explain` and `/sc:document`)

| Normative ID | Keyword Constraint | Operational Directive for Code Elucidation |
|---|---|---|
| SC.CMD.7.5 | MUST | The `/sc:document` command MUST be utilized to automatically generate formal, in-line code documentation and system architecture records based strictly on implemented, verifiable logic. |
| SC.CMD.7.6 | OPTIONAL | If a human developer struggles to comprehend an agent-generated module, they MAY invoke `/sc:explain`, optionally appending the `--explain` flag to trigger progressive disclosure and pedagogical breakdown of complex algorithmic paths. |

## §8 Aspect 8: The Nightly Maintenance Protocol and Refactoring

Software entropy is inevitable. The `MAINTENANCE.md` specification governs the continuous, automated upkeep of the repository. SuperClaude provides dedicated maintenance commands, primarily `/sc:improve`, `/sc:cleanup`, and `/sc:build`, to fulfill this mandate without consuming prime engineering hours.

### §8.1 Systemic Refactoring (`/sc:improve`)

As feature branches merge and architectural drift occurs, code smells manifest. The `/sc:improve` command is designed to realign codebase segments with the paradigms defined in `AGENTS.md`.

| Normative ID | Keyword Constraint | Operational Directive for Code Improvement |
|---|---|---|
| SC.CMD.8.1 | MUST | When structural code smells or deviations from style guidelines are identified during the nightly pass, the system MUST execute `/sc:improve` to generate formal refactoring suggestions. |
| SC.CMD.8.2 | MUST | The command MUST be permitted to auto-fix minor, safe, localized styling changes but MUST pause and prompt the human operator before initiating any widespread, risky, or logic-altering refactoring. |
| SC.CMD.8.3 | SHOULD | For large-scale, repository-wide, context-aware transformations, the orchestrator SHOULD engage the Morphllm-Fast-Apply MCP server, which is specifically optimized for massive codebase modifications. |

### §8.2 Dead Code Elimination (`/sc:cleanup`)

| Normative ID | Keyword Constraint | Operational Directive for Repository Hygiene |
|---|---|---|
| SC.CMD.8.4 | MUST | As an integral phase of the nightly maintenance protocol defined in `MAINTENANCE.md`, the system MUST execute `/sc:cleanup --scope module` to surgically remove dead code paths, prune unused imports, and eliminate stale or resolved TODO comments. |

### §8.3 Build Verification (`/sc:build`)

| Normative ID | Keyword Constraint | Operational Directive for Compilation |
|---|---|---|
| SC.CMD.8.5 | MUST | Following any maintenance sweep or cleanup operation, the system MUST execute `/sc:build` to verify that refactoring efforts have not broken compilation processes across any target variants (e.g., `devDebug`, `staging`). |

## §9 Summary Matrix of Governing Modifiers and Execution Flags

To ensure strict adherence to the meta-programming configuration framework, agents and human users alike MUST utilize the appropriate behavioral modifiers. Executing raw commands without flags leads to generalized, suboptimal outputs. The following matrix dictates flag compatibility, operational purpose, and integration mandates across the SuperClaude system:

| Execution Flag | Operational Purpose and Implication | Compatible Primary Commands |
|---|---|---|
| `--lean` | Ruthlessly eliminates verbosity, chatty explanations, and pedagogical output. Focuses the agent strictly on generating raw code deltas. Crucial for saving tokens. | `/sc:implement`, `/sc:improve`, `/sc:cleanup` |
| `--parallel` | Enables concurrent processing queues, allowing independent tasks to execute simultaneously across multiple isolated agent threads. | `/sc:spawn`, `/sc:task`, `/sc:workflow` |
| `--performance` | Explicitly biases the underlying LLM to optimize generated code architectures specifically for raw execution speed and computational efficiency over readability. | `/sc:analyze`, `/sc:implement`, `/sc:test` |
| `--readonly` | Restricts the execution command from modifying the physical file system state. Forces strict diagnostic, advisory mode. | `/sc:troubleshoot`, `/sc:analyze`, `/sc:reflect` |
| `--fix` | Bypasses read-only restrictions, empowering the agent to write patches directly to the file system. Demands mandatory human validation. | `/sc:troubleshoot` |
| `--think` | Activates deep, multi-step reasoning models (e.g., latent chain-of-thought) for complex deductive logic. Sacrifices execution speed for extreme accuracy. | `/sc:analyze`, `/sc:research` |
| `--delegate` | Bypasses general execution by forcing the `/sc:pm` orchestrator to assign highly specialized sub-agent personas to the target task. | `/sc:task` |
| `--no-mcp` | Explicitly disables all Model Context Protocol (MCP) server integrations, preventing unintended network calls, scraping, or side-effects during simple, isolated logic modifications. | All implementation execution commands |
| `--strategy` | Defines the workflow parsing methodology. Valid arguments dictate whether execution mimics systematic, agile, or enterprise rigor. | `/sc:spawn`, `/sc:workflow`, `/sc:task` |
| `--focus` | Constrains the context window to a specific domain array. Valid arguments include `quality`, `security`, `performance`, or `architecture`. | `/sc:analyze`, `/sc:test` |

## §10 Synthesis and Governance Enforcement

The architecture meticulously detailed within this specification creates a hermetically sealed, highly disciplined environment for AI-driven software engineering within the netzkontrast/agency ecosystem. By mapping the vast capabilities of the SuperClaude framework — encompassing its thirty specialized slash commands, eight distinct MCP servers, and numerous behavioral modification flags — directly to the physical markdown topography of the repository, the system achieves a level of deterministic output impossible in unstructured chat interfaces.

The strict, unyielding delineation between discovery parameters (`/sc:brainstorm`, `/sc:research`), task orchestration (`/sc:spawn`, `/sc:task`), and actual software implementation (`/sc:implement`, `/sc:improve`) prevents the catastrophic context-collapse that typically plagues long-running, autonomous agentic loops. An agent cannot write code it has not planned, and it cannot plan without first analyzing the environment. Furthermore, by mandating continuous meta-learning through the `sc-document` skill and `FRUSTRATED.md` friction logging, the system inherently hardens itself, evolving mathematical defenses against repeating systemic errors.

Any deviations from the workflows documented herein constitute a severe violation of repo-native governance. Examples of critical violations include attempting to implement feature code without a prior `/sc:spawn` Directed Acyclic Graph, circumventing the `/sc:analyze` security checkpoints prior to a merge, or manually disabling the Serena MCP server during long-running architectural shifts. All updates, modifications, or deprecations to this specification document MUST adhere to standard pull request protocols, undergo evaluation by the `/sc:spec-panel` with a scoring gate of 7.0 or higher, and pass all automated pre-commit hooks before being merged into the active governance baseline.