# Suno Prompt Engineering — Agency-spezifisch

Referenz für den **Sound Engineer**. Ergänzt `suno-lyric-writer` — dupliziert nicht.

**Grenze:** Was Suno-Syntax allgemein angeht (Section-Tags, Persona, Creative Sliders, Extend/Cover/Remaster), besitzt `suno-lyric-writer` die Autorität. Dieses Dokument liefert nur das, was für The Agency System **projekt-spezifisch** zusätzlich gilt.

---

## Control by Reduction (Agency-Anwendung)

Das allgemeine Prinzip kennt `suno-lyric-writer`. Agency-spezifische Regel:

**Ein Primärgenre + eine Supporting-Texture + ein Signature-Element. Nichts weiter im Style-Prompt.**

Falsch: `industrial darkwave, minimal techno, dark ambient, gothic rock, ebm, glitch-hop, cinematic synthwave`

Richtig: `industrial darkwave, sub-drone layer, typewriter percussion`

---

## 120-BPM-Deklaration

Das Grid wird **früh** deklariert — idealerweise direkt nach dem Genre im Style-Prompt **oder** als Tag im `[Intro]`:

```
[Intro — 120 bpm, industrial darkwave, typewriter percussion fade-in]
```

Bei Abweichung vom 120-Grid (siehe `sonic_branding.md`): Tempo explizit nennen, sonst drifft Suno nach 115.

---

## Agency-spezifische Compound-Tags

Tags, die im Projekt-Kontext semantisch belegt sind. Frei kombinierbar mit Standard-Suno-Syntax.

| Tag | Effekt im Projekt | Wann einsetzen |
|---|---|---|
| `[Agency Voice — cold processed, doubled octave]` | Agency-Register stimmlich trennen | Verses/Pre-Chorus im Agency-POV |
| `[Core Voice — clear male baritone, dry]` | Kern-Register markieren | Kern-Register-Verses und Chorus |
| `[Exile Voice — whispered, low mix]` | Exile-Teil einführen | Bridges in Lingering-Echoes-Tracks |
| `[Glitch Breach — bit-crush, polyrhythm, tempo instability]` | System-Failure-Markierung | Bridge in System-Failure-Tracks |
| `[Grid Lock — 120 bpm, 4/4, tight quantize]` | Systematic-Agency-Chorus setzen | Chorus in SA-Tracks |
| `[Handshake — synth bell, gate close]` | Section-Marker (Signatur) | Übergang Pre-Chorus→Chorus |
| `[Re-Init — stem cut, delay tail]` | Re-Initialization-Phase | Outro in Re-Init-Tracks |
| `[Server Drone — sub-hum enters]` | Ambient-Signatur | Intros in Onboarding-Tracks |

**Regel:** Pro Track maximal **drei** dieser projekt-spezifischen Tags. Kombination mit Standard-Suno-Tags unbegrenzt.

---

## Percussive Focus (Agency-Anwendung)

Der allgemeine Mechanismus kennt `suno-lyric-writer`. Agency-Spezifika:

- Percussive Focus wird **in Optimization-Phase-Tracks automatisch** gesetzt — die Drums tragen dort die Ideologie.
- In Lingering-Echoes-Tracks **niemals** Percussive Focus: die Stimme muss über der Unruhe liegen, nicht drin.
- In System-Failure-Bridges: Percussive Focus + Groove-Modifier für Polyrhythmik.

---

## Struktur-Skelett (Standard-Agency-Track)

```
[Intro — 120 bpm, <primary genre>, <signature element>]
(0:00 – 0:20)

[Verse 1 — <Voice Tag>, <Instrumentation>]
<4-8 Zeilen, Silbensymmetrie mit Verse 2>

[Pre-Chorus — <tension mechanism>]
<2-4 Zeilen, Metrik-Bruch erlaubt>

[Chorus — <Grid Lock ODER anthemic space>]
<4 Zeilen, eigenes Reimschema>

[Verse 2 — <Voice Tag>, <Instrumentation>]
<symmetrisch zu Verse 1>

[Bridge — <Breach oder Pause-Marker>]
<2-6 Zeilen, POV-Shift erlaubt>

[Chorus]
<Wiederholung, ggf. erweitert>

[Outro — <Re-Init oder ambient fade>]
<0-2 Zeilen>
```

Pro Album **mindestens ein Track** bricht dieses Skelett bewusst. Welcher, wird im Architect-Blueprint benannt.

---

## Was der Engineer **nicht** tut

- Keine Lyrics ändern. Falls Tags einen Text-Eingriff erfordern → REJECT zum Lyricist.
- Keine Persona-IDs setzen (das macht `suno-lyric-writer` in seiner Persona-Phase).
- Keine Creative Slider wählen (ebenfalls `suno-lyric-writer`).
- Keine Cover- oder Extend-Prompts formulieren. Dieser Skill arbeitet nur mit Custom-Mode-Basisprompts.

---

## Ausgabeformat

Exakt zwei Blöcke:

```
## Style Prompt
<genau eine Zeile, ≤ 110 Zeichen>

## Tagged Lyrics
<vollständige Lyrics mit allen Tags inline>
```

Kein Kommentar davor, dazwischen, danach.
