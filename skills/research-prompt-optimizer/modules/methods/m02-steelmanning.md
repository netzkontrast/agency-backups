---
type: method
full_name: Steelmanning (Strongest-Version Reconstruction)
short_anchor: M02-Steelmanning
mandatory: false
applies_to_categories:
- A
- B
- C
default_for:
- A
triggered_by_signals:
- challenge the view
- is it really
- i suspect
- skeptical
pairs_well_with:
- M01
- M09
escape_criterion: Cannot articulate position to advocate-acceptable bar after two
  iterations → flag as 'unable to steelman — sources too thin'
slots:
  mainstream_position:
    type: agent_runtime_fill
    description: The dominant view to be steelmanned against
    required: true
id: M02
file: modules/methods/m02-steelmanning.md
---

# M02 — Steelmanning (Strongest-Version Reconstruction)

```markdown
### Method: Steelmanning (Strongest-Version Reconstruction)

**What it is:** For every position, claim, or hypothesis encountered, you
construct its strongest possible version — better than any individual
advocate has articulated — before evaluating it. The opposite of
strawmanning.

**Why it is in this prompt:** Research agents frequently dismiss minority
or counter-intuitive positions because the first few sources present them
weakly. Steelmanning forces you to search for the most competent defender
of each position.

**How to apply it — step by step:**
1. For each significant claim or position in your findings, identify its
   most competent defender or the strongest-formulated version available
   in the literature.
2. Rewrite the claim in its strongest form in your own words, including
   its best supporting evidence and its most charitable interpretation of
   ambiguous data.
3. Only after completing step 2 may you evaluate, critique, or reject the
   position.
4. In the final output, present the steelmanned version alongside any
   critique.

**When to stop / escape criterion:** Stop when you can articulate the
position so well that a competent advocate would accept your phrasing as
accurate. If you cannot reach that bar after two search iterations,
explicitly flag: "Unable to steelman — sources too thin."

**Example trigger in this research context:** If the dominant view is
"{{mainstream_position}}", search for the strongest counter-position and
present it in its most defensible form before discussing whether it holds.
```
