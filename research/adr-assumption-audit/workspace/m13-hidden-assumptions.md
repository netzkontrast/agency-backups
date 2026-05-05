---
type: note
status: active
slug: adr-assumption-audit-m13
summary: "Subagent A output: [M13] adversarial query expansion across adjacent / opposing / abstraction / orthogonal axes against the ADR governance spec. 9 hidden assumptions, each with falsifiability and blast radius."
created: 2026-05-05
updated: 2026-05-05
---

# Subagent A — [M13] Hidden Assumption Extraction

**Method:** [M13] Adversarial Query Expansion across all four axes.
**Target:** `research/adr-spec-research-synthesis/output/SPEC.md` (primary); Gemini draft (secondary).
**Output contract:** ≥ 5 ASMs with `Assumption ID / Axis / Assumption text / Where embedded / Falsifiability / Blast radius`.

## Axis 1 — Adjacent

Comparators: OPA/Rego (policy-as-code), RFC standards process (IETF), MADR / log4brains / adr-tools, legal statute amendment.

### ASM-001

- **Axis:** adjacent
- **Assumption text:** A repository's normative governance rules can be losslessly compressed into a token-bounded summary using a deterministic, non-ML algorithm.
- **Where embedded:** SPEC §5.1 ADR.A.3.4 ("MUST achieve a fidelity score ≥ 0.95 under the algorithm selected by `--fidelity-mode`"); SPEC §5.3 rationale ("the MDL framing forces the pipeline to treat the corpus as a compression problem").
- **Falsifiability:** Build the v0 `bcp14-keyword` fidelity scorer and run it against a synthetic corpus where the synthesis pipeline strips a `MUST NOT` qualifier from one rule. If the scorer reports ≥ 0.95 (the floor), the assumption is false: the metric does not detect polarity inversion, the most consequential failure mode.
- **Blast radius:** **HIGH.** A polarity-inversion miss produces an `AGENTS.md` that *forbids* what should be required (or vice versa) without any validator catching it. Every downstream agent then operates against an inverted rule.

### ASM-002

- **Axis:** adjacent
- **Assumption text:** Sequential numbering (`ADR-NNNN` monotonically increasing) is sufficient for unique identity in a multi-branch agentic repo.
- **Where embedded:** SPEC §4.1 ADR.A.2.7 (filename `<NNNN>-<slug>.md`); SPEC §7.4 JSON-Schema `pattern: "^ADR-[0-9]{4}$"`.
- **Falsifiability:** The repo already has documented duplicate `task_id` collisions (Task 013, Task 024 lineage) caused by parallel-branch numbering races. Run two parallel branches each authoring `ADR-0042`; the merge produces two files at the same id. The duplicate-detection only triggers post-merge.
- **Blast radius:** **MEDIUM.** Caught by ADR.A.5.6 *after* merge; resolution requires a renumber Task analogous to Task 024. Annoying but not silent.

### ASM-003

- **Axis:** adjacent
- **Assumption text:** The MADR template's three-part body (Context / Decision Outcome / Consequences) is the natural shape for every architectural decision in this repo.
- **Where embedded:** SPEC §4.1 ADR.A.2.1 ("MUST conform to MADR 4.0.0 section structure").
- **Falsifiability:** Audit the 14 implicit-ADR candidates in `research/adr-spec-research-synthesis/workspace/analysis.md §A`. If any decision is *not* expressible in the MADR shape without a multi-page contortion (e.g. "T1/T2/T3/T4 repair tier model" is a *taxonomy*, not a decision; "Frontmatter is layered L0-L3" is a *schema*, not a decision), the assumption is partially false.
- **Blast radius:** **MEDIUM.** Forces either an awkward MADR fit (lower readability) or a schema extension (the MAY clause for Y-Statements is a half-measure).

## Axis 2 — Opposing (Falsification Scenarios)

Build the failure: under what conditions does the model produce a corrupted `AGENTS.md` that no validator catches?

### ASM-004

- **Axis:** opposing
- **Assumption text:** The `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` markers are sufficient to prevent destructive overwrite.
- **Where embedded:** SPEC §2.3, §5.1 ADR.A.3.5.
- **Falsifiability:** Three failure paths the marker check does NOT catch:
  1. A maintainer edits the comment markers themselves (e.g. typo: `<!-- BEGIN AGENT-ADR SYNTHESIS -->`). The validator says "marker missing", refuses to write, but no diagnostic suggests the *typo* hypothesis.
  2. A merge conflict resolution duplicates the markers. Now there are two BEGIN/END pairs; the synthesis writes between the *first* pair and the second pair becomes orphan content.
  3. A markdown renderer mis-handles the HTML comment (e.g. when AGENTS.md is rendered to a web view), embedded `-->` inside the synthesised content (an ADR body containing an HTML comment) closes the marker early.
- **Blast radius:** **HIGH.** Path 2 is the worst — silent content drift between the two marker pairs over many synthesis runs.

### ASM-005

- **Axis:** opposing
- **Assumption text:** `agency-adr validate` running inside `tools/check-governance.sh` is sufficient to catch every ADR-related governance violation before commit.
- **Where embedded:** SPEC §2.4, §7.1 ADR.A.5.8.
- **Falsifiability:** The pre-commit hook only fires on the *committing* branch. Three corruption paths bypass it:
  1. A `git push --force` from another agent's branch lands new commits on the remote without re-running the local hook.
  2. A maintainer disables hooks (`HUSKY=0` or `git commit --no-verify`); the spec does not block this.
  3. A web-UI edit (GitHub's edit-in-browser) skips local hooks entirely and relies on the (not-yet-existent) GitHub Actions workflow specified in plan §4.
- **Blast radius:** **HIGH** for path 3 (no CI exists yet); **MEDIUM** for paths 1–2 (covered once CI lands).

### ASM-006

- **Axis:** opposing
- **Assumption text:** When two Accepted ADRs make contradictory claims about the same subject, the supersession DAG is sufficient to resolve the conflict.
- **Where embedded:** SPEC §6.1 ADR.A.4.4 ("MUST resolve contradictory rules by prioritising the most recent ADR utilizing a Directed Acyclic Graph traversal of supersession edges").
- **Falsifiability:** Two Accepted ADRs ADR-0010 and ADR-0011 are committed simultaneously, neither lists the other in `adr_supersedes` (because their authors didn't realise the topical overlap). The DAG has no edge between them; the synthesis pipeline has no rule for which one wins. The spec assumes contradiction implies supersession; the failure mode is *contradiction without supersession claim*.
- **Blast radius:** **MEDIUM.** The synthesis output non-deterministically picks one (ordering by `adr_id` is a reasonable default, but it is not in the spec).

## Axis 3 — Abstraction (Meta-Assumption)

What is the entire spec resting on at the highest level?

### ASM-007

- **Axis:** abstraction
- **Assumption text:** Architectural decisions in an agentic repository will be authored *by humans, proactively, in advance of the implementation*. The spec models the human MADR workflow.
- **Where embedded:** Spec language throughout uses "the author" without specifying agent vs human (SPEC §3.1 ADR.A.1.1, §4.1 ADR.A.2.x). The exploration phase (§3) presupposes a deliberative drafting step that maps poorly onto an agent's session-bounded execution. The supersession lifecycle (§6) presupposes a human reviewer recognising that a new ADR semantically overlaps an old one.
- **Falsifiability:** Survey the repo's actual decision authorship pattern. The 14 implicit decisions catalogued in Task 027's analysis were *all* embedded in tooling and root specs by either (a) an agent during a Task execution or (b) a maintainer during PR review. *Zero* decisions were authored proactively by a human as a standalone ADR. If this pattern continues, the spec's Aspect-1 (Explore) and Aspect-2 (Plan) phases describe a workflow that no one in the repo actually performs.
- **Blast radius:** **HIGH (cultural).** The spec ships and is technically correct, but the corpus stays empty because the workflow it describes does not match the repo's actual decision-making locus. This is the *log4brains adoption-failure pattern* — the tooling exists but the decisions never reach the canonical store.

### ASM-008

- **Axis:** abstraction
- **Assumption text:** Token efficiency is the binding constraint on `AGENTS.md` quality.
- **Where embedded:** SPEC §0 World-Change Annotation; SPEC §5.1 ADR.A.3.3 (token-limit normative); SPEC §5.3 rationale ("MDL framing forces the pipeline to treat the corpus as a compression problem").
- **Falsifiability:** The current `AGENTS.md` is ≈ 4,800 tokens by heuristic. The narrative-ontology section alone is ≈ 1,200 tokens. If the maintainer's actual binding constraint is *agent comprehension* (not raw token count), then aggressive MDL compression that strips human-narrative context will *reduce* `AGENTS.md` quality even while reducing its token count. The assumption is testable: instrument an agent to read the synthesised `AGENTS.md` and measure task-completion accuracy versus reading the un-synthesised manual prose. If accuracy drops, MDL was the wrong objective function.
- **Blast radius:** **MEDIUM.** Spec is salvageable by lowering the compression aggressiveness (raise `--token-limit`, soften `--fidelity-floor`).

## Axis 4 — Orthogonal (MDL Lens on Load-Bearing Assumptions)

What assumptions are load-bearing for the compression-ratio claim, and what is the worst-case if they fail?

### ASM-009

- **Axis:** orthogonal
- **Assumption text:** The "Decision Outcome" and "Consequences" sections of an ADR contain the entirety of its normative content; the rest (Context, Considered Options, rationale prose) is non-normative and safely discardable.
- **Where embedded:** SPEC §5.1 ADR.A.3.1 ("MUST extract normative content exclusively from the 'Decision Outcome' and 'Consequences' sections").
- **Falsifiability:** Audit any well-written existing root spec in the repo (e.g. [`MAINTENANCE.md §1`](../../../MAINTENANCE.md)). Many normative MUSTs live in *table cells* or in the *prose surrounding* the formal "Decision" — for example `MAINTENANCE.md §3.4` "Stale-Task Audit" buries normative classification rules inside the bucket-action table, not in any "Decision Outcome" header. If ADR authors follow this pattern, ADR.A.3.1 will silently drop normative rules.
- **Blast radius:** **HIGH.** Synthesised `AGENTS.md` is missing rules that *exist* in the corpus; agents operate against an under-specified contract. The fidelity check (ADR.A.3.4) does not catch this because the metric only compares what the extractor *did* extract; it has no awareness of what was *not* extracted.

## Worst-Case Compression-Ratio Scenario

If ASM-001 fails (polarity inversion undetected) AND ASM-009 fails (normatives outside the recognised sections are dropped):

- The synthesised guarded section may report a "passing" 0.95+ fidelity score against the *recognised* extracted content.
- But the *full* corpus normative density may have been silently halved.
- The *true* compression ratio is then 2× the claimed ratio (because the denominator was undercounted).
- An agent reading `AGENTS.md` is operating against a 2:1-undermined rule set with no diagnostic signal.

This is the worst-case scenario this spec must hedge against. Mitigations are listed in `output/REPORT.md §4`.

## Summary Table

| ASM | Axis | Blast | One-line text |
|---|---|---|---|
| 001 | adjacent | HIGH | Polarity inversion is undetectable by deterministic compression. |
| 002 | adjacent | MEDIUM | Sequential numbering races on parallel branches. |
| 003 | adjacent | MEDIUM | MADR shape may not fit every governance decision. |
| 004 | opposing | HIGH | Marker-pair check has at least three bypass paths. |
| 005 | opposing | HIGH | Pre-commit-only enforcement is bypassable; CI does not yet exist. |
| 006 | opposing | MEDIUM | Two simultaneous Accepted ADRs may contradict without a supersession claim. |
| 007 | abstraction | HIGH (cultural) | Spec models human authorship; this repo's culture is agent-driven. |
| 008 | abstraction | MEDIUM | Token efficiency may not be the binding constraint on `AGENTS.md` quality. |
| 009 | orthogonal | HIGH | Normatives outside "Decision Outcome"/"Consequences" are silently dropped. |

**3 HIGH (technical) + 1 HIGH (cultural) + 4 MEDIUM + 1 (counted in HIGH cultural) = 9 ASMs.**

Findings flow into `output/REPORT.md §1`, sorted by blast radius.
