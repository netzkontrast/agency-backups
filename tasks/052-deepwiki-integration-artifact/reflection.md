---
type: note
status: active
slug: deepwiki-integration-artifact-reflection
summary: "Five-question reflection grounded in the Gemini DeepWiki research result + Task 051 analysis. Establishes the audit trail for every repo_notes entry and pages entry in .devin/wiki.json: which conventions apply, page-budget validation, M03 pre-mortem failure modes, human-vs-agent utility tradeoff, and Machine/Actor/Space isomorphism check."
created: 2026-05-07
updated: 2026-05-07
---

# Task 052 Reflection — DeepWiki Integration Artifact

## 0. Inputs

- Gemini result: [`research/gemini/deepwiki-rendering-conventions-agentic-workflows/result.md`](../../research/gemini/deepwiki-rendering-conventions-agentic-workflows/result.md). Citations as `result.md:Lstart-Lend`.
- Task 051 analysis: [`../051-deepwiki-rendering-conventions-agentic-workflows/analysis.md`](../051-deepwiki-rendering-conventions-agentic-workflows/analysis.md). Citations as `analysis.md:R<n>`.
- Repository corpus: nine root specs (`AGENTS.md`, `TASK.md`, `RESEARCH.md`, `PROMPT.md`, `FOLDERS.md`, `SKILLS.md`, `FRUSTRATED.md`, `MAINTENANCE.md`, `PRE_COMMIT.md`), `decisions/0001-0005`, the spec-first audit graph.

This reflection is the audit trail for [`/.devin/wiki.json`](../../.devin/wiki.json). Every `repo_notes` entry and every `pages` entry must trace back to a finding (analysis R-id) or a mitigation (this document's M-id) below.

---

## 1. Q1 — Which `.devin/wiki.json` conventions apply directly to this repo?

The Gemini result documents two configuration arrays (`result.md:45-55`):

- `repo_notes` — array of `{content, author?}` objects; injects high-level context into the LLM indexer; "best practice: define monorepo boundaries, state architectural patterns, explicitly exclude legacy/test directories" (`result.md:53`).
- `pages` — array of `{title, purpose, parent?}` objects; *overrides* the default autonomous planning when defined; "purpose field must be highly specific, referencing exact file paths and technical concepts" (`result.md:49`).

Mapping onto our folder topology:

| Convention from `result.md` | Applies here? | Rationale |
|---|---|---|
| Define monorepo boundaries via `repo_notes` (`result.md:47`) | **Yes — N5** | Agency-System is a separate product layer; the indexer must not conflate it with governance. Direct downstream of R1 hallucination-prevention. |
| Explicitly exclude legacy directories via `repo_notes` (`result.md:53`) | **Partial** | We have no legacy code, but we DO have non-operational storage folders (`templates/`, `tools/`, `maintenance/`, `decisions/`, `Agency-System/` per FOLDERS.md §8). N5 covers the exclusion narrative. |
| `pages` overrides default clustering (`result.md:49`) | **Yes** | Without an explicit `pages` array, the indexer would miss the spec-first model entirely (R1). |
| Each `purpose` field references exact paths (`result.md:49`) | **Yes** | Adopted as a binding rule for Task 052 — every `purpose` cites at least one file path or directory name, even though the audience is human (R4 concession). |
| Construct parent-child documentation hierarchies (`result.md:62`) | **Yes** | The 16-page hierarchy uses parents `Governance Layer`, `How This Repo Works`, `Machine · Actor · Space Map` to encode the spec-first taxonomy. |
| Iterative steering (notes first, pages if gaps persist) (`result.md:62`) | **Mixed** | We commit to BOTH `repo_notes` AND `pages` in the first deliverable because the 16-page taxonomy is *known a priori* from the spec corpus; the iterative model is for repos where the maintainer is discovering structure as they go. |
| `llms.txt` auto-generation by DeepWiki (`result.md:66`) | **Defer** | Per R2: do not file an in-house `llms.txt` Task ahead of `.devin/wiki.json` adoption; observe the auto-generated index first. |
| Tiered nested `AGENTS.md` files (`result.md:72`) | **No — already covered isomorphically** | Per R3: our per-folder `readme.md` + `prompts/<slug>/{prompt.md,brief.md,readme.md}` three-file scaffold serves the same purpose with stricter enforcement. |

**Conclusion:** The `repo_notes` and `pages` conventions apply directly. The iterative-steering and tiered-nested-AGENTS.md conventions do not, for the reasons documented above.

---

## 2. Q2 — What is the correct page budget?

The Gemini result establishes the constraints (`result.md:60`):

- Standard: 30 pages.
- Enterprise: 80 pages.
- Notes cap: 100 total, each ≤ 10,000 characters.

Task 052 task.md proposes 16 pages in 4 tiers. Validation:

| Tier | Pages | Cumulative | Margin to 30 |
|---|---|---|---|
| Tier 1 — Repository Identity | 4 | 4 | 26 |
| Tier 2 — Governance Layer | 4 | 8 | 22 |
| Tier 3 — Working Layers | 6 | 14 | 16 |
| Tier 4 — History & Horizon | 2 | 16 | 14 |
| **Total** | **16** | **16** | **14** |

**Verdict:** 16 pages comfortably fits the 30-page standard limit (47% utilization). No enterprise tier required. The 14-page margin allows future growth (e.g. one page per ratified ADR cluster, or a per-amendment-chain history page) without restructuring.

**Possible merges considered and rejected:**

- *Merge "How This Repo Works" (Page 2) into "Repository Overview" (Page 1)?* No — Page 1 is the elevator pitch (`README.md` + `AGENTS.md §1`); Page 2 is the operational model (`PROMPT.md`, `RESEARCH.md §1`, `TASK.md §1`). Different audiences, different depths.
- *Merge "Frontmatter Schema" (Page 7) into "The Nine Root Specs" (Page 5)?* No — Page 7 is decisively about the L1/L2 ontology specifically and is the most-referenced operational concept; it deserves a dedicated page.
- *Merge "How We Got Here" (Page 15) and "What Is Next" (Page 16)?* No — these are temporally disjoint and serve different decision contexts. Page 15 is for auditors; Page 16 is for contributors.

The proposed 16-page structure is preserved.

---

## 3. Q3 — What are the highest-risk indexer blind spots? (M03 Pre-Mortem)

Counter-factual: imagine DeepWiki has produced its first pass over this repository with NO `.devin/wiki.json` in place. What would go wrong? Top three failure modes, ranked by blast radius:

### M1 (highest risk) — Indexer conflates governance layer with product layer

**Failure scenario.** The indexer treats `/Agency-System/` as core repository content because it contains a working FastAPI backend and HTML/JSX frontend with substantial code volume. The wiki would document Agency-System APIs as "the agency repository's primary interface" — directly contradicting FOLDERS.md §8 which explicitly exempts it from the governance audit graph.

**Source signal supporting the risk.** The Gemini result's LibreOffice-Buck case (`result.md:39`) is the canonical version of this failure mode: a deprecated config file dominated the indexer's understanding. Our equivalent: Agency-System's substantial JS/HTML payload would dominate the indexer's understanding of "what this repo is for."

**Mitigation.** `repo_notes` N1 (M·A·S map) plus N5 (Agency-System product-layer separation) inject explicit boundary declarations. Page 4 ("Machine · Actor · Space Map") makes the boundary canonical. Direct downstream of R1.

### M2 — Indexer documents 25–44 files and misses supporting infrastructure

**Failure scenario.** The DeepWiki benchmark (`result.md:115`) shows 25–44 files documented per project. Our repo has ~9 root specs + dozens of folders + ~50 tasks + ~30 prompts + ~30 research workspaces. A 25–44 file budget would cover only the top-level specs, missing the operational examples that make the spec-first model concrete.

**Source signal supporting the risk.** Direct quote (`result.md:109`): "it omitted vast swaths of supporting infrastructure, such as continuous integration pipelines and internal testing harnesses." Our `tools/`, `maintenance/`, and `.githooks/` are exactly that kind of infrastructure.

**Mitigation.** Page 14 ("Toolchain — The Machine Layer") explicitly forces coverage of `tools/readme.md`, `tools/fm/`, `tools/adr/`. Page 8 ("Pre-Commit Enforcement") forces coverage of `.githooks/pre-commit` and `tools/check-governance.sh`. The 16-page hierarchy *is* the mitigation.

### M3 — Indexer treats spec files as casual documentation rather than normative contracts

**Failure scenario.** DeepWiki's narrative-coherence optimisation (`result.md:101-103`) generates "polished, accessible technical prose" — but our root specs are *normative contracts* with RFC 2119 keywords and Gherkin acceptance criteria. A friendly narrative about "AGENTS.md is the agent instructions file" loses the binding nature of the spec; the wiki user might read the wiki, miss the binding clauses, and act on the prose summary.

**Source signal supporting the risk.** The Gemini result celebrates DeepWiki's presentation strength (`result.md:101`); presentation polish is exactly the lever that flattens normative force.

**Mitigation.** `repo_notes` N2 ("This repo is spec-first … Every file in /prompts/, /research/, /tasks/ carries frontmatter that cross-references these specs. The tools/ layer mechanically enforces these cross-references.") sets the frame. Page 5 ("The Nine Root Specs") makes the contract status canonical and lists every root `*.md`. Page 7 ("Frontmatter Schema") makes the linkage rules explicit.

**Pre-mortem complete.** All three failure modes have explicit `repo_notes` and `pages` mitigations.

---

## 4. Q4 — Where does the human-vs-agent utility dichotomy bite us?

The Gemini benchmarks (`result.md:113-118`) establish the dichotomy: DeepWiki optimises for human presentation (Presentation 8.1/10) at the cost of agent referencing density (Referencing 7.1/10).

For *this* repository's primary audience the analysis (R4) confirmed: **human readers are primary**. New contributors, reviewers, auditors. Claude Code agents work directly off the source files, not the rendered wiki — they read `AGENTS.md` and the frontmatter graph, not DeepWiki output.

So we accept the human-presentation optimisation. **Two agent-utility concessions are still made:**

### Concession 1 — Every `purpose` field cites at least one exact file path or directory

Even though agents will not be the wiki's primary audience, a human reader who is *also* operating an agent (the maintainer's most common workflow) benefits from being able to copy a path out of the wiki and hand it to the agent. The Task 052 task.md Todo item enforces this.

### Concession 2 — The Machine·Actor·Space map appears verbatim in `repo_notes[0]`

The verbatim table is structurally dense (10 spaces × 3 columns). It is not narrative-friendly, but it IS the conceptual core. Putting it in `repo_notes` rather than only in a page narrative ensures the LLM indexer carries it as explicit structured context for every page it generates downstream. This is a deliberate trade against pure presentation optimisation.

**No further agent-utility concessions are warranted.** Going further would dilute the human-presentation optimisation that motivated `.devin/wiki.json` adoption in the first place.

---

## 5. Q5 — Is the Machine · Actor · Space map isomorphic?

The map (Task 052 task.md):

| Space (directory) | Actor (canonical operator) | Machine (enforcement layer) |
|---|---|---|
| `/` root | Human maintainer | `tools/check-governance.sh`, `.githooks/pre-commit` |
| `/prompts/` | Human (intent author) + Claude Code | `tools/lint-linkage.py`, `tools/fm/validate` |
| `/research/` | Claude Code + External agents (Gemini) | `tools/lint-structure.py`, `tools/fm/validate` |
| `/tasks/` | Claude Code + Human reviewer | `tools/lint-linkage.py`, `tools/fm/validate`, `tools/check-task-lifecycle-classification.py` |
| `/decisions/` | Human architect + Claude Code | `tools/adr/` CLI (`agency-adr`) |
| `/skills/` | Human + Claude Code | `tools/fm/validate` |
| `/tools/` | Claude Code (implementation) | `tools/tests/` (pytest), `tools/lint-runlog.py` |
| `/Agency-System/` | Frontend/backend product layer | Separate from governance framework |
| `/maintenance/` | Claude Code (maintenance runs) | `tools/lint-runlog.py`, `tools/check-maintenance-bypass.py` |
| `/templates/` | Human + Claude Code | `tools/fm/validate` |

**Isomorphism invariant:** every Space has exactly one canonical Actor role and exactly one canonical Machine enforcer.

### Gap audit

- **`/` root.** Actor: Human maintainer. Machine: `tools/check-governance.sh` + `.githooks/pre-commit`. *Isomorphic.* Note: when an Accepted ADR enters the synthesis pipeline, the Machine row implicitly extends to `tools/adr/cli.py synthesize` (which rewrites the AGENTS.md guarded block); this is captured under `/decisions/` rather than duplicated here.
- **`/prompts/`.** Actor: Human (intent author) + Claude Code. Machine: `tools/lint-linkage.py` + `tools/fm/validate`. *Isomorphic.* (The Actor "or" is intentional: humans author intent, Claude Code may also draft prompts during research follow-ups.)
- **`/research/`.** Actor: Claude Code + External agents (Gemini). Machine: `tools/lint-structure.py` + `tools/fm/validate`. *Isomorphic.* Note: external agents are first-class actors here per RESEARCH.md §6.
- **`/tasks/`.** Actor: Claude Code + Human reviewer. Machine: three linters. *Isomorphic.* The third linter (`tools/check-task-lifecycle-classification.py`) is required because lifecycle classification has T1 / T2 / T3 / T4 tiers absent from other folders.
- **`/decisions/`.** Actor: Human architect + Claude Code. Machine: `tools/adr/` CLI. *Isomorphic.* The CLI is the singular enforcer (it bundles validate, synthesize, compress, graph).
- **`/skills/`.** Actor: Human + Claude Code. Machine: `tools/fm/validate`. *Isomorphic, but minimal.* The skills layer is intentionally lighter — only frontmatter validation; per FOLDERS.md §8, individual skill `readme.md` files are auto-generated and not hand-edited.
- **`/tools/`.** Actor: Claude Code (implementation). Machine: pytest + `tools/lint-runlog.py`. *Isomorphic.* `tools/tests/` is the test runner; `lint-runlog.py` checks the maintenance run-log invariant the tooling layer participates in.
- **`/Agency-System/`.** Actor: Frontend/backend product layer (not a governance actor). Machine: "Separate from governance framework". *Deliberately non-isomorphic — by design.* This row is the boundary marker; it makes the exemption explicit rather than implicit.
- **`/maintenance/`.** Actor: Claude Code (maintenance runs). Machine: `tools/lint-runlog.py` + `tools/check-maintenance-bypass.py`. *Isomorphic.*
- **`/templates/`.** Actor: Human + Claude Code. Machine: `tools/fm/validate`. *Isomorphic.* The validator skips `REPLACE`-token files for templates per FOLDERS.md §8.

### Verdict

Nine of ten rows are isomorphic. The tenth row (`/Agency-System/`) is *deliberately* non-isomorphic and serves as the boundary marker between the governance framework and the product layer.

**One gap noted, not blocking.** The Machine column for `/` root does not explicitly reference `tools/adr/cli.py synthesize`, even though the synthesis pipeline rewrites the AGENTS.md guarded block. This is captured under `/decisions/` and is mentioned in N4 (`repo_notes`); duplicating it under `/` would violate the "exactly one canonical Machine enforcer per Space" rule. Acceptable.

**No structural gaps that would block `.devin/wiki.json` synthesis.** The map ships as written.

---

## 6. Trace Table — Every `.devin/wiki.json` Entry to a Finding

### `repo_notes` traces

| Note | Finding source | Mitigation target |
|---|---|---|
| N1 — M·A·S map verbatim | Q5 isomorphism check + analysis R6 (planning/execution isomorphism) | M1 (governance/product conflation) |
| N2 — spec-first declaration | Q1 conventions audit + analysis R3 (AGENTS.md exceeds best practices) | M3 (specs-as-narrative flattening) |
| N3 — Prompt → Research → Task pipeline | Analysis R6 (ACU planning/execution alignment) | M2 (missing supporting infrastructure) |
| N4 — 032–039 amendment chain | Analysis R9 (audit graph IS compliance trail) | M3 (normative-contract loss) — chain context |
| N5 — Agency-System product-layer separation | Q1 monorepo-boundary convention + analysis R1 | M1 (governance/product conflation) |

### `pages` traces (16 pages)

| # | Page | Finding source | Mitigation target |
|---|---|---|---|
| 1 | Repository Overview | Q1 conventions; analysis R3 | Orientation baseline |
| 2 | How This Repo Works | Analysis R6 (pipeline isomorphism) | M3 (normative framing) |
| 3 | How to Navigate | Q1 hierarchy preference; FOLDERS.md | M2 (folder coverage) |
| 4 | Machine · Actor · Space Map | Q5 isomorphism; analysis R6 | M1 (governance/product conflation) |
| 5 | The Nine Root Specs | Analysis R3; Q1 spec-first declaration | M3 (specs-as-narrative loss) |
| 6 | Session Protocol | AGENTS.md SS.1–SS.3 | Operational binding |
| 7 | Frontmatter Schema | Analysis R3; AGENTS.md L1/L2 ontology | M3 (linkage-as-prose loss) |
| 8 | Pre-Commit Enforcement | Analysis R3; Q3 M2 mitigation | M2 (toolchain coverage) |
| 9 | Prompts — The Intent Layer | Analysis R6 (planning surface) | M2 (working-layer coverage) |
| 10 | Research — The Evidence Layer | Analysis R6; RESEARCH.md §1-§6 | M2 (working-layer coverage) |
| 11 | Tasks — The Coordination Layer | Analysis R6; TASK.md §3 | M2 (working-layer coverage) |
| 12 | Decisions (ADRs) | Analysis R9 (compliance trail) | M3 (ADR T4-immutability) |
| 13 | Skills — Capability Registry | SKILLS.md; CLAUDE.md §1 | M2 (capability-layer coverage) |
| 14 | Toolchain — The Machine Layer | Q3 M2 mitigation; analysis R5 (citation density) | M2 (infrastructure coverage) |
| 15 | How We Got Here | Analysis R9 (compliance trail) | M3 (history binds present) |
| 16 | What Is Next | Analysis R7 (deferred 10-ACU encoding) | Forward-looking horizon |

Every `repo_notes` entry and every `pages` entry traces to at least one finding (R-id) AND at least one mitigation (M-id). The audit invariant holds.

---

## 7. Friction Notes (informal)

Authoring this reflection consumed roughly the time-equivalent of reading `result.md` once + `analysis.md` once + cross-referencing four root specs. No friction events that warrant FL2+. The `.devin/wiki.json` schema in the Gemini result is unambiguous; the M·A·S map in Task 052 task.md was already self-consistent. The only minor friction (FL1 candidate) was reconciling whether the `/Agency-System/` row should be "non-isomorphic by design" vs. an isomorphism gap — resolved by treating the row as a boundary marker in §5, with the `/decisions/` synthesis pipeline as the only true gap noted (not blocking).

Final FL declaration is tracked in the closing commit, not here.
