# Plan Rethink — Overview of What Should Change

> **Status.** Synthesis-driven rethink. Companion to [`synthesis-gemini-1-2.md`](./synthesis-gemini-1-2.md). The synthesis was written WITHOUT regard to existing locks; this overview maps synthesis findings ONTO the current plan to surface what should change. **No new AskUser rounds yet** — this is the pre-AskUser overview the user explicitly requested.
>
> **Reading order.** §1 (one-line thesis) → §2 (what survives) → §3-5 (what changes) → §6 (new patterns) → §7 (proposed Round-11-onward dialogue plan).

---

## 1. The one-line thesis

> The 2023–2026 literature says: **keep the four-layer separation, keep the gates, keep the DAG — but replace SemVer with content-addressed hashes, replace the central ID dispenser with UUIDv7, replace retroactive Gherkin with plan-first Gherkin, drop the theatrical rename and `notes:` escape valve, and add the missing bootstrap-budget machinery (context tiering + repo-map + description-only skills + MCP resources + subagent isolation) that closes the ~50K → ≤8K gap.**

This is good news. The architectural skeleton of the plan is correct. The locks that need to change are concentrated in three areas: **versioning/addressing**, **gate timing**, and **bootstrap mechanics**.

---

## 2. What survives (literature-validated; no change needed)

| Plan element | Validation source | Round |
|---|---|---|
| Four-layer Task / Prompt / Research / Skill separation | Anthropic Skills, Praetorian, LangGraph | R1, R7 |
| Mandatory Gherkin + JSON-Schema gate-tooling | GitHub Spec Kit, Stripe, Checkmarx | R7 |
| Explicit DAG via `task_depends_on`; topological gate evaluation; no cycles | Airflow, Snakemake | R10 Lock D |
| 8-step pre-commit governance | GitHub Spec Kit, Bitloops | (current) |
| ≤ 8K bootstrap target | Aider, Praetorian, Anthropic context engineering | R1 (now externally funded) |
| `task_phase` lifecycle as 4 states (undecomposed → decomposed | ready-to-execute → closed) | Generalises ADaPT / Plan-and-Solve | R10 Lock A/B |
| No-decomposition direct-promotion path | Plan-and-Solve, ReAct, Praetorian | R10 Lock B |
| Goal-only init (Task carries only a goal at creation) | Compatible with Plan-and-Solve; **but see §4.2 for gate-timing change** | R10 |
| `task_kind: goal` subtype, not a new top-level folder | Validated by absence of counter-evidence; idiomatic for hierarchical task systems | R6 |
| 1:N at amendment level (within a single Task's amendments) | Compatible with all orchestration literature | R9 SemVer scheme |
| ADR governance + MADR + T4-immutability of accepted ADRs | Spec-driven literature consensus | (current) |
| Frontmatter-namespaced schema (L1 Vault Core + L2 Domain) | Compatible; **but see §4.4 for compile-to-SQLite** | (current) |

**Implication.** ~60 % of the plan is ratified. Stop relitigating these.

---

## 3. What changes — REPLACE (lock is wrong; substitute named-alternative)

### 3.1 SemVer on non-code artefacts → **CalVer + content-addressed hashes**
- **Lock affected:** R9 SemVer scheme (amendment-folder naming `1.0.0`, `1.1.0`, `2.0.0`).
- **Why:** Empirical Maven/NPM studies show even compiled-code developers can't agree on "breaking"; for prose-and-data artefacts the concept is undefined. Causes "semantic divergence" — version implies stability while definition drifts silently.
- **Replacement:**
  - **Research workspaces** → CalVer (`2026-05-13` style), since they are time-bound.
  - **Task / amendment snapshots** → Git SHA / content-addressed hash for exact reproducibility.
  - **Prompt versions** → CalVer + hash for reproducibility of executed traces.
- **Cascade effect.** This is **the highest-impact change**. It also resolves:
  - Round 10 Lock C (subtask address = MCP ID + `task_parent_semver`) becomes **MCP ID + content-hash + parent-edge** (the parent-relative SemVer disappears).
  - The whole amendment-folder layout `amendments/1.1.0-validator/` becomes `amendments/<calver>-<hash>-validator/` or similar.

### 3.2 Centralised MCP ID dispenser → **UUIDv7 (RFC 9562) or ULID, locally generated**
- **Lock affected:** R6 / R10 Lock C (every Task / subtask is dispensed by an MCP service).
- **Why:** Network round-trip on every artefact creation is slow and brittle. Single point of failure. RFC 9562 (UUIDv7) is the standard for this exact problem since 2024.
- **Replacement:** Agents generate UUIDv7 IDs locally. Time-sortable, collision-free, no coordination. The MCP service is deprecated entirely.
- **Cascade effect.** Round 1 goal "parallel-work numbering collision" is solved trivially: UUIDv7 cannot collide across parallel branches by construction.

### 3.3 Theatrical rename (`enactments/`, `witness/`) → **drop entirely**
- **Lock affected:** R8 / R9 rename-direction lock.
- **Why:** Violates DDD ubiquitous language; breaks `grep` ergonomics; imposes cognitive load; no engineering benefit.
- **Replacement:** Keep `tasks/`, `prompts/`, `research/`, `skills/`. Done.

### 3.4 `notes:` escape-valve string field → **explicit schema-upgrade Task subtype**
- **Lock affected:** R9 "Reserved `notes:` field per schema".
- **Why:** EAV anti-pattern; agents will dump malformed JSON to bypass linters; proximate cause of tool-argument rot in production.
- **Replacement:** Remove `notes:` from every schema. Introduce a first-class `task_kind: schema-upgrade` subtype that opens a PR against the JSON Schema itself when an agent encounters a real schema gap. Makes schema evolution traceable instead of invisible.

---

## 4. What changes — REVISE (lock is partially wrong; adjust mechanism)

### 4.1 Strict 1:1:1 main-level cardinality → **1:N main-level** (one Task → many Prompts → fragmented Research)
- **Lock affected:** R7 closed-question 1 ("1 Task : 1 Prompt : 1 Research at main level").
- **Why:** Real orchestration fans out — planner prompt, researcher prompt, synthesiser prompt — each producing distinct artefacts. Forcing 1:1:1 produces prompt spaghetti.
- **Revised lock:** Drop the strict 1:1:1 main-level pairing. Adopt **1:N at main level** (one Task → N Prompts where N ≥ 1). Keep 1:1:1 at amendment level if needed for audit clarity.
- **Cascade.** Prompt-folder schema gets a `prompt_role` field: `{planner, researcher, executor, synthesiser, validator}`. Research workspaces get a `research_produced_by_prompt: <hash>` edge.

### 4.2 Retroactive Gherkin (synthesis writes parent Gherkin AFTER decomposition) → **plan-first Gherkin (planner agent writes and freezes Gherkin BEFORE execution)**
- **Lock affected:** R10 Lock A.
- **Why:** Retroactive criteria introduces hindsight bias; the agent who wrote the output also writes the test, guaranteeing 100 % pass. Tests must be deterministic exit gates.
- **Revised lock:** The decomposition agent (planner prompt) writes the subtask Gherkin AND the parent's derived Gherkin (`Given <goal>, When all subtasks PASS their gates, Then …`) DURING decomposition, not after. Linter enforces phase-conditional: `Gherkin REQUIRED iff task_phase ∈ {decomposed, ready-to-execute}` — same rule as Lock A, just the *write-time* moves earlier.
- **Optional strengthening (open question):** require a separate "Gherkin reviewer" subagent or human gate between planner output and executor start. The literature is split.

### 4.3 Subtask address = MCP ID + parent-relative SemVer → **UUIDv7 + flat parent edge (DAG-only)**
- **Lock affected:** R10 Lock C.
- **Why:** Subsumed by §3.1 + §3.2. Once SemVer is dropped and UUIDv7 is adopted, the dual-address scheme collapses naturally.
- **Revised lock:** Subtask carries `task_id: <uuidv7>`, `task_parent: <uuidv7>`, and `task_depends_on: [<uuidv7>, …]`. No SemVer coordinate. Hierarchy is reconstructed from the parent-edge graph; no special folder-name encoding.
- **Side-effect.** Amendment folders drop SemVer in the name. Use `amendments/<calver>-<short-hash>-<slug>/` or even just `amendments/<uuidv7>-<slug>/`.

### 4.4 Frontmatter-only audit graph → **frontmatter declaration + compiled SQLite index at pre-commit**
- **Lock affected:** Implicit in "frontmatter-only audit graph; no body links".
- **Why:** Flat-file YAML graphs hit silent link-rot at ~10K artefacts; Logseq forced to migrate to SQLite for exactly this reason.
- **Revised lock:** Frontmatter remains the human-readable declaration. Pre-commit step (new linter `tools/fm/compile_graph.py`) compiles all frontmatter into `.agent_cache/graph.sqlite` (gitignored). Cross-layer queries run against the SQLite, not against grep. The compiled graph also enforces referential integrity — orphan `task_uses_prompts: <id>` pointing to nonexistent prompt fails pre-commit.
- **Cascade.** The 8-step pre-commit gate gains a 9th step. Frontmatter authoring tools (`tools/fm/edit.py`) are unaffected.

---

## 5. What changes — DEFER (lock that may need to change, but not now)

### 5.1 Move from pre-commit governance to runtime MCP-validation tools
- **Why deferred:** Brief #2's meta-question. Migrating governance to runtime would close the bootstrap gap definitively (the schemas wouldn't need to be in context) but **changes the substrate's identity** from "file-based + git-verifiable" to "service-based + runtime-validated".
- **Defer to:** A future Major-version rethink after Tiers 1–3 of the bootstrap-reduction roadmap (see §6) are shipped and measured.

### 5.2 Move from markdown+frontmatter to graph-database (Neo4j) backing
- **Why deferred:** Same identity question. Would solve referential integrity at scale but breaks the git-as-authoritative-store premise.
- **Defer to:** Same future Major-version rethink.

---

## 6. What gets added — NEW patterns the current plan does not have

The current plan has no mechanism for closing the bootstrap-budget gap. Brief #2 supplies the named patterns. Adopt in three independently-shippable tiers.

### 6.1 Tier 1 — within ~1 week, no architecture changes (~50K → ~30K)
- **Context Tiering.** Truncate `CLAUDE.md` to ≤ 100 lines (Permanent). Move granular rules to `.claude/rules/*.md` (On-Demand). Move per-session ephemera to `.claude/scratch/` (Temporary).
- **Glob-Scoped Rules.** Each `.claude/rules/*.md` carries `globs: <pattern>` frontmatter. Rule injects only when the agent touches matching files.
- **Description-Only Skill / Layer Bootstrapping.** Replace inline layer specs in `AGENTS.md` with `{name, description, fetch-tool}` entries. Body fetched via a `read_layer(name)` tool on demand. Same pattern Anthropic Skills already uses.

### 6.2 Tier 2 — within ~1 month, integrate into pre-commit gate (~30K → ~15K)
- **Aider-style repo-map.** New pre-commit step: tree-sitter parses `tasks/`, `prompts/`, `research/`, `skills/`; PageRank ranks the most-referenced symbols; output `index-quick.md` capped at 2K tokens. Agent reads only this map at boot.
- **Lazy ADR synthesis.** Extract the 5K `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` block from `AGENTS.md` into a standalone `ADR_SYNTHESIS.md`. `AGENTS.md` carries only a one-line pointer.

### 6.3 Tier 3 — within ~3 months, runtime fetching + subagent isolation (~15K → ~5K)
- **MCP Resources for static governance docs.** Mount `TASK.md`, `RESEARCH.md`, etc. as MCP `resource://agency/spec/<layer>` resources. Agent receives only URIs at boot.
- **Subagent context isolation.** Orchestrator never reads raw code. Spawns `deep-research` / `code-reviewer` subagents that consume large contexts and return ~1K compressed summaries. Already partially in place via `.claude/skills/superpowers-dispatching-parallel-agents/` and `superpowers-subagent-driven-development/`.

**Each tier is independently shippable as one or more Tasks.** Tier 1 is mechanical and risk-free. Tier 2 touches `tools/check-governance.sh`. Tier 3 touches the harness contract.

---

## 7. What remains open (the next Round-of-AskUser inventory)

These are the questions that the briefs do NOT settle, and that the user must answer before Round 11 can produce more locks. **Listed as an inventory; not yet asked.** The actual AskUser rounds will pick from this list in batches of ≤4.

### 7.A — Address-space + versioning collapse
1. **Replace SemVer with what exactly?** CalVer + content-hash (brief #1) vs. CalVer-only vs. content-hash-only? Affects amendment folder names and reproducibility tooling.
2. **UUIDv7 vs. ULID** — both work; ULID is more grep-friendly (Crockford base32). Pick one.
3. **Amendment folder name format** once SemVer is dropped: `<calver>-<short-hash>-<slug>/`? `<uuidv7-prefix>-<slug>/`? `<calver>-<slug>/` + frontmatter-only hash?

### 7.B — Plan-first Gherkin specifics
4. **Planner writes Gherkin alone** vs. **planner writes + separate reviewer subagent gates** vs. **planner writes + human approves before executor starts**. The literature is split.
5. **What happens if executor fails its Gherkin gate?** Replan? Amend? Promote the failure into a follow-up subtask?

### 7.C — Bootstrap-budget mechanics
6. **Tier-1 ordering and scope.** Start with Context Tiering alone, or roll all three Tier-1 patterns simultaneously?
7. **Aider repo-map: build with tree-sitter externally** or write a frontmatter-only equivalent? Tree-sitter pulls a new dependency.
8. **Lazy ADR synthesis: as a separate `ADR_SYNTHESIS.md`** or as an MCP resource from day 1?

### 7.D — Integrity layer
9. **Embedded SQLite as Tier-2** or defer to a separate Task? Adds a 9th pre-commit step.
10. **Schema-upgrade Task subtype** — what is its lifecycle? Goal-only? Or always fully specified?

### 7.E — Open items the briefs DID NOT cover (still on the table)
11. **`decompose-goal` as a first-class SKILL** (Round 10's open question). Survives unchanged; needs a decision.
12. **`meta/` restructure** (Round 9 reopen). Briefs are silent.
13. **Migration mechanics for 96 / 77 / 30 existing artefacts.** Briefs are silent.
14. **Initial goal-seeding** — which existing top-level concerns become the seed `task_kind: goal` parents.

### 7.F — Synthesis-level meta-question (defer; signal-only for now)
15. **Move governance to runtime (MCP-validation tools)?** This is the brief #2 §8 meta-question. Not asking now; signalling that a future Major-version rethink may want to.

---

## 8. Recommended Round-11+ sequencing

If the user approves this overview, propose the following AskUser-round sequencing (≤ 4 questions per round):

- **Round 11** (Address-space collapse): items §7.A 1, 2, 3 + one warm-up confirmation that SemVer is dropped.
- **Round 12** (Plan-first Gherkin): items §7.B 4, 5 + a confirmation that retroactive Gherkin is dropped.
- **Round 13** (Bootstrap-budget Tier-1 scope): items §7.C 6, 7, 8.
- **Round 14** (Integrity layer + schema-upgrade): items §7.D 9, 10 + (optional) §7.E 11.
- **Round 15** (Migration + seeding): items §7.E 12, 13, 14.

After Round 15, the plan is fully re-locked and the substrate refactor can be decomposed into Tasks (Tiers 1–3 of the bootstrap roadmap + the address-space migration + the gate-timing migration).

---

## 9. What this overview is NOT

- It is **not** a final plan. It is the input to Rounds 11+.
- It is **not** a commitment to drop locks. Each REPLACE/REVISE item is a *proposal* that the user gets to confirm or push back on in Round 11+.
- It is **not** an implementation roadmap. The Tier 1/2/3 ordering in §6 is the literature's recommendation, not the user's commitment.

---

*Lives at `.claude/plans/plan-rethink-overview.md`, alongside [`agency-refactor-plan.md`](./agency-refactor-plan.md), [`round-10-additions.md`](./round-10-additions.md), [`synthesis-gemini-1-2.md`](./synthesis-gemini-1-2.md), and [`readme.md`](./readme.md). See readme.md for full navigation.*
