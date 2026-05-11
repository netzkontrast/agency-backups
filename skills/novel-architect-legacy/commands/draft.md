# /draft — Kapitel-Entwurf

> **Status**: Stub. Voller Prompt-Template ausstehend.

## Zweck

Ein Kapitel wird als Prosa-Entwurf geschrieben. HARTE Pre-Checks — wenn etwas fehlt, wird /draft NICHT gestartet.

## Pre-Checks (HARD)

Alle müssen erfüllt sein:

1. **Phasen 1-6 für die im Kapitel relevanten Storypoints abgeschlossen** (Throughline-Encoding, Dynamics, Storyweaving)
2. **Storyweaving-Eintrag für Ch X existiert** in `outputs/weaving/chapter-map.md`
3. **Per-Kapitel-Beat-Pattern festgelegt** (welche Beats, in welcher Reihenfolge, mit welcher Computational-Class-Markierung)
4. **Polyphonie-Verteilung für Ch X klar** (welche Alters POV haben, wie wechseln sie, welche Stil-Ebene)
5. **Slot 16 (Per-Chapter Dual-POV) entschieden** — ohne diese Entscheidung kann nicht gedraftet werden
6. **Keine blockierende OQ für dieses Kapitel offen**

Wenn ein Pre-Check failt: **STOP**, drafting blockiert. Erst Pre-Check fixen, dann /draft erneut.

## Skill-Stack

1. **novel-architect** — Canon laden, Pre-Checks verifizieren, Constraints für die Szenen vorbereiten
2. **dramatica-vocabulary** — Term-Präzision während Prosa-Entscheidungen (Driver, Limit, Element-Pairs in Szenen-Spannung)
3. **docx** — Export als .docx ins `outputs/drafts/`

## Prosa-Regeln (siehe canon-state.md → Prosa-Regeln Sektion)

Vor Draft-Start prüfen und einhalten:

- **Lesersteuerung** = oberstes Prinzip (jede Entscheidung gegen das Prinzip prüfen)
- **Max 1 Konzept/Szene**, durch Erfahrung gezeigt
- **Polyphonie** entsprechend Akt: I = fragmentiert/staccato, II = Übergang, III = chorisch
- **Stil-Ebene**: 1 (KW1) = kalt/steril, 2 (KW2-3) = heiß/fragmentiert, 3 (KW4/Juna) = poetisch
- **Syntax** alterspezifisch: Lex = hypotaktisch, Nyx = staccato, Kiko = kindlich
- **Ted-Chiang-Maßstab**
- **Somatischer Filter**: Landauer → Hitze/Ozon, niemals Gleichung
- **Erste 50 Seiten KEINE DKT-Terminologie**
- **Dissoziation** = Amnesie-Terror, NIEMALS Crew-Menü
- **Fraktale Zeit-Struktur** — Erinnerung schichtet sich, nicht linear

## Output

- **Format**: .docx in `outputs/drafts/ch-XX.docx`
- **Inhalt**: Voller Kapitel-Prosa-Entwurf
- **Begleit-Notiz**: Optional `outputs/drafts/ch-XX-notes.md` mit Storyform-Bezug, getroffenen Entscheidungen, offenen Punkten zur Revision

## Checkpoint

Chapter-Draft ist eine Phase-Unit-Complete → Checkpoint nach jedem fertigen Draft.

## Anti-Pattern

- /draft starten ohne Pre-Checks
- Stillschweigend Mosaik-Brüche „glätten" (POV-Schutz)
- DKT-Terminologie in den ersten 50 Seiten
- Crew-Menü-artige Alter-Switches
- Zwei Konzepte in eine Szene packen

## TODO

- Vollen Skeleton-Prompt formulieren mit allen Pre-Check-Calls
- Per-Akt-Stil-Beispiele aus dem Canon zusammenstellen
- Revisions-Workflow für /draft-Outputs definieren (eigener Workflow `chapter-revision`?)
