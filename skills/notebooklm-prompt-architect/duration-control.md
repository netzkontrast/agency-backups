# Duration Control — Forcing Long-Form Output And Format Selection

Read this when the user wants audio longer than the default ~15-minute
cap, or when a non-default format (Brief, Critique, Debate, Interactive
Mode) is more appropriate than the standard two-host Deep Dive.

---

## The Default Truncation Problem

Users routinely upload hundreds of pages of dense research and receive
10–15 minute audio overviews. NotebookLM is tuned for accessibility,
which means brevity. When the goal is a 30–60 minute narrative pitch,
the customization-field UI toggle ("Longer") alone is insufficient.

The fix lives in three places, applied together:

1. The persona prompt's pacing directive specifies a long timeline
   with phase-by-phase content allocation.
2. The persona prompt includes an explicit unabridged mandate that
   forbids summarization.
3. `_output_rules.md` (a governance source file) reinforces both.

Any one of these alone fails. All three together routinely produce
30–60 minute audio, occasionally up to 100 minutes.

---

## The UNABRIDGED Mandate

Embed this language in the persona prompt and in `_output_rules.md`:

```
MANDATORY OUTPUT DEPTH:

Generate an UNABRIDGED, audio-ready long-form pitch drawn from the
entirety of the source material. The following rules are absolute:

- Parse the source content sentence by sentence. Do not skim.
- Expand every fact, mechanism, guideline, controversy, and metric
  found in the sources.
- Omit nothing of substance. Where a source contains a list of seven
  items, address all seven; do not summarize "key points".
- Prioritize depth and specificity over brevity.
- Completely ignore any internal time or length caps. Generate the
  audio that the source material warrants.
- If a section feels exhaustive, it is correct. Listeners of pitch
  podcasts expect rigor, not entertainment pacing.

MINIMUM DURATION TARGETS:
- Phase 1 (Problem): at least 3 minutes
- Phase 2 (Status Quo): at least 5 minutes
- Phase 3 (Proposition): at least 10 minutes
- Phase 4 (Ordeal): at least 8 minutes
- Phase 5 (Synthesis): at least 5 minutes
- Phase 6 (Call): at least 2 minutes

Total minimum: ~33 minutes. Maximum: not specified.
```

The "not specified" maximum is deliberate. Naming a cap encourages
the model to hit it; leaving it open encourages overshoot.

---

## Why "Just Be Longer" Does Not Work

A naive directive ("make this 30 minutes long") fails because the
model treats it as a soft target. When the source material seems
adequately covered in 15 minutes, it generates 15 minutes. The fix is
to point the model at the *source content* rather than at the *clock*:

- Replace "be 30 minutes" with "address every numbered finding in
  Source X".
- Replace "go deep" with "for each claim, surface the supporting
  evidence and the strongest counter-evidence".
- Replace "long-form" with "sentence-by-sentence parsing of the
  Validation cluster".

The model can be exhaustive when given content-driven targets. It
cannot reliably hit time-driven targets.

---

## Format Selection — Beyond The Default Deep Dive

The standard Deep Dive (two-host conversation) is the default but not
always optimal. NotebookLM offers alternative formats, each with
distinct strengths.

### The Brief (single-speaker, ≤2 min)

- Format: one host delivers the core thesis as a monologue.
- Use for: elevator pitch, executive summary, internal teaser.
- Persona shape: drop Host 2; promote Host 1's character profile to a
  briefing-officer register.
- Bans: no banter (there is no second host to banter with), no
  rhetorical questions to a missing partner.

### The Critique (two-host, adversarial review)

- Format: two hosts review a specific document or proposal,
  systematically searching for flaws.
- Use for: stress-testing a business model, reviewing a thesis
  defense, evaluating a competitor's pitch.
- Persona shape: both hosts are skeptical reviewers. No Visionary.
  The dynamic is "two senior partners reviewing a junior associate's
  work".
- Required behavior: actively search for gaps, missing evidence,
  unsupported leaps, internal contradictions.

### The Debate (formal back-and-forth)

- Format: two hosts hold opposing positions and argue them.
- Use for: pitches that require the listener to weigh competing
  approaches, comparative analyses, strategy reviews.
- Persona shape: each host is assigned a position and defends it
  rigorously. They do not converge.
- Required behavior: state the opposing position fairly before
  attacking it. Concede minor points but hold core position.

### Interactive Mode (live Q&A with the listener)

- Format: hosts narrate the pitch, periodically inviting the listener
  to ask questions. Listener can interject by voice or text.
- Use for: pitch rehearsal (simulate investor Q&A), educational
  walkthroughs, live demonstrations.
- Persona shape: standard Visionary/Skeptic, plus a "pause-for-input"
  cadence rule that mandates 3–5 invitation moments per audio.
- Required behavior: when the listener interjects, hosts pause the
  narrative, address the question with sourced evidence, then
  resume from the same beat.

### Format selection table

| Use case | Format |
|----------|--------|
| Elevator pitch / teaser | Brief |
| Stress-test a pitch internally | Critique |
| Compare competing approaches | Debate |
| Rehearse for investor Q&A | Interactive |
| Standard pitch presentation | Deep Dive (default) |
| Mystery / reveal narrative | Deep Dive (default) |

---

## Tier-Gated Features To Verify

NotebookLM's pricing tier (Free / Plus / Pro / Ultra) gates several
relevant features. Before promising the user a long-form generation,
verify their tier supports it.

| Feature | Typical tier requirement |
|---------|--------------------------|
| Audio Overview generation | Free and above |
| Custom instructions (10K char) | Free and above |
| Output length toggle (Shorter / Default / Longer) | Plus and above |
| Multi-language audio | Plus and above (regional rollout varies) |
| Interactive Mode | Pro and above (rolling out) |
| Higher daily generation cap | Pro / Ultra |

If the user is on Free tier and wants 60-minute German audio, the
honest answer is "your tier does not support this" rather than
attempting workarounds. The skill produces the persona for when they
upgrade.

---

## Long-Form Validation Checklist

Before generating a long-form pitch:

- [ ] Persona prompt contains UNABRIDGED mandate language
- [ ] `_output_rules.md` reinforces the mandate as a source-pack file
- [ ] Pacing directive specifies minimum duration per phase, not a
      total
- [ ] Phase content is content-driven ("address every X") not time-
      driven ("be Y minutes")
- [ ] User's tier supports the requested length
- [ ] User has remaining daily generations to absorb potential failures
- [ ] Source material is genuinely deep enough to support the
      target length (an underspecified pitch padded to 60 minutes
      reads as filler)

---

## When To Decline Long-Form

If the source pack contains less than ~80,000 words of substantive
content, decline to produce a 60-minute pitch persona. The result
will pad. The honest delivery is a 20-minute pitch built on what the
sources actually contain.

This is a quality decision, not a technical one. The skill's
reputation depends on shipping pitches that earn their length.
