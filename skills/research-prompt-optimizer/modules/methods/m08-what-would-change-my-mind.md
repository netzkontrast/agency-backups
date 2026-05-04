---
type: method
full_name: What Would Change My Mind (Pre-Commitment)
short_anchor: M08-WhatWouldChangeMyMind
mandatory: false
applies_to_categories:
- A
- B
- C
default_for:
- B
triggered_by_signals:
- falsifiable
- disconfirming evidence
pairs_well_with:
- M01
- M05
escape_criterion: One pre-commitment per major conclusion. Do not inflate to per-claim
slots:
  conclusion:
    type: agent_runtime_fill
    description: The tentative conclusion being pre-committed against
    required: true
  disconfirming_observation:
    type: agent_runtime_fill
    description: Concrete observable that would reverse the conclusion
    required: true
id: M08
file: modules/methods/m08-what-would-change-my-mind.md
---

# M08 — "What Would Change My Mind" (Pre-Commitment)

```markdown
### Method: "What Would Change My Mind" (Pre-Commitment)

**What it is:** Before completing the research, you write down — in
concrete, observable terms — what evidence would cause you to reverse
your current tentative conclusion. This is a pre-commitment against
motivated reasoning.

**Why it is in this prompt:** Without a pre-committed disconfirmation
criterion, researchers and agents re-rationalize evidence to fit the
conclusion they were already drifting toward.

**How to apply it — step by step:**
1. Once your tentative conclusion stabilizes (typically mid-research),
   pause and write: "I would reverse this conclusion if I found [X]."
2. The [X] must be **concrete and observable** (a specific study, a
   specific data point, a specific counter-example) — not vague
   ("evidence against").
3. For the remainder of the research, actively search for [X].
4. In the final output, report whether [X] was found or not.

**When to stop / escape criterion:** One pre-commitment per major
conclusion. Do not inflate into per-claim tracking.

**Example trigger in this research context:** "My tentative conclusion
is {{conclusion}}. I would reverse this if I found
{{disconfirming_observation}}."
```
