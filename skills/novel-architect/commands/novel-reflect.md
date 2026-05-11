# /novel-reflect — Phase 7 Trigger (3-Mode)

> **Phase:** 7 (Iteration & Refinement)
> **/sc:-Analog:** `sc:reflect`, `sc:improve`, `sc:save`, `sc:analyze`

## Zweck

Continuous iteration loop. 3-Mode-Pattern adaptiert von `spec-skill`:

- **generate:** Roman-Spec aus aktuellem Stand
- **apply:** Workflow-Empfehlung, Canon-Update, OQ-Resolution
- **audit:** Konsistenz-Check zwischen Workspace-Files

## Trigger

- „/novel-reflect"
- „/reflect"
- „Konsistenz prüfen"
- „Audit"
- „Was als nächstes?"
- „OQ-Resolution"
- „Session-Ende"

## Mode-Routing

```
askuser: "Welcher Mode?"
options:
  - "Audit (Konsistenz-Check)"     → Mode: audit
  - "Apply (nächster Schritt)"     → Mode: apply
  - "Generate (Roman-Spec)"        → Mode: generate
  - "Session-Ende (Checkpoint)"    → Mode: apply + Session-End-Checkpoint
```

## Mode: audit

Checkliste (siehe `phases/phase7-iteration.md` §1.3):

1. intent.yaml ↔ architecture.yaml: Methoden konsistent?
2. architecture.yaml ↔ <slug>.ncp.json: NCP-Skeleton vollständig?
3. character-architecture.yaml ↔ NCP players[]: alle gespiegelt?
4. scene-matrix.md ↔ NCP storybeats[]+moments[]: synced?
5. canon-meta.md ↔ drafts/: keine Widersprüche?
6. open-questions.md: blockierende OQs?
7. learnings.md: aktueller Eintrag?

→ `audit-report.md` mit Verdict (pass / fix-recommended / fix-required)

## Mode: apply

Empfiehlt nächsten Schritt. Optionen:
- Phase X starten / weiterführen
- OQ-Y resolved
- Canon-Update für Z
- Research-Brief für <domain>
- Session beenden + Skill packen

## Mode: generate

Erstellt formale Roman-Spec im RFC-2119-Stil:
- §1 Genre & Audience (aus intent.yaml)
- §2 Narrative Architecture
- §3 Character Architecture
- §4 World & Canon
- §5 Scene Matrix
- §6 Konsistenz-Checks (Acceptance Criteria)

→ `roman-spec.md`. Optional delegation an `spec-skill`.

## Session-End-Checkpoint (MANDATORY)

```
1. learnings.md Eintrag (auch wenn null-event)
2. progress.md final update
3. Audit-Mode laufen → verdict pass?
4. Skill packen via scripts/package_skill.sh
5. present_files mit .skill-Datei
```

## Detail

- `phases/phase7-iteration.md`
- `references/significance-heuristics.md`
- `references/ncp-integration-contract.md`
