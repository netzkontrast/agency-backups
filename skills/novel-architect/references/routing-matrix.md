# Routing Matrix — Methodisch (v1.0)

> **Load when:** Workflow-Verzweigung mehrdeutig, oder Phase-Übergang
> **Replaces:** Legacy `workflows.md` (war projekt-spezifisch für Kohärenz Protokoll)

## §0 Konzept

Methodische Routing-Tabelle — welche Trigger-Phrasen führen zu welcher Phase
und welchem Skill-Stack. Anders als Legacy-Matrix: nicht 10 projekt-spezifische
Workflows, sondern 8 generische Phasen.

## §1 Phasen-Routing

| Trigger-Phrase | Phase | Skill-Stack |
|----------------|-------|-------------|
| „Starte Roman", „Neues Projekt", „Setup" | 0 — Bootstrap | self |
| „Was ist mein Genre", „Audience", „Konflikt-Frage" | 1 — Intent Capture | self |
| „Storyform", „Throughlines", „Dynamics", „Klassen" | 2 — Architecture | dramatica-theory → dramatica-vocabulary → ncp-author → self |
| „Charaktere", „Players", „Persönlichkeit", „Beziehungen" | 3 — Characters | dramatica-vocabulary → ncp-author → self |
| „Welt", „Recherche", „Forschung", „World-Bible" | 4 — World & Research | research-prompt-optimizer → self |
| „Akt-Struktur", „Kapitel-Plan", „Scene-Matrix", „Storybeats" | 5 — Scene Matrix | dramatica-theory → ncp-author → self |
| „/draft", „Kapitel X schreiben", „Prosa" | 6 — Drafting | self → dramatica-vocabulary → (docx) |
| „/reflect", „Konsistenz-Check", „Audit", „OQ-Resolution" | 7 — Iteration | self → ggf. spec-skill → ncp-author |
| „Kanon ändern", „resolved" | 7 — Iteration (apply) | ncp-author + canon-meta-Edit → self |

## §2 Sub-Workflow-Routing (innerhalb Phase 7)

| Trigger | Sub-Workflow | Mode |
|---------|--------------|------|
| „Erstelle Roman-Spec" | Phase 7.1 (generate) | generate |
| „Was als nächstes" | Phase 7.2 (apply) | apply |
| „Prüfe Konsistenz", „Audit" | Phase 7.3 (audit) | audit |
| „Memory updaten" (explizit) | Phase 7 + memory-sync | apply |
| „Skill packen" | Phase 7 + scripts/package_skill.sh | apply |

## §3 Cross-Skill-Delegations-Karte

Per AGENTS.md NO.2 + Skill-Delegation-Map:

| Roman-Frage | Delegate to | Navigator |
|---|---|---|
| „Warum ist diese Class/Type/Variation richtig?" | dramatica-theory | (prose) |
| „Storyform diagnose" | dramatica-theory | (prose) |
| „Dynamic Pair check" | dramatica-vocabulary | `nav.py by-id <id> --include-pairs` |
| „Element-Quad lookup" | dramatica-vocabulary | `nav.py by-quad quad.<name>-el` |
| „NCP enum string" | ncp-author | `nav.py by-ncp '<string>'` |
| „NCP Schema validation" | ncp-author | `node ncp-author/scripts/validate.js` |
| „Deep Research Prompt" | research-prompt-optimizer | n/a |
| „PDF → Markdown" | pdf-to-markdown (oder Fallback in scripts/) | n/a |
| „Drive sync" | drive-markdown-converter | n/a |
| „Memory broadcast (explizit)" | memory-sync | n/a |
| „Spec aus Stand generieren" | spec-skill (optional in Phase 7 generate) | n/a |
| „Skill packen" | skill-creator/scripts/package_skill.py | n/a |

## §4 Routing-Heuristik

- **Mehrdeutige Trigger:** kurz nachfragen via `ask_user_input_v0`, max 4 Optionen
- **Multi-Phase Trigger:** z.B. „Setup neuer Roman" könnte 0+1 sein — beide ankündigen, sequenziell durchlaufen
- **Workflow-Pivot innerhalb Session:** progress.md notiert beide; ist Checkpoint-Trigger
- **Unbekannter Trigger:** generic askuser „Was möchtest du?" mit Phase-Liste

## §5 Anti-Patterns

- „Triggert dramatica-theory" als Antwort — niemals, delegate properly
- Phase überspringen weil „Trigger sagt Phase 5, aber Phase 2 nicht done" — invalid, abbrechen
- Beliebige Phase-Reihenfolge — Phase-Hand-off-Kontrakt ist sequenziell
