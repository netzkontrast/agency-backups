---
type: cross_pollination
inject_into_category: B
source_category: C
full_name: World-Change Check (pre + mid-batch)
selected_when: category == B
slots: {}
id: c-into-b
file: modules/cross-pollination/c-into-b.md
---

# Cross-Pollination: Category C → Category B

> Inject into an **Extraction** prompt (primary = B). Guards against
> the core B failure mode that hides in plain sight: facts treated as
> static within the temporal window are sometimes already obsolete by
> the time the synthesis is delivered, because the world moved while
> the extraction was running.

## Paste-Ready Injection — One Step (minimum) into the Steps section

```markdown
### Step [i.c] — World-Change Check (cross-pollination from Category C)

This step imports one lifecycle discipline from Category C because
a Category-B extraction implicitly treats every fact within the
temporal scope as static. For fast-moving domains (regulation, market
data, leadership, technology versions), facts harvested at the start
of a long batch may already be wrong by the end of the batch.

Perform the following at two points in the run:

1. **Pre-batch world-change scan.** Before starting the batch, run
   one targeted search for **state changes that occurred within the
   last [time-since-temporal-window-end] for each major item type
   in the input list**. Format: *"changes in [item type] [back-edge
   of temporal window]–today"*. The point is not to extend the
   temporal window, but to **flag items whose extracted values may
   already be stale** by the time the synthesis is delivered.

2. **Mid-batch world-change check.** At the halfway point of the
   batch (or every [N] iterations, whichever fires first), repeat the
   scan with focus on items already extracted. Any item whose state
   has measurably moved since its extraction goes into a
   **World-Change Annotation** column in the output schema, alongside
   the original extracted value.

3. **Annotate, do not retroactively edit.** A core B-discipline
   (Method M06 Source Triangulation) requires the extracted value at
   the moment of extraction to be preserved. World-Change Annotations
   are an additional layer; the original triangulated value remains
   the primary record, with the annotation flagging downstream caution.

4. **Do not hybridize.** This step does not turn the extraction into
   ongoing monitoring. It is a one- or two-pass check that surfaces
   staleness risk before the synthesis is delivered. If the user
   wants ongoing monitoring, route the next prompt as Category C.
```

## When to Apply

Always when the temporal scope is recent (within last 24 months) or
the domain is fast-moving (regulation, financial markets, tech
versions, personnel). Skip with explicit note for stable historical
domains. Cost: 2 additional batched searches.
