# Scene Matrix — `<PROJECT-SLUG>`

> **Schema:** 4-Akt × N-Kapitel × M-Szenen Hierarchie (typisch 40 Kapitel = 4×10)
> **Persistenz:** Struktur in NCP `storybeats[]` + `moments[]`; Prosa-Hinweise hier (außerhalb NCP)
> **Written by:** Phase 5 (Scene & Chapter Matrix)

## Akt-Übersicht

| Akt | Kapitel-Range | Thema | Dramatica Sub-Concern |
|-----|---------------|-------|----------------------|
| I   | 1–10          | <PLACEHOLDER Setup, Hook, Inciting Incident> | <Storypoint> |
| II  | 11–20         | <PLACEHOLDER Rising Action, First Pinch>     | <Storypoint> |
| III | 21–30         | <PLACEHOLDER Midpoint, Reversal>             | <Storypoint> |
| IV  | 31–40         | <PLACEHOLDER Climax, Resolution>             | <Storypoint> |

## Kapitel-Detail

### Kapitel 1 — `<PLACEHOLDER Titel>`

- **Akt:** I (Setup)
- **POV / Erzählperspektive:** <PLACEHOLDER>
- **Storyform A (oder Single):**
  - Throughline-Fokus: <OS|MC|IC|SS>
  - Storybeat-Type: <signpost|progression|event>
  - Storypoint: <PLACEHOLDER aus architecture.yaml>
- **Storyform B (nur bei dual):**
  - Throughline-Fokus: <...>
  - Storybeat-Type: <...>
- **Moments (Szenen-Übersicht):**
  1. <PLACEHOLDER Szene 1 Beschreibung>
  2. <PLACEHOLDER Szene 2 Beschreibung>
  3. <PLACEHOLDER Szene 3 Beschreibung>
- **NCP-Referenzen:**
  - `narratives[0].subtext.storybeats[].id: beat_ch01_a`
  - `narratives[0].storytelling.moments[].id: moment_ch01_a_s01`
- **Charaktere im Fokus:** <char_001, char_003>
- **Welt-Anker:** <PLACEHOLDER Setting>
- **Konflikt-Vektor:** <PLACEHOLDER welcher Aspekt des core_conflict treibt dieses Kapitel?>

---

<!-- Wiederhole Block für Kapitel 2-N -->

## Konsistenz-Checks

- [ ] Jedes Kapitel referenziert mindestens einen Storybeat
- [ ] Jedes Moment hat eine `moment.id` in NCP
- [ ] Dramatica Storypoint pro Kapitel zugeordnet
- [ ] Charakter-Auftritte konsistent mit `character-architecture.yaml`
- [ ] Bei dual storyform: beide Narratives in 5D-Interferenz
