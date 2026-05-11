# NCP-Integration Contract (v1.0)

> **Load when:** NCP-Edit-Frage, oder Phase-2/3/5 startet
> **Authority:** Bindend für alle Phasen, die NCP berühren

## §0 Prinzipien

1. **NCP-Mutation NUR via `ncp-author`** — Direkte Hand-Edits an `.ncp.json` sind verboten
2. **NCP ist die einzige strukturelle State-Quelle** — nicht canon-meta.md, nicht progress.md, nicht Memory
3. **AGENTS.md NO.2:** Dramatica-Slots vorher über Ontology auflösen (`nav.py by-id`)
4. **Validation nach jeder Mutation** — `node skills/ncp-author/scripts/validate.js <file>`

## §1 NCP-Slot-zu-Phase Mapping

| Phase | NCP-Slots befüllt | Source-File |
|-------|-------------------|-------------|
| 0 — Bootstrap | (Skeleton initial leer oder via Migration) | template-empty.json oder migration |
| 1 — Intent | KEINE | (intent.yaml separat) |
| 2 — Architecture | `narratives[].subtext.perspectives[]`, `narratives[].subtext.dynamics[]` | architecture.yaml |
| 3 — Characters | `narratives[].subtext.players[]`, `players[].motivations[]`, `players[].perspectives[]` | character-architecture.yaml |
| 4 — Research | optional: Updates an `signposts[]` content | findings + canon-meta |
| 5 — Scene Matrix | `narratives[].subtext.storypoints[]`, `narratives[].subtext.storybeats[]`, `narratives[].storytelling.moments[]` | scene-matrix.md |
| 6 — Drafting | optional: `moments[].prose_status` | drafts/ |
| 7 — Iteration | beliebige Updates basierend auf Resolution | open-questions resolution |

## §2 Mutation-Workflow

```
1. novel-architect ruft ncp-author auf mit:
   - Operation (create_skeleton, add_player, add_storybeat, etc.)
   - Input-Daten (aus architecture.yaml / character-architecture.yaml / scene-matrix.md)
   - Target NCP file (canon/<slug>.ncp.json)

2. ncp-author:
   - lädt aktuelles NCP
   - validiert Schema-Compliance der neuen Daten
   - resolved Dramatica-Ontology-IDs zu NCP-enum-Strings (via nav.py)
   - mutiert das JSON
   - schreibt zurück
   - validiert via scripts/validate.js

3. novel-architect:
   - liest Validation-Result
   - bei Fail: surface Error, askuser
   - bei Pass: weiter zu nächstem Schritt
```

## §3 Ontology-Resolution (AGENTS.md NO.2)

Bevor ein Dramatica-Slot in NCP geschrieben wird:

```bash
# Beispiel: User sagt "MC Class = Universe"
python3 tools/dramatica-nav/nav.py by-id throughline.main-character
# → liefert canonical_label, ncp_appreciation_string

python3 tools/dramatica-nav/nav.py by-id class.universe
# → liefert canonical_label
```

Erst dann wird in NCP geschrieben (mit korrektem canonical NCP-enum-String).

## §4 Validation-Regeln

Nach jeder Mutation:

1. **Schema-Validation:** `node skills/ncp-author/scripts/validate.js canon/<slug>.ncp.json`
2. **Required Fields:** Per `references/schema-cheatsheet.md` (in ncp-author)
3. **Enum-Compliance:** Per `references/canonical-vocabulary.md` (in ncp-author)
4. **Cross-Skill-Consistency:**
   - `players[].id` referenziert in `storybeats[].player_focus` muss existieren
   - `storybeats[].storypoint_id` referenziert in `storypoints[].id` muss existieren

Bei Fail: surface Error im Status-View, askuser für Fix.

## §5 Storyform-Count-Pattern

Bei `architecture.storyform_count: single`:
- `narratives[]` array hat genau 1 Eintrag

Bei `architecture.storyform_count: dual`:
- `narratives[]` array hat genau 2 Einträge (storyform_a, storyform_b)
- Pro `player`: kann unterschiedliche `perspectives` in A vs. B haben (selbe `id`)
- Storybeats: ein parallel-Paar pro Kapitel (eins in A, eins in B)

## §6 Append-Only-Disziplin

- **Players NEVER deleted** — wenn Charakter raus, markieren als `inactive: true`
- **Storybeats NEVER renumbered** — wenn umstrukturiert, neuer Storybeat + alter als `superseded_by`
- **Moments NEVER renumbered** — gleiche Regel
- **Storyform-Slots editierbar** — bei größeren Änderungen: revision-Tracking

## §7 Migration vom Legacy

Wenn `scripts/bootstrap_project.sh kohaerenz-protokoll` läuft:
1. Legacy NCP-Datei wird zu `canon/<slug>.ncp.json` kopiert
2. Validation läuft sofort
3. Bei Schema-Drift (Legacy v1.2.x vs. neue v1.3.0): warning + askuser

## §8 Hard Rules

- **Nie direkt JSON editieren** — immer über `ncp-author`
- **Nie Schema-Felder selbst coinen** — Enum-Werte sind upstream-fixed
- **Nie validation skippen** — bei Schema-Fail: stop, fix, retry
- **Nie players[] in mehreren narratives duplizieren** — gleiche `id`, andere `perspectives`

## §9 Anti-Patterns

- „Quick fix" durch direktes JSON-Editing → Schema-Drift, validator scheitert silent
- Ontology-Lookups skippen → falsche NCP-Strings, validator scheitert
- Migration ohne Validation → Legacy-Drift unbemerkt
