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

**Lesson (cartographer over-scope; FL1 anchor).** The first `/sc:design`
run during this hardening cycle spawned an Explore subagent ("line-level
cartographer") that produced a 12-file manifest projecting 524 LOC of
MOVE + 14 new sub-module method files. Post-setup-commit grep-
verification revealed the reality: 17 broken refs across 6 files, no
MOVE, no new method files. The cartographer had reasoned structurally
without verifying which paths were actually broken — three of its named
files (`phase2-narrative-architecture.md`, `phase4-world-research.md`,
`phase6-drafting.md`) had **zero** broken refs and were already in
correct two-layer state; one file the cartographer missed entirely
(`phase1-intent-capture.md`) needed fixing.

**Mitigation rule** (binding for future planning-ladder runs; proposed
for `TASK.md §4.9` follow-up amendment): any Explore subagent producing
a structural-rewrite manifest MUST (a) cite the `grep` / search command
that produced its claims, (b) include the grep output line-by-line,
(c) classify findings as "verified broken" vs. "structurally suggested."
Subagents that perform pure structural reading without grep-
verification SHOULD have their manifests treated as design hypotheses,
not implementation targets — and the orchestrator agent (the
`/sc:design` synthesizer) SHOULD demand grep evidence before accepting
the manifest into the workflow plan.

**Action (v1.1.1 shipped across 11 commits on the v1.1.1 branch):**

1. **Two-layer contract enforcement:** rewrote 17 broken refs across 6
   files (`phase1-intent-capture.md`, `phase3-character-architecture.md`,
   `phase5-scene-matrix.md`, `commands/novel-{characters,research,scenes}.md`)
   into canonical `[→ novel-architect-<sub>]` delegation prose (3 phase
   files, REWRITE+delegate) or sub-module-path links (3 command files,
   REWRITE-only). `methods/conflict/` stays orchestrator-resident per
   the cross-cutting-method rule. Commit `51063bf`.
2. **Scene graduation:** scene sub-module's "stub in v1.1.0" self-
   qualifier was a metadata-level limitation that no longer matched
   reality — `scene-level-bridge.md` (149 LOC, Task 075) shipped in
   v1.1.0 and fully covers Q1–Q5 audit + scene-matrix execution +
   drafting-precheck. The qualifier dropped from orchestrator
   `metadata.delegates_to`; both SKILL.md versions bumped to v1.1.1.
   Commit `3308ffe`.
3. **SKILL_VERSION SSoT:** `io_helpers.SKILL_VERSION` had drifted from
   `SKILL.md.metadata.version` (constant said `1.0.0`, frontmatter
   said `1.1.0`). Bumped to `1.1.1` and added a pytest assertion
   (`TestSkillVersionSsot`) that loads the frontmatter and asserts
   equality — future drift fails at pre-commit. Commit `d5b2216`.
4. **Three WARN-tier CLI linters shipped** (predecessors to the
   ERROR-tier Epic 083 work):
   - `tools/check-canon-status.py` (170 LOC, 8 rules `CANON.*`,
     13 tests) — commit `78296c6`
   - `tools/check-worksheet-order.py` (160 LOC, 6 rules `WORKSHEET.*`,
     10 tests) — commit `dd68a25`
   - `tools/check-hard-rules.py` (200 LOC, 8/12 rules H1-H4 + H9-H12
     mechanical; H5-H8 deferred as INFO tier pending dramatica-nav
     ontology integration; 16 tests) — commit `706bbd8`

   Fixtures at `tools/tests/fixtures/novel-architect-v111/`. Wired into
   `tools/check-governance.sh` under the "novel-architect v1.1.1 linters"
   advisory block. ERROR-tier promotion + replacement under
   `tools/novel-architect-checks/` is the scope of [Epic 083 v1.2.0
   enforcement](../../../tasks/083-novel-architect-v120-enforcement-epic/task.md)
   sub-tasks 084/085/086 — each carries an explicit "WARN-tier
   predecessor disposition" section deciding replace vs. evolve.

**Planning-ladder provenance:** v1.1.1 executed the full
`/sc:analyze → /sc:brainstorm → /sc:design → /sc:workflow` ladder
codified in [TASK.md §4.9](../../../TASK.md#49-planning-pipeline-for-t3-structural-tasks-sc-ladder).
The ladder is itself a v1.1.1 contribution — §4.9 was authored in commit
`aaf9567` based on the lessons from this very cycle (5 normative rules
T.4.9.1–T.4.9.5 + 3 Gherkin scenarios). The cartographer-over-scope
mitigation rule above is the open follow-up amendment for §4.9.

**Status:** v1.1.1 shipped across 11 commits on this branch
(`aaf9567` through `706bbd8`); the 4 planning-Tasks 090/091/092/093 that
tracked the work were deleted in the v1.1.1-to-v1.2.0 declutter pass —
the executed work lives in git history + this changelog entry. v1.2.0
enforcement work tracked under [Epic 083](../../../tasks/083-novel-architect-v120-enforcement-epic/task.md)
+ standalone [Task 089](../../../tasks/089-retire-novel-architect-legacy/task.md)
(legacy retirement, blocked on observable criteria).

---

## Reserved für künftige Einträge

<!-- Jede Session schreibt hier neue Einträge -->
