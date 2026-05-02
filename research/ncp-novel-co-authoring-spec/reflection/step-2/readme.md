# Step 2: M07 Contradiction Log

**Method Used:** Contradiction Log (M07)

## Workbook & Findings
In this step, I reviewed the contradictions surfaced during the research phase to ensure they were handled transparently and not silently smoothed over.

- The most significant contradiction was between the workflow's need for 8 distinct phases and NCP's limited 3-state `status` field. Instead of pretending NCP supported 8 states, I explicitly designed the workflow architecture (in `SPEC.md` §7.6 and §7.7) to poll both the `status` string AND the array lengths (e.g., checking for 16 progressions) to infer the correct phase.
- Out-of-scope concepts identified during the Cross-Pollination phase (`narrator-position`, `research`) were correctly excluded from the normative SPEC.md sections, respecting the hard constraints of the prompt.

## Artefact Links
- [M07 Contradiction Review](./artifacts/M07-contradiction-review.md)
