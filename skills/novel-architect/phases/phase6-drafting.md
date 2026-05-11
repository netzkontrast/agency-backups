# Phase 6 — Drafting

> **Load when:** Phase 6 ist aktiv, oder per-Kapitel Drafting beginnt

## §0 Goal

Per-Kapitel Prosa-Entwürfe in `drafts/ch-XX.docx` (oder `.md`), mit harten
Pre-Checks gegen Architektur + Characters + Scene Matrix. **Prosa lebt
außerhalb NCP** — cross-reference via `moment.id`.

## §1 Input / Output

**Input:**
- `<slug>.ncp.json` (für Kapitel-X-spezifische Storybeats/Moments)
- `scene-matrix.md` (Kapitel-Detail)
- `character-architecture.yaml` (Charaktere im Kapitel)
- `canon-meta.md` (Prosa-Regeln, Mandate)
- `world-bible.md` (Welt-Lore für Kapitel)
- `open-questions.md` (blockierende OQs?)

**Output:**
- `drafts/ch-XX.docx` (oder `.md`) — die eigentliche Prosa
- Optional: NCP `moments[].prose_status` Update via `ncp-author`

## §2 Pre-Draft Checks (mandatorisch)

```
1. NCP geladen, Kapitel-X-storybeats vorhanden ✓
2. canon-meta.md geladen (Prosa-Regeln) ✓
3. open-questions.md → keine blockierenden OQs für Kapitel X? ✓
4. character-architecture.yaml für beteiligte Charaktere geladen ✓
5. Storypoint des Kapitels klar (aus scene-matrix.md) ✓
6. POV / Erzählperspektive festgelegt ✓
7. Konflikt-Vektor klar ✓
```

Wenn EIN Check failed: **stop**, surface in askuser, optional Phase 5 oder
Phase 7 (OQ-Resolution) first.

## §3 Drafting-Workflow

```
1. Lade chapter-draft-template.md (assets/)
2. Fülle Metadata aus scene-matrix.md + architecture.yaml
3. Erstelle drafts/ch-XX.<format>
4. Drafte Szene für Szene:
   - Konsultiere dramatica-vocabulary für Term-Präzision bei jedem Storybeat
   - Halte POV-Schutz ein (Mosaikstruktur, unzuverlässige Erzähler nicht glätten)
   - Bei Konflikt zwischen Draft und Architektur: surface, fallback zu Story-First-Rule
5. Post-Draft Konsistenz-Check (siehe Template)
6. NCP `moments[].prose_status: drafted` setzen (via ncp-author)
7. progress.md aktualisieren
```

## §4 Hard Rules (CRITICAL)

- **POV-Schutz**: Strukturelle/stilistische Signale erst BESTÄTIGEN, dann ändern — nie stillschweigend glätten
- **Story-First**: Wenn Theorie und Draft sich widersprechen, gewinnt der Draft. Theorie ist Diagnose, kein Rezept
- **Pre-Checks sind NICHT optional** — ein Draft ohne NCP-Anker ist Floating Prose
- **Prosa lebt außerhalb NCP** — NICHT versuchen, Prosa in NCP-Schema zu pressen
- **Konsistenz mit canon-meta.md**: Wenn canon-meta DKT-Physik oder Welt-Regel definiert, einhalten
- **Drafts versionieren**: bei größeren Re-Drafts → `ch-XX_v2.docx` etc.

## §5 Delegations

- **`dramatica-vocabulary`** für Term-Präzision pro Szene (Element-Encoding)
- **`tools/dramatica-nav/nav.py`** für Quick-Lookups
- **`ncp-author`** für `prose_status` Update (optional, nach Draft fertig)
- **`pdf-to-markdown`** wenn alte Material-PDFs als Reference benötigt

## §6 Edge Cases

### §6.1 Storybeat im NCP, aber Draft will Anders

→ Story-First Rule: Draft gewinnt
→ Aber: surface dem User, dass NCP-Update nötig ist
→ Optional: pause Drafting, → Phase 7 (Canon-Update)

### §6.2 Charakter hat Verhalten, das `character-architecture.yaml` nicht abdeckt

→ Drei Optionen:
   1. Charakter-Architektur war zu eng → back to Phase 3 für Update
   2. Verhalten ist outlier/forced → Draft anpassen
   3. Neuer Aspekt entdeckt → Phase 7 (Canon-Update) + character-architecture.yaml update

### §6.3 Blockierende OQ entdeckt während Drafts

→ Stop Drafting für betroffene Szene
→ Surface in `open-questions.md`
→ Pivot zu Phase 7 oder Phase 4 (wenn Research-OQ)

## §7 Exit Gate

Phase 6 für ein Kapitel ist done, wenn:
- `drafts/ch-XX.docx` exists, content-complete
- Post-Draft Konsistenz-Check passed
- NCP `prose_status: drafted` (optional)
- progress.md aktualisiert
- Keine neuen blockierenden OQs

→ Übergang zum nächsten Kapitel oder Phase 7 (Iteration)

## §8 /sc:-Mapping

| Schritt | /sc: Command |
|---|---|
| Drafting | `sc:implement` |
| Konsistenz-Check | `sc:test` |
| Re-Draft | `sc:improve` |
| Term-Lookup | `sc:explain` |
