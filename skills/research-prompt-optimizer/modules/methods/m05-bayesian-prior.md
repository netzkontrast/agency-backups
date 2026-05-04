---
type: method
full_name: Bayesian Prior Surfacing
short_anchor: M05-BayesianPrior
mandatory: false
self_applicable: true
self_applied_phase2:
  sub_phase: '4.2'
  hook_role: Before category cascade runs, write one-line prior with confidence and
    rationale. Logged to meta-prompt.routing.prior. Pairs with M01 falsification afterward.
  depth_active:
  - standard
  - exhaustive
applies_to_categories:
- A
- B
- C
default_for:
- A
triggered_by_signals:
- prior belief
- my hunch is
- gut says
- vermute
pairs_well_with:
- M08
escape_criterion: One prior at start, one updated belief at end. Do not inflate to
  per-step
auto_select_when: intent.priors_and_constraints.known_priors is not null
slots:
  expected_finding:
    type: phase2_fill
    description: User's prior — what they expect the answer to be
    required: true
    fill_from_intent: priors_and_constraints.known_priors
    fill_from_intent_required: false
  prior_reason:
    type: phase2_fill
    description: Why the user holds this prior
    required: true
    fill_from_intent: null
    ask_user_if_missing:
      question: Warum dieser Prior? Eine Zeile reicht.
      type: free_text
id: M05
file: modules/methods/m05-bayesian-prior.md
---

# M05 — Bayesian Prior Surfacing

```markdown
### Method: Bayesian Prior Surfacing

**What it is:** Before gathering evidence, you state explicitly what you
believe the answer probably is and how confident you are. New evidence
then updates these priors in a way the reader can audit.

**Why it is in this prompt:** Without surfaced priors, readers cannot tell
whether the research confirmed what the researcher already believed
(confirmation theater) or genuinely updated the belief. Surfacing priors
turns the research into a legible update process.

**How to apply it — step by step:**
1. At the start, write a **Prior Statement**: "Before investigating, my
   rough expectation is that [X] with confidence [LOW / MEDIUM / HIGH]."
2. Include **why** — what in the question, the framing, or general
   knowledge produces that prior.
3. After evidence-gathering, write an **Updated Belief**: "After
   investigation, my belief is [Y] with confidence [LOW / MEDIUM / HIGH].
   The update from prior is [MINOR / MODERATE / MAJOR]."
4. If the update is MAJOR, flag it: it indicates the initial framing was
   wrong, which may matter for the reader.

**When to stop / escape criterion:** One prior statement at the start,
one updated belief at the end. Do not inflate into per-step tracking.

**Example trigger in this research context:** "My prior is that
{{expected_finding}}. I hold this with medium confidence
because {{prior_reason}}."
```
