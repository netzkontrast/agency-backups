---
name: spec-skill
description: "Authoring, applying, and auditing normative specifications for autonomous AI agents and long-horizon agentic workflows — using RFC-2119 keywords, Gherkin acceptance criteria, and a fixed five-aspect schema (Explore, Plan, Implement, Review, Validate). Use this skill whenever the user wants to write a spec or specification for an agent, codify best practices for a coding/research/orchestration agent, draft normative MUST/SHOULD/MAY statements, derive prompts or workflows from an existing spec, validate a spec for schema-conformance and BCP-14 compliance, or convert vague requirements into a structured Markdown agent-specification document. Triggers on terms like spec, specification, RFC-2119, BCP-14, normative statement, MUST/SHOULD/MAY, Gherkin, acceptance criteria, agent best practices, agentic workflow spec, codify conventions, spec-driven, prompt spec, agent governance, long-horizon agent, autonomous agent prompt, write a spec, audit a spec, derive prompts from spec."
skill_bundles_tools:
  - tools/fm
---

# Spec-Skill — Normative Specifications for Agentic Workflows

## What this skill is for

This skill captures the **format and discipline** of writing normative specifications for autonomous AI agents — the kind of document that codifies best practices, conventions, and verification criteria for a long-horizon agent (coding agent, research agent, orchestration system, or any tool-using agent that operates over multiple steps).

The format is domain-neutral. It draws from RFC-2119 (BCP-14) for keyword discipline, Gherkin for acceptance criteria, and a five-aspect operational schema (Explore → Plan → Implement → Review → Validate) that has emerged as the de-facto structure for agentic-workflow governance in 2025–2026.

This skill does **not** prescribe what is true about any particular agent. It prescribes **how to write down what you believe is true** so that the document is reviewable, testable, and stable under contradiction.

## Three modes

The user request will fall into one of three modes. Decide which one before drafting anything.

| Mode | Trigger | Output |
| :--- | :--- | :--- |
| **`generate`** | "Write a spec for X", "Codify our agent conventions", "Turn these notes into a spec" | A complete Markdown spec following the schema in `references/spec-schema.md` |
| **`apply`** | "Take this spec and derive prompts for Jules", "Generate a CLAUDE.md from spec B", "What workflow does this spec imply?" | Prompts, config files, or workflows that operationalize the spec |
| **`audit`** | "Check this spec for compliance", "Is this Gherkin valid?", "Does this spec contradict itself?" | A structured findings report against the audit checklist in `references/audit-checklist.md` |

If the user's request is ambiguous, ask which mode — don't guess. The three modes have very different output shapes, and getting the mode wrong wastes the user's time.

## Mode 1: Generate

### Step 1 — Capture intent

Before writing a single normative statement, get clear on:

1. **Subject system** — what agent or workflow is being specified? (e.g., "our internal code-review agent", "Jules", "a Gemini Deep Research pipeline")
2. **Maturity** — is this `Mature (High Confidence)`, `Stable`, `Draft`, or `Experimental`? This goes in §0 and signals to readers how much to trust the normative statements.
3. **Sources** — what evidence backs the statements? Vendor docs, internal post-mortems, papers, observed behavior. The spec is only as good as its sourcing.
4. **Scope of aspects** — does the standard five-aspect structure (Explore/Plan/Implement/Review/Validate) fit? Or does the subject need a different decomposition? The five-aspect structure is the default; deviate only with reason.

If the user hands you a research document, transcript, or notes, extract the answers from there first. Then ask the user only what's missing.

### Step 2 — Decide on the prefix

Each spec gets a single-letter prefix that anchors all its normative statements: `A.2.1`, `B.4.3`, `C.7.5`. The prefix lets multiple specs coexist in one document without ID collisions and makes statements easy to cite in conversation ("we're violating B.5.2"). When a document holds multiple specs, prefixes go A, B, C, …

### Step 3 — Fill the schema

The full schema lives in `references/spec-schema.md`. The skeleton is:

```
## Spec-X: <Subject System>

### §0. Status & Provenance
### §1. Normative Conventions          (the BCP-14 paragraph — copy verbatim)
### §2. System-Level Prompt Conventions (X.2.1 … X.2.N)
### §3. Aspect 1 — Explore              (X.3.1 … X.3.N + Gherkin + Rationale)
### §4. Aspect 2 — Plan / Develop Spec  (X.4.1 … X.4.N + Gherkin + Rationale)
### §5. Aspect 3 — Implement / Execute  (X.5.1 … X.5.N + Gherkin + Rationale)
### §6. Aspect 4 — Review               (X.6.1 … X.6.N + Gherkin + Rationale)
### §7. Aspect 5 — Validate / Verify    (X.7.1 … X.7.N + Gherkin + Rationale)
### §8. Known Limitations & Open Questions
### §9. Source Index
```

Each `§3`–`§7` aspect block has three sub-sections: `§X.1 Normative Statements`, `§X.2 Acceptance Criteria (Gherkin)`, `§X.3 Rationale`. See the schema reference for the full per-section rules.

### Step 4 — Write normative statements with discipline

This is where most specs go wrong. Open `references/normative-discipline.md` and follow it. The short version:

- **All-caps keywords only** — `MUST`, `MUST NOT`, `SHOULD`, `MAY`, `REQUIRED`, etc. Lowercase "must" is regular English and does not bind.
- **One claim per statement** — no "and" clauses that hide a second requirement.
- **Specify the actor** — who must do what: the agent, the user, the system, the developer.
- **Testable** — if a statement can't be checked against a Gherkin scenario or an external observation, rewrite it.
- **Don't smuggle vendor-specific surface details** into normative statements — say "the agent's planning interface" not "the blue Approve button". Surface details belong in rationale, not in MUSTs.

### Step 5 — Write Gherkin scenarios with anchors

Every aspect block needs at least one Gherkin scenario, and each scenario carries an anchor comment pointing to the normative statement it verifies:

```gherkin
# anchor: A.4.2
Feature: Interactive Plan Review

  Scenario: Developer reviews and refines an execution plan
    Given a user has prompted the agent to bump a dependency
    When the agent outputs an interactive plan
    And the user replies with a request for additional changes
    Then the agent halts execution
    And the agent regenerates the plan
    And the agent waits for final approval
```

The anchor is what makes the spec auditable. Without it, scenarios float free of the statements they're supposed to verify.

### Step 6 — Write the rationale

For each aspect, explain *why* the normative statements are what they are. The rationale is where you reason about failure modes, mitigations, and trade-offs. This is also where vendor-specific surface details and citations live. Rationale does not bind — it explains.

### Step 7 — Optional epistemic appendices

For high-stakes specs where the evidence base is contested or evolving, include any of:

- **Contradictions Encountered** — claims from different sources that disagree, your hypothesized cause, and what evidence would resolve it.
- **World-Change Log** — recent product/policy changes that affect the spec.
- **Open Questions** — what's genuinely unsettled, with the threshold or evidence needed to close each.

These appendices signal that the author thought adversarially about the material. They are optional but raise the spec's credibility considerably.

## Mode 2: Apply

The user has a spec and wants something operational from it: prompts, config files, workflows, agent harnesses. The spec is the source of truth; the output is a translation.

### Workflow

1. **Read the spec end-to-end first.** Don't skim. Note the prefix, the §0 status, and any §8 limitations — limitations often constrain what can be safely derived.
2. **Identify which statements bind the output.** A request like "write a CLAUDE.md from this spec" is governed by §2 (system-level conventions) and any aspect-statements that mention persistent context or instruction files.
3. **Distinguish MUST from SHOULD from MAY in the output.** Statements marked MUST become hard requirements in the derived artifact. SHOULD becomes a default with an explicit comment. MAY becomes optional with a note.
4. **Cite the statement IDs in the output.** When you derive something from `B.2.2`, mark it `# from B.2.2`. This lets the user trace any line back to its normative source.
5. **Flag genuine gaps.** If the user asks for an output the spec doesn't cover, say so explicitly. Don't fabricate a position the spec didn't take.

### Common derivations

- **Spec → repository instruction file** (CLAUDE.md, AGENTS.md, JULES.md): pull §2 conventions plus relevant aspect-statements; respect length limits if the spec specifies one.
- **Spec → prompt template**: for each aspect, write a prompt that operationalizes the §X.1 statements and references the §X.2 Gherkin scenarios as success criteria.
- **Spec → review checklist**: convert the Gherkin scenarios into checkbox items, grouped by aspect.
- **Spec → eval set**: for each Gherkin scenario, generate a test case whose pass condition is the `Then` clauses.

## Mode 3: Audit

The user has a spec and wants it checked. Audit against the checklist in `references/audit-checklist.md`. Output a structured findings report — not free-form prose.

### Findings shape

```
# Audit: <spec name>

## Schema conformance
- [ ] §0 present with Status, Last Review Date, Primary Sources
- [ ] §1 BCP-14 paragraph present and verbatim
- [ ] §§3–7 each have Normative Statements, Gherkin, Rationale
- [ ] §9 Source Index present
[…]

## Normative discipline (per statement)
- A.3.1 — PASS
- A.3.2 — FAIL: contains two distinct requirements joined by "and"; split into A.3.2a and A.3.2b
[…]

## Gherkin validity
- A.3.2 anchor: PASS
- A.4.2 anchor: FAIL: scenario tests A.4.2 but anchor cites A.4.1
[…]

## Cross-cutting issues
- A.5.1 contradicts A.7.5 …
- §8 lists a limitation that should weaken A.6.1 from MUST to SHOULD …
```

The audit doesn't rewrite the spec. It surfaces problems precisely enough that the author can fix them.

## When to push back on the user

The format invites three failure modes that you should name when you see them:

1. **Overspecification.** Filling every aspect with five MUSTs because the schema has slots is worse than three well-grounded statements. If the user wants to fill slots that aren't supported by evidence, say so. Empty space is honest; padded specs lie.
2. **Vendor-coupling in normative statements.** Saying `The user MUST click the green Approve button` couples the spec to a UI version. The statement should describe the action ("approve the plan via the planning interface"); the UI detail goes in rationale.
3. **MUST inflation.** If everything is MUST, nothing is. SHOULD and MAY exist for a reason — they signal the gradations real systems actually have. A spec that's all MUSTs is usually a spec the author hasn't thought hard enough about.

## Reference files

- `references/spec-schema.md` — full schema with field-by-field rules and per-section examples
- `references/normative-discipline.md` — how to write MUST/SHOULD/MAY/MAY NOT statements that don't fall apart under review
- `references/audit-checklist.md` — the audit checklist used in Mode 3
- `references/example-spec-jules.md` — worked example of an asynchronous, cloud-isolated coding agent (Spec-A from the source research document). Shows the canonical 5-statement-per-aspect structure with mixed MUST/SHOULD/MAY discipline.
- `references/example-spec-claude-code.md` — worked example of a synchronous, terminal-resident coding agent (Spec-B). Shows quantitative §2 limits, prohibition-heavy aspects, and adversarial review patterns.
- `references/example-spec-gemini-dr.md` — worked example of a research/synthesis agent (Spec-C). Shows the schema generalizing beyond coding — different failure modes (citation hallucination, conflicting evidence) and a `MUST NOT` that protects user epistemics.
- `references/example-document-appendices.md` — worked examples of the document-level appendices: Common Conventions, Contradictions Encountered, World-Change Log, Query Expansion Log, Reflection History, Open Questions, and Methodology Note. Use when authoring a multi-spec document or a research-derived spec.

Read these as needed. Don't load them upfront — the SKILL.md gives you enough orientation to decide which mode you're in and which references matter. As a guide:

- Generating a coding-agent spec → load schema + discipline + the closest example (Jules for async/cloud, Claude Code for sync/terminal).
- Generating a research or non-coding spec → load schema + discipline + Gemini DR example.
- Generating a multi-spec document → also load document-appendices.
- Auditing → load schema + audit-checklist; consult discipline for borderline statement-level findings.
- Applying a spec → load schema; load discipline only if you suspect the source spec has issues you need to flag.
