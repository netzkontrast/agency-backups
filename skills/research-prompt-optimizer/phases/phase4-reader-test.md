# Phase 4 — Reader Test (Detail Spec)

This is the lazy-loaded detail document for Phase 4. The thin
SKILL.md describes Phase 4 in summary; this file holds worked
patterns, edge cases, and verdict thresholds.

**Status (v3.3):** Phase 4 is **opt-in, default OFF**. The audit
body described in this document only runs after the user explicitly
selects "Ja — Audit laufen lassen" at the Phase 4 opt-in gate
(SKILL.md → Phase 4 → Algorithm step 0). On "Nein" the pipeline
skips directly to Phase 5 — none of the steps below execute.

## Purpose

The rendered research prompt will be read by an external agent that
has none of:
- The Phase 1 askuser dialogue
- The intent.yaml or meta-prompt.yaml
- Conversation context with the user
- Any of the skill's catalog vocabulary

Phase 4 audits the rendered prompt **as if** Claude were that
external agent reading it cold. The audit's job is to surface what
the prompt assumes the reader knows that the reader probably doesn't.

## Algorithm in Detail

### Step 0 — Opt-in Gate (mandatory · always runs first)

The audit body (steps 1–5 below) is gated by an explicit user yes.
The gate itself is mandatory and runs every time the pipeline
reaches the end of Phase 3:

```python
ask_user_input_v0([{
    "question": (
        "Reader-Test-Audit auf den gerenderten Prompt laufen lassen? "
        "(Frischkontext-Sicht, prüft Blindstellen)"
    ),
    "options": [
        "Ja — Audit laufen lassen",
        "Nein — direkt zu Phase 5 (Finalize)",
    ],
}])
```

Routing:
- **"Nein"** → skip steps 1–5 entirely. Proceed directly to Phase 5.
  No `research-prompt-audit_<slug>.md` file is written.
- **"Ja"** → continue with steps 1–5. The audit produces a written
  artefact and a post-audit fix/accept gate.

Default position: **OFF.** The gate exists because the audit is
valuable for high-stakes prompts and overkill for quick exploratory
ones; forcing it on every run creates askuser fatigue and writes
audit artefacts the user never asked for.

### Step 1 — Load and Strip

```python
from pathlib import Path
import yaml, re

rendered_path = Path("/mnt/user-data/outputs/research-prompt_<slug>.md")
text = rendered_path.read_text()

# Strip the v3.2 provenance frontmatter — the audit treats the
# prompt AS IF it had no upstream context. Module-level frontmatter
# (the second `---` block) stays.
m = re.match(r"^---\n.*?\n---\n", text, flags=re.DOTALL)
if m:
    body = text[m.end():]
else:
    body = text
```

### Step 2 — Predict 5 Reader Questions

Anchor predictions on these high-yield surfaces:

1. **Scope question.** "What's NOT in scope here?" The
   `research_question_unpacked` field exists for exactly this — if
   the rendered prompt elides it, that's a finding.
2. **Success criterion question.** "How will the agent know it's
   done?" If the prompt doesn't restate the success criterion in a
   form the agent can self-check against, that's a finding.
3. **Constraint question.** "Which sources are off-limits?" CB1
   (Source Priority) and CB3 (Output Exclusions) carry this; if
   they're vague or missing, that's a finding.
4. **Cross-pollination question.** "What technique am I supposed to
   borrow from the other category?" Cross-pollination directives
   are notoriously easy to miss in long prompts.
5. **Verification question.** "What does the final-checklist
   actually require?" The 11-item self-verification at the end
   should be readable as a checklist, not as prose.

If the depth is exhaustive, predict 7 questions instead of 5
(add: temporal-scope question, batch-cardinality question).

### Step 3 — Self-Audit Sweeps

For each predicted question, scan the rendered body and answer:

```python
finding = {
    "q": question_text,
    "predicted_answer": "what the doc seems to say (paraphrase)",
    "doc_provides": True | False,
    "finding": None | "what's missing or ambiguous",
}
```

Then three full-document sweeps:

**Ambiguity sweep.** Look for:
- Pronouns with unclear antecedents ("this", "that", "they")
- Adjectives without measurable threshold ("substantial",
  "significant", "appropriate")
- Lists that read as exhaustive but have an implicit "etc."
- Time references without anchor ("recently", "in the past few
  years")

EXCLUDE `{{slot_name}}` markers. These are `agent_runtime_fill`
placeholders the executing agent fills with concrete values during
the run. Filter them with regex before applying the sweep.

**Assumption sweep.** Look for:
- Domain jargon used without definition (acronyms, in-house terms)
- References to "the team" / "our process" / similar
  organisational context the external agent doesn't have
- Technical assumptions ("standard practice", "as expected")

**Contradiction sweep.** Look for:
- A statement and its negation in different sections
- Constraint blocks that conflict (e.g., CB1 says "EU sources only"
  and CB3 says "exclude EU regulatory texts")
- Method directives that conflict (e.g., M01 falsification vs. M02
  steelmanning applied to the same hypothesis without ordering)

### Step 4 — Verdict

```
findings = (n_question_failures, n_ambiguities, n_assumptions, n_contradictions)

if any_contradictions or sum(findings) >= 3:
    verdict = "fix-required"
elif sum(findings) >= 1:
    verdict = "fix-recommended"
else:
    verdict = "pass"
```

### Step 5 — Write Audit File

```python
from io_helpers import write_audit_md

audit = {
    "rendered_path": str(rendered_path),
    "reader_questions": [...],
    "ambiguities": [...],
    "assumptions": [...],
    "contradictions": [...],
    "verdict": verdict,
}
write_audit_md(output_dir, slug, audit)
```

Then call `present_files(audit_path)`. Then the gate askuser.

## Verdict Thresholds — Detail

| Verdict | Threshold | UX |
|---------|-----------|-----|
| `pass` | 0 findings | Audit still presented; user usually picks "Accept" |
| `fix-recommended` | 1–2 findings, no contradiction | Default option in askuser stays "Accept"; user can fix or skip |
| `fix-required` | ≥ 3 findings OR ≥ 1 contradiction | Default option in askuser is "Fix constraints / seeds" |

The threshold is advisory — the user decides. The audit's job is to
surface, not to enforce.

## Edge Cases

### Bilingual prompts (intent.language != "en")

The rendered prompt is in English with a language warning at the top
("intent.language: de — templates remain English; agent must
translate output"). The audit runs in English regardless. Don't flag
the language switch as an ambiguity — the warning addresses it.

### Empty cross-pollination findings

If a cross-pollination directive is rendered but the predicted
reader question for "what technique to borrow" passes, the audit
should affirmatively note that — not silently move on. Format:

```
- finding: doc_provides=True; cross-pollination "B-into-A" anchored
  at section 7.2; instructions read as standalone, no prior context
  needed.
```

### Audit on a re-rendered prompt (`_v2.md`, `_v3.md`)

The audit reads from the `_vN.md` file, not the base file. Verdict
files are also versioned (`research-prompt-audit_<slug>_v2.md`)
through `next_versioned_path` with kind="audit". The audit's
provenance block links `previous_version` to the prior audit.

### When the user picks "Fix intent" at the gate

This jumps all the way back to Phase 1 EXTRACT. The existing
intent.yaml is preserved; the user edits one or more slots (an
`append_revision` entry is logged on intent.yaml), Phase 1 re-emits
intent.yaml as `_v2.yaml`, Phase 2 re-runs from scratch with the
new intent. The full chain re-runs.

## Anti-Patterns

| Anti-pattern | Why it fails |
|---|---|
| Treating `{{agent_runtime_fill}}` as ambiguity | Generates massive false-positive count; user starts ignoring audits |
| Predicting questions about the skill's own architecture (modules, catalog, etc.) | The external agent has no visibility into those — questions must be about RESEARCH content |
| Auditing intent.yaml or meta-prompt.yaml directly | Phase 4 audits the RENDERED prompt; the YAMLs are scaffolding, not delivery |
| Suggesting fixes inline in the audit file | The audit surfaces findings; fixes go through Phase 2 edit branches |
| Skipping the audit when the verdict would be "pass" | The audit file is the user's evidence the audit ran — always write it |

## Worked Example

Input: `research-prompt_eu-ai-act-saas-2026.md` (rendered from the
EU AI Act test case).

Predicted questions:
1. "Which AI Act articles are out of scope for this research?"
2. "How does the agent know when the deliverable is complete?"
3. "Are paywalled EU regulatory sources allowed?"
4. "What's the cross-pollination from category C trying to teach me?"
5. "What does the final-checklist mean by 'temporal coverage adequate'?"

Suppose the audit finds:
- Q1: doc_provides=True (CB3 lists exclusions clearly)
- Q2: doc_provides=Partial (success_criterion present but not
  rendered as a checkable list)
- Q3: doc_provides=True (CB1 explicit on paywall exclusion)
- Q4: doc_provides=False (cross-poll directive renders but no
  example of what to borrow)
- Q5: doc_provides=False (final-checklist item phrased ambiguously)

Plus 1 ambiguity ("recently" without anchor in §6) and 1
assumption (acronym "GPAI" undefined on first use).

Total findings: 4 (2 question failures + 1 ambiguity + 1 assumption).
Verdict: `fix-required`.

User's likely choice: "Fix constraints / seeds" → loops back to
Phase 2.5 to tighten CB3 wording and 2.6 to add a concrete
cross-pollination example. After Phase 2 re-approval and Phase 3
re-render, Phase 4 re-audits. If verdict drops to `pass` or
`fix-recommended` and user accepts, pipeline complete.
