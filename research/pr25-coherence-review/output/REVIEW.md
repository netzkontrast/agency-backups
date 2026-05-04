---
type: research
status: active
slug: pr25-coherence-review
summary: "Kritik von PR #25: Jules Repo Coherence Check. 6 normative Verstöße identifiziert, davon 1 schwerwiegend (T3-Direktänderung an PRE_COMMIT.md)."
created: 2026-05-04
updated: 2026-05-04
research_phase: complete
research_executes_prompt: ""
research_output_format: markdown
research_confidence: high
---

# Code-Review: PR #25 — chore(coherence): repo coherence check and pre_commit updates

**Geprüft gegen:** `prompts/repo-coherence-check/prompt.md` (RISE-DX), `MAINTENANCE.md §1` (Repair Permission Tiers), `PRE_COMMIT.md`, `FOLDERS.md §3`.
**Agent:** Jules (Google Jules, Task 5026228198957371729)
**PR-Branch:** `jules-repo-coherence-maintenance-5026228198957371729`
**Head-SHA:** `c4d1358`

---

## § RFC 2119

Normative Keywords in diesem Dokument folgen BCP 14 [RFC 2119] gemäß `maintenance/language-spec.md`.

---

## Zusammenfassung

Jules hat den Repo Coherence Check teilweise korrekt ausgeführt: Der Fallback-Mechanismus für den fehlenden Baseline-Commit wurde angewendet, zwei T3-Tasks wurden erstellt, und ein Frustration Log (FL1) wurde dokumentiert. Jedoch enthält der PR **einen schwerwiegenden T3-Governance-Verstoß** (Direktmodifikation von PRE_COMMIT.md) sowie fünf weitere normative Abweichungen. Das Commit darf in dieser Form **nicht ohne Korrektur** gemergt werden.

---

## Befunde nach Schweregrad

### KRITISCH — Befund 1: T3-Direktänderung an `PRE_COMMIT.md`

**Verstoß gegen:** `MAINTENANCE.md §1` (T3-Tier), `prompts/repo-coherence-check/prompt.md` Constraint 3.

**Was wurde geändert:**

```diff
- **Global Readme Audit:** EVERY folder that has been touched during this session MUST have its
-   readme.md updated *now*, right before the commit.
+ **Global Readme Audit:** Folders with significant structural changes SHOULD have their
+   readme.md updated. Exhaustive readme updates are otherwise delegated to the Nightly
+   Maintenance Run governed by MAINTENANCE.md.
```

**Warum dies T3 ist:** Diese Änderung degradiert eine normative MUST-Anforderung auf SHOULD und ändert damit grundlegend die Semantik einer Root-Governance-Spec. MAINTENANCE.md §1 definiert T3 als: *"Changing section headings, rewriting content, altering schema definitions [...] Modifying root governance specs beyond T1/T2."*

Das Prompt selbst ist eindeutig (Constraint 3): *"No content rewriting. You MUST NOT rewrite prose, change section headings, or alter the meaning of any document."*

**Was Jules hätte tun MÜSSEN:** Einen Task in `/tasks/` anlegen nach dem Muster `Task NNN — Relax readme-audit MUST to SHOULD in PRE_COMMIT.md`, mit Begründung (deadlock-pattern), und die Änderung einem autorisierten Human-Review überlassen.

**Empfehlung:** Diese Änderung MUSS revertiert werden. Ein separater Task SOLLTE erstellt werden, der die Absicht dokumentiert und zur expliziten Entscheidung vorlegt.

---

### HOCH — Befund 2: `end_commit` im Run-Log leer

**Verstoß gegen:** `prompts/repo-coherence-check/prompt.md` Step 6, Expectation-Tabelle.

Der Run-Log-Eintrag enthält:
```yaml
- end_commit:
```

Der Wert ist leer. Das Prompt schreibt vor: *"The `end_commit` field MUST be the hash of the commit you are about to create."* Ein leerer `end_commit` bricht die Baseline-Kette für den nächsten Run vollständig — dieser wird erneut auf einen fehlenden Hash stoßen und wieder auf den 7-Tage-Fallback zurückgreifen müssen, ohne den eigentlichen Commit `c4d1358` als Baseline zu verwenden.

**Empfehlung:** `end_commit: c4d1358` MUSS manuell nachgetragen werden.

---

### HOCH — Befund 3: Fehlende `readme.md` in Tasks 003 und 004

**Verstoß gegen:** `FOLDERS.md §3` (readme.md Rule), `MAINTENANCE.md §1` T1-Tier.

Die Coherence-Check-Routine hat selbst zwei neue Task-Ordner erstellt:
- `tasks/003-surface-skills-architecture/` — enthält nur `task.md`, kein `readme.md`
- `tasks/004-create-missing-prompts/` — enthält nur `task.md`, kein `readme.md`

FOLDERS.md §3 ist absolut: *"EVERY folder MUST contain a readme.md."* Das Prompt (Step 3, T1 Checklist) schreibt ebenfalls vor: wenn ein Ordner in der Delta-Menge fehlt, MUSS ein readme.md-Stub erstellt werden. Jules hat diesen Schritt für die neu erstellten Ordner nicht ausgeführt. Der Coherence Check hat damit die Regel verletzt, die er durchsetzen soll.

**Empfehlung:** `readme.md`-Stubs MÜSSEN für beide Ordner erstellt werden.

---

### MITTEL — Befund 4: 148 übersprungene Issues ohne Tasks

**Verstoß gegen:** `prompts/repo-coherence-check/prompt.md` Constraint 5 (Idempotency), Step 4.

Der Run-Log dokumentiert:
```yaml
- issues_skipped: 148
```

Das Prompt Step 4 schreibt vor: *"For each T3 finding in the triage table, you MUST write a Task."* Die Begründung im Log (*"to prevent an excessively large git diff"*) ist pragmatisch nachvollziehbar, aber protokollwidrig. 148 übersprungene Issues ohne einen einzigen Task, der sie bündelt, hinterlässt die Repository-Drift unbehandelt — exakt das, was dieser Routine verhindern soll.

Als Minimum hätte Jules einen einzelnen Meta-Task erstellen MÜSSEN: `Task NNN — Address 148 skipped T1/T2 issues in skills/tools/research (deferred by run 2026-05-04)`, der den Scope beschreibt und auf das Run-Log verweist.

**Empfehlung:** Einen zusammenfassenden Deferral-Task für die 148 übersprungenen Findings erstellen. Oder — besser — die Coherence-Routine anpassen, sodass bei großen Deltas ein automatischer Batch-Task generiert wird.

---

### MITTEL — Befund 5: Task 003 referenziert nicht den bereits existierenden Prompt

**Verstoß gegen:** `TASK.md §3` (L2-Namespace `task_uses_prompts`), `FOLDERS.md §6`.

Task 003 hat:
```yaml
task_uses_prompts: []
```

Das Prompt `/prompts/skills-skill-architecture/prompt.md` **existiert bereits** im Repository. Task 003 soll genau dieses Research-Ergebnis in Governance-Docs integrieren — der Link hätte gesetzt werden MÜSSEN:
```yaml
task_uses_prompts: ["skills-skill-architecture"]
```

Ohne diesen Link ist das Audit-Graph unterbrochen und CLI-Tooling kann die Verbindung nicht traversieren.

---

### NIEDRIG — Befund 6: Frontmatter-Validator nicht erwähnt

**Verstoß gegen:** `PRE_COMMIT.md §7`.

PRE_COMMIT.md §7 schreibt vor: *"the agent MUST run `tools/validate-frontmatter.py` against the staged files."* Es gibt keinen Hinweis im PR oder im Run-Log, dass dieser Schritt ausgeführt wurde. Die neuen Task-Dateien könnten Validierungsfehler enthalten (z.B. durch leere `task_uses_prompts`-Listen statt `[]`-Syntax).

---

## Positive Aspekte

| Aspekt | Bewertung |
|---|---|
| Fallback-Mechanismus für fehlenden Baseline-Commit | Korrekt angewendet (Reflection gate R1) |
| T3-Tasks 003 und 004 erstellt | Korrekt — echte Governance-Lücken identifiziert |
| Frustration Log FL1 in PR-Body | Vorhanden und konkret |
| `t4_skipped` für completed Research korrekt | 151 complete workspaces korrekt übersprungen |
| Run-Log-Format eingehalten | Strukturell korrekt (außer leerem `end_commit`) |

---

## Zusammenfassende Empfehlung

```
BLOCK — Nicht mergen ohne:
  1. Revert der PRE_COMMIT.md-Änderung (oder explizite menschliche Freigabe als Ausnahme)
  2. end_commit: c4d1358 im Run-Log nachtragen
  3. readme.md-Stubs für tasks/003 und tasks/004

SHOULD — Verbesserungen für Follow-up:
  4. Deferral-Task für 148 übersprungene Issues
  5. task_uses_prompts: ["skills-skill-architecture"] in Task 003
  6. Frontmatter-Validator in Commit-Workflow integrieren
```

---

## Frustration Log

**FL1** — Die Coherence-Routine läuft in einen strukturellen Widerspruch: Bei großen Deltas (474 Dateien) ist die "keine T3-Direktänderungen, aber schreibe Tasks für alles"-Anforderung nicht skalierbar. Die Routine benötigt einen expliziten "Batch-Deferral"-Mechanismus im Prompt für Szenarien mit >50 skippable Files. Dieser fehlt aktuell.
