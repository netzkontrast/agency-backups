# Spec Schema — Field-by-Field Reference

This document defines the exact structure of a normative agent specification. Use it when generating a spec in Mode 1 or auditing structure in Mode 3.

## Top-level shape

A specification document contains one or more specs. Each spec is identified by a single-letter prefix (A, B, C, …) that anchors all its normative statements.

```
## Spec-<PREFIX>: <Subject System>

### §0. Status & Provenance
### §1. Normative Conventions
### §2. System-Level Prompt Conventions
### §3. Aspect 1 — Explore
### §4. Aspect 2 — Plan / Develop Spec
### §5. Aspect 3 — Implement / Execute
### §6. Aspect 4 — Review
### §7. Aspect 5 — Validate / Verify
### §8. Known Limitations & Open Questions
### §9. Source Index
```

When multiple specs share a document, each gets its own `## Spec-X` block, and the document MAY add a top-level `## Common Conventions Across Systems` block before Spec-A and a top-level `## Contradictions Encountered`, `## World-Change Log`, `## Open Questions`, and `## Methodology Note` after the last spec.

## §0. Status & Provenance

Three required fields:

- **Status:** one of `Draft`, `Experimental`, `Stable`, `Mature (High Confidence)`, `Deprecated`. Choose conservatively. A `Mature` status implies the normative statements have survived adversarial review and at least one round of real-world use.
- **Last Review Date:** ISO date or human-readable date of the most recent end-to-end review. Not the date a single statement was added.
- **Primary Sources:** a short prose list of the source categories (vendor docs, engineering blogs, papers, internal observations). Specific citations go in §9.

## §1. Normative Conventions

This section is verbatim. Copy this paragraph unchanged:

> The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in every produced Spec are to be interpreted as described in BCP 14 when, and only when, they appear in all capitals, as shown here.

Do not paraphrase. The whole point of BCP-14 is that it's a fixed reference; rewording it breaks the contract.

## §2. System-Level Prompt Conventions

Numbered statements `X.2.1` through `X.2.N`. These are conventions that apply across all aspects — things like "MUST specify a working directory", "MUST NOT bypass CI", "SHOULD use structured output delimiters".

Aim for 3–7 statements. More than 10 usually signals that aspect-specific conventions have leaked up here.

## §§3–7. Aspect blocks

Each of the five aspects has the same internal structure:

```
### §N. Aspect <N-2> — <Aspect Name>

#### §N.1 Normative Statements

  - X.N.1 — <statement>
  - X.N.2 — <statement>
  - […]

#### §N.2 Acceptance Criteria (Gherkin)

  ```gherkin
  # anchor: X.N.<id>
  Feature: <name>
    Scenario: <name>
      Given …
      When …
      Then …
  ```

#### §N.3 Rationale

<Prose explaining why the statements take the shape they do. Citations
allowed. Vendor-specific surface details belong here, not in §N.1.>
```

### Aspect semantics

- **Explore** — the agent gathers information about the problem space without committing to changes. Codebase analysis, source discovery, context loading.
- **Plan / Develop Spec** — the agent proposes a strategy and waits for approval before acting. This is the leverage point for human oversight.
- **Implement / Execute** — the agent performs the planned action. File edits, code generation, search execution, report drafting.
- **Review** — the work is checked, ideally by a separate agent or fresh context. Adversarial review breaks self-confirmation bias.
- **Validate / Verify** — empirical evidence that the work meets the criteria. Tests pass. Citations resolve. Output matches the contract.

If the subject system collapses two aspects (e.g., a system where Plan and Implement are inseparable), say so explicitly in the section header (`### §4–5. Plan + Implement (combined)`) and explain in rationale. Don't silently drop a section.

### Statement count per aspect

3–6 statements per aspect is the sweet spot. Fewer than 3 suggests the aspect is underspecified or doesn't apply; more than 6 suggests several statements should be combined or moved to a sub-aspect.

## §8. Known Limitations & Open Questions

A bulleted list of:

- Things the spec deliberately doesn't cover.
- Behaviors of the subject system that no normative statement can fully constrain.
- Open empirical questions where the evidence is contested.

Each bullet should be a single sentence followed by an optional reference. Example:

> - The system struggles with monolithic repositories exceeding 1M LOC; instructions must remain extremely localized. [^11]

This section is non-negotiable. A spec without §8 is making the implicit claim that nothing is unknown — which is never true and corrodes the spec's credibility on contact with reality.

## §9. Source Index

Numbered list of citations. Match the citation markers used in §3–§8 rationales. Keep this section thin — it's an index, not a bibliography essay.

```
1. <Source title>
2. <Source title>
…
```

## Optional epistemic appendices (document-level, not per-spec)

These attach to the document, not to any individual spec. Use them when the evidence base is contested or evolving.

### Contradictions Encountered

For each contradiction:

- **Claims:** what disagrees with what.
- **Hypothesized Cause:** your best guess at why the sources diverge.
- **Resolution Evidence Needed:** what would actually settle it.

### World-Change Log

Recent changes to the subject systems that altered the spec. Each entry: short description, date, and which spec/section it affects.

### Query Expansion Log (optional, for research-derived specs)

Tabular record of how the research that produced the spec was extended adversarially — what axes were probed (adjacent, opposing, abstraction, orthogonal), what novel findings emerged, and which statements were modified as a result.

### Reflection History (optional, for research-derived specs)

Per-iteration self-assessment using the five-question template (current belief and confidence; strongest counter-evidence; most likely error; what would change if restarted; highest-value next action). Documents the reasoning trajectory for future audit.

### Methodology Note

A short paragraph describing the research/authoring process: what frameworks were used (e.g., ReAct, source triangulation, adversarial expansion), what was excluded and why. This gives readers the meta-context to weigh the spec's claims.

## Anti-patterns to refuse

- **Numbering drift.** If you have A.3.1, A.3.2, A.3.4, find A.3.3 or renumber. Gaps suggest deletions that aren't reflected in the audit trail.
- **Mixing prefixes.** A statement labeled `B.3.1` inside a Spec-A block is a copy-paste error and must be flagged.
- **Gherkin without anchors.** Every scenario needs a `# anchor: X.N.<id>` comment. Otherwise the scenario is decorative.
- **Rationale that contradicts the statement.** If the rationale says "in practice, this rarely matters", the statement is probably misclassified — demote MUST to SHOULD or remove it.
