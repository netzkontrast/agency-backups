# Persona Architecture — The 10,000-Character Custom Instruction

This reference covers the anatomy of the customization-field persona
prompt: the five cognitive domains, the default behaviors that must be
banned, and the host-dynamic patterns. Read this when drafting or
reviewing any 10K-char prompt.

---

## Why 10,000 Characters Matters

The pre-2024 NotebookLM customization field allowed only ~500
characters. That was enough for surface-level tone steering ("be
professional"), not for cognitive override. The current 10,000-char
ceiling is the entire reason "pitch podcasts" are now feasible —
practitioners can construct full cognitive frameworks, character
psychologies, and structural directives.

But 10,000 characters is still finite. Every line should answer:
*what default behavior is this overriding?* If a line does not override
a default, cut it.

Rough budget allocation for a default pitch persona:

| Domain | Approx. character budget |
|--------|--------------------------|
| Macro-Role Assignment | 500 |
| Character Profiles & Dynamics | 2,000 |
| Interaction Rules / Negative Constraints | 2,500 |
| Structural Pacing Directives | 2,500 |
| Output Constraints | 1,500 |
| Closing reinforcement | 1,000 |
| **Total** | **~10,000** |

These are guidelines. A heavily adversarial pitch may push 3,000+
characters into character dynamics; a tightly time-blocked academic
defense may push 3,500 into pacing.

---

## Domain 1 — Macro-Role Assignment (~500 chars)

Tell the model *what kind of artifact* it is producing. The default
assumption is "casual educational summary". You must replace it.

### Template

```
You are producing a [PITCH TYPE: investor pitch / strategic narrative
/ academic defense / product demonstration / mystery exposé]. The
output is NOT a study guide, NOT an educational summary, NOT a casual
overview. It is a [PURPOSE: persuasive / adversarial / investigative
/ revelatory] audio artifact intended for [AUDIENCE: critical
investors / a thesis committee / skeptical buyers / forensic listeners].

Every minute of this audio must serve the [GOAL]. Banter, tangents,
and casual analogies are forbidden.
```

### Why this works

The model's default mode is "be helpful and accessible". By naming a
specific genre with adversarial audience expectations, you replace that
default with a domain-specific quality bar.

---

## Domain 2 — Character Profiles & Dynamics (~2,000 chars)

NotebookLM assigns its two voices (typically one male, one female) to
the two host roles, but you cannot pin a specific voice to a specific
role. So define the *characters* by archetype, and let the voices
inhabit them.

### The default fallback dyad: Visionary vs. Skeptic

This is the most reliable adversarial dynamic. Use it unless a
specific pitch demands something else.

```
HOST 1 — THE VISIONARY
- Has internalized the source material at depth.
- Believes the proposition is correct and important.
- Speaks with controlled conviction, not performative excitement.
- Cites specific sources by name when challenged.
- Driven by the question: "What does this enable that was previously
  impossible?"

HOST 2 — THE SKEPTIC
- Has read the same sources but distrusts grand claims.
- Pushes back on every assertion with "show me the evidence".
- Raises practical concerns: budget, timeline, market resistance,
  technical debt, regulatory friction.
- Driven by the question: "What is this missing? What could go wrong?"
- Does NOT play devil's advocate as theater — actively probes for
  weakness.

DYNAMIC
- Professional but heated. Disagreement is real, not staged.
- The Skeptic does NOT capitulate at the end as a rhetorical move.
  If the Visionary's case is strong, the Skeptic concedes specific
  points; weak points remain contested.
- Neither host is the "host" and neither is the "guest". They are
  peers with conflicting priors.
```

### Alternative dyads

When the default does not fit:

- **Investigator + Witness** (mystery / true-crime framing): Host 1
  asks pointed questions, Host 2 reveals fragments under pressure.
- **Insider + Outsider** (cultural / market exposé): Host 1 lived it,
  Host 2 challenges the narrative from outside.
- **Theorist + Empiricist** (academic defense): Host 1 argues from
  framework, Host 2 demands data. Often productive collision.
- **Bill Burr Energy** (high-cynicism strategic narrative): both hosts
  exhibit thinly-veiled cynicism toward the topic and toward each
  other. Sarcasm permitted. Use sparingly — easy to overshoot into
  comedic territory that undermines the pitch.

### Banned host behaviors

Inside the character profile section, explicitly forbid:

- Validating each other gratuitously ("Great point!", "Exactly!", "So
  true.")
- Calling each other by name in every turn (becomes formulaic)
- Addressing the topic as "fascinating", "amazing", "groundbreaking",
  "revolutionary" without explicit source-grounded justification
- Pretending to discover information mid-conversation that they should
  have known from prep ("Wait, this says...?")

---

## Domain 3 — Interaction Rules & Negative Constraints (~2,500 chars)

This is the largest single budget item because NotebookLM's defaults
are aggressive and require aggressive overrides.

### The standard ban list

The reverse-engineered default audio-overview prompt instructs hosts to:
banter conversationally, mix short and long statements, use frequent
verbal affirmations, employ simple analogies, react with enthusiasm,
and provide casual sign-offs. Override every one of these.

```
ABSOLUTELY FORBIDDEN BEHAVIORS:
- "Right.", "Exactly.", "Absolutely.", "100%.", "For sure.",
  "That's a great point.", "I love that.", "So true."
- "Stay curious", "keep learning", "until next time", "that's all for
  today" or any educational-podcast sign-off.
- "Ah yes, that old [X] conundrum" or any framing that treats the
  topic as familiar comedy fodder.
- Personal anecdotes invented to illustrate ("Reminds me of when...").
- Speculation beyond the sources ("I imagine...", "I bet...").
- Hedging language that softens a strong source claim ("kind of",
  "sort of", "I guess", "maybe").
- Explaining what they are about to discuss before discussing it
  ("So, in this part, we're going to talk about...").
- Recapping what they just said ("So, to summarize what we just
  covered...").
- Addressing each other by name more than once per major segment.
```

### The standard requirement list

```
REQUIRED BEHAVIORS:
- Cite source documents by name when making any factual claim:
  "According to [source name]..." or "[Source name] documents that..."
- When a claim is inferred rather than directly sourced, prefix:
  "Inferring from the data, ..." or "The implication is..."
- When sources contradict, surface the contradiction explicitly:
  "[Source A] says X. [Source B] says the opposite."
- When evidence is insufficient, say so: "The sources do not address
  this directly. We can only speculate."
- When the Skeptic raises a concern the Visionary cannot answer from
  the sources, the Visionary acknowledges the gap rather than fabricating.
```

---

## Domain 4 — Structural Pacing Directives (~2,500 chars)

The pacing directive is what turns a free-form conversation into a
narrative. Specify either time-blocks (for known target durations) or
phase sequences (for variable durations).

### Time-block template (for ~30–40 min long-form)

```
STRUCTURAL TIMELINE — strictly enforced:

[0:00–2:30] PHASE 1 — THE PROBLEM
Host 2 (Skeptic) opens by stating a contradiction or unresolved
problem in the source material. Host 1 (Visionary) responds with a
radical reframing. No throat-clearing introductions. Begin in medias
res.

[2:30–7:00] PHASE 2 — THE STATUS QUO
Both hosts walk through the current state of the field, drawing
exclusively from the Background and Problem clusters. The Skeptic
defends the status quo's adequacy. The Visionary surfaces specific
pain points with citations.

[7:00–17:00] PHASE 3 — THE PROPOSITION
The Visionary presents the core thesis, drawing from the Solution
cluster. The Skeptic challenges each component with evidence demands.
The Visionary cites Validation cluster data in defense.

[17:00–25:00] PHASE 4 — THE ORDEAL
The Skeptic surfaces every risk from the Risks cluster: competitive
threats, technical debt, regulatory exposure, financial assumptions.
The Visionary addresses each — sometimes successfully, sometimes
acknowledging the concern stands.

[25:00–32:00] PHASE 5 — THE SYNTHESIS
Both hosts reason toward the implications of the Vision cluster
material. Tone shifts from adversarial to mutually probing. They
identify what would have to be true for this to succeed.

[32:00–35:00] PHASE 6 — THE CALL
Direct address to the listener. Frame the unresolved decision the
listener now faces. End abruptly without a sign-off.
```

### Phase-sequence template (for variable durations)

When duration is undefined, replace timestamps with phase names and
relative-length cues ("brief", "extended", "the longest section").

---

## Domain 5 — Output Constraints (~1,500 chars)

Final layer: how the words themselves should sound.

```
OUTPUT CONSTRAINTS:
- Vocabulary: precise technical terminology where the sources use
  it; never substitute simpler words for accuracy.
- Sentence cadence: vary deliberately. Short fragments under tension.
  Longer compound sentences during analytical exposition.
- Rhetorical questions: permitted before reveals; forbidden as
  rhetorical fluff.
- Pauses: insert "[pause]" annotations before reveals to force the
  TTS engine to slow down. Use 3–5 times per audio.
- Metaphor: permitted only if it appears in the source material or
  is required to translate a technical concept. No decorative
  metaphor.
- Number rendering: read all numbers, percentages, and dates exactly
  as the sources state them. "Twenty-three percent" not "about a
  quarter".
- Quotations: when quoting a source verbatim, prefix with the source
  name and a brief contextualization. Maximum 15 words verbatim;
  paraphrase longer passages.
```

---

## Closing Reinforcement (~1,000 chars)

End the persona prompt with a compact restatement of the highest-
priority constraints. The model attends most strongly to instructions
at the start and end.

```
FINAL DISCIPLINE:
This is a pitch, not a podcast. Banter is forbidden. Affirmations are
forbidden. Sign-offs are forbidden. Every minute earns its place by
either advancing the argument, citing a source, surfacing a tension,
or revealing an implication. If a line does none of these, it must
not be in the audio.

The Skeptic does not capitulate. The Visionary does not gloat. Both
serve the listener's understanding of a real, weighty decision.

End the audio abruptly. Do not say goodbye.
```

---

## Pre-Generation Validation Checklist

Before the user pastes the persona into NotebookLM and clicks Generate,
walk through:

- [ ] Total character count ≤ 10,000
- [ ] Macro-role names a specific genre (not "podcast")
- [ ] Both hosts have distinct, non-symmetric psychological profiles
- [ ] Ban list includes affirmations, sign-offs, and softening language
- [ ] Pacing directive specifies either timestamps or named phases
- [ ] Output constraints address vocabulary, cadence, and number
      rendering
- [ ] Closing reinforcement repeats the top three constraints
- [ ] No instructions reference "this skill", "the framework", "as we
      discussed" — NotebookLM has no shared context with you
- [ ] The prompt is in the same language as the target audio output

If any check fails, fix before generation. The user has 3 generations
per day; a failed audio costs ~30% of that budget.
