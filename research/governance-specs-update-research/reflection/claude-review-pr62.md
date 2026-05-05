---
type: note
status: active
slug: claude-review-pr62
summary: "Claude Code review of PR #62 — Task 026 closure: governance spec updates implementation. Identifiziert drei MUST-Verstöße und drei SHOULD-Mängel."
created: 2026-05-05
updated: 2026-05-05
---

# Claude Code Review — PR #62: Close Task 026 — Implement Governance Spec Updates

**Reviewed branch:** `claude/adr-spec-research-synthesis-ZwFB2` → `main`  
**PR:** [#62](https://github.com/netzkontrast/agency/pull/62)  
**Reviewer:** Claude Code (`claude/stoic-mendel-Ymp9e`)  
**Datum:** 2026-05-05  
**Commits:** `1728b35` (feat: spec updates), `2fa7c95` (chore: orphan cleanup)  
**Scope:** Zwei Commits. Commit 1 implementiert die vier SPEC.md-Empfehlungen und schließt Task 026. Commit 2 entfernt den Orphan-Folder `tasks/026-adr-spec-research-synthesis/`.

---

## Executive Summary

PR #62 implementiert die vier Governance-Spec-Updates aus `research/governance-specs-update-research/output/SPEC.md` korrekt und vollständig. Die chirurgischen Einfügungen in MAINTENANCE.md, PRE_COMMIT.md, FOLDERS.md und TASK.md sind substanziell und schließen echte Lücken. Task 026 wird formal korrekt geschlossen. Dennoch bestehen drei MUST-Verstöße, die vor dem Merge behoben werden MÜSSEN: SS.2-Verstoß im ersten Commit, inkonsistenter L1-`status`-Wert in `task.md`, und unvollständige `task_affects_paths`. Drei SHOULD-Mängel werden zusätzlich angemerkt.

---

## Verstöße (MUST-Ebene)

### V1 — SS.2-Verstoß in Commit 1 (`1728b35`)

**Betroffene Datei:** `tasks/026-update-governance-specs-from-research/friction-log.md` (eigene Dokumentation)  
**Spec:** AGENTS.md §Session Setup, Regel SS.2:
> "An agent MUST run `tools/check-governance.sh` immediately after `install.sh` completes and MUST NOT proceed if it exits non-zero."

Commit `1728b35` wurde erstellt, während `tools/check-governance.sh` aufgrund des Orphan-Folders `tasks/026-adr-spec-research-synthesis/` (kein `task.md`, kein `readme.md`) non-zero exitete. Der `friction-log.md` dokumentiert dies transparent (FL1, Punkt 1) — das PR-Body eskaliert die Entscheidung an den Reviewer. Transparenz ist positiv, aber sie substituiert die Compliance nicht: SS.2 enthält keine Carve-out-Klausel für "pre-existing failures unrelated to the current change".

**Kontext:** Die Sequenz ist nachvollziehbar — Commit 2 (`2fa7c95`) stellt Compliance wieder her — dennoch verletzt Commit 1 SS.2 zum Commit-Zeitpunkt.

**Erforderliche Maßnahme:** Entweder (a) die Orphan-Cleanup-Arbeit hätte *vor* den Spec-Updates committed werden sollen (Commit-Reihenfolge umkehren), oder (b) beide Änderungen in einem einzigen Commit zusammenfassen, sodass `check-governance.sh` zum Commit-Zeitpunkt grün ist. Die aktuelle Commit-Reihenfolge ist in der Merge-History technisch sauber, widerspricht aber SS.2 für Commit 1 isoliert.

---

### V2 — L1 `status: active` in `task.md` nicht auf `completed` aktualisiert

**Betroffene Datei:** `tasks/026-update-governance-specs-from-research/task.md`  
**Spec:** AGENTS.md §Frontmatter Ontology, L1 Field Semantics:
> "`status` — One of: `draft`, `active`, `blocked`, `completed`, `archived`."
> "`updated` — MUST be updated on every substantive change."

Die Datei hat korrekt `task_status: done` (L2-Namespace) gesetzt, aber das L1-Feld `status: active` wurde nicht aktualisiert. Wenn eine Task geschlossen wird (`task_status: done`), MUSS das L1-`status`-Feld auf `completed` wechseln, da `active` bedeutet, dass das Artefakt noch in Bearbeitung ist. Agenten, die nach der Semantik von `status: archived` skippen, lesen `status: active` als "in Bearbeitung" — ein falscher positiver Befund in jedem Future-Agent-Scan.

Ein Präzedenzfall für diese Inkonsistenz findet sich auch in `claude-review-pr51.md` nicht (da dort Task 026 noch nicht geschlossen war), aber das Muster — L1 `status` nicht synchron mit L2 `task_status` zu halten — wurde in vorherigen Reviews als Inhaltsintegritätsfehler eingestuft.

**Fix:** `status: active` → `status: completed` in `tasks/026-update-governance-specs-from-research/task.md`.

---

### V3 — `task_affects_paths` unvollständig

**Betroffene Datei:** `tasks/026-update-governance-specs-from-research/task.md`  
**Spec:** TASK.md §7.4 (Closure Pre-Commit Check, Punkt 4):
> "**Path Containment** — Files modified by the Task fall within `task_affects_paths` (or the agent has updated that list to reflect reality)."

Das aktuelle `task_affects_paths` listet:
```yaml
task_affects_paths:
  - MAINTENANCE.md
  - PRE_COMMIT.md
  - FOLDERS.md
  - TASK.md
```

Diese PR-Session modifiziert aber zusätzlich:
- `tasks/026-adr-spec-research-synthesis/notes.md` — gelöscht (Commit 2)
- `tasks/readme.md` — `done`-Status-Update
- `tasks/026-update-governance-specs-from-research/friction-log.md` — neu erstellt
- `tasks/026-update-governance-specs-from-research/readme.md` — Link zu `friction-log.md` ergänzt

Vier Pfade fehlen. TASK.md §7.4 erlaubt nachträgliche Aktualisierung ("or the agent has updated that list to reflect reality"), aber die Liste wurde nicht aktualisiert.

**Fix:** `task_affects_paths` um die vier fehlenden Pfade ergänzen.

---

## Qualitätsmängel (SHOULD-Ebene)

### Q1 — TASK.md §8.1 — Normative Schritte ohne RFC 2119 Keywords

**Betroffene Datei:** `TASK.md`  
**Spec:** AGENTS.md §Spec Language Reference, R1:
> "Every normative statement MUST use exactly one RFC 2119 keyword per sentence."

Die vier neuen nummerierten Schritte unter "Until a linter check is added..." sind de-facto normative Agenten-Verpflichtungen:
1. "Before creating a new `tasks/<NNN>-<slug>/` folder, run `ls tasks/ | sort`..."
2. "Run `git fetch origin main && git ls-tree...`..."
3. "If the slot is used, pick the next free `<NNN>` immediately..."
4. "When the agent encounters an *existing* duplicate..., the agent MUST file a renumber Task..."

Schritt 4 verwendet korrekt `MUST`. Schritte 1–3 sind jedoch als normative Imperative formuliert, ohne RFC 2119 Keyword. Konsistente Formulierung: "An agent MUST run `ls tasks/ | sort`...", "An agent MUST also run `git fetch origin main...`", "An agent MUST pick the next free `<NNN>` immediately."

---

### Q2 — Deletion des Orphan-Folders ohne formelle T3-Dokumentation

**Betroffene Dateien:** `tasks/026-adr-spec-research-synthesis/notes.md` (deleted)  
**Spec:** MAINTENANCE.md §3.5 (neu eingeführt in diesem PR):
> "Because the change spans multiple files and rewrites cross-references, the maintenance agent MUST NOT perform the renumber inline during a coherence run. Instead it MUST file a Task..."

§3.5 adressiert explizit T3-Renummerierungen, nicht Löschungen — daher ist dies kein MUST-Verstoß. Dennoch ist die Analogie stark: Das Löschen eines unvollständig strukturierten Ordners direkt im selben PR wie die inhaltliche Task-Arbeit weicht vom Geist des neu eingeführten §3.5 ab, der strukturelle Aktionen in dedizierte Tasks auslagern soll. Die Sequenzierung (Spec-Updates in Commit 1, Cleanup in Commit 2 desselben Branch) ist pragmatisch sauber, aber methodisch inkonsistent mit dem Prinzip, das §3.5 schützt.

**Empfehlung:** Zukünftige Orphan-Folder-Cleanups SOLLTEN entweder als vorangehender Commit auf einem separaten Branch oder als eigene Task (z.B. Task 024-Klasse) durchgeführt werden, nicht als nachgestellter Commit im selben Feature-Branch.

---

### Q3 — `research_phase: complete` Workspace erneut modifiziert (Anschluss an B.V6)

**Betroffene Datei:** `research/governance-specs-update-research/reflection/readme.md`  
**Spec:** RESEARCH.md §1:
> "`/research/` IS: A read-mostly archive once a run is `complete` or `archived`."

Dieser PR berührt die Reflection-Artefakte des `governance-specs-update-research`-Workspace nicht direkt. Der vorliegende Review-Commit (von `claude/stoic-mendel-Ymp9e`) fügt jedoch erneut eine Datei in `reflection/` ein — das Muster einer Modifikation eines `complete`-Workspace ohne `research_phase`-Rücksetzung wurde bereits in `claude-review-pr51.md` als B.V6 eingestuft und ist für jede nachfolgende Session weiterhin relevant.

**Empfehlung:** Der Review-Autor-Commit (dieser hier) SOLLTE das `research_phase`-Feld in `research/governance-specs-update-research/readme.md` temporär auf `reflection` zurücksetzen und nach Abschluss des Review-Zyklus auf `complete` zurückführen.

---

## Positive Befunde

### P1 — Vollständige und korrekte Spec-Implementierung

Alle vier SPEC.md-Empfehlungen wurden chirurgisch und präzise implementiert:
- MAINTENANCE.md §1.1 (Toolchain Migration Context) ✓
- MAINTENANCE.md §3.5 (Duplicate `task_id` Governance) ✓
- PRE_COMMIT.md §7.A (Toolchain Selection Matrix) ✓
- PRE_COMMIT.md §7.B (Frontmatter Waivers — Burn Protocol) ✓
- FOLDERS.md §4.1 (Mandatory Scaffold for `/prompts/<slug>/`) ✓
- TASK.md §7.3 (Research Linkage Enforcement Scope) ✓
- TASK.md §8.1 (Duplicate IDs — Enforcement Status) ✓

### P2 — Friction-Log ehrlich und substanziell (FL1)

`friction-log.md` benennt beide FL1-Quellen klar: den pre-existing Governance-Check-Fehler und den `task_id: "026"` Kollision. Die Empfehlung für einen T3-Cleanup-Task ist konkret und actionable. Kein FL0-Greenwashing.

### P3 — Two-Commit-Struktur konzeptuell sauber

Die Trennung von Spec-Updates (Commit 1) und Orphan-Cleanup (Commit 2) ist konzeptuell sauber — jeder Commit hat einen klar definierten Scope. Die commit messages sind präzise und referenzieren den Session-URL.

### P4 — MAINTENANCE.md §3.5 ist genuiner Governance-Beitrag

Die T3-Renumbering-Prozedur mit den sechs Schritten (identify → pick → rename → rewrite → update readme → verify) schließt eine echte Lücke. Die Unterscheidung zwischen T3-Aktionen und T1/T2-Mutationen ist korrekt angewendet. Der Querverweis auf `tools/fm/edit.py` ist präzise.

### P5 — PRE_COMMIT.md §7.B Burn Protocol gut spezifiziert

Die fünf Regeln sind klar, mutual-exclusive, und adressieren reale Failure-Modes (Task 001 FL1-Finding direkt zitiert). Rule 5 (Re-expression at toolchain flip) ist besonders wertvoll als Future-Proof-Klausel.

### P6 — Todo-Completion und Task-Closure korrekt

Alle vier `- [x]` Todos abgehakt. `task_status: done`, `task_owner: "claude-code"`. `tasks/readme.md` auf `done` aktualisiert. `friction-log.md` und `readme.md`-Link korrekt hinzugefügt.

---

## Gesamturteil

**Empfehlung: Changes Requested**

| # | Schwere | Beschreibung | Status |
|---|---|---|---|
| V1 | MUST | SS.2-Verstoß: Commit 1 bei non-zero `check-governance.sh` | Offen |
| V2 | MUST | L1 `status: active` nicht auf `completed` gesetzt | Offen |
| V3 | MUST | `task_affects_paths` unvollständig (4 Pfade fehlen) | Offen |
| Q1 | SHOULD | TASK.md §8.1 Steps 1–3 ohne RFC 2119 Keywords | Offen |
| Q2 | SHOULD | Orphan-Cleanup direkt im Feature-Branch statt dedizierter Task | Info |
| Q3 | SHOULD | `research_phase: complete` Workspace modifiziert | Offen |

V2 und V3 sind mechanisch lösbare Frontmatter-Korrekturen, die in einem Fix-Commit vor Merge behoben werden SOLLTEN. V1 ist eine Commit-Hygiene-Frage, die der Reviewer mit Kenntnis des Zwei-Commit-Kontexts beurteilen muss — der finale Merge-Zustand ist `check-governance.sh`-konform, aber die Commit-Historie dokumentiert einen non-compliant Zwischenstand.

Die inhaltliche Qualität der Spec-Updates ist hoch. Kein Review-Artefakt aus dem PR-52-Review-Zyklus (A.V1, A.V2 aus `claude-review-pr50.md` und `claude-review-pr51.md`) bleibt unresolved in diesem PR — diese Punkte wurden in separaten Merge-Commits adressiert oder sind out-of-scope für Task 026.
