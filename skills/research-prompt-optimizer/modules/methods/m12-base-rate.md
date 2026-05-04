---
type: method
full_name: Base-Rate Anchoring
short_anchor: M12-BaseRate
mandatory: false
applies_to_categories:
- A
- B
- C
default_for:
- B
triggered_by_signals:
- how common is
- typical rate
- how often
pairs_well_with:
- M04
- M06
escape_criterion: Apply to every numerical frequency/probability claim. Skip pure
  qualitative
slots: {}
id: M12
file: modules/methods/m12-base-rate.md
---

# M12 — Base-Rate Anchoring

```markdown
### Method: Base-Rate Anchoring

**What it is:** For every frequency, probability, or prevalence claim, you
anchor it against the **base rate** of the relevant reference population.
Specific cases are interpreted against general rates, not in isolation.

**Why it is in this prompt:** Representativeness bias causes research to
weight vivid specific examples over statistically-grounded base rates.
Anchoring reverses this by making the base rate primary.

**How to apply it — step by step:**
1. For every probability / frequency / "how common" claim, identify the
   **reference population** the claim is made against.
2. Find the base rate in that reference population.
3. State the specific claim **explicitly relative to** the base rate:
   "2x the base rate", "well below the base rate", "within the base-rate
   range".
4. If no base rate can be found, flag the claim as **unanchored**.

**When to stop / escape criterion:** Apply to every numerical frequency or
probability claim. Skip for purely qualitative observations.

**Example trigger in this research context:** "Company X had
[PLACEHOLDER] failures" is meaningless without the base rate: what is
the failure rate in comparable companies of similar size, industry,
and time period?
```
