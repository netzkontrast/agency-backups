# Open Questions — Kohärenz Protokoll

> Stand: 2026-05-03 (nach Reset 2026-04-30, Outline-Revision 2026-05-01)

---

## Blockierende OQs

Aktuell **keine** OQs blockieren die nächste Phase (Encoding).

Die alten OQ-01/02/03 aus der WIP-Skill-Version sind durch den Reset 2026-04-30 erledigt:
- ~~OQ-01: Junas Natur (Alter vs. eigenständige Entität)~~ → entschieden: Witness-Function + Gödel-Property, NICHT Alter
- ~~OQ-02: Alter-Zahl 11 vs. 13~~ → entschieden: 13 fix
- ~~OQ-03: Kaels Ursprungs-Trauma (Grad der Explizitheit)~~ → entschieden: Genesis 3-Beat strukturell, somatischer Filter, keine explizite Trauma-Ausarbeitung

Aus Session 2 (2026-05-03):
- ~~OQ-04: A1-vs-V3 (AEGIS-Position in Storyform B)~~ → entschieden 2026-05-03 via /interview: **A1 bleibt Canon (AEGIS = MC in B)**. Begründung in canon-meta.md Sektion „Verworfene Storyform-Alternativen mit Begründung". V3 falsifiziert durch Bewusstseins-Kategorie-Fehler + Verletzung der ANP-Symmetrie.
- ~~OQ-05: AEGIS-Ontologie (Bewusstseins-Status für MC-Position)~~ → entschieden 2026-05-03 via User-Setzung: **AEGIS = System-Ebene-ANP**. Strukturelle Zwillingschaft zu Kael (Individual-Ebene-ANP). Holon-Spiegelachse mit AEGIS↔Oblivion und Juna↔Silas. Kanonisiert in canon-meta.md.
- ~~OQ-06: Dual-Storyform vs. Quasi-/Single-Storyform~~ → entschieden 2026-05-03 via /interview: **Dual-Storyform behalten**. Begründung: ANP-Symmetrie verlangt parallele Storyform-Behandlung, andernfalls bricht die Symmetrie zwischen Kael und AEGIS auf den zwei Holon-Ebenen.

---

## Architektur-Frage (höchste Priorität für nächste Session)

### Slot 16: Per-Chapter Dual-POV

Originalformulierung (vom User in Storyforming-Session festgelegt):
> Jedes Kapitel muss BEIDE Storyforms simultan enthalten als Dual-POV WITHIN the chapter — nicht odd/even Wechsel zwischen Kapiteln. Zwei narrative Instanzen simultan im selben Kapitel, ohne in Crosscut zu kollabieren.

**Was zu lösen ist**:
- Wie operationalisieren wir „simultan im selben Kapitel"?
- Was unterscheidet das vom Crosscut?
- Welche typografische / strukturelle Markierung trennt die Instanzen ohne sie zu trennen?
- Bleibt die Akt-Struktur + Pacing valide? (User-Setzung: ja.)

**Status**: ungelöst, blockiert in Praxis Phase 6 (Storyweaving).

---

## Appendix C — Open Questions

Aus dem Reset-Doc, nicht-blockierend für Encoding, aber mittelfristig zu klären:

### OQ-A: Post-Vortex-AEGIS-Status

Nach dem Vortex (Ch35-36, Driver-Pivot Action → Decision, Algorithm.Melancholy als Schicksal): **Was ist AEGIS in Akt III noch?**
- Aufgelöst? Transformiert? Erinnerung?
- Existiert AEGIS für Kael überhaupt noch oder nur als historische Tatsache?
- Wenn transformiert: in was?

### OQ-B: Moonshine-Boundary

Der Moonshine-Link ist Storyform A's RS-Throughline (Physics, physische Anstrengung, materielle Begegnung Kael ↔ Juna).
- **Wo genau ist die Grenze**, ab der der Moonshine-Link wirkt vs. nicht wirkt?
- Was sind Bedingungen für Resonanz vs. Stille?
- Ist Phone-Silence eine notwendige Bedingung, hinreichende, oder nur die häufigste?

### OQ-C: Juna-Erscheinungs-Modus-Anker

Juna wird nie physisch beschrieben, nur durch Wirkung. **Welche konkreten Anker** lassen ihre Präsenz erkennbar werden?
- Anomale Erasure-Balance (canonisch)
- Phantom-Resonanz im Host/System-Feld (canonisch)
- Phone-Silence als Anker (canonisch)
- **Was sonst?** Mindestens 2-3 weitere Modi nötig für narrative Variation über 39 Kapitel.

### OQ-D: Genesis 4. Beat?

Genesis ist aktuell 3-Beat: Unity → Separation Protocol → Kael = Component 734.
- **Gibt es einen 4. Beat**, der erst rückblickend lesbar wird (z. B. nach Vortex)?
- Oder schließt die 3-Beat-Struktur strukturell ab?
- Status: offen, kein Entscheid getroffen.

---

## Nicht-blockierende Skill-OQs

(Diese sind Skill-intern, nicht Canon)

- Wann wird `commands/` von Stubs zu vollen Templates ausgebaut?
- Wann wird `ncp-author` reif genug, um als Storyform-JSON-Persistenz integriert zu werden?
- Brauchen wir einen `canon-diff`-Skill, der NCP + canon-meta gegen einen externen Snapshot (Drive-Reset-Doc, Memory-Export) diffed — als optionales Audit-Tool, nicht als Synchronisierungs-Pflicht?

---

## Resolution-Workflow

OQs werden via Workflow `open-questions-resolution` (siehe `workflows.md`) abgearbeitet:
- novel-architect lädt OQ-Kontext
- dramatica-theory liefert Implikationen
- Entscheid wird festgelegt
- NCP-Datei (falls strukturell) und/oder canon-meta.md (falls nicht-strukturell) werden geupdated
- Eintrag wird hier oben als „erledigt" markiert (mit Datum + Entscheid)
- memory-sync nur dann, wenn User explizit Memory-Broadcast wünscht
- Checkpoint: package + present
