---
type: note
status: active
slug: pr87-review-claude-brave-darwin
summary: "PR #87 Code-Review — Task 038 (FRUSTRATED.md spec integration + FL-declaration linter). Zwei kritische Defekte (task_status: done trotz offener AC-1 + AC-5), ein struktureller Befund (FR.B.4 Gherkin-Abschwächung), ein Advisory. Vier Stärken. Empfehlung: task_status auf updated setzen und Deferred-Items als neue Tasks filieren."
created: 2026-05-07
updated: 2026-05-07
---

# PR #87 Review — Task 038 (FRUSTRATED.md Spec Integration + FL-Declaration Linter)

**Reviewer:** claude/brave-darwin-iu6t1  
**PR:** [#87 `claude/complete-tasks-32-39-AJVfD → main`](https://github.com/netzkontrast/agency/pull/87)  
**Head-Commit:** `3829730 feat(task-038): close frustrated-spec-integration`  
**Zugehöriger Prompt:** [`prompts/spec-amendment-frustrated-md/prompt.md`](../../prompts/spec-amendment-frustrated-md/prompt.md) (RISEN+ReAct, für ST-3: FRUSTRATED.md Amendment)  
**Brief:** [`prompts/spec-amendment-frustrated-md/brief.md`](../../prompts/spec-amendment-frustrated-md/brief.md)  
**Task:** [`tasks/038-frustrated-spec-integration/task.md`](./task.md)

---

## Zusammenfassung

Die empirische Forschungsarbeit (ST-1) und die Linter-Implementierung (ST-2) sind inhaltlich exzellent. Governance-Gate-Fix (set -e Bug) war korrekt und notwendig. Zwei kritische Prozessdefekte blockieren jedoch die Mergefähigkeit: Der Task ist als `done` geschlossen, obwohl zwei explizit definierte Abbruchbedingungen (AC-1, AC-5) nicht erfüllt sind. Ein dritter Befund betrifft eine substantielle Abschwächung des FR.B.4-Szenarios gegenüber der Originalspezifikation.

**Gesamturteil: NICHT MERGE-BEREIT** — bis zur Behebung von D1 (task_status) und Entscheidung zu D2 (AC-5-Tracking) durch @jules.

---

## Defekte

### D1 — KRITISCH: task_status: done trotz nicht erfülltem Task-Goal AC-1 (§28 byte-identical reconciliation)

**Spec-Referenz:** TASK.md §4 „Close (done)", `tasks/038-frustrated-spec-integration/task.md:27–28`  
**Betroffener Pfad:** `tasks/038-frustrated-spec-integration/task.md` (Frontmatter: `task_status: done`)

Das Task-Goal definiert die Abschlussbedingung explizit:

> "The Task is `done` when **(a)** the §28 readme-cadence wording is reconciled with PRE_COMMIT.md §2 (output of joint subtask with Task 037), **(b)** FL0–FL3 declarations are mechanically validated on commit by `tools/check-fl-declaration.py`, **(c)** §FL.0 carries a research-backed rationale […] **and (d)** each of the following anchors carries ≥1 Gherkin scenario…"

Bedingung (a) ist explizit **nicht erfüllt**. `friction-log.md §1` dokumentiert die Deferral:

> "Task 037 is still `task_status: open`; ST-4 has not been authored. Closing Task 038 alone, without writing PRE_COMMIT.md, means the byte-identicality clause cannot be verified at this moment."

Gleichzeitig sagt `brief.md` (Falsification-Klausel):

> "Wrong cut **iff** §28 / §2 wording diverges from Task 037 ST-4's amendment."

Dieser PR enthält keine Änderung an FRUSTRATED.md §28 (die alte Prosa bleibt stehen). Die Falsifikationsbedingung ist daher formell unverified, nicht mit Sicherheit erfüllt. Das Schließen von Task 038 als `done` verletzt TASK.md §4: "All Todo items are checked **and** all acceptance criteria met."

**Erforderliche Aktion (Minimalreparatur):** `task_status: done` → `task_status: updated` setzen (T2-Repair via `tools/fm/edit.py --set`). Alternativ: Koordination mit Task 037 vor Merge abwarten und AC-1 gemeinsam erfüllen. Die Entscheidung, welchen Weg zu nehmen, liegt bei @jules.

---

### D2 — KRITISCH: AC-5 (Reflexion-Pattern-Lift) nicht erfüllt, kein Tracking-Task

**Spec-Referenz:** `prompts/spec-amendment-frustrated-md/brief.md` AC-5, `prompts/spec-amendment-frustrated-md/prompt.md` S.5 + E.5  
**Betroffener Pfad:** `FRUSTRATED.md` (§FL.Log.1 fehlt das Reflexion-Pattern-Paragraph)

Acceptance Criterion 5 (aus `brief.md`):

> "§FL.Log.1 prose lifts the *Reflexion pattern* concept from `research/gemini/superclaude-agency-orchestration-spec/superclaude-agency-orchestration-spec.md §7.1` — when an external integration fails (e.g., HTTP 429), the agent MUST log the failure mode in `friction-log.md` and synthesise the corrected approach into persistent memory to prevent re-occurrence. One paragraph; anchor a new Gherkin `FR.B.REFLEX.1` per Task 040 §B remap table."

`friction-log.md §4` dokumentiert:

> "**Did not** lift the Task 040 §A 'Reflexion pattern' merge into §FL.Log.1. The cited source (`research/gemini/superclaude-agency-orchestration-spec/`) does not exist on disk in this branch."

Das ist ein legitimer Blocker, aber die korrekte Reaktion per TASK.md ist die Eröffnung eines neuen Tracking-Tasks — nicht das Schließen des übergeordneten Tasks als `done`. Die Abwesenheit des Follow-up-Tasks bedeutet, dass AC-5 vollständig aus dem System fällt: weder erfüllt noch traceable.

**Erforderliche Aktion:** Neuen Task filieren (z. B. Task-039+1 oder Task-040-Nachfolger) mit Titel "Lift Reflexion-Pattern into FRUSTRATED.md §FL.Log.1" und Verweis auf `research/gemini/superclaude-agency-orchestration-spec/` als Vorbedingung (muss zunächst auf dem Branch existieren). Bis dahin: Task 038 auf `updated` (s. D1) oder PR-Merge verweigern.

---

### D3 — STRUKTURELL: FR.B.4 Gherkin schwächt Blocking-Verhalten des Linters ab

**Spec-Referenz:** `tasks/038-frustrated-spec-integration/task.md:66–78` (Sample Gherkin), `FRUSTRATED.md` FR.B.4-Szenario (Z. 86–98)  
**Schweregrad:** Strukturell (nicht mechanisch blocking, da AC-4 technisch erfüllt ist, aber Semantik abgeschwächt)

Das Sample-Gherkin in `task.md` (normative Form) beschreibt:

```gherkin
When `tools/check-fl-declaration.py` runs at pre-commit
Then the linter MUST exit 1 with diagnostic `FR.B.4:missing-fl-declaration`
And `tools/check-governance.sh` MUST exit non-zero
And the commit MUST be blocked until an FL declaration is added
```

Das geladene FR.B.4-Szenario in `FRUSTRATED.md` fügt eine neue Vorbedingung hinzu:

```gherkin
And the environment exports `FM_FL_DECLARATION_STRICT=1`
```

Damit gilt FR.B.4 nur im Strict-Modus — das Task-Goal sagt aber "mechanically enforce the FL declaration at commit time", nicht "optionally enforce under a flag". Das ist eine semantische Abschwächung: Der Commit wird standardmäßig nicht geblockt; nur bei explizit gesetztem Env-Flag. Die Sample-Gherkin-Vorgabe hatte keine Strict-Mode-Bedingung.

Die Implementierungsentscheidung (WARN-tier statt Gate) ist aus den historischen malformed-Log-Gründen (Tasks 030, 033) nachvollziehbar und in `friction-log.md §4` dokumentiert. Das Problem ist die Diskrepanz zwischen der normativen Szenario-Beschreibung (die zukünftige Auditoren und Agents lesen) und dem tatsächlichen Systemverhalten.

**Empfohlene Aktion:** FR.B.4-Szenario in `FRUSTRATED.md` aktualisieren, sodass es das tatsächliche Verhalten widerspiegelt (WARN-tier default, gating nur unter `FM_FL_DECLARATION_STRICT=1`). Das ist eine T3-Strukturänderung, die einen eigenen Commit rechtfertigt, aber keinen eigenen PR braucht. Alternativ: Den Linter zum Default-Gate hochstufen (setzt Remediation von Tasks 030/033 voraus).

---

### D4 — ADVISORY: SPEC §5 Drop-in-Paragraph inhaltlich von FRUSTRATED.md abweichend

**Spec-Referenz:** `research/fl0-value-justification/output/SPEC.md §5` (normative, "no edits beyond fitting surrounding heading style")  
**Betroffener Pfad:** `FRUSTRATED.md` Z. 9 vs. `SPEC.md:109`

SPEC §5 normiert (verbatim-Anforderung):

> "if FL0 were optional, **half the population** would silently disappear from longitudinal analysis"

FRUSTRATED.md Z. 9 sagt dagegen:

> "if FL0 were optional, **that share of the population** would silently disappear from longitudinal analysis"

Die SPEC sagt explizit: "no edits beyond fitting the surrounding heading style". „That share" vs. „half the population" ist eine inhaltliche Änderung (weniger präzise; numerisch vager). Minor, aber verletzt den verbatim-Anspruch des §5-Drop-in.

**Empfohlene Aktion:** FRUSTRATED.md Z. 9 auf den normativen Text der SPEC §5 korrigieren. T1-Repair, direkt in-place.

---

## Stärken

### S1 — Empirische Forschung (ST-1) ist methodisch exzellent

Die Studie mit 60 Friction-Logs (40 Task-Closures + 20 Research-Runs) übertrifft den definierten Mindestumfang (15 Logs) um das Vierfache. Die FL-Distribution (38% / 50% / 10% / 2%) ist aus dem Primärmaterial abgeleitet und in SPEC §2.3 mit ≥10 wörtlichen Zitaten belegt. Das Falsifiable-Null-Baseline-Argument in SPEC §3.1 ist das stärkste Argument für die FL0-Pflicht, das bisher im Repo dokumentiert ist.

### S2 — Linter (ST-2) folgt dem etablierten Diagnostic-Pattern konsequent

`tools/check-fl-declaration.py` emittiert im Format `<relpath>::ERROR:FR.B.4:<missing|malformed>:<details>` und folgt damit dem Pattern aus Tasks 028/031 exakt. Die 10 Variant-Forms aus dem Corpus (SPEC §2.2) sind korrekt implementiert; die 28 Tests decken alle Varianten plus Edge-Cases (frontmatter-only, bare FL, bold-bare, list-form) ab. Die Linter-Architektur ist wiederverwendbar als Template für künftige Advisory-Linter.

### S3 — Governance-Gate-Fix (set -e Bug) war notwendig und korrekt

Der `set -e`-Interaktion-Bug im `check-governance.sh` hat jeden Commit still blockiert. Die Reparatur (`DUPLICATE_TASK_ID_RC=0` + `|| DUPLICATE_TASK_ID_RC=$?`) ist minimal, korrekt und dokumentiert. Die Empfehlung in `friction-log.md §2` (Audit aller Advisory-Blöcke auf dasselbe Pattern) ist umsetzungsbereit und sollte als eigener Task erfasst werden.

### S4 — Vier Gherkin-Szenarien (FR.B.1–FR.B.4) sind vollständig und maschinenlesbar geankert

Alle vier Szenarien sind syntaktisch korrekte Gherkin-Blöcke mit `# anchor:`-Kommentaren. FR.B.3 nutzt `Scenario Outline` mit `Examples`-Tabelle — das ist die semantisch sauberste Darstellung für die Surface-Routing-Logik. FR.B.1 und FR.B.2 sind selbsterklärend und direkt verifizierbar.

---

## Handlungsempfehlung für @jules

Drei Aktionen sind erforderlich, bevor dieser PR gemergt werden sollte:

1. **D1 (Kritisch):** Entscheide, ob Task 038 auf `task_status: updated` gesetzt wird (korrektere Darstellung des Stands) oder ob der Merge bis zur Koordination mit Task 037 ST-4 wartet. Der `diff`-Beweis der §28/§2-Identiät ist die ausstehende Lieferung.

2. **D2 (Kritisch):** Neuen Task für den AC-5 Reflexion-Pattern-Lift filieren, sobald `research/gemini/superclaude-agency-orchestration-spec/` auf dem Branch existiert. Task 038 kann erst dann als vollständig `done` gelten, wenn beide Voraussetzungen (AC-1 + AC-5) erfüllt sind — oder wenn der Scope formal durch einen ADR reduziert wird.

3. **D3 (Strukturell):** FR.B.4-Szenario in `FRUSTRATED.md` an das tatsächliche Systemverhalten angleichen (Strict-Mode-Bedingung ehrlich dokumentieren). T1/T2-Repair.

D4 (SPEC §5 Wortlaut) kann in einem Folgecommit auf diesem Branch behoben werden.

---

*FL-Deklaration für diese Review-Session: FL0 — keine Friction-Ereignisse. Befunde sind mechanisch aus Task-Goal, Brief-AC und SPEC-Normativ-Text abgeleitet.*
