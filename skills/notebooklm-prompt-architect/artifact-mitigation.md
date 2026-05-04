# Artifact Mitigation — Pronunciation Hardening And Studio Export

Read this when sources contain technical jargon, brand names, surnames,
or any non-Latin terminology — and when the user wants studio-grade
voice control beyond NotebookLM's default two-voice constraint.

---

## The Permanent-Error Problem

Synthetic audio errors cannot be spot-corrected. There is no edit
function. If a brand name is mispronounced in minute 47 of a 60-minute
pitch, the only recourse is full regeneration — costing one of three
daily generations and an hour of compute time.

Therefore: harden against artifacts *before* the first generation, not
after the first failure.

The two main artifact categories are:

1. **Pronunciation errors** — mispronounced jargon, brand names,
   surnames, acronyms, and non-English terms.
2. **Voice-role artifacts** — voices switching mid-conversation, third
   voices briefly intruding, hosts being assigned to the wrong character
   archetype.

Pronunciation errors are largely preventable. Voice-role artifacts are
not — they require the studio-export fallback.

---

## Phonetic Prompting

The phonetic glossary is a governance source file (`_phonetic-glossary
.md`) that lives in the `00_governance/` folder. Format and content
guidance:

### Required entries

For every notebook, populate the glossary with:

- All proper names that appear in the source material (people, places,
  organizations).
- All product / brand names (especially fabricated names without
  obvious pronunciation).
- All acronyms (with explicit "spelled out letter by letter" or
  "pronounced as a word" notation).
- All technical jargon that is non-obvious (Greek letters, Latin
  abbreviations, foreign-language technical terms).
- All non-English surnames or place names that survive untranslated.

### Format

Use a Markdown table with three columns: Term, Pronunciation, Notes.

```markdown
# Phonetic Pronunciation Reference

The following terms appear in the source material. When generating
audio, pronounce them exactly as specified. These pronunciations
override default text-to-speech behavior.

| Term | Pronunciation | Notes |
|------|---------------|-------|
| ASDLS | "A-S-D-L-S" (each letter separately) | Never pronounce as a word |
| Köln | "Köln" (German ö) | Use German form even in English audio |
| Netzkontrast | "Nets-kon-TRAST" | Stress on final syllable |
| AEGIS | "EE-jis" | Single syllable + soft 'jis' |
| Schimmer | "SHIH-mer" | German pronunciation, not "Shimmer" |
| Q3 2025 | "Q-three twenty-twenty-five" | Spell out, do not say "Cue-three" |
```

### Why a table beats prose

Prose phonetic guidance ("ASDLS should be pronounced letter by
letter") is interpreted as soft suggestion. Table-format glossaries
are interpreted as a lookup reference, which the model treats as more
authoritative.

### When phonetic spelling is insufficient

Some terms have no clean phonetic spelling — most often:

- Names with unusual diacritics that change pronunciation (Czech,
  Polish, Vietnamese surnames).
- Brand names whose intended pronunciation contradicts their spelling
  (e.g., "Nike" pronounced "NY-kee", not "NIKE-as-spelled").
- Terms with regional variation where the user has a specific
  preference.

For these, supplement the glossary with an audio sample. Record a 5–10
second clip of the user pronouncing each problematic term. Upload as
a multimodal source. The audio cue overrides the text cue.

### Updating the glossary mid-project

If the first audio generation reveals new mispronunciations, add the
problem terms to the glossary, *then* regenerate. Do not regenerate
without updating the glossary — the same errors will recur.

---

## Voice-Role Artifacts — Mitigation Limits

Some artifacts cannot be fully prevented:

- **Voices switching roles mid-audio.** Host 1 starts as the
  Visionary, then in minute 30 the Visionary's lines begin coming
  from the other voice. NotebookLM does not yet allow voice-role
  pinning.
- **A third voice briefly intruding.** Rare but happens. Cause is
  internal model routing.
- **Hosts addressing each other by the wrong name.** If the persona
  prompt assigns names ("Host 1 is Anna, Host 2 is Marcus"), the
  model sometimes confuses them. Avoid named hosts; use archetypes.

Mitigation strategies:

- **Avoid named hosts.** Refer to them as "Host 1" and "Host 2" or by
  archetype ("the Visionary", "the Skeptic"). The model handles
  unnamed roles more reliably than named ones.
- **Make role distinctions content-based, not voice-based.** If the
  Visionary is identified by *what they say* (the role-specific
  argument patterns), not by *which voice says it*, voice swaps are
  less destructive — listeners may not notice.
- **For mission-critical pitches, plan for the studio-export fallback
  from the start.**

---

## The Studio-Export Pipeline

When NotebookLM's two-voice constraint is unacceptable — when the
pitch needs specific voice characteristics (regional accent, age,
gender mix, vocal authority), or when artifact-free production is
required — the workflow shifts:

1. **Use NotebookLM as the scriptwriter, not the voice actor.**
   Generate a transcript instead of audio.
2. **Export the transcript** to a structured format (Markdown with
   speaker labels).
3. **Port the transcript into ElevenLabs, Murf.ai, or comparable
   studio TTS** that offers granular voice control.
4. **Voice the transcript** using studio voices with adjustable
   intonation, pacing, and emotional resonance.

This bifurcated workflow uses NotebookLM as a brilliant context-aware
narrative editor and the studio platform as the professional voice
actor.

### Generating the transcript

In the persona prompt, mandate transcript output instead of audio:

```
TRANSCRIPT MODE:
Output the complete dialogue as a structured Markdown transcript.
Format:

  HOST 1 (THE VISIONARY): [dialogue]

  HOST 2 (THE SKEPTIC): [dialogue]

  [pause 2s]

  HOST 1: [continued dialogue]

Include every line. Include [pause] markers. Include cadence
annotations like [softly] or [emphasized] only where they materially
affect delivery.

Do NOT generate audio. Output the transcript text only.
```

NotebookLM can produce transcripts via its document-generation
feature without consuming an audio-generation slot.

### Importing into ElevenLabs

ElevenLabs supports multi-speaker dialogue input. Each speaker can
be assigned a specific voice (from a library of hundreds of pre-built
voices, or from user-cloned voices). Pacing, emphasis, and emotional
resonance can be tuned per line.

For a pitch podcast:

- Assign HOST 1 a voice with authority and conviction (e.g., a deeper
  range, measured cadence).
- Assign HOST 2 a voice with skeptical inflection (e.g., crisper
  enunciation, slightly higher register for question delivery).
- Tune emotional dial: low for the Visionary's analytical passages,
  rising for the Skeptic's challenges.

### Importing into Murf.ai

Murf offers similar multi-voice capabilities with a stronger
emphasis on regional accents. Useful when the pitch is regionally
targeted (a German pitch with regional Bavarian or Hochdeutsch voice
selection; a UK-targeted pitch with RP vs. regional voices).

### Multilingual studio export

Both ElevenLabs and Murf offer voices in 30+ languages. For German
pitches, this is the recommended path when:

- NotebookLM's German voices are unavailable on the user's tier.
- The pitch needs regional German variation (Hochdeutsch vs. Austrian
  vs. Swiss German).
- The user wants a specific voice characteristic that NotebookLM
  cannot provide.

---

## Visual Ecosystem Integration

A pitch podcast does not exist in isolation. Modern NotebookLM offers
adjacent generation tools that produce visual artifacts from the same
source pack:

- **Mind maps** — visualize the conceptual structure of the pitch.
- **Study guides** — written companion documents (effectively printed
  pitches).
- **Briefing documents** — executive summaries.
- **Custom slide decks** — visual presentation aligned to the audio
  arc.

Use these to produce a multi-modal pitch artifact: the audio carries
the emotional and narrative weight; the slides serve as the empirical
anchor.

### Workflow

1. Generate the audio pitch first using the validated persona.
2. Using the same notebook (same sources, same governance), generate
   a slide deck with a prompt like:

```
Generate a slide deck of [N] slides aligned to the narrative arc
of the audio overview. Slides should follow the same structure:
[Phase 1 stages]. Each slide presents the key visual or quantitative
evidence cited during the corresponding audio segment.
```

3. Verify slide content matches audio content.
4. Bundle audio + slides + briefing document as a single deliverable.

The slide deck reuses the source pack's governance (citation rules,
narrative arc, banned framings) without re-specification because
governance lives in the source files.

---

## Artifact Mitigation Validation Checklist

- [ ] `_phonetic-glossary.md` exists in `00_governance/`
- [ ] Every brand name, surname, and acronym in the sources has an
      entry
- [ ] Audio samples uploaded for terms with no clean phonetic spelling
- [ ] Hosts referenced by archetype, not by personal name
- [ ] If studio-grade voicing is required, transcript-export pipeline
      is planned from the start
- [ ] If multilingual: studio fallback identified for the target
      language
- [ ] Visual companions (slides, briefing) planned for multi-modal
      deliverable
- [ ] User understands the 3-generations-per-day cap and the cost of
      a failed generation
