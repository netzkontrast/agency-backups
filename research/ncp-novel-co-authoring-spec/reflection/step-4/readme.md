# Step 4: M10 First-Principles Decomposition

**Method Used:** First-Principles Decomposition (M10)

## Workbook & Findings
In this step, I reviewed the Glossary in `SPEC.md` to ensure that overloaded terms across the 5 research tracks were broken down to their fundamental components rather than silently conflated.

- I audited the terms 'Scene', 'Story', and 'Throughline'.
- The decomposition of 'Scene' was particularly successful. By recognizing that NCP does not have a native "Scene" entity but instead uses `moments` under the `storytelling` key, and `storybeats` (events) under the `subtext` key, I prevented the specification from directing agents to write to non-existent JSON paths.
- The glossary accurately reflects these multi-track disambiguations.

## Artefact Links
- [M10 Decomposition Audit](./artifacts/M10-decomposition-audit.md)
