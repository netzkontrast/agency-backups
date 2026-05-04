# Worked Example — Spec-B: Claude Code

This is the second of three reference specs reproduced from the May 2026 research report on agentic-workflow best practices. It specifies a synchronous terminal-native coding agent — a meaningfully different system shape from Spec-A (Jules), which is asynchronous and cloud-isolated.

The example demonstrates:

- A **tighter §2** than Spec-A, including a hard quantitative limit (`B.2.2` — 200-line cap on context files)
- **Prohibition-heavy aspects** — Spec-B uses MUST NOT more often than Spec-A because the synchronous architecture surfaces specific anti-patterns the author wants to call out
- An aspect (Review) built around an **adversarial pattern** rather than an internal critic — same goal, different mechanism
- **Architectural §8 limitations** — limits that aren't just about scale but about fundamental design trade-offs

---

## Spec-B: Claude Code

### §0. Status & Provenance

**Status:** Mature (High Confidence)
**Last Review Date:** May 2, 2026
**Primary Sources:** Anthropic official documentation, Anthropic Engineering Blog, independent community repositories.

### §1. Normative Conventions

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in every produced Spec are to be interpreted as described in BCP 14 when, and only when, they appear in all capitals, as shown here.

### §2. System-Level Prompt Conventions

- B.2.1 — A terminal agent session MUST be invoked with an explicit working directory passed as an argument or set via the session context.
- B.2.2 — A project MUST limit its repository-level context file to a maximum of 200 lines to prevent instruction drift and context dilution.
- B.2.3 — A developer MUST utilize XML tags to structure prompts that contain mixed instructions, examples, and variable inputs.
- B.2.4 — A session SHOULD rely on manual context compaction via the terminal interface rather than waiting for automatic token exhaustion.
- B.2.5 — A developer MUST NOT duplicate standard language conventions or rigid linter rules inside the general context file.

### §3. Aspect 1 — Explore

#### §3.1 Normative Statements

- B.3.1 — An exploration prompt MUST execute within the dedicated planning mode to prevent unintended file modifications during discovery.
- B.3.2 — A developer SHOULD utilize isolated subagents to explore large log files or execute high-volume searches.
- B.3.3 — An exploration prompt MUST explicitly instruct the subagent to return only the summarized findings to the main orchestrator context.
- B.3.4 — A developer MUST NOT spawn a subagent for work that can be completed directly in a single context window.
- B.3.5 — An exploration prompt MAY pipe file contents directly into the command-line interface via standard bash commands.

#### §3.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: B.3.2
Feature: Safe Exploration using Subagents

  Scenario: Developer delegates log analysis to an isolated subagent
    Given the developer is in an active terminal agent session
    When the developer prompts the system to spawn a subagent to search through the last 50 error logs
    Then the system initializes an isolated subagent context
    And the subagent reads the logs without polluting the orchestrator's context window
    And the subagent returns a concise summary of the errors to the main session
```

#### §3.3 Rationale

Context management is the primary bottleneck in synchronous terminal agents. Exploring a codebase natively consumes massive amounts of tokens. By isolating exploration tasks to read-only subagents or using dedicated planning modes, the main orchestrator agent retains its reasoning capacity and token budget for the actual implementation work.

### §4. Aspect 2 — Plan / Develop Spec

#### §4.1 Normative Statements

- B.4.1 — A planning prompt MUST direct the system to create a step-by-step plan before writing any code.
- B.4.2 — A developer MUST review and explicitly approve the generated plan before transitioning the agent back to execution mode.
- B.4.3 — A planning prompt SHOULD instruct the agent to generate and store the execution steps in a local markdown file for persistence.
- B.4.4 — The agent MUST base its planning phase on the architectural constraints defined within the repository's primary context file.
- B.4.5 — A developer MUST NOT micromanage specific reasoning paths; instead, they should ask the agent to reason thoroughly via dedicated thinking tags.

#### §4.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: B.4.1
Feature: Plan Mode Workflow

  Scenario: The agent generates a plan before implementation
    Given the user invokes the terminal agent and switches to the planning mode
    When the user prompts the system to draft a plan to migrate authentication protocols
    Then the agent analyzes the codebase
    And the agent outputs a numbered list of planned steps
    And the agent does not execute any file write operations
```

#### §4.3 Rationale

Because this terminal-native agent has immediate access to the filesystem and shell environments, jumping straight to implementation frequently results in correct syntax applied to the wrong architectural solution. Mandating a distinct planning step ensures that human oversight occurs before the agent executes potentially destructive or complex terminal commands.

### §5. Aspect 3 — Implement / Execute

#### §5.1 Normative Statements

- B.5.1 — An implementation prompt MUST define the specific output tools or external server connections the agent is permitted to use.
- B.5.2 — A developer MUST utilize lifecycle hooks to enforce deterministic quality gates after file modifications occur.
- B.5.3 — An execution prompt SHOULD chain complex instructions using sequential application programming interface calls if intermediate outputs require inspection.
- B.5.4 — The agent MUST execute tasks conforming to the strict formatting guidelines outlined via custom command structures if invoked.
- B.5.5 — A developer MUST NOT embed long tutorials or exhaustive framework documentation in the execution prompt.

#### §5.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: B.5.2
Feature: Deterministic Execution via Hooks

  Scenario: A hook intercepts a file write to run a linter
    Given a project has a pre-execution hook configured for formatting
    When the terminal agent attempts to save a new source file
    Then the hook intercepts the action
    And the hook executes the project's linter
    And the file is only saved if the linter passes successfully
```

#### §5.3 Rationale

While large language models excel at fluid reasoning, they occasionally fail at rigid deterministic formatting. By offloading deterministic constraints to execution hooks, developers guarantee that the generated code matches project standards without expending prompt tokens. Utilizing external server protocols and well-scoped prompt tags limits hallucination and bounds the agent's action space safely.

### §6. Aspect 4 — Review

#### §6.1 Normative Statements

- B.6.1 — A review prompt MUST establish an adversarial review pattern where a separate instance explicitly attempts to find flaws in the generated code.
- B.6.2 — The review instance MUST evaluate the code against the anti-patterns listed in the repository's context file.
- B.6.3 — A review prompt SHOULD request the agent to quote relevant portions of the codebase using specific tags before providing its critique.
- B.6.4 — A developer MUST NOT accept an agent's claim that a refactoring will function correctly without verified test outputs.
- B.6.5 — A review task MAY be encapsulated into a custom alias command for repeatable and standardized execution.

#### §6.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: B.6.1
Feature: Adversarial Review Pattern

  Scenario: A secondary instance reviews a newly implemented feature
    Given the primary instance has completed coding a new application programming interface endpoint
    When the developer prompts a new isolated instance to act as an adversarial security reviewer
    Then the reviewing instance analyzes the endpoint independently
    And the reviewing instance produces a comprehensive vulnerability report
```

#### §6.3 Rationale

Generative models suffer from inherent confirmation bias regarding their own outputs. An agent that recently authored a specific module is highly likely to declare it correct upon review. Spawning a fresh context window or a dedicated subagent with an adversarial prompt breaks this bias, forcing the model to re-evaluate the code from a highly critical perspective.

### §7. Aspect 5 — Validate / Verify

#### §7.1 Normative Statements

- B.7.1 — A validation prompt MUST require the agent to run the project's test suite natively in the terminal and parse the output.
- B.7.2 — An agent MUST NOT mark a user interface implementation task as complete without verifying it visually via browser automation tools.
- B.7.3 — A validation prompt SHOULD instruct the agent to address the root cause of an error rather than suppressing the specific symptom.
- B.7.4 — A developer MUST provide a minimal, reproducible example if the agent fails to validate the code after multiple automated attempts.
- B.7.5 — The agent MUST utilize a comparative verification pattern by executing a diff against the primary branch to verify its logic.

#### §7.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: B.7.1
Feature: Evidence-Based Validation

  Scenario: The agent verifies an implementation by running tests
    Given the agent has finished refactoring a utility function
    When the developer prompts the system to verify the implementation
    Then the agent executes the standard test command in the terminal
    And the agent reads the standard output stream
    And the agent only reports success if all tests pass without errors
```

#### §7.3 Rationale

The methodology of evidence-based completion is paramount in agentic engineering. Agents will frequently hallucinate successful completion if not strictly forced to observe actual terminal output. Mandating that the agent interact directly with test runners, linters, or visual diff tools ensures that the artificial intelligence's assertions of correctness are grounded in empirical, machine-verified evidence rather than predictive text generation.

### §8. Known Limitations & Open Questions

- The system's performance degrades sharply if the repository context file exceeds maximum recommended limits due to severe attention dilution.
- Subagent orchestration can occasionally lead to infinite feedback loops if hand-off parameters and termination conditions are not rigidly defined.
- Native multi-agent orchestration across independent terminal sessions remains architecturally complex and prone to synchronization issues.

### §9. Source Index

1. Anthropic Claude Code official documentation
2. Anthropic Engineering Blog: "Effective Context Engineering for AI Agents"
3. "The Complete Guide to Building Skills for Claude" (Anthropic PDF)
4. GitHub open-source specification for AGENTS.md
5. ETH Zurich research paper: "Evaluating AGENTS.md" (Feb 2026)

---

## What this example adds beyond Spec-A

- **Quantitative constraint in §2.** `B.2.2` ("max 200 lines") is a hard number, not a vague "keep it short". This is appropriate when the system has a measurable failure threshold. Use quantitative MUSTs sparingly — they age fast — but when the evidence supports them, write the number.
- **Subagent discipline as a paired pattern.** `B.3.2` (SHOULD spawn subagents for heavy exploration) is paired with `B.3.4` (MUST NOT spawn for trivial work). The pair captures the real trade-off: subagents are powerful but have setup cost. A spec that only said `B.3.2` without `B.3.4` would push users toward over-orchestration.
- **Adversarial review as a different mechanism.** Spec-A §6 uses an *internal critic* that ships with the system. Spec-B §6 uses an *adversarial instance* the developer explicitly spawns. Both achieve "second pair of eyes"; the spec records the mechanism the system actually exposes.
- **Visual validation explicitly required.** `B.7.2` calls out a specific failure mode (claiming UI work is done without seeing it render). When you've watched a class of agents repeatedly skip something, write the prohibition by name.
- **§8 names architectural limits.** Spec-B's §8 doesn't just list scale issues — it names "subagent orchestration can lead to infinite loops" and "multi-agent across sessions remains complex". These aren't bugs; they're properties of the design. A spec that hides them oversells the system.

When generating a similar spec for any synchronous, terminal-resident, single-developer agent, this is the structure to model.
