# Quality Gate — 13-Punkt-Audit

Referenz für den **Quality Auditor**. Binäre Prüfung. Keine Ermessensspielräume.

---

## Prüfregel

Jeder Punkt wird mit **PASS** oder **FAIL** bewertet. Ergebnis:

- **13× PASS** → Gesamturteil `PASS`, Output geht zum Orchestrator.
- **≥ 1× FAIL** → Gesamturteil `REJECT`, benannte Rolle wird zurückgerufen.

Bei mehrdeutigem Fall: FAIL. Der Audit ist adversariell, nicht wohlwollend.

---

## Die 13 Punkte

### Gruppe A — Narrative Integrität (Architect-Output)

1. **Phase-Klarheit.** Genau eine dominante Phase. Nicht zwei, nicht keine.
2. **Cluster-Klarheit.** Genau ein dominanter Cluster. Schatten-Cluster optional, aber benannt.
3. **Metaphern-Budget.** Genau zwei Leit-Metaphern aus der erlaubten Liste (`narrative_bible.md`).

### Gruppe B — Sprachliche DNA (Lyricist-Output)

4. **Register-Reinheit.** Innerhalb einer Section nur ein Register (Agency ODER Kern). Wechsel nur an Section-Grenzen.
5. **POV-Konsistenz mit Blueprint.** Die in `VOICES (IFS)` benannten Stimmen sprechen — keine, die nicht benannt sind. **Ausnahme:** wenn der Draft einen POV-Shift enthält, der *nicht* im Blueprint steht → **FLAG for USER**, nicht automatisch FAIL (Kern-Invariante 5).
6. **Keine Emotions-Adjektive.** Null Vorkommen von traurig/einsam/verzweifelt/wütend/glücklich/stolz/leer (Liste in `sprachliche_abbildung.md`).
7. **Keine Lexikon-Ausschlüsse.** Null Vorkommen der Verbotsliste (Pop-Liebes-Vokabular, generische Schatten-Tropen, freie Religion, Diminutive).
8. **Prosodie-Symmetrie.** Parallele Verses haben Silbenzahl ±1. `scripts/validate_prosody.py` liefert Zahlen.
9. **Reimschema konstant pro Section.** AABB oder ABAB innerhalb einer Section nicht gemischt.

### Gruppe C — Sonische DNA (Engineer-Output)

10. **Style Prompt ≤ 110 Zeichen.** Harte Grenze.
11. **Control by Reduction.** Genau 1 Primärgenre + 1 Supporting-Texture + 1 Signature im Style Prompt. Zählbar.
12. **120-BPM-Deklaration.** Das Grid ist entweder im Style Prompt oder im `[Intro]`-Tag explizit benannt. Bei Abweichung: alternatives BPM explizit.
13. **Projekt-Tag-Budget.** Maximal 3 Agency-spezifische Tags aus `suno_prompt_engineering.md`. Standard-Suno-Tags unbegrenzt.

---

## Report-Format des Auditors

```
AUDIT REPORT — Track: <name>
Phase×Cluster: <X × Y>

Group A (Narrative)   — 1:[✓/✗]  2:[✓/✗]  3:[✓/✗]
Group B (Sprache)     — 4:[✓/✗]  5:[✓/✗/FLAG]  6:[✓/✗]  7:[✓/✗]  8:[✓/✗]  9:[✓/✗]
Group C (Sonik)       — 10:[✓/✗] 11:[✓/✗] 12:[✓/✗] 13:[✓/✗]

VERDICT: PASS | REJECT
Return to: <Architect | Lyricist | Engineer | USER for FLAG>
Violations: <präzise Benennung mit Section-Referenz>
```

---

## Beispiele

### Beispiel 1 — REJECT auf Punkt 6

```
Violation: Punkt 6 — "Emotions-Adjektiv" in [Chorus] Zeile 2:
  "Ich bin so einsam im Firewall-Schatten."
→ Return to Lyricist.
→ Hinweis: Ersetze "einsam" durch objective correlative
  (z.B. Zustand des Firewalls selbst).
```

### Beispiel 2 — FLAG auf Punkt 5

```
Status: Punkt 5 — FLAG (nicht FAIL).
Blueprint benennt VOICES = "Core (Manager)".
[Bridge] Zeile 3 enthält 1. Sg. in Exile-Duktus
  ("Leiser. Ich halte nur noch den Namen.").
→ Question to USER: War der POV-Shift in die
  Exile-Stimme beabsichtigt? Wenn ja, Blueprint nachträglich
  erweitern. Wenn nein, Lyricist korrigieren.
```

### Beispiel 3 — REJECT auf Punkt 11

```
Violation: Punkt 11 — Style Prompt enthält 4 Genres:
  "industrial darkwave, minimal techno, dark ambient,
   post-rock, clinical mood, sub-bass, FM arps, baritone"
→ Return to Engineer.
→ Hinweis: Reduziere auf 1 Primär + 1 Support + 1 Signature.
```

---

## Eskalation

Bei **3 aufeinanderfolgenden REJECTs** am selben Track:

1. Auditor gibt `ESCALATE` zurück.
2. Orchestrator pausiert die DAG.
3. Strukturierter Problem-Report an den User:
   - Track-Name, Phase×Cluster
   - Welche Punkte in jedem Durchlauf versagt haben
   - Hypothese: liegt die Blockade im Blueprint, der sprachlichen Umsetzung oder der sonischen Übersetzung?
   - Vorschlag: Blueprint überdenken oder Invariante temporär lockern (User-Entscheidung).
