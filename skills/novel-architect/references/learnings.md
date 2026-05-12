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

### 2026-05-11 — v1.1.0 Sub-Module Refactor + Dramatica-Native Integration

**Trigger:** PR #101 (v1.0.0) review surfaced 10 findings, three with
structural depth: (a) hardcoded `project_workspace_root`, (b) inlined
prompts in subtasks rather than `/prompts/` extraction, (c) no automated
tests. v1.0.0 was monolithic — phase logic, method libraries, render
helpers all in one skill directory — which made the skill hard to extend
and made the dramatica-theory reference corpus structurally unused.

**Lesson:** A skill that delegates to a domain-skill (here:
`dramatica-theory`) but never *applies* its references is structurally
incomplete. The 13 references in `skills/dramatica-theory/references/`
(Worksheet, Hard Rules, Anti-Patterns, Scene-Level-Bridge, Worked
Examples) needed first-class adoption — not as separate copies, but as
phase-bound application contracts.

The Dual-Kernel "Architect-with-Submodules" pattern is the right shape:
one orchestrator + N sub-skills, each with a single domain entry point
+ a delegation contract back to the orchestrator. This reduces skill-
match ambiguity (the loader picks the most specific sub-skill) and lets
each sub-skill evolve independently. The `delegates_to` metadata field
documents the routing.

**Action (v1.1.0 — Tasks 071–077):**

1. **Sub-Module Refactor (Task 071):** Split monolith into orchestrator
   + 4 sub-skills (`novel-architect-{character,structure,world,scene}`).
   Methods migrated, `delegates_to` updated, config-loading boundary
   redesigned (`NOVEL_ARCHITECT_PROJECTS_ROOT` env var; per-project
   `project-config.yaml:project.workspace_root` honoured).
2. **Phase 2 Worksheet-Loop (Task 072):** Dramatica's
   `00-storyform-worksheet.md` is now the SSoT for Phase 2 slot order;
   `architecture.yaml` writes follow the worksheet sequence.
3. **Hard Rules H1–H12 (Task 073):** Storyform validation runs after
   each slot write; H-rule violations block Gate 2 / Gate 3.
4. **Anti-Patterns AP-1 to AP-14 (Task 074):** New
   `references/anti-patterns.md` cross-references all 14 patterns to
   their phase-of-occurrence with detection hints.
5. **Scene-Level-Bridge Q1–Q5 (Task 075):** Per-moment audit between
   storyform and prose; runs as pre-check in Phase 6, as detail-fill in
   Phase 5.
6. **Canon-Status Schema (Task 076):** Dual-Kernel canon-status
   lifecycle (`proposed → accepted → contested → superseded → archived`)
   adopted for `canon-meta.md`; Phase 7 audit-mode resolves contested
   entries.
7. **MIF Level 3 + SessionStart-Hook (Task 077):** Per-entry frontmatter
   card in `learnings.md`; lean `session-start.sh` emits unresolved-
   learning + contested-canon roll-up at Bootstrap.

**Tests scaffolded (PR #101 review §3):** `render/tests/` with 32
pytest cases covering `io_helpers` slug validation, env-override
projects-root, atomic-write, and renderer contracts (single + dual
storyform_count, fail-loud on missing `chapter_count_target`).

**Bilingual contract (PR #101 review §2.7):** DE-prose + EN-schema
mixing is intentional and documented in SKILL.md §"Bilingual Contract"
— normalisation to a single language requires escalation.

**Status:** v1.1.0 shipped via Task 070 Epic close (this commit set).
Legacy `novel-architect-legacy@0.3.3-archived` retained per Task 070
§"Legacy Retirement Criterion"; retirement Task gated on 3+
productive Kohärenz-Protokoll sessions without legacy fallback.

---

### 2026-05-12 — v1.1.1 Hardening (Two-Layer Contract + Scene Graduation + SKILL_VERSION SSoT)

**Trigger:** Post-v1.1.0 `/sc:analyze` surfaced 11 H/M/L findings against
the v1.1.0 release. The biggest were structural: H1 (16+ broken refs to
migrated `methods/character/`, `methods/structure/`, `methods/research/`
paths in the orchestrator's phase + command prose) and H2 (zero
delegation prose to sub-modules — only `metadata.delegates_to` declared
the relationship, so the prose layer was *monolithic-as-before*).
v1.1.0 had achieved metadata-level sub-module delegation but not
runtime-level — the user-facing prose still loaded files from paths the
git mv had emptied.

**Lesson:** A sub-module refactor needs to land at TWO layers: (1) the
`metadata.delegates_to` declaration in SKILL.md, AND (2) the prose
layer that *invokes* the delegation at runtime (phase/command files
naming the sub-module by name, not naming its internal file paths). The
first without the second produces a skill that *says* it delegates
but doesn't. The Dual-Kernel "Architect-with-Submodules" pattern
requires both — an "architect" that knows it delegates must also
*demonstrate* the delegation in its own prose, not just in metadata.

**The cartographer over-scope finding (FL1 — F-090.1).** The first
`/sc:design` run spawned an Explore subagent ("line-level cartographer")
that produced a 12-file manifest projecting 524 LOC of MOVE + 14 new
sub-module method files for cluster A. Post-A.0 grep-verification
revealed the reality: 17 broken refs across 6 files, no MOVE, no new
method files. The cartographer had reasoned structurally without
verifying which paths were actually broken. Mitigation rule (proposed
for `TASK.md §4.9` follow-up): any subagent producing a structural-
rewrite manifest MUST cite the grep / search command it ran and include
the grep output line-by-line; structural reading without grep-
verification produces design *hypotheses*, not implementation targets.

**Action (v1.1.1 — Task 090):**

1. **Two-layer contract enforcement (cluster A.1):** rewrote 17 broken
   refs across 6 files (`phase1-intent-capture.md`, `phase3-character-architecture.md`,
   `phase5-scene-matrix.md`, `commands/novel-{characters,research,scenes}.md`)
   into canonical `[→ novel-architect-<sub>]` delegation prose (3 phase
   files, REWRITE+delegate) or sub-module-path links (3 command files,
   REWRITE-only). `methods/conflict/` stays orchestrator-resident per
   the cross-cutting-method rule.
2. **Scene graduation (cluster B.1):** scene sub-module's "stub in
   v1.1.0" self-qualifier was a metadata-level limitation that no
   longer matched reality — `scene-level-bridge.md` (149 LOC, Task 075)
   shipped in v1.1.0 and fully covers V111.US2's Q1–Q5 audit + scene-
   matrix execution + drafting-precheck per `/sc:design` Revised
   Artifact 3. The qualifier dropped from orchestrator
   `metadata.delegates_to`; both SKILL.md versions bumped to v1.1.1.
3. **SKILL_VERSION SSoT (cluster B.2):** `io_helpers.SKILL_VERSION` had
   drifted from `SKILL.md.metadata.version` (constant said `1.0.0`,
   frontmatter said `1.1.0`). Bumped to `1.1.1` and added a pytest
   assertion (`TestSkillVersionSsot`) that loads the frontmatter and
   asserts equality — future drift fails at pre-commit.
4. **Three CLI linters (cluster C):** `tools/check-{worksheet-order,hard-rules,canon-status}.py`
   ship at WARN tier with fixture corpus and `check-governance.sh`
   integration. Hard-rules promotion to ERROR gated on Task 092 after
   one validation cycle.
5. **Dead-code prune + docstring fix (cluster D):** 8 unused public
   helpers in `io_helpers.py` removed (YAGNI); `project_workspace()`
   docstring promise about per-project YAML override dropped (was
   unimplemented; either implement or stop promising — chose stop).

**Planning ladder:** Task 090 is the worked example codified in
`TASK.md §4.9` — `/sc:analyze` → `/sc:brainstorm` (6 locked decisions
D1–D6) → `/sc:design` (5 artifacts, 4 Explore subagents) →
`/sc:workflow` (revised to 12 commits / 3–4 h after cartographer
correction). The full planning provenance is recoverable from
`tasks/083-*/{task,readme,workflow}.md` without re-running the ladder.

**Status:** v1.1.1 shipped via Task 090 close (this commit set).
Companion Tasks 084 (retirement placeholder), 085 (linter ERROR
promotion), and 086 (scene-audit linter) filed alongside as
`task_status: blocked`, gated on Task 090 plus their own preconditions.

---

## Reserved für künftige Einträge

<!-- Jede Session schreibt hier neue Einträge -->
