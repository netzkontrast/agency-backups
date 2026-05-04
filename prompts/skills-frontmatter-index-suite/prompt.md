---
type: prompt
status: active
slug: skills-frontmatter-index-suite
summary: "Survey existing OSS frontmatter indexers, then design and implement a token-efficient frontmatter index + skills tool suite that lets Claude Code, Jules, and Gemini navigate /skills/ without opening file bodies."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: skills-frontmatter-index-suite
prompt_spawned_from_research: token-efficiency-tool-suite
---

# Skills Frontmatter Index & Tool Suite — Research Proposal + Build

## Framework

**RISEN + ReAct.** The work has two phases. Phase 1 is a short evidence pass (do *any* OSS tools already do this? Obsidian Dataview, Astro content collections, MkDocs, vault-toolbox, frontmatter-cli — survey them) — RISEN structure with ReAct loops on each candidate. Phase 2 is the implementation tranche (build / wire / benchmark) — pure RISEN.

---

## § RFC 2119

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

---

## R — Role

You are a tool-suite architect operating under the four-stage **Token-Estimator → Context-Pruner → Budget-Enforcer → Schema-Validator** architecture defined in `research/token-efficiency-tool-suite/output/SPEC.md`. Your scope is the second stage (Context-Pruner): you build the structural mechanism that lets agents avoid loading the bodies of files whose summaries already answer the question.

## I — Input

The executor MUST read:

1. `/tasks/010-skills-frontmatter-index-suite/task.md` — the binding plan.
2. `/research/token-efficiency-tool-suite/output/SPEC.md` — architectural source. Especially §4 (Surviving Architecture) and §5 (Normative Specification).
3. `/TASK.md §3` and `/PROMPT.md §3` — the L1+L2 frontmatter contract this index parses.
4. `/tools/validate-frontmatter.py` — the existing parser whose semantics MUST be reproduced.
5. `/skills/skills-skill-bootstrap/sync.sh` — the script the manifest-generator MUST integrate with.
6. `/skills/readme.md` and a sample of three SKILL.md files (`pdf-to-markdown`, `prompt-optimizer`, `the-agency-system-architect`) so the index shape is grounded in real frontmatter.
7. `/SKILLS.md` once Task 009 lands (this prompt MUST detect whether SKILLS.md exists; if not, the executor MUST treat the `skill_*` namespace as proposed-not-ratified and tag affected entries `schema_pending: true`).

## S — Steps

### Step 1 — Phase 1: OSS landscape pass

The executor MUST survey at least five existing OSS tools that index Markdown frontmatter. Suggested seeds: Obsidian Dataview, Obsidian Templater, Astro `getCollection`, MkDocs Material `meta` plugin, Hugo `front-matter` API, and `frontmatter-cli` (npm). For each:

- Note the schema shape (flat JSON? Lucene-style? GraphQL?).
- Note the parse cost (full file read or YAML-only?).
- Note the cross-platform feasibility (Node-only is a no-go; Python is mandatory because `tools/check-governance.sh` is a bash+python pipeline).

The executor MUST record the survey in `notes.md` (under the task folder) and pick one of three outcomes:

- **Reuse** — Vendor an existing library that fits.
- **Adapt** — Take the schema of an existing library, reimplement in Python.
- **Author** — Build from scratch (the default if no library survives the survey).

ReAct loop: for each candidate, Thought ("could this fit?"), Action (read its README, check the schema), Observation (record outcome).

### Step 2 — Phase 2a: Author `tools/build-frontmatter-index.py`

Output JSON shape exactly as specified in `tasks/010-skills-frontmatter-index-suite/task.md` §Plan step 2. Determinism is REQUIRED: the same input tree MUST produce a byte-identical JSON file on every machine. Use sorted keys, no timestamps inside individual entries (only at top level), and ASCII-safe encoding.

The walker MUST honour the same file-targeting rules as `tools/validate-frontmatter.py`:

- `/tasks/<NNN>-<slug>/task.md` → schema `task`
- `/prompts/<slug>/prompt.md` → schema `prompt`
- `/research/<slug>/output/SPEC.md` and `readme.md` → schema `research`
- `/skills/<slug>/SKILL.md` → schema `skill`
- All `readme.md` in operational folders → schema `index`

### Step 3 — Phase 2b: Author `tools/query-frontmatter-index.py`

Implement all ten canonical commands from `tasks/010-skills-frontmatter-index-suite/task.md` §Plan step 3. Each command MUST default to ≤ 1 KB of output; pagination flag `--limit N` may extend.

Constraints on the CLI:

1. The CLI MUST exit 0 when the answer set is empty (with a one-line `(no results)` message).
2. The CLI MUST exit 1 only on parse / lookup failures, never on empty results.
3. The CLI MUST NOT open file bodies. If a command's output requires a file body (only `query header <slug> <header>`), the slice MUST be guided by the headers ontology (Task 011) and limited to the named header's contents.

### Step 4 — Phase 2c: Author `tools/skills-manifest.py`

Subset of the index, scoped to `/skills/`. Output written to `$AGENCY_SKILLS_ROOT/.skills-manifest.json`. The manifest entries MUST be a strict subset of the index entries (same shape, fewer rows). Acceptance test: `query manifest` from the index CLI produces output byte-identical to the manifest file.

### Step 5 — Wire pre-commit drift detection

Append to `tools/check-governance.sh` a step that:

1. Runs `python3 tools/build-frontmatter-index.py --target /tmp/agency-index.json`.
2. Compares against `.agent_cache/frontmatter-index.json`.
3. Exits non-zero if they differ and the staged set does not include the updated index.

The agent MUST update `MAINTENANCE.md` with the new gate description.

### Step 6 — Token-efficiency benchmark

For each of the ten canonical CLI questions, the executor MUST measure and record in `friction-log.md`:

- `tokens_via_index`: tokens in the CLI output (use `tiktoken` or a fixed approximation: 4 chars ≈ 1 token).
- `tokens_via_bodies`: tokens that would have been read by the naive alternative (full body of every file the agent would otherwise have opened).
- `speedup`: ratio.

Acceptance: average speedup ≥ 8x; minimum (worst-case) speedup ≥ 4x. Below 4x → redesign that entry's shape.

### Step 7 — Final lint sweep

`tools/check-governance.sh` MUST exit 0 with the new gate active. The executor MUST NOT commit a tree where the rebuild produces a diff against the staged index.

## E — Expectations

The following files MUST exist and be staged on completion:

| Path | Purpose |
|---|---|
| `/tools/build-frontmatter-index.py` | Index builder. |
| `/tools/query-frontmatter-index.py` | Query CLI. |
| `/tools/skills-manifest.py` | Manifest emitter. |
| `/tools/check-governance.sh` | Updated with the index-drift gate. |
| `/skills/skills-skill-bootstrap/sync.sh` | Updated to call the manifest emitter after sync. |
| `/.agent_cache/frontmatter-index.json` | The current index. |
| `/.gitignore` | Confirm `.agent_cache/` policy: tracked or ignored, decision logged in `notes.md`. |
| `/tasks/010-skills-frontmatter-index-suite/notes.md` | Phase-1 survey + benchmark table + decision log. |
| `/tasks/010-skills-frontmatter-index-suite/friction-log.md` | FL declaration + benchmark results. |

## Constraints

1. **MUST NOT** require dependencies outside the existing `pyproject.toml`. The validator already runs on stdlib + `pyyaml`-shaped manual parsing; the index MUST hold to the same baseline.
2. **MUST NOT** read file bodies during indexing. Only YAML frontmatter and the list of `## H2` lines (for the headers list) are inspected.
3. **MUST** be deterministic across machines. Sorted keys, locale-independent ordering, ASCII-safe.
4. **MUST** integrate with the proposed `$AGENCY_SKILLS_ROOT` path, but MUST NOT fail if the variable is unset (fall back to `git rev-parse --show-toplevel`).
5. **MUST** declare an FL value in the friction log per `FRUSTRATED.md`.
6. **SHOULD** keep total tool-suite Python source under 800 lines combined. Small surface, readable code.
