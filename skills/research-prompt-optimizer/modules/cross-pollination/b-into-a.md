---
type: cross_pollination
inject_into_category: A
source_category: B
full_name: Surviving-Branch Triangulation
selected_when: category == A
slots: {}
id: b-into-a
file: modules/cross-pollination/b-into-a.md
---

# Cross-Pollination: Category B → Category A

> Inject into an **Exploration** prompt (primary = A). Guards against
> the core A failure mode: an indefinite hypothesis tree whose
> surviving branch is never pinned to triangulated evidence, leaving
> a plausible story with no verified anchor.

## Paste-Ready Injection — One Step (minimum) into the Steps section

```markdown
### Step [i.b] — Surviving-Branch Triangulation (cross-pollination from Category B)

This step imports one extraction discipline from Category B because
an exploration that ends with a "most likely" hypothesis, without
triangulating the evidence under that hypothesis, has produced a
narrative — not a finding.

Perform the following **once the hypothesis tree has produced a
surviving branch** (a hypothesis with net-positive evidence after
falsification attempts, per Method M01):

1. **Lock a mini-schema for the surviving branch.** For the surviving
   hypothesis, write a small structured schema:
   - Claim: [one-sentence statement of the surviving hypothesis]
   - Key evidence 1: [source + finding]
   - Key evidence 2: [source + finding]
   - Key evidence 3: [source + finding]
   - Strongest counter-evidence: [source + finding]
   - Confidence: [LOW / MEDIUM / HIGH]
   - What-would-change-my-mind: [concrete future observation]

2. **Force triangulation on the top three evidence items.** Each must
   trace to at least two independent sources (primary + confirmation)
   — not aggregator-chains. If any item is single-source, flag the
   surviving branch as **single-source-supported** rather than
   confirmed. Apply Method M06 (Source Triangulation) here as if the
   primary category were B.

3. **Do not hybridize.** The hypothesis tree structure (Category A
   core) remains. This schema is attached **below** the tree in the
   output, not in place of it.
```

## When to Apply

Always, unless no branch survives. In that case, the exploration
terminates with "no hypothesis survived disconfirmation" as the legitimate
finding (see Category A inline block) and this step is skipped with an
explicit note. Cost: 1–3 additional triangulation queries.
