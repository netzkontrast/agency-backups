---
type: note
status: active
slug: pr88-review-claude-brave-darwin
summary: "PR #88 Code-Review — Task 035 (RESEARCH.md Spec Integration: 3 Linter + Session-Continuity-Workspace + Spec-Amendment). Vier strukturelle/advisory Defekte identifiziert; fünf Stärken. Hauptbefund: synthesis/methodology.md als behavioral-Gate-Item ohne normativen RESEARCH.md-Rückhalt — kann im Strict-Modus konforme Workspaces blockieren. Gesamturteil: MERGE-BEREIT nach Entscheidung zu D1."
created: 2026-05-07
updated: 2026-05-07
---

# PR #88 Review — Task 035 (RESEARCH.md Spec Integration)

**Reviewer:** claude/brave-darwin-byPwb  
**PR:** [#88 `claude/complete-tasks-32-39-uSMVT → main`](https://github.com/netzkontrast/agency/pull/88)  
**Head-Commit:** `45c17fa feat(task-035): close research-spec-integration`  
**Zugehöriger Prompt:** [`prompts/spec-amendment-research-md/prompt.md`](../../prompts/spec-amendment-research-md/prompt.md) (RISEN+ReAct, ST-5: RESEARCH.md Amendment)  
**Brief:** [`prompts/spec-amendment-research-md/brief.md`](../../prompts/spec-amendment-research-md/brief.md)  
**Task:** [`tasks/035-research-spec-integration/task.md`](./task.md)

---

## Zusammenfassung

Die drei Linter (ST-2/ST-3/ST-4) sind methodisch präzise implementiert und schließen die in `task.md` beschriebenen Enforcement-Gaps mechanisch. Alle 24 neuen Tests bestehen. Das Session-Continuity-Research-Workspace (ST-1) liefert ein konkretes `state.md`-Format, das in RESEARCH.md §4.10 korrekt verankert ist. Die Spec-Amendment (ST-5) erfüllt alle sechs Acceptance Criteria aus `brief.md`.

Ein struktureller Defekt (D1) verdient Aufmerksamkeit vor dem Merge: Das Trust-Audit-Linter führt `synthesis/methodology.md` als behavioral-Gate-Item, obwohl RESEARCH.md §5 dieses File nicht normativ fordert. Die Threshold-Arithmetik (5 Items, 90%) bedeutet, dass ein fehlendes `methodology.md` allein die behavioral-Dimension scheitern lässt (4/5 = 80% < 90%). Solange das Linting advisory läuft, blockiert das nichts — aber sobald `FM_TRUST_AUDIT_STRICT=1` gesetzt wird, werden konforme Workspaces fälschlich geblockt.

**Gesamturteil: MERGE-BEREIT nach Entscheidung zu D1** — entweder `synthesis/methodology.md` normativ in RESEARCH.md §5 verankern (T3-Task), oder die Threshold-Grenze für 5 Items auf ≥80% senken, sodass eine fehlende Datei toleriert wird.

---

## Defekte

### D1 — STRUKTURELL: `synthesis/methodology.md` als behavioral-Gate-Item ohne RESEARCH.md-Normierung

**Spec-Referenz:** `tools/check-trust-audit.py:_score_behavioral()` Z. ~52; `RESEARCH.md §5` (Pre-Commit-Checkliste, jetzt §5.7); `RESEARCH.md §2` (Ordner-Baum)  
**Betroffener Pfad:** `tools/check-trust-audit.py`

Das Trust-Audit-Linter listet `synthesis/methodology.md` als viertes behavioral-Check-Item:

```python
("methodology-md", (workspace / "synthesis" / "methodology.md").exists()),
```

`RESEARCH.md §5.7` (neue Trust-Audit-GATE-Formulierung) delegiert an `check-trust-audit.py`, nennt aber die drei Threshold-Werte ohne die zugrundeliegenden Items zu normieren. `RESEARCH.md §5` (Pre-Commit-Checkliste Schritt 7) ersetzt die alte Synthesis-Verification-Liste durch die Trust-Audit-Formel, ohne `methodology.md` explizit als Pflichtdatei aufzuführen. Im gesamten RESEARCH.md erscheint `methodology.md` nur einmal: im informativen Ordner-Baum (§2, Z. 46).

**Threshold-Arithmetik:** 5 behavioral Items, Threshold 90% → Mindestpflicht 4,5/5 → aufgerundet: 5/5. Ein fehlendes `methodology.md` ergibt 4/5 = 80% < 90% → behavioral FAIL. Damit kann diese eine fehlende Datei die Dimension kippen, auch wenn alle anderen vier Items erfüllt sind.

**Auswirkung im Strict-Modus:** Workspaces, die konform zu RESEARCH.md sind (alle Pflichtdateien vorhanden, korrekt befüllt), können den Trust-Audit-GATE scheitern lassen, wenn sie kein `synthesis/methodology.md` führen. Das neue `research/session-continuity-protocol-instantiation`-Workspace hat das File — aber ältere konforme Workspaces möglicherweise nicht.

**Erforderliche Aktion (zwei Optionen):**

Option A (normativ): `synthesis/methodology.md` in RESEARCH.md §5 Schritt 7 als explizite Anforderung aufführen — "synthesis/methodology.md documents the critical-thinking methods applied (M06, M13, …)". Das ist eine T3-Strukturänderung; separater Task empfohlen.

Option B (threshold): Behavioral-Threshold von 90% auf 80% senken (toleriert genau 1 Miss von 5 Items). Die Entscheidung liegt bei @jules.

---

### D2 — ADVISORY: Provider-Liste in zwei Quellen hardcoded

**Spec-Referenz:** `tools/check-governance.sh` Z. ~208–210; `tools/check-trust-audit.py:_is_research_workspace()` Z. ~195  
**Betroffener Pfad:** `tools/check-governance.sh`, `tools/check-trust-audit.py`

Die Shell-Schleife im Governance-Script und die Python-Funktion `_is_research_workspace` enthalten dieselbe hardcodierte Provider-Liste:

```bash
# check-governance.sh
case "$base" in gemini|gpt|human|other) continue ;; esac
```

```python
# check-trust-audit.py
if parts[1] in {"gemini", "gpt", "human", "other"}:
```

Ein neuer Provider (z. B. `perplexity`, `openai`) müsste in beiden Stellen manuell eingetragen werden. RESEARCH.md §6 definiert keine kanonische Provider-Liste, von der beide Tools lesen könnten.

**Empfohlene Aktion:** Provider-Liste als Konstante in `check-trust-audit.py` exportieren (z. B. `EXTERNAL_PROVIDERS: frozenset[str]`) und in `check-governance.sh` via `python3 -c "from tools.check_trust_audit import EXTERNAL_PROVIDERS; print('|'.join(EXTERNAL_PROVIDERS))"` generieren — oder als statische Quelle in RESEARCH.md §6 normieren.

---

### D3 — ADVISORY: WARN-Tier in R.B.2-Gherkin permanent kodifiziert

**Spec-Referenz:** `RESEARCH.md §5.11` R.B.2-Szenario; `RESEARCH.md §4.4` ("MUST be deleted")  
**Betroffener Pfad:** `RESEARCH.md §5.11`

Das R.B.2-Szenario endet mit:

```gherkin
Then the linter MUST emit `<path>::WARN:R.4.4:execution-script-not-cleaned`
```

`check-external-result-downstream-task.py` (R.6.5, gleiches PR) emittiert dagegen `ERROR`-Tier für strukturell vergleichbare Verstöße (fehlender Task-Backlink). Die Tier-Inkonsistenz wird zum Problem, sobald MAINTENANCE.md-Aggregatoren (`DIAGNOSTIC_SCHEMA` aus `check-trust-audit.py`) Diagnostics nach Tier filtern: WARN würde dann unterhalb der Maintenance-Eskalationsschwelle bleiben, auch wenn `FM_WORKSPACE_CLEANLINESS_STRICT=1` gesetzt ist und der Commit tatsächlich geblockt wird.

**Empfohlene Aktion:** Nach Ende des Migration-Windows WARN → ERROR anheben und R.B.2-Szenario aktualisieren. Bis dahin: im Szenario explizit dokumentieren, dass WARN ein temporärer Migration-Window-Wert ist (`# migration-window: promote to ERROR after Task 039 backfill`).

---

### D4 — ADVISORY: R.B.5 Gherkin-Szenario beschreibt Trigger ungenau

**Spec-Referenz:** `RESEARCH.md §5.11` R.B.5-Szenario; `tools/check-governance.sh` Trust-Audit-Loop  
**Betroffener Pfad:** `RESEARCH.md §5.11`

Das R.B.5-Szenario:

```gherkin
When the agent stages a frontmatter edit setting `research_phase: complete`
```

Das tatsächliche mechanische Verhalten (`check-governance.sh`) ist breiter: die Trust-Audit-GATE läuft bei JEDEM Commit, wenn `research_phase: complete` bereits im `readme.md` steht — unabhängig davon, ob der Commit die Phase selbst setzt. Ein Agent, der eine bereits abgeschlossene Workspace-Datei korrigiert (z. B. einen Tippfehler in `output/SPEC.md`), wird den Trust-Audit-GATE triggern, auch ohne eine Phase-Transition.

Das ist kein Bug im Linter, aber das Gherkin-Szenario führt Agenten in die Irre: Sie erwarten den GATE nur bei Phase-Transitionen, nicht bei beliebigen Workspace-Berührungen.

**Empfohlene Aktion:** `When`-Klausel anpassen: `When any commit touches files under the workspace AND the workspace readme declares research_phase: complete`.

---

## Stärken

### S1 — Drei Linter methodisch präzise und diagnostic-pattern-konform

Alle drei Linter (`check-workspace-cleanliness.py`, `check-external-result-downstream-task.py`, `check-trust-audit.py`) folgen dem kanonischen `<relpath>::TIER:CODE:message`-Format aus Tasks 028/031. Die `DIAGNOSTIC_SCHEMA`-Exportkonstante in `check-trust-audit.py` ist ein durchdachtes Forward-Compatibility-Design für den Task 039-AGGREGATOR; die C3-Partition (GATE vs. AGGREGATOR) wird konsequent eingehalten.

### S2 — 24 neue Tests: vollständig und edge-case-bewusst

Alle 24 Tests bestehen. Die `.cleanignore`-Tests (Glob, Path-Prefix, Kommentarzeilen) sind besonders gründlich. `test_multi_workspace_partition_rejected` ist eine wichtige Boundary-Condition. Lediglich ein Test für `methodology-md`-Absenz fehlt (vgl. D1).

### S3 — R.4.3 Prompt-Snapshot-Disambiguierung präzise und vollständig

Die Lock-at-Start-Policy mit explizitem Mid-Run-Divergenz-Handling (archive + neuer Prompt statt weiter gegen stale Snapshot) schließt eine genuine Ambiguität, die in älteren Research-Runs implizit zu Inkonsistenzen führen konnte. Der Verweis auf `workspace/session.log` als Audit-Trail für Divergenzen ist traceability-gerecht.

### S4 — §4.10 Session-Continuity-Protokoll mit verifiziertem state.md-Format

Das konkrete `state.md`-Format (4 staleness probes, event-stream body, cadence-Regel an synthesis-step-Grenzen) ist direkt aus `research/adr-spec-research-synthesis/` empirisch validiert. Die `require_human_review()`-Fence (Spec-I.7.1) ist korrekt: kein automatisches Resume bei Probe-Mismatch. Token-Budget (600 tokens für state.md) liegt unter dem 10%-Budget des Parent-Prompts.

### S5 — Strict-Gate-Architektur folgt FM_DUPLICATE_TASK_ID_STRICT-Präzedenzfall konsistent

Die drei neuen Env-Variablen (`FM_WORKSPACE_CLEANLINESS_STRICT`, `FM_EXTERNAL_RESULT_STRICT`, `FM_TRUST_AUDIT_STRICT`) spiegeln das etablierte `FM_DUPLICATE_TASK_ID_STRICT`-Pattern exakt. Migration-Window-Kommentare in `check-governance.sh` sind klar und nennen die Voraussetzungen für Strict-Mode-Aktivierung.

---

## Handlungsempfehlung für @jules

Drei Aktionen vor dem Merge:

1. **D1 (Strukturell):** Entscheide zwischen Option A (RESEARCH.md normiert `synthesis/methodology.md`) und Option B (Threshold 90% → 80%). Option B ist schneller (1 Zeile in `check-trust-audit.py`); Option A ist spec-konformer. Ohne diese Entscheidung wird Strict-Mode-Aktivierung Regressions-Failures auf konformen Workspaces produzieren.

2. **D3+D4 (Advisory):** Erwäge, die zwei Gherkin-Szenarien (R.B.2 Migration-Window-Kommentar, R.B.5 korrekter Trigger) in einem Follow-up-Commit auf diesem Branch zu reparieren — beides sind T1/T2-Reparaturen, die den Merge nicht blockieren müssen, aber besser jetzt als nach dem Merge.

3. **D2 (Advisory):** Provider-Liste-DRY-Violation ist niedrig-prioritär und kann in einem Folge-Task (z. B. Task 039 Nachfolger) adressiert werden.

---

*FL-Deklaration für diese Review-Session: FL0 — keine Friction-Ereignisse. Befunde mechanisch aus Task-Goal, Brief-AC, Linter-Code und RESEARCH.md-Diff abgeleitet.*
