---
type: note
status: active
slug: pr86-review-claude-brave-darwin
summary: "PR #86 Review — Task 053 (Core Architecture Review + Dispatch 054–061). Zwei strukturelle Defekte (review-report.md Layer-Verstoß, fehlendes triage.md) und ein Advisory-Befund (fehlender Prompt). Vier Stärken. Adressiert an @jules."
created: 2026-05-07
updated: 2026-05-07
---

# PR #86 Review — Task 053 + Dispatch Tasks 054–061 (Core Architecture Review)

**Reviewer:** claude/brave-darwin-Y0ubD  
**PR:** [#86 `claude/review-core-architecture-bMU9X → main`](https://github.com/netzkontrast/agency/pull/86)  
**Head Commit:** `d54be55 tasks: add ## Assumptions Log to Tasks 053–061 readmes`  
**Zugehöriger Prompt:** **FEHLT** — `task_uses_prompts: []`; kein Prompt in `/prompts/` verknüpft. (→ D3)

---

## Zusammenfassung

Die inhaltliche Qualität des `review-report.md` ist hoch: 10 Findings mit zeilenanker-genauen Zitaten, klare Gut/Schlecht/Besser-Struktur, realistische Priorisierung. Die acht Nachfolge-Tasks 054–061 sind frontmatter-korrekt, vollständig verlinkt und bilden eine klare Dispatch-Kette.

Zwei strukturelle Defekte behindern die Mergefähigkeit: Das zentrale Artefakt (`review-report.md`) verletzt die Machine/Actor/Space-Grenzregel (D1), und `triage.md` fehlt entgegen der eigenen Plan-Verpflichtung (D2). Ein dritter Befund (D3) ist Advisory.

**Gesamturteil: CHANGE REQUESTED** — D2 ist ein Blocker nach TASK.md §4; D1 erfordert eine begründete Disposition (triage oder ADR), bevor gemergt wird.

---

## Defekte

### D1 — STRUKTURELL: `review-report.md` verletzt die Machine/Actor/Space-Trennung

**Spec-Referenz:** FOLDERS.md §1, RESEARCH.md §1, README.md §1 (L11–21), AGENTS.md §Session Setup  
**Betroffene Pfade:**
- `tasks/053-core-architecture-review-followups/review-report.md` — **falsche Ebene**
- `/research/<slug>/` — **fehlt**
- `/prompts/<slug>/` — **fehlt**

Die Frontmatter-Beschreibung von `review-report.md` lautet:

> "Verbatim architectural review of Agency's Machine/Actor/Space substrate… Findings B.1-B.10 are dispatched by Task 053 task.md Plan step 2-3."

Das ist per Definition ein Research-Artefakt — es dokumentiert **was das Ausführen einer Analyse produziert hat** (Space). Per README.md §1 (L11–21), RESEARCH.md §1 und FOLDERS.md §1 gehört solches Material unter `/research/<slug>/output/`, nicht in einen Task-Ordner.

Gleichzeitig ist die **Actor-Ebene vollständig abwesend**: `task_uses_prompts: []` und kein Prompt-Eintrag in `/prompts/`. Die Analyse wurde ohne dokumentierte Instruktion durchgeführt — das "What is the agent told to do?"-Layer ist leer. Damit ist die Audit-Graph-Kette `Task → Prompt → Research` vollständig unterbrochen.

Die eigentliche Ironie: Der `review-report.md`-Bericht kritisiert in **B.2** (LOOP_LOG in AGENTS.md) genau dieses Anti-Pattern — Runtime-State in einem Governance-Dokument — und wiederholt es selbst, indem er ein Research-Artefakt direkt in den Task-Ordner schreibt. Das Review bricht die Grenzregel, die es zu verteidigen behauptet.

**Erforderliche Disposition:** Entweder (a) `review-report.md` in ein nachträgliches Research-Workspace (`/research/core-architecture-review-2026-05/`) verschieben und Task 053 mit `task_spawns_research: [core-architecture-review-2026-05]` verlinken, oder (b) per ADR (MADR 4.0.0) ratifizieren, dass "verbatim-intake"-Reviews ohne vorangehenden Prompt-Draft direkt in Task-Ordner dürfen. Option (b) erfordert einen ADR-Eintrag unter `/decisions/`, weil es eine Repo-Architektur-Konvention betrifft.

---

### D2 — KRITISCH: `triage.md` fehlt trotz Plan-Verpflichtung

**Spec-Referenz:** Task 053 `task.md` Plan step 2, Todo-Item 2; TASK.md §4 (Done-Criteria)  
**Betroffener Pfad:** `tasks/053-core-architecture-review-followups/triage.md` — **fehlt**

Task 053 Plan step 2 ist eindeutig:

> "For each 'What's Bad' item B.1–B.10 in the report, append a row to `triage.md` (created in step 4) citing the owning Task…"

Und Plan step 4:

> "Add `triage.md` recording the ten-row map above with one row per finding: `finding_id | owning_task | gap_residual | dispatch_decision | new_task_slot`."

Das korrespondierende Todo-Item im `task.md` ist **unabgehakt**:

```
- [ ] Author `triage.md` with one row per B.1–B.10 finding (Plan step 2).
```

Der Task-Folder enthält nach drei Commits ausschließlich `task.md`, `readme.md` und `review-report.md`. Kein `triage.md`.

Das PR-Body-Self-Review-Tableau weist diese Lücke **nicht aus**: Alle Checks sind ✅, obwohl das zentrale Dispatch-Dokument fehlt. Das Self-Review ist damit unvollständig.

Ein PR mit `task_status: open` kann mit offenen Todos geöffnet werden — das ist per TASK.md §4 erlaubt. Aber dann MUSS das Self-Review diese Lücken ehrlich deklarieren, statt alle Checks als bestanden zu markieren.

**Erforderliche Aktion:** `triage.md` mit der 10-Zeilen-Mapping-Tabelle (finding_id | owning_task | gap_residual | dispatch_decision | new_task_slot) erstellen **und** das Todo-Item abhaken, bevor gemergt wird.

---

### D3 — ADVISORY: Kein Prompt verlinkt — Actor-Layer fehlt strukturell

**Spec-Referenz:** PROMPT.md §1.4, AGENTS.md §Folder Management, FOLDERS.md §2  
**Betroffener Pfad:** `tasks/053-core-architecture-review-followups/task.md:12` — `task_uses_prompts: []`

Per PROMPT.md §1.4 und der Audit-Graph-Spezifikation in FOLDERS.md §2 soll ein Task, der auf einer Agent-Analyse beruht, einen zugehörigen Prompt unter `/prompts/<slug>/` tragen und diesen via `task_uses_prompts` verlinken. Für ein Review dieser Tiefe — 10 strukturierte Findings mit Zitaten — wäre das die kanonische Form.

Das ist kein harter Blocker (Task 053 ist eine Dispatch-Task, kein Research-Execution-Task), aber es macht den Auftrag unsichtbar. Ein späterer Agent, der nachvollziehen will, warum genau diese 10 Findings mit dieser Priorisierung erscheinen, findet keine Instruktion. Der Review-Bericht ist die einzige Evidenz — und er liegt, wie D1 zeigt, im falschen Layer.

**Empfohlene Aktion:** Retrospektiv einen Prompt-Stub unter `/prompts/core-architecture-review-2026-05/` anlegen (drei Dateien per PROMPT.md §2: `prompt.md`, `brief.md`, `readme.md`) und `task_uses_prompts` aktualisieren. Kein sofortiger Merge-Blocker.

---

## Stärken

### S1 — Selbst-erkannte WARN-Cluster vor PR-Öffnung behoben

Der `/sc:reflect`-Durchlauf hat 9× `WARN:ASSUMPTION.LOG.MISSING` aufgedeckt und in einem separaten Commit (`d54be55`) behoben, **bevor** der PR geöffnet wurde. Das ist exakt das vorgesehene Verhalten des Friction-Loops. FL0 ist verdient.

### S2 — Nachfolge-Tasks 054–061 sind frontmatter-korrekt und vollständig verlinkt

Alle acht Successor-Tasks erfüllen die TASK.md §5-Pflichtstruktur (Goal / Plan / Todo / Links), referenzieren Task 053 per Relativpfad in `## Links`, tragen `task_blocked_by: []` korrekt (keiner blockiert auf 053), und das `task_id`-Slot-Verfahren (§8.1, kein Pre-Allocation) wurde eingehalten.

### S3 — `review-report.md` ist inhaltlich gründlich und zitierbar

10 Findings mit zeilenanker-genauen Referenzen (z. B. `tools/fm/_core.py:145–149`, `AGENTS.md:340–385`). Strukturierung in G (Good) / B (Bad) / Would-Do-Differently mit einer abschließenden Mapping-Tabelle ist klar und reproduzierbar. Die Einschränkung "Zitate gelten für `main@dbd996f`" ist explizit dokumentiert.

### S4 — Wartungsbypass korrekt und begründet eingesetzt

Der bestehende `F.4.2 ERROR` aus Task 046 ist korrekt via Maintenance-Bypass abgedeckt. Keine neuen ungecoverten Fehler eingeführt. Die Bypass-Logik ist damit sauber.

---

## Handlungsempfehlung für @jules

**Vor dem Merge zwei Dinge erforderlich:**

1. **D2 (Blocker):** `triage.md` mit der 10-Zeilen-Tabelle erstellen; korrespondierendes Todo-Item `- [x]` abhaken.
2. **D1 (Disposition erforderlich):** Entscheiden, ob `review-report.md` in einen nachträglichen Research-Workspace verschoben wird, oder ob ein ADR ratifiziert, dass Verbatim-Intake-Reviews im Task-Ordner erlaubt sind. Eine unkommentierte Merge-Entscheidung ohne Disposition wäre ein precedent-setting Silenz.

**D3 (nicht-blockierend):** Prompt-Stub in `/prompts/core-architecture-review-2026-05/` für spätere Ausführbarkeit — kann in einem Follow-up Task adressiert werden.

---

*FL-Deklaration für diese Review-Session: FL0 — Befunde mechanisch aus Spec abgeleitet; keine Interpretationsspielräume. Alle Defekte sind über Spec-Klauseln verifizierbar.*
