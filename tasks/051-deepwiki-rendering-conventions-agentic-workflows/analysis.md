---
type: note
status: active
slug: deepwiki-conventions-analysis
summary: "Cross-reference of the Gemini DeepWiki research result against this repository's governance posture: ten findings (R1–R10) covering conventions audit, benchmark dichotomy, agentic economics, open-source alternatives, and compliance — with explicit citations into research/gemini/deepwiki-rendering-conventions-agentic-workflows/result.md."
created: 2026-05-07
updated: 2026-05-07
---

# Task 051 Analysis — DeepWiki Rendering, Conventions, Agentic Workflows

## 0. Method and Citation Convention

The analysis is a five-scope cross-reference between the Gemini external research result and this repository's current governance corpus (the nine root specs, `decisions/0001-..0005-`, `research/adr-assumption-audit/output/REPORT.md`, the ADR pipeline at `tools/adr/`). Citations into the Gemini result use the form `result.md:Lstart-Lend` and refer to [`research/gemini/deepwiki-rendering-conventions-agentic-workflows/result.md`](../../research/gemini/deepwiki-rendering-conventions-agentic-workflows/result.md). Citations into our own corpus use `path:Lstart-Lend` against the file's current commit.

Each finding has the shape `R<n> [tier] — <title> — <recommendation>`. Tiers:

- **A — Adopt:** the Gemini recommendation already aligns with our posture or is straight-forwardly compatible; act on it.
- **G — Gap:** a real, addressable gap; file a follow-up Task or amendment.
- **N — Not applicable:** the recommendation does not transfer to a spec-first governance repo, or it is already solved by an isomorphic local mechanism.

---

## 1. Conventions Audit (`.devin/wiki.json`, `llms.txt`, `AGENTS.md`)

### R1 [A] — Adopt `.devin/wiki.json` for deterministic DeepWiki steering

The Gemini result frames `.devin/wiki.json` as a "high-level system prompt that overrides the indexer's default clustering logic" (`result.md:41`) and warns that unsupervised indexing of complex repos hallucinates — citing the LibreOffice-Buck case (`result.md:39`). For `netzkontrast/agency`, the failure mode is acute: the repo deliberately partitions governance (root specs + `/tasks/` + `/prompts/` + `/research/`) from the product layer (`/Agency-System/`), and a default indexer would conflate the two. The 30-page standard limit (`result.md:60`) is also the binding constraint for our ≈ 50 root-level files plus dozens of operational folders.

**Recommendation:** Task 052 produces `.devin/wiki.json` with explicit `repo_notes` (M·A·S map + spec-first declaration) and a 16-page hierarchy. This R1 is the upstream rationale; Task 052 is the implementation.

### R2 [G] — `llms.txt` is not yet generated, and we should not generate it from `.devin/wiki.json` alone

The Gemini result distinguishes two purposes (`result.md:66-72`):

- `llms.txt` is a *human-summary* index for LLM consumption ("highly condensed map of the repository's landscape").
- `AGENTS.md` is a *strict-operational-boundary* file for autonomous entities ("exact build, test, and run commands … operational boundaries").

Our `AGENTS.md` already covers the second purpose (and goes further with RFC 2119 + Gherkin acceptance criteria). We have no `llms.txt`. DeepWiki auto-generates one from the wiki (`result.md:66`) but that index would lag the repo by however long the indexer takes to re-run.

**Recommendation:** Do not file an amendment Task to author a hand-rolled `llms.txt` ahead of `.devin/wiki.json` adoption. The DeepWiki-generated `llms.txt` is downstream of `.devin/wiki.json`; let Task 052 land first, observe the auto-generated `llms.txt`, then decide whether to file Task 053 to author a richer in-house `llms.txt`. This is a *deferred* gap, not an immediate one.

### R3 [A] — `AGENTS.md` already exceeds the Gemini-cited best practices

The Gemini result lists `AGENTS.md` requirements (`result.md:70-72`): exact build/test/run commands, operational boundaries, tiered structure (root + nested), human-in-the-loop authorization for dangerous operations.

Our `AGENTS.md` covers all of this and adds:

- RFC 2119 normative keywords with mechanical polarity-inversion linting (`tools/check-rfc2119-polarity.py`).
- Gherkin acceptance criteria as binding scenarios (six in `AGENTS.md` alone).
- Frontmatter Ontology (Layered Schema with Namespacing) routing every operational file.
- Closing Run Procedure (`/sc:createPR` rules CR.1–CR.6) — the strict authorization boundary the Gemini result calls for, formalized.
- ADR governance: a synthesis pipeline (`<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->`) that *re-writes* a section of `AGENTS.md` from the `decisions/` corpus, mechanically enforced.

We do not have nested `AGENTS.md` files inside subfolders (the Gemini-recommended tiered approach, `result.md:72`). Our equivalent: per-folder `readme.md` + the `prompts/<slug>/{prompt.md,brief.md,readme.md}` mandatory three-file scaffold. The two patterns are isomorphic; ours is more strictly enforced. **No action needed.**

---

## 2. Benchmark Cross-Reference (ProdE vs DeepWiki — Human/Agent Utility Dichotomy)

### R4 [A] — Confirm the human-audience optimisation target for `.devin/wiki.json`

The Gemini benchmarks (`result.md:113-118`) reveal a sharp dichotomy: DeepWiki scores 8.1/10 on Presentation (humans) but only 7.1/10 on Referencing (agents); ProdE achieves 9.0/10 on both. The second-order insight (`result.md:120`): "deploying [DeepWiki] as the sole contextual layer for autonomous multi-file editing agents may induce higher error rates due to the dramatically reduced retrieval surface area."

For *this* repository the audience analysis is straightforward:

- **Human audience for DeepWiki:** new contributors trying to understand the spec-first governance model; reviewers asking "how is this repo organised?"; auditors verifying compliance traceability (R9 below).
- **Agent audience:** Claude Code agents already work directly off the source files — `AGENTS.md`, `TASK.md`, frontmatter — not the rendered wiki. The wiki is *not* the agent's primary navigation surface here.

**Recommendation:** Task 052 explicitly optimises for human readability while making one concession to agent utility — every `purpose` field cites at least one exact file path or directory name. This concession survives even though DeepWiki itself will not be the agent's surface.

### R5 [G→Tracked] — Maintain explicit-citation density via the existing audit-graph rather than chasing ProdE

ProdE's edge comes from a 4,008-source-citation density (`result.md:116`) that DeepWiki cannot match because it documents only 25–44 files per repo (`result.md:115`). For our repository the equivalent of ProdE's density is the *frontmatter audit graph* (`task_uses_prompts`, `prompt_relates_to_task`, `research_executes_prompt`, `prompt_spawned_from_research`) plus the citation form `path/to/file.ext:Lstart-Lend@<sha>` mandated by `AGENTS.md "Citation Reproducibility Protocol"`.

In other words: we already encode ProdE-style retrieval density into a different layer (frontmatter + linters), not into a generated wiki. **No action needed; record the alignment.** This finding is the rationale for why we do not pursue ProdE adoption: we already have its substance.

---

## 3. Agentic Economics (ACU Planning-Execution Separation)

### R6 [A] — Our Prompt → Research → Task pipeline already enforces planning-execution separation

The "Ask Devin" model (`result.md:74-84`) separates a *low-cost planning surface* (vector search over the pre-rendered wiki) from the *high-cost execution surface* (sandbox + multi-file edits + tests). The 10-ACU degradation threshold (`result.md:78`) is the empirical justification.

Our isomorphic structure:

| Devin layer | This repo | Cost characteristic |
|---|---|---|
| Pre-indexed DeepWiki | `tools/fm/query.py`, `tools/dramatica-nav/nav.py`, `frontmatter audit graph` | Stateless, near-zero cost — single-file reads. |
| Ask Devin (planning) | `/prompts/<slug>/{brief.md,prompt.md}` + `/tasks/<NNN>-<slug>/task.md` | Tokens-only; no sandbox, no git side effects. |
| Devin Agent Mode (execution) | A Claude Code session that *executes* the prompt and produces `/research/<slug>/output/SPEC.md` | Sandbox + git + ACUs proportional to scope. |
| Devin Review | `review` skill, `ultrareview`, `/sc:reflect` | Diff-bounded; cheaper than re-execution. |

The two pipelines are isomorphic. **Recommendation:** Document the alignment as a `repo_notes` entry in `.devin/wiki.json` (Task 052 N3 already covers this — "the Prompt → Research → Task pipeline is the core workflow"). No further amendment Task is needed.

### R7 [G] — The 10-ACU degradation threshold is a useful budget hint we do not currently encode

The Gemini result identifies a hard quality cliff at 10 ACUs per session (`result.md:78`). Our equivalent metric is *context-window saturation* (which CLAUDE.md §7 mentions but does not quantify) plus *iteration count*. Tasks 008 (coherence baseline protocol) and 044 (improve maintenance spec) touch the issue obliquely but do not encode an explicit budget.

**Recommendation:** This is a deferred gap — file as part of Task 044 / Task 047 follow-ups rather than a new amendment Task. The Task 052 reflection logs this as a known mitigation gap; the immediate value is the awareness, not the encoding.

---

## 4. Open-Source Alternatives (`deepwiki-open`, `deepwiki-rs`/Litho)

### R8 [N] — Neither alternative warrants adoption today; revisit when DeepWiki-generated docs prove insufficient

The Gemini result distinguishes (`result.md:122-140`):

- **`deepwiki-open`** — Python/FastAPI + TypeScript/Next.js, provider-agnostic via `generator.json`/`embedder.json`/`repo.json`. Defining feature: composable model architecture (Gemini, OpenAI, Azure, Ollama).
- **`deepwiki-rs` (Litho)** — Rust, C4-model, deterministic AST parsing, "analyze once benefit everywhere" caching via `.litho/`.

**Recommendation:** *Defer.* Three reasons:

1. **Data sovereignty is not currently violated.** This repo is public on GitHub; `result.md:124` cites privacy as the primary driver for self-hosting. We have no proprietary IP at risk.
2. **Operational overhead is non-trivial.** `deepwiki-open` requires hosting a FastAPI/Next.js stack; `deepwiki-rs` requires Rust toolchain + C4-model adoption. Neither aligns with our Python-stdlib-only tooling discipline (CLAUDE.md §6).
3. **`.devin/wiki.json` adoption is reversible.** If hosted DeepWiki proves insufficient or the cost model changes, both alternatives will still exist; the `.devin/wiki.json` file we ship in Task 052 is a portable artifact (it's just JSON with `repo_notes` and `pages`) and should map cleanly onto either alternative.

This is the clearest **N — not applicable today** finding in the analysis. Record the rationale; do not file a Task.

---

## 5. Compliance Implications (EU AI Act, U.S. Algorithmic Accountability Act)

### R9 [A] — Our audit graph is already compliance infrastructure; the wiki extends it for human auditors

The Gemini result frames AI-generated wikis as "foundational compliance infrastructure" (`result.md:162`): tamper-evident audit trails linking architectural claims to time-stamped source citations. The transparency paradox (`result.md:164`) — that excessive structural exposure aids adversaries — is managed via zero-data-retention and customer-managed encryption keys.

For us, the audit-graph is *already* the compliance trail:

- Every `Accepted` ADR in `decisions/<NNNN>-<slug>.md` is T4-immutable (CLAUDE.md §8).
- The `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` block in `AGENTS.md` is a tamper-evident, machine-rewritten bridge from raw decisions to the binding agent contract.
- `tools/lint-linkage.py` enforces frontmatter linkage; `tools/lint-runlog.py` enforces maintenance-run records.
- The friction-log + `tools/check-trust.py` chain ensures no `task_status: done` is achieved without a traceable FL declaration.

**Recommendation:** Surface these mechanisms in `.devin/wiki.json` page #15 ("How We Got Here" → `decisions/0001-0005`, `maintenance/run-log.md`, Tasks 032–039 amendment chain). This is the compliance-infrastructure narrative for human auditors; Task 052 already plans this page. **Adoption is automatic via Task 052; no further action.**

### R10 [N] — The transparency-paradox concession does not bind us today

The Gemini result warns that exposing "excessive internal code structure" can aid adversaries (`result.md:164`). For our repository this concession is moot: we have no proprietary algorithms, no production credentials, no PII. The repo is by design fully transparent. **Record and dismiss.** This finding is included for completeness; no recommendation.

---

## 6. Synthesis Table — Findings Index

| ID | Tier | Scope | Title | Action | Owner |
|---|---|---|---|---|---|
| R1 | A | Conventions | Adopt `.devin/wiki.json` for deterministic steering | Already implemented by Task 052 | Task 052 |
| R2 | G | Conventions | `llms.txt` deferred until DeepWiki auto-gen lands | Observe post-Task-052; possibly file Task 053 | Maintainer |
| R3 | A | Conventions | `AGENTS.md` already exceeds best practices | None — record alignment | — |
| R4 | A | Benchmarks | Confirm human-audience optimisation target | Implemented by Task 052 page-budget choice | Task 052 |
| R5 | G→T | Benchmarks | Citation density already encoded in audit graph | None — record alignment | — |
| R6 | A | Economics | Planning/execution separation already isomorphic | `repo_notes` N3 in `.devin/wiki.json` | Task 052 |
| R7 | G | Economics | 10-ACU degradation budget not encoded | Defer to Task 044/047 follow-up | Maintainer |
| R8 | N | Alternatives | `deepwiki-open` / `deepwiki-rs` defer | None — record dismissal | — |
| R9 | A | Compliance | Audit graph IS our compliance trail | Page 15 in `.devin/wiki.json` | Task 052 |
| R10 | N | Compliance | Transparency-paradox concession moot | None — record dismissal | — |

**Tier counts:** A = 5, G = 3 (one tracked, two deferred), N = 2.

**Open-questions audit:** zero open questions warrant a follow-up prompt under `/prompts/`. Every gap is either (a) absorbed by Task 052 deliverables, (b) explicitly deferred with a tracked owner, or (c) dismissed with rationale. This satisfies `RESEARCH.md §4 step 9` ("file new prompts for unresolved questions") trivially — no new prompts needed.

---

## 7. Hand-off to Task 052

Task 052 must encode the following from this analysis:

1. **`repo_notes[0]`** = the verbatim Machine · Actor · Space map (Task 052 task.md already specifies this).
2. **`repo_notes[1]`** = spec-first declaration (Task 052 N2).
3. **`repo_notes[2]`** = Prompt → Research → Task pipeline narrative (Task 052 N3 — directly downstream of R6).
4. **`repo_notes[3]`** = the 032–039 amendment chain context (Task 052 N4 — directly downstream of R9).
5. **`repo_notes[4]`** = Agency-System product-layer separation (Task 052 N5 — directly downstream of R1's hallucination-prevention rationale).
6. **Page 15 ("How We Got Here")** — must reference `decisions/0001-0005`, `maintenance/run-log.md`, and the 032–039 amendment chain (R9 mandate).
7. **Page 4 ("Machine · Actor · Space Map")** — the centrepiece page; downstream of R6's isomorphism finding.
8. **Pre-mortem mitigations in `reflection.md` §3** — must include "indexer conflates governance with product layer" (downstream of R1) and "indexer documents only 25–44 files, missing supporting infrastructure" (downstream of R4).

Task 052 picks up here.
