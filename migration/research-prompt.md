---
type: note
status: pending
slug: research-prompt
summary: "Adversarial state-of-the-art audit prompt for Gemini Deep Research — covers all 11 ratified locks + 7 open questions across 12 axes. Rendered via skills/research-prompt-optimizer v3.3.1 in strict interactive mode. Workspace zip at /mnt/user-data/outputs/workspace_agency-refactor-soa-audit.zip."
created: 2026-05-13
updated: 2026-05-13
research_prompt_optimizer_version: "3.3.1"
research_prompt_category: "B"
research_prompt_methods: ["M01", "M06", "M07", "M08", "M09", "M10", "M12", "M13"]
research_prompt_frameworks: ["ReAct", "RISEN", "Synthesis", "TIDD-EC"]
research_prompt_cross_pollination: ["b-into-a", "b-into-c"]
research_prompt_target: "Gemini Deep Research (model-agnostic)"
---

---
topic: "Adversarial state-of-the-art audit for `agency` repo's complete refactoring (12-type ontology + 3-mode placement + ULID + auto-readmes + 11 ratified locks + 7 open questions)"
slug: "agency-refactor-soa-audit"
research_category: "B"
research_category_label: "Extraction"
critical_thinking_methods:
  - "M01 Falsification"
  - "M06 Source Triangulation"
  - "M07 Contradiction Log"
  - "M08 What Would Change My Mind"
  - "M09 Red Team / Devil's Advocate Review"
  - "M10 First-Principles Decomposition"
  - "M12 Base-Rate Anchoring"
  - "M13 Adversarial Query Expansion"
prompt_engineering_framework_agentic_spine: "ReAct"
prompt_engineering_framework_structural: "RISEN"
cross_pollination:
  - source_category: "A"
    module: "b-into-a"
    title: "Exploratory Skepticism Injection (meta-counter-argument about migration path itself)"
  - source_category: "C"
    module: "b-into-c"
    title: "Lifecycle Audit Injection (where each lock breaks across creation/promotion/archival/rebuild)"
constraint_blocks:
  - "0 — Reflection Baseline (Always Active)"
  - "1 — Known Priors — VERBATIM from /migration/"
  - "2 — Temporal Scope"
  - "3 — Output Format + Exclusions"
language: "en"
target_agent: "model-agnostic"
created: "2026-05-13T19:30:00+02:00"
version: "1.0"
source_skill: "research-prompt-optimizer v3.2.0"
---

# Research Prompt: Adversarial state-of-the-art audit for `agency` repo's complete refactoring (12-type ontology + 3-mode placement + ULID + auto-readmes + 11 ratified locks + 7 open questions)

> **For the executing AI:** This prompt is self-contained. Every
> method, framework, and constraint you need is defined inline below.
> You do not need external context, prior training on specific
> methodologies, or knowledge of the skill that generated this
> prompt. **Read the entire prompt before beginning.** Specifically,
> read the three layers in the Meta-Header below and verify you
> understand how they compose.



---

## Meta-Header — What This Prompt Is and How To Read It

This research prompt combines **three independent layers**. Each
governs a different aspect of your work:

### Layer 1 — Epistemological Layer (Extraction)

This layer defines **how to think** about the research — what kind of
question it is, what counts as success, what failure modes are likely.

## Epistemological Layer — Category B (Extraction)

This research is an **extraction**, not an exploration. The answer
exists in the world; your task is to locate it, verify it, and present
it in a structured form. You are not generating new hypotheses.

**What this means for your execution:**

1. **Follow the plan exactly.**
   The Steps section below specifies an ordered procedure. Execute it
   end-to-end. Do not improvise alternative strategies. If the plan
   proves impossible to execute, halt and report the blockage — do not
   silently substitute another approach.

2. **Fill every field of the output schema or flag it as missing.**
   The final output has a locked schema (specified in the Expectations
   section). Every field must be populated with evidence-backed content,
   OR explicitly marked "not found — [reason]". Never invent content to
   fill a gap.

3. **Source triangulation is mandatory.**
   Every factual claim requires at least three independent sources, at
   least one of which is a primary source. Aggregators count as one
   source, regardless of how many aggregators confirm the same thing.
   This rule is enforced by Method: Source Triangulation (defined in
   the critical-thinking methods section).

4. **Handle contradictions transparently.**
   When sources disagree, you do not silently pick one side. You log
   the disagreement per Method: Contradiction Log (defined below) and
   present both positions with their evidence in the final output.

5. **Extraction is not interpretation.**
   Your task is to collect and structure, not to opine. Reserve
   evaluative judgments for a clearly-flagged "Analyst Note" section
   if one is requested; otherwise present findings factually.

**Operational constraint:** Speed is less important than completeness
of the schema. If the schema is fully populated and triangulated, the
research is complete — further search produces diminishing returns.

### Layer 2 — Agentic Spine (ReAct)

This layer defines **how to iterate** — the micro-execution loop that
each Step in this prompt expands into.

## Prompt-Engineering Framework — Agentic Spine: ReAct

This prompt uses the **ReAct framework** as its agentic spine. Every
autonomous research loop in this prompt follows the ReAct cycle. Each
iteration of your work loop consists of three phases:

- **Reason** — You articulate your current understanding and plan the
  next action in plain language. You select exactly one of the active
  critical-thinking methods (see palette below) as the governing
  method for the next Act.
- **Act** — You execute exactly one action — typically one search,
  one retrieval, one calculation. Not three. One.
- **Observe** — You record what the action returned and what it means.
  You decide: continue this branch, backtrack, or expand vocabulary
  via M13 Adversarial Query Expansion.

| Anchor   | Method                          | When to choose                        |
|----------|---------------------------------|---------------------------------------|
| [M01] | Falsification                   | When you have a hypothesis to falsify |
| [M06] | Source Triangulation            | —                                     |
| [M07] | Contradiction Log               | —                                     |
| [M08] | What Would Change My Mind       | —                                     |
| [M09] | Red Team / Devil's Advocate Review | —                                     |
| [M10] | First-Principles Decomposition  | —                                     |
| [M12] | Base-Rate Anchoring             | —                                     |
| [M13] | Adversarial Query Expansion     | Always-on; minimum once per 10-minute window |

### The Reason Phase — Verbatim Template (used in every Reason)

In every Reason phase you write, fill these five lines verbatim,
in this order, before you move to Act:

> **Active method this Act:** [M__] — one sentence why this method,
>     not another, governs the next Act.
> **Constraint compliance:** CB__ — one example of how the next Act
>     honors this Constraint Block.
> **Local-minimum risk:** [low / medium / high]. If medium or high,
>     invoke [M13] Adversarial Query Expansion BEFORE the Act.
> **Reflection trigger:** [is this an M0 checkpoint?]. If yes, write
>     the reflection entry HERE before the Act, not after.
> **Plan:** [the concrete next Act in one line].

A Reason phase missing any of the five lines is incomplete; do not
advance to Act.

### Loop Structure

### Layer 3 — Structural Layer (RISEN)

This layer defines **how the document is organized** — what sections
exist, what order they go in, and what each section is for.

## Prompt-Engineering Framework (Structural Layer): RISEN

This prompt follows the **RISEN framework** as its structural layer,
stacked on top of the ReAct agentic spine. RISEN governs how the
sections of this prompt are organized; ReAct governs how you iterate
within each step. RISEN stands for:

- **R — Role**: Who you are acting as during this task.
- **I — Input**: What materials, questions, or data you are starting with.
- **S — Steps**: The explicit ordered procedure to follow.
- **E — Expectations**: What a successful output looks like (format,
  coverage, depth).
- **N — Narrowing**: Hard constraints, exclusions, and scope limits.

**Your first action before Step 1:** Restate the Role and Narrowing
sections in your own words. Confirm you have internalized them. Do not
begin Step 1 until this restatement is written.

Each section of this prompt is labeled with its RISEN component in
parentheses, e.g., "(R — Role)". Honor each component as a hard contract.

### How the Layers Compose

- **Layer 1** governs the *strategy* (exploration vs. extraction vs.
  lifecycle).
- **Layer 2** governs the *micro-execution* inside each Step (Reason
  → Act → Observe).
- **Layer 3** governs the *macro-organisation* of this document
  (sections, ordering, first-action directive).

You honor all three simultaneously. They are orthogonal, not nested.

---

## Constraint Blocks

## CONSTRAINT BLOCK 0 — Reflection Baseline (Always Active)

Reflection is not a polish step. It is a **baseline operational
requirement** that runs in parallel to every other activity in this
research. You — the executing agent — perform targeted reflection at
every defined checkpoint, in writing, using the template below. A
checkpoint reached without a reflection entry is an incomplete
checkpoint; do not advance past it.

### Reflection Checkpoints (Minimum)

1. **Kickoff reflection** — immediately after restating the research
   objective and Constraint Blocks, before the first Reason phase.
2. **Mid-run reflection** — after the first batch of searches, once
   you have a tentative direction but before you commit to it.
3. **Post-Query-Expansion reflection** — after each Adversarial Query
   Expansion pass (Method M13).
4. **Pre-synthesis reflection** — immediately before the Pre-Synthesis
   Integrity Check (M4).
5. **Post-synthesis reflection** — after the draft synthesis, before
   delivery.

Additional checkpoints apply if the research category has its own
(e.g., per-session reflections in lifecycle research).

### Reflection Template — Use Verbatim Structure

Each reflection entry answers these five questions, in order, in
writing:

> **Q1. What do I actually believe right now, and how confident?**
> (One sentence. Use an explicit confidence band: low / medium / high.)
>
> **Q2. What is the strongest piece of evidence against my current
> belief?** (Name the specific source or the specific observation. If
> you cannot name one, that itself is the answer — and it is a warning.)
>
> **Q3. Where am I most likely wrong, and why?** (Not generic — name
> the specific claim, assumption, or inference that is weakest.)
>
> **Q4. What would I do differently if I restarted the research from
> scratch knowing what I know now?** (Forces de-anchoring from the
> path already taken.)
>
> **Q5. What is the single highest-value next action?** (Must be a
> concrete, executable next step — a specific search, a specific
> verification, a specific hypothesis branch to open or close.)

### Rules

- Reflections are **written**, not internal. They become part of the
  research notes and of the final output's Reflection History
  section in the Synthesis.
- Reflections may not be skipped "because the answer is obvious". If
  the answer feels obvious, write the obvious answer in one line and
  advance — but do not omit the entry.
- **Reflections on reflections are allowed but not required.** If a
  reflection surfaces a contradiction with an earlier reflection, log
  both in the Contradiction Log (Method M07) with a note that the
  disagreement is internal rather than inter-source.
- If a reflection produces an action item (Q5) that contradicts the
  current Step's plan, the action item **takes precedence**. Update
  the plan, note the change, and continue.

### Anti-Rationalization Guard

If you find yourself writing "N/A" or "nothing to reflect on" in a
reflection entry — stop and re-read the entry's five questions. At
least Q2 and Q3 always have a real answer. "N/A" is a signal that the
reflection is being skipped performatively; write the real answer
instead.

### CONSTRAINT BLOCK 1 — Known Priors — VERBATIM from /migration/

The `agency` repository's `/migration/` workspace contains the
following authoritative-but-PROVISIONAL design state. Every
lock and citation below is to be treated as A FALSIFIABLE
CLAIM, not a fact. Your default verdict is REPLACE; KEEP must
be earned via falsification-resistance.

==================================================================
CATEGORY A — THE 11 RATIFIED LOCKS (verbatim from
migration/locks-ratified.md)
==================================================================

## L11.32‴ — Twelve first-class artifact types

Supersedes L11.32′ (7 types) and L11.32″ (9 types).

Base (7, unchanged from L11.32′):
1. `task` — orchestration / coordination unit
2. `prompt` — executable instruction set for an agent
3. `research` — evidence + synthesis workspace
4. `skill` — reusable agent capability
5. `adr` — architecture decision record
6. `spec` — root governance specification
7. `readme` — folder navigation index

Promoted (5, new this round):
8. `role` — agent-persona definition (was: embedded in prompts)
9. `lock` — design-decision checkpoint (was: embedded in plan notes)
10. `gherkin` — acceptance-scenario artifact (was: embedded in spec bodies)
11. `friction-log` — FL0–FL3 friction record (was: embedded in PR body)
12. `hook` — Claude Code event hook (was: tools/hooks/<event>.sh)

Each promoted type was being authored or referenced as if first-
class but had no graph edge type. Promotion creates explicit
edges (e.g. `prompt_uses_role`, `task_references_locks`).

## L11.36′ — Three placement modes

Every artifact type declares which modes it permits via
templates/<type>/manifest.yml:
- STANDALONE: own folder under /<type>/<id>/
- SUBFILE: own file inside another artifact's folder
- SUBDOC: embedded in another artifact's body via Pandoc fenced
  div with internal YAML

Constraint: every type permits at least STANDALONE. SUBFILE /
SUBDOC are per-type opt-ins; the matrix is Q1 in open-questions.

## L11.37′ — SQLite uniform across modes

Single graph DB at tools/graph/agency.db. Edges are mode-blind.
Tables: artifacts(id, type, placement_mode, parent_id, path,
slug, ulid, created_at, updated_at) + edges(source_id, target_id,
edge_type) + subdocument_locations(artifact_id, parent_path,
fenced_div_id, byte_offset_start, byte_offset_end) — the
subdocument_locations table is a REGENERABLE cache, never source
of truth.

## L11.38′ — Pandoc fenced divs as SUBDOC syntax

:::{.prompt id=draft-pr-body type=prompt status=draft}
---
slug: draft-pr-body
summary: Prompt for drafting the PR body...
---
# Body content here...
:::

Subfile syntax = standard top-of-file YAML frontmatter.

## L11.39′ — Mode-aware `agency` CLI surface

agency new <type> [--mode standalone|subfile|subdoc]
                  [--in <parent-path>] --slug <slug>
agency extract <subdoc-id> --to standalone
agency edit <id>
agency promote <id> --to <new-mode>
agency archive <id> [--all]
agency readme <id> [--all] [--check]

## L11.40′ — Lock placement

Locks are STANDALONE-only under decisions/locks/<lock-id>-<slug>.md.
Content-addressed via lock_sha (SHA-256 of body bytes below the
frontmatter). No SemVer. Supersession via lock_supersedes:
<previous-lock-id>.

Per Decision 4, the <lock-id> portion preserves user-facing
L<round>.<sub> notation (e.g. L11.43). Slug remains kebab-case;
filename and slug differ.

## L11.41′ — Hook placement

Hooks are STANDALONE-only under tools/hooks/<event>/<slug>/.
Each hook folder MUST contain hook.md + <event>.sh + _<event>.py.
Registration in .claude/settings.json via ${CLAUDE_PROJECT_DIR}
exec form (D.7 enforcement).

## L11.42 — Closed schemas everywhere

No notes: / extra: / metadata: escape hatches in any
frontmatter schema. Every key declared in the namespace
registry. Forward compatibility via schema versioning (new keys
land via ADR), not free-form blobs.

## L11.43 (revised v2 — IN-BODY) — Tasks-only ULID convention

Original L11.43 (Roundtable 7) applied ULIDs to all 12 types
except ADR with <slug>-<ulid>/ folder shape. Revised in
Roundtable 8 to narrow scope and move the ULID into frontmatter.

- Scope: tasks only, permanently.
- Folder shape: tasks/<slug>/ — bare slug.
- Identity: id: 01KRH6J3Y4B2YPD0X276D2GEBY in task.md frontmatter.
- Slug uniqueness enforced at `agency new` time.
- Prose references: slug alone is canonical; short-prefix ULID
  appended only on collision.
- Migration: archive-first. Current tasks/<NNN>-<slug>/ move to
  archive/tasks/<NNN>-<slug>/. No retroactive ULID minting.

## L11.43 v3 (R1 — PROVISIONAL, REVISION HISTORY) — 6-type scope

Revision history answer: "All ULID-prefixed like tasks (extend
L11.43)" — replaces earlier "per-type natural fit". Scope
extends to 6 types: task, role, lock, gherkin, friction-log,
hook. PROVISIONAL — user clicked but interrupted before
confirming cascade implications.

## L11.44 (v2) — `agency readme` CLI auto-generates every readme

Every readme.md is fully auto-generated, end-to-end. No hand-
written body content. Frontmatter is the SOLE source of truth.

- Scope: all operational folders.
- Trigger: pre-commit auto-regenerates when any touched file's
  frontmatter changes.
- Edge direction: bidirectional.
- Schemas expand to carry purpose: + assumptions: fields.
- Renderer output: entire readme.md is machine-written, marked
  with <!-- AUTOGENERATED by agency readme; edit frontmatter
  to change. -->

## Decision 4 — Per-type natural-fit ID convention for 5 promoted types

| Type | Convention | Folder shape |
|---|---|---|
| role | slug | roles/<slug>/role.md (NEW top-level folder) |
| lock | preserve L<round>.<sub> notation | decisions/locks/L<r>.<s>-<slug>.md |
| gherkin | # anchor: <id>; SUBDOC/SUBFILE | <parent>/scenarios/<slug>.gherkin.md |
| friction-log | parent + session-date | <parent>/reflection/friction-log.md |
| hook | event-name PK | tools/hooks/<event>/<slug>/hook.md |

CONTRADICTION WITH R1 (v3): If R1 is confirmed, Decision 4 is
reversed — all 5 promoted types adopt ULID instead of per-type
natural fit. Both presented for adversarial review.

==================================================================
CATEGORY B — THE 8 D-CITATIONS (verbatim from
migration/gemini-evidence.md)
==================================================================

NOTE: The cited source path
`research/gemini-architectural-audit-2/output/SPEC.md` is STALE.
Actual brief lives at:
- `.claude/research-results/gemini-1-architecture-audit.md` (75KB)
- `.claude/research-results/gemini-2-bootstrap-context-engineering.md` (54KB)

## D1 — Promote role/lock/gherkin/friction-log/hook to first-class

Gemini finding: Audit graph cannot function if cross-references
degrade to body-Markdown links. Body links are unreachable to
linker. Every concept that participates in cross-references MUST
be first-class with frontmatter and edge type.
Anchors: L11.32‴.

## D2 — Three-mode placement, not STANDALONE-only

Gemini finding: STANDALONE-only forces fragmentation of
inherently-parented concepts. Graph layer is mode-blind by
design — embedding does not compromise graph completeness.
Per-type opt-in is right factoring. Anchors: L11.36′.

## D3 — Locks are content-addressed checkpoints, not versioned packages

Gemini finding: Lock is a snapshot of agreed text. Right
identity is content hash (SHA-256 of body bytes). SemVer carries
package-management semantics that don't apply. Anchors: L11.40′.

## D4 — Pandoc fenced divs as SUBDOC syntax

Gemini finding: Pandoc fenced divs win because (i) published AST
(pandoc-ast); (ii) degrade gracefully on plain Markdown; (iii)
explicit id attributes; (iv) YAML inside follows same shape as
top-of-file frontmatter. Anchors: L11.38′.

## D5 — SQLite is sufficient; no graph DB

Gemini finding: At ~350 artifact scale, SQLite with two tables
(artifacts, edges) handles every query in <10ms. Graph DBs
(Neo4j, Memgraph) introduce operational overhead without
performance benefit until ~100K nodes. Defer until evidence
warrants. Anchors: L11.37′.

## D6 — subdocument_locations must be regenerable, never source of truth

Gemini finding: Byte offsets are derivable from full repo scan.
Storing them as primary data introduces cache-coherence problem.
Cache offsets in DB for query convenience; regenerable via
`agency rescan`. Source of truth = filesystem. Anchors: L11.37′.

## D7 — `agency promote` is a first-class CLI verb

Gemini finding: `agency promote` (mode transition) has
fundamentally different semantics from `agency rename` and
`agency archive`. Three explicit verbs are easier to teach and
easier to lint. Anchors: L11.39′.

## D8 — Closed schemas everywhere

Gemini finding: Open schemas defeat the closed-world graph
assumption. Every key the linker honours must be declared in
namespace registry; unknown keys imply silent edge omissions.
Forward compatibility via versioned schema additions through
ADRs. Anchors: L11.42.

==================================================================
CATEGORY C — THE 7 OPEN QUESTIONS (verbatim from
migration/open-questions.md)
==================================================================

## Q1 — Mode matrix per type

For each of the 12 types, which of STANDALONE / SUBFILE / SUBDOC
are permitted? Draft matrix shows task/research/skill/adr/spec/
readme/lock/hook = STANDALONE-required; prompt/role/gherkin =
all three modes; friction-log = STANDALONE+SUBFILE.
Migration recommendation: restrict SUBDOC to four types
(prompt, role, gherkin, friction-log); ban elsewhere.

## Q2 — `agency promote` edge-rewrite semantics

When a SUBDOC promotes to STANDALONE (or vice versa):
(a) Auto — edges follow automatically.
(b) Confirm per edge — user confirms each rewrite.
(c) Staged — promotion generates reviewable diff.
Migration recommendation: (a) for non-destructive, (c) for
T4-boundary-crossing.

## Q3 — Parallel-edit locking

When two agents simultaneously edit different SUBDOCs in same
parent file:
(a) File-level lock (current behaviour; second waits).
(b) Byte-range CRDT — both edits land if non-overlapping.
(c) Optimistic — both commit, git resolves.
Migration recommendation: (a) file-level.

## Q4 — Slug-collision disambiguation tooling

Where does collision detection live?
(a) `agency new` at mint time — error or --allow-collision.
(b) Pre-commit linter — WARN on collisions.
(c) Lazy at reference resolution.
Migration recommendation: (a) primary + (b) backstop.

## Q5 — `assumption-entry` as the 13th type?

L11.44 v2 moves assumption log into frontmatter as
assumptions: list[Assumption]. Should each entry also become
queryable first-class artifact with own ID + edges?
Migration recommendation: defer; promote only if assumption-
level edges become needed.

## Q6 — Detailed natural-fit for gherkin/friction-log/hook

gherkin: always-parented vs STANDALONE under scenarios/.
friction-log: always-parented; singular vs dated.
hook: one-per-event vs multi-hook-per-event.
Migration recommendation: start parented-only for gherkin +
friction-log; one-per-event for hook with future multi-expand.

## Q7 — Sequencing

Path A: Close Q1-Q6 → ratify ADR-0013 → cascade specs → tooling.
Path B: Build agency-readme prototype → revise ADR → cascade.
Path C: Land schema deltas first → ADR references already-landed.
Migration recommendation: Path A.

==================================================================
CATEGORY D — 14 PHASE-2 CONTRADICTIONS DETECTED
(from /sc:analyze run before this brief)
==================================================================

P0 (Critical, 3): locks-ratified.md L148 header "Tasks-only" vs
revision-history L215-224 "6 types"; adr-draft.md L21 summary
stale on R1; adr-draft.md L104 Lock 9 stale on R1; next-task.md
§3 exempt paths exceed user-authorised 2-folder directive.

P1 (High, 4): adr-draft.md L126/L160 stale; adr-draft.md L179
missing v3 supersession edge; schemas-delta.md L62/L68 SQL
comments stale on R1; locks-ratified.md L218 R1 self-flagged
provisional but no other file marks itself stale-pending-R1.

P2 (Medium, 2): schemas-delta.md L70-76 slug-pattern relaxation
may need broader scope if R1 confirmed; locks-ratified.md L160
rejected candidate L11.43‴ not separately documented.

P3 (Low, 1): inconsistent supersession trail for L11.43‴.

Plus 5 hidden assumptions per dimension (Quality / Security /
Performance / Architecture) — see Phase 2 analysis report.

==================================================================
CATEGORY E — 6 UNCOVERED-GAP CATEGORIES
==================================================================

1. Migration tooling — git filter-branch vs git filter-repo
   vs big-bang `git mv`; history preservation at 1000+ files.
2. Refactoring case studies — monorepo migrations (Bazel, Nx,
   Sourcegraph); ontology evolution (W3C, schema.org).
3. Hook architecture security — --no-verify bypass, injection
   vectors, agent tampering at pre-commit layer.
4. Skill packaging — SuperClaude vs Anthropic Agent Skills SDK
   vs MCP plugins; versioning + deprecation.
5. Multi-agent orchestration — deadlock prevention, backpressure,
   fan-out caps, priority queuing.
6. Trust audit + research immutability — content addressing
   (IPFS CID, Git SHA, Sigstore), notary v2 patterns.

==================================================================
CATEGORY F — 30-QUESTION BRAINSTORM TREE (Phase 3 /sc:brainstorm)
==================================================================

Ontology axis: Q-O1 cardinality 12 vs alternatives;
Q-O2 prompt+research as one type; Q-O3 lock vs adr namespace.

Schema axis: Q-S1 YAML vs TOML vs JSON Schema $id;
Q-S2 closed vs open at 50+ types; Q-S3 L1+L2+L3 layering.

ID axis: Q-I1 ULID vs UUIDv7 vs CUIDv2 vs nanoid vs Snowflake;
Q-I2 single seq vs per-type vs ULID; Q-I3 filename↔slug↔ID.

Storage axis: Q-St1 SQLite vs DuckDB vs Postgres vs RDF at
7200+72K-edge scale; Q-St2 frontmatter vs DB vs hybrid;
Q-St3 cache-invalidation patterns.

Tooling axis: Q-T1 Python vs Rust vs Go for 7200-artifact CLI;
Q-T2 multi-lang vs single-lang; Q-T3 Pandoc alternatives
(Markdoc, MDX, Quarto AST).

Workflow axis: Q-W1 placement-mode matrix patterns;
Q-W2 promote/archive/edit completeness; Q-W3 parallel-edit
coordination.

Governance axis: Q-G1 pre-commit alternatives (lefthook,
pre-commit.com, husky); Q-G2 T1-T4 repair-tier patterns;
Q-G3 RFC 2119 + Gherkin vs Concordion / JBehave / ATDD.

Hook architecture: Q-H1 5-event model vs alternatives;
Q-H2 security audit of --no-verify; Q-H3 D.7 SessionStart
ban pattern.

Migration mechanics: Q-M1 big-bang vs incremental vs no-archive;
Q-M2 git mv vs git filter-repo at 1000+ files;
Q-M3 two-folder strict vs pragmatic exemption.

Observability: Q-Ob1 FL0-FL3 self-reporting industrial precedent;
Q-Ob2 skill-invocation-log vs OpenTelemetry; Q-Ob3 trust-audit
drift detection.

Skill packaging: Q-Sk1 SuperClaude vs Anthropic SDK vs MCP;
Q-Sk2 SHA-pinned versioning + deprecation.

### CONSTRAINT BLOCK 2 — Temporal Scope

Primary window: 2024-11-01 to 2026-05-13. Highest-quality
citations come from this window (post-Anthropic Skills launch,
post-SuperClaude v4, post-MCP maturation).

Secondary window: 2024-05-01 to 2024-10-31. Used only when
primary-window evidence is insufficient for an axis.

Foundational: pre-2024-05. Must be explicitly flagged
[FOUNDATIONAL]. Accepted only for foundational claims (RFC
2119, ADR origins, IPFS CID).

Reject: pre-2023 unless cited verbatim by a primary-window
source.

### CONSTRAINT BLOCK 3 — Output Format + Exclusions

Markdown report with SEVEN sections + required matrices:

§1 — Executive Verdict per Axis (Axes 1–12).
    For EACH axis: KEEP / REVISE / REPLACE verdict, confidence
    (low/medium/high), ≥3 citations.

§2 — Per-Axis State-of-the-Art Survey.
    For EACH axis: ≥5 industrial/academic sources (post-2024-11
    primary), 1-paragraph synthesis per source, URL + access
    date.

§3 — Strongest Counter-Arguments per Ratified Lock.
    For EACH of the 12 lock identities (L11.32‴, L11.36′,
    L11.37′, L11.38′, L11.39′, L11.40′, L11.41′, L11.42,
    L11.43 v2, L11.43 v3/R1, L11.44 v2, Decision 4):
    (a) counter-claim verbatim,
    (b) M01 falsification test,
    (c) M08 WWCMM condition,
    (d) ≥2 supporting citations.

§4 — Comparison Matrices (≥8 required):
    (i) ID conventions (ULID/UUIDv7/CUIDv2/nanoid/Snowflake/seq);
    (ii) Storage backends (SQLite/DuckDB/Postgres/RDF/Neo4j);
    (iii) Placement-mode syntax (Pandoc-divs/MDX/Markdoc/HTML);
    (iv) Pre-commit gates (lefthook/pre-commit.com/husky/custom);
    (v) Spec language (RFC2119+Gherkin/Concordion/JBehave/ATDD);
    (vi) ADR formats (MADR4/y-statement/Nygard/Henderson);
    (vii) Ontology cardinality (7/12/18/N types);
    (viii) Lock-vs-lock interaction matrix (added per L4 lens).

§5 — Open-Question Resolutions.
    For EACH of Q1–Q7: recommendation + 2-3 alternatives +
    tradeoff matrix + evidence chain (≥3 citations) +
    falsifiable success criterion.

§6 — Stale-Citation Correction Log.
    Exactly 8 rows (one per D1–D8). Each: confirm/refute
    verdict + corrected source path + paraphrase fidelity check
    against `.claude/research-results/gemini-1-architecture-
    audit.md`.

§7 — Recommended Next Actions for the Rebuild.
    Prioritised action list derived from §§1–6. Each action:
    owner role (CTO/agent/external), prerequisites, effort
    estimate, falsifiable success criterion, supersession edges
    to the 11 locks.

MUST INCLUDE — orthogonal-lens questions (L1–L6 from Phase 2.6):
  L1: Why migrate at all vs. fresh repo?
  L2: Agent-identity / authorship under conflict?
  L3: Rollback story for half-done rebuild?
  L4: Lock-vs-lock interaction matrix?
  L5: Agent-onboarding curve cold-start?
  L6: Gemini-as-dependency reproducibility?
Address each at least once in §3 or §5.

MUST NOT INCLUDE:
- Implementation of the rebuild (out of scope per CB0).
- Auditing user's complete-refactor directive.
- Replacing /migration/ workspace artifacts.

## Critical-Thinking Methods (Always Active)

### Method: Falsification (Karl Popper's Disconfirmation Principle)

**What it is:** Instead of searching for evidence that supports a
hypothesis, you actively search for evidence that would refute it. A
hypothesis only earns credibility after surviving serious attempts to
break it.

**Why it is in this prompt:** Confirmation bias is the dominant failure
mode of autonomous research agents. Without explicit falsification
steps, you will tend to surface supporting evidence and ignore or
under-weight contradicting evidence.

**How to apply it — step by step:**

1. Before searching, write down the hypothesis you are testing as a
   falsifiable statement (one that can, in principle, be proven wrong
   by observable evidence). In this prompt, you generate the hypothesis
   as part of the Reason phase that selects this method; refer to it as
   `{{hypothesis}}` when restating, but write the actual statement in
   your working notes.

2. For every supporting piece of evidence you find, execute a **matched
   disconfirmation query** — a search specifically designed to surface
   the strongest counter-evidence. Generate two query phrasings during
   the Reason phase: one of the form `{{disprove_phrase}}` (a phrase
   that would directly refute the hypothesis) and one of the form
   `{{failure_mode_phrase}}` (the failure case for the same hypothesis).

3. Weight disconfirmation attempts equal to or higher than confirmations
   in your final synthesis.

4. If no serious disconfirmation attempt surfaced any counter-evidence,
   explicitly state in your Observe phase: *"This hypothesis survived
   N disconfirmation queries."* If counter-evidence surfaced, mark the
   hypothesis as **contested** and document both sides.

**When to stop / escape criterion:** Stop applying M01 to a single
hypothesis when it has survived **at least three orthogonal
disconfirmation queries** OR when contradicting evidence exceeds 20%
of the total evidence pool — whichever comes first.

**Example trigger in this research context:** When the active method
in your Reason phase is `[M01]`, you generate `{{hypothesis}}` (a
falsifiable claim) and run searches phrased like `{{disprove_phrase}}`
and `{{failure_mode_phrase}}` before committing to confirmation
searches. The placeholders are filled by you, the executing agent, at
the moment you select M01 — not in advance.

### Method: Source Triangulation

**What it is:** Every significant factual claim is confirmed across at
least **three independent source types** before being admitted to the
final output. Aggregators counting as one source, not three.

**Why it is in this prompt:** Single-source claims propagate errors.
Aggregator-heavy research agents are especially prone to citation chains
that all trace back to one primary source that is wrong.

**How to apply it — step by step:**
1. For every significant claim, identify the **primary source** (the
   original research, filing, dataset, or firsthand report).
2. Find at least **two additional independent sources** of different type
   (e.g., primary + secondary analysis + regulatory filing).
3. If all confirmations trace back to a single primary source, mark the
   claim as **single-source** and flag it in the output.
4. Prefer source types in this order: (a) peer-reviewed papers, (b)
   official primary documents (SEC filings, government data), (c) major
   news outlets with editorial accountability, (d) industry reports,
   (e) blog posts and social media (rarely sufficient alone).

**When to stop / escape criterion:** Stop searching once three
independent confirmations are found OR when the claim is minor enough
that single-source citation is acceptable (flag it).

**Example trigger in this research context:** If you find "{{claim}}" in
one source, your next queries must be designed to confirm or disconfirm
it from two independent channels before including it.

### Method: Contradiction Log

**What it is:** A dedicated running log of every contradiction, tension,
or disagreement encountered between sources. Contradictions are not
silently resolved by picking one side — they are documented and
characterized.

**Why it is in this prompt:** Autonomous research agents tend to smooth
over contradictions by picking the majority or the most recent source,
which hides real disagreement in the field from the reader.

**How to apply it — step by step:**
1. Maintain a section titled **Contradiction Log** in your working notes.
2. For each contradiction, record: (a) the two (or more) conflicting
   claims, (b) the sources, (c) what you believe is the source of the
   disagreement (methodology, time period, definitional mismatch, genuine
   empirical dispute).
3. In the final output, include a synthesized version of the Contradiction
   Log as its own section.
4. For each logged contradiction, state what additional evidence would
   resolve it.

**When to stop / escape criterion:** No ceiling — log all contradictions
discovered. If the log exceeds 10 entries, consider whether the research
question itself is ill-posed.

**Example trigger in this research context:** If Source A says
"{{claim_x}}" and Source B says "{{claim_not_x}}", log both with context
rather than silently picking one.

### Method: "What Would Change My Mind" (Pre-Commitment)

**What it is:** Before completing the research, you write down — in
concrete, observable terms — what evidence would cause you to reverse
your current tentative conclusion. This is a pre-commitment against
motivated reasoning.

**Why it is in this prompt:** Without a pre-committed disconfirmation
criterion, researchers and agents re-rationalize evidence to fit the
conclusion they were already drifting toward.

**How to apply it — step by step:**
1. Once your tentative conclusion stabilizes (typically mid-research),
   pause and write: "I would reverse this conclusion if I found [X]."
2. The [X] must be **concrete and observable** (a specific study, a
   specific data point, a specific counter-example) — not vague
   ("evidence against").
3. For the remainder of the research, actively search for [X].
4. In the final output, report whether [X] was found or not.

**When to stop / escape criterion:** One pre-commitment per major
conclusion. Do not inflate into per-claim tracking.

**Example trigger in this research context:** "My tentative conclusion
is {{conclusion}}. I would reverse this if I found
{{disconfirming_observation}}."

### Method: Red Team / Devil's Advocate Review

**What it is:** Before finalizing the output, you switch into the role of
a hostile, competent critic whose job is to find every weakness. You
document the attacks, then either repair them or concede them.

**Why it is in this prompt:** The same cognitive process that produces
the research is poor at critiquing it. Explicit role-switching
(researcher → critic) simulates external review.

**How to apply it — step by step:**
1. After drafting the conclusions, declare: "I now switch to critic mode."
2. Attack each major conclusion from at least three angles:
   (a) source quality — are the sources strong?
   (b) logical chain — does the conclusion actually follow?
   (c) alternative explanations — is there a competing explanation for
       the evidence that is equally or more plausible?
3. Record each attack.
4. For each attack, either: (i) repair the conclusion to survive the
   attack, OR (ii) concede and soften the conclusion, OR (iii) document
   the attack as a known limitation in the final output.

**When to stop / escape criterion:** Three attack angles per major
conclusion. Stop when you cannot generate a non-trivial new attack.

**Example trigger in this research context:** Conclusion: "{{conclusion}}."
Attacks: (1) sources concentrated in {{biased_domain}}; (2) the reasoning
assumes {{hidden_premise}}; (3) alternative explanation:
{{competing_hypothesis}}.

### Method: First-Principles Decomposition

**What it is:** You decompose the research question into its most basic,
empirically or logically fundamental components, refusing to accept any
intermediate concept without justification. Then you rebuild the analysis
from these ground-level pieces upward.

**Why it is in this prompt:** Complex research questions carry inherited
vocabulary and framings that smuggle in unexamined assumptions. First-
principles decomposition forces each conceptual layer to earn its place.

**How to apply it — step by step:**
1. Write the research question in plain language.
2. For every noun or adjective in the question, ask: "What is this
   *really* — at the most fundamental level?" Replace the term with its
   decomposed components.
3. Iterate until the question is expressed only in terms of directly
   observable or logically necessary components.
4. Answer the decomposed version. Then translate back up to the original
   vocabulary, noting where the translation introduces assumptions.

**When to stop / escape criterion:** Stop decomposing when further
decomposition would no longer reveal new structure — typically after 2–3
layers.

**Example trigger in this research context:** The question "Is
[PLATFORM] a successful product?" decomposes into: what defines
"success" → revenue? adoption? retention? strategic position? — answer
each separately, then reassemble.

### Method: Base-Rate Anchoring

**What it is:** For every frequency, probability, or prevalence claim, you
anchor it against the **base rate** of the relevant reference population.
Specific cases are interpreted against general rates, not in isolation.

**Why it is in this prompt:** Representativeness bias causes research to
weight vivid specific examples over statistically-grounded base rates.
Anchoring reverses this by making the base rate primary.

**How to apply it — step by step:**
1. For every probability / frequency / "how common" claim, identify the
   **reference population** the claim is made against.
2. Find the base rate in that reference population.
3. State the specific claim **explicitly relative to** the base rate:
   "2x the base rate", "well below the base rate", "within the base-rate
   range".
4. If no base rate can be found, flag the claim as **unanchored**.

**When to stop / escape criterion:** Apply to every numerical frequency or
probability claim. Skip for purely qualitative observations.

**Example trigger in this research context:** "Company X had
[PLACEHOLDER] failures" is meaningless without the base rate: what is
the failure rate in comparable companies of similar size, industry,
and time period?

### Method: Adversarial Query Expansion

**What it is:** A standing directive that requires you — the executing
agent — to **autonomously expand the search vocabulary** at defined
checkpoints during the run. You are not bound to the query terms given
in the initial prompt; you are obligated to outgrow them. The purpose
is to prevent **local-minimum lock-in**, where the agent iterates within
a narrow semantic neighborhood of the user's phrasing and misses the
adjacent, opposing, or higher-abstraction evidence that would change
the answer.

**Why it is in this prompt:** The initial query vocabulary carries the
user's framing — including the user's blind spots. If your search stays
inside that vocabulary, your conclusions will be shaped by the same
blind spots. Critical thinking requires the queries themselves to be
critically expanded, not just the findings critically evaluated.

**How to apply it — step by step:**

1. **Build a Seed Query Set.** Your starting vocabulary for this run
   is `['agentic repo', 'complete refactoring', '12-type ontology', 'three placement modes', 'ULID convention', 'auto-generated readmes', 'audit graph', 'closed schemas', 'big-bang archive', 'governance waiver']` (extracted at composition time from the
   research question). Begin from this set; do not narrow it further.

2. **Expand along four axes at every major checkpoint.** After every
   batch of searches (or every 10 minutes of agentic time, whichever
   is sooner), generate new queries along each of these axes and
   execute the most promising one per axis:

   - **Adjacent axis** — synonyms, related sub-fields, neighbouring
     disciplines, equivalent industry terms, other-language terms.
     You generate `{{adjacent_term}}` candidates during the run.
     Example: "AI Act compliance" → "Rechtssicherheit KI",
     "algorithmic accountability".

   - **Opposing axis** — the negation, the failure case, the opposite
     school of thought, the "X doesn't work" literature. You generate
     `{{opposing_term}}` candidates during the run. Example: "benefits
     of microservices" → "microservices failure modes".

   - **Abstraction axis** — step one level up or down. Up: the category
     the topic belongs to. Down: a concrete sub-case. You generate
     `{{higher_level_term}}` and/or `{{lower_level_term}}` during the
     run. Example: "ChatGPT enterprise adoption" ↑ "LLM enterprise
     adoption"; ↓ "ChatGPT in pharmaceutical R&D".

   - **Orthogonal axis** — an angle the original framing did not
     consider at all. **For this run, the orthogonal lens is
     pre-specified by the user as: `The 6 orthogonal-lens questions L1-L6 (migrate-at-all, agent
identity, rollback, lock-vs-lock interaction, agent onboarding,
Gemini-as-dependency reproducibility) — Gemini MUST address
each at least once in §3 or §5.`.** Execute
     queries from that lens. (Other orthogonal lenses may also surface
     during the run; log them, but the pre-specified lens is the one
     you must invoke at minimum.)

3. **Log every expansion.** Maintain a **Query Expansion Log** in your
   working notes: for each expansion, record (a) the axis, (b) the new
   query, (c) whether the search returned novel findings not covered
   by the seed set, (d) whether those findings modified a tentative
   conclusion. This log is included in the final output's Synthesis
   section.

4. **Feed expansions back into hypotheses / schema fields.** If an
   expansion surfaces a finding that contradicts or enlarges the
   current working answer, treat it as a first-class input: re-run the
   relevant Restatement Checkpoint, update the Contradiction Log,
   consider whether it merits a new hypothesis branch (Category A),
   a new schema row (Category B), or a World-Change Log entry
   (Category C).

5. **Drive the expansion by reflection, not by token budget.** Before
   each expansion pass, pause and write one sentence answering:
   *"What am I most likely missing right now, and why?"* The answer
   selects which of the four axes to prioritize this pass.

**When to stop / escape criterion:** Stop expanding a single axis when
two consecutive expansions along that axis produce no novel findings.
Do not stop the method as a whole until every axis has been exhausted
in this sense. The full method only terminates at the Pre-Synthesis
Integrity Check.

**Example trigger in this research context:** Your seed vocabulary is
`['agentic repo', 'complete refactoring', '12-type ontology', 'three placement modes', 'ULID convention', 'auto-generated readmes', 'audit graph', 'closed schemas', 'big-bang archive', 'governance waiver']`. Your pre-specified orthogonal lens is
`The 6 orthogonal-lens questions L1-L6 (migrate-at-all, agent
identity, rollback, lock-vs-lock interaction, agent onboarding,
Gemini-as-dependency reproducibility) — Gemini MUST address
each at least once in §3 or §5.`. After the first search batch, you generate one
candidate per axis: adjacent (`{{adjacent_term}}`), opposing
(`{{opposing_term}}`), abstraction (`{{higher_level_term}}` or
`{{lower_level_term}}`), and execute one query from the orthogonal
lens. You log all four in the Query Expansion Log before continuing.

**Hard anti-rationalization rule:** If you catch yourself thinking *"the
seed vocabulary is already comprehensive"*, that is the signal to
expand — not the signal to skip. The feeling of completeness inside a
narrow vocabulary is precisely what the local-minimum failure feels
like from the inside.

## Steps and Replication Mechanisms

### Per-Step Restatement Checkpoint Template

Apply this template at the start of every step / iteration:

### Restatement Checkpoint — Before {{step_or_iteration_label}}

Before executing this step, I restate the currently-active constraints
verbatim:

- **CONSTRAINT BLOCK 0 — Reflection Baseline (Always Active):** [Paste the full text of the block here. Do not paraphrase.]
- **CONSTRAINT BLOCK 1 — Known Priors — VERBATIM from /migration/:** [Paste the full text of the block here. Do not paraphrase.]
- **CONSTRAINT BLOCK 2 — Temporal Scope:** [Paste the full text of the block here. Do not paraphrase.]
- **CONSTRAINT BLOCK 3 — Output Format + Exclusions:** [Paste the full text of the block here. Do not paraphrase.]

I also restate the currently-active critical-thinking methods:

- **Method: Adversarial Query Expansion** — [Paste the "How to apply" bullet list verbatim.]
- **Method: Falsification** — [Paste the "How to apply" bullet list verbatim.]
- **Method: Source Triangulation** — [Paste the "How to apply" bullet list verbatim.]
- **Method: Contradiction Log** — [Paste the "How to apply" bullet list verbatim.]
- **Method: What Would Change My Mind** — [Paste the "How to apply" bullet list verbatim.]
- **Method: Red Team / Devil's Advocate Review** — [Paste the "How to apply" bullet list verbatim.]
- **Method: First-Principles Decomposition** — [Paste the "How to apply" bullet list verbatim.]
- **Method: Base-Rate Anchoring** — [Paste the "How to apply" bullet list verbatim.]

I confirm these are active for the step below.

### {{step_or_iteration_label}} — {{step_title}}

{{step_content}}

### Batch Procedures

## BATCH PROCEDURE — per-axis-audit

You will execute the following procedure **exactly 12 times**,
once per item in this list:

1. Axis 1 Ontology (L11.32‴ + Q-O1/O2/O3)
2. Axis 2 Placement modes (L11.36′/L11.38′ + Q1)
3. Axis 3 ID conventions (L11.43 v2+v3 + Decision 4 + Q4)
4. Axis 4 Storage (L11.37′ + Q-St1/St2/St3)
5. Axis 5 Tooling (L11.39′ + Q-T1/T2/T3)
6. Axis 6 Workflows (Q2/Q3 + Q-W1/W2/W3)
7. Axis 7 Governance (Q-G1/G2/G3)
8. Axis 8 Hooks (L11.41′ + Q-H1/H2/H3)
9. Axis 9 Migration mechanics (Q-M1/M2/M3)
10. Axis 10 Observability (Q-Ob1/Ob2/Ob3)
11. Axis 11 Skill packaging (Q-Sk1/Sk2)
12. Axis 12 Schema design (L11.42 + Q-S1/S2/S3 + Q5)

For each iteration, you execute the steps below **in full**, including
the Restatement Checkpoint and the Reflection entry. Do not batch-skip
either. Do not summarize across items until all iterations are complete.

---

### Iteration Template — Apply to Each Item in Turn

**Restatement Checkpoint — Before Iteration [i] for Item [ITEM i]**

[Paste the full Restatement Checkpoint template from
`m2-restatement-checkpoint.md`.]

**Reflection Entry — Iteration [i]**

[Paste the five-question reflection template from CONSTRAINT BLOCK 0.
Minimum: Q1, Q3, Q5 per iteration. Q2 and Q4 at least every third
iteration.]

**Iteration [i] Steps:**

1. Apply M13 Adversarial Query Expansion to the item.
2. Apply each category-default method (M06, M07, M08, M12 etc.) to the item per its protocol.
3. Populate the per-iteration output schema below.

**Iteration [i] Output Schema (fill all fields):**

- Axis label: [...]
- First-principles derivation (M10): [...]
- ≥5 SoTA citations (M06): [...]
- Base-rate prevalence (M12): [...]
- Counter-arguments per lock (M01 + M09): [...]
- WWCMM conditions (M08): [...]
- Contradictions vs migration (M07): [...]
- Lifecycle audit (b-into-c): [...]
- Confidence: {{confidence_label}}

You may not proceed to Iteration [i+1] until Iteration [i]'s output
schema is fully populated.

### Cross-Pollination Steps

### Step [i.b] — Surviving-Branch Triangulation (cross-pollination from Category B)

This step imports one extraction discipline from Category B because
an exploration that ends with a "most likely" hypothesis, without
triangulating the evidence under that hypothesis, has produced a
narrative — not a finding.

Perform the following **once the hypothesis tree has produced a
surviving branch** (a hypothesis with net-positive evidence after
falsification attempts, per Method M01):

1. **Lock a mini-schema for the surviving branch.** For the surviving
   hypothesis, write a small structured schema:
   - Claim: [one-sentence statement of the surviving hypothesis]
   - Key evidence 1: [source + finding]
   - Key evidence 2: [source + finding]
   - Key evidence 3: [source + finding]
   - Strongest counter-evidence: [source + finding]
   - Confidence: [LOW / MEDIUM / HIGH]
   - What-would-change-my-mind: [concrete future observation]

2. **Force triangulation on the top three evidence items.** Each must
   trace to at least two independent sources (primary + confirmation)
   — not aggregator-chains. If any item is single-source, flag the
   surviving branch as **single-source-supported** rather than
   confirmed. Apply Method M06 (Source Triangulation) here as if the
   primary category were B.

3. **Do not hybridize.** The hypothesis tree structure (Category A
   core) remains. This schema is attached **below** the tree in the
   output, not in place of it.

### Step [i.b] — Per-Session Locked Schema (cross-pollination from Category B)

This step imports one extraction discipline from Category B because
lifecycle research without a locked per-session schema slowly degrades
into a journal: every session has a slightly different shape, and after
six months the cross-session comparison the user actually wanted is
impossible to reconstruct.

Perform the following at every session, immediately after the
Resumption Protocol and before any new search:

1. **Re-anchor the per-session schema.** The persistent knowledge
   store defines a fixed per-session record schema (see the Knowledge
   Store Schema in this prompt). Restate the schema verbatim at the
   start of every session. Do not silently extend or shrink it.

2. **Treat each session as one batch iteration.** Apply Replication
   Mechanism M3 (Batch-Explicit Framing) with cardinality = 1 per
   session. The session output is one record that fully populates
   every schema field, including the explicit "not-found — [reason]"
   marker for any field that genuinely cannot be filled this session.

3. **Cross-session diff.** Before closing the session, run a B-style
   diff between this session's record and the previous session's
   record on the same schema fields. Surface the diff in the
   Session-End Summary as a structured list:
   - Fields unchanged: [...]
   - Fields with new evidence: [...]
   - Fields whose values reversed since last session: [...] (these
     escalate into the World-Change Log per Method M07).

4. **Do not hybridize.** The Resumption Protocol, Compaction
   Protocol, and Assumption-Decay Audit (Category C core) remain in
   place. The locked schema sits inside the per-session record;
   it does not replace the lifecycle scaffolding.

## PRE-SYNTHESIS INTEGRITY CHECK

Before writing the final synthesis, execute this verification pass in
writing. Each item produces a written line; "done" by memory does not
count.

1. **Re-read Constraint Blocks 0–[N] verbatim.** Confirm in writing:
   *"I have re-read each constraint block and they are all still
   active."*

2. **Re-read the critical-thinking method blocks.** Confirm in writing:
   *"Each method listed below is active and I have applied it:
   [enumerate methods, including M13 Adversarial Query Expansion]."*

3. **Reflection audit (CONSTRAINT BLOCK 0).** Count the reflection
   entries written during this run. Confirm: *"I wrote [K] reflection
   entries at the following checkpoints: [enumerate]."* If K is below
   the minimum required by CONSTRAINT BLOCK 0, write the missing
   reflections **now** before continuing.

4. **Query-expansion audit (M13).** Confirm in writing: *"Method M13
   Adversarial Query Expansion was invoked [N] times across the four
   axes (adjacent / opposing / abstraction / orthogonal). The Query
   Expansion Log contains [M] entries, of which [P] produced novel
   findings that modified tentative conclusions."* If N = 0, the
   research is incomplete — run at least one pass before proceeding.

5. **Cross-pollination audit.** Confirm in writing: *"Steps adapted
   from the two non-primary categories were executed as follows:
   [enumerate the cross-pollinated steps]."* If none were executed,
   the generated prompt did not honor Phase 2b — halt and report.

6. **Constraint-compliance audit.** For each constraint block (0
   through N), check the accumulated findings and cite one specific
   example of how you honored it. If you cannot cite a specific
   example, flag the constraint as **not-demonstrably-honored**.

7. **Scope audit.** Confirm: *"All findings are within the temporal
   scope defined in Constraint Block 2."* If any are outside, flag
   and remove.

8. **Exclusion audit.** Confirm: *"None of the findings or
   recommendations fall into the exclusion list in Constraint Block
   3."*

Only after all eight items are complete in writing may you begin the
Synthesis section.

## SYNTHESIS — Final Output

You have completed the Pre-Synthesis Integrity Check. Now write the
synthesis filling the schema below. Every section is required unless
explicitly marked optional.

---

### Executive Summary
1–2 paragraphs. The single most important finding plus the next-most
important. No more than 200 words.

### Key Findings
Numbered list of the principal findings, each with:
- The finding in one sentence
- Confidence level (LOW / MEDIUM / HIGH)
- Top 2-3 sources by relevance
- Any caveats or single-source flags

### Output Matrix (Category B — Extraction)
Render the comparison/extraction matrix per the Expectations section. Every row gets the full per-iteration schema; gaps marked explicitly as 'not found — [reason]' rather than silently omitted.

### Contradictions Encountered
From your Method M07 Contradiction Log. For each contradiction:
- The two (or more) conflicting claims
- The sources
- Your characterisation of *why* the disagreement (methodology /
  time period / definitional / genuine empirical dispute)
- What additional evidence would resolve it

If no contradictions: write *"No contradictions encountered during this
research"* — but only after explicitly checking. Silence here without
verification is a Method M07 violation.



### Query Expansion Log (Method M13)
The full log of adversarial query expansions. For each expansion entry:
- Axis (adjacent / opposing / abstraction / orthogonal)
- The new query
- Whether the search returned novel findings not covered by the seed
- Whether those findings modified a tentative conclusion

This section is mandatory regardless of category. An empty log indicates
M13 was not invoked, which is a Pre-Synthesis Integrity Check failure
(item 4) that must be repaired before delivery.

### Reflection History (Constraint Block 0)
All reflection entries written during this run, in chronological order,
verbatim as written. This includes:
- Kickoff reflection
- Mid-run reflection
- Post-Query-Expansion reflections (one per M13 pass)
- Pre-synthesis reflection
- Post-synthesis reflection (written *after* this Synthesis is drafted,
  appended below)

Reflections were written in writing during the run. If any are missing
here, the run is incomplete.

### Cross-Pollination Log (Phase 2b)
The two cross-pollinated steps from Phase 2b — what they returned and
whether they modified the final answer. Format per import:
- Source category (A / B / C)
- Step ID and title
- What it surfaced
- Did it change the conclusion? (yes / no / partially — explain)

### Open Questions / Unresolved
What this research could *not* settle. Be explicit. "We do not know"
is a legitimate finding when documented honestly.

### Sources
Structured source list:
- **Primary sources** first (peer-reviewed, official, primary documents)
- **Secondary sources** next (analyses, reports with editorial accountability)
- **Aggregators** last (only if used as discovery aids, not as evidence)

For each source: title, author/org, date, URL/citation, type tag.

### Methodology Note
Brief audit:
- Which critical-thinking methods were applied (refer by short anchor)
- Which methods were active for which findings
- Any "unanchored" / "single-source" / "unable to steelman" flags
- Total search iterations
- Any Pre-Synthesis Integrity Check items that flagged

This methodology note is the auditability handle — it is what allows
a reader to assess the trustworthiness of the synthesis without
re-running the research themselves.

## SELF-VERIFICATION CHECKLIST (11 items)

Before you deliver the Synthesis, verify each of these in writing.
A "done" by memory does not count — write one line per item
confirming you completed it.

- [ ] **1. Restatement integrity.** Every major step began with a
      verbatim Restatement Checkpoint that included CONSTRAINT BLOCK 0
      first, followed by all other active CBs and all active methods
      (with M13 always present).

- [ ] **2. Reflection regime (CONSTRAINT BLOCK 0).** All five mandatory
      reflection checkpoints were honored in writing: Kickoff, Mid-run,
      Post-Query-Expansion, Pre-synthesis, Post-synthesis. Confirm:
      *"I wrote [N] reflection entries at the following checkpoints:
      [enumerate]."* If N is below 5, write the missing reflections
      now before continuing.

- [ ] **3. Method invocation audit.** Every method listed in the active
      methods palette has at least one concrete invocation visible in
      the Reason history. Methods with zero invocations are flagged
      in the Methodology Note as "active but not invoked — likely
      inappropriate for this run".

- [ ] **4. Adversarial Query Expansion (M13).** M13 was invoked along
      all four axes (adjacent / opposing / abstraction / orthogonal)
      at least once each. The Query Expansion Log is populated with
      ≥ 4 entries. Confirm: *"M13 was invoked [N] times; the orthogonal
      axis (`The 6 orthogonal-lens questions L1-L6 (migrate-at-all, agent
identity, rollback, lock-vs-lock interaction, agent onboarding,
Gemini-as-dependency reproducibility) — Gemini MUST address
each at least once in §3 or §5.`) was used [M] times."* If N=0 or M=0,
      run a final pass before proceeding.

- [ ] **5. Cross-pollination audit.** Both cross-pollinated steps
      (Phase 2b — one from each non-primary category) were executed
      and logged. Confirm: *"Cross-pollination steps adapted from
      Categories X and Y were executed as follows: [enumerate]."* If
      none were executed, the generated prompt did not honor Phase 2b —
      halt and report.

- [ ] **6. Source triangulation (where M06 active).** Every factual
      claim has been through Source Triangulation with ≥ 3 independent
      sources, or is explicitly flagged as **single-source**. Aggregator-
      chains do not count as multiple sources.

- [ ] **7. Contradiction Log populated.** The Contradiction Log section
      of the Synthesis has been written. If no contradictions were
      encountered, the section explicitly states *"No contradictions
      encountered during this research"* — written only after a
      verification pass, never as a default placeholder.

- [ ] **8. Temporal scope honored.** All findings are within the
      temporal scope defined in CONSTRAINT BLOCK 2. Anything outside
      has been removed.

- [ ] **9. Output exclusions honored.** None of the findings or
      recommendations fall into the exclusion list in CONSTRAINT
      BLOCK 3. Verify by reading each finding against the exclusion
      list.

- [ ] **10. Pre-Synthesis Integrity Check (M4) executed in writing.**
      All 8 items of the M4 check were completed before the Synthesis
      was drafted. The check is in the working notes; it is not
      retrofitted after the fact.

- [ ] **11. Synthesis sections complete.** The Synthesis contains:
      Executive Summary · Key Findings · category-specific main body ·
      Contradictions · Query Expansion Log · Reflection History ·
      Cross-Pollination Log · Open Questions · Sources · Methodology
      Note. Any missing section is a blocker; write it before delivery.

If any checkbox fails, repair before delivery. Do not deliver a
Synthesis with failing items. The user will read this checklist
state in the Methodology Note — partial completion is visible.

---

*End of research prompt — generated by research-prompt-optimizer v3.2.0 at 2026-05-13T19:30:00+02:00.*
