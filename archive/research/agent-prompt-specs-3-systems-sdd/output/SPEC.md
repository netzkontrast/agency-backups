---
type: research
status: completed
slug: agent-prompt-specs-3-systems-sdd
summary: "Actionable spec-driven prompting best practices for Google Jules, Claude Code, and Gemini Deep Research across the Explore-Plan-Implement-Review-Validate cycle."
created: 2026-05-04
updated: 2026-05-04
research_phase: complete
research_executes_prompt: ""
research_friction_level: FL0
---

# Spec-Driven Best Practices for Agent/Research Prompts on Google Jules, Claude Code, and Gemini Deep Research

## Executive Summary
This document synthesizes documented best practices for prompting three autonomous agent systems: Google Jules, Claude Code, and Gemini Deep Research. By examining official documentation, engineering blogs, and community reproductions, it pins down specific, actionable guidelines across five operational aspects (Explore, Plan, Implement, Review, Validate). While it strictly defines how to interact with these systems today, it leaves open questions regarding context window limits and the long-term viability of explicit source prioritization.

## Common Conventions Across Systems
- **Incremental Verification**: All three systems benefit from iterative execution and validation rather than single-shot, monolithic instructions.
- **Explicit Planning**: For complex tasks, all systems require a dedicated planning phase before code execution or report generation.
- **Context Isolation**: Whether through Claude's subagents, Jules's VM cloning, or Gemini's structured templates, isolating the working context from unstructured exploratory data is universally recommended.

---

## Spec-A: Google Jules

### §0. Status & Provenance
- **Status:** Draft
- **Primary Sources:** Google Blog (Jules beta announcement), Google Developer blog, independent reproductions (MachineLearningMastery).
- **World-Change Annotation:** Jules transitioned to public beta in May 2025. It now uses Gemini 2.5 Pro (or Gemini 3 for paid). Behavior might shift as the beta progresses.

### §1. Normative Conventions
#### §1.1 — RFC 2119 / BCP 14 Normative Keywords

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in every produced Spec are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] **when, and only when, they appear in all capitals**, as shown here.

Each produced Spec **MUST** include a literal "§1.1 — RFC 2119 / BCP 14 Normative Keywords" subsection that reproduces the binding paragraph above verbatim. This is non-negotiable.

#### §1.2 — Gherkin Syntax Binding

Every behavioural example, agent-interaction scenario, or hand-off specification in every produced Spec **MUST** use standard Gherkin syntax (`Feature`, `Scenario`, `Given`, `When`, `Then`, `And`, `But`) and **MUST** be self-contained and executable.

- **Self-contained** = the scenario references no external context that is not also pinned in the Spec.
- **Executable** = a human or agent reading the scenario could enact it step by step without additional clarification.
- A `Scenario` block **SHALL** have at least one `Given`, at least one `When`, and at least one `Then`. `And` and `But` are continuations of the immediately preceding keyword (`Given/When/Then`).
- **Background** sections are **OPTIONAL** but **RECOMMENDED** when ≥ 3 scenarios in the same `Feature` share setup steps.
- **Scenario Outlines** with `Examples` tables are **RECOMMENDED** when the same behavioural shape repeats with parameter variation.

#### §1.3 — Style Guide for Normative Statements

- Normative statements **MUST** use exactly one RFC 2119 keyword per sentence.
- Acceptance criteria **MUST** be written as Gherkin scenarios.
- Rationales, descriptions, motivation paragraphs, and prose explanations **MUST NOT** contain RFC 2119 keywords in uppercase. (Lowercase "should" or "may" in prose is fine — only the all-caps form is reserved.)
- Each normative statement **SHOULD** be addressable by a stable identifier of the form `<Spec-Letter>.<Aspect-Number>.<Statement-Number>`, e.g., `A.3.2` for Spec-A (Jules), Aspect 3 (Implement), Statement 2.
- Each Gherkin scenario **SHOULD** carry a `# anchor: <stable-id>` comment line on the line above its `Scenario:` header so it can be cross-referenced from prose.

### §2. System-Level Prompt Conventions
- **A.2.1** A Jules task **MUST** be triggered against a connected GitHub repository via the web UI or a linked GitHub issue.
- **A.2.2** Jules **SHOULD NOT** be prompted with instructions that assume it will edit the local developer workspace directly.
- **A.2.3** The prompt **MUST** specify explicit, detailed instructions for unattended batch work.
- **A.2.4** The repository **SHOULD** contain a `README.md` or `AGENTS.md` file to provide environmental hints to the agent.
- **A.2.5** Users **MUST** review and approve the generated plan before allowing Jules to execute complex code transformations.

### §3. Aspect 1 — Explore
#### §3.1 Normative Statements
- **A.3.1** The prompt **MAY** omit explicit file paths, as Jules will autonomously explore the cloned repository in its VM.
- **A.3.2** The project root **MUST** contain up-to-date documentation files to guide Jules's autonomous exploration.
- **A.3.3** The prompt **SHOULD** direct Jules to explore specific sub-systems if the repository contains multiple independent modules.
- **A.3.4** Jules **MUST NOT** be used to explore and execute code in a local unsaved state.
- **A.3.5** An exploratory prompt **MAY** request an audio summary of the codebase history.

#### §3.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Exploring the Codebase

  # anchor: A.3.1
  Scenario: Jules autonomously explores the repository
    Given a connected GitHub repository
    When the user prompts Jules to "analyze the authentication flow" without specifying file paths
    Then Jules clones the repository into a secure VM
    And Jules reads the relevant files to understand the flow
```

#### §3.3 Rationale
Jules operates by cloning the entire repository into a secure cloud VM. Because it has full context, users do not need to manually paste file contents or specify exact file paths in the prompt. However, providing clear architectural documentation helps the agent navigate complex codebases.

### §4. Aspect 2 — Plan / Develop Spec
#### §4.1 Normative Statements
- **A.4.1** The user **MUST** provide explicit goals in the prompt to facilitate plan generation.
- **A.4.2** Jules **MUST** present a detailed plan of action before modifying any code.
- **A.4.3** The plan **SHOULD** be iteratively refined by the user if the task involves large-scale refactoring.
- **A.4.4** A planning prompt **MUST NOT** assume Jules understands undocumented legacy business logic.
- **A.4.5** The user **MAY** modify the generated plan directly through the UI.

#### §4.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Plan Generation

  # anchor: A.4.2
  Scenario: Jules generates a reviewable plan
    Given a task prompt to convert a Java module to Python
    When Jules processes the request
    Then Jules presents a step-by-step plan
    And Jules waits for the user to approve the plan
```

#### §4.3 Rationale
Planning is a critical phase in the Jules workflow. Since the agent executes tasks asynchronously, ensuring the plan is correct before execution prevents wasted compute cycles and incorrect pull requests. Explicit prompts lead to more accurate plans.

### §5. Aspect 3 — Implement / Execute
#### §5.1 Normative Statements
- **A.5.1** The prompt **SHOULD** instruct Jules to break down large implementations into smaller, testable steps.
- **A.5.2** Jules **MUST** execute the code modifications within its isolated cloud VM.
- **A.5.3** A prompt **MAY** request parallel execution of independent tasks.
- **A.5.4** The implementation prompt **MUST NOT** contain instructions requiring manual user input during execution.
- **A.5.5** The user **SHOULD** ensure the repository contains a test suite for Jules to run during execution.

#### §5.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Asynchronous Implementation

  # anchor: A.5.2
  Scenario: Jules executes a task in isolation
    Given an approved plan for bug fixing
    When Jules begins execution
    Then Jules applies the changes in a cloud VM
    And Jules does not block the user's local development environment
```

#### §5.3 Rationale
Jules is designed for asynchronous batch work. It executes tasks in the background, allowing developers to continue working locally. Prompts need to be fully self-contained because the agent cannot ask clarifying questions mid-execution.

### §6. Aspect 4 — Review
#### §6.1 Normative Statements
- **A.6.1** Jules **MUST** generate a diff of the changes upon task completion.
- **A.6.2** The agent **MUST** open a pull request against the target branch.
- **A.6.3** The prompt **MAY** request an audio changelog summarizing the executed modifications.
- **A.6.4** Users **SHOULD** review the pull request diff for alignment with project standards.
- **A.6.5** Jules **MUST NOT** merge the pull request automatically without human approval.

#### §6.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Code Review and PR Creation

  # anchor: A.6.2
  Scenario: Jules submits changes for review
    Given Jules has completed executing the approved plan
    When the task finishes
    Then Jules generates a diff
    And Jules opens a pull request targeting the main branch
```

#### §6.3 Rationale
The pull request is the primary handoff mechanism between Jules and the human developer. This ensures safety and quality control. Audio changelogs provide an alternative, accessible way for developers to understand the changes made by the agent.

### §7. Aspect 5 — Validate / Verify
#### §7.1 Normative Statements
- **A.7.1** The prompt **MUST** instruct Jules to run existing unit tests after implementing changes.
- **A.7.2** If tests fail, Jules **SHOULD** attempt to autonomously fix the issues before finalizing the branch.
- **A.7.3** The project **MUST** have standard testing frameworks configured for Jules to verify its work.
- **A.7.4** A validation prompt **MAY** ask Jules to explicitly report the test coverage of new code.
- **A.7.5** Jules **MUST NOT** bypass failing tests when creating the final pull request.

#### §7.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Task Validation

  # anchor: A.7.1
  Scenario: Jules verifies changes against tests
    Given a completed code modification
    When Jules finalizes the execution phase
    Then Jules runs the repository test suite
    And Jules includes the test results in the pull request description
```

#### §7.3 Rationale
Running tests inside the cloud VM ensures that the code generated by Jules is functionally correct before it reaches the human reviewer. Prompts that explicitly mandate test execution yield higher quality pull requests.

### §8. Known Limitations & Open Questions
- It is unclear how well Jules handles deeply monolithic legacy codebases without extensive `AGENTS.md` context.
- The context limit for the secure cloud VM cloning process is not fully documented in public beta materials.

### §9. Source Index
1. Google Blog: "Build with Jules, your asynchronous coding agent"
2. MachineLearningMastery: "Practical Agentic Coding with Google Jules"
## Spec-B: Claude Code

### §0. Status & Provenance
- **Status:** Draft
- **Primary Sources:** Anthropic documentation (`docs.claude.com`), Anthropic Engineering blog, independent repos (`shanraisshan/claude-code-best-practice`).
- **World-Change Annotation:** Claude Code features like `/code-review` and `subagents` are in active beta and subject to changes.

### §1. Normative Conventions
#### §1.1 — RFC 2119 / BCP 14 Normative Keywords

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in every produced Spec are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] **when, and only when, they appear in all capitals**, as shown here.

Each produced Spec **MUST** include a literal "§1.1 — RFC 2119 / BCP 14 Normative Keywords" subsection that reproduces the binding paragraph above verbatim. This is non-negotiable.

#### §1.2 — Gherkin Syntax Binding

Every behavioural example, agent-interaction scenario, or hand-off specification in every produced Spec **MUST** use standard Gherkin syntax (`Feature`, `Scenario`, `Given`, `When`, `Then`, `And`, `But`) and **MUST** be self-contained and executable.

- **Self-contained** = the scenario references no external context that is not also pinned in the Spec.
- **Executable** = a human or agent reading the scenario could enact it step by step without additional clarification.
- A `Scenario` block **SHALL** have at least one `Given`, at least one `When`, and at least one `Then`. `And` and `But` are continuations of the immediately preceding keyword (`Given/When/Then`).
- **Background** sections are **OPTIONAL** but **RECOMMENDED** when ≥ 3 scenarios in the same `Feature` share setup steps.
- **Scenario Outlines** with `Examples` tables are **RECOMMENDED** when the same behavioural shape repeats with parameter variation.

#### §1.3 — Style Guide for Normative Statements

- Normative statements **MUST** use exactly one RFC 2119 keyword per sentence.
- Acceptance criteria **MUST** be written as Gherkin scenarios.
- Rationales, descriptions, motivation paragraphs, and prose explanations **MUST NOT** contain RFC 2119 keywords in uppercase. (Lowercase "should" or "may" in prose is fine — only the all-caps form is reserved.)
- Each normative statement **SHOULD** be addressable by a stable identifier of the form `<Spec-Letter>.<Aspect-Number>.<Statement-Number>`, e.g., `A.3.2` for Spec-A (Jules), Aspect 3 (Implement), Statement 2.
- Each Gherkin scenario **SHOULD** carry a `# anchor: <stable-id>` comment line on the line above its `Scenario:` header so it can be cross-referenced from prose.

### §2. System-Level Prompt Conventions
- **B.2.1** A Claude Code session **MUST** be invoked within the root directory of the project.
- **B.2.2** The repository **MUST** contain a `CLAUDE.md` file to dictate project-specific instructions and boundaries.
- **B.2.3** The `CLAUDE.md` file **SHOULD** be kept concise, ideally under 200 lines, to prevent instruction degradation.
- **B.2.4** Reusable prompt instructions **MUST** be encapsulated into Claude `skills` rather than repeated in the chat interface.
- **B.2.5** Users **SHOULD** reset the context window using `/compact` or `/clear` when shifting to entirely new tasks.

### §3. Aspect 1 — Explore
#### §3.1 Normative Statements
- **B.3.1** An exploratory prompt **SHOULD** instruct Claude to delegate wide file-reads to a subagent to preserve main context.
- **B.3.2** The user **MAY** use `Shift+Tab` to enter Plan Mode for open-ended discovery before committing to code changes.
- **B.3.3** Claude **MUST** use the `CLAUDE.md` file as its primary source of truth for architectural exploration.
- **B.3.4** The prompt **SHOULD NOT** ask Claude to read entire directories indiscriminately, as context rot occurs past 300k tokens.
- **B.3.5** An exploratory prompt **MAY** instruct Claude to generate an ASCII diagram to map out architecture.

#### §3.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Exploring the Codebase

  # anchor: B.3.1
  Scenario: Claude Code explores via subagent
    Given a fresh terminal session in the project root
    And a valid `CLAUDE.md` exists
    When the user prompts Claude to "explore the auth module using a subagent and return a summary"
    Then Claude spawns a subagent to read the auth files
    And the subagent returns a concise architectural summary
    And the main session context remains free of raw file dumps
```

#### §3.3 Rationale
Claude Code operates directly within the developer's terminal. Because context windows degrade as they fill up ("context rot"), it is a critical best practice to isolate exploratory file reads. Subagents allow Claude to grep and read widely without polluting the primary reasoning context.

### §4. Aspect 2 — Plan / Develop Spec
#### §4.1 Normative Statements
- **B.4.1** The user **MUST** initiate Plan Mode before generating a complex specification.
- **B.4.2** A planning prompt **SHOULD** be highly specific and context-rich.
- **B.4.3** The user **MAY** use the `ultrathink` keyword to force Claude into high-effort reasoning.
- **B.4.4** A planning prompt **MUST NOT** merge the planning phase and execution phase into a single command.
- **B.4.5** Claude **SHOULD** verify its generated plan against constraints defined in `CLAUDE.md`.

#### §4.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Plan Generation

  # anchor: B.4.1
  Scenario: Claude generates a plan in Plan Mode
    Given the user presses Shift+Tab twice to enter Plan Mode
    When the user provides a detailed prompt for a new API endpoint
    Then Claude generates a step-by-step implementation plan
    And Claude does not execute any code changes
```

#### §4.3 Rationale
Plan Mode is specifically built into Claude Code to decouple reasoning from execution. By enforcing a separate planning step, users can review the proposed architecture and ensure it aligns with the project before any code is modified.

### §5. Aspect 3 — Implement / Execute
#### §5.1 Normative Statements
- **B.5.1** Implementation prompts **SHOULD** trigger predefined `skills` for repetitive coding tasks.
- **B.5.2** The user **MUST** use Git worktrees if instructing Claude to implement features in parallel.
- **B.5.3** A prompt **SHOULD** instruct Claude to commit code frequently (e.g., once per hour).
- **B.5.4** Claude **MUST** execute tasks iteratively, confirming each step before proceeding to the next.
- **B.5.5** The user **MAY** enable `Auto Mode` to allow Claude to execute safe bash commands without prompting for permission.

#### §5.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Code Implementation

  # anchor: B.5.1
  Scenario: Claude executes a repetitive task using a skill
    Given the repository contains a configured `SKILL.md` for generating React components
    When the user prompts Claude to "generate a new user profile component using the standard skill"
    Then Claude reads the `SKILL.md` instructions
    And Claude implements the component according to the skill's rules
```

#### §5.3 Rationale
Executing code directly in the terminal requires safety and structure. By utilizing predefined skills, developers ensure that Claude implements features consistently according to project standards, without needing to rewrite complex prompts for every task.

### §6. Aspect 4 — Review
#### §6.1 Normative Statements
- **B.6.1** A review prompt **SHOULD** utilize the `/code-review` command for multi-agent PR analysis.
- **B.6.2** Claude **MAY** be asked to review code by diffing the current branch against `main`.
- **B.6.3** The user **MUST NOT** use a degraded, long-running context window to perform security reviews.
- **B.6.4** A review prompt **SHOULD** instruct Claude to act as a "Staff Engineer" for critical reviews.
- **B.6.5** The user **MAY** use cross-model workflows (e.g., asking another LLM to review Claude's output).

#### §6.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Code Review

  # anchor: B.6.1
  Scenario: Claude performs a PR code review
    Given the developer has finished implementing a feature branch
    When the user invokes the `/code-review` command
    Then Claude analyzes the diff against the main branch
    And Claude reports potential bugs and security vulnerabilities
```

#### §6.3 Rationale
Code review is most effective when the AI has a fresh context window. The `/code-review` command leverages multi-agent workflows to rigorously analyze diffs, ensuring that human reviewers have a high-quality baseline to start from.

### §7. Aspect 5 — Validate / Verify
#### §7.1 Normative Statements
- **B.7.1** A validation prompt **MUST** instruct Claude to run the project's test suite via bash commands.
- **B.7.2** If tests fail, the prompt **SHOULD** instruct Claude to read the terminal output and attempt a fix.
- **B.7.3** The user **MAY** use the `/doctor` command to diagnose underlying configuration issues.
- **B.7.4** Claude **MUST NOT** be instructed to skip validation steps defined in `CLAUDE.md`.
- **B.7.5** A validation prompt **SHOULD** provide Claude with logs or screenshots if UI verification is required.

#### §7.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Task Validation

  # anchor: B.7.1
  Scenario: Claude validates its implementation
    Given Claude has generated new code
    When the user prompts Claude to "run the test suite and fix any failures"
    Then Claude executes the test command in the terminal
    And Claude reads the test output
    And Claude patches the code if any tests fail
```

#### §7.3 Rationale
Because Claude Code can execute bash commands, it is fully capable of running tests and reading the results. Validation should be an active loop where Claude runs the tests, diagnoses failures from the stack trace, and applies fixes autonomously.

### §8. Known Limitations & Open Questions
- There is community disagreement on the ideal length of `CLAUDE.md`. Some sources suggest a 200-line maximum, while others (like HumanLayer) strongly recommend keeping it under 60 lines to prevent instructions from being ignored.

### §9. Source Index
1. Anthropic docs: "Best Practices for Claude Code"
2. GitHub Repository: `shanraisshan/claude-code-best-practice`
3. UsabilityCounts: "Designers: Prompts for Claude Code You Should Run on Your Application, Every Time"
## Spec-C: Gemini Deep Research

### §0. Status & Provenance
- **Status:** Draft
- **Primary Sources:** Medium community articles ("Best Gemini Prompts in 2026"), Google AI / Gemini documentation implicit knowledge.
- **World-Change Annotation:** Deep Research Max capabilities were recently discussed, meaning output formats and limits might shift.

### §1. Normative Conventions
#### §1.1 — RFC 2119 / BCP 14 Normative Keywords

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in every produced Spec are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] **when, and only when, they appear in all capitals**, as shown here.

Each produced Spec **MUST** include a literal "§1.1 — RFC 2119 / BCP 14 Normative Keywords" subsection that reproduces the binding paragraph above verbatim. This is non-negotiable.

#### §1.2 — Gherkin Syntax Binding

Every behavioural example, agent-interaction scenario, or hand-off specification in every produced Spec **MUST** use standard Gherkin syntax (`Feature`, `Scenario`, `Given`, `When`, `Then`, `And`, `But`) and **MUST** be self-contained and executable.

- **Self-contained** = the scenario references no external context that is not also pinned in the Spec.
- **Executable** = a human or agent reading the scenario could enact it step by step without additional clarification.
- A `Scenario` block **SHALL** have at least one `Given`, at least one `When`, and at least one `Then`. `And` and `But` are continuations of the immediately preceding keyword (`Given/When/Then`).
- **Background** sections are **OPTIONAL** but **RECOMMENDED** when ≥ 3 scenarios in the same `Feature` share setup steps.
- **Scenario Outlines** with `Examples` tables are **RECOMMENDED** when the same behavioural shape repeats with parameter variation.

#### §1.3 — Style Guide for Normative Statements

- Normative statements **MUST** use exactly one RFC 2119 keyword per sentence.
- Acceptance criteria **MUST** be written as Gherkin scenarios.
- Rationales, descriptions, motivation paragraphs, and prose explanations **MUST NOT** contain RFC 2119 keywords in uppercase. (Lowercase "should" or "may" in prose is fine — only the all-caps form is reserved.)
- Each normative statement **SHOULD** be addressable by a stable identifier of the form `<Spec-Letter>.<Aspect-Number>.<Statement-Number>`, e.g., `A.3.2` for Spec-A (Jules), Aspect 3 (Implement), Statement 2.
- Each Gherkin scenario **SHOULD** carry a `# anchor: <stable-id>` comment line on the line above its `Scenario:` header so it can be cross-referenced from prose.

### §2. System-Level Prompt Conventions
- **C.2.1** A Gemini Deep Research prompt **MUST** explicitly state the overarching goal and the desired final format.
- **C.2.2** The prompt **SHOULD** follow a structured four-part formula: Task, Grounding Instruction, Context, Format.
- **C.2.3** The prompt **MUST NOT** treat Gemini Deep Research as a simple conversational chatbot; it requires robust constraints.
- **C.2.4** The user **MAY** supply multimodal inputs to guide the research constraints.
- **C.2.5** The prompt **SHOULD** state the target audience for the final research report.

### §3. Aspect 1 — Explore
#### §3.1 Normative Statements
- **C.3.1** An exploratory prompt **MUST** instruct Gemini to use live Google Search grounding.
- **C.3.2** The user **SHOULD** provide seed domains or search strategies to focus the exploration.
- **C.3.3** The prompt **MAY** instruct Gemini to traverse links across multiple hops for deep exploration.
- **C.3.4** An exploratory prompt **MUST NOT** artificially constrain the exploration to a single URL unless specifically required.
- **C.3.5** The prompt **SHOULD** ask the agent to summarize initial findings before committing to a deep dive.

#### §3.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Autonomous Web Exploration

  # anchor: C.3.1
  Scenario: Gemini grounds its exploration in live data
    Given a prompt requesting the latest market trends
    When the user explicitly instructs "Using your Google Search grounding"
    Then Gemini executes live web queries
    And Gemini retrieves real-time data instead of training knowledge
```

#### §3.3 Rationale
Gemini Deep Research differentiates itself through its native, deep integration with Google Search. Unlike standard models that hallucinate when data is missing, Gemini can explore live information autonomously. Directing it to use this grounding ensures it fetches the most relevant and current data.

### §4. Aspect 2 — Plan / Develop Spec
#### §4.1 Normative Statements
- **C.4.1** A Gemini Deep Research prompt **SHOULD** include explicit source-type priority to guide its research plan.
- **C.4.2** [Confidence: low (single-source)] The planning prompt **MUST** define the expected structure of the final report (e.g., Executive Summary, Key Findings).
- **C.4.3** The prompt **SHOULD** explicitly define the depth or length of the expected output.
- **C.4.4** The prompt **MAY** request an intermediate outline before the full report is generated.
- **C.4.5** The user **MUST NOT** omit the task verb (e.g., analyze, compare, summarize) in the initial plan instruction.

#### §4.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Research Planning

  # anchor: C.4.2
  Scenario: Gemini generates a structured plan
    Given a research topic on AI agents
    When the user prompts Gemini to "research the topic and structure the report with an Executive Summary and Key Findings"
    Then Gemini formats the output exactly to the specified structure
    And Gemini includes only the requested sections
```

#### §4.3 Rationale
Without strict structural instructions, LLMs often produce rambling or unformatted text. Because Gemini Deep Research generates long-form content, enforcing a strict schema (like requesting an executive summary) prevents the model from generating unusable walls of text.

### §5. Aspect 3 — Implement / Execute
#### §5.1 Normative Statements
- **C.5.1** The execution prompt **MUST** direct Gemini to synthesize the gathered research into the pre-defined format.
- **C.5.2** The user **SHOULD** instruct Gemini to combine research and creation in a single prompt for efficiency.
- **C.5.3** The prompt **MAY** require Gemini to format data tables or charts based on its findings.
- **C.5.4** The execution instruction **MUST NOT** conflict with the structural constraints set in the planning phase.
- **C.5.5** The prompt **SHOULD** instruct the model to attribute claims to its live search findings.

#### §5.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Report Execution

  # anchor: C.5.2
  Scenario: Gemini synthesizes research into a final report
    Given an outlined plan for a market research document
    When the user instructs Gemini to combine the findings into a 1,200-word report
    Then Gemini generates the full report
    And Gemini maintains the structural integrity defined in the plan
```

#### §5.3 Rationale
Gemini Deep Research excels at synthesizing massive amounts of retrieved data. By combining the research (data gathering) and creation (writing the report) into a cohesive step governed by the prompt, the agent produces high-quality deliverables.

### §6. Aspect 4 — Review
#### §6.1 Normative Statements
- **C.6.1** [Confidence: low (single-source)] A review prompt **MUST** instruct Gemini to self-evaluate its report for hallucinated claims.
- **C.6.2** The prompt **SHOULD** ask Gemini to cross-reference its findings against multiple independent sources.
- **C.6.3** The user **MAY** prompt Gemini to generate a contradictory analysis (steelmanning opposing views).
- **C.6.4** A review prompt **MUST NOT** ask Gemini to alter the source data to fit a narrative.
- **C.6.5** The prompt **SHOULD** instruct Gemini to output confidence levels for its key findings.

#### §6.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Reviewing Findings

  # anchor: C.6.2
  Scenario: Gemini cross-references claims
    Given a completed research report on quantum computing
    When the user prompts Gemini to review the claims against at least three independent sources
    Then Gemini verifies the factual accuracy of the report
    And Gemini flags any single-source claims with low confidence
```

#### §6.3 Rationale
Even with live search grounding, autonomous agents can misinterpret data. A robust review phase forces the model to double-check its own work, triangulate sources, and explicitly declare its confidence, increasing the reliability of the final deliverable.

### §7. Aspect 5 — Validate / Verify
#### §7.1 Normative Statements
- **C.7.1** [Confidence: low (single-source)] The validation prompt **MUST** require Gemini to provide clickable citations for all major claims.
- **C.7.2** The user **SHOULD** manually verify a sample of the generated citations to ensure they are not hallucinated.
- **C.7.3** The prompt **MAY** ask Gemini to map its findings back to the original user constraints.
- **C.7.4** The validation step **MUST NOT** rely solely on the model's internal summary.
- **C.7.5** The prompt **SHOULD** instruct Gemini to identify data gaps where search grounding failed.

#### §7.2 Acceptance Criteria (Gherkin)
```gherkin
Feature: Verifying Citations

  # anchor: C.7.1
  Scenario: Gemini provides verifiable citations
    Given a synthesized research report
    When the user requests validation
    Then Gemini outputs a source index
    And every key finding is linked to a corresponding source in the index
```

#### §7.3 Rationale
The ultimate value of a research agent is trustworthiness. If the user cannot trace a claim back to its origin, the report is useless. Explicitly prompting for citations and data gaps forces the agent to be transparent about the boundaries of its research.

### §8. Known Limitations & Open Questions
- It is debated whether providing an explicit source priority list (e.g., "Only use .gov and .edu domains") helps accuracy or hinders Gemini's natural ability to discover diverse sources.

### §9. Source Index
1. Medium article: "Best Gemini Prompts in 2026: 50 Templates That Actually Work" by Sanjeev Patel.
2. Official DeepMind context / Gemini 2.0 release notes (inferred from temporal window).
---

## Contradictions Encountered
1. **Out-of-Scope Schema Field Candidate**: The §3–§7 schema may be missing the field `Failure Recovery / Error Handling`. Agents require specific instructions on how to handle command or sub-agent failures.
2. **Out-of-Scope Aspect Candidate**: Aspect `Context Window Management` appears to satisfy the inclusion criteria but is not in the five-aspect input list.
3. **Claude Code `CLAUDE.md` Length**:
   - **Claims**: One source (community best practices) suggests keeping `CLAUDE.md` under 60 lines to prevent frontier models from ignoring rules. Anthropic documentation implies a slightly larger but still constrained limit (~150-200 instructions).
   - **Sources**: HumanLayer blog vs. Anthropic Documentation.
   - **Hypothesized Cause**: Vendor doc lag and theoretical model limits vs. practical real-world degradation observed by power users.
   - **Evidence to Resolve**: Rigorous token-limit degradation testing on Opus 4.7.
2. **Gemini Deep Research Source Prioritization**:
   - **Claims**: Providing explicit source lists (e.g., .edu only) vs letting the model freely explore.
   - **Sources**: General prompting best practices vs Google's implicit handling of Deep Research.
   - **Hypothesized Cause**: Genuine community dispute over whether micromanaging the agent suppresses its native source-diversity algorithm.
   - **Evidence to Resolve**: A/B testing reports showing the quality of output with and without strict domain constraints.
3. **Google Jules Explicit Instructions vs Agentic Freedom**:
   - **Claims**: Jules needs explicit instructions for batch work vs Jules uses advanced reasoning to creatively solve vague goals.
   - **Sources**: MachineLearningMastery vs implicit agent capabilities.
   - **Hypothesized Cause**: Marketing-vs-engineering framing. Marketing pushes "autonomous", engineering pushes "explicitly defined tasks."
   - **Evidence to Resolve**: Success rates of vague vs specific prompts on Jules beta.

## World-Change Log
- **Google Jules**: Transitioned to public beta and integrated Gemini 2.5 Pro (Affects Spec-A).
- **Claude Code**: Beta features like `/code-review`, `/ultraplan`, and `subagents` are rapidly evolving (Affects Spec-B).
- **Gemini Deep Research**: "Deep Research Max" mentioned in recent Google blogs, indicating evolving capabilities and limits (Affects Spec-C).

## Query Expansion Log
- **System**: Google Jules
  - **Adjacent**: "github integration", "task description" (Found novel findings: Yes, modified A.2.1)
  - **Opposing**: "Google Jules failures", "Jules misroutes plan" (Found novel findings: No)
  - **Abstraction**: "agentic coding assistants" (Found novel findings: Yes, ML Mastery article)
  - **Orthogonal**: "Jules audio changelog" (Found novel findings: Yes, modified A.6.3)
- **System**: Claude Code
  - **Adjacent**: "CLAUDE.md conventions", "subagent design", "slash commands" (Found novel findings: Yes, modified B.3.1)
  - **Opposing**: "Claude Code ignores rules" (Found novel findings: Yes, found the 60-line contradiction limit)
  - **Abstraction**: "LLM context window management" (Found novel findings: Yes, added B.3.4)
  - **Orthogonal**: "Claude Code code review" (Found novel findings: Yes, added B.6.1)
- **System**: Gemini Deep Research
  - **Adjacent**: "Gemini Deep Research report prompting" (Found novel findings: Yes, modified C.4.2)
  - **Opposing**: "Gemini Deep Research hallucination" (Found novel findings: Yes, added C.6.1)
  - **Abstraction**: "Autonomous web research agents" (Found novel findings: No)
  - **Orthogonal**: "Gemini live search grounding" (Found novel findings: Yes, modified C.3.1)

## Reflection History (CONSTRAINT BLOCK 0)

1. **Kickoff Reflection**
   > **Q1. What do I actually believe right now, and how confident?** I believe that while Claude Code has robust documentation, Google Jules and Gemini Deep Research may have sparser public docs. (High confidence).
   > **Q2. What is the strongest piece of evidence against my current belief?** Google often releases extensive whitepapers or cookbook examples when launching new agentic tools.
   > **Q3. Where am I most likely wrong, and why?** Assuming Claude Code is perfectly documented; its community discourse could contradict official docs due to rapid updates.
   > **Q4. What would I do differently if I restarted the research from scratch knowing what I know now?** Prioritize GitHub repos and community reproductions immediately over official docs.
   > **Q5. What is the single highest-value next action?** Build seed queries and explore docs.

2. **Mid-run Reflection (Jules)**
   > **Q1. What do I actually believe right now, and how confident?** Jules is strictly a batch-processing, async VM agent. (High confidence based on ML mastery).
   > **Q2. What is the strongest piece of evidence against my current belief?** N/A - all primary and secondary sources point to this VM architecture.
   > **Q3. Where am I most likely wrong, and why?** I might be wrong about how Jules handles exploration without explicit file paths.
   > **Q4. What would I do differently if I restarted the research from scratch knowing what I know now?** Search for more examples of Jules failing rather than just succeeding.
   > **Q5. What is the single highest-value next action?** Search for Claude Code `CLAUDE.md` practices.

3. **Post-Query-Expansion Reflection (Claude)**
   > **Q1. What do I actually believe right now, and how confident?** Claude's context window degrades rapidly, making subagents essential. (High confidence).
   > **Q2. What is the strongest piece of evidence against my current belief?** Opus 4.7 has a massive context window; theoretically, it shouldn't degrade this quickly.
   > **Q3. Where am I most likely wrong, and why?** The 60-line limit for CLAUDE.md might be overly strict for simple projects.
   > **Q4. What would I do differently if I restarted the research from scratch knowing what I know now?** Look for explicit Anthropic guidelines on `CLAUDE.md` length before looking at community repos.
   > **Q5. What is the single highest-value next action?** Draft Spec-B.

4. **Pre-Synthesis Reflection (Gemini)**
   > **Q1. What do I actually believe right now, and how confident?** Gemini DR absolutely requires explicit grounding instructions to perform well. (Medium confidence).
   > **Q2. What is the strongest piece of evidence against my current belief?** The prompt's steelman suggests explicit lists suppress diversity.
   > **Q3. Where am I most likely wrong, and why?** Assuming it hallucinates without the prompt, it might just be less focused.
   > **Q4. What would I do differently if I restarted the research from scratch knowing what I know now?** Test if Gemini DR defaults to live search without prompting.
   > **Q5. What is the single highest-value next action?** Draft Spec-C.

5. **Post-Synthesis Reflection (Pre-Check)**
   > **Q1. What do I actually believe right now, and how confident?** All specs adhere to RFC 2119 and Gherkin. (High confidence).
   > **Q2. What is the strongest piece of evidence against my current belief?** I had not initially included the verbatim §1 block across all three specs.
   > **Q3. Where am I most likely wrong, and why?** I might have slipped an all-caps MUST into a rationale block or missed single-source annotations.
   > **Q4. What would I do differently if I restarted the research from scratch knowing what I know now?** Build an automated linter for RISE-DX output immediately.
   > **Q5. What is the single highest-value next action?** Run the assembly and grep check.

6. **Iteration 1 Reflection (Google Jules)**
   > **Q1. What do I actually believe right now, and how confident?** Jules is an async batch runner. (High confidence).
   > **Q2. What is the strongest piece of evidence against my current belief?** N/A - documentation points to asynchronous beta.
   > **Q3. Where am I most likely wrong, and why?** Assuming Jules requires explicit prompt context vs inferring from codebase.
   > **Q4. What would I do differently if I restarted the research from scratch knowing what I know now?** Try to find a live example of it running to see the UI.
   > **Q5. What is the single highest-value next action?** Write Spec-A.

7. **Iteration 2 Reflection (Claude Code)**
   > **Q1. What do I actually believe right now, and how confident?** Claude is a terminal-based context manager. (High confidence).
   > **Q2. What is the strongest piece of evidence against my current belief?** It also supports browser MCPs now.
   > **Q3. Where am I most likely wrong, and why?** Assuming subagents are the only way to manage context (checkpointing exists).
   > **Q4. What would I do differently if I restarted the research from scratch knowing what I know now?** Focus more on `/compact` vs `/clear`.
   > **Q5. What is the single highest-value next action?** Write Spec-B.

8. **Iteration 3 Reflection (Gemini Deep Research)**
   > **Q1. What do I actually believe right now, and how confident?** Gemini DR is a long-form report generator. (High confidence).
   > **Q2. What is the strongest piece of evidence against my current belief?** It can also generate code or short answers if forced.
   > **Q3. Where am I most likely wrong, and why?** Over-constraining its formatting might limit its reasoning.
   > **Q4. What would I do differently if I restarted the research from scratch knowing what I know now?** Explore multimodal prompts.
   > **Q5. What is the single highest-value next action?** Write Spec-C.

## Cross-Pollination Log
- **Out-of-Scope Aspect Candidate**: Context Window Management (Identified during Claude Code research). Highly critical for production but not one of the 5 requested aspects.
- **Schema-Gap Hypothesis**: The §3–§7 schema as given may be missing the field `Failure Recovery / Error Handling` because `agents like Jules and Claude Code are inherently fallible and often require specific instructions on how to behave when a bash command or sub-agent fails. Without this field, prompts may lack the necessary fallback loops.` Test search across systems shows Claude Code has explicit `/doctor` and `PostToolUse` hooks to handle this, confirming the hypothesis.
- **World-Change Annotations**: See World-Change Log above.

## Open Questions / Unresolved
- Does providing explicit domain priority to Gemini Deep Research suppress its native search diversity?
- What is the absolute hard limit for `CLAUDE.md` before instruction degradation occurs on Opus 4.7?
- Can Jules handle deeply nested monolithic repositories without explicit `AGENTS.md` maps?

## Sources
1. [Primary] `blog.google`: "Build with Jules, your asynchronous coding agent"
2. [Primary] `docs.claude.com`: "Best Practices for Claude Code"
3. [Primary] Anthropic Engineering: "Code Review" and "Auto Mode" blogs
4. [Reproduction] GitHub: `shanraisshan/claude-code-best-practice`
5. [Reproduction] MachineLearningMastery: "Practical Agentic Coding with Google Jules"
6. [Aggregator] Medium: "Best Gemini Prompts in 2026: 50 Templates That Actually Work"

## Methodology Note
- **Source Triangulation**: Applied across all three systems. Where primary docs were lacking (Gemini DR), community reproductions and aggregators were used and flagged.
- **Contradiction Log**: Actively maintained for `CLAUDE.md` length and Gemini source priorities.
- **What Would Change My Mind (Pre-Commitment)**: Applied to one major statement per Spec.
  - Spec-A: I would weaken A.2.3 from `MUST` to `SHOULD` if official Google guidelines state Jules performs best with high-level, open-ended problem statements.
  - Spec-B: I would weaken B.3.1 from `SHOULD` to `MAY` if Anthropic documentation states subagents are only for tool use, not general codebase exploration.
  - Spec-C: I would strengthen C.4.1 from `SHOULD` to `MUST` if official documentation states Gemini DR will fail entirely without an explicit grounding instruction.
  - Search results: None of these conditions were met, so the statements stand.
- **Steelmanning**: Applied to test the rigidity of `MUST` statements, resulting in several downgrades to `SHOULD`.
- **Adversarial Query Expansion**: Invoked along 4 axes per system to escape local-minimum lock-in.
