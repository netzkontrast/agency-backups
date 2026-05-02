# Narrative Context Protocol — Specification for AI-Agent-Driven Novel Co-Authoring

**Version:** 1.0
**Date:** 2026-05-02
**Repo SHA Pinned:** 0b9ab1223d3822a49eddc139bcdf2669aa067734
**Source-Skill:** research-prompt-optimizer v2.1.0
**Conformance Level:** Strict (RFC 2119 / Gherkin)
**Audience:** Senior Software Architect / AI Systems Developer

## §1 Conformance Language

### §1.1 RFC 2119 / BCP 14 normative keywords
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.

### §1.2 Gherkin syntax binding
Every behavioural example, agent-interaction scenario, or hand-off specification in this document MUST use standard Gherkin syntax (Feature, Scenario, Given, When, Then, And, But). Every `Scenario:` block MUST be self-contained and independently executable.

### §1.3 Style Guide for normative statements
1. Normative statements MUST NOT be combined with rationale; rationale MUST be provided in plain prose.
2. An agent-directed rule MUST include an explicit trigger condition or context constraint.
3. Every normative constraint regarding the NCP schema MUST cite the relevant JSON schema property or $def.
4. Gherkin Scenarios MUST NOT contain implementation-specific API parameters; they MUST describe structural outcomes only.

## §2 Glossary

- **Story**:
  - *NCP Track*: The root document entity containing metadata, ideation, and narratives.
  - *Dramatica Track*: The entirety of the "Story Mind", a complete argument resolving a central inequity.
- **Scene**:
  - *NCP Track*: A specific instantiation of a `moment` with defined `fabric` limits.
  - *Dramatica Track*: A temporal unit of Storytelling; Dramatica theory technically operates down to the 'Beat' or 'Progression' level, not strictly the prose 'Scene'.
- **Beat**:
  - *NCP Track*: A `storybeat`, connecting a structural appreciation to narrative function and sequencing.
  - *Dramatica Track*: The smallest unit of plot progression within a quad.
- **Throughline**:
  - *NCP Track*: An attribute on a `storypoint` or `storybeat` linking it to one of the four perspectives.
  - *Dramatica Track*: One of the four mandatory perspectives (OS, MC, IC, RS) required to complete a Story Mind.
- **Skill**:
  - *Skill-Spec Track*: A functional module (SKILL.md) providing contextual playbooks for the agent.
- **Workflow**:
  - *SDD Track*: The orchestrated sequence of plan-then-implement cycles executed by an agent.
- **Phase**:
  - *SPEC.md Track*: One of the eight mandatory stages of novel co-authoring defined herein.
- **Context**:
  - *NCP Track*: The serialized JSON state holding the narrative structure.
- **Protocol**:
  - *NCP Track*: The standardized schema (narrative-context-protocol) used for inter-agent communication.

## §3 Scope and Non-Goals

### §3.1 In scope
This specification REQUIRES implementation of the following eight phases of novel co-authoring:
1. Premise & Concept
2. Dramatica Storyform
3. Outline & Plot Structure
4. Character Work & Relationships
5. Worldbuilding & Wiki Build-up
6. Scene Drafting
7. Revision & Consistency Checks
8. Editing & Final Polish

### §3.2 Non-goals
This specification explicitly excludes:
- Style, voice, or tone generation rules.
- Auto-publishing or distribution pipelines.
- Direct output integration with proprietary Dramatica software (e.g., Dramatica Pro).

## §4 Architectural Decision: NCP ↔ Dramatica Relationship

### §4.1 Option A — Parallel Layers
NCP handles context and serialization; Dramatica logic is maintained strictly in agent memory/side-files. Bidirectional sync is required.
### §4.2 Option B — Dramatica-In-NCP
Dramatica concepts (Storypoints, Dynamics, Elements) are modeled as first-class enums and fields natively within the NCP JSON schema.
### §4.3 Option C — NCP-In-Dramatica
The Dramatica engine leads execution, outputting NCP purely as a dumb file format at the very end of processing.
### §4.4 Trade-off matrix
| Architecture | Extension Cost | Agent Ergonomics | Fidelity to Canon | Hexagonal Compatibility |
|---|---|---|---|---|
| Option A | Low | High | Medium | High |
| Option B | High | Low | High | Medium |
| Option C | N/A | Low | High | Low |

### §4.5 Recommendation
The system MUST implement **Option B (Dramatica-In-NCP)**.
*Justification:* The current NCP repository `schema/ncp-schema.json:L25-L352@0b9ab1223d3822a49eddc139bcdf2669aa067734` already hardcodes Dramatica canon (e.g., `canonical_appreciation`, `canonical_narrative_function`) into its `$defs` enums. Deviating from the primary source code would introduce severe friction.
### §4.6 Pre-commitment (Method M08)
I would reverse this recommendation if I found that NCP removes `canonical_narrative_function` and `canonical_appreciation` enums in a future schema v2.0 update, delegating them strictly to custom namespaces.

## §5 NCP Data Model

### §5.1 Entity inventory
- `story` (`schema/ncp-schema.json:L10-L40@0b9ab1223d3822a49eddc139bcdf2669aa067734`)
- `narratives` (`schema/ncp-schema.json:L50-L80@...`)
- `perspectives`, `players`, `dynamics` (`schema/ncp-schema.json:L100-L150@...`)
- `storypoints`, `storybeats`, `moments` (`schema/ncp-schema.json:L160-L220@...`)

### §5.2 Relationships and cardinalities
A `story` MUST contain exactly one `ideation` block and one or more `narratives`. Each narrative MUST contain `subtext` (perspectives, players, dynamics, storypoints, storybeats) and `storytelling` (overviews, moments).

### §5.3 State machines
NCP natively tracks state loosely via the `status` string on narratives. Agents MUST enforce workflow transitions externally using the Router pattern.

### §5.4 Entry points
The specification supports JSON/YAML file format serialization natively. There are no explicit API/CLI entry points defined strictly within the schema itself.

### §5.5 Integration surfaces for Dramatica
Dramatica integrates natively via the `dynamics` and `storypoints` arrays within the `subtext` object.

### §5.6 Gaps requiring Dramatica-side extension
NCP does NOT strictly guard against invalid Storyform selections (e.g., mismatching Domain and Concern). Validation MUST be handled by cross-cutting agent skills.

## §6 Dramatica Canon

### §6.1 Story Mind and the four Throughlines
A complete story MUST model a single Story Mind containing Overall Story, Main Character, Influence Character, and Relationship Story throughlines.

### §6.2 Domain / Concern / Issue / Problem
Each Throughline MUST map sequentially downwards through Universe/Situation, Mind/Fixed Attitude, Physics/Activity, and Psychology/Manipulation.

### §6.3 Quads
Elements MUST be arranged in Quads (e.g., Knowledge, Thought, Ability, Desire).

### §6.4 Dynamics
The narrative MUST define Story Driver, Limit, Outcome, and Judgment to control resolution.

### §6.5 Authoring phases
Concept → Storyform → Storyweaving → Storytelling.

## §7 Workflow Architecture

### §7.1 Candidate patterns
- Option A: Pipeline (Strict unidirectional flow)
- Option B: DAG (Directed Acyclic Graph with explicit dependencies)
- Option C: Autonomous hand-off via NCP-state (Agents read `status` and act)

### §7.2 Trade-off matrix
| Pattern | Thrashing Risk | Flexibility | Hand-off Complexity |
|---|---|---|---|
| Pipeline | Low | Low | Low |
| DAG | Low | High | Medium |
| Autonomous | High | High | High |

### §7.3 Recommendation
The system MUST implement **Option B (DAG)**.
*Justification:* Autonomous hand-offs risk endless revision loops (thrashing) without rigid external state, while strict pipelines forbid necessary creative backtracking. DAG allows structured iteration.

### §7.4 Pre-commitment (Method M08)
I would reverse this recommendation if I found that future Claude Code native implementations introduce a strict 'state-lock' mechanism preventing an agent from modifying previously approved NCP phases without explicit user override.

### §7.5 Workflow diagram
```text
[Phase 1] --> [Phase 2] --> [Phase 3] --> [Phase 5]
                            |
                            +-> [Phase 4] -+
                                           v
                                      [Phase 6] --> [Phase 7] --> [Phase 8]
```

### §7.6 NCP state-machine conventions
Agents MUST update the narrative `status` enum upon completing a Phase before routing to the next Phase.

### §7.7 Hand-off Gherkin scenarios
```gherkin
Feature: Phase Routing Hand-off
  Scenario: Advancing from Phase 2 to Phase 3
    Given the current phase is "Phase 2: Dramatica Storyform"
    And the agent verifies all 4 throughlines are populated in NCP
    When the agent updates the narrative status to "storyformed"
    Then the router skill MUST delegate control to "Phase 3: Outline Structure"
```

## §8 Skill Catalog (Hybrid Hexagonal)

### §8.1 Catalog conventions
All skills MUST be structured as directories containing a `SKILL.md` file using YAML frontmatter with `name`, `description` (triggers), and `metadata`.

### §8.2 Phase 1 — Premise & Concept
#### §8.2.1 Router Skeleton
`SKILL.md`: `name: route-premise`, `description: Triggers when narrative status is empty. Routes to ideation.`
#### §8.2.2 Sub-skills
- `SKILL.md`: `name: gen-logline`
- `SKILL.md`: `name: map-ideation`

### §8.3 Phase 2 — Dramatica Storyform
#### §8.3.1 Router Skeleton
`SKILL.md`: `name: route-storyform`
#### §8.3.2 Sub-skills
- `SKILL.md`: `name: set-dynamics`
- `SKILL.md`: `name: map-throughlines`
- `SKILL.md`: `name: assign-elements`

### §8.4 Phase 3 — Outline & Plot Structure
#### §8.4.1 Router Skeleton
`SKILL.md`: `name: route-outline`
#### §8.4.2 Sub-skills
- `SKILL.md`: `name: sequence-beats`
- `SKILL.md`: `name: define-moments`

### §8.5 Phase 4 — Character Work
#### §8.5.1 Router Skeleton
`SKILL.md`: `name: route-character`
#### §8.5.2 Sub-skills
- `SKILL.md`: `name: build-players`
- `SKILL.md`: `name: assign-perspectives`

### §8.6 Phase 5 — Worldbuilding
#### §8.6.1 Router Skeleton
`SKILL.md`: `name: route-world`
#### §8.6.2 Sub-skills
- `SKILL.md`: `name: expand-fabric`
- `SKILL.md`: `name: map-settings`

### §8.7 Phase 6 — Scene Drafting
#### §8.7.1 Router Skeleton
`SKILL.md`: `name: route-drafting`
#### §8.7.2 Sub-skills
- `SKILL.md`: `name: draft-prose`
- `SKILL.md`: `name: sync-moment-status`

### §8.8 Phase 7 — Revision
#### §8.8.1 Router Skeleton
`SKILL.md`: `name: route-revision`
#### §8.8.2 Sub-skills
- `SKILL.md`: `name: check-consistency`
- `SKILL.md`: `name: apply-edits`

### §8.9 Phase 8 — Editing
#### §8.9.1 Router Skeleton
`SKILL.md`: `name: route-edit`
#### §8.9.2 Sub-skills
- `SKILL.md`: `name: copy-edit`
- `SKILL.md`: `name: final-polish`

### §8.10 Cross-cutting skills
- `SKILL.md`: `name: read-write-ncp`
- `SKILL.md`: `name: validate-storyform`

## §9 Agent Targets

### §9.1 Claude Code
Claude Code natively discovers `SKILL.md` via the filesystem. It MUST read the `ncp-schema.json` via the `read-write-ncp` sub-skill.

### §9.2 Gemini Jules
Gemini Jules MAY lack native directory skill loading. If so, a compensation pattern MUST be used: compile the SKILL.md router paths into a single `agent-notes.md` file in the project root.

### §9.3 Portability requirements
```gherkin
Feature: Cross-Agent Execution
  Scenario: Agent parses SKILL.md uniformly
    Given an agent reads Phase 2 Router SKILL.md
    When it encounters the trigger description
    Then it MUST successfully route to the `set-dynamics` sub-skill regardless of underlying LLM architecture.
```

## §10 Acceptance Criteria for SPEC.md

### §10.1 Coverage scenarios
```gherkin
Feature: Phase Coverage
  Scenario: All 8 Phases Present
    Given the SPEC.md document
    When the reader searches for Phase Router Skills
    Then the document MUST contain exactly 8 distinct Phase sections in §8.
```

### §10.2 NCP-entity coverage
```gherkin
Feature: Entity Mapping
  Scenario: Entities are mapped
    Given the Track 1 extracted entities
    When cross-referencing §5
    Then every entity MUST be cited with a path and SHA.
```

### §10.3 Hexagonal-pattern scenarios
```gherkin
Feature: Sub-skill routing
  Scenario: No orphan skills
    Given any Phase router
    Then it MUST contain at least 1 delegated sub-skill.
```

### §10.4 Conformance-language scenarios
```gherkin
Feature: RFC 2119 Validation
  Scenario: Normative force check
    Given a behavioural requirement in SPEC.md
    Then it MUST contain an uppercase RFC 2119 keyword.
```

## §11 Validation Walkthrough

### §11.1 Worked example
**Genre:** Cyber Noir
**Length:** Novella (40k words)
**Premise:** A detective must stop a rogue AI.
*Justification:* A generic cyberpunk plot allows clear mapping to 'Universe' (dystopia) and 'Mind' (AI alignment) without infringing on real authors.

### §11.2 Walkthrough phase-by-phase
- **Phase 1**: Agent calls `route-premise`, invokes `gen-logline`. Updates NCP `story` metadata.
- **Phase 2**: Agent calls `route-storyform`. Sets OS to 'Physics', MC to 'Universe'. Validates via cross-cutting skill.
- **Phase 3**: Agent calls `route-outline`. Generates `moments` array.
- **Phase 4**: Agent calls `route-character`. Populates `players` (Detective, AI).
- **Phase 5**: Agent calls `route-world`. Details 'Neo-Tokyo' in `fabric`.
- **Phase 6**: Agent calls `route-drafting`. Reads Phase 3 `moments` and generates prose.
- **Phase 7**: Agent calls `route-revision`. Compares prose to OS 'Physics' parameters.
- **Phase 8**: Agent calls `route-edit`. Final proofread and `status` set to 'complete'.

## §12 Open Questions and Deferred Decisions
- [NOT-MAPPED] Out-of-Scope Candidates from M13: POV-shift events, parallel quads, and beat-sheeting phases remain theoretically valid but fall outside this document's locked scope.
- Will NCP schema v2.0 decouple Dramatica enums into strict schemas?

## §13 Versioning and Change-Control
This SPEC.md is version 1.0. Any modifications to normative keywords MUST bump the minor version.

## §14 References
- NCP Repository (`0b9ab1223d3822a49eddc139bcdf2669aa067734`)
- Dramatica Theory Book (https://dramatica.com/theory)
- RFC 2119 (https://datatracker.ietf.org/doc/html/rfc2119)
- GitHub Spec-Kit / SDD Literature
- Anthropic Claude Skills (https://docs.claude.com)
