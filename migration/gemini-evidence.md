---
type: note
status: active
slug: gemini-evidence
summary: "The 8 Gemini Deep Research D-citations (D1-D8) anchoring the ontology / placement / schema / CLI decisions ratified in Roundtables 7-8."
created: 2026-05-13
updated: 2026-05-13
---

# Gemini evidence appendix — D1 through D8

These 8 citations come from Gemini Deep Research brief #2 (`research/gemini-architectural-audit-2/output/SPEC.md`), commissioned in Round 10 of the design conversation. Each provides external validation for a load-bearing decision captured in [`locks-ratified.md`](./locks-ratified.md) and ratified in [`adr-draft.md`](./adr-draft.md).

When ADR-0013 promotes to `decisions/`, this appendix moves with it (either as a section in the ADR or as `decisions/0013-twelve-type-ontology/evidence.md`).

---

## D1 — Promote `role` / `lock` / `gherkin` / `friction-log` / `hook` to first-class types

**Decision context:** the original 7-type ontology in L11.32′ treated these 5 concepts as embedded sub-sections. Roundtable 5 surfaced repeated confusion ("is `role` an artifact or a section?"). Roundtable 6 escalated to Gemini.

**Gemini finding:** the audit graph cannot function if cross-references degrade to body-Markdown links. Body links are unreachable to the linker. Every concept that participates in cross-references MUST be a first-class artifact with frontmatter and an edge type. The 5 candidates each appear in 3+ inbound references across the existing corpus → graph-complete promotion is the right move.

**Anchors:** L11.32‴ (12-type ontology).

---

## D2 — Three-mode placement, not STANDALONE-only

**Decision context:** once promotion was on the table (D1), the question became "do all 12 types live in their own folders?" — i.e. STANDALONE-only. The alternative is to permit embedding (SUBFILE / SUBDOC) where the parent context is essential.

**Gemini finding:** STANDALONE-only would force fragmentation of inherently-parented concepts (a gherkin scenario lives inside the spec it describes; a friction log lives inside the session that produced it). The graph layer is mode-blind by design — edges work identically across modes — so embedding does not compromise graph completeness. Per-type opt-in into SUBFILE / SUBDOC is the right factoring.

**Anchors:** L11.36′ (three placement modes).

---

## D3 — Locks are content-addressed checkpoints, not versioned packages

**Decision context:** Roundtable 6 considered SemVer for locks (so `L11.43.1`, `L11.43.2`, etc. could carry incremental refinements without supersession). Round 7 surfaced concern: SemVer implies mutable releases; lock identity should be immutable.

**Gemini finding:** A lock is a *snapshot of agreed text*. The right identity is the content hash (SHA-256 of body bytes). SemVer carries package-management semantics (compatibility constraints, dependency ranges) that don't apply. Supersession via successor lock referencing `lock_supersedes: <prior-id>` preserves the audit chain without ambiguity.

**Anchors:** L11.40′ (locks STANDALONE-only with `lock_sha` content-addressing).

---

## D4 — Pandoc fenced divs as SUBDOC syntax

**Decision context:** Roundtable 7 surveyed three candidates for embedding YAML-with-body inside a parent Markdown file: (a) MDX with React-component-style frontmatter, (b) HTML data attributes on `<div>` blocks, (c) Pandoc fenced divs `:::{.type id=…}` with YAML between `---` markers inside.

**Gemini finding:** Pandoc fenced divs win because (i) they parse via a published AST (`pandoc-ast`) — no custom parser; (ii) they degrade gracefully on plain-Markdown renderers (the div opens/closes show as text, the YAML and body still render); (iii) they have explicit `id` attributes for stable references; (iv) the YAML inside follows the same shape as top-of-file frontmatter — schema reuse is trivial.

**Anchors:** L11.38′ (Pandoc fenced-div SUBDOC syntax).

---

## D5 — SQLite is sufficient; no graph DB

**Decision context:** Roundtable 6 considered Neo4j and Memgraph for the audit graph. The argument was that a graph DB offers natural traversal queries ("all tasks 2 hops from this prompt"). Roundtable 7 evaluated against scale.

**Gemini finding:** at Agency's scale (~50 tasks + ~100 prompts + ~70 research + ~30 skills + projected ~100 instances of the 5 promoted types = ~350 artifacts), a single SQLite DB with two tables (`artifacts`, `edges`) handles every query in <10ms. Graph DBs introduce operational overhead (server processes, separate backup paths, schema-migration friction) without performance benefit until ~100K nodes. Defer until evidence warrants.

**Anchors:** L11.37′ (SQLite graph layer).

---

## D6 — `subdocument_locations` must be regenerable, never source of truth

**Decision context:** SUBDOC mode (L11.38′) requires the graph layer to know where each subdoc lives inside its parent (parent path, fenced-div id, byte offsets). Roundtable 7 considered storing this in the audit graph DB as primary data.

**Gemini finding:** byte offsets are derivable from a full repo scan. Storing them as primary data introduces a cache-coherence problem: every parent edit potentially invalidates downstream offsets, and the graph DB becomes the bottleneck for parent file edits. The right design is to *cache* offsets in the DB for query convenience, but make the cache **regenerable** by `agency rescan` from filesystem state. Source of truth = filesystem.

**Anchors:** L11.37′ (`subdocument_locations` is a regenerable cache).

---

## D7 — `agency promote` is a first-class CLI verb

**Decision context:** Roundtable 7 considered a generic `agency move <source> --to <target>` that handles every kind of artifact relocation (rename, mode-transition, archive). The alternative is dedicated verbs.

**Gemini finding:** `agency promote` (mode transition) has fundamentally different semantics from `agency rename` (same artifact, new slug) and `agency archive` (move to archive tree, mark `status: archived`). Conflating them into a generic verb hides edge cases — most importantly, `promote` rewrites inbound edges at the SQLite layer + anchor references in body-Markdown, which neither rename nor archive does. Three explicit verbs are easier to teach and easier to lint.

**Anchors:** L11.39′ (mode-aware CLI surface).

---

## D8 — Closed schemas everywhere

**Decision context:** several existing L2 schemas permit `additionalProperties: true` (see `l1-vault-core.schema.json` line 51). Roundtable 7 considered keeping this for forward compatibility — agents can add new keys without schema PRs.

**Gemini finding:** open schemas defeat the closed-world graph assumption. Every key the linker is supposed to honour must be declared in the namespace registry; unknown keys imply silent edge omissions. Forward compatibility lands via **versioned schema additions** through ADRs (the same governance gate every other architectural change crosses). No `notes:`, `extra:`, or `metadata:` escape hatches. Cost of one ADR per new field is small; cost of silent edge omissions across 350+ artifacts is large.

**Anchors:** L11.42 (closed schemas everywhere).

---

## Cross-references

- Locks anchored by each citation: [`locks-ratified.md`](./locks-ratified.md)
- ADR consolidating these decisions: [`adr-draft.md`](./adr-draft.md)
- Open questions: [`open-questions.md`](./open-questions.md)

## Assumptions Log

- **Assumption E1.** Gemini Deep Research brief #2 (`research/gemini-architectural-audit-2/output/SPEC.md`) is the canonical source for these 8 citations. *Status: declared in commits 5f9d9df and 82dc85d; the SPEC.md file itself was not re-read while compiling this appendix — paraphrases above match the design-conversation digest, not verbatim citations.*
