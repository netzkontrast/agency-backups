# M01 — Falsification (Karl Popper's Disconfirmation Principle)

## Hypothesis under test

> *"Per-term frontmatter is sufficient to power scenario-keyed lookup without a separate scenario index file."*

This is the design hypothesis at the heart of [`task.md § Target Architecture`](../../../tasks/015-integrate-dramatica-ncp-skills/task.md). If it survives, Task 015 plan steps 5–9 are correctly scoped. If it fails, the navigator suite needs an additional offline `scenario-index.json` build pass, which would expand plan step 8 by ~30%.

## Disconfirmation conditions identified in `task.md` Pre-Work

The Task itself names two falsification triggers; we re-state them and test against the kickoff evidence.

1. **Median scenarios-per-term > 8.** Per-term frontmatter exceeds the cap, the schema can no longer hold the data flat, and the navigator must precompute an index.
2. **Scenarios cross-reference each other** (e.g. *"Scene 12 invokes Crucial Element under the Organist's Refrain pattern"*). Per-term frontmatter is the wrong shape for graph queries.

## Kickoff evidence

| Trigger | Kickoff measurement | Verdict |
|---|---|---|
| Median scenarios-per-term | ≈ 2.4 (per `synthesis/scenario-survey.md § Aggregate`) | **Trigger does not fire.** Well below the 8-cap. |
| Hottest term scenario count | 4–5 (Crucial Element + the four high-frequency Element pairs) | **Trigger does not fire.** Within cap. |
| Cross-scenario references in the eleven scenarios | 0 found in the kickoff scenario set | **Trigger does not fire.** All eleven scenarios are categorical, none cross-reference. |

## Verdict

**Hypothesis survives the kickoff.** Per-term frontmatter is sufficient for the lookup workload defined by the eleven personas-scenarios. The schema's `scenarios: ≤8` constraint is comfortable.

## Pre-commitment

If the **real** per-term tagging in Task 015 plan step 6 produces a median >5, the M01 contingency triggers automatically: Plan step 8 expands to add `tools/dramatica-nav/scenario-index.py` (compiles `scenario-index.json` from per-term frontmatter; `nav.py by-scenario` reads the index instead of walking files). The contingency is recorded here so Step 6 can flip the design without Step 8 needing rework.

## Honest framing

The kickoff survey is first-pass. It is plausible that downstream tagging exposes hot terms with 6–8 scenarios that the survey under-counted. The hypothesis remains *more likely than not* to survive — but the contingency is cheap (one more script of ~80 lines) and not dropping it from the plan is the conservative choice.

## What this falsification does *not* test

- The performance/token-cost claim (M01 hypothesis is **structural**: can the data fit; it is not the **performance** hypothesis: does navigator-path beat prose-path by ≥60%? Performance is tested at Task 015 plan step 12 benchmark, not here).
- The cross-skill-ID hypothesis (resolved by M07; see [`M07-contradiction-log.md`](./M07-contradiction-log.md)).
- The persona-set sufficiency (whether two personas Anna + Otto cover the user's real use cases is an authorial judgement, not a falsifiable claim — testable only by use).
