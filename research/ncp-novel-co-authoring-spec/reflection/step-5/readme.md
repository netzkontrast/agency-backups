# Step 5: M13 Adversarial Query Expansion

**Method Used:** Adversarial Query Expansion (M13)

## Workbook & Findings
In this step, I evaluated whether my autonomous query expansion effectively prevented local-minimum lock-in during the research phase.

- The expansion was highly effective on the Adjacent and Opposing axes. By searching for *why* agent specs fail (Opposing), I recognized the necessity of property-based testing and strict conformance language. This elevated `SPEC.md` from a generic markdown guide to a rigorous, Gherkin-backed technical specification.
- The Orthogonal axis (Tabletop RPG engines) did not yield actionable architectural changes for this specific prompt, but successfully functioned as a blind-spot check.
- Overall, M13 prevented the research from merely regurgitating standard Dramatica or Anthropic tutorials.

## Artefact Links
- [M13 Query Expansion Efficacy](./artifacts/M13-query-expansion-efficacy.md)
