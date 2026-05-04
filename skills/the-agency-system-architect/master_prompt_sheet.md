# Master Prompt Sheet — Track Template

Das finale Dokument, das der Orchestrator an den User zurückgibt.
Eine Datei pro Track. Suno-ready copy-paste.

---

## Track-Header

```
Track-Titel: [TITEL]
Album: [1 | 2 | 3] — [Together We Confide | Moment der Klarheit | Gegenüber]
Track-Nummer im Album: [N]
Datum: [YYYY-MM-DD]
```

---

## Blueprint (vom Concept Architect)

```
PHASE: [Onboarding | Optimization | System Failure | Re-Initialization]
CLUSTER: [Lingering Echoes | Polyphony of Self | Systematic Agency | Fragile Connections | Meaning in the Mosaic]
VOICES (IFS): [z.B. "Manager + Exile"]
CORE_METAPHORS: [Metapher 1, Metapher 2]
EMOTIONAL_GRADIENT: [Start → Ende]
```

---

## Lyrics (vom Lyricist, nach suno-lyric-writer-Phase 2-4)

```
[Intro]
...

[Verse 1]
...

[Pre-Chorus]
...

[Chorus]
...

[Verse 2]
...

[Bridge]
...

[Chorus]
...

[Outro]
...
```

**Prosodie-Notiz:**
- Verse 1 Silben: [liste]
- Verse 2 Silben: [liste]
- Δ max: [zahl]
- Reimschema pro Section: [liste]

---

## Suno Style Prompt

```
[≤ 110 Zeichen]
```

---

## Suno Tagged Lyrics (Engineer-Output)

```
[vollständige Lyrics mit allen Meta-Tags inline,
 direkt copy-paste-fertig in Suno Custom Mode]
```

---

## Auditor-Verdict

```
VERDICT: PASS
Groups: A=[✓✓✓]  B=[✓✓✓✓✓✓]  C=[✓✓✓✓]
Flags (falls vorhanden): [...]
Retry-Count: [0 | 1 | 2]
```

---

## Album-State nach diesem Track

```
State-Datei: state/ALBUM_STATE.json
Neuer Status: [draft | prompted | validated | completed]
Letzte Aktualisierung: [ISO-Timestamp]
```

---

## Notizen für die Produktion (optional)

- [Persona-ID für Suno, falls verwendet — via suno-lyric-writer]
- [Creative Slider-Werte, falls relevant]
- [Extend/Cover-Anweisungen, falls Track auf bestehendem Material baut]
- [Sonstiges, was in Phase 4 von suno-lyric-writer angefallen ist]
