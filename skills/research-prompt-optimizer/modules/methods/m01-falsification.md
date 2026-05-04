---
id: M01
type: method
file: "modules/methods/m01-falsification.md"
full_name: "Falsification (Karl Popper's Disconfirmation Principle)"
short_anchor: "M01-Falsification"
mandatory: false
applies_to_categories: [A, B, C]
default_for: [A]
triggered_by_signals: ["prove", "show that", "validate"]
pairs_well_with: [M02, M08]
escape_criterion: "≥3 orthogonal disconfirmations OR contra-evidence >20% of pool"
when_to_choose_short: "When you have a hypothesis to falsify"
self_applied_phase2:
  sub_phase: "4.2"
  hook_role: "After category cascade decides, run one counter-pass: 'what signals would falsify this routing?' Escalate to askuser if non-trivial counter-signals exist."
  depth_active: ["standard", "exhaustive"]
slots:
  hypothesis:
    type: agent_runtime_fill
    description: "The current hypothesis being tested as a falsifiable statement"
    required: true
  disprove_phrase:
    type: agent_runtime_fill
    description: "Search phrase designed to surface counter-evidence"
    required: true
  failure_mode_phrase:
    type: agent_runtime_fill
    description: "Phrase capturing the failure case"
    required: true
---

# M01 — Falsification (Karl Popper's Disconfirmation Principle)

> **v3.0 sample module.** All three slots are `agent_runtime_fill` —
> Phase 2 does NOT ask the user about hypothesis content. The
> rendered prompt contains `{{hypothesis}}` etc. as literal placeholder
> text, with a one-line directive that the agent fills these during
> the run.

## Rendered Block (composed into the research prompt)

```markdown
### Method: Falsification (Karl Popper's Disconfirmation Principle)

**What it is:** Instead of searching for evidence that supports a
hypothesis, you actively search for evidence that would refute it. A
hypothesis only earns credibility after surviving serious attempts to
break it.

**Why it is in this prompt:** Confirmation bias is the dominant failure
mode of autonomous research agents. Without explicit falsification
steps, you will tend to surface supporting evidence and ignore or
under-weight contradicting evidence.

**How to apply it — step by step:**

1. Before searching, write down the hypothesis you are testing as a
   falsifiable statement (one that can, in principle, be proven wrong
   by observable evidence). In this prompt, you generate the hypothesis
   as part of the Reason phase that selects this method; refer to it as
   `{{hypothesis}}` when restating, but write the actual statement in
   your working notes.

2. For every supporting piece of evidence you find, execute a **matched
   disconfirmation query** — a search specifically designed to surface
   the strongest counter-evidence. Generate two query phrasings during
   the Reason phase: one of the form `{{disprove_phrase}}` (a phrase
   that would directly refute the hypothesis) and one of the form
   `{{failure_mode_phrase}}` (the failure case for the same hypothesis).

3. Weight disconfirmation attempts equal to or higher than confirmations
   in your final synthesis.

4. If no serious disconfirmation attempt surfaced any counter-evidence,
   explicitly state in your Observe phase: *"This hypothesis survived
   N disconfirmation queries."* If counter-evidence surfaced, mark the
   hypothesis as **contested** and document both sides.

**When to stop / escape criterion:** Stop applying M01 to a single
hypothesis when it has survived **at least three orthogonal
disconfirmation queries** OR when contradicting evidence exceeds 20%
of the total evidence pool — whichever comes first.

**Example trigger in this research context:** When the active method
in your Reason phase is `[M01]`, you generate `{{hypothesis}}` (a
falsifiable claim) and run searches phrased like `{{disprove_phrase}}`
and `{{failure_mode_phrase}}` before committing to confirmation
searches. The placeholders are filled by you, the executing agent, at
the moment you select M01 — not in advance.
```

---

## Notes on the Slot Treatment (v3.0 vs v2.1)

In v2.1 this method block had `[BRACKETED]` placeholders that the user
was implicitly expected to fill in advance — leading to either pre-
specified hypotheses (defeats the exploratory purpose) or vague
`[HYPOTHESIS PLACEHOLDER]` strings the agent ignored.

In v3.0 the three slots are typed as `agent_runtime_fill` in the
catalog. The rendered prompt makes this **explicit to the executing
agent**: it tells the agent *"you generate these placeholders during
your Reason phase, not in advance"*. This is honest about the workflow
and prevents both the user-side over-specification and the agent-side
ignore-the-placeholder failure mode.

## Phase 2 Behaviour

When M01 is selected (default for Cat-A, or signal-word-triggered
elsewhere), Phase 2:

- Adds M01 to `selected_methods` in the meta-prompt.yaml
- Does **NOT** ask the user any questions about M01 (no slots to fill)
- Does **NOT** populate `slot_fills` for M01 (the slots are runtime-only)

The rendered block above goes into the research prompt verbatim, with
no substitution at composition time. The `{{hypothesis}}` etc. literal
strings remain as placeholders in the rendered Markdown, with the
prose around them telling the agent what to do.
