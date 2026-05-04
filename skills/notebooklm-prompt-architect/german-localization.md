# German Localization — Three-Layer Alignment + German Spannung

Read this when output language is German, when sources are mixed-
language, or when the user reports the audio reverting to English
mid-generation.

---

## The Cross-Language Failure Mode

The most common German-output bug: the audio begins in flawless
German, then somewhere in minute 8 the host switches to English mid-
sentence, sometimes returns to German, sometimes does not. Listeners
find this jarring and unprofessional.

Cause: the underlying LLM has stronger statistical pull toward
English than toward German. When the model encounters a complex
reasoning step (a long inference chain, a synthesis across sources,
a stage transition), it routes to its highest-confidence language
path — which is English. The German output is the *surface*; the
reasoning is happening in English-weighted token space.

Fix: align all three layers so the model has no English fallback
path available.

---

## The Three-Layer Alignment Protocol

### Layer 1 — System / Account Settings

NotebookLM inherits the output-language preference from the user's
Google account or from the application's own language toggle.

Steps:

1. Open NotebookLM settings.
2. Set Output Language to **Deutsch (German)** explicitly. Do not
   rely on auto-detection.
3. Verify the Audio Overview voice options show German voices
   (typically two: one male, one female).

If German voices do not appear, the regional rollout has not yet
reached the account. In that case, the workflow falls back to
transcript-export → ElevenLabs / Murf with German voice models. See
`artifact-mitigation.md`.

### Layer 2 — Source Language Homogeneity

Every source in the notebook should be in German. Mixed-language
sources are the second-largest cause of language switching.

If the user has English-language research material:

- **Preferred path:** translate the sources to German *before*
  upload, using a high-quality translator (DeepL Pro or similar
  preserves technical accuracy better than generic LLM translation).
  Upload the German translations as the canonical sources. Keep the
  English originals in a separate notebook for reference.
- **Acceptable fallback:** keep English sources, add a `_translation_
  rules.md` governance file that mandates "translate all citations to
  German on the fly" — but this routinely fails at scale and risks
  semantic drift.
- **Forbidden:** mix German and English sources without explicit
  governance instructions. The model will pick whichever language
  the most semantically relevant chunk happens to be in.

### Layer 3 — Custom Instruction Language

The 10,000-character persona prompt must be written entirely in
German. No English fragments, no bilingual mixing. If the persona
says "be skeptical" in English but demands German output, the model
experiences cognitive friction at every reasoning step and routes to
English when stressed.

This is non-negotiable. A bilingual persona prompt is a guaranteed
language-switch bug.

---

## German-Specific Suspense Mechanics

German offers structural tools for tension that English lacks. Exploit
them.

### Verbendstellung (verb-final position in subordinate clauses)

In German subordinate clauses, the verb migrates to the end. This
means the *action* of a sentence is delayed until the final word — a
natural, language-level form of withholding.

Example:

> *"Was die Daten zeigen, nachdem wir alle drei Quellen gegeneinander
> abgeglichen haben, ist beunruhigend."*

The reveal — *beunruhigend* (disturbing) — sits at the end. English
cannot replicate this without contortion ("What the data show, after
we have compared all three sources against each other, is disturbing"
front-loads "disturbing" semantically because the listener anticipates
the predicate).

Instruct the persona to exploit this:

```
NUTZE DEUTSCHE SYNTAX FÜR SPANNUNGSAUFBAU:
- Verschachtle Hauptsätze mit Nebensätzen, sodass das Verb am Ende
  steht. Der Hörer wartet auf die Auflösung des Satzes.
- Bei Enthüllungen platziere das entscheidende Adjektiv oder Verb
  als letztes Wort des Satzes.
- Verwende komplexe Satzgefüge ("Verschachtelte Sätze") in
  analytischen Passagen, um die geistige Tiefe zu signalisieren.
- Vermeide englischsprachige SVO-Reihenfolge ("Subjekt-Verb-Objekt"),
  wenn die deutsche Satzkonstruktion mehr Spannung zulässt.
```

### Verschachtelte Sätze (nested sentences)

German tolerates and expects sentences with multiple subordinate
clauses. In a pitch context, a well-constructed nested sentence
signals analytical seriousness and forces the listener to follow the
argument across its full arc.

Use sparingly — three or four per audio is enough. Each one functions
as a "tension peak". Surrounding them with shorter declarative
sentences amplifies their effect.

### Sachlichkeit (factual register)

In German professional and academic contexts, an *understated* hyper-
rational delivery often heightens suspense more than melodramatic
inflection. The audience reads restraint as authority.

The persona should mandate:

```
TONALITÄT:
- Sachliche, nüchterne Sprechweise. Keine Begeisterung, kein
  Pathos.
- Untertreibe statt zu übertreiben. Wenn ein Befund schwerwiegend
  ist, sage "das ist bemerkenswert" statt "das ist unglaublich".
- Sprich mit gemessener Autorität, nicht mit Enthusiasmus.
- Lange Pausen vor Schlüsselaussagen. Stille ist erlaubt.
```

### Banned colloquialisms

German conversational filler destroys Sachlichkeit immediately.
Forbid these explicitly in `_dosanddonts.md`:

```
VERBOTENE FLOSKELN:
- "Das ist ja verrückt."
- "Krass."
- "Boah."
- "Ehrlich gesagt..."
- "Wirklich, das ist mal ne Sache."
- "Voll spannend."
- "Auf jeden Fall."
- "Genau, ja, genau."
- "Mega."
- "Brutal."
- "Halt einfach..."

PFLICHTREGISTER STATTDESSEN:
- "Bemerkenswert." statt "Krass."
- "Die Implikationen sind tiefgreifend." statt "Das ist mega."
- "Das wirft eine zentrale Frage auf." statt "Boah, voll spannend."
- "Kontraintuitiv." statt "Verrückt."
```

### Required German register

```
PFLICHT-REGISTER:
- Hochdeutsch, ohne dialektale Färbung.
- Fachvokabular dort, wo die Quellen es verwenden — nicht
  vereinfachen.
- Konjunktiv für Hypothesen ("wäre", "hätte", "könnte").
- Indikativ für gesicherte Behauptungen aus den Quellen.
- Direkte Anrede des Hörers ("Sie") nur am Ende, nie zwischendurch.
```

---

## German Persona Prompt — Structural Differences

A German persona prompt is *not* a translation of an English one. The
character profiles, banned behaviors, and required behaviors all have
German-specific content.

Key differences from the English template:

| English | German equivalent | Notes |
|---------|-------------------|-------|
| "Be professional" | "Sachlich, nüchtern, präzise" | Single-word German concepts often replace English phrases |
| "Cite sources" | "Quellenangabe explizit nennen" | German prefers nouns over verbs in instructions |
| "End abruptly" | "Schluss ohne Verabschiedungsfloskel" | German requires more specific instruction |
| "Adversarial dynamic" | "Konstruktiver Widerstreit" | "Adversarial" has aggressive connotation in German; reframe |
| "Bill Burr energy" | "Trockene Ironie" or "lakonische Schärfe" | Cultural reference does not translate; describe the register |

See `assets/pitch-podcast-10k-template-de.md` for a full German
persona scaffold. Do not regenerate from scratch — fork the template.

---

## Source-Language Translation Workflow

When the user has English research and needs a German pitch:

1. **Identify which sources need translation.** Quantitative data
   (numbers, charts, technical specs) often does not need translation
   if presented as tables. Narrative content always needs translation.
2. **Translate with DeepL Pro** (better technical fidelity than generic
   LLM translation) and have a native German speaker review.
3. **Translate brand names and proper nouns deliberately.** Some stay
   in English (most product names); some have established German
   forms ("Cologne" → "Köln" should always be Köln in German audio,
   never Cologne).
4. **Update the phonetic glossary** to reflect German pronunciation
   for terms that appear in both languages.
5. **Upload German sources to a fresh notebook** — do not mix into an
   existing English-language notebook.

---

## German Localization Validation Checklist

- [ ] NotebookLM output language set to Deutsch in account settings
- [ ] All sources are in German (or explicit translation governance
      is in place)
- [ ] Persona prompt is entirely in German — no English fragments
- [ ] `_dosanddonts.md` lists banned German colloquialisms
- [ ] `_governance.md` mandates Sachlichkeit register
- [ ] At least one Verbendstellung pattern is encoded in the pacing
      instructions
- [ ] Phonetic glossary reflects German pronunciation rules
- [ ] Brand names and proper nouns have explicit translation
      decisions (German form vs. English form retained)
