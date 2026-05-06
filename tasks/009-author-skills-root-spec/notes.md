---
type: note
status: active
slug: claude-review-pr73
summary: "Claude Code review of PR #73 — SKILLS.md root spec (fixed, replaces PR #60). Identifiziert 2 kritische und 3 signifikante Spec-Verstöße trotz der 5 adressierten Blocker aus dem Vorläufer-Review."
created: 2026-05-06
updated: 2026-05-06
---

# Claude Code Review — PR #73: Author SKILLS.md Root Spec (fixed — replaces PR #60)

**Reviewed branch:** `claude/fix-broken-pr-W02JG` → `main`  
**PR:** [#73](https://github.com/netzkontrast/agency/pull/73)  
**Reviewer:** Claude Code (`claude/brave-darwin-e1KCR`)  
**Datum:** 2026-05-06  
**Ausgangspunkt:** PR #73 replaces PR #60. Die 5 Blocker des Vorläufer-Reviews (C1–C2, S1–S3) wurden mit Commit `92562a5` adressiert. Dieser Review bewertet den aktuellen Stand des Branches.

---

## Scope

PR #73 enthält zwei Commits:

| Commit | Autor | Inhalt |
|---|---|---|
| `0d4a00e` | Jules (`google-labs-jules[bot]`) | SKILLS.md, templates/skill.md, AGENTS.md, FOLDERS.md, PROMPT.md, RESEARCH.md, skills/readme.md, task.md (done), friction-log.md |
| `92562a5` | Claude Code (PR#60 fix) | Alle 5 Blocker-Fixes: tasks/readme.md Index-Update (C1), type: spec in template (C2), Gherkin §7.1 B.2–B.5 (S1), Gherkin §4.1 LC.1.1/LC.2.1 (S2), L1-Feldtabelle §3.2 (S3) |

---

## Ergebnis-Übersicht

| ID | Schwere | Sektion | Beschreibung | Fix nötig vor Merge? |
|---|---|---|---|---|
| C1 | 🔴 Kritisch | §6.1 | Gherkin fehlt für Klauseln X.2 und X.3 | Ja |
| C2 | 🔴 Kritisch | §4.1 LC.2.1 | „no agent MUST invoke" = normative Inversion | Ja |
| S1 | 🟡 Signifikant | §4 | Kein State-Machine-Diagramm für `status`-Übergänge | Empfohlen |
| S2 | 🟡 Signifikant | §7 | Bootstrap-Sektion zitiert Research, verlinkt aber nicht `sync.sh` | Empfohlen |
| S3 | 🟡 Signifikant | §3.1 | Stub-Abschnitt — verletzt Self-Containedness-Constraint | Empfohlen |
| M1 | 🔵 Minor | §7 B.1 | `claude-ai` fehlt in der Bootstrap-Agenten-Liste | Optional |
| M2 | 🔵 Minor | friction-log.md | Fehlendes Newline am Dateiende | Optional |

---

## Kritische Findings

### C1 — §6 Gherkin-Abdeckung: X.2 und X.3 ohne Scenarios (MUST-Verletzung)

**Normative Grundlage:**
- Prompt-Spec §S Step 3: *"Each clause MUST be paired with a Gherkin scenario in the same section."*
- AGENTS.md §G6: *"Acceptance criteria in this repository MUST be written as Gherkin scenarios, not as bullet-list assertions."*

**Problem:**  
§6 (Skill-to-Skill Cross-References) definiert vier Klauseln: X.1, X.2, X.3, X.4.  
§6.1 enthält nur zwei Scenarios: `X.1.1` (deckt X.1 ab) und `X.4.1` (deckt X.4 ab).

**X.2** (*Jede Referenz MUSS zur Lint-Zeit auflösen — ein broken reference ist ein pre-commit failure*) hat kein Scenario.  
**X.3** (*Reciprocity wird vom Linter berechnet, nicht authored*) hat kein Scenario.

**Fix:**  
Zwei Scenarios zu §6.1 hinzufügen, z.B.:

```gherkin
  # anchor: X.2.1
  Scenario: Broken skill reference fails pre-commit
    Given a skill "the-agency-system-architect/SKILL.md" lists "nonexistent-skill" in "skill_references_skills"
    When the agent runs tools/lint-linkage.py
    Then the linter MUST exit with a non-zero code
    And the agent MUST NOT commit until the broken reference is removed or the referenced skill exists

  # anchor: X.3.1
  Scenario: Linter computes reciprocity without author involvement
    Given skill A lists skill B in "skill_references_skills"
    When the linter generates the skills manifest
    Then the manifest MUST include B's reverse-reference to A under a computed "skill_referenced_by" field
    And the author of skill A MUST NOT manually write "skill_referenced_by" in any SKILL.md frontmatter
```

---

### C2 — §4.1 LC.2.1: „no agent MUST invoke" ist eine normative Inversion (RFC-2119-Verstoß)

**Normative Grundlage:**
- AGENTS.md §Spec Language Reference R1: *"Every normative statement MUST use exactly one RFC 2119 keyword per sentence."*
- RFC 2119: MUST = absolute obligation. MUST NOT = absolute prohibition.

**Problem:**  
LC.2.1 `Then`-Klausel lautet:

```
Then no agent MUST invoke that skill for new work
```

Die Phrase „no agent MUST" ist grammatikalisch zweideutig:
- **Lesart 1 (wahrscheinliche Absicht):** Agenten dürfen diesen Skill nicht ausführen → sollte MUST NOT sein.
- **Lesart 2 (buchstäbliche RFC-2119-Lesart):** Kein Agent ist *verpflichtet*, diesen Skill aufzurufen → invocation ist OPTIONAL, nicht verboten.

Ein Agent, der die Spec buchstäblich liest, würde schlussfolgern: *Deprecated skills dürfen weiterhin genutzt werden, nur ist die Nutzung nicht mehr obligatorisch.* Das ist das genaue Gegenteil der beabsichtigten Semantik.

**Fix:**

```gherkin
  # anchor: LC.2.1
  Scenario: Maintainer deprecates an existing skill
    Given a skill is superseded or no longer safe to use
    When the maintainer sets `status: deprecated` in the skill's SKILL.md frontmatter
    Then agents MUST NOT invoke that skill for new work
    And the `updated` date MUST be set to the date of the deprecation commit
```

---

## Signifikante Findings

### S1 — §4 Workflow: Kein State-Machine-Diagramm für `status`-Übergänge

**Normative Grundlage:**
- Strukturparität mit TASK.md §4, die explizit definiert: `open → (blocked ↔) in_progress → (done | updated | abandoned)`.
- §3.2 listet 4 gültige `status`-Werte: `active`, `draft`, `deprecated`, `archived`.

**Problem:**  
§4 beschreibt 5 Workflow-Schritte in Prosa (1–5), aber definiert keine erlaubten Übergänge zwischen den Status-Werten. Die Gherkin-Scenarios decken nur `→ active` (LC.1.1) und `active → deprecated` (LC.2.1) ab. Offen:
- Wann wird ein Skill mit `status: draft` erstellt (statt direkt `active`)?
- Wie unterscheiden sich `deprecated` und `archived`?
- Ist `draft → deprecated` ein valider Pfad?

**Fix-Empfehlung:**  
Zu Beginn von §4 hinzufügen:

```
Die Lifecycle-Zustände sind: `draft` → `active` → `deprecated` → `archived`.
Ein Skill KANN direkt als `active` erstellt werden, wenn er unmittelbar einsatzbereit ist.
`draft` ist OPTIONAL für Specs, die noch reviewed werden müssen.
`deprecated` bedeutet: nicht mehr für neue Arbeit verwenden.
`archived` bedeutet: historischer Record, kein Agent öffnet den Body ohne expliziten Anlass.
```

---

### S2 — §7 Bootstrap Protocol verlinkt nicht auf die bestehende Implementierung (`sync.sh`)

**Normative Grundlage:**
- Prompt-Spec §I Input, Item 7: Der Executor MUSS `/skills/skills-skill-bootstrap/readme.md` und `sync.sh` lesen — diese sind die existierende Implementierung, die §7 ratifizieren soll.

**Problem:**  
§7 zitiert korrekt `research/skills-skill-architecture/output/SPEC.md (§2 R1, §8 R7)`, verlinkt aber weder die existierende Shell-Implementierung (`skills/skills-skill-bootstrap/sync.sh`) noch das Bootstrap-Skill-Readme. Ein Agent, der §7 als einzige Referenz liest und B.1 implementieren möchte, würde das bereits vorhandene Werkzeug ignorieren und von Grund auf neu schreiben.

**Fix-Empfehlung:**  
Einen Hinweis am Beginn von §7 ergänzen:

```markdown
Die kanonische Shell-Implementierung dieses Protokolls ist [`skills/skills-skill-bootstrap/sync.sh`](./skills/skills-skill-bootstrap/sync.sh). 
Neue Agenten SOLLEN diese Implementierung lesen, bevor sie eigene Bootstrap-Logik entwerfen.
```

---

### S3 — §3.1 Layer Overview ist ein Stub und verletzt den Self-Containedness-Constraint

**Normative Grundlage:**
- Prompt-Spec §Constraints #4: *"MUST keep SKILLS.md self-contained: every term, framework, or convention referenced MUST be either defined in §1 or linked to its canonical source."*

**Problem:**  
§3.1 besteht aus einer einzigen Zeile:

> The layer overview is canonically defined in [TASK.md §3](./TASK.md).

Verlinkung zur kanonischen Quelle erfüllt den Buchstaben der Constraint, aber nicht den Geist: Agenten, die SKILLS.md lesen (insbesondere beim ersten Einsatz in einem neuen Kontext), müssen TASK.md parallel öffnen, um L0/L1/L2/L3 zu verstehen — die Abstraktionsschicht, auf der §3.2 und §3.3 vollständig aufbauen. AGENTS.md §Frontmatter Ontology Summary enthält genau diese Tabelle. Eine minimal ausreichende Lösung ist, diese Tabelle direkt in §3.1 zu reproduzieren.

**Fix-Empfehlung:**  
§3.1 durch die Zusammenfassungstabelle aus AGENTS.md ersetzen:

```markdown
### 3.1 Layer Overview

| Layer | Scope | Mandate |
|---|---|---|
| **L0** — Obsidian Reserved | `tags`, `aliases`, `cssclasses` | Optional; preserved if present. |
| **L1** — Vault Core | `type`, `status`, `slug`, `summary`, `created`, `updated` | MUST be present on all operational files. |
| **L2** — Domain Namespace | `skill_*` keys | MUST be present inside `/skills/`. |
| **L3** — Agent-Only | Vector embeddings, graph scores | MUST NOT appear in YAML. Lives in `/.agent_cache/<file>.meta.json`. |

Vollständige Semantik: [TASK.md §3](./TASK.md).
```

---

## Minor Findings

### M1 — B.1 Bootstrap-Agenten-Liste inkonsistent mit `skill_target_agents`

B.1 listet: „Every agent (Claude Code, Jules, Gemini) MUST run the bootstrap."  
§3.3 `skill_target_agents` enthält als validen Member: `claude-ai` (die Web-Oberfläche).  
`claude-ai` fehlt in B.1. Da U3 in §10 das Host-Routing für claude.ai als offen markiert, sollte B.1 zumindest einen qualifizierenden Hinweis enthalten: „(claude.ai deferred to §10 U3)."

---

### M2 — `friction-log.md` fehlt ein Newline am Dateiende

`tasks/009-author-skills-root-spec/friction-log.md` endet ohne `\n`. Kann zu Lint-Warnungen führen. Trivial zu fixen: einfach eine Leerzeile anhängen.

---

## Fazit und Merge-Empfehlung

Die 5 Blocker aus dem PR-#60-Review wurden korrekt adressiert. Die grundlegende Struktur von SKILLS.md ist solide: 11 Sektionen vorhanden, RFC-2119 Deklaration korrekt, Bootstrap-Protokoll vollständig, Frontmatter-Namespace vollständig definiert, Pre-Commit-Tabelle vollständig.

**Vor einem Merge müssen C1 und C2 behoben werden.** Beide betreffen Gherkin-Korrektheit — C1 durch fehlende Scenarios (Prompt-MUST-Verletzung), C2 durch eine normative Inversion die fälschlicherweise deprecated-Skill-Invocations erlauben würde.

S1, S2 und S3 sind signifikant genug, um sie im gleichen Fix-Commit zu lösen, aber nicht merge-blockierend sofern nachgearbeitet wird (z.B. als eigene Task oder Folgecommit auf diesem Branch).

@jules — bitte C1 und C2 auf diesem Branch fixen, bevor der PR gemergt wird. S1–S3 können als Folgearbeit in einem neuen Commit auf `claude/fix-broken-pr-W02JG` erfolgen.
