---
type: method
full_name: First-Principles Decomposition
short_anchor: M10-FirstPrinciples
mandatory: false
applies_to_categories:
- A
- B
- C
default_for:
- A
triggered_by_signals:
- from first principles
- ground up
- why does this exist
pairs_well_with:
- M04
escape_criterion: Stop at 2-3 decomposition layers; further produces no new structure
slots: {}
id: M10
file: modules/methods/m10-first-principles.md
---

# M10 — First-Principles Decomposition

```markdown
### Method: First-Principles Decomposition

**What it is:** You decompose the research question into its most basic,
empirically or logically fundamental components, refusing to accept any
intermediate concept without justification. Then you rebuild the analysis
from these ground-level pieces upward.

**Why it is in this prompt:** Complex research questions carry inherited
vocabulary and framings that smuggle in unexamined assumptions. First-
principles decomposition forces each conceptual layer to earn its place.

**How to apply it — step by step:**
1. Write the research question in plain language.
2. For every noun or adjective in the question, ask: "What is this
   *really* — at the most fundamental level?" Replace the term with its
   decomposed components.
3. Iterate until the question is expressed only in terms of directly
   observable or logically necessary components.
4. Answer the decomposed version. Then translate back up to the original
   vocabulary, noting where the translation introduces assumptions.

**When to stop / escape criterion:** Stop decomposing when further
decomposition would no longer reveal new structure — typically after 2–3
layers.

**Example trigger in this research context:** The question "Is
[PLATFORM] a successful product?" decomposes into: what defines
"success" → revenue? adoption? retention? strategic position? — answer
each separately, then reassemble.
```
