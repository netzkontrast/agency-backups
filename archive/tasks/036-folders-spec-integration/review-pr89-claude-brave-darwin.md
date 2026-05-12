---
type: note
status: active
slug: pr89-review-claude-brave-darwin
summary: "PR #89 Code-Review — Task 036 (FOLDERS.md Spec Integration: 2 Linter + Spec-Amendment). Fünf Befunde identifiziert; fünf Stärken. Hauptbefund: Notice-Block am Anfang von FOLDERS.md wurde nicht aktualisiert — neue Linter fehlen dort. Gesamturteil: MERGE-BEREIT nach T1-Nachbesserung D1."
created: 2026-05-07
updated: 2026-05-07
---

# PR #89 Review — Task 036 (FOLDERS.md Spec Integration)

**Reviewer:** claude/brave-darwin-tBMfW  
**PR:** [#89 `claude/complete-tasks-32-39-7AZfU → main`](https://github.com/netzkontrast/agency/pull/89)  
**Head-Commit:** `98e6893 feat(task-036): close folders-spec-integration`  
**Zugehöriger Prompt:** [`prompts/spec-amendment-folders-md/prompt.md`](../../prompts/spec-amendment-folders-md/prompt.md) (RISEN+ReAct, ST-3: FOLDERS.md Amendment)  
**Brief:** [`prompts/spec-amendment-folders-md/brief.md`](../../prompts/spec-amendment-folders-md/brief.md)  
**Task:** [`tasks/036-folders-spec-integration/task.md`](./task.md)

---

## Zusammenfassung

Alle fünf Acceptance Criteria aus `brief.md` sind erfüllt: F.1.1-Exemption-Klausel, F.5-Promotion SHOULD→MUST, F.6-Dual-Surface-Guidance mit Linter-Referenz, fünf Gherkin-Szenarien F.B.1–F.B.5, Governance-Check exits 0. Die 20 neuen Tests bestehen vollständig. Die T1-Slug-Repair-Burst (18 task-folder readmes) ist korrekt als ungeplanter T1-Aufwand dokumentiert und sauber via `tools/fm/edit.py` ausgeführt. Das `FM_AUDIT_GRAPH_STRICT=1`-Muster folgt dem etablierten Präzedenzfall konsistent.

Ein struktureller T1-Defekt (D1) verdient Nachbesserung: Der Mechanical-Enforcement-Notice-Block am Anfang von `FOLDERS.md` (Z. 12) wurde nicht um die beiden neuen Linter erweitert — Agenten, die den Block als vollständige Enforcement-Übersicht lesen, erhalten ein unvollständiges Bild. Das ist eine T1-Reparatur im laufenden Branch, die den Merge nicht blockieren muss.

**Gesamturteil: MERGE-BEREIT nach T1-Nachbesserung D1** (empfohlen im Branch vor Merge; alternativ als sofortiger Follow-up-Commit nach Merge vertretbar).

---

## Defekte

### D1 — STRUKTURELL (T1): Notice-Block in `FOLDERS.md` nicht aktualisiert

**Spec-Referenz:** `FOLDERS.md` Z. 12; `MAINTENANCE.md §1` T1-Reparatur  
**Betroffener Pfad:** `FOLDERS.md`

Der Mechanical-Enforcement-Notice-Block am Anfang der Datei lautet aktuell:

```
The readme.md rule (§3) is enforced by `tools/lint-structure.py`;
the cross-directory linkage rule (§6) is enforced by `tools/lint-linkage.py`.
```

Nach Task 036 ist dies in zwei Punkten unvollständig:

1. **§5** (Frontmatter auf Folder-Indexes) wird jetzt ebenfalls mechanisch durchgesetzt — von `tools/check-readme-frontmatter.py` (ERROR-tier `[2b/6]`). Der Notice-Block erwähnt §5 nicht.
2. **§6** hat jetzt *zwei* Enforcement-Schichten: `tools/lint-linkage.py` (Frontmatter-Schlüssel-Auflösung, wie bisher) **und** `tools/check-audit-graph-consistency.py` (Body-Link-Drift-Erkennung, neu). Der Block nennt nur die erste.

Agenten, die den Notice-Block als Schnellreferenz für Enforcement-Coverage lesen (wie es die Spec-Konvention vorsieht), bekommen eine unvollständige Enforcement-Map geliefert. Das ist eine T1-Reparatur per MAINTENANCE.md §1 (mechanical repair, broken surface reference).

**Empfohlene Korrektur:**

```markdown
> **Mechanical Enforcement Notice:** This spec is mechanically enforced by
> `tools/check-governance.sh`. Before editing any folder under `/tasks/`,
> `/prompts/`, or `/research/`, install the pre-commit hook once with
> `tools/install-hooks.sh`. The readme.md presence rule (§3) is enforced by
> [`tools/lint-structure.py`](./tools/lint-structure.py); the readme.md
> frontmatter rule (§5) is enforced by
> [`tools/check-readme-frontmatter.py`](./tools/check-readme-frontmatter.py)
> (ERROR-tier); the cross-directory frontmatter linkage rule (§6) is enforced
> by [`tools/lint-linkage.py`](./tools/lint-linkage.py); the body-link /
> frontmatter dual-surface drift rule (§6) is detected (WARN-tier) by
> [`tools/check-audit-graph-consistency.py`](./tools/check-audit-graph-consistency.py).
```

---

### D2 — ADVISORY: Sektionsüberschrift weicht von Brief-AC-Formulierung ab

**Spec-Referenz:** `prompts/spec-amendment-folders-md/brief.md` AC4; `FOLDERS.md §6.1`  
**Betroffener Pfad:** `FOLDERS.md`

Brief-AC4 verlangt explizit: `≥5 Gherkin scenarios anchored F.B.1-F.B.5 land in a new **"## Acceptance Criteria"** section.`

Die gelieferte Sektion heißt: `## 6.1 Acceptance Scenarios (Gherkin)`.

Die fünf F.B.n-Anker sind korrekt gesetzt; die Szenarien sind inhaltlich vollständig. Es handelt sich nur um eine Namens-Abweichung. Da der Sektionsname für Downstream-Tooling als stabiler Identifier dienen könnte (z. B. Gherkin-Parser), ist die Abweichung dokumentationswürdig, blockiert den Merge jedoch nicht.

---

### D3 — ADVISORY: `FM_AUDIT_GRAPH_STRICT` nicht in FOLDERS.md §6 dokumentiert

**Spec-Referenz:** `tools/check-governance.sh` Z. 144; `FOLDERS.md §6`  
**Betroffene Pfade:** `FOLDERS.md`, `tools/check-governance.sh`

Die Env-Variable `FM_AUDIT_GRAPH_STRICT=1` für das strikte Gating ist im Governance-Script inline kommentiert, erscheint aber nicht in FOLDERS.md §6, wo die Dual-Surface-Drift-Regel beschrieben ist. Andere Strict-Mode-Variablen (`FM_WORKSPACE_CLEANLINESS_STRICT`, `FM_DUPLICATE_TASK_ID_STRICT`) folgen diesem Muster — aber deren Spec-Heimdokumente (RESEARCH.md, TASK.md) könnten ebenfalls nachdokumentiert worden sein (nicht geprüft).

**Empfohlene Aktion:** In FOLDERS.md §6 einen einzigen Hinweissatz ergänzen:

```
Set `FM_AUDIT_GRAPH_STRICT=1` to promote the WARN-tier diagnostics to gating
(useful once the historical drift backlog is resolved by a triage Task).
```

---

### D4 — ADVISORY: Kein Follow-up-Task für den 343-WARN-Backlog angelegt

**Spec-Referenz:** `TASK.md §4` (discovered work-items MUST be captured as Tasks); Friction-Log `## Drift findings booked for follow-up`  
**Betroffener Pfad:** `tasks/readme.md`

Friction-Log und PR-Body nennen 343 historische F.6-Drift-Findings und verweisen auf einen zukünftigen "follow-up triage Task". Im `tasks/readme.md` ist kein entsprechender Task (z. B. `037-audit-graph-drift-triage`) registriert. Die Advisory-Linting-Architektur (`FM_AUDIT_GRAPH_STRICT=1` als Opt-in) macht den Backlog nicht dringend — aber TASK.md §4 verlangt, dass entdeckte Arbeitspakete als Tasks erfasst werden.

**Empfohlene Aktion:** Vor oder kurz nach dem Merge einen minimalen Task (P4, `task_status: open`) anlegen, der die Triage der 343 WARN-Findings als Scope definiert. Die aktuelle Lage ist transparent dokumentiert; das ist positiv — es fehlt nur das formale Tracking-Artefakt.

---

### D5 — ADVISORY: `_iter_sources`-Schleife in `check-audit-graph-consistency.py` hat redundante Semantik

**Spec-Referenz:** `tools/check-audit-graph-consistency.py` Z. 266–288  
**Betroffener Pfad:** `tools/check-audit-graph-consistency.py`

Die Funktion `_iter_sources(roots, repo_root)` iteriert `for root in roots`, aber der innere Glob-Aufruf ist `repo_root.glob(glob)` — er läuft also immer vom Repo-Root, nicht von `root`. Die Scoping-Filterung erfolgt nachträglich via `_is_under(path, r)`. Das Ergebnis ist korrekt, aber das `for root in roots`-Äußere ist architektonisch irreführend: es lässt vermuten, dass der Glob je Root eingeschränkt wird, was nicht der Fall ist. Bei N Roots wird der gleiche Glob N-mal ausgeführt; de-dupliziert durch das `seen`-Set. Kein falsches Verhalten, aber potentielle Verwirrung bei zukünftigen Erweiterungen.

---

## Stärken

### S1 — Alle fünf Acceptance Criteria aus `brief.md` mechanisch verifizierbar erfüllt

F.1.1-Klausel (Z. 44), F.5-MUST-Promotion (Z. 74), F.6-Dual-Surface-Guidance (Z. 108), F.B.1–F.B.5-Szenarien (§6.1), Governance-Check exits 0 — sämtliche ACs lassen sich deterministisch gegen den Diff verifizieren. Kein AC ist durch Prosa "erklärt", alle sind mechanisch nachweisbar.

### S2 — Substring-Match statt Exact-Match für Slug-Validierung: korrekte Abstraktion

Die initiale Exact-Match-Implementierung hätte die übliche `task-<NNN>-<slug>`-Qualifier-Konvention als Fehler behandelt. Der zweistufige Ansatz (Linter auf Substring-Containment relaxieren, dann die 18 echten Outlier reparieren) ist methodisch richtig und transparent dokumentiert. Das Ergebnis ist eine robustere Invariante: `slug ⊇ folder-bare-slug` statt `slug == folder-name`.

### S3 — Diagnostics-Format konsistent mit dem Corpus-Pattern

Beide Linter emittieren `<relpath>::{ERROR,WARN}:F.{5,6}.<CODE>:<message>`, identisch zu den Precedent-Linters aus Tasks 028/031/032/035. Die Exit-Code-Semantik (`0` clean, `1` ERROR, `2` WARN-advisory) ist klar und folgt dem `check-workspace-cleanliness.py`-Präzedenzfall.

### S4 — 20 Tests methodisch vollständig, inkl. Provider-Exemptions und Self-Reference-Edge-Case

Besonders `TestProviderExemption::test_non_provider_research_workspace_still_checked` und `TestSelfReference::test_link_to_own_subfolder_does_not_warn` decken nicht-triviale Grenzen ab. Der Self-Reference-Test verhindert, dass ein `task.md`, das auf sein eigenes Subtask-Verzeichnis verlinkt, als Audit-Graph-Drift-Finding gewertet wird.

### S5 — Friction-Log-Transparenz und korrekte T1-Reparatur-Klassifikation

Die 18-readme-Slug-Repair-Burst ist exakt als T1-Mechanical-Repair klassifiziert und via `tools/fm/edit.py --set` ausgeführt — kein `sed`/`awk`, keine manuellen Frontmatter-Edits. Friction-Log dokumentiert den Grund für FL1 (ungeplantem Detour) ehrlich, ohne die Ausführung zu übertreiben. Das ist die Referenzimplementierung des Frustrations-Log-Protokolls.

---

## Handlungsempfehlung für @jules

Zwei Aktionen empfohlen:

1. **D1 (Strukturell, T1):** Notice-Block in `FOLDERS.md` Z. 12 im laufenden Branch vor Merge ergänzen (Korrekturtext oben). Ist eine mechanical repair — dauert <5 Minuten; kein neuer Task nötig.

2. **D4 (Advisory):** Follow-up-Task für die 343-WARN-Backlog-Triage anlegen (minimal: `task_status: open`, P4, 2-Satz-Scope). Das Advisory-WARN-Tier hält den Block offen — aber TASK.md §4 verlangt formale Erfassung.

D2, D3, D5 sind niedrig-prioritär und können in einem Folge-Task (z. B. zusammen mit D4) adressiert werden.

---

*FL-Deklaration für diese Review-Session: FL0 — keine Friction-Ereignisse. Befunde mechanisch aus Task-Goal, Brief-AC, Linter-Code und FOLDERS.md-Diff abgeleitet.*
