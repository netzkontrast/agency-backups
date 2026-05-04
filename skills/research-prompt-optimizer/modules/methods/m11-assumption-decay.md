---
type: method
full_name: Assumption-Decay Audit
short_anchor: M11-AssumptionDecay
mandatory: false
applies_to_categories:
- A
- B
- C
default_for:
- C
triggered_by_signals:
- ongoing
- monitor
- still valid
pairs_well_with:
- M03
- M07
escape_criterion: Per checkpoint, not per search. Stop entirely only when research
  is closed
slots:
  foundational_assumptions:
    type: phase2_fill_or_runtime
    description: List of foundational assumptions; seeded from intent.priors if present,
      agent extends during run
    seed_from_intent: priors_and_constraints.known_priors
    required: false
  concrete_check:
    type: agent_runtime_fill
    description: Decay test per assumption — agent designs during run
    required: true
id: M11
file: modules/methods/m11-assumption-decay.md
---

# M11 — Assumption-Decay Audit

```markdown
### Method: Assumption-Decay Audit

**What it is:** Assumptions made at the start of a research project have
a half-life. An explicit audit step re-tests each foundational assumption
at defined checkpoints to catch silent invalidation.

**Why it is in this prompt:** In lifecycle / long-running research, the
world moves while the research runs. Market data, regulations, key
personnel, and source reliability can all shift. Without an audit step,
stale assumptions silently poison later conclusions.

**How to apply it — step by step:**
1. At the start, list every **foundational assumption** — what must
   remain true for the conclusions to hold?
2. For each assumption, define a **decay test**: a concrete check that
   verifies it is still true.
3. At each checkpoint (e.g., every week, every 500 tokens of new
   evidence, every new research sub-task), run the decay tests.
4. If an assumption fails its decay test, **halt** and re-evaluate the
   chain of conclusions that depend on it.

**When to stop / escape criterion:** Apply per checkpoint, not per search.
Stop entirely only when the research is closed out.

**Example trigger in this research context:** Foundational assumption:
"{{foundational_assumptions}}." Decay test: "{{concrete_check}}." Run this test at every
checkpoint.
```
