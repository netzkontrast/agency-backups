# Tracks

Three parallel evidence-gathering tracks were run during the kickoff.

## Track 1 — Corpus Inventory

**Goal.** Enumerate every term file and every theory chapter; produce a per-file row with kind, term count, and provenance.

**Method.** Explore subagent walked `skills/dramatica-vocabulary/references/*.md` (22 files) and `skills/dramatica-theory/references/*.md` (15 files), extracting heading-level data via grep. Main agent verified salient counts by direct probe (synonym index rows, dynamic-pair index rows).

**Output.** [`inventory.md`](./inventory.md). 310 terms (22 vocab files), 15 theory chapters totalling ~1010 KB.

**Confidence.** High for the per-file totals; medium for the per-kind classifications because some files mix kinds (e.g. `overview-appreciations.md` covers both story-level and per-throughline appreciations). Final classification happens in the schema authoring step (Task 013 plan step 5).

## Track 2 — Cross-Skill ID Audit

**Goal.** Find places where the four skills disagree on the *name* of the same Dramatica entity, since the ontology's whole point is to resolve those disagreements via canonical IDs + aliases.

**Method.** `grep -in` across the four `SKILL.md` files plus `ncp-author/references/canonical-vocabulary.md` for the suspect pairs (`Impact|Influence`, `Subjective|Relationship`, `Mental Sex|Problem-solving Style`).

**Output.** [`id-audit.md`](./id-audit.md). Three contradictions surface; all are *naming*, not theory.

**Confidence.** High. The contradictions are mechanical and reproducible from the greps in the session log.

## Track 3 — Scenario-Tag Survey

**Goal.** First-pass mapping of the 11 personas-scenarios to candidate term files, so Task 013 plan step 6 ("tag the top-≥40 terms") has a starting heuristic.

**Method.** For each scenario from `task.md § Personas and Working Scenarios`, identify the 1–3 vocabulary files most likely to host the matching terms, plus a rough term count.

**Output.** [`scenario-survey.md`](./scenario-survey.md). Median estimated terms-per-scenario ≈ 12 (lower bound 6, upper 25).

**Confidence.** Medium. This is intended as a *starting* heuristic, not a final tag list. The downstream authoring step (Task 013 plan step 6) will do the real per-term tagging by reading individual term sections.
