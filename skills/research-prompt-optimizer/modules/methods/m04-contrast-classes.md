---
type: method
full_name: Contrast Classes (Making Implicit Baselines Explicit)
short_anchor: M04-ContrastClasses
mandatory: false
applies_to_categories:
- A
- B
- C
default_for:
- A
triggered_by_signals:
- compared to what
- alternatives
- versus baseline
- vs
pairs_well_with:
- M12
escape_criterion: Apply to every evaluative claim; skip pure descriptive statements
slots: {}
id: M04
file: modules/methods/m04-contrast-classes.md
---

# M04 — Contrast Classes

```markdown
### Method: Contrast Classes (Making Implicit Baselines Explicit)

**What it is:** Every evaluative claim ("X is high", "Y is effective",
"Z is unusual") compares to a reference class — the "compared to what".
Contrast-class analysis forces you to name that reference class explicitly
before accepting the claim.

**Why it is in this prompt:** Implicit baselines hide the most common
research errors. "Company X grew 40%" means nothing without the contrast
class (the industry average, the previous year, similar-stage companies,
...).

**How to apply it — step by step:**
1. For every evaluative claim you consider including in the output, write
   down its implicit contrast class.
2. Search specifically for the contrast-class baseline.
3. Reformulate the claim to make the contrast explicit:
   "X grew 40%, compared to industry median of Y% over the same period."
4. If the contrast class cannot be found or is genuinely missing from the
   literature, flag the claim as "unanchored".

**When to stop / escape criterion:** Apply to every evaluative adjective
or percentage claim. Skip for pure descriptive statements.

**Example trigger in this research context:** If you encounter "adoption
rate of [X] is high", the contrast class questions are: high compared to
which competitor? Which year? Which geography?
```
