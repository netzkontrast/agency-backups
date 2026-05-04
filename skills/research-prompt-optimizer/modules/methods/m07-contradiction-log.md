---
type: method
full_name: Contradiction Log
short_anchor: M07-ContradictionLog
mandatory: false
self_applicable: true
self_applied_phase2:
  sub_phase: '4.1'
  hook_role: Scan parsed intent for internal inconsistencies (depth ↔ output_format,
    scope ↔ priors, etc.). Findings logged to meta-prompt.contradictions[] and surfaced
    in plan view.
  depth_active:
  - standard
  - exhaustive
applies_to_categories:
- A
- B
- C
default_for:
- B
- C
triggered_by_signals:
- conflicting reports
- contradictions
- disagreement
pairs_well_with:
- M06
- M09
escape_criterion: No ceiling. If log >10 entries, consider the research question may
  be ill-posed
slots:
  claim_x:
    type: agent_runtime_fill
    description: First conflicting claim
    required: true
  claim_not_x:
    type: agent_runtime_fill
    description: Counter-claim
    required: true
id: M07
file: modules/methods/m07-contradiction-log.md
---

# M07 — Contradiction Log

```markdown
### Method: Contradiction Log

**What it is:** A dedicated running log of every contradiction, tension,
or disagreement encountered between sources. Contradictions are not
silently resolved by picking one side — they are documented and
characterized.

**Why it is in this prompt:** Autonomous research agents tend to smooth
over contradictions by picking the majority or the most recent source,
which hides real disagreement in the field from the reader.

**How to apply it — step by step:**
1. Maintain a section titled **Contradiction Log** in your working notes.
2. For each contradiction, record: (a) the two (or more) conflicting
   claims, (b) the sources, (c) what you believe is the source of the
   disagreement (methodology, time period, definitional mismatch, genuine
   empirical dispute).
3. In the final output, include a synthesized version of the Contradiction
   Log as its own section.
4. For each logged contradiction, state what additional evidence would
   resolve it.

**When to stop / escape criterion:** No ceiling — log all contradictions
discovered. If the log exceeds 10 entries, consider whether the research
question itself is ill-posed.

**Example trigger in this research context:** If Source A says
"{{claim_x}}" and Source B says "{{claim_not_x}}", log both with context
rather than silently picking one.
```
