---
type: research
status: completed
slug: repo-maintenance-protocol-spec
summary: "Normative spec for the Nightly Maintenance Protocol, dynamic (executable) readme schema, and the /todo/ delegation pipeline. Bounds the maintenance agent's scope away from Root Specs."
created: 2026-05-02
updated: 2026-05-04
research_phase: complete
research_executes_prompt: repo-maintenance-protocol-spec
research_friction_level: FL1
---

# Repository Maintenance Protocol and Dynamic Documentation Standard

## §1. Normative Conventions
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.

## §2. Nightly Maintenance Run Protocol
The repository MUST undergo a scheduled maintenance loop to ensure that state, documentation, and technical debt remain synchronized.

### 2.1 Triggering and Scope
- The maintenance run MUST be triggered autonomously on a scheduled basis (e.g., nightly) or upon explicit human invocation.
- The scope of the maintenance agent MUST be restricted to aggregating learnings, updating dynamic documentation state, and converting raw logs into actionable delegation tasks.
- The maintenance agent MUST NOT modify Root Specs (`AGENTS.md`, `FOLDERS.md`, `RESEARCH.md`, `PRE_COMMIT.md`, or `MAINTENANCE.md`). [SYNTHESIS]

# anchor: maintenance-scope-rule
```gherkin
Feature: Maintenance Run Scope Constraint
  Scenario: Agent attempts to modify a Root Spec
    Given a scheduled maintenance run is active
    When the agent detects an optimized architecture rule
    Then the agent MUST NOT edit `AGENTS.md` directly
    And the agent MUST generate a `prompt.md` proposing the change in the `/todo/` pipeline
```

## §3. Dynamic Readme Schema
The `readme.md` files mandated by `FOLDERS.md` MUST transition from static indices to executable state machines.

### 3.1 Partitioning
Every `readme.md` MUST be partitioned into:
1. **Static Section:** Contains the *Purpose* and *Linked Navigation*. The maintenance agent SHOULD NOT overwrite this unless links are broken.
2. **Dynamic Section:** Contains *Current State*, *Latest Synthesized Learnings*, and *Open Blockers*. The maintenance agent MUST update this section during the run.

# anchor: dynamic-readme-update
```gherkin
Feature: Dynamic Readme Updating
  Scenario: Agent processes a completed research folder
    Given the agent is scanning `/research/task-xyz`
    When the agent finds new insights in `/synthesis/post-synthesis-log.md`
    Then the agent MUST update the `Latest Synthesized Learnings` section in `/research/task-xyz/readme.md`
    And the agent MUST leave the `Purpose` section intact
```

## §4. Task Delegation and the `/todo/` Pipeline
Raw friction logs (`FL1-FL3`) and unresolved contradictions represent unstructured technical debt.

### 4.1 Delegation Processing
- The maintenance agent MUST extract complex issues or architectural friction from `/reflection/friction-log.md` files.
- The agent MUST transform these unstructured logs into self-contained `prompt.md` files.
- The generated `prompt.md` MUST be deposited into a central `/todo/` directory for future task execution. [SYNTHESIS]

# anchor: friction-log-delegation
```gherkin
Feature: Friction Log to Delegation Pipeline
  Scenario: Converting FL2 friction into a task
    Given a `friction-log.md` contains an FL2 entry about "API rate limit failures"
    When the maintenance agent parses the log
    Then the agent MUST create `/todo/api-rate-limit-fix/prompt.md`
    And the new prompt MUST contain the context and instructions to resolve the failure
```

## §5. Summary of Confidence & Traceability
- **Dynamic Readme concept:** Synthesized from "Readmes as State Machines" concept (T1/T2 unavailable, Single-Source Synthesized).
- **Decoupled Maintenance Runs:** Synthesized based on context window limitations (Single-Source Synthesized).
- **Delegation Pipeline:** Synthesized based on the necessity of decoupling yak-shaving from active execution (Single-Source Synthesized).
