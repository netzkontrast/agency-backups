---
type: note
status: active
slug: claude-review-pr50
summary: "Claude Code review of PR #50 — governance specs update plan. Identifiziert Spec-Verstöße und Qualitätsmängel in Jules' Einreichung."
created: 2026-05-05
updated: 2026-05-05
---

# Claude Code Review — PR #50: Governance Specs Update Plan

**Reviewed branch:** `jules-governance-update-plan-9348435567774060218` → `main`  
**PR:** [#50](https://github.com/netzkontrast/agency/pull/50)  
**Reviewer:** Claude Code (`claude/stoic-mendel-4m1LT`)  
**Datum:** 2026-05-05

---

## Executive Summary

PR #50 erstellt erfolgreich das strukturelle Gerüst für einen Governance-Specs-Updatezyklus: Prompt, Research-Workspace, Task 026 und die Supersession von Task 001. Dennoch müssen mehrere Spec-Verstöße und Qualitätsmängel vor dem Merge behoben werden.

---

## Verstöße (MUST-Ebene)

### V1 — `updated:`-Feld in Task 001 nicht aktualisiert (TASK.md §4.7, AGENTS.md L1)

`tasks/001-refactor-governance-from-specs/task.md` wechselt `task_status` von `done` → `updated` und ergänzt `task_superseded_by` — beides am 2026-05-05 — jedoch liest das L1-Feld `updated:` weiterhin `2026-05-04`.

Per AGENTS.md L1 Field Semantics:
> `updated` — MUST be updated on every substantive change.

Per TASK.md §4.7:
> "the predecessor's `updated` field MUST be set to today's ISO date."

**Fix:** `updated: 2026-05-04` → `updated: 2026-05-05` in `tasks/001-refactor-governance-from-specs/task.md`.

---

### V2 — `brief.md` enthält Paraphrase statt unverändertem User-Request (PROMPT.md §4.2, §6.1)

`prompts/governance-specs-update-research/brief.md` enthält:

> "The user wants to review the current tooling and specs (`MAINTENANCE.md`, `PRE_COMMIT.md`, `FOLDERS.md`, etc.), particularly focusing on how to update them after Task 001. The objective is to create an update plan for these specs."

PROMPT.md §4.2 verlangt:
> **Store Brief** — Save the **unedited user request** and contextual metadata into `brief.md`. **This is the immutable record of what was asked.**

§6.1 präzisiert:
> **Brief Integrity** — `brief.md` exists and contains the **exact, unedited user request**.

Eine Dritte-Person-Paraphrase ("The user wants to...") ist nicht der wörtliche Input. Sie unterbricht die Audit-Kette und ist damit eine mechanisch durchsetzbare Integritätsverletzung.

**Fix:** `brief.md` durch den literal empfangenen Jules-Prompt ersetzen.

---

### V3 — `notes.md` in Task 026 enthält ungefüllte Template-Boilerplate (TASK.md §5)

`tasks/026-update-governance-specs-from-research/notes.md` wurde mit leeren Platzhaltern committed:

- Titel: `# Notes — Task NNN-<slug>` (der Slug ist bekannt)
- Abschnitt: `## Session — YYYY-MM-DD` ohne Datum
- Mehrfach: `REPLACE — one paragraph explaining what is blocking progress.`
- Spec-Referenzen (`Spec-I.3.1`) als strukturelle Boilerplate ohne inhaltlichen Bezug

Ein operational file in Template-Zustand zu committen stellt einen Inhaltsintegritätsfehler dar. `notes.md` soll Ist-Zustand dokumentieren, nicht Template-Scaffolding.

**Fix:** Datei entweder mit einem echten Session-Eintrag füllen oder auf ein minimales datiertes Stub reduzieren.

---

## Qualitätsmängel (SHOULD-Ebene)

### Q1 — `SPEC.md` zu dünn für einen "detaillierten Update-Plan"

Der Prompt deklariert `RISEN+ReAct` als Framework — was iterative Observe/Think/Act-Zyklen erfordert. Das Output-`SPEC.md` ist 34 Zeilen lang und nutzt durchgängig Bullet-Assertions ohne Gherkin-Scenarios. `synthesis/methodology.md` listet exakt eine Methode (M06 Source Triangulation), obwohl der Prompt vier ReAct-Schritte über fünf separate Dateien vorschreibt.

Per AGENTS.md Gherkin Rule G6:
> "Acceptance criteria in this repository MUST be written as Gherkin scenarios, not as bullet-list assertions."

Diese Regel gilt primär für normative Specs, nicht für Research-Output — dennoch deutet das Missverhältnis zwischen Prompt-Versprechen (RISEN+ReAct) und gelieferter Substanz (flache Bullets) auf unzureichende Ausführungstiefe hin.

**Empfehlung:** Task 026 SOLLTE die SPEC.md-Empfehlungen als grobe Startrichtung behandeln, nicht als implementierbare Spezifikationen. Jede Sektion benötigt Gherkin-Acceptance-Criteria, bevor Änderungen an den Root-Specs committed werden.

---

### Q2 — FL0-Deklaration fragwürdig (FRUSTRATED.md)

`research/governance-specs-update-research/reflection/friction-log.md` behauptet:
> "No friction encountered. The specs and run logs were very detailed and easy to synthesize."

Bei einem Output von 34 Zeilen für die Analyse von fünf Governance-Dokumenten plus `check-governance.sh`, und bei einer Methodik, die nur eine einzige Methode (M06) dokumentiert, erscheint FL0 optimistisch. FRUSTRATED.md verlangt ehrliche FL-Deklarationen. FL0 bei dünnem Output auf nicht-trivialem Input ist ein gelbes Flag.

---

### Q3 — Task 026 ohne `task_blocked_by` trotz potentieller Abhängigkeit

Task 025 (`025-maintenance-spec-remaining-findings`) ist explizit durch Task 019 geblockt und modifiziert dieselben Dateien (`MAINTENANCE.md`, `TASK.md`) wie Task 026. Sollte Task 019's Toolchain-Migration diese Dateien strukturell verändern, entstehen potentielle Konflikte.

Das Fehlen von `task_blocked_by` ist kein harter Verstoß (OPTIONAL), aber TASK.md §8.7 setzt voraus, dass Inter-Task-Abhängigkeiten bewusst evaluiert werden. Diese Evaluation fehlt in `notes.md`.

---

## Positive Befunde

- `research_executes_prompt` in `research/governance-specs-update-research/readme.md` verlinkt korrekt. ✓
- Task 026 Task-Namespace-Frontmatter vollständig und korrekt strukturiert. ✓
- Supersession-Reziprozität zwischen Task 001 und Task 026 korrekt gesetzt. ✓
- `tasks/readme.md` im selben Commit aktualisiert. ✓
- `prompt.md`-Snapshot in `research/governance-specs-update-research/prompt.md` konform zu RESEARCH.md §4.3. ✓

---

## Gesamturteil

**Empfehlung: Changes Requested**

V1 und V2 sind MUST-Verstöße, die vor Merge behoben werden MÜSSEN. V3 ist ein Qualitätsfehler, der behoben werden SOLLTE. Das strukturelle Gerüst (Task 026, Research-Workspace, Supersession) ist solide; Metadaten-Genauigkeit und Inhaltsqualität benötigen Nachbesserung.
