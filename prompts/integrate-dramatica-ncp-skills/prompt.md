---
type: prompt
status: active
slug: integrate-dramatica-ncp-skills
summary: "Authoritative instruction set for Task 015 — author Narrative Ontology schemas, bootstrap the ontology, generate per-term frontmatter, build the dramatica-nav navigator suite, and wire all four narrative skills to it. Encodes the binding resolutions of OQ-A, OQ-B, OQ-C from the kickoff research SPEC."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: integrate-dramatica-ncp-skills
prompt_spawned_from_research: integrate-dramatica-ncp-skills
---

# Integrate Dramatica Skills With NCP and Novel-Architect

## Framework

**RISEN + ReAct.** The output mix is structured — JSON Schemas, JSON ontology table, per-term YAML frontmatter, Python scripts — for which RISEN gives a clean role/input/steps/expectations/narrowing scaffold. The execution is loop-shaped — walk every Type-bucket file, emit frontmatter, validate, fix, re-validate — for which ReAct gives the Reason → Act → Observe loop. The two compose cleanly: RISEN structures the *static* deliverable shape; ReAct structures the *dynamic* authoring loop.

---

## § RFC 2119

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

---

## R — Role

You are the **Narrative Ontology architect** for the four narrative skills (`dramatica-theory`, `dramatica-vocabulary`, `ncp-author`, `novel-architect`). Your output is the canonical machine-readable bridge between (a) Dramatica theory, (b) the Narrative Context Protocol's JSON enum surface, and (c) the persona-driven working scenarios of the novel author and the organist / lyric architect. You write the schemas, you bootstrap the ontology, you generate per-term frontmatter, you implement the navigator suite, and you wire the four skills to it. You do **not** rewrite Dramatica theory and you do **not** coin new NCP enum values.

## I — Input

The executor MUST read, in order:

1. [`/tasks/015-integrate-dramatica-ncp-skills/task.md`](../../tasks/015-integrate-dramatica-ncp-skills/task.md) — the binding plan, the eleven persona scenarios, the schema skeletons, the Gherkin acceptance criteria.
2. [`/research/integrate-dramatica-ncp-skills/output/SPEC.md`](../../research/integrate-dramatica-ncp-skills/output/SPEC.md) — the kickoff specification with the twelve normative recommendations addressed at this prompt's steps.
3. [`/research/integrate-dramatica-ncp-skills/synthesis/inventory.md`](../../research/integrate-dramatica-ncp-skills/synthesis/inventory.md), [`id-audit.md`](../../research/integrate-dramatica-ncp-skills/synthesis/id-audit.md), [`scenario-survey.md`](../../research/integrate-dramatica-ncp-skills/synthesis/scenario-survey.md) — corpus inventory, the three resolved naming contradictions, and the first-pass scenario survey.
4. [`/research/integrate-dramatica-ncp-skills/reflection/M01-falsification.md`](../../research/integrate-dramatica-ncp-skills/reflection/M01-falsification.md), [`M07-contradiction-log.md`](../../research/integrate-dramatica-ncp-skills/reflection/M07-contradiction-log.md) — falsification triggers and the nine catalogued contradictions.
5. [`AGENTS.md`](../../AGENTS.md), [`TASK.md §3`](../../TASK.md), [`PROMPT.md §3`](../../PROMPT.md), [`RESEARCH.md`](../../RESEARCH.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md) — repo governance.
6. `skills/dramatica-theory/SKILL.md` + `references/`, `skills/dramatica-vocabulary/SKILL.md` + `references/`, `skills/ncp-author/SKILL.md` + `upstream/schema/ncp-schema.json`, `skills/novel-architect/SKILL.md` — the four skills under integration.
7. `skills/spec-skill/SKILL.md` — Mode 1 (Generate) discipline for the schemas' acceptance criteria.
8. `tasks/011-skills-frontmatter-schema-files/task.md` — the L1/L2 schema infrastructure this task consumes (and MUST NOT duplicate).

## Binding Resolutions of Open Questions

The kickoff SPEC's three Open Questions are **resolved** in this prompt and are now binding. The downstream agent MUST NOT re-open them.

### OQ-A — Locale alias YAML shape

**Resolved: flattened keys.** Aliases are stored as `aliases_en`, `aliases_de`, `deprecated_aliases_en`, `deprecated_aliases_de` — each a depth-1 list of strings. The repo-wide constraint *"YAML MUST NOT nest beyond one level"* ([`AGENTS.md § Frontmatter Ontology`](../../AGENTS.md)) is preserved without exception. The nested form `aliases: { en: [...], de: [...] }` is **rejected**: it would either require a repo-wide rule waiver (high cost, low reward) or split the schema across two competing conventions (worse).

The schemas, the ontology JSON, and the per-term frontmatter MUST all use the flattened form. The locale suffix MUST be a 2-letter ISO-639-1 code. New locales (e.g. `aliases_fr`) become legal automatically by adding a key — the schema's pattern allows any `aliases_[a-z]{2}` and any `deprecated_aliases_[a-z]{2}`.

### OQ-B — `# Element (70)` heading

**Resolved: keep the heading; the per-term `kind` field handles the semantics.** The heading in `skills/dramatica-vocabulary/references/elements.md` is a count of *file rows*, not a claim about Dramatica theory. The seven non-canonical rows (Crucial Element, MC Problem, OS Problem/Response/Solution/Symptom, Symptom Element) MUST be authored with `kind: concept` in their per-term frontmatter; the canonical 64 MUST be authored with `kind: element`. A reader querying by `kind` filters cleanly.

Rationale: rewriting the heading to `# Element (64) + Concept (6)` would (a) change human-facing prose for a schema-internal reason, (b) trigger a cascade of similar edits in `types.md` (16+25), `archetypes.md` (8+1), and (c) put the file's own count into conflict with its `## Contents` table-of-contents which lists 70 entries. The schema-side `kind` discriminator does the same job at zero prose cost.

### OQ-C — Dynamic-pair representation

**Resolved: hybrid.** Two complementary representations:

1. **Property of an Element / Variation entry.** Every `kind: element` and `kind: variation` ontology entry whose canonical theory has a dynamic-pair partner MUST carry a `dynamic_pair_id` field pointing at its partner's ontology ID. This makes "what's the partner of `el.trust`?" a constant-time lookup with no extra entry to traverse.
2. **Standalone `kind: dynamic-pair` entries.** Each of the 75 reciprocal pairs from `dramatica-vocabulary/references/dynamic-pairs-index.md` MUST also be minted as a standalone ontology entry with `kind: dynamic-pair`, carrying `pair_member_a` and `pair_member_b` fields pointing at the two halves' IDs. This makes "list every pair where `el.test` is one half" a single query against `pair_member_a == el.test OR pair_member_b == el.test`, and it makes scenario-tagging at the pair level (e.g. `lyric.verse-chorus-pair`) addressable without forcing the tag onto both Element halves.

Reciprocity invariant: for every standalone `kind: dynamic-pair` entry `dp.X`, the entry referenced by `dp.X.pair_member_a` MUST have `dynamic_pair_id == <id of dp.X's other half>`, and symmetrically for `pair_member_b`. The validator script (Step 9 below) MUST verify this on every run.

## S — Steps

### Step 0 — ReAct loop preamble (mandatory bookkeeping)

Before any file edit, write `tasks/015-integrate-dramatica-ncp-skills/notes.md` with three sections (initially empty, populated as the loop runs):

```markdown
## ReAct Trace
<!-- one bullet per Reason → Act → Observe iteration -->

## Inventory Cross-Check
<!-- discrepancies between this run's count and the kickoff inventory -->

## Token-Cost Benchmark
<!-- populated at Step 12 -->
```

Also flip `tasks/015-integrate-dramatica-ncp-skills/task.md`'s `task_status` to `in_progress` (already set) and `updated` to today's ISO date on every checkpoint.

### Step 1 — Inventory term universe

Walk `skills/dramatica-vocabulary/references/*.md`. For every `## <Term>` anchor, record one row in `notes.md § Inventory Cross-Check` with: file basename, anchor, current `kind` guess (per the inventory's per-file primary kind), provenance flag (source vs. extension based on the presence of `⚠ EXTENSION NOTE` at the file head). The kickoff inventory lists 310 rows; this run MUST reproduce that count ±5 — any larger drift indicates a corpus change since 2026-05-04 and MUST be flagged before continuing.

### Step 2 — Author the four schema files

Create `maintenance/schemas/narrative-ontology/`:

- `ontology.schema.json` — JSON Schema Draft 2020-12 for one ontology entry. Fields: `id`, `kind`, `canonical_label`, `aliases_<locale>` (pattern-keyed), `deprecated_aliases_<locale>` (pattern-keyed), `dynamic_pair_id`, `pair_member_a`, `pair_member_b`, `quad_id`, `ktad_position`, `class_id`, `type_id`, `variation_id`, `ncp_appreciation`, `ncp_appreciation_partial`, `ncp_schema_min_version`, `provenance`, `term_file`, `scenarios`. Constraints:
   - `kind` enum: `class | type | variation | element | archetype | character-dynamic | plot-dynamic | storypoint | dynamic-pair | quad | signpost-slot | concept`.
   - `ncp_appreciation` is OPTIONAL. `ncp_appreciation_partial` MUST be present iff `ncp_appreciation` is present (per SPEC R.3.1.2).
   - `pair_member_a` and `pair_member_b` are REQUIRED iff `kind: dynamic-pair`; FORBIDDEN otherwise.
   - `dynamic_pair_id` is RECOMMENDED for `kind: element | variation`; FORBIDDEN for `kind: archetype | quad | concept | dynamic-pair`.
   - `provenance` enum: `source-original | extension-derived`.
   - `additionalProperties: false`.
- `scenarios.schema.json` — schema for one scenario entry: `id` (pattern `^(novel|lyric)\.[a-z0-9-]+$`), `persona` (enum `novel | lyric`), `summary` (≤ 25 words enforced via `maxLength: 200`), `created`.
- `term-frontmatter.schema.json` — same as `ontology.schema.json` minus the fields that live only in the ontology table (`term_file`). Per-term YAML frontmatter MUST validate against this.
- `theory-chunk.schema.json` — schema for theory-chapter frontmatter: `chunk_id`, `covers_ontology_ids` (list, MAY use `kind.*` wildcard), `serves_scenarios` (list of scenario IDs), `summary`.

Cap each schema at 200 lines (per the discipline of `tasks/011`); if any schema exceeds, factor into `<name>.partials.json`.

`additionalProperties: false` on every schema. Drift fails closed.

Write `maintenance/schemas/narrative-ontology/readme.md` describing the four schemas, the canonical-vs-extension provenance rule, and the OQ-A/B/C resolutions encoded above.

### Step 3 — Author canonical scenario set

`maintenance/schemas/narrative-ontology/scenarios.json`. Exactly the eleven scenarios from `task.md § Personas and Working Scenarios`:

```
novel.storyform-slot-fill, novel.act-pivot, novel.crucial-element-audit,
novel.character-arc, novel.diagnose-flat-draft, novel.dual-storyform,
lyric.verse-chorus-pair, lyric.bridge-pivot, lyric.album-arc-mapping,
lyric.archetype-as-system-part, lyric.refrain-as-restatement
```

No additions in this step. New scenarios go through the proposal procedure declared in `task.md § Scenario Taxonomy Rules` and are out of scope for the v0.1 ontology.

### Step 4 — Bootstrap the ontology table

`maintenance/schemas/narrative-ontology/ontology.json`. Hand-author approximately 215 entries: 4 Classes + 16 Types + 64 Variations + 64 Elements + 8 Archetypes + 4 character-dynamics + 4 plot-dynamics + ≈ 35 concept meta-entries + 16 Quads + 75 dynamic-pair standalone entries. The exact count depends on how meta-entries deduplicate; record the final count in `notes.md`.

For the three contradictions resolved by SPEC §2.2, **NCP labels are canonical**:

- `throughline.relationship` — canonical_label `Relationship Story`; `aliases_en: ["Subjective Story", "RS", "SS"]`.
- `throughline.influence` — canonical_label `Influence Character`; `aliases_en: ["Impact Character", "IC"]`.
- `character-dynamic.problem-solving-style` — canonical_label `Problem-solving Style`; `aliases_en: ["Mental Sex"]`; `deprecated_aliases_en: ["Male/Female problem-solving"]`.

The seven concept entries inside `elements.md` (Crucial Element, MC Problem, OS Problem / Response / Solution / Symptom, Symptom Element) MUST be authored with `kind: concept`, NOT `kind: element` (per OQ-B + SPEC R.3.3.2).

`provenance` MUST match the host file's documented status (16 source / 6 extension, per `synthesis/inventory.md`).

### Step 5 — Insert per-term frontmatter

Build the helper `tools/dramatica-nav/ontology-build.py --bootstrap` (Step 9 implements the full script; the bootstrap mode is callable on its own). Run it once to walk every `## <Term>` anchor in `skills/dramatica-vocabulary/references/*.md` and insert a YAML frontmatter block immediately after the heading, copying the matching `ontology.json` entry minus the table-only fields.

The Type-bucket files retain their existing prose; the bootstrap touches only the heading-to-first-content boundary. Verify via `git diff --stat` that no prose lines change. If any prose line changes, the bootstrap script is broken — stop, fix, re-run.

### Step 6 — Tag scenarios on the top-≥40 terms

For each of the eleven scenarios, set `scenarios: [<id>, ...]` on the candidate terms identified by `synthesis/scenario-survey.md`. Cap at 8 scenarios per term (schema-enforced). After tagging:

1. Rebuild `ontology.json` via `ontology-build.py` so the table mirrors the per-term frontmatter.
2. Compute the median scenario count across tagged terms; record in `notes.md`.
3. **If median > 5**, the M01 contingency from `reflection/M01-falsification.md` activates:
   - Add `tools/dramatica-nav/scenario-index.py` (≈ 80 lines, builds `scenario-index.json` from frontmatter).
   - Modify `nav.py by-scenario` to read the index instead of walking files.
   - Document the contingency activation in `notes.md`.

### Step 7 — Theory-chunk frontmatter

Add `type: theory-chunk` frontmatter to each of `skills/dramatica-theory/references/*.md` (15 chapters). Each block lists `covers_ontology_ids` (wildcards permitted: `class.*`, `type.*`, etc.) and `serves_scenarios`. Validate against `theory-chunk.schema.json`.

### Step 8 — Implement the navigator scripts

`tools/dramatica-nav/`:

- `nav.py` — CLI with subcommands `by-id`, `by-alias`, `by-scenario`, `by-quad`, `by-ktad`, `by-ncp`, `by-pair`. Default output is JSON record + `term_file` pointer; `--full` inlines the prose section via `extract.py`. Per `task.md § D.1`.
- `extract.py` — given an ontology ID or `term_file` path with anchor, return the bytes between the heading and the next sibling heading. No YAML, no surrounding chapter. Per `task.md § D.2`.
- `validate.py` — five integrity checks (the four from `task.md § D.3` plus the alias-uniqueness check from SPEC R.3.6.3): Frontmatter↔ontology equality; dynamic-pair reciprocity (now including the `pair_member_a/b` ↔ `dynamic_pair_id` invariant from OQ-C); quad membership (4 members, KTAD-complete); NCP enum closure (treats *absent* `ncp_appreciation` as legal for `kind: archetype | quad | dynamic-pair | concept`); alias-uniqueness per locale.
- `ontology-build.py` — rebuild `ontology.json` from per-term frontmatter; idempotent; no reverse-direction. Per `task.md § D.4`.
- `lib/frontmatter.py`, `lib/ontology.py`, `lib/ncp_bridge.py` — shared helpers. `lib/frontmatter.py` MUST handle the flattened `aliases_<locale>` keys (OQ-A) — no special-casing of `aliases.en`-style nested forms.

Dependency footprint: stdlib + `pyyaml` + `jsonschema` (already in scope via Task 011). No new third-party packages.

### Step 9 — Smoke tests

`tools/dramatica-nav/tests/`:

- `test_nav.py` — at minimum three fixtures per subcommand; the seven Gherkin scenarios in `task.md § Acceptance Criteria` MUST each have at least one corresponding test.
- `test_extract.py` — verify `extract.py` returns the prose section without surrounding chapter; assert byte count is ≤ 2 KB for typical Element entries.
- `test_validate.py` — both passing and deliberately broken fixtures for each of the five integrity checks (so `pytest -v` shows ten validate-related test functions, five PASS and five XFAIL-style negative cases).

`pytest tools/dramatica-nav/tests/` MUST exit 0.

### Step 10 — Wire skills + verify AGENTS.md

[`AGENTS.md § Narrative Ontology`](../../AGENTS.md) already names the schemas, the navigator, and the load triggers (NO.1–NO.6) in advance — that section was authored at the start of Task 015 so every agent entering the repo sees the load contract regardless of whether they trigger a narrative skill. **Step 10 does not re-author it.** Step 10 verifies the path links resolve now that the schemas exist, and adds the *skill-specific* operational detail under each affected SKILL.md.

Edit four `SKILL.md` files in this order:

1. `skills/dramatica-vocabulary/SKILL.md` — add `## Navigator` section pointing at `tools/dramatica-nav/nav.py`. Update `## Lookup-Disziplin` to mention the navigator as the *fast path*; prose lookup remains the path for conceptual questions. Cross-link to `AGENTS.md § Narrative Ontology` for the cross-cutting load triggers.
2. `skills/dramatica-theory/SKILL.md` — add `## Navigator` section; note `extract.py` as a way to pull a single term from a 90 KB chapter. Cross-link to `AGENTS.md § Narrative Ontology`.
3. `skills/ncp-author/SKILL.md` — update `## Dramatica Integration Map` to reference ontology IDs (e.g. `nav.py by-id <id> --include-pairs`). Retain the prose delegation rules — they answer *meaning* questions; the navigator answers *lookup* questions. Cross-link to `AGENTS.md § Narrative Ontology` (NO.2 binds NCP authoring directly).
4. `skills/novel-architect/SKILL.md` — add `## Navigator-Backed Lookups` paragraph; gain a "preferred nav.py call" column in the routing matrix for pure-lookup workflow steps. Cross-link to `AGENTS.md § Narrative Ontology` (NO.3 binds Kohärenz Protokoll structural canon edits).

Then verify in `AGENTS.md § Narrative Ontology`:

- Every schema link resolves (no 404). If still 404 anywhere, that schema file is missing — go back and create it in Step 2.
- The status-note paragraph ("paths above MAY resolve to placeholders or 404") is updated to reflect that the schemas now exist (flip from forward-declaration to live state).
- The Gherkin `# anchor: NO.1.1`, `NO.2.1`, `NO.5.1` scenarios pass empirically when the navigator and the schemas are exercised on the test fixtures from Step 9.

### Step 11 — Wire CI

Add to `tools/check-governance.sh`, gated on `maintenance/schemas/narrative-ontology/ontology.json` existing (so the rest of the repo doesn't break if the narrative ontology is removed):

```bash
echo "--- [4/4] Narrative-ontology validator ---"
if [ -f "$REPO_ROOT/maintenance/schemas/narrative-ontology/ontology.json" ]; then
  if ! "$PYTHON" tools/dramatica-nav/validate.py; then
    FAIL=1
  fi
fi
```

Update `PRE_COMMIT.md` to document the new check and the failure modes (per-clause linter mapping, mirroring the `[7.0 Mechanical Enforcement Mapping]` table in `TASK.md`).

### Step 12 — Token-cost benchmark

For ten queries (3 Anna, 3 Otto, 4 storyform-validation), measure bytes loaded via prose-only path vs. navigator path. Record results in `notes.md § Token-Cost Benchmark`. Acceptance threshold: **≥ 60% reduction on lookup-shaped queries**; conceptual queries that legitimately need the prose are exempt.

If any lookup-shaped query falls below 60%, the design needs investigation before closure — either the per-term frontmatter is too verbose (add an extract step), or the prose-only baseline was over-counted (re-measure). Do not paper over.

### Step 13 — Promote the prompt

This file (`/prompts/integrate-dramatica-ncp-skills/prompt.md`) was promoted from `status: draft` to `status: active` as part of the prompt authoring step. No further status flip is required by Step 13; the step is a sentinel that the prompt body and the implementation match.

### Step 14 — Synthesis-phase research

Re-execute against the new artefacts. Append a synthesis pass to `/research/integrate-dramatica-ncp-skills/`:

- New `synthesis/post-impl-acceptance.md` recording which Gherkin scenarios from `task.md` pass / fail empirically.
- New `reflection/M03-pre-mortem.md` — re-run the pre-mortem now that the design is concrete; record what *actually* failed (likely-but-not-yet-failed items in `task.md`'s pre-work pre-mortem).
- Update `synthesis/state.md` and `output/SPEC.md`'s `research_phase: kickoff` → `synthesis`.

### Step 15 — Friction log + closing

When all acceptance scenarios pass: write `tasks/015-integrate-dramatica-ncp-skills/friction-log.md` per `FRUSTRATED.md`, flip `task_status` to `done`, run `tools/check-governance.sh` to confirm exit 0, and invoke `/sc:createPR` per `AGENTS.md § Closing Run Procedure`.

## E — Expectations

The following files MUST exist and be staged on completion:

| Path | Purpose |
|---|---|
| `/maintenance/schemas/narrative-ontology/ontology.schema.json` | Ontology entry contract. |
| `/maintenance/schemas/narrative-ontology/scenarios.schema.json` | Scenario entry contract. |
| `/maintenance/schemas/narrative-ontology/term-frontmatter.schema.json` | Per-term YAML contract. |
| `/maintenance/schemas/narrative-ontology/theory-chunk.schema.json` | Theory-chapter YAML contract. |
| `/maintenance/schemas/narrative-ontology/ontology.json` | Canonical entry table (~215 entries). |
| `/maintenance/schemas/narrative-ontology/scenarios.json` | 11-entry scenario table. |
| `/maintenance/schemas/narrative-ontology/readme.md` | Reader's guide + OQ-A/B/C statement. |
| `/skills/dramatica-vocabulary/references/*.md` | All 22 files now carry per-term frontmatter (310 blocks); no prose lines changed. |
| `/skills/dramatica-theory/references/*.md` | All 15 chapters now carry theory-chunk frontmatter. |
| `/tools/dramatica-nav/{nav,extract,validate,ontology-build}.py` | The four navigator scripts. |
| `/tools/dramatica-nav/lib/{frontmatter,ontology,ncp_bridge}.py` | Shared helpers. |
| `/tools/dramatica-nav/tests/` | Pytest-clean. |
| `/tools/check-governance.sh`, `/PRE_COMMIT.md` | Wired to invoke `validate.py`. |
| `/skills/{dramatica-theory,dramatica-vocabulary,ncp-author,novel-architect}/SKILL.md` | Navigator wiring sections. |
| `/tasks/015-integrate-dramatica-ncp-skills/notes.md` | ReAct trace + benchmark + cross-check. |
| `/tasks/015-integrate-dramatica-ncp-skills/friction-log.md` | FL declaration. |
| `/research/integrate-dramatica-ncp-skills/` | Synthesis-phase artefacts appended. |

The seven Gherkin acceptance scenarios in `task.md § Acceptance Criteria (Gherkin)` MUST all pass. The token-cost benchmark in Step 12 MUST hit ≥ 60% reduction on lookup queries.

## N — Narrowing (Out of Scope)

The executor MUST NOT do any of the following in this run. They are out of scope and any drift toward them is a reason to stop and ask.

1. **MUST NOT** rewrite Dramatica theory prose. The schemas are *about* Dramatica; they do not redefine it. New theoretical claims belong in upstream Dramatica publications, not in this ontology.
2. **MUST NOT** coin new NCP enum values. The NCP project owns its enums; this prompt produces a *one-way* mapping from Dramatica IDs to NCP strings.
3. **MUST NOT** modify `skills/ncp-author/upstream/`. The pinned upstream snapshot is the source of truth for the NCP enum list; if the upstream needs a change, that is a separate Task that updates the pin.
4. **MUST NOT** refactor `novel-architect`'s NCP canon file (`references/canon/kohaerenz-protokoll.ncp.json`). Project-state lives there and is governed by `novel-architect`'s own iteration discipline.
5. **MUST NOT** introduce dependencies outside stdlib + `pyyaml` + `jsonschema`.
6. **MUST NOT** redistribute Dramatica source prose into ontology entries. The license bar is documented in `task.md § Pre-Work § Adversarial Query Expansion (M13)`. Per-term descriptions, where authored, MUST be original.
7. **MUST NOT** expand the scenario list past the eleven in `scenarios.json` v0.1. Additions go through the documented proposal procedure as a separate change.
8. **MUST NOT** re-open OQ-A, OQ-B, or OQ-C. They are resolved above; the resolutions are binding.
9. **MUST NOT** skip the token-cost benchmark in Step 12. It is the falsifiable proof that the navigator earned its keep; without it the deliverable is a feature without evidence.
10. **MUST NOT** invoke `/sc:createPR` if `tools/check-governance.sh` exits non-zero, per `AGENTS.md § Closing Run Procedure CR.3`.

## Constraints

1. **MUST** target JSON Schema Draft 2020-12 unless a hard validator incompatibility forces an older draft (record decision in `notes.md`).
2. **MUST** keep each schema file under 200 lines; if exceeded, factor.
3. **MUST** preserve byte-equivalence of skill prose lines after Step 5 — only frontmatter blocks are inserted; prose is not touched.
4. **MUST** declare an FL value in `friction-log.md` even at FL0 (per `FRUSTRATED.md`).
5. **MUST** validate `ontology.json` against `ontology.schema.json` after every regeneration; the build script is idempotent.
6. **MUST** preserve ReAct discipline: every non-trivial action gets a Reason→Act→Observe entry in `notes.md § ReAct Trace` so the audit graph is reconstructible.
7. **SHOULD** consult `dramatica-theory` and `dramatica-vocabulary` for *meaning* questions during authoring; **MUST NOT** delegate *schema* decisions to them — they are the consumer, not the architect, of the ontology.
8. **MUST** complete in a single coordinated run unless explicitly paused by the user (the schemas, the ontology, and the navigator are mutually dependent — partial states leak inconsistency).

## Closing

The deliverable is not "an ontology"; it is **a working contract between four skills that previously could not call each other**. The schemas are necessary; the navigator is what makes the contract callable; the per-term frontmatter is what makes the navigator cheap; the persona scenarios are what makes any of it answer real questions. The success measure is the ≥ 60% token reduction on the ten benchmark queries — everything else in this prompt is in service of that measurement.
