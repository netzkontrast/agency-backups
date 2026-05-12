# Methodology & Triangulation (M06)

## M06 Source Triangulation

**Topic: When should an agent update operational `readme.md` files in a multi-folder commit — per-touch, batched at pre-commit, or hybrid?**

**Query 1:** Read PRE_COMMIT.md §2 verbatim.
- *Synthesis:* The clause "EVERY folder ... MUST have its `readme.md` updated *now*, right before the commit" can be parsed two ways: (a) "right before the commit" = the pre-commit phase (batched), or (b) "now" = at every touch (per-file). The ambiguity is the entire defect.
- *Confidence:* High (text inspection).

**Query 2:** Read FRUSTRATED.md §28 (Special Triggers) verbatim.
- *Synthesis:* Explicitly names per-file readme spam as FL2 ("updating a `readme.md` for every single minor file change *instead of batching them at the pre-commit stage*"). Intent is unambiguously batched-at-pre-commit.
- *Confidence:* High.

**Query 3:** Empirical corpus survey — count readme.md touches per commit on `origin/main` since 2026-04-15.
- *Synthesis:* Of 35 sampled commits, the heavy-readme commits (top quartile: 9–33 touches) are all single batched commits; zero commits in the corpus do per-file readme-only sequencing for organic feature work. The de-facto practice is already batched.
- *Confidence:* High (mechanical evidence).

**Query 4:** Token-cost projection on a hypothetical 30-file PR touching 10 folders.
- *Option A (per-touch):* 30 × ~150 tok = ~4 500 tok of readme reload across the commit window.
- *Option B (batched-at-precommit):* 10 × ~150 tok = ~1 500 tok.
- *Option C (hybrid):* ~3 000 tok (per-touch on the 5 folders whose purpose changed, batched on the rest).
- *Synthesis:* Option B is ≈3× cheaper than A and ≈2× cheaper than C; the corpus norm matches B; FRUSTRATED.md §28 already prescribes B.
- *Confidence:* High.

## M08 What Would Change My Mind (Pre-Commitment)

- I believe Option B (batched-at-pre-commit) is the canonical cadence.
- *What would change my mind:* If the corpus showed a meaningful population of per-file readme commits OR if Option A were systematically cheaper at scale than B (e.g., when readmes carry per-file invariants the agent regenerates lazily). Neither held under the survey.

## Falsification Clause (from prompt brief)

> "Wrong cut iff any choice yields >2× token cost vs. status quo."

The status quo is the de-facto corpus norm (Option B). Option A scores 3× the cost; Option C scores 2× the cost. Option B *is* the status quo, so the criterion is trivially satisfied. The falsification clause did not fire.
