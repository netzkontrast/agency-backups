---
type: method
full_name: Red Team / Devil's Advocate Review
short_anchor: M09-RedTeam
mandatory: false
applies_to_categories:
- A
- B
- C
default_for:
- C
triggered_by_signals:
- steelman the opposition
- attack this
- break it
pairs_well_with:
- M02
- M07
escape_criterion: Three attack angles per major conclusion. Stop when no non-trivial
  new attack surfaces
slots:
  conclusion:
    type: agent_runtime_fill
    description: Conclusion under red-team attack
    required: true
  biased_domain:
    type: agent_runtime_fill
    required: false
  hidden_premise:
    type: agent_runtime_fill
    required: false
  competing_hypothesis:
    type: agent_runtime_fill
    required: false
id: M09
file: modules/methods/m09-red-team.md
---

# M09 — Red Team / Devil's Advocate

```markdown
### Method: Red Team / Devil's Advocate Review

**What it is:** Before finalizing the output, you switch into the role of
a hostile, competent critic whose job is to find every weakness. You
document the attacks, then either repair them or concede them.

**Why it is in this prompt:** The same cognitive process that produces
the research is poor at critiquing it. Explicit role-switching
(researcher → critic) simulates external review.

**How to apply it — step by step:**
1. After drafting the conclusions, declare: "I now switch to critic mode."
2. Attack each major conclusion from at least three angles:
   (a) source quality — are the sources strong?
   (b) logical chain — does the conclusion actually follow?
   (c) alternative explanations — is there a competing explanation for
       the evidence that is equally or more plausible?
3. Record each attack.
4. For each attack, either: (i) repair the conclusion to survive the
   attack, OR (ii) concede and soften the conclusion, OR (iii) document
   the attack as a known limitation in the final output.

**When to stop / escape criterion:** Three attack angles per major
conclusion. Stop when you cannot generate a non-trivial new attack.

**Example trigger in this research context:** Conclusion: "{{conclusion}}."
Attacks: (1) sources concentrated in {{biased_domain}}; (2) the reasoning
assumes {{hidden_premise}}; (3) alternative explanation:
{{competing_hypothesis}}.
```
