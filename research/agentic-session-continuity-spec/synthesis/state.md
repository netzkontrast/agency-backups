# Synthesis State

**Status:** Initialized — awaiting research execution

When the executing agent begins the research task, it MUST replace this file with a
live checklist tracking every synthesis step. All steps MUST show `[x]` before the
pre-commit check can pass.

## Expected Checklist Structure (to be completed by executing agent)

```
## Research Steps

- [ ] S0 — Kickoff Reflection written
- [ ] S1 — Prior Art Ingestion complete
- [ ] S2 — Seed Queries constructed for G, H, I
- [ ] S3 — Research Execution: Spec-G sources triangulated
- [ ] S3 — Research Execution: Spec-H sources triangulated
- [ ] S3 — Research Execution: Spec-I sources triangulated
- [ ] S4 — M13 Adversarial Query Expansion: Spec-G (≥3 axes)
- [ ] S4 — M13 Adversarial Query Expansion: Spec-H (≥3 axes)
- [ ] S4 — M13 Adversarial Query Expansion: Spec-I (≥3 axes)
- [ ] S5 — Contradiction Log: C1 investigated
- [ ] S5 — Contradiction Log: C2 investigated
- [ ] S5 — Contradiction Log: C3 investigated
- [ ] S6 — Spec-G drafted (§§0–9, Reflection checkpoint)
- [ ] S6 — Spec-H drafted (§§0–9, Reflection checkpoint)
- [ ] S6 — Spec-I drafted (§§0–9, Reflection checkpoint)
- [ ] S6.a — Exploration Sanity Pass completed for each Spec
- [ ] S7 — Pre-Synthesis Integrity Check: all 7 items ✓
- [ ] S7.c — World-Change Scan executed (pre-Spec-H and pre-Spec-I)
- [ ] S8 — Final Assembly complete (12-section SPEC.md)

## Synthesis Steps

- [ ] Cross-Spec Dependency Map populated
- [ ] Source Index complete and tiered
- [ ] All Reflection History entries written (≥5)
- [ ] friction-log.md FL level declared
```
