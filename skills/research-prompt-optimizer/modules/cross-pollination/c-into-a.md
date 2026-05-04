---
type: cross_pollination
inject_into_category: A
source_category: C
full_name: Hypothesis Half-Life Audit
selected_when: category == A
slots: {}
id: c-into-a
file: modules/cross-pollination/c-into-a.md
---

# Cross-Pollination: Category C → Category A

> Inject into an **Exploration** prompt (primary = A). Guards against
> the core A failure mode that emerges in the *medium* run: a
> hypothesis branch that survives early falsification gets re-used
> implicitly across later searches as a foundational assumption,
> without ever being re-tested.

## Paste-Ready Injection — One Step (minimum) into the Steps section

```markdown
### Step [i.c] — Hypothesis Half-Life Audit (cross-pollination from Category C)

This step imports one lifecycle discipline from Category C because
even within a one-shot exploration, a hypothesis that survived
falsification at minute 5 of the run is often treated as established
truth at minute 45 — without anyone re-running the disconfirmation
attempts on it. That is exactly the assumption-decay failure mode of
long-running research, compressed.

Perform the following whenever a hypothesis has been **active for
three or more search iterations** without re-test:

1. **List foundational hypotheses.** Write down each hypothesis that
   the current line of search is implicitly assuming. Not the active
   working hypothesis — the *implicit* ones, the ones that earlier
   branches resolved into.

2. **Define a decay test per hypothesis.** For each implicit
   hypothesis, write a one-sentence concrete test that would tell
   you it has decayed. Format: *"Hypothesis [H] decays if a search
   for [QUERY] returns [PATTERN]."*

3. **Run the decay tests.** Execute each. If any test fires (returns
   the decay pattern), halt the current branch, re-open the
   hypothesis, and re-run Method M01 (Falsification) on it from
   scratch. Do not patch around the failure.

4. **Log the audit.** Add a **Hypothesis Half-Life Audit** entry to
   the working notes recording: hypotheses tested, tests run, results,
   any decay detected. This entry is included in the final output's
   Methodology Note.

5. **Do not hybridize.** The hypothesis tree (Category A core)
   remains the primary structure. This audit is an internal
   consistency check, not a re-organization of the tree.
```

## When to Apply

Trigger after every third search iteration, or whenever a tentative
conclusion stabilizes. Cost: 2–4 audit queries per trigger. Benefit:
catches the "stale-hypothesis-as-foundation" failure that exploration
prompts otherwise hit only after the synthesis is already drafted.
