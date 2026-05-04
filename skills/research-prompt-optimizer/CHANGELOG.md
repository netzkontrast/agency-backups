# Changelog

All notable changes to **research-prompt-optimizer** are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/);
versions follow SemVer.

---

## [3.3.1] — 2026-05-03 — SKILL.md slim-down

### Changed (no behaviour change)

Refactor pass to bring SKILL.md back under the skill-creator
≤ 500-line Progressive Disclosure budget. v3.3.0 had pushed the
body to 599 lines after adding Phase 5 + opt-in gate logic.

- **Phase 1 — algorithm pseudocode block moved to detail file.**
  The four-step EXTRACT/ASK/CONFIRM/EXIT pseudocode now lives in
  `phases/phase1-intent-capture.md` §0 (new "The Loop — Algorithm"
  section, added at the top of that file's body). SKILL.md keeps
  a 6-line prose summary plus a pointer to §0.
- **Phase 2 — sub-phase algorithm details moved to detail file.**
  The 130-line Sub-Phase Algorithms section (2.1–2.9 with full
  signal-word tables, override-trigger logic, self-applied-hook
  details, sub-enum dispatch shapes) is replaced by a single 11-row
  summary table covering what each sub-phase does, its output, and
  which gate it precedes. The detailed algorithms were already in
  `phases/phase2-planning.md` §1–§10 — no information lost.
- **Phase 4 — audit-body steps compressed.** The Step 0 opt-in gate
  pseudocode stays inline (it's the v3.3.0 behaviour-change anchor
  and must be visible in the thin file), but Steps 1–5 are now a
  3-sentence prose summary pointing to
  `phases/phase4-reader-test.md` §0–§4.
- **Phase 5 — non-gate steps compressed.** Step 3 export-gate
  pseudocode stays inline (same reasoning — visible behaviour
  contract), Steps 1, 2, 4 are now prose pointing to
  `phases/phase5-finalize.md` §1–§4.

### Added — `phases/phase1-intent-capture.md` §0

New "The Loop — Algorithm" section at the top of the file, holding
the four-step pseudocode that was previously inline in SKILL.md.
ToC updated. No content removed from later sections.

### Added — `phases/phase4-reader-test.md` Step 0

The opt-in gate pseudocode (was only referenced before) is now
written out inline in the detail file as a new "Step 0 — Opt-in
Gate" section before Step 1, so the detail file is self-contained
without needing to read SKILL.md to know what Step 0 looks like.

### Result

- SKILL.md: 599 → 460 lines (139-line reduction; well under the
  500 budget).
- Phase 1 detail file: 419 → 457 lines (added §0 algorithm).
- Phase 4 detail file: 229 → 259 lines (added Step 0 opt-in gate).
- All other files unchanged.
- All audit + zip + Drive-upload behaviour identical to v3.3.0.

### Not changed

- Frontmatter description, triggers — untouched.
- All schemas, modules, examples, render code, io_helpers — untouched.
- Phase 2, 3, 5 detail files — untouched (already complete).
- All v3.3.0 behaviour change semantics — preserved verbatim.

### Migration

None. This is a documentation refactor; pipeline behaviour is
byte-identical to v3.3.0. Callers that read SKILL.md programmatically
will see the slimmer body but identical YAML frontmatter version
slot (`3.3.0` → `3.3.1`).

---

## [3.3.0] — 2026-05-02 — opt-in audit + workspace finalize

### Behaviour change (breaking for callers that assumed always-audit)

Phase 4 (Reader Test) is now **opt-in, default OFF.** Every
pipeline run inserts a mandatory askuser gate immediately after
Phase 3 with the question *"Reader-Test-Audit auf den gerenderten
Prompt laufen lassen?"* The audit body — five-question prediction,
three sweeps, `write_audit_md`, post-audit fix/accept gate — only
executes on explicit `Ja`. On `Nein` the pipeline jumps directly
to the new Phase 5.

Rationale: the audit is valuable for high-stakes prompts and
overkill for quick exploratory ones. Forcing it on every run
creates askuser fatigue and writes audit artefacts the user never
asked for. The opt-in gate keeps the capability one tap away
without paying its cost upfront.

### Added — Phase 5 (Finalize)

New terminal phase that runs unconditionally after Phase 3 (when
audit is skipped) or after Phase 4 acceptance:

1. Bundles every artefact for the current slug into
   `workspace_<slug>.zip` via the new `zip_workspace` helper.
2. Presents the zip via `present_files`.
3. Asks via askuser whether to: download only / additionally
   upload to Google Drive / nothing further.
4. On Drive upload: loads `Google Drive:create_file` via
   `tool_search` (lazy — never before the gate), uploads the zip,
   surfaces the Drive link.

### Added — `render/io_helpers.py::zip_workspace`

```python
zip_workspace(output_dir, slug, paths=None) -> Path
```

Auto-collects every file in `output_dir` whose name contains
`slug` (excluding prior `workspace_*.zip` to prevent recursion),
or accepts an explicit `paths=[...]` override. Atomic write via
`.tmp` + `os.replace`. Idempotent per slug. Smoke-tested against
intent + meta-prompt + rendered-prompt fixture.

### Added — `phases/phase5-finalize.md`

Lazy-loaded detail spec covering:
- `zip_workspace` invocation patterns
- Export gate semantics
- Google Drive upload flow (folder selection, auth-failure
  recovery via `suggest_connectors`, large-zip handling)
- Re-run / slug-collision edge cases
- Recap of Hard Rules

### Changed

- **SKILL.md frontmatter:** version `3.2.2` → `3.3.0`. Description
  updated from "four-phase pipeline" to "five-phase pipeline" and
  now mentions opt-in audit + workspace finalize.
- **SKILL.md pipeline overview table:** Phase 4 marked
  *(opt-in, default OFF)*; Phase 5 row added.
- **SKILL.md hand-off contract paragraph:** "Phase 4 audits when
  opted in" instead of unconditional audit.
- **SKILL.md Phase 3 closing line:** "proceed to the Phase 4
  opt-in gate" instead of "proceed directly to Phase 4".
- **SKILL.md Phase 4 algorithm:** inserts step 0 (opt-in gate)
  before the load/predict/audit steps. Steps 1–5 only execute on
  `Ja`.
- **SKILL.md Phase 4 Hard Rules:** "Phase 4 always runs" replaced
  with "Phase 4 is opt-in. The pre-audit gate is mandatory; the
  audit body is what's optional." Re-audit rule clarified to
  "if opted in again."
- **SKILL.md Anti-Patterns:** removed stale *"Skip Phase 4 because
  the rendered prompt looks fine"* (skipping is now valid).
  Added four new anti-patterns covering: auto-running audit
  without yes, skipping the opt-in gate, silent Drive upload,
  premature `tool_search` for Drive.
- **SKILL.md Reference Files table:** new `phases/phase5-finalize.md`
  row; `render/io_helpers.py` row updated to "Phase 1, 2, 4, 5
  file I/O" with `workspace zip` in the writers list.
- **SKILL.md End-to-End walk-through:** updated to show the new
  opt-in gate + Phase 5 zip + Drive option. Estimated askuser
  turns adjusted from 4–7 to 5–8.
- **`phases/phase4-reader-test.md`:** intro now flags the document
  as describing the audit body that only executes on opt-in `Ja`.

### Not changed

- All Phase 1, Phase 2, Phase 3 algorithms — untouched.
- `catalog.yaml`, all `modules/`, all `docs/` — untouched.
- `meta-prompt-spec.md` — untouched (no schema change).
- `examples/example-intent.yaml`,
  `examples/example-meta-prompt.yaml` — untouched.
- Audit semantics when opted in — identical to v3.2.x.

### Migration

Callers that relied on the audit always running must now
explicitly select `Ja` at the new Phase 4 gate. No artefact
filenames changed; `research-prompt-audit_<slug>.md` is still
written when the audit runs. The new `workspace_<slug>.zip`
is additive — prior workflows that ignored Phase 5 still work,
they just gain a packaged bundle at the end.

---



### Changed
- **Frontmatter `description` cut from ~190 to 95 words.**
  skill-creator §"Progressive Disclosure" guidance is "~100 words" —
  the v3.2.1 description was nearly double that.
- **Trigger keywords removed from `description:`** — they live only
  in `metadata.triggers:` now (single source of truth, no
  duplication). The `description:` body refers readers to that
  field rather than re-listing.
- **Description style:** kept the skill-creator-recommended pushy
  phrasing ("Use whenever / even when the user does not literally
  say…") but expressed as coherent use-case prose rather than a
  pipeline-stage enumeration plus keyword dump.

### Not changed
- SKILL.md body content — no reference-file split was needed; the
  body sits at 490 lines (within the ≤ 500 budget).
- `metadata.triggers:` content — same 18 keywords, just now the
  single home for them.
- All schemas, modules, examples, render code — untouched.

---

## [3.2.1] — 2026-05-02 — skill-creator review pass

Post-v3.2.0 review applied via the `skill-creator` skill's anatomy
+ writing-style + description-triggering checklists. No behavioural
changes; documentation hygiene + triggering surface widened.

### Changed
- **Description rewritten** to declare four phases (was three),
  add Phase-4 trigger anchors (`audit research prompt`,
  `validate research prompt`, `reader-test`, `blind-spot check`),
  and adopt the skill-creator-recommended "use whenever / even when
  the user does not explicitly say" pushy phrasing for better
  trigger recall.
- **Hard Rules across Phases 1, 2, 4** rephrased: `Never X`
  imperatives reframed as `Don't X — because <reason>` per
  skill-creator §"Writing Style" ("explain the why … if you find
  yourself writing ALWAYS or NEVER in all caps, that's a yellow
  flag"). 7 Never-imperatives reduced to 1 (in an anti-pattern
  cell where it reads naturally).
- **Anti-Patterns table header** softened from "Things to Never Do"
  to "Anti-Patterns" with a one-sentence introduction.
- **H1 header** in SKILL.md updated from `v3.0` to `v3.2`.
- **AGENTS.md pressure-tracker** clarified to count body-only lines
  against the 500 budget (frontmatter excluded).

### Added
- **Tables of Contents** in three reference files: 
  - `phases/phase1-intent-capture.md` (405 lines)
  - `phases/phase2-planning.md` (883 lines)
  - `meta-prompt-spec.md` (722 lines)
  Per skill-creator §"Progressive Disclosure" — for files >300
  lines, a ToC at the top gives Claude a navigation index before
  it descends into detail.
- **`evals/trigger-eval.json`** — 18-query eval set (9 should-trigger
  + 9 should-not-trigger) for description-triggering optimization.
  Mix of German and English, Phase-1 and Phase-4 use-cases, casual
  and formal phrasing. Near-miss negatives test trigger-overlap
  vocabulary without being too easy.
- **`evals/readme.md`** — folder index per the decentralized-doc
  rule in `AGENTS.md`.

### Drift fixes during the pass
- `meta-prompt-spec.md` opening listed Phase 3 as "🚧 stubbed" —
  corrected to live with schema_version 3.1.
- `phase2-planning.md` ToC entry for §9 now flags it as legacy
  (Soft-Cap-5 superseded by mini-gates in v3.2).

---

## [3.2.0] — 2026-05-02 — Phase 4 (Reader Test) + file-first I/O + provenance

Kaizen pass driven by structural patterns from the `doc-coauthoring`
skill: visible context status, generate-before-apply at decision
points, and a fresh-frame audit pass against the rendered output.
Combined with a Python-first / chat-minimalism overhaul and
provenance tracking with append-only revisions.

### Added
- **Phase 4 — Reader Test** (NEW). Audits the rendered prompt from a
  fresh-context vantage point: 5 predicted reader questions,
  ambiguity sweep, assumption sweep, contradiction sweep. Writes
  `research-prompt-audit_<slug>.md` with verdict
  (`pass` / `fix-recommended` / `fix-required`). Single askuser gate:
  Accept / Fix constraints+seeds / Fix intent.
- **`phases/phase4-reader-test.md`** — full Phase-4 specification:
  audit-question patterns, verdict thresholds, edge cases (bilingual
  prompts, re-rendered audits, "fix intent" flow), worked example.
- **`render/io_helpers.py`** — centralised file-IO module: atomic
  writes, normalised `make_provenance()`, `next_versioned_path()` for
  append-only versioning, plus typed writers for intent.yaml,
  meta-prompt.yaml, status views, plan views, and audit views. All
  Phase 1, 2, 4 outputs go through these helpers.
- **Three-gate Phase-2 approval** replacing the monolithic Soft-Cap-5
  loop: Gate 1 after Routing (2.2), Gate 2 after Constraint Blocks
  (2.5), Gate 3 after Plan View (2.8). Per-gate hard cap on edit
  cycles; early routing/module errors are caught before downstream
  work runs.
- **Status view** for Phase 1 — `intent-status_<slug>.md` written
  before each askuser turn, showing all slots grouped as
  ✓ filled / ⚠ partial / ✗ missing plus the intent assembled so far.
- **Plan view** for Phase 2 — `meta-prompt-planview_<slug>.md`
  written and progressively filled at each gate; user reads file
  instead of YAML in chat.
- **Normalised `provenance` block** across all three schemas:
  Schema 1.0 → 1.1, Schema 2.0 → 2.1, Schema 3.0 → 3.1. Carries
  `created`, `skill_version`, `phase`, `slug`, `output_filename`,
  `category_signal`, `selected_methods`, `selected_framework_structural`,
  `cross_pollination_pair`, `previous_version`, `revision_count`.
- **Append-only revisions log** — every YAML artefact has a
  `revisions[]` array; post-approval edits append entries via
  `io_helpers.append_revision()`. Original state remains visible
  through the `previous_version` chain.
- **Render versioning** — `render.py` writes
  `research-prompt_<slug>.md` on first render, then `_v2.md`,
  `_v3.md` etc. on subsequent renders. Each new file's frontmatter
  carries `previous_version` for chain navigation.

### Changed
- **Chat minimalism throughout.** Sub-phase status announcements
  ("Phase 2.3 läuft...") removed. Plan-view YAML no longer printed in
  chat — written to file and `present_files`'d. Self-applied hook
  outputs go to `meta-prompt.self_reflection` block, not chat.
- **Hard 3-question cap** on every `ask_user_input_v0` call —
  "1–3 questions" loosely was tightened to "max 3, never more".
- **`render.py` schema validator** accepts both Schema 2.0 and 2.1.
  v3.2 provenance frontmatter is prepended above existing module
  frontmatter; `_yaml_inline()` helper added for clean serialisation.
- **SKILL.md compressed** from 489 → 497 lines despite adding a full
  fourth phase: large algorithm bodies and YAML output blocks moved
  to `phases/phase[1-4]-*.md`; inline-Python `ask_user_input_v0`
  blocks compressed to prose; verbose self-applied-hooks table
  compressed to summary with single source of truth in
  `catalog.yaml`.

### Anti-patterns added
- "Print intent or plan YAML in chat" — file-first violation.
- "Announce sub-phase status in chat" — chat noise.
- "Skip Phase 4 because the rendered prompt looks fine" — exactly
  the blind spot Phase 4 catches.
- "Flag `{{slot}}` placeholders as ambiguities in the audit" —
  those are intentional `agent_runtime_fill` markers.
- "Overwrite an existing rendered prompt instead of versioning" —
  append-only semantics required for audit chain.

### Migration notes
- Existing v3.1 `meta-prompt.yaml` files (schema 2.0) still render
  correctly via the relaxed validator — no migration required.
- New v3.2 features (versioning, provenance, audit) only activate
  when the meta-prompt carries the new `provenance` block.
- The two example fixtures (`examples/example-intent.yaml`,
  `examples/example-meta-prompt.yaml`) were updated to v3.2 schema
  with provenance + revisions; smoke-tested through render.py.

---

## [3.1.0] — 2026-05-02 — Phase 3 (Render) live

End-to-end pipeline now functional: a single `intent.yaml` flows
through Phase 1 → Phase 2 → Phase 3 and exits as a fully-rendered
`research-prompt_<slug>.md`.

### Added
- **`render/render.py`** — single-file Python renderer (pure stdlib +
  pyyaml). Reads approved `meta-prompt.yaml`, resolves all four slot
  types (`phase2_fill` / `phase2_fill_or_runtime` /
  `agent_runtime_fill` / `fill_from`), composes Schema-3-ordered
  Markdown, writes `research-prompt_<slug>.md`.
- **15 deterministic `fill_from` handlers** for computed slots.
- **Cross-module `phase2_fill` flatten** — e.g. `M13.orthogonal_lens`
  now visible inside `final-checklist`.
- **Auto-fill bridge** for `m3-batch` slots from `batches[]` when
  Phase 2 didn't write them explicitly.
- **3 new `fill_from` handlers** for `m3-batch`:
  `items_render_block`, `iteration_steps_render_block`,
  `output_schema_render_block`.

### Changed
- **`m3-batch.md` template** upgraded to actually consume its declared
  slots (was using structural brackets only).
- **End-to-end smoke-tested** against
  `examples/example-meta-prompt.yaml`: 900-line research-prompt
  output, 0 unfilled non-runtime slots, 0 Jinja remnants.

### Consistency pass (post-3.1.0)
- Frontmatter version bumped from `3.0.0-phase1` to `3.1.0`,
  status from `incremental` to `stable`.
- Removed all "next iteration" / "stubbed" / "not yet implemented"
  references in `SKILL.md`.
- Phase-1 algorithm step 3.c and Phase-2 sub-phase 2.10 now show
  clean phase-to-phase transitions instead of "announce that the
  next phase isn't built yet".
- Reference-files table corrected: actual module counts (13 methods,
  7 frameworks, 5 replication, 6 cross-pollination, 3 categories,
  5 partials, 1 verification) instead of "samples shipped".
- `SKILL.md` line count: 497 → 489 (≤ 500 budget preserved).
- Anti-patterns table refreshed: removed two roll-out-era patterns
  ("Improvise before Phase 2 ships", "Promise outputs you cannot
  deliver"); added Phase-2 approval-gate pattern + hand-edit
  anti-pattern.
- `created_by_skill` field in YAML output template synced to
  `v3.1.0`.

### Removed
- **`NEXT_STEPS.md`** — superseded by this `CHANGELOG.md`. Future
  roadmap items live in the "Forward look" section below.
- **`ARCHIVE_NOTE.md`** — described the historical v2.1 → v3.0
  migration; obsolete since v3.0 has been the running version for
  two iterations.
- **`MANIFEST.sha256`** — was a one-time integrity-check artefact for
  the v3.0-phase2 delivery. Repository now relies on git for
  integrity tracking.

### Repository documentation
- **`AGENTS.md` (skill-root)** — generic skill-development spec
  consolidating folder hierarchy, decentralized-readme rule,
  drift-prevention, pre-commit checklist, frustration logging.
- **`AGENTS.md` (project-specific)** — phase-pipeline contract,
  schema-change rules, catalog/module discipline, self-applied-hook
  index sync, 500-line pressure tracker, per-project pre-commit
  additions.
- **19 new `readme.md` files** across `modules/`, `docs/`, `phases/`,
  `render/`, `examples/`. Cross-linked: every `modules/<type>/readme.md`
  links to the corresponding `docs/<type>/<file>.md` (📖 concept), and
  every `docs/<type>/readme.md` links back (⚙️ module). 206 relative
  links validated.

---

## [3.0.1] — Template polish + concept-doc library

### Added
- 9 new slots finalized in 3 modules during template-polish sweep
  (synthesis: 3, m2-restatement: 5, m3-batch: 1).
- 3 frontmatter `self_applied_phase2:` blocks synced with catalog
  index (M01, M13, m0-reflection).
- 40 per-module concept docs in `docs/<type>/<id>.md`.
- 4 master docs in `docs/`:
  - `_README.md` (docs-tree overview)
  - `_CONCEPT-TEMPLATE.md` (canonical structure)
  - `_BRACKET-INVENTORY.md` (bracket classification)
  - `_SLOT-PROVENANCE-MAP.md` (intent-field → slot map)

---

## [3.0.0-phase2] — Planning algorithm complete

### Added
- Three-phase architecture in `SKILL.md`.
- Phase 2 algorithm specified inline in `SKILL.md` (v1.2 spec frozen).
- `phases/phase2-planning.md` — full detail with edge cases, worked
  example, §12 Self-Applied Critical Thinking.
- `meta-prompt-spec.md` — Schema 1 + Schema 2 frozen.
- `catalog.yaml` — master index of all 34 modules + 7
  `self_applied_phase2` hook specs.
- All 5 partials shipped, including `react-loop-anchored` (KEY
  INNOVATION) and `language-warning`.
- All 13 methods (M01–M13). Four self-applied in Phase 2: M01, M03,
  M05, M07.
- All 7 frameworks (react, risen, tidd-ec, co-star, care, crispe,
  synthesis).
- All 5 replication mechanisms (m0–m4). m0 and m4 self-applied in
  Phase 2.
- All 6 cross-pollinations (a↔b, a↔c, b↔c).
- All 3 categories (a-exploration, b-extraction, c-lifecycle).
- `examples/example-meta-prompt.yaml` — worked Phase-2 output with
  full `self_reflection` block.

### Changed
- `[BRACKET]` → `{{slot}}` body conversion in module files (14
  explicit slot conversions; remaining brackets are intentional
  format markers).

---

## [3.0.0-phase1] — Intent capture only

First incremental ship. Phase 1 fully specified and runnable:
askuser-loop until 100% slot clarity, explicit user-approval gate
before file write, intent.yaml as forward-compatible artifact.

---

## Migration: v2.1 → v3.0

Historical, completed. No `_archive/` directory exists in this
repository — the v2.1 codebase was archived externally before v3.0
was installed. Key architectural deltas v2.1 → v3.0:

| Aspect | v2.1 | v3.0 |
|--------|------|------|
| Intent capture | "if ≥ 2 params blocking, ask 1 compound question" | iterative askuser-loop (Phase 1) |
| User approval | none — Phase 6 writes file directly | explicit approval gate before each file write |
| Hand-off | implicit (chat context) | structured YAML files between phases |
| Templates | `[BRACKETS]` with collapsed semantics | partials with `{{slot}}` + 4-type slot system |
| Module catalog | implicit (folder structure) | explicit `catalog.yaml` with provides/requires deps |
| ReAct anchoring | generic 3-question prompt | dynamic, names active methods in every Reason phase |
| Language handling | EN/DE mixed silently | explicit warning if `intent.language != "en"` |
| Bespoke threshold | implicit / never auto | explicit ≥ 2 override-triggers (Q3 v1.1) |
| Edit loop | none | hybrid sub-enums + free-text fallback, soft cap @ 5 |
| Self-applied critical thinking | none | 7 hooks anchored at sub-phases, depth-scaled (Q6 v1.2) |
| Composition | Claude assembles inline at runtime | Python script renders from approved plan (Phase 3) |

---

## Forward look

No active roadmap items at the time of writing. Candidates for v3.3
or v4.0:

- **Diff harness** — feed the same intent into archived v2.1 vs v3.x,
  compare rendered prompts, catalog which failure modes were fixed
  vs introduced.
- **Audit history view** — given multiple `_v1.md`, `_v2.md`,
  `_v3.md` rendered prompts and their audits, render a diff timeline
  showing which findings were resolved at each iteration.
- **Skill-internal eval harness** — currently delegated to the
  separate `skill-engineering` skill; could become first-class here.
- **Pluggable framework catalogs** — currently the 27-framework
  `prompt-optimizer` catalog is referenced via the `synthesis`
  protocol, not duplicated. Whether to inline-import remains open.

---

## Out of scope (decided)

- Multi-language template variants beyond DE/EN annotation (Q1 v1.1
  decision: EN templates only with warning).
- Cloud / API integration — pure local file-generation skill.
