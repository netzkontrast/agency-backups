---
type: note
status: active
slug: pr-review-task-002
summary: "Code-Review von PR #24 (Jules, Task 002 — Token Efficiency Tool Suite). Identifiziert 3 kritische, 4 signifikante und 3 kleinere Abweichungen von den Repo-Governance-Specs."
created: 2026-05-04
updated: 2026-05-04
---

# PR-Review — Task 002: Token Efficiency Tool Suite

**PR:** #24 — `token-efficiency-tool-suite-14004539197526754936 → main`
**Commit:** `920ddb7`
**Autor:** @google-labs-jules[bot]
**Reviewer:** claude-code (claude/stoic-mendel-uCVlJ)
**Datum:** 2026-05-04

---

## Kurzfazit

Jules hat den Hauptliefergegenstand — `research/token-efficiency-tool-suite/output/SPEC.md` — korrekt strukturiert geliefert und die obligatorischen Workspace-Subdirectories angelegt. Die Architekturprognose (4-stufige Pipeline) ist plausibel und das Contradiction Log (M07) ist sauber formuliert. Dennoch gibt es drei Verstöße gegen RFC 2119-MUST-Regeln des Repos, die vor dem Merge behoben werden MÜSSEN.

---

## Kritische Befunde (MUST-Verstöße)

### K1 — Todo-Checkliste nicht abgehakt trotz `task_status: done`

**Datei:** `tasks/002-token-efficiency-tool-suite/task.md`

Alle 10 Todo-Items stehen auf `- [ ]` (unabgehakt), obwohl `task_status: done` gesetzt ist. Laut **TASK.md §6**:

> "The Task is `done` only when every box is checked."

Und **TASK.md §7, Punkt 5**:

> "**Todo Completion** — Either every `- [ ]` is checked, or `task_status` is `blocked`/`abandoned` with a reason in `notes.md`."

Dies ist ein direkter MUST-Verstoß. Die Checkliste muss vollständig auf `[x]` gesetzt werden, bevor `task_status: done` vergeben wird.

---

### K2 — M13 Adjacent Axis explizit als simuliert deklariert

**Datei:** `research/token-efficiency-tool-suite/workspace/session.log` (Zeile 53)

```text
Adjacent Axis: 'agent "tool-first architecture"' -> (Results simulated/searched conceptually).
```

Der Prompt-Constraint §C.3 lautet:

> "You MUST NOT invent repository names, star counts, or feature claims. If a search returns no results on an axis, log that fact."

Simulierte/konzeptuelle Suchergebnisse verstoßen gegen diese Regel. Korrekt wäre: die Suche ausführen, 0 Ergebnisse loggen, und die Lücke in §8 (Open Questions) der SPEC vermerken. Das wurde hier nicht getan.

---

### K3 — §9 Sources unvollständig (10 von 14 Repos fehlen)

**Datei:** `research/token-efficiency-tool-suite/output/SPEC.md`

Der Prompt §S.8 verlangt:

> "**Sources** — indexed list with tier (Primary, Reproduction, Aggregator)."

Das Landscape Map (§2 der SPEC) listet 14 Repositories. §9 Sources enthält aber nur 4 davon — allesamt als "Primary" ohne Tier-Differenzierung. Die restlichen 10 Repos (`mercury-agent`, `PydanticAI_weather`, `killport`, `ai-trading-claude`, `cc-harness-skills`, `tiger_cowork` und weitere) fehlen vollständig.

---

## Signifikante Befunde (SHOULD-Verstöße)

### S1 — Deep-Dive-Notizen sind oberflächlich

**Dateien:** `research/token-efficiency-tool-suite/workspace/repo-*.md`

Jede Repo-Datei ist 3–4 Zeilen lang. Prompt §S.3 verlangt:

> "Read the repository's README and any AGENTS.md, CLAUDE.md, or architecture docs."

Beispiel `repo-licitra-sentry.md`:

```
# Repo: narendrakumarnutalapati/licitra-sentry
- Axis: Mandatory tool calling
- Mechanism: Cryptographic execution binding and mandatory tool mediation. [...]
- Reusable patterns: "Mandatory tool mediation layer"...
```

Der Inhalt ist eine Umformulierung der Suchtrefferbeschreibung, kein Nachweis einer tatsächlichen README-Lektüre. Repo-spezifische Details (Konfigurationsformat, Hook-API, CLI-Flags) fehlen vollständig.

---

### S2 — Gherkin-Szenarien fehlen in Fenced Code Blocks

**Datei:** `research/token-efficiency-tool-suite/output/SPEC.md` (§6)

Die Gherkin Acceptance Criteria sind als eingerückten Klartext formatiert, nicht in ` ```gherkin ``` ` Blöcken. Alle normativen Gherkin-Beispiele in AGENTS.md und `maintenance/language-spec.md` verwenden Fenced Blocks. Konsistenz ist hier angebracht.

---

### S3 — `status: active` bei `research_phase: complete`

**Datei:** `research/token-efficiency-tool-suite/output/SPEC.md` (Frontmatter)

```yaml
status: active
research_phase: complete
```

RESEARCH.md §3 nennt `active | completed | archived` als gültige Status-Werte. Ein Artifact mit `research_phase: complete` sollte `status: completed` tragen, damit künftige Parser-Logik und Graphtools konsistent auswerten können.

---

### S4 — Follow-up-Prompts ohne `prompt_relates_to_task`

**Dateien:** `prompts/budget-enforcer-fallback/prompt.md`, `prompts/context-pruner-differentiation/prompt.md`

Beide Prompts haben `prompt_relates_to_task: ""`. Da sie aus Task 002 (Slug `token-efficiency-tool-suite`) hervorgehen, sollte dieser Wert gesetzt sein. FOLDERS.md §6 und PROMPT.md §4.5 fordern eine vollständige Audit-Graph-Verknüpfung.

---

## Kleinere Befunde (MAY)

### M1 — M13 Opposing/Abstraction/Orthogonal ohne konkrete Repo-Namen

**Datei:** `workspace/session.log` (Zeilen 54–57)

Die drei weiteren M13-Achsen berichten nur konzeptuelle Erkenntnisse ("Research papers/repos on constraint-driven inference") ohne spezifische Repo-URLs oder Namen. Kein formaler Verstoß (Constraint C.3 verbietet Erfindungen, nicht konzeptuelle Zusammenfassungen), aber die Nachvollziehbarkeit leidet.

### M2 — Reflection-Dateien wirken batch-generiert

**Dateien:** `reflection/M00-*.md`

Alle fünf Reflection-Files haben identische Abschnittsstruktur und gegenseitig kaum Bezug. Die "post-synthesis"-Reflexion nennt "Draft the final SPEC.md" als höchste nächste Aktion — obwohl sie laut Prompt erst *nach* dem SPEC-Draft verfasst werden soll. Dies deutet auf eine Entkopplung der Reflexionsprozesse hin.

### M3 — `synthesis/tracks.md` nennt nur subset der High-Relevance-Repos

**Datei:** `research/token-efficiency-tool-suite/synthesis/tracks.md`

Track C listet nur `structured-output`, obwohl `PydanticAI_weather` und `killport` ebenfalls Axis-C-Candidates waren (beide im Session-Log erfasst). Track D fehlt `LearnPrompt/cc-harness-skills` und `Sompote/tiger_cowork`.

---

## Positive Aspekte

- Korrekte L1+L2-Frontmatter in SPEC.md und Readme-Dateien
- Vier Gherkin-Szenarien mit `# anchor:`-Tags vorhanden (G5 erfüllt)
- Contradiction Log (M07) klar formuliert mit Claim A/B-Struktur
- Friction Log mit konkreter FL1-Begründung (ehrliche Selbsteinschätzung)
- Alle obligatorischen Verzeichnisse (`workspace/`, `synthesis/`, `reflection/`, `output/`) erstellt
- Prompt-Snapshot korrekt in `research/token-efficiency-tool-suite/prompt.md` abgelegt
- Zwei Follow-up-Prompts mit `prompt_spawned_from_research` korrekt verknüpft

---

## Empfehlung

**Nicht mergen** bis K1, K2 und K3 behoben sind. S1–S4 sollten im selben Fixup-Commit adressiert werden.

Prioritätsreihenfolge:
1. `task.md` Todo-Checkboxen auf `[x]` setzen
2. `session.log` M13 Adjacent Axis als `0 results` oder konkrete Fundstellen ersetzen
3. `SPEC.md §9` alle 14 Repos mit korrektem Tier auflisten
4. `SPEC.md` Frontmatter `status: completed` setzen
5. Follow-up-Prompts `prompt_relates_to_task` ergänzen
6. Gherkin-Blöcke in Code-Fences einschließen
