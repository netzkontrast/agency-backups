---
type: note
status: active
slug: review-pr-90-task-064
summary: "PR #90 Review — coherence-check 2026-05-08 + Task 064 filing. Three findings: D1 (end_commit: PENDING nie finalisiert), D2 (zwei Commits statt atomarem Einzelcommit, Begründung zirkulär), D3 (F25-Disposition vorab festgelegt)."
created: 2026-05-08
updated: 2026-05-08
---

# PR #90 Review — Coherence Check 2026-05-08 + Task 064

Reviewer: claude-code (session `claude/brave-darwin-SBeMs`)
Reviewed: PR #90, commits `dd23029` + `d940c1b`
Branch: `claude/peaceful-carson-EL75t` → `main`
Prompt executed: [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md)

---

## Zusammenfassung

Der Run selbst ist sauber: Governance-Gate exitiert 0, alle sieben Findings F20–F26 sind klar formuliert, mit konkreten Diffs und Ziel-Pfaden versehen, und die Dedup-Prüfung gegen Tasks 025 und 044 ist dokumentiert. Die drei Befunde unten sind struktureller Natur — zwei davon haben unmittelbare Auswirkung auf den nächsten Coherence-Run.

**Status:** APPROVED with required follow-up — D1 MUST be resolved before the next coherence run executes.

---

## D1 — `end_commit: PENDING` wurde nie finalisiert (CRITICAL)

**Fundstelle:** `maintenance/run-log.md`, Zeile `end_commit: PENDING` im Eintrag `Run 2026-05-08`.

**Sachverhalt.** Das Prompt (Step 6) schreibt vor:

> The `end_commit` field MUST be the hash of the commit you are about to create (use `git rev-parse HEAD` after staging but before the final commit, or record it as the first hash of the next run's baseline if you cannot compute it pre-commit).

Commit `dd23029` trägt den Run-Log-Eintrag mit `end_commit: PENDING` ein. Commit `d940c1b` (`/sc:improve`-Refinements) enthält keine Aktualisierung des `end_commit`-Felds. Das PR wird mit `PENDING` gemergt.

**Folgewirkung.** Der awk-Fall-Forward (`git cat-file -e PENDING` → non-zero → nächste Zeile) überspringt diesen Eintrag. Der nächste Coherence-Run baut auf dem vorherigen gültigen `end_commit` auf (`0825eb8`, Task 032). Das bedeutet: alle 193 Dateien aus dem PR #89-Merge-Wave plus die fünf Dateien dieses PRs landen erneut im Delta — ein unnötig breiter Scan. Wenn mehrere aufeinanderfolgende Runs `PENDING` tragen, wächst der Delta-Bereich unbegrenzt.

**Erwartete Aktion.** Vor dem Merge MUSS `end_commit: PENDING` auf den tatsächlichen Commit-Hash (`dd23029`) gesetzt werden. Das ist eine T1-Reparatur (stale/falsche Metadaten), ausführbar via `tools/fm/edit.py`. Alternativ, falls `d940c1b` als kanonischer End-Commit gilt (da er die Post-Commit-Refinements enthält), MUSS `end_commit: d940c1b` gesetzt werden.

---

## D2 — Zwei Commits statt atomarem Einzelcommit, Begründung zirkulär (MODERATE)

**Fundstelle:** Commit-Graph `dd23029` → `d940c1b`; Commit-Message `d940c1b` zitiert „Task 044 F18 proposed carve-out".

**Sachverhalt.** Prompt Step 5 ist normativ:

> All T1 and T2 repairs, any new Tasks, and the run-log entry (Step 6) MUST be committed together in a single atomic commit.

Dieser PR enthält zwei Commits. Die Begründung in der Commit-Message von `d940c1b` lautet:

> committed separately per the Task 044 F18 proposed carve-out for operator-instructed follow-ups distinct from the coherence run's own atomic commit.

Task 044 F18 ist im Status `proposed` — das Finding steht in `task.md`, der zugehörige Diff gegen die Specs wurde noch nicht gemergt. Ein `proposed`-Finding ist kein geltender Spec-Text; es ist ein Vorschlag, der erst nach Plan-6 von Task 044 normative Kraft erhält. Die Abweichung von Step 5 wird also mit einem zirkulären Argument legitimiert: das Dokument, das die Abweichung erlaubt, existiert noch nicht in finaler Form.

**Konsequenz.** Die Abweichung ist in diesem Fall faktisch harmlos (die zweiten Commit-Inhalte sind additive Verfeinerungen ohne inhaltliche Konflikte). Das Muster ist jedoch ein Präzedenzfall: jeder Agent kann eine beliebige Spec-Abweichung mit einem `proposed`-Finding begründen, bevor dieses Finding überhaupt gelandet ist.

**Erwartete Aktion.** Task 044 F18 SOLLTE priorisiert landen, bevor das Muster in weiteren Sessions repliziert wird. Alternativ MUSS die Begründung in der Commit-Message explizit als „this deviation is accepted pending F18 landing; revert if F18 is rejected" markiert werden, damit der nächste Reviewer die Abhängigkeit erkennt.

---

## D3 — F25-Disposition in friction-log.md vorab festgelegt (MINOR)

**Fundstelle:** `tasks/064-improve-maintenance-spec-may-08-2026/friction-log.md`, Abschnitt `## Per-Finding Disposition (at file time)`:

> F25 (TodoWrite case sensitivity): expected `won't-fix` (out of repo governance scope).

**Sachverhalt.** Das Plan-7-Schritt ist: „Land F25 (won't-fix disposition or one-line CLAUDE.md note)." Die friction-log.md nimmt die Entscheidung vorweg, bevor Plan-7 ausgeführt wird. Das kollabiert das Zwei-Schritt-Muster „file finding → decide in Plan step" auf einen Schritt. Für einen externen Agenten, der Plan-7 durchführt, fehlt damit die explizite Entscheidungsanweisung im `task.md` selbst — er kann die Disposition nur aus dem friction-log ableiten, der eigentlich ein Protokoll-Artefakt ist, kein Planungs-Artefakt.

**Erwartete Aktion (optional).** Plan-7 im `task.md` SOLLTE um einen expliziten Entscheidungspfad ergänzt werden: „Default: won't-fix — verify by checking CLAUDE.md §13 / §14 for existing agent-tool notes; if none present, consider one-line addition." Die friction-log-Notation bleibt als Beobachtung stehen.

---

## Positive Befunde (kein Handlungsbedarf)

- **Linter-First-Triage korrekt angewendet.** 193 Dateien im Delta, 0 T1/T2-Findings — der Step-2.5-Pfad funktioniert wie spezifiziert.
- **Cross-Task-Dedup sauber dokumentiert.** Task 025 und Task 044 wurden gelesen; F20–F26 sind tatsächlich distinct von F2/F3/F4/F7 und F14–F19.
- **Skip-with-Citation korrekt angewendet.** Alle drei `issues_skipped` tragen Absorbing-Task-Zitierungen im `notes:`-Block.
- **Frontmatter vollständig.** L1+L2-Schlüssel in allen drei neuen Dateien; `tasks/readme.md` Index-Bullet für Task 064 korrekt gesetzt; `index_diff.py` exitiert 0.
- **F21 (Cadence Rule) ist meta-konsistent.** Der Text erkennt die Catch-22-Situation (drittes offenes Task in der Lineage) explizit an und adressiert sie als Finding, nicht als Fehler.

---

## Links

- PR: [#90](https://github.com/netzkontrast/agency/pull/90)
- Prompt: [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md)
- Run-Log-Eintrag: [`maintenance/run-log.md`](../../maintenance/run-log.md) — `Run 2026-05-08`
- Reviewed Task: [`tasks/064-improve-maintenance-spec-may-08-2026/task.md`](./task.md)
- Sibling reviews: [PR #89 review](../036-pr-review-task/), [PR #88 review](../035-pr-review-task/) (Muster-Referenz)
