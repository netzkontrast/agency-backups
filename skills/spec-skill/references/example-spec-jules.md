# Worked Example — Spec-A: Google Jules

This is a complete, real specification reproduced as a reference for what a finished spec looks like. It was extracted from a research report on agentic-workflow best practices (May 2026). Use it as a template to compare against when generating or auditing specs.

The example demonstrates:

- All required sections (§§0–9)
- A mix of MUST, MUST NOT, SHOULD, MAY across normative statements
- Gherkin scenarios with anchors
- Rationale that cites sources without introducing new normative content
- A §8 that honestly names what the spec doesn't cover

---

## Spec-A: Google Jules

### §0. Status & Provenance

**Status:** Mature (High Confidence)
**Last Review Date:** May 2, 2026
**Primary Sources:** Google Jules official documentation, Google Cloud Developer Experiences, Google Labs engineering blog posts, Agentic AI Foundation specifications.

### §1. Normative Conventions

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in every produced Spec are to be interpreted as described in BCP 14 when, and only when, they appear in all capitals, as shown here.

### §2. System-Level Prompt Conventions

- A.2.1 — A Jules task prompt MUST specify the target repository and the target branch.
- A.2.2 — A project utilizing Jules MUST maintain a human-curated instructions file in its root directory to enforce team conventions without manual prompting.
- A.2.3 — A Jules session MUST execute asynchronously in an isolated cloud environment.
- A.2.4 — A developer SHOULD utilize the specialized command-line interface tool for scripting and orchestrating automated batch coding tasks.
- A.2.5 — A Jules prompt MUST NOT bypass the project's established continuous integration testing workflows.

### §3. Aspect 1 — Explore

#### §3.1 Normative Statements

- A.3.1 — An exploration prompt directed at Jules MUST clearly specify the sub-directory or package to be analyzed.
- A.3.2 — The developer MUST ensure that repository instruction files are populated with navigation tips to guide the autonomous discovery process.
- A.3.3 — The agent SHOULD utilize its internal retrieval mechanisms to autonomously identify relevant prior solutions within the codebase before proposing new patterns.
- A.3.4 — An exploration task MAY be triggered directly via an issue-tracking integration using a specialized mention tag.
- A.3.5 — A prompt aiming to discover codebase context MUST NOT mandate immediate code implementation.

#### §3.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: A.3.1
Feature: Explore Phase Scope Definition

  Scenario: Jules receives a scoped exploration request
    Given an active agent session connected to a valid repository
    And the repository contains an instruction file detailing directory structure
    When the user prompts the agent to analyze the authentication implementation in a specific directory
    Then the agent restricts its search footprint to the specified directory
    And the agent outputs an overview of the authentication implementation without editing files
```

#### §3.3 Rationale

During the exploration phase, allowing an autonomous agent to scan an entire large-scale monolithic repository without boundaries leads to severe context dilution. By explicitly defining the scope in the initial prompt and supporting it with structured repository files, the agent successfully identifies the correct architectural patterns. Requesting immediate changes during this discovery phase bypasses the agent's ability to thoroughly map dependencies, which reinforces why exploration and execution workflows are decoupled in professional environments.

### §4. Aspect 2 — Plan / Develop Spec

#### §4.1 Normative Statements

- A.4.1 — A planning prompt MUST explicitly request the agent to generate a step-by-step proposal before code execution begins.
- A.4.2 — A user MUST interact with the interactive planning interface to approve or reject the proposed file modifications.
- A.4.3 — The internal critic module MUST autonomously review the generated plan for edge cases before it is presented to the user.
- A.4.4 — A user SHOULD provide revision feedback directly into the conversational interface if the generated plan omits critical dependencies.
- A.4.5 — A plan MAY be configured to bypass manual review if the system's auto-approval timer is explicitly enabled.

#### §4.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: A.4.2
Feature: Interactive Plan Review

  Scenario: Developer reviews and refines an execution plan
    Given a user has prompted the agent to bump a specific dependency framework version
    When the agent outputs an interactive plan detailing changes to package files
    And the user replies with a request to also update the corresponding testing library dependencies
    Then the agent halts all execution pathways
    And the agent regenerates the plan to include the testing library updates
    And the agent waits for final user approval before modifying files
```

#### §4.3 Rationale

The interactive planning phase serves as the most critical intervention point in the asynchronous workflow. Because the system operates independently in a cloud virtual machine, catching a hallucinated dependency or an incorrect architectural assumption at the planning stage preserves substantial compute resources and mitigates debugging effort. The integration of an internal planning critic agent further reduces task failure rates by autonomously filtering out brittle execution paths before human review occurs.

### §5. Aspect 3 — Implement / Execute

#### §5.1 Normative Statements

- A.5.1 — An execution prompt MUST define precise acceptance criteria that the autonomous agent can independently verify.
- A.5.2 — The system MUST author the subsequent code commits according to the authorship configuration set by the user.
- A.5.3 — An implementation prompt SHOULD leverage environment snapshots to bypass redundant dependency installation procedures.
- A.5.4 — The user MUST NOT continuously interrupt the execution agent with new instructions while a multi-file task is actively running.
- A.5.5 — An execution run MAY span multiple concurrent tasks if the developer holds an enterprise-tier subscription.

#### §5.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: A.5.2
Feature: Commit Authorship Adherence

  Scenario: The agent commits code using a co-authored configuration
    Given the user has configured the commit authorship mode to indicate joint collaboration
    When the execution agent completes a code implementation task
    And the execution agent creates a new branch
    Then the resulting version control commit contains a trailer referencing the human user
    And the pull request reflects joint authorship
```

#### §5.3 Rationale

Implementation within this architecture occurs asynchronously. Unlike synchronous terminal agents, developers cannot safely inject immediate course corrections while the virtual machine is actively compiling or editing source files. Therefore, robust prompts provide clear definitions of done upfront. Controlling the authorship attribute ensures that engineering organizations can properly audit which commits were entirely machine-generated versus those that were co-authored with human oversight.

### §6. Aspect 4 — Review

#### §6.1 Normative Statements

- A.6.1 — The system MUST run its internal critique module against the generated patch prior to finalizing the implementation.
- A.6.2 — A code review prompt SHOULD instruct the critique module to evaluate the code specifically for performance bottlenecks and security vulnerabilities.
- A.6.3 — The user MUST NOT treat the automated critique as a full substitute for human-in-the-loop security audits.
- A.6.4 — A critique prompt MUST instruct the agent to utilize reference-free evaluation methods to judge logic and overall correctness.
- A.6.5 — The system MAY automatically rewrite portions of its own code if the critique module flags a subtle logic error during the generation cycle.

#### §6.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: A.6.1
Feature: Internal Critique Loop

  Scenario: The internal critic flags an inefficient algorithm
    Given the execution module has drafted a sorting function
    When the critique module performs its single-pass adversarial review
    And the critique module detects a nested loop causing exponential time complexity
    Then the critique module halts the pull request creation
    And the critique module loops the code back to the execution module for refactoring
```

#### §6.3 Rationale

The integration of actor-critic reinforcement learning mechanisms into agentic workflows addresses the limitations of standard generative models. An isolated generation model often lacks the self-reflection needed to identify edge cases. The internal critique agent acts as an adversarial peer reviewer during the generation phase, drastically reducing the number of trivial logic flaws that reach the pull request stage, shifting the review burden leftward.

### §7. Aspect 5 — Validate / Verify

#### §7.1 Normative Statements

- A.7.1 — A validation prompt MUST instruct the agent to execute the project's test suite inside the cloud virtual machine environment.
- A.7.2 — The continuous integration fixing module MUST automatically intercept and attempt to resolve failures on pull requests it generates.
- A.7.3 — A developer MUST include explicit testing instructions within the repository's configuration file for the validation module to consume.
- A.7.4 — A validation task SHOULD include instructions to generate new unit tests for any previously uncovered edge cases.
- A.7.5 — The agent MUST NOT blindly suppress error logs to force a continuous integration build to pass.

#### §7.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: A.7.2
Feature: Autonomous Pipeline Repair

  Scenario: The agent resolves a broken build autonomously
    Given the agent has submitted a pull request
    And the continuous integration pipeline reports a failure
    When the autonomous fixing module receives the webhook containing the error logs
    Then the module autonomously provisions a new execution environment
    And the module generates and commits a patch to resolve the failed test
    And the module waits for the pipeline to report a successful status
```

#### §7.3 Rationale

The ultimate measure of an autonomous coding agent is its ability to produce working, verifiable software. Passing the test suite is an absolute baseline. The autonomous continuous integration repair functionality closes the loop on agentic development by ensuring that an agent can interpret test runner output and self-correct without requiring a developer to manually paste error logs back into a chat interface.

### §8. Known Limitations & Open Questions

- The system struggles with exceptionally large monolithic repositories where context cannot be easily isolated; instructions must remain extremely localized.
- Visual validation for complex web applications remains experimental; the agent can test web applications, but debugging highly nuanced rendering issues is inconsistent.
- The academic community continues to debate whether automated repository instruction files create context dilution in repositories exceeding one million lines of code.

### §9. Source Index

1. Google Jules official documentation
2. Google Cloud Developer Experiences blog
3. Google Labs engineering blog: agentic coding posts
4. Linux Foundation: Agentic AI Foundation announcement
5. Independent engineering reports on Jules workflows (Medium, Reddit, MachineLearningMastery)

---

## What this example demonstrates

- **Statement count per aspect:** 5 statements per aspect — at the upper end of the recommended 3–6 range.
- **Modal calibration:** each aspect has a mix of MUST (1–3), SHOULD (1–2), MAY (1), MUST NOT (0–1). No aspect is all MUSTs.
- **Anchor discipline:** every Gherkin scenario has a `# anchor:` comment that points to a real statement.
- **Surface vs. normative:** §4.2's scenario describes "the interactive planning interface" not "the green button". Surface details ("a green Approve button") would belong in §4.3 rationale, not in the Gherkin or in §4.1.
- **Rationale honesty:** §3.3 admits the failure mode ("severe context dilution") that motivates the constraints. The rationale does the explanatory work; the statements stay terse.
- **§8 candor:** the limitations section names real open questions, including the contested empirical question about instruction-file efficacy.

When auditing a spec, compare it against this example's structure and discipline. When generating one, model the modal mix and the rationale style.
