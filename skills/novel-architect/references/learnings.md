# Learnings — novel-architect Self-Improvement Log

> **Mandatorisch:** Bei jedem Session-Ende-Checkpoint wird hier mindestens ein
> Eintrag ergänzt — was hat suboptimal funktioniert, was ist die Korrektur.
> Anschließend Skill packen.

## Format

Jeder Eintrag hat: Datum, Trigger (was passierte), Lesson, Action (was wird
ab jetzt anders gemacht — entweder als SKILL.md-Edit, references-Edit oder als
Heuristik in einer phase-/method-Datei).

---

## Skill-übergreifende Patterns (generic, übernommen aus v0.3.3)

### 2026-05-03 — Drive-Doc-Ingest: PDF-Export statt read_file_content

**Trigger:** Bei „Drive-Files in markdown ingesten" griff der Skill reflexhaft
zu `Google Drive:read_file_content`, das den vollen Text als Tool-Response in
den Context lädt. Bei 14 Files à 30-200KB hätte das den Context massiv
aufgebläht.

**Lesson:** Für Google Docs in Drive ist der korrekte token-sparende Pfad:
`download_file_content` mit `exportMimeType: 'application/pdf'` → bytes nach
`/tmp/<slug>.pdf` schreiben → `pdf-to-markdown` skill läuft → `.md` landet in
`ingest/`, ohne dass je der volle Text durch den Context muss.

**Action:**
1. In Research-Workflows (`methods/research/`): Pflicht-Pfad ist
   Drive→PDF-Export→pdf-to-markdown
2. `scripts/convert_pdfplumber.py` als Fallback dokumentiert

**Status:** In v1.0.0 als Pattern in `methods/research/deep-research-briefs.md` verankert.

---

### 2026-05-03 — Self-Improvement als Pflicht-Schritt am Session-Ende

**Trigger:** User-Vorgabe: „Self-Improvement-Steps should always be mandatory at the end of a session."

**Lesson:** Der Skill hatte `learnings.md` und `skill-improvement-todo.md`, aber
der Trigger zum Updaten dieser Files war nirgends als Pflicht-Schritt im
Iteration-Discipline-Block kodifiziert. „Wäre nett" → wurde inkonsistent gemacht.

**Action:** In Phase 7 (Iteration) als mandatory Session-End-Checkpoint kodifiziert.

**Status:** v1.0.0 — Phase 7 §6 Session-End-Workflow.

---

### 2026-05-03 — Bootstrap: Reference-Files lesen, nicht skimmen

**Trigger:** Beim Workspace-Setup wurden Reference-Files nur header-geskimmt;
spät im Body kanonisierte Klärungen wurden übersehen, ganze Session-Hälften
liefen redundant.

**Lesson:** Reference-Files (insb. `progress.md`, `canon-meta.md`,
`open-questions.md` mit Strikethrough-resolved-Einträgen) müssen mindestens
auf Sektion-Erst-Absatz-Niveau gelesen werden.

**Action:** In Phase 0 (Bootstrap) §3.2 als verbindlich kodifiziert + Pre-Action-Sanity-Check.

**Status:** v1.0.0.

---

### 2026-05-11 — Refactoring zu projekt-agnostisch

**Trigger:** v0.3.3 war zu inhalts-gebunden (Kohärenz-Protokoll-spezifisch).
User-Vorgabe: methodisch statt inhaltlich, AskUserQuestion-Pattern wie
`research-prompt-optimizer`.

**Lesson:** Projekt-spezifische Skills sind nicht wiederverwendbar. Methoden-
zentrierte Skills mit selektierbarer Methoden-Bibliothek skalieren über mehrere
Projekte.

**Action:**
1. Skill in v1.0.0 komplett refactored: 8 Phasen mit Hard Exit Gates
2. AskUserQuestion-Pattern adaptiert von `research-prompt-optimizer`
3. Methoden-Bibliothek (`methods/character/`, `methods/structure/`, etc.) selektierbar
4. Projekt-Workspaces leben außerhalb (`/home/claude/novel-projects/<slug>/`)
5. NCP weiterhin zwingend (delegated via `ncp-author`)
6. /sc:-Commands intern gemappt pro Phase
7. Legacy als `novel-architect-legacy@0.3.3-deprecated` parallel

**Status:** v1.0.0 — siehe `SKILL.md` Frontmatter.

---

## Reserved für künftige Einträge

<!-- Jede Session schreibt hier neue Einträge -->
