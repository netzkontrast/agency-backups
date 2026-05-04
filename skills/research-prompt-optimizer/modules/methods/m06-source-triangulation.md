---
type: method
full_name: Source Triangulation
short_anchor: M06-SourceTriangulation
mandatory: false
applies_to_categories:
- A
- B
- C
default_for:
- B
triggered_by_signals:
- cite sources
- verify with multiple
- cross-check
pairs_well_with:
- M07
- M12
escape_criterion: ≥3 independent confirmations OR claim minor enough for single-source
  (flag)
slots:
  claim:
    type: agent_runtime_fill
    description: The claim being triangulated
    required: true
id: M06
file: modules/methods/m06-source-triangulation.md
---

# M06 — Source Triangulation

```markdown
### Method: Source Triangulation

**What it is:** Every significant factual claim is confirmed across at
least **three independent source types** before being admitted to the
final output. Aggregators counting as one source, not three.

**Why it is in this prompt:** Single-source claims propagate errors.
Aggregator-heavy research agents are especially prone to citation chains
that all trace back to one primary source that is wrong.

**How to apply it — step by step:**
1. For every significant claim, identify the **primary source** (the
   original research, filing, dataset, or firsthand report).
2. Find at least **two additional independent sources** of different type
   (e.g., primary + secondary analysis + regulatory filing).
3. If all confirmations trace back to a single primary source, mark the
   claim as **single-source** and flag it in the output.
4. Prefer source types in this order: (a) peer-reviewed papers, (b)
   official primary documents (SEC filings, government data), (c) major
   news outlets with editorial accountability, (d) industry reports,
   (e) blog posts and social media (rarely sufficient alone).

**When to stop / escape criterion:** Stop searching once three
independent confirmations are found OR when the claim is minor enough
that single-source citation is acceptable (flag it).

**Example trigger in this research context:** If you find "{{claim}}" in
one source, your next queries must be designed to confirm or disconfirm
it from two independent channels before including it.
```
