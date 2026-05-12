---
type: task
status: active
slug: skills-frontmatter-index-suite
summary: "Design and implement a token-efficient frontmatter index + tool suite that lets Claude Code, Jules, and Gemini agents navigate /skills/ (and the rest of the repo) without opening file bodies."
created: 2026-05-04
updated: 2026-05-05
task_id: "010"
task_owner: "claude-code"
task_status: updated
task_priority: P1
task_uses_prompts:
  - skills-frontmatter-index-suite
task_spawns_research:
  - skills-frontmatter-index-suite
task_spawns_prompts: []
task_superseded_by:
  - "022"
task_affects_paths:
  - tools/build-frontmatter-index.py
  - tools/query-frontmatter-index.py
  - tools/skills-manifest.py
  - tools/check-governance.sh
  - .agent_cache/frontmatter-index.json
  - skills/skills-skill-bootstrap/sync.sh
  - SKILLS.md
---

# Task 010 — Skills Tool Suite & Frontmatter Index

## Goal

Build the tool suite that turns `/skills/` (and every other operational markdown folder) into a *queryable database* without forcing agents to open file bodies. The Task is `done` when:

1. A `tools/build-frontmatter-index.py` walks the repository, parses the L1 + L2 frontmatter of every operational markdown file, and emits a deterministic JSON index at `.agent_cache/frontmatter-index.json` (per `TASK.md §3.4`, L3 metadata lives in sidecar files, not in YAML).
2. A `tools/query-frontmatter-index.py` exposes a CLI that lets any agent answer ten canonical questions in O(index-size) without opening file bodies — full list in §Plan.
3. The `skills-skill-bootstrap` sync.sh emits a `.skills-manifest.json` (per the proposed `SKILLS.md §B.3`) so agents bootstrapping into a fresh workspace have an instant routing table.
4. Both tools integrate with `tools/check-governance.sh` so the index stays current: a pre-commit run rebuilds the index and fails if the rebuild produces a diff that was not staged.
5. A measured token-efficiency claim is recorded: "answering question Qn via index costs ≤ K tokens; answering it by opening file bodies costs ≥ M tokens; speedup factor = M/K." This claim is verified for the ten canonical questions and logged in `friction-log.md`.

The Task explicitly inherits the **Token-Estimator → Context-Pruner → Budget-Enforcer → Schema-Validator** four-stage architecture from `research/token-efficiency-tool-suite/output/SPEC.md`. The frontmatter index *is* a Context-Pruner: it is the structural mechanism that lets agents avoid loading 60+ KB of skill bodies when they only need the description of one skill.

## Background — Why This Task Exists

1. **Skill bodies are large but agents rarely need the full body.** The 14 skills in `/skills/` total ~280 KB. A typical agent question — "which skill handles PDF conversion?" — is answered by 200 chars of one skill's `description` field. Today the agent reads the whole `skills/readme.md` (5.7 KB) and sometimes opens `pdf-to-markdown/SKILL.md` (~2 KB) just to confirm. With an index it reads ~80 chars.
2. **Frontmatter is already the de-facto routing surface.** `TASK.md §3` (Layered Schema with Namespacing) and `AGENTS.md § Frontmatter Ontology Summary` mandate that the agent SHOULD read `summary` before opening the body. Without an index, "read summary first" is enforceable on a single file but not across the repo.
3. **Jules and Gemini lack the IDE-side helpers Claude Code has.** Claude Code's Explore subagent and `Grep` tool partly compensate for the lack of an index; Jules (asynchronous, cloud-isolated) and Gemini (no filesystem in the Deep Research surface) cannot. A stable JSON index is the cross-agent equivalent.
4. **Skill-to-skill linkage is mechanically unenforceable today.** The proposed `SKILLS.md §X.2` ("every reference MUST resolve at lint time") cannot be implemented without an index: reciprocity requires looking up the referenced skill's frontmatter, which is what an index makes cheap.
5. **The token-efficiency-tool-suite SPEC has no implementation.** Task 002 produced a spec, not code. This task is its first implementation tranche, scoped to the index/manifest layer (Context-Pruner stage of the four-stage pipeline). The remaining three stages (Token-Estimator, Budget-Enforcer, Schema-Validator) are out of scope for this Task and should be filed as follow-ups.

## Plan

1. **Survey the corpus.** Walk the repo with `tools/build-frontmatter-index.py --dry-run` and count: total operational markdown files, files with L1 frontmatter, files with valid L2 namespaces, files in `/skills/` lacking the proposed `skill_*` namespace (expected: 14 — Task 009 ratifies the namespace, Task 011 ships the schemas, this task ships the index that consumes them).
2. **Author `tools/build-frontmatter-index.py`.** The output JSON shape:
   ```json
   {
     "schema_version": "1",
     "built_at": "2026-05-04T12:00:00Z",
     "built_from_sha": "abc1234",
     "entries": [
       {
         "path": "skills/pdf-to-markdown/SKILL.md",
         "type": "skill",
         "slug": "pdf-to-markdown",
         "summary": "Convert a PDF to Markdown using PyMuPDF4LLM.",
         "namespace": {
           "skill_kind": "tool",
           "skill_target_agents": ["claude-ai", "claude-code"],
           "skill_references_skills": [],
           "skill_references_research": [],
           "skill_references_prompts": [],
           "skill_bootstrap_required": true
         },
         "headers": ["What", "How to use", "References"],
         "byte_size": 1893,
         "frontmatter_sha": "9a1c…"
       },
       ...
     ],
     "graph": {
       "skill_referenced_by": { "<slug>": ["<other-slug>"] },
       "task_uses_prompts":   { "<slug>": ["<task-id>"] },
       "research_executes_prompt": { "<slug>": "<prompt-slug>" }
     }
   }
   ```
   The `graph` block is computed from the entries; reciprocity links (`skill_referenced_by`) are derived, not authored.
3. **Author `tools/query-frontmatter-index.py`.** CLI surface — every command MUST return ≤ 1 KB of text by default:
   - `query summary <slug>` — Print the L1 `summary` of a slug (skill, task, prompt, or research).
   - `query skills --kind tool` — List slugs filtered by `skill_kind`.
   - `query skills --target-agent jules` — List skills portable to Jules.
   - `query references <slug>` — List forward + reverse skill references.
   - `query orphans` — List operational files with frontmatter that does not resolve cleanly (broken links).
   - `query stale --since 30d` — List entries whose `updated` is older than 30 days.
   - `query path <slug>` — Print the absolute path for a slug; bootstrap helper.
   - `query header <slug> <header>` — Print the body of a single `##` section by name (replaces "open the whole file just to read § Goal").
   - `query graph --type task --status open` — Emit the open-tasks subgraph as a flat list.
   - `query manifest` — Emit `.skills-manifest.json` for the bootstrap consumer.
4. **Author `tools/skills-manifest.py`.** Subset of the index, scoped to `/skills/` only, emitted at bootstrap time. Contract: `sync.sh` MUST call this script after pulling skills; the manifest is the single artifact every agent reads to decide which skill to load.
5. **Wire into `tools/check-governance.sh`.** Add a step: rebuild the index, diff against the staged `.agent_cache/frontmatter-index.json`, fail commit if drift is detected. Rationale: stale indexes silently mislead Jules/Gemini, which have no fallback to body-reading.
6. **Wire into `skills/skills-skill-bootstrap/sync.sh`.** After the existing sync logic, the script MUST run `tools/skills-manifest.py --target $AGENCY_SKILLS_ROOT/.skills-manifest.json` (path canonicalized by `SKILLS.md §B.2`).
7. **Token-efficiency benchmark.** For each of the ten CLI questions in step 3, measure: tokens-via-index vs. tokens-via-bodies. Record the speedup matrix in `friction-log.md`. Acceptance threshold: average speedup ≥ 8x; if a question is < 4x, redesign the index entry shape.
8. **Run the linters.** `tools/check-governance.sh` exits 0; `validate-frontmatter.py` clean; `lint-linkage.py` resolves the new graph entries.
9. **Document Jules/Gemini integration.** A short section in `SKILLS.md §B` (delegated to Task 009) declares: "Jules and Gemini agents MUST query the index, not the file bodies, when routing skill requests." This Task delivers the artifact that statement binds against.

## Todo

- [ ] 1. Survey corpus; record current frontmatter coverage in `notes.md`.
- [ ] 2. Implement `tools/build-frontmatter-index.py` with the JSON shape above.
- [ ] 3. Implement `tools/query-frontmatter-index.py` with all ten canonical commands.
- [ ] 4. Implement `tools/skills-manifest.py` and integrate with `sync.sh`.
- [ ] 5. Wire index-rebuild into `tools/check-governance.sh` (drift-detection gate).
- [ ] 6. Run the ten-question token-efficiency benchmark; record results in `friction-log.md`.
- [ ] 7. Confirm `tools/check-governance.sh` exits 0 on the staged tree.
- [ ] 8. Set `task_status: done`, update `updated`, write `friction-log.md`.

## Links

- Executing prompt: [`/prompts/skills-frontmatter-index-suite/prompt.md`](../../prompts/skills-frontmatter-index-suite/prompt.md)
- Source spec: [`/research/token-efficiency-tool-suite/output/SPEC.md`](../../research/token-efficiency-tool-suite/output/SPEC.md)
- Depends on Task 009 (defines the `skill_*` namespace this index consumes): [`../009-author-skills-root-spec/`](../009-author-skills-root-spec/)
- Depends on Task 011 (provides the JSON schemas the index validates against): [`../011-skills-frontmatter-schema-files/`](../011-skills-frontmatter-schema-files/)
- Governing specs: [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md), [`FOLDERS.md`](../../FOLDERS.md)
