# Audit Checklist

Use this in Mode 3 to produce a structured findings report on an existing spec. Work through it section by section. Output the findings in the shape shown in SKILL.md (under "Mode 3: Audit / Findings shape"); do not reformat into prose.

## Layer 1: Schema conformance

For each spec in the document:

- [ ] `## Spec-<PREFIX>: <Subject System>` header present, prefix is a single uppercase letter
- [ ] §0 Status & Provenance present, contains all three required fields (Status, Last Review Date, Primary Sources)
- [ ] §0 Status value is one of: Draft, Experimental, Stable, Mature, Deprecated
- [ ] §1 Normative Conventions present, contains the BCP-14 paragraph **verbatim** (compare against the canonical text in spec-schema.md)
- [ ] §2 System-Level Prompt Conventions present with at least one statement
- [ ] §§3–7 each present (Explore / Plan / Implement / Review / Validate)
- [ ] Each of §§3–7 contains all three sub-sections (§N.1 Normative Statements, §N.2 Acceptance Criteria, §N.3 Rationale)
- [ ] §8 Known Limitations & Open Questions present (even if short)
- [ ] §9 Source Index present

If an aspect has been collapsed or merged, the section header explicitly says so AND the rationale explains why. Silent omissions fail this check.

## Layer 2: Prefix and ID hygiene

- [ ] Every normative statement in Spec-X uses prefix X (no orphaned `B.4.1` inside a Spec-A block)
- [ ] Statement IDs within each section are sequentially numbered with no gaps (or gaps are noted in a change log)
- [ ] No duplicate IDs anywhere in the document

## Layer 3: Normative discipline (per statement)

For each statement in §2 and §§3.1–7.1:

- [ ] All BCP-14 keywords appear in **all caps** (catch lowercase "must", "should", "may")
- [ ] Statement has an identifiable actor, modal verb, and action
- [ ] Statement contains exactly one claim — no covert and-clauses joining two requirements
- [ ] Statement is testable — a Gherkin scenario could plausibly verify it
- [ ] Statement does not embed UI-specific or version-specific surface details (those belong in rationale)
- [ ] Modal choice is calibrated — not every statement is MUST; SHOULD and MAY appear where appropriate

Common failures to flag explicitly:

- **Lowercase keyword:** "the agent should validate output" — does not bind
- **And-bug:** "MUST do X and MUST do Y" — split into two statements
- **Vague actor:** "the system MUST be efficient" — who? measured how?
- **Surface detail:** "MUST click the green Approve button" — couples to UI version
- **MUST inflation:** every statement in an aspect is MUST — force-rank

## Layer 4: Gherkin validity

For each scenario in §§3.2–7.2:

- [ ] Scenario has a `# anchor: X.N.<id>` comment at the top
- [ ] Anchor cites a statement that exists in the spec
- [ ] Anchor cites a statement that the scenario actually tests (not just a nearby statement)
- [ ] Scenario uses Given/When/Then structure (And/But are valid extensions)
- [ ] Scenario describes observable behavior, not internal state
- [ ] Scenario is concrete enough to convert into a test case

## Layer 5: Cross-cutting integrity

- [ ] No two statements in the same spec contradict each other (e.g., A.5.1 says MUST X, A.7.5 says MUST NOT X)
- [ ] §8 limitations are consistent with the strength of the §§3.1–7.1 statements (a known limitation that breaks an aspect should weaken the corresponding MUSTs to SHOULDs)
- [ ] §9 Source Index entries are referenced by at least one rationale or §8 bullet (orphan citations fail this check)
- [ ] If the document has multiple specs, statements in `Common Conventions` are not duplicated inside individual specs

## Layer 6: Rationale honesty

For each §N.3 rationale:

- [ ] Rationale explains *why* the statements take their form, not just what they say
- [ ] Rationale does not contradict the statements (a rationale that says "in practice this rarely matters" undermines a MUST and signals miscalibration)
- [ ] Rationale cites sources for non-obvious claims
- [ ] Rationale does not introduce new normative requirements that aren't reflected in §N.1

## Layer 7: Epistemic integrity (for specs with appendices)

If the document includes Contradictions Encountered, World-Change Log, Open Questions, or Methodology Note:

- [ ] Each contradiction lists Claims, Hypothesized Cause, and Resolution Evidence Needed
- [ ] World-Change Log entries link to the affected spec/section
- [ ] Open Questions specify what evidence or threshold would close them
- [ ] Methodology Note describes the authoring process honestly (frameworks used, exclusions, known biases)

## Severity classification for findings

When reporting, classify each finding:

- **BLOCKER** — schema violation, contradiction, broken anchor. The spec cannot be relied on until fixed.
- **MAJOR** — discipline violation (and-bug, vague actor, surface coupling, MUST inflation). The spec is usable but will cause confusion.
- **MINOR** — formatting, missing optional appendix, citation cleanup. Worth fixing but doesn't change semantics.
- **OBSERVATION** — non-defects that the author should consider. Not findings per se.

## What the audit does not do

- The audit does not rewrite the spec. Findings are precise enough that the author can fix them; doing the rewrite yourself robs the author of the chance to make the call.
- The audit does not opine on whether the *content* of the normative statements is correct (whether MUST X is the right thing for the subject system to require). That's a domain judgment, not a structural one. If you have domain reservations, surface them as OBSERVATIONs, not BLOCKERs.
