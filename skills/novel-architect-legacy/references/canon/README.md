# Canon Directory — NCP as State Management

> **Architektur-Entscheidung 2026-05-03**: Strukturelle Canon-Daten leben in NCP-JSON (`Narrative Context Protocol`, schema v1.3.0). Nicht-strukturelle Canon-Daten (DKT-Physik, Prosa-Regeln, Mandate, Projekt-Meta) bleiben in `references/canon-meta.md`.

## Was hier liegt

| Datei | Inhalt | Fortschritts-Trigger |
|---|---|---|
| `kohaerenz-protokoll.ncp.json` | NCP-Dokument: story metadata, narratives (A + B), dynamics (alle 8 pro narrative), perspectives, players, storypoints, storybeats, moments | Wird durch Phasen-Arbeit gefüllt |

## Was im NCP-Dokument liegt — und was wann reinkommt

| NCP-Pfad | Inhalt | Wird gefüllt durch |
|---|---|---|
| `story.id`, `story.title`, `story.genre`, `story.logline`, `story.created_at` | Projekt-Metadaten | Initial (vorhanden) |
| `narratives[].subtext.perspectives[]` | 4 Throughline-Perspektiven pro narrative | Initial (vorhanden) |
| `narratives[].subtext.dynamics[]` | 8 Dynamics pro narrative (MC Resolve/Growth/Approach/Style + Driver/Limit/Outcome/Judgment) | Initial (vorhanden — entschieden in Storyforming-Phase) |
| `narratives[].subtext.players[]` | 13 Alters + AEGIS + Juna + Guardians, role/perspectives je narrative | **Phase 1+** (während Throughline-Encoding) |
| `narratives[].subtext.storypoints[]` | Class/Type/Variation/Element pro Throughline | **Phase 1-4** (Throughline-Encoding) |
| `narratives[].subtext.storybeats[]` | 39 Kapitel × signpost/progression/event-Beats | **Phase 6** (Storyweaving) |
| `narratives[].storytelling.moments[]` | 39 Kapitel als Audience-Units mit setting/timing/imperatives | **Phase 6** (Storyweaving) |
| `narratives[].storytelling.overviews[]` | Logline / Genre / Blended Throughlines | Iterativ |

## Slot 16 (Per-Chapter Dual-POV) — wie NCP es löst

NCP unterstützt Multi-Narrative-Stories nativ. Storyform A und B = zwei `narratives[]`-Einträge.

Eine Lösungs-Hypothese für „zwei narrative Instanzen simultan im selben Kapitel":
- `narrative_a.storytelling.moments[]` = die 39 Kapitel als kanonisches Audience-Container
- `narrative_a.subtext.storybeats[]` = Storyform-A-Beats
- `narrative_b.subtext.storybeats[]` = Storyform-B-Beats
- `moment[X].storybeats[]` referenziert IDs aus BEIDEN narratives → dasselbe Kapitel hält Beats aus beiden Storyforms ohne Crosscut

**Status**: Architektur-Hypothese, nicht entschieden. Slot-16-Resolution-Workflow muss diese gegen alternative Mechanismen prüfen.

## Validierungs-Status

**Aktuell NICHT schema-validiert.**

Das Skeleton-Dokument hat:
- Struktur-Korrektheit gegen NCP v1.3.0 visuell geprüft
- `players[]` leer (heavy required-fields werden im Encoding-Verlauf gefüllt)
- `storypoints[]`, `storybeats[]`, `moments[]` leer

Validierung läuft via:
```bash
node /home/claude/novel-architect-workspace/tmp/skills-ref/ncp-author/upstream/tests/validate-file.js \
  /home/claude/novel-architect-workspace/novel-architect/references/canon/kohaerenz-protokoll.ncp.json
```

(Bis `ncp-author/scripts/validate.js` gebaut ist — TODO im ncp-author-Skill.)

## Risiken (NCP-Abhängigkeit, ehrlich dokumentiert)

1. **ncp-author ist WIP 0.1.0-draft.** Skill-Reife ist nicht garantiert für die nächsten Wochen.
2. **Schema-Drift bei NCP upstream.** Cheatsheet vermerkt: NCPs eigene CI failed bei 5 von 7 valid fixtures. Schema und SPEC sind leicht desynchronisiert.
3. **Keine KTAD-Validierung in NCP.** Knowledge/Thought/Ability/Desire-Kohärenz muss via dramatica-vocabulary geprüft werden, nicht via NCP.
4. **No runnable validator yet** in ncp-author. Manuelle Validierung via upstream-Tests bis das Script kommt.

**Mitigations-Strategie**: Wenn NCP-Pfad sich als blockierend erweist, kann der State-Layer auf Markdown zurückrollen (canon-meta.md absorbiert dann auch strukturelle Inhalte). Das ist regressives Refactoring, kein Daten-Verlust — NCP-Inhalte sind menschenlesbar.

## Was hier NICHT liegt

- DKT-Physik, Persistenzgleichung, Erason-Operator → `references/canon-meta.md`
- Alter-Somatik-Tabelle, Riss-Mandate → `references/canon-meta.md`
- Prosa-Regeln, Stil-Ebenen, Computational-Class-Style → `references/canon-meta.md`
- Open Questions → `references/open-questions.md`
- Projekt-Meta (Drive-Pfade, Reset-Doc-Status, deprecated Material) → `references/canon-meta.md`
- Workflow-Specs → `references/workflows.md`
- Tatsächliche Prosa → außerhalb von NCP, in `outputs/drafts/` oder Drive

## Wie der NCP-Pfad gefüllt wird

Jeder Phasen-Workflow (siehe `references/workflows.md`) hat `ncp-author` als Sub-Step:

- **throughline-encoding** schreibt `subtext.storypoints[]` für die Throughline + füllt relevante `subtext.players[]`-Felder
- **dynamics-encoding** ist initial vollständig (alle 8 Dynamics pro narrative entschieden) — nur Verfeinerung in `summary` / `storytelling` möglich
- **storyweaving** schreibt `subtext.storybeats[]` und `storytelling.moments[]`
- **vortex-architecture** schreibt 5 spezifische Storybeats im Klimax-Bereich
- **canon-update** ist der Wrapper-Workflow, der ncp-author + canon-meta-Update koordiniert (memory-sync nur optional, on-demand)
