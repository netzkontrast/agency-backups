# Phase 5 — Scene & Chapter Matrix (3-Gate Approval)

> **Load when:** Phase 5 ist aktiv, oder Akt-Struktur-Frage, oder Storybeat-Conflict

## §0 Goal

Erstelle 40-Kapitel-Matrix (oder gewählte Akt-Struktur aus `intent.yaml`),
persistiere Storybeats und Moments in NCP via `ncp-author`, schreibe
`scene-matrix.md` als menschen-lesbares Begleit-Dokument.

## §1 Input / Output

**Input:**
- `architecture.yaml` (storyform + dynamics)
- `character-architecture.yaml` (players)
- `world-bible.md` (welt-context)
- `intent.yaml` (`chapter_count_target`, `methods_preference.structure`)

**Output:**
- `scene-matrix.md` (Schablone in `assets/scene-matrix-template.md`)
- NCP Updates: `storypoints[]`, `storybeats[]`, `moments[]` (via `ncp-author`)
- `scene-matrix-status-view.md`

## §2 Sub-Phases mit 3 Gates

```
Phase 5.1   Load architecture + character + world             (silent)
Phase 5.2   Select structure template                          (askuser if [→ novel-architect-structure] offers multiple options)
Phase 5.3   Fill act-level structure (4 acts, storypoints)    (auto + askuser per act)
            ──── GATE 1 (act outline) ────                     (1 askuser: Approve / Edit acts)
Phase 5.4   Per act: fill chapter-level (storybeats per chapter) (loop)
            ──── GATE 2 (chapter outline) ────                 (1 askuser: Approve / Edit)
Phase 5.5   Per chapter: fill scene-level (moments per scene) (loop)
Phase 5.6   Write NCP storybeats[] + moments[]                 (delegate ncp-author)
Phase 5.7   Render scene-matrix.md                             (file-first)
            ──── GATE 3 (final scene matrix) ────              (1 askuser: Approve / Edit)
Phase 5.8   Persist + present_files
```

## §3 Structure-Templates (load on demand)

Aus `[→ novel-architect-structure]` (load on demand via `intent.methods_preference.structure`):
- **`40-chapter-matrix.md`** (Default) — 4 Akte × 10 Kapitel, ~2-4 Szenen pro Kapitel
- **`heroes-journey.md`** — 12 Stufen (Departure × 4, Initiation × 6, Return × 2)
- **`save-the-cat.md`** — 15 Beats mit fixen Positionen
- **`dramatica-quad.md`** — fraktale Rekursion: Akt = Kapitel = Szene = Quad

Wenn `intent.methods_preference.structure` mehrere wählt, kombiniere (z.B.
40-Kapitel-Matrix + Dramatica-Quad → 40 Kapitel mit Quad-Strukturierung).

## §4 Gate-Details

### §4.1 Gate 1 — Act Outline

Approval-View zeigt:
- 4 Akte mit Themen, Kapitel-Range, Dramatica Sub-Concern per Akt
- Storypoints (Goal, Requirements, Consequences, Forewarnings, Cost, Dividend) je Akt

**Approval-Optionen:** Approve / Edit Akt I-IV / Restart

### §4.2 Gate 2 — Chapter Outline

Approval-View pro Akt:
- 10 (oder N) Kapitel mit Title, Throughline-Fokus, Storybeat-Type (signpost/progression/event), Storypoint
- Bei dual storyform: zwei Throughline-Spalten

**Approval-Optionen:** Approve Akt / Edit Akt / Loop back to Gate 1

### §4.3 Gate 3 — Final Scene Matrix

Komplette `scene-matrix.md` + Statistiken:
- N Kapitel mit N Szenen
- M Storybeats in NCP
- K Moments in NCP

**Approval-Optionen:** Approve / Edit specific chapter / Loop back to Gate 2

## §5 Storyweaving-Pattern (Dramatica)

Pro Kapitel:
1. Welche Throughline ist Fokus? (OS/MC/IC/SS)
2. Welcher Storybeat-Type? (signpost = thematischer Anker, progression = Story-Movement, event = Wendepunkt)
3. Welcher Storypoint? (aus architecture.yaml)
4. Welche Moments? (Szenen, 2-4 pro Kapitel)

**Bei dual storyform:** Pro Kapitel zwei Storybeats (einer pro narrative), parallel orchestriert.

## §6 NCP-Workflow für Phase 5 (delegated to ncp-author)

Per Akt → Kapitel → Szene:

1. **Storybeat erstellen:**
   - `narratives[X].subtext.storybeats[]`
   - `id`, `chapter`, `throughline_focus`, `storybeat_type`, `appreciation` (NCP enum)
2. **Moment erstellen:**
   - `narratives[X].storytelling.moments[]`
   - `id`, `parent_storybeat`, `scene_summary`, `pov`, `setting`
3. **Storypoint linken:**
   - `storybeats[].storypoint_id` → `subtext.storypoints[].id`

**Validation:** Nach jedem Akt: `node skills/ncp-author/scripts/validate.js canon/<slug>.ncp.json`

## §7 Hard Rules

- **3 Gates, kein Monolith.** Edits in einem Gate re-run nur dieses Gate
- **NCP-Mutation NUR via ncp-author**
- **Bei dual storyform: parallele Storybeats pro Kapitel** — sonst 5D-Interferenz weg
- **Storybeats müssen Storypoints referenzieren** — sonst Floating Beats
- **Maximal 5-10 Moments pro Kapitel** — sonst zu granular für Drafting
- **Akt-Übergänge respektieren Plot Driver** (Action/Decision) aus architecture.yaml

## §8 Edge Cases

### §8.1 User will andere als 40 Kapitel

→ `intent.chapter_count_target` ändert sich — back to Phase 1?
→ Oder: structure_template anpassen, z.B. 32 = 4×8

### §8.2 Storybeats kollidieren in dual storyform

z.B. Beat A sagt „Plotpunkt X", Beat B sagt „opposite of X"
→ Das KANN intentional sein (5D-Interferenz)
→ Surface in Gate 2: *„Sind diese parallel-counter intentional?"*

### §8.3 Scene-Matrix wird zu groß

z.B. 40 Kapitel × 4 Szenen × 2 narratives = 320 Moments
→ NCP kann das, aber Token-Budget wird teuer
→ Strategy: per-Akt schreiben + packen + Session-Pause

## §9 Exit Gate

Phase 5 ist done (für einen Akt), wenn:
- Akt-Outline approved (Gate 1)
- Chapter-Outline approved (Gate 2)
- NCP storybeats + moments für Akt geschrieben
- `scene-matrix.md` für Akt vollständig
- Validation passed

Bei größeren Projekten: Phase 5 läuft pro Akt iterativ, Phase 6 (Drafting)
kann parallel starten für completed Akte.

## §10 /sc:-Mapping

| Schritt | /sc: Command |
|---|---|
| Akt-Struktur | `sc:design` |
| Kapitel-Outline | `sc:workflow` |
| Scene-Detail | `sc:design` |
| Konsistenz-Check | `sc:analyze` |
