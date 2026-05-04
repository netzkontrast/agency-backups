---
type: note
status: completed
slug: harden-coherence-baseline-protocol
summary: "Governance critique of PR #32 (docs(008): governance critique of PR #31 post-merge review) by claude-code session claude/stoic-mendel-Sk9lZ. Identifies two critical meta-violations, one governance gap, and one recurring process failure. Content quality of critique-pr31.md assessed as high."
created: 2026-05-04
updated: 2026-05-04
task_id: "008"
task_status: in_progress
task_owner: "claude-code/claude/stoic-mendel-Sk9lZ"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_affects_paths:
  - tasks/008-harden-coherence-baseline-protocol/critique-pr32.md
  - tasks/008-harden-coherence-baseline-protocol/readme.md
  - tasks/008-harden-coherence-baseline-protocol/task.md
---

# Critique — PR #32 (`docs(008): governance critique of PR #31 post-merge review`)

**Reviewer:** `claude-code` session `claude/stoic-mendel-Sk9lZ`  
**Date:** 2026-05-04  
**PR reviewed:** #32 — `claude/stoic-mendel-iCz32` → `main` (merged, SHA `7fa3dc4`)  
**Governing specs:** `AGENTS.md`, `TASK.md §3.3`, `TASK.md §6`, `PROMPT.md §1`, `FOLDERS.md §3`  

---

## 0. Vorbemerkung — Fehlender ursprünglicher Prompt

Bevor die eigentliche Analyse beginnt, ist ein grundlegendes Governance-Problem festzuhalten:

`task.md` weist `task_uses_prompts: []` aus. Es existiert **kein verlinkter Prompt** in `/prompts/` für die Session `claude/stoic-mendel-iCz32`, die PR #32 erzeugte. Laut `PROMPT.md §1` sind Prompts "the single source of truth for 'what the agent is told to do'." Die Instruktionsmenge für PR #32 ist **nicht aus dem Repository rekonstruierbar** — sie lebte ausschließlich in der rohen Nutzernachricht der Session.

Dies ist die Ausgangsbedingung dieser Kritik: Eine Konformitätsanalyse, deren eigene Instruktionsbasis nicht im Repository verankert ist.

---

## 1. Verdict

`critique-pr31.md` ist analytisch präzise und inhaltlich stark. Die vier identifizierten Governance-Verletzungen (V1–V4) sind korrekt klassifiziert und die Empfehlungen sind handlungsfähig. Dennoch perpetuiert PR #32 **zwei der vier Verletzungen**, die es in PR #31 kritisiert — ein strukturelles Paradox, das die Autorität des Dokuments untergräbt. Hinzu kommt ein systemischer Prozessfehler, der in beiden PRs identisch auftritt.

Die Kernaussage: **Das Kritik-Framework funktioniert; der Enforcement-Mechanismus nicht.** Solange der Pre-Commit-Hook nicht installiert ist, werden strukturelle Verletzungen unabhängig von der Qualität der Kritikdokumentation `main` erreichen.

---

## 2. Kritische Meta-Verletzungen

### MV1 — `critique-pr31.md` Trägt Kein L2 Task-Namespace (Kritisch)

**Betroffene Regel:** `TASK.md §3.3` — "mandatory in `/tasks/<NNN>-<slug>/`"

`critique-pr31.md`-Frontmatter:

```yaml
type: note
status: completed
slug: harden-coherence-baseline-protocol
summary: "..."
created: 2026-05-04
updated: 2026-05-04
```

Dies ist die **exakt identische Verletzung**, die `critique-pr31.md` §2 V1 als "Critical" klassifiziert und gegen `notes.md` erhebt. Zitat aus der Kritik:

> Every file inside an operational directory (`/tasks/`, `/prompts/`, `/research/`) MUST carry the L2 namespace appropriate to that directory.

`critique-pr31.md` ist selbst eine Datei in `/tasks/008-harden-coherence-baseline-protocol/` und trägt kein einziges `task_*`-Feld. `tools/validate-frontmatter.py` würde dieselbe Fehlermeldung produzieren wie für `notes.md`. Das Kritikdokument begeht die Verletzung, die es als "trivially fixable" bezeichnet — und fixiert sie nicht für sich selbst.

**Schweregrad:** Kritisch (identisch mit V1 der Kritik selbst)  
**Fix:** L2-Pflichtfelder (`task_id`, `task_status`, `task_owner`, `task_priority`, `task_uses_prompts`, `task_spawns_research`, `task_affects_paths`) in `critique-pr31.md` nachtragen.

---

### MV2 — Task Nicht Beansprucht Vor dem Schreiben (Kritisch)

**Betroffene Regel:** `AGENTS.md Gherkin §AG.3.1 / TASK.md §6 Scenario: "Agent picks up an open Task"`

Nach dem Mergen von PR #32 zeigt `task.md`:

```yaml
task_status: open
task_owner: "unassigned"
```

Die Session `claude/stoic-mendel-iCz32` schrieb `critique-pr31.md` und aktualisierte `readme.md`, ohne Task 008 jemals zu beanspruchen. Dies ist die **exakt identische Verletzung**, die `critique-pr31.md` §2 V2 als "Critical" klassifiziert und gegen die Session von PR #31 erhebt. Zitat aus der Kritik:

> The session that created `notes.md` wrote extensively about Task 008 without ever claiming it.

Die Session, die `critique-pr31.md` erstellte, schrieb ebenfalls extensiv über Task 008 ohne es je zu beanspruchen. Das Kritikdokument benennt die normative Anforderung präzise ("This is not a SHOULD — it is a MUST") und verletzt sie im selben Zug.

**Schweregrad:** Kritisch (identisch mit V2 der Kritik selbst)  
**Fix:** `task.md` hätte im ersten Commit der Session auf `task_status: in_progress` und `task_owner: "claude-code/claude/stoic-mendel-iCz32"` gesetzt werden müssen — vor jedem anderen Write in den Task-Folder.

---

## 3. Governance-Lücke — Fehlende Prompt-Verankerung

**Betroffene Regel:** `PROMPT.md §1`, `AGENTS.md — Task Type Routing`

Die in PR #32 durchgeführte Arbeit ist eine Governance-Review: Execution-Arbeit, die einen definierten Instruktionssatz voraussetzt. Laut `AGENTS.md` — Task Type Routing-Tabelle gilt für "Authoring an executable instruction set": konsultiere `PROMPT.md`, ablegen in `/prompts/`. Per `PROMPT.md §4.2`: "Store Brief — Save the unedited user request and contextual metadata into `brief.md`. This is the immutable record of what was asked."

Für PR #32 existiert weder:
- Ein `/prompts/<slug>/prompt.md` mit dem Instruktionssatz für die Review-Aufgabe
- Ein `brief.md` mit der rohen Nutzeranfrage

Dies bedeutet: **Die Arbeitsbasis der Session ist nicht auditierbar.** Ein zukünftiger Agent, der Task 008 weiterführt, kann nicht feststellen, was die Review-Session beauftragt, eingeschränkt oder ausgeschlossen hatte. Das widerspricht direkt dem Prinzip "Prompts are the single source of truth."

**Schweregrad:** Mittel-Hoch (struktureller Audit-Gap)  
**Empfehlung:** Für Review-/Critique-Aufgaben SOLLTE ein Prompt in `/prompts/` angelegt werden, bevor die Session startet — auch wenn es sich um eine kurzläufige einmalige Aufgabe handelt. Alternativ: Der Prompt-Spec-Typ `general` (`prompt_kind: general`) ist genau für diesen Fall vorgesehen.

---

## 4. Systemischer Prozessfehler — 10-Sekunden-Merge-Fenster (Wiederholt)

**Betroffene Situation:** `AGENTS.md CR.1`, Prozess-Recommendation

PR #32 Zeitstempel:
- `created_at: 2026-05-04T15:31:36Z`
- `merged_at: 2026-05-04T15:31:46Z`
- **Merge-Fenster: 10 Sekunden**

`critique-pr31.md` §3 M3 identifiziert für PR #31 das identische 10-Sekunden-Merge-Fenster und kommentiert: "a process gap worth flagging." PR #32 wiederholt dieses Pattern in exakt derselben Ausprägung. Dies ist kein Einzelfall mehr — es ist ein **systemisches Pattern**.

Konsequenz: Ein Konformitätsdokument, das selbst nicht konform ist (MV1, MV2), hat keine Chance auf menschliche Prüfung vor dem Merge. Der einzige wirksame Schutz ist der Pre-Commit-Hook (Task 008 Plan Item 3) — nicht das soziale Protokoll eines Merge-Fensters.

**Empfehlung:** Branch-Protection-Regeln mit mindestens einem Required Review vor Merge auf `main` aktivieren — kombiniert mit dem Maintenance-Bypass-Modus für Pre-Commit-Checks. Ohne diese zwei Maßnahmen wird das Muster sich fortsetzen.

---

## 5. Positive Befunde

### 5.1 FL0 in PR-Body (CR.5-Konform)

PR #32 enthält am Ende der Beschreibung: `FL: FL0`. Dies erfüllt `AGENTS.md CR.5` korrekt — im Gegensatz zu PR #31, das `critique-pr31.md` §2 V4 als Non-Compliant markiert. Die kritisierende Session hat hier aus dem Vorgänger gelernt.

### 5.2 Standard-Commit-Typ (`docs(008)`)

PR #32 verwendet `docs(008):` — ein gültiger Conventional-Commits-Typ. Dies korrigiert die `review(008):`-Nomenklatur von PR #31, die `critique-pr31.md` §3 M2 als "non-standard" beanstandet. Konsistent mit dem kritisierten Befund.

### 5.3 Analytische Stärke von `critique-pr31.md`

Unabhängig von den Meta-Verletzungen: Die Analyse in `critique-pr31.md` ist methodisch solide. Abschnitt 4 (Content Assessment) ist fair und kontextualisiert; Abschnitt 5 (Spec Ambiguity) identifiziert eine echte Lücke im Typsystem (`type: review` / `type: analysis` fehlt im Ontologie-Vokabular). Die Zusammenfassungstabelle (Abschnitt 6) ist maschinell lesbar und klar priorisiert.

### 5.4 `readme.md` Aktualisierung

Das Update von `readme.md` zur Verlinkung von `critique-pr31.md` ist korrekt per `FOLDERS.md §3` durchgeführt worden.

---

## 6. Rekursives Muster — Strukturelle Diagnose

Die Sequenz PR #26 → PR #31 → PR #32 zeigt ein konsistentes Muster:

| PR | Produziert | Kritisiert | Eigene Verletzungen |
|----|-----------|-----------|---------------------|
| #26 (chore + task) | Task 007, Task 008 | — | L2-Gap in Notes (später gefunden) |
| #31 (notes.md) | Post-merge Review PR #26 | — | V1, V2, V3, V4 (laut PR #32) |
| #32 (critique-pr31.md) | Governance-Kritik PR #31 | V1–V4 in PR #31 | MV1, MV2 (L2 fehlt, Task unclaimed) |

**Diagnose:** Jede Session produziert qualitativ hochwertige Analyse der Vorgänger-Violations — und begeht dieselben strukturellen Violations. Der Grund ist trivial: **Der Pre-Commit-Hook ist nicht installiert** (Task 008 Background §3). Ohne mechanische Durchsetzung sind Konformitätsdokumente keine Konformitätsgarantie. Die Kritikschleife ist produktiv als Audit-Trail, aber wirkungslos als Enforcement-Mechanismus.

Die einzige wirksame Unterbrechung des Musters ist Task 008 Plan Item 3 (Pre-commit Bypass Policy + Hook Installation) — nicht mehr Critique-Iterationen.

---

## 7. Zusammenfassungstabelle

| ID | Schwere | Regel | Status |
|----|---------|-------|--------|
| MV1 | Kritisch | TASK.md §3.3 — L2 task namespace fehlt in critique-pr31.md | Offen |
| MV2 | Kritisch | TASK.md §6 / AGENTS.md — Task nicht beansprucht vor Write | Offen (task.md jetzt korrigiert durch diese Session) |
| G1 | Mittel-Hoch | PROMPT.md §1 — kein verlinkter Prompt für Review-Session | Strukturell offen |
| P1 | Mittel | Prozess — 10-Sek.-Merge-Fenster wiederholt (PR #31 + #32) | Systemisches Pattern |

---

## 8. Friction Level

FL0 — Keine Tooling-Reibung. Alle relevanten Informationen waren aus PR #32 Diff, den Task-Dateien und den Governance-Specs zugänglich. Die Task-Beanspruchung (MV2-Korrektur) wurde als erster Write dieser Session durchgeführt, bevor dieses Dokument erstellt wurde.
