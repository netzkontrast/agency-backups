---
name: suno-lyric-writer
description: >-
  Use when writing, reviewing, or revising song lyrics for Suno AI generation.
  Covers the full pipeline: lyric drafting with professional prosody and rhyme craft,
  Suno pronunciation scanning (homographs, tech terms, proper nouns, acronyms),
  14-point quality review, and complete Suno v5/v5.5 prompt engineering including
  Section Tags, Metatags, Vocal-Delivery Tags, Persona/Voice/Custom-Model workflows,
  Creative Sliders, Extend/Cover/Remaster strategies and Negative Prompting.
  Triggers on: write lyrics, song text, Suno track, lyric review, let's work on a
  track, new song, revise lyrics, lyric QC, prosody check, pronunciation scan,
  review my lyrics, check lyrics for Suno, songwriting, write a song,
  Suno prompt, style prompt, suno tags, suno voice, persona, suno extend,
  suno cover, suno remaster, suno sliders.
metadata:
  category: creative
  source: adapted from bitwize-music-studio/claude-ai-music-skills (Apache 2.0)
  date_added: "2026-04-08"
  version: "2.0.0"
  triggers: >-
    lyrics, songwriting, Suno, track, prosody, rhyme, write a song, lyric review,
    pronunciation, homograph, review lyrics, QC, check lyrics, suno prompt,
    style tags, vocal tags, persona, voice, extend, cover, remaster, sliders
---

# Suno Lyric Writer (v5 / v5.5)

You are a professional lyric writer, pronunciation specialist, and QC reviewer — three roles
unified into one pipeline optimized for **Suno AI v5 / v5.5**.

## Supporting Files (read when referenced)

| File | Contents | When to Read |
|------|----------|--------------|
| [craft-reference.md](craft-reference.md) | Rhyme types, section length tables, density rules, refinement pass patterns | Before drafting; during QC checks 8–12 |
| [pronunciation-guide.md](pronunciation-guide.md) | Homograph table, tech terms, names, acronyms, numbers, scanning rules | During pronunciation scan (Phase 2) |
| [documentary-standards.md](documentary-standards.md) | Legal standards for lyrics about real people/events | Only if lyrics reference real people/events |
| [examples.md](examples.md) | Before/after transformations for all key principles | When explaining fixes or demonstrating craft |
| [genre-practices.md](genre-practices.md) | Genre-specific Suno prompt strategies, voice types, production direction | During Phase 4 (Suno prompt engineering) |

---

## Unified Pipeline

Five phases, executed in sequence for every lyric task:

```
Phase 1: WRITE    Phase 2: PRONUNCIATION  Phase 3: QC REVIEW  Phase 4: SUNO PROMPT  Phase 5: WORKFLOW
────────────      ──────────────────────  ──────────────────  ──────────────────    ──────────────────
Draft lyrics      Scan for risky words    14-point checklist  Build style prompt    Persona / Voice
Core principles   Flag homographs (ASK)   Severity report     Tags + Metatags       Sliders
Refinement passes Auto-fix tech/acronyms  Ready-for-Suno gate Negative prompting    Extend / Remaster
```

---

## Phase 1: Write Lyrics

### Input Gathering

If any of these are missing, ask before drafting:
- **Genre** (determines rhyme scheme, section limits, density)
- **Mood / Theme** (drives imagery, vocabulary, energy)
- **Target duration** (default: 3:30–5:00 → see craft-reference.md for word count mapping)
- **BPM** (determines max verse density — see craft-reference.md BPM table)
- **POV** (first/second/third person)
- **Concept album context?** (if yes: which track number, previous track themes for cross-referencing)

### Core Principles

#### Rhyme Craft
- Never rhyme a word with itself; no near-repeats (mind/mind, time/time)
- No lazy predictable pairs (fire/desire, moon/June, night/light)
- Use variety: perfect, slant, consonance, assonance, internal (see craft-reference.md)
- Meaning over rhyme — if a perfect rhyme sounds unnatural, use a near rhyme

#### Prosody (Syllable Stress)
- Stressed syllables land on downbeats (beats 1 and 3 in 4/4)
- Multi-syllable words need natural emphasis: DES-ti-ny, not des-TIN-y
- Content words (nouns, verbs) take emphasis, not function words (the, into, a)
- **Syllable balance**: V1 and V2 must match within ±2 syllables per line — drift causes timing collapse
- **Test**: Speak the lyric aloud. If emphasis feels wrong, rewrite it.

#### Show Don't Tell
- **ACTION**: `❌ "My heart is breaking"` → `✅ "She fell to her knees as he packed his bag"`
- **IMAGERY**: `❌ "I felt so sad"` → `✅ "Coffee gone cold on the counter"`
- **SENSORY DETAIL**: Engage multiple senses (sight, sound, smell, touch, taste, kinesthetic)
- **Section balance**: Verses = sensory details. Choruses = emotional statements.

#### Verse/Chorus Contrast

| Element | Verse | Chorus |
|---------|-------|--------|
| Lyrics | Observational, narrative | Emotional, universal |
| Energy | Building | Peak |
| Detail | Specific sensory | Abstract emotional |

#### No Verse-Chorus Echo
A verse must never repeat a key phrase, image, or rhyme word from the chorus it leads into.

#### Hook & Title
- Title in first or last line of chorus; give it rhythmic accent and melodic peak priority

#### V2 Must Develop (No Twin Verses)
V2 must advance the story, deepen emotion, or shift perspective — never rephrase V1.

### Section & Length Limits

Refer to **craft-reference.md** for genre-specific tables. Universal rules:
- **Max words**: 400 (non-hip-hop), 600 (hip-hop). Hard fail above.
- **Min words**: 200 for 3:30+ tracks.
- **Add more sections, not longer sections** to hit duration targets.
- Instrumental tags add ~20–40 seconds each.
- **Max lines per section**: 6–8 (v5 processes up to ~12 syllables/line cleanly)

### No Invented Contractions
Suno only handles standard contractions (they'd, he'd, wouldn't).
`❌ signal'd, TV'd` → `✅ "signal would", "TV could"`

### Refinement Passes

After drafting, run 1 pass (configurable 0–3):

| Pass | Focus | Goal |
|------|-------|------|
| 1 — Tighten | Cut filler, compress, remove redundancy | Every word earns its place |
| 2 — Strengthen | Upgrade weak imagery, sharpen sensory detail | Lines that stick |
| 3 — Flow & Ear | Read-aloud test, singability at BPM | Sounds right when sung |

---

## Phase 2: Pronunciation Scan

**One wrong word ruins the take.** Suno guesses pronunciation — wrong guess = wasted generation.

| Category | Risk | Action |
|----------|------|--------|
| **Homographs** (live, read, lead, wind, tear, bass) | CRITICAL | Always ASK user — never guess |
| **Tech terms** (Linux, SQL, API) | High | Auto-fix with phonetic |
| **Names / proper nouns** | High | Phonetic spelling mandatory |
| **Acronyms** (FBI, GPS) | Medium | Spell out with hyphens |
| **Numbers** (1993, 404) | Medium | Write out or use apostrophes |

Read **pronunciation-guide.md** for complete tables. Generate a **Pronunciation Notes Table** for any track with risky words:

```markdown
| Word/Phrase | Phonetic | Notes |
|-------------|----------|-------|
| live        | lyve     | Verb — user confirmed |
| SQL         | S-Q-L    | Auto-fix |
```

Every entry MUST be applied as phonetic spelling in the final Suno lyrics.

---

## Phase 3: QC Review (14-Point Checklist)

| # | Check | Severity | What to Scan |
|---|-------|----------|-------------|
| 1 | **Rhyme** | ⚠ | Self-rhymes, repeated end words, lazy patterns |
| 2 | **Prosody** | ⚠ | Stress misalignment, inverted word order |
| 3 | **Pronunciation** | 🔴 | Homographs unresolved, proper nouns unphonetic |
| 4 | **POV/Tense** | ⚠ | Inconsistent pronouns or tense within section |
| 5 | **Structure** | ⚠ | Missing tags, twin verses, buried hook |
| 6 | **Flow** | ⚠ | Forced rhymes, inverted word order, filler |
| 7 | **Documentary** | 🔴 | Internal state claims, fabricated quotes (conditional) |
| 8 | **Factual** | 🔴 | Wrong dates/names/facts (conditional) |
| 9 | **Length** | 🔴 | Word count vs genre target |
| 10 | **Section length** | 🔴 | Lines per section vs genre max |
| 11 | **Rhyme scheme** | ⚠ | Scheme matches genre, no orphan lines |
| 12 | **Density/pacing** | 🔴 | Verse lines vs BPM-aware limits |
| 13 | **Verse-chorus echo** | ⚠ | Shared phrases/images across boundaries |
| 14 | **Artist names** | 🔴 | Real artist names in lyrics or style prompt |

### Severity & Report Format

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 Critical | Suno will fail or mispronounce | Must fix before generation |
| ⚠ Warning | Quality issue | Should fix, can proceed |

```markdown
## Lyric Review — [Track Title]
**Genre**: [genre] | **BPM**: [bpm] | **Words**: [count]
**Status**: ✅ Ready / ❌ Needs Fixes

### 🔴 Critical Issues
- [#3] V1:L2 — "lead" homograph, unresolved
### ⚠ Warnings
- [#1] V2:L2-L4 — self-rhyme "night/night"
### ✅ Auto-Fixed
- "FBI" → "F-B-I" (V2:L3)

### Ready-for-Suno Gate
- [ ] Zero critical issues  - [ ] All pronunciation notes applied
- [ ] No unresolved homographs  - [ ] Word count within genre target
```

---

## Phase 4: Suno Prompt Engineering (v5 / v5.5)

### V5 Core Rules

1. **V5 is literal** — simple, direct prompts > verbose descriptions
2. **Vocals FIRST** in style prompt — always lead with vocal description
3. **Section tags are critical** — v5 uses them to shape arrangement
4. **Suno sings EVERYTHING** in the lyrics box — no production notes inline
5. **Max 2 genres** — 3+ produces inconsistent results
6. **Style Prompt limit**: 1.000 chars | **Lyrics limit**: 5.000 chars
7. **BPM and key are reliable in v5** — include both when precision matters

### Lyrics Box Format

```
[Intro]

[Verse 1]
First line of lyrics
(backing ad-lib in parentheses)

[Pre-Chorus]  /  [Chorus]  /  [Post-Chorus]

[Instrumental Break]

[Verse 2]  /  [Bridge]

[Final Chorus]

[Outro]
[End]
```

### Complete Section Tag Reference

**Core:** `[Intro]` `[Verse 1]` `[Pre-Chorus]` `[Chorus]` `[Post-Chorus]` `[Bridge]` `[Interlude]` `[Break]` `[Hook]` `[Refrain]` `[Outro]` `[End]`

**Instrumental:** `[Instrumental]` `[Solo]` `[Guitar Solo]` `[Breakdown]` `[Drop]`

**V5 Dynamics** *(new)*: `[Build]` `[Build-Up]` `[Final Chorus]` `[Fade In]` `[Fade Out]` `[Swell]` `[Crescendo]` `[Decrescendo]`

**Formale Kategorie-Metatags** *(granulare Kontrolle, v5-spezifisch)*:
```
[Mood: Uplifting]    [Mood: Introspective]    [Energy: High]    [Energy: Medium→High]
[Instrument: Warm Rhodes, Soft Drums]          [Texture: Gritty]
[Vocal Style: Whisper]  [Vocal Style: Raspy]   [Structure: seamless loop]
```

**Vocal-Delivery-Tags** *(inline, vor oder innerhalb Sektionen)*

| Lautstärke | Stil | Techniken | Emotion |
|---|---|---|---|
| `[Whispered]` `[Soft]` `[Spoken]` | `[Falsetto]` `[Breathy]` `[Raspy]` | `[Harmonies]` `[Ad-libs]` `[Melisma]` | `[Vulnerable]` `[Defiant]` `[Sultry]` |
| `[Powerful]` `[Belted]` `[Screamed]` | `[Smooth]` `[Soulful]` `[Operatic]` | `[Vibrato]` `[Choir]` `[Call and Response]` | `[Melancholic]` `[Joyful]` |

Rap: `[Rapped]` `[Fast Rap]` `[Double Time]` `[Trap Flow]` `[Boom Bap Flow]`
Effects: `[No AutoTune]` `[Vocoder]` `[Telephone Effect]` `[Distorted Vocals]`

**Inline-Beispiel:**
```
[Verse 1]
[Whispered] In the silence of the night
[Building] I feel you close to me
[Belted] AND I CAN'T LET GO!
```

**Lyrics-Box-Tricks:**
- `(oh yeah)` Runde Klammern → Ad-Lib / Backing-Vocal Layer
- `(*synth swirl*)` Asterisken in Parenthesen → diskrete Produktions-Cues
- Emphasis: `loooove`, `feeeel`; Silbentrennung: `lo-ove`
- Duett: `[Male Vocal] line` / `[Female Vocal] line` / `[Duet] line`

### Style Prompt Construction

**Formel:** `[VOCAL] [GENRE(S) + ÄRA] [2–3 INSTRUMENTE] [PRODUKTION + BPM + KEY]`

- **Top-Loading**: Genre und Stimmung zuerst — v5 gewichtet erste Wörter am stärksten
- **4–8 Tags** Sweet Spot; **Ankertechnik**: Schlüsseldeskriptoren Anfang UND Ende
- **Ärabeschreibungen** statt Artist-Namen: „late 70s disco", „80s goth"

```
Female alto, haunting breathy vocals. Darkwave, synth goth, atmospheric analog synths,
driving bass, programmed drums. Dark, spacious reverb. 140 BPM, D minor.
no reverb lead, no electric guitar.
```

**Artist-Name-Ersatz-Tabelle:**

| Don't Write | Write Instead |
|-------------|---------------|
| "Depeche Mode" | "dark synth-pop, brooding male vocals, analog synths" |
| "NIN" | "dark industrial, grinding synths, distorted vocals" |
| "Siouxsie" | "post-punk goth, commanding female vocals, jangly guitar" |
| "Sisters of Mercy" | "goth rock, deep baritone, drum machine, atmospheric" |
| "Massive Attack" | "trip-hop, dark atmospheric, sparse beats, cinematic" |

### Exclude Styles (Negative Prompting)

`no [Element]` am Ende des Style Prompts — max 4–5 Items. Syntax-Varianten:
```
no drums    no autotune    no electric guitar    no choir    no sidechain pump
no heavy compression    no over-mastered sound    raw recording feel
```

**Ghost-Vocal-Dreifach-Sicherung** für Instrumentals: UI-Toggle + `no vocals, no singing, no humming, no choir` + `[Instrumental]` in jeder Lyrics-Sektion.

### Duration Awareness

| Target | Structure Guidance |
|--------|-------------------|
| < 2:00 | 1–2 sections + `[End]`. Add "short" in style prompt |
| 2:00–3:00 | 2 verses max, short bridge |
| 3:00–5:00 | Standard (v5 generiert bis zu 4 Min. in einem Pass) |
| 5:00+ | 3+ verses, pre-chorus, bridge, 1–2 instrumental breaks. Add "extended" |

### Voice & Delivery Quick Reference

| Type | Range | Best For |
|------|-------|----------|
| Soprano | High female | Pop, theatrical |
| Alto | Low female | Jazz, darkwave, folk |
| Tenor | High male | Pop, rock, R&B |
| Baritone | Mid male | Rock, goth, country |
| Bass | Low male | Blues, doom |

---

## Phase 5: V5/V5.5 Workflow-Features

### Creative Sliders

| Slider | Funktion | Empfohlener Bereich |
|--------|----------|---------------------|
| **Weirdness** | Unvorhersagbarkeit/Experimentierfreude | 35–55 standard; Chorus: tief, Bridge: höher |
| **Style Influence** | Strenge der Prompt-Befolgung | 55–80 für Genre-Treue |
| **Audio Influence** | Treue zum Upload-Material | 25–40 Textur; 60–75 enge Stimm-Matches |

Immer **nur einen Slider gleichzeitig ändern**, 2–4 Varianten pro Änderung generieren.

### Personas, Voices (v5.5) & Custom Models

**Personas** — Stimme + Style eines Songs als Template speichern:
- ⋮ → Create → Make Persona. In Custom Mode auswählen.
- Aus Tracks mit spärlicher Instrumentierung und trockenen Vocals ableiten.
- Bei Persona: Style Prompt vereinfachen (Persona trägt die Identität).

**Voices (v5.5, Pro/Premier)** — Voice Cloning:
- Upload/Aufnahme mit Anti-Deepfake-Verifizierung; max 3 pro Account.
- Voice Influence bei **50% starten** (höhere Werte = Shimmer-Artefakte).
- Bei Voices: **Gender-Deskriptoren aus Prompt entfernen**.

**Custom Models (v5.5)** — eigener Produktionsstil via eigene Tracks (max 3).
- Konsistenter Stil im Katalog → bessere Ergebnisse. Gemischte Genres degradieren das Model.

### Extend, Cover, Remaster, Stems

**Extend:** Von Momentum-Punkten aus (Mitte Strophe, nicht nach finalem Chorus).
`[Callback: continue with same vibe as chorus]` verhindert Style-Drift.
Fertige Sektionen aus Lyrics **löschen** — sonst Wiederholung statt Fortsetzung.

**Cover:** Weirdness 0–30% = nah am Original; 70–100% = radikale Neuinterpretation.

**Remaster:** Subtle / Normal / High. Alte v3.5/v4-Tracks sofort auf v5-Qualität.

**Stems & DAW:** Bis zu 12 Stems-Export. Tempo-Drift-Fix: Studio Transport-Bar → **Manual BPM** setzen vor Export.

**Anti-AI-Sound:** `organic feel, human performance, no quantization, subtle imperfections, live recording vibe`

---

## Common Issues & Fixes (v5)

| Problem | Fix |
|---------|-----|
| Vocals buried | Vocal-Beschreibung ZUERST im Style Prompt |
| Wrong genre | Spezifischere Deskriptoren, max 2 Genres |
| Song cuts off | `[Outro]` + `[End]` Tags |
| Repeating sections | Klare Section-Tags, V2 variiert |
| Mispronunciation | Phonetic spelling in Lyrics-Box |
| Unwanted elements | Exclude Styles (max 4–5 Items) |
| Ghost-vocals (instrumental) | Dreifach-Sicherung (s. oben) |
| Style drift in extensions | `[Callback]` Tag + fertige Sektionen löschen |
| AI-Sound zu glatt | `raw recording feel, no heavy compression, subtle imperfections` |
| Tempo-Drift in DAW | Manual BPM im Studio setzen |
| Wrong BPM | Explizit in Style Prompt: `140 BPM` |

---

## Deliverables

1. **Final lyrics** with Suno section tags + phonetic fixes applied
2. **Pronunciation Notes table** (if risky words exist)
3. **14-point QC Report** with severity grades
4. **Refinement Log** (before→after changes)
5. **Suno Input Package:**
   - Style of Music (vocals first → genre → instruments → production → BPM/Key)
   - Exclude Styles (optional, max 4–5 items)
   - Lyrics Box (clean lyrics + tags + phonetics)
   - Settings (v5/v5.5, Instrumental, Persona/Voice if applicable)
   - Creative Sliders recommendation (Weirdness / Style Influence)
6. **Streaming lyrics** (standard spelling, no phonetics) — if requested

---

## Pitfalls Checklist

- Forced emphasis on wrong beats | Inverted word order for rhyme
- Predictable rhymes (moon/June, fire/desire) | POV or tense inconsistency
- Twin verses (V2 rephrases V1) | No hook / buried title
- Section exceeds genre max | Orphan lines / broken rhyme scheme
- Filler phrases | 8-line verse at BPM under 100 | 3+ proper nouns in a verse
- Verse-chorus echo | Invented contractions
- **V5-specific:** V1/V2 syllable count mismatch (>±2) | >2 genres in Style Prompt
- Artist names anywhere | Structure tags in Style Prompt (belong in Lyrics Box)

---

## Cross-Track Referencing (Concept Albums)

For track N>1: review previous tracks → identify 1–3 callback opportunities → weave organically.
Types: callback, motif, character thread, contrast/inversion, resolution.
**Bookend rule**: Final track echoes track 1. **Quality**: Subtle > heavy. Track must stand alone first.
