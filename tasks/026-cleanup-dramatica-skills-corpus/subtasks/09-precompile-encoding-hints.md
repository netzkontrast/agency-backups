---
type: note
status: draft
slug: task-026-st9-precompile-encoding-hints
summary: "Subtask ST-9: ship tools/dramatica-nav/precompile.py + emit one JSON per persona scenario under maintenance/schemas/narrative-ontology/precompiled/. Token cost for a typical scenario query MUST drop ≥40% vs. the prose path."
created: 2026-05-05
updated: 2026-05-05
subtask_id: "ST-9"
subtask_phase: "C"
subtask_recommended_agent: "python-expert"
subtask_depends_on:
  - "ST-1"
  - "ST-2"
  - "ST-3"
  - "ST-4"
  - "ST-5"
  - "ST-6"
  - "ST-7"
  - "ST-8"
subtask_falsification: "Wrong cut iff the precompiled payloads turn out to be redundant with calling nav.py by-scenario directly. Mitigated by a token-cost benchmark — if the precompiled path doesn't beat nav.py by ≥40%, the artefacts are deleted and the task closes without §Goal item 4."
---

# ST-9: Precompile Persona-Scenario Encoding Hints

## Goal

Two coupled deliverables:

1. **`tools/dramatica-nav/precompile.py`** — a CLI that reads the post-ST-8 ontology and emits one structured JSON per persona scenario.

   ```text
   tools/dramatica-nav/precompile.py emit-all                  # writes one JSON per scenario in scenarios.json
   tools/dramatica-nav/precompile.py emit --scenario <id>      # writes one JSON for a single scenario
   tools/dramatica-nav/precompile.py validate                  # validates emitted JSONs against precompiled.schema.json
   tools/dramatica-nav/precompile.py benchmark --query <id>    # measures token cost vs. nav.py by-scenario for the same query
   ```

2. **`maintenance/schemas/narrative-ontology/precompiled/<scenario-id>.json`** — eleven JSON artefacts (one per persona scenario), each carrying:

   ```json
   {
     "schema_version": "0.1",
     "scenario_id": "novel.crucial-element-audit",
     "scenario_summary": "...",
     "persona": "novel-author",
     "generated_from_ontology_version": "0.2",
     "generated_at": "2026-05-05",
     "primary_terms": [
       {
         "id": "el.trust",
         "canonical_label": "Trust",
         "kind": "element",
         "dynamic_pair_id": "el.test",
         "quad_id": "quad.effect-cause-el",
         "ktad_position": "A",
         "encoding_hint": "Use Trust ↔ Test as the dramatic axis when MC's Crucial Element is the giving-up-of-trust...",
         "ncp_appreciation": null,
         "term_file": "skills/dramatica-vocabulary/references/elements.md#trust"
       },
       ...
     ],
     "primary_quads": [...],
     "primary_pairs": [...],
     "consumer_hints": {
       "novel-architect": "Load this file when answering novel.crucial-element-audit queries; cite by ID, not label.",
       "ncp-author": "The ncp_appreciation field maps to NCP enum 'Influence Character Problem' (or null if absent)."
     }
   }
   ```

3. **`maintenance/schemas/narrative-ontology/precompiled.schema.json`** — JSON Schema (Draft 2020-12) validating each precompiled file. The `encoding_hint` field is OPTIONAL but RECOMMENDED; when present, it carries a one-paragraph encoding-suggestion synthesised from the term's prose section. Schema MUST follow the same structural conventions as the existing four narrative-ontology schemas (no nested objects beyond depth 1 per [AGENTS.md](../../../AGENTS.md), `additionalProperties: false`).

**Token-cost benchmark mandate.** For each of the 11 scenarios, measure:

- bytes loaded by `nav.py by-scenario <id>` + the prose extracts the agent reads to answer the query
- bytes loaded by reading the precompiled JSON directly

The precompiled path MUST consume ≤60% of the prose path on average. If not, the artefacts are deleted and §Goal item 4 of [task.md](../task.md) closes without the precompiled layer.

## Falsification

Wrong cut **iff** the precompiled payloads turn out to be redundant with calling `nav.py by-scenario <id>` directly. Mitigation: ST-9's `benchmark` subcommand does the token-cost measurement explicitly. If precompiled doesn't beat nav.py by ≥40%, the artefacts are deleted in the same commit and the task's §Goal item 4 is documented as "investigated; not landed; ratification deferred to Task 027".

## Inputs

- `maintenance/schemas/narrative-ontology/ontology.json` — read-only source.
- `maintenance/schemas/narrative-ontology/scenarios.json` — read-only source (the 11 scenarios).
- `tools/dramatica-nav/lib/ontology.py` — reuse load/index helpers.
- `tools/dramatica-nav/extract.py` — reuse for prose extraction when synthesising encoding_hint.
- `skills/dramatica-vocabulary/references/encoding-patterns.md` — read-only consultation for encoding-hint heuristics.

## Acceptance Criteria

1. **CLI complete.** All four subcommands (`emit-all`, `emit`, `validate`, `benchmark`) work as documented.
2. **11 JSON files emitted.** One per scenario under `maintenance/schemas/narrative-ontology/precompiled/`. Each passes `precompiled.schema.json`.
3. **Schema authored.** `maintenance/schemas/narrative-ontology/precompiled.schema.json` exists and is referenced from [`maintenance/schemas/narrative-ontology/readme.md`](../../../maintenance/schemas/narrative-ontology/readme.md).
4. **Idempotent.** Running `precompile.py emit-all` twice produces a byte-identical filesystem state.
5. **Benchmark passes.** Token-cost benchmark shows precompiled path ≤60% of prose path on average across all 11 scenarios. Per-scenario results recorded in `tasks/026-cleanup-dramatica-skills-corpus/notes.md §10` (a new section).
6. **Tests.** `tools/dramatica-nav/tests/test_precompile.py` covers schema validation, idempotency, benchmark sanity (≥4 tests).
7. **No new ontology-surface amendment.** [AGENTS.md § Narrative Ontology](../../../AGENTS.md) is NOT modified — the load-trigger amendment is deferred to a Task-027 follow-up. ST-9 emits the artefacts; consumers don't load them yet (per FE-10 in [notes.md §3](../notes.md)).
8. **Single commit.** Title: `feat(dramatica-nav): precompile persona-scenario encoding hints (Task 026 ST-9)`.

## Dependencies

All Phase A + Phase B subtasks must merge first. Plus ST-8's scenario-tag coverage (without it, the precompiled payloads would be empty for under-tagged scenarios).

## Estimated Effort

Medium (~250 LOC tool + ~150 LOC tests + 11 JSON artefacts emitted by the tool itself).

## Agent Prompt

```text
You are implementing ST-9 of Task 026 (cleanup-dramatica-skills-corpus) for
the netzkontrast/agency repo on branch claude/cleanup-dramatica-skills-1cEOO.

This subtask runs in worktree isolation.

Repo root: /home/user/agency
Working directory: /home/user/agency

Context files (read first):
  - tasks/026-cleanup-dramatica-skills-corpus/task.md
  - tasks/026-cleanup-dramatica-skills-corpus/subtasks/09-precompile-encoding-hints.md (this file)
  - maintenance/schemas/narrative-ontology/ontology.json (post-ST-8 source)
  - maintenance/schemas/narrative-ontology/scenarios.json
  - skills/dramatica-vocabulary/references/encoding-patterns.md (read-only consultation)
  - tools/dramatica-nav/lib/ontology.py (reuse helpers)
  - tools/dramatica-nav/extract.py (reuse for prose extraction)

Goal:
  Ship tools/dramatica-nav/precompile.py + emit 11 JSON artefacts under
  maintenance/schemas/narrative-ontology/precompiled/. Author the schema.
  Run the token-cost benchmark; precompiled path MUST consume ≤60% of
  prose path on average.

Acceptance criteria (reproduce verbatim from this file's Acceptance Criteria
section). All eight must be true.

Implementation approach:
  1. Author the schema first: precompiled.schema.json (Draft 2020-12).
     Lock the structure: scenario_id, persona, primary_terms[],
     primary_quads[], primary_pairs[], consumer_hints. No nesting beyond
     depth 1 within array items.
  2. Implement precompile.py:
     - emit-all: walks scenarios.json; for each scenario, walks
       ontology.json finding entries tagged with that scenario; emits
       a structured JSON.
     - The encoding_hint per term is synthesised from extract.py's prose
       output: take the first ≤2 sentences AFTER any opening definition
       paragraph. If extract returns nothing usable, leave encoding_hint
       null and surface as a "needs-prose" warning.
     - emit (single scenario): same as emit-all but for one ID.
     - validate: jsonschema check on every emitted file.
     - benchmark: for each scenario, measures bytes by both paths.
       Emits a markdown table to stdout AND appends to notes.md §10.
  3. Author tests/test_precompile.py.
  4. Run all gates.
  5. If benchmark fails (precompiled path > 60% of prose path average),
     DELETE the precompiled/ directory and document the closure in
     notes.md §10 + the commit body.
  6. Commit one focused commit; do NOT push.

Constraints:
  - Python 3.11 stdlib + jsonschema only.
  - DO NOT modify AGENTS.md, ontology.schema.json, term-frontmatter.schema.json,
    or any of the four existing narrative-ontology schemas.
  - DO NOT add encoding hints that quote >1 line of source prose.
  - The encoding_hint field is OPTIONAL; null is a valid value when prose
    extraction yields nothing usable.
  - The benchmark gate is binding. Failure means the artefacts are
    deleted, not landed.

When done:
  - pytest tools/dramatica-nav/tests/                                       (must pass)
  - python3 tools/dramatica-nav/precompile.py emit-all                      (must succeed)
  - ls maintenance/schemas/narrative-ontology/precompiled/                  (must show 11 *.json files)
  - python3 tools/dramatica-nav/precompile.py validate                      (must succeed)
  - python3 tools/dramatica-nav/precompile.py benchmark --query novel.crucial-element-audit
                                                                              (must show precompiled ≤60% of prose path)
  - cat tasks/026-cleanup-dramatica-skills-corpus/notes.md | grep -A3 "§10" (must show benchmark table)
  - Commit "feat(dramatica-nav): precompile persona-scenario encoding hints (Task 026 ST-9)"
  - Do NOT push.
```
