# Phase 7 — Iteration & Refinement (3-Mode)

> **Load when:** Phase 7 ist aktiv, oder OQ-Resolution, oder Canon-Update,
> oder Session-End-Checkpoint

## §0 Goal

Continuous loop nach jedem Checkpoint: Open Questions Resolution, Canon
Updates, Memory Sync (optional), Skill-Packaging. **3-Mode-Pattern** adaptiert
von `spec-skill`.

## §1 3-Mode-Pattern

| Mode | Trigger | Output |
|---|---|---|
| **generate** | "Erstelle Roman-Spec aus aktuellem Stand" | RFC-2119-Style Roman-Spec (Genre, Charakter, Plot Konsistenz) |
| **apply** | "Was ist der nächste Schritt?", "Welche Methode für X?" | Workflow-Empfehlung, Phasen-Routing |
| **audit** | "Prüfe Konsistenz", "OQ-Check", "Canon-Drift?" | Audit-Report (pass / fix-recommended / fix-required) |

### §1.1 Mode: generate

Generiert eine formale Roman-Spec im RFC-2119-Stil aus aktuellem Stand:

```
Input: intent.yaml + architecture.yaml + character-architecture.yaml + 
       <slug>.ncp.json + scene-matrix.md + canon-meta.md
       
Output: roman-spec.md (RFC-2119, Gherkin-Scenarios)
  - §1 Genre & Audience (MUST conform to intent.yaml)
  - §2 Narrative Architecture (Storyforms, Throughlines, Dynamics)
  - §3 Character Architecture (Players, Psycho-Models)
  - §4 World & Canon (Lore, Mandates)
  - §5 Scene Matrix (Akt → Kapitel → Szene)
  - §6 Konsistenz-Checks (Acceptance Criteria)
```

Optional delegation: `spec-skill` für formale Spec-Erstellung.

### §1.2 Mode: apply

Konkrete Workflow-Empfehlung basierend auf aktuellem Stand:

```
Input: progress.md + open-questions.md + project-config.yaml
Output: askuser mit empfohlenem nächsten Schritt
  Optionen aus:
  - "Phase X starten / weiterführen"
  - "OQ-Y resolved"
  - "Canon-Update für Z"
  - "Research-Brief für <domain>"
  - "Session beenden + Skill packen"
```

### §1.3 Mode: audit

Konsistenz-Check zwischen allen Workspace-Files:

```
Checks:
  1. intent.yaml ↔ architecture.yaml: Methoden konsistent?
  2. architecture.yaml ↔ <slug>.ncp.json: NCP-Skeleton vollständig?
  3. character-architecture.yaml ↔ NCP players[]: alle Charaktere gespiegelt?
  4. scene-matrix.md ↔ NCP storybeats[]+moments[]: alle Kapitel synced?
  5. canon-meta.md ↔ drafts/: keine Drafts widersprechen Canon?
  6. open-questions.md: blockierende OQs für nächste Phase?
  7. learnings.md: aktueller Eintrag für diese Session?

Output: audit-report.md
  Verdict: pass / fix-recommended / fix-required
  - Pass: alle Checks OK
  - Fix-recommended: nicht-blockierend, sollte gefixt werden
  - Fix-required: blockierend für nächste Phase
```

## §2 Iteration Discipline (Übernommen aus Legacy)

Detail-Heuristik in `references/significance-heuristics.md`.

### §2.1 Was ist „signifikant" (= Checkpoint-Trigger)

Ein Checkpoint löst aus:
1. `progress.md` im Projekt-Workspace aktualisieren
2. **NCP-Update** falls strukturell: `<slug>.ncp.json` via `ncp-author`
3. **canon-meta.md aktualisieren** falls nicht-strukturell
4. **`learnings.md` Eintrag** (mandatorisch bei Session-End)
5. **memory-sync NUR** wenn User explizit Memory-Broadcast wünscht
6. **Skill packen** via `bash scripts/package_skill.sh`
7. `present_files` mit `.skill`-Datei + Output-Artefakt

### §2.2 Checkpoint triggert wenn

- **Canon-Shift (strukturell)** — NCP-Mutation
- **Canon-Shift (nicht-strukturell)** — canon-meta.md Änderung
- **Phase-Unit complete** — Throughline encoded, Akt-Block gemapped, Chapter draft fertig
- **Workflow-Pivot** — User wechselt Phase
- **Volume threshold** — 3+ neue Files oder ~2000 Wörter
- **Session-End** — immer

### §2.3 Was ist NICHT signifikant (kein Package)

- Term-Lookup in dramatica-vocabulary
- Q&A ohne Canon-Berührung
- Brainstorm ohne Festlegung
- Reference-Reading

## §3 Hard Rules

- **Memory-Sync ist outward-only und explizit opt-in.** Niemals Memory→Skill
- **NCP-Mutation NUR via ncp-author**
- **Session-End-Checkpoint ist mandatorisch** — auch wenn nichts auffiel
- **learnings.md Eintrag pro Session** — auch wenn „nichts auffälliges" steht als Eintrag

## §4 OQ-Resolution Workflow

```
1. Lade open-questions.md
2. Für jede OQ: 
   - Trigger-Bedingung erfüllt? (z.B. genug Recherche, Charakter klar)
   - Resolution-Workflow vorhanden? (Phase 1 für Intent, Phase 2 für Architektur, etc.)
3. askuser: "OQ-X resolved? Entscheidung: ___"
4. Bei Resolution:
   - update open-questions.md (Strikethrough mit Resolution-Datum)
   - update entsprechende Workspace-File (intent/architecture/canon-meta/NCP)
   - falls NCP betroffen: delegate ncp-author
   - update progress.md
   - learnings.md Eintrag (falls relevant)
5. Checkpoint
```

## §5 Canon-Update Workflow

```
1. Surface canon-shift trigger (z.B. "AEGIS-Direktive ändert sich")
2. Klassifizieren: strukturell (NCP) oder nicht-strukturell (canon-meta)?
3. Bei strukturell: delegate ncp-author + entsprechender NCP-Workflow
4. Bei nicht-strukturell: edit canon-meta.md (mit Datum-Stempel)
5. Cascading checks:
   - Beeinflusst das Character-Architecture? → Phase 3 update
   - Beeinflusst das Scene-Matrix? → Phase 5 update
   - Beeinflusst das gedraftete Kapitel? → drafts/ revision needed
6. update open-questions.md (closed?)
7. Checkpoint
```

## §6 Session-End-Workflow

```
MANDATORY am Session-Ende:
1. learnings.md Eintrag schreiben (auch wenn null-event)
2. progress.md final update
3. Audit-Mode laufen lassen (siehe §1.3) → verdict pass?
4. Skill packen via scripts/package_skill.sh
5. present_files mit .skill-Datei
```

## §7 Edge Cases

### §7.1 OQ resolved, aber NCP-Update zerstört existing storybeats

→ Surface conflict
→ Optionen: Soft-Resolve (canon-meta only) / Hard-Resolve (NCP + cascading)

### §7.2 Memory enthält älteren Stand als Skill-Files

→ Per Skill-Constraint: Skill-Files gewinnen
→ User aktiv darüber informieren
→ Memory wird NICHT automatisch synced

### §7.3 Audit-Mode findet Drift

→ Verdict: fix-required für blockierende, fix-recommended für nicht-blockierende
→ User entscheidet Fix-Order
→ Bei multiplen Drifts: priorisieren (NCP > canon-meta > scene-matrix > drafts)

## §8 Exit Gate

Phase 7 hat **keine Exit Gate** — sie ist kontinuierlich. Aber für Session-End:
- learnings.md Eintrag exists
- progress.md aktuell
- Audit verdict: pass (oder fix-required explizit deferred)
- Skill gepackt

## §9 /sc:-Mapping

| Mode / Schritt | /sc: Command |
|---|---|
| Mode generate | `sc:document`, `sc:design`, optional `spec-skill` |
| Mode apply | `sc:recommend`, `sc:workflow` |
| Mode audit | `sc:analyze`, `sc:test` |
| Self-Improvement | `sc:reflect`, `sc:improve` |
| Session-Save | `sc:save` |
| Skill-Packaging | (manuell: `bash scripts/package_skill.sh`) |
