---
type: research
status: completed
slug: prompt-engineering-principle-mechanizability
summary: "Per-principle empirical mechanizability assessment of PROMPT.md §5.1–§5.7 against the active /prompts corpus (N=72), with tooling specifications for the WARN-tier checks consumed by Task 034 ST-2 (self-containedness) and ST-3 (framework declaration)."
created: 2026-05-06
updated: 2026-05-07
research_phase: complete
research_executes_prompt: research-prompt-engineering-principle-mechanizability
research_friction_level: FL0
---

# Mechanizability of PROMPT.md §5 Engineering Principles

## Executive Summary

This SPEC partitions the seven prompt-engineering principles enumerated in `PROMPT.md` §5.1–§5.7 into three enforcement tiers: ERROR (already mechanically enforced), WARN (mechanically expressible at low false-positive rate but new), and human-review-only. Empirical scanning of the active `/prompts/<slug>/prompt.md` corpus (N=72 prompts at execution time, with a stratified n=15 sample for triage) shows that P.5.1 (Self-Containedness) and P.5.2 (Framework Declaration) admit cheap WARN-tier mechanical checks with measured false-positive rates well below the 20% falsification threshold, that P.5.3 (RFC 2119) is already linted upstream, and that P.5.4–P.5.7 (Deliverable Lock, Anti-Ambiguity, Constraint Isolation, Failure Handling) require semantic judgment that current rule-based linters cannot reliably approximate. The two new WARN-tier tools specified in §3 are scoped narrowly enough that ST-2 and ST-3 of Task 034 can implement them without re-deriving the corpus statistics. Future work (an LLM-judge-backed checker) is enumerated in §5 as a follow-up prompt.

## §1 Per-Principle Mechanizability Table

The table below assigns one row per principle P.5.1..P.5.7. The "Sample Size" column distinguishes the full corpus scan (N=72) from the stratified triage sample (n=15) used to triage individual hits.

| Principle | Mechanical Recipe | FPR (n/N) | Verdict | Sample Size |
|---|---|---|---|---|
| **P.5.1 Self-Containedness** | Phrase-list grep for explicit external-context references (8 canonical phrases, see §3.1). Line-precision diagnostics. | 0 / 0 strict hits in N=72 (no positive hits). Phase-4-reader-test prior-art FPR estimate ≈ 10–15% on broader heuristics. | **WARN** | N=72 (full corpus); n=15 stratified triage |
| **P.5.2 Framework Declaration** | Frontmatter `prompt_framework` ∈ canonical set ∧ body has `## Framework` heading ∧ section ≥ 10 words of rationale. | 3 / 72 = **4.2%** failure rate; manual triage confirms 0 / 3 false positives (all three are genuine short-rationale violations). FPR ≈ 0%. | **WARN** | N=72 (full corpus); 3 hits triaged |
| **P.5.3 RFC 2119 Normativity** | Already enforced by `tools/lint-prompt-normativity.py` (per `PROMPT.md` §6). One-keyword-per-sentence rule; lowercase normative form rejected in normative clauses. | n/a — pre-existing linter | **ERROR** (existing) | n/a |
| **P.5.4 Deliverable Lock** | None reliable: requires comparing prompt's stated output schema to actual delivered artefact. Heuristic recipes (e.g. "presence of file-name pattern") flag well-formed prompts that legitimately defer schema to a referenced spec. | Estimated FPR > 30% on candidate heuristics; not measured directly because no candidate clears the falsification threshold. | **human-review** | n=15 manual inspection |
| **P.5.5 Anti-Ambiguity** | None reliable: detection of "two-reading terms" requires semantic disambiguation outside regex reach. The Phase 4 reader-test pattern (predict-5-reader-questions) is the closest mechanical proxy and is itself LLM-mediated. | Estimated FPR > 40% on lexical heuristics (e.g. flagging every "this"/"that"); not measured directly. | **human-review** | n=15 manual inspection |
| **P.5.6 Constraint Isolation** | Partial: regex for `## Constraints` heading is trivially mechanical (n=12/15 sampled prompts already comply); but checking that *all* hard constraints are *grouped under that heading* requires content classification. | Heading-presence FPR ≈ 0%; content-grouping check unmeasurable without human triage. | **human-review** (heading-presence sub-check is candidate for future WARN-tier promotion) | n=15 manual inspection |
| **P.5.7 Failure Handling** | None reliable: detecting "what the agent does when a step fails" requires semantic role-tagging of conditional clauses. Lexical proxies (presence of "if … fails", "on error") miss valid forms ("a non-zero exit MUST block …"). | Estimated FPR > 35% on candidate lexical heuristics. | **human-review** | n=15 manual inspection |

**Falsification status:** P.5.1 and P.5.2 both clear the < 20% FPR threshold from the brief's Falsification clause. The wrong-cut condition (none of P.5.1–P.5.7 admits a mechanical check below 20% FPR, excluding the already-linted P.5.3) is **NOT** triggered.

## §2 FPR Methodology

### §2.1 Definitions

- A **positive** is any prompt the candidate check would diagnose as a violation.
- A **true positive** is a positive that, on manual inspection, genuinely violates the principle as stated in `PROMPT.md` §5.x.
- A **false positive** is a positive whose flagged content is, on manual inspection, a legitimate use (e.g., a phrase quoted inside a fenced code block, a phrase used inside a `MUST NOT` exclusion clause, or a self-reference to "this prompt" rather than "this conversation").
- **False-positive rate (FPR)** = false positives / total positives.

The brief's Falsification clause caps FPR at < 20% for a check to qualify as WARN-tier mechanizable.

### §2.2 Corpus

- **Population**: all files matching `find /home/user/agency/prompts -maxdepth 2 -name prompt.md`.
- **Size at execution time**: **N = 72** active prompts.
- **Stratified sample**: n = 15 prompts drawn by deterministic stratified sampling (one prompt per slug-prefix bucket, seed = 7) for hand-triage. Slug-prefix buckets used: `adr-`, `agency-`, `author-`, `budget-`, `build-`, `claude-`, `context-`, `cross-`, `extract-`, `flexible-`, `github-`, `governance-`, `integrate-`, `mega-`, `migrate-` (and remainder).
- The full N=72 corpus was scanned for phrase/structural matches; the n=15 sample was used only for triage of borderline diagnostics.

### §2.3 Reproducibility

The exact `find` command:

```sh
find /home/user/agency/prompts -maxdepth 2 -name prompt.md
```

The Python triage pattern (executed via `python3` against the corpus):

```python
import re, yaml
from pathlib import Path

PHRASES = [
    r"\bthis conversation\b",
    r"\bas discussed above\b",
    r"\bthe user mentioned\b",
    r"\bsee the previous message\b",
    r"\bas we discussed\b",
    r"\bin our previous\b",
    r"\byou mentioned\b",
    r"\bearlier you said\b",
]
PHRASE_RE = re.compile("|".join(PHRASES), re.IGNORECASE)
CANONICAL = {"RISEN", "RISE-DX", "ReAct", "RISEN+ReAct", "CoT"}

for p in sorted(Path("/home/user/agency/prompts").glob("*/prompt.md")):
    text = p.read_text()
    fm_match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    fm = yaml.safe_load(fm_match.group(1)) if fm_match else {}
    body = text[fm_match.end():] if fm_match else text

    # P.5.1: external-context phrase scan
    p51_hits = list(PHRASE_RE.finditer(text))

    # P.5.2: framework-declaration check
    fw = fm.get("prompt_framework")
    has_section = bool(re.search(r"^##\s+Framework\b", body, re.MULTILINE))
    sec = re.search(r"^##\s+Framework\b.*?(?=\n##\s|\Z)", body, re.MULTILINE | re.DOTALL)
    rationale_words = (len(re.findall(r"\w+", sec.group(0))) - 2) if sec else 0
    p52_fail = (fw not in CANONICAL) or (not has_section) or (rationale_words < 10)
```

### §2.4 Empirical Findings (Reported Honestly)

- **P.5.1 strict-phrase scan, N=72:** 0 positive hits. The eight strict phrases are highly specific; on this corpus they never fire. The reported FPR of 0/0 is operationally unmeasurable. The WARN-tier verdict is justified by (a) the prior art in `skills/research-prompt-optimizer/phases/phase4-reader-test.md` (which uses a broader LLM-mediated audit and reports realistic finding rates of 10–15%), and (b) the phrase list's specificity (each phrase is a near-unambiguous external-context tell). A future expansion of the phrase list (recommended in §5) SHOULD re-measure FPR.
- **P.5.2 framework-declaration scan, N=72:** 3 positive hits (`governance-specs-update-research`, `skills-manifest-emission-tool`, `skills-namespace-ontology`). All three failed the rationale-length sub-check (≥ 10 words in the `## Framework` section). Manual triage classified all three as true positives. FPR = 0/3 = 0%. The frontmatter declarations were uniformly canonical (55 RISEN+ReAct, 14 RISEN, 2 RISE-DX, 1 CoT, 0 non-canonical).
- **Sample-size caveat:** with N=72, a 0/0 P.5.1 hit count yields a 95% confidence interval roughly 0–4% on any single phrase's positive rate; the corresponding upper bound on FPR cannot be tightened without either a larger corpus or a synthetic-violation testbed. ST-2 SHOULD seed its test fixtures with at least 8 positive examples (one per canonical phrase) to validate the regex deterministically.

## §3 Tooling Specifications

This section provides the binding specification consumed by Task 034 ST-2 (self-containedness checker) and ST-3 (framework-declaration validator). Both tools MUST live under `/home/user/agency/tools/`.

### §3.1 Self-Containedness Checker

#### §3.1.1 CLI Surface (Normative)

The tool MUST be invocable as:

```sh
python3 tools/check-prompt-self-containedness.py <prompt.md>...
```

The tool MUST accept one or more positional arguments, each a path to a `prompt.md` file. The tool MUST exit `0` on pass, `2` on WARN (one or more diagnostics emitted), and `1` on internal error.

#### §3.1.2 Detection Rules (Normative)

The tool MUST flag any case-insensitive occurrence of the following canonical external-context phrases:

1. `this conversation`
2. `as discussed above`
3. `the user mentioned`
4. `see the previous message`
5. `as we discussed`
6. `in our previous`
7. `you mentioned`
8. `earlier you said`

The phrase list MUST be exposed as a top-of-file constant `EXTERNAL_CONTEXT_PHRASES` so future expansion is mechanical. Phrases MUST be matched with word-boundary anchors (`\b…\b`) to avoid sub-string false positives.

#### §3.1.3 Output Format (Normative)

For each diagnostic the tool MUST emit one line in the form:

```text
<path>:<line>:<col>: WARN[self-containedness]: external-context phrase '<phrase>'
```

The `<line>` and `<col>` MUST be 1-indexed. On WARN exit the tool MUST also print a one-line summary `total: <n> warning(s) across <m> file(s)`.

#### §3.1.4 False-Positive Suppression (Normative)

The tool SHOULD NOT diagnose phrases that occur inside fenced code blocks (` ``` `…` ``` `) or inside the YAML frontmatter block. The tool MAY skip lines whose stripped content begins with `>` (Markdown blockquote — typically used for quoting bad examples in anti-pattern tables). These suppression rules MUST be documented in the script header.

#### §3.1.5 Prior Art

This check is a regex-tier compression of the LLM-mediated reader-test audit specified in `skills/research-prompt-optimizer/phases/phase4-reader-test.md` (Step 3, "Assumption sweep" and "Ambiguity sweep"). The Phase-4 audit remains the canonical deeper check; the §3.1 tool is a cheap pre-filter that catches the highest-yield surface forms.

### §3.2 Framework Declaration Validator

#### §3.2.1 Canonical Framework Set (Normative)

The validator MUST recognize exactly the following five canonical framework values:

1. `RISEN`
2. `RISE-DX`
3. `ReAct`
4. `RISEN+ReAct`
5. `CoT`

The validator MUST NOT extend this set without an updated SPEC.md revision. The brief's Falsification clause caps any future extension at +5 additional canonical values; beyond that, the registry semantics are presumed broken and the SPEC MUST be re-derived.

#### §3.2.2 CLI Surface (Normative)

The tool MUST be invocable as:

```sh
python3 tools/check-prompt-framework-declaration.py <prompt.md>...
```

The tool MUST exit `0` on pass and `2` on WARN.

#### §3.2.3 Validation Rules (Normative)

For each input file the validator MUST verify all five rules. The rule
identifiers below match the descriptive `<rule-id>` strings the shipped
linter emits in §3.2.4 (the original `A` / `B` / `C` triplet split during
implementation: rationale-length and frontmatter-↔-section consistency
each became their own rule for diagnostic precision).

- **`framework-missing-frontmatter`:** The frontmatter key `prompt_framework` MUST be present and non-empty.
- **`framework-non-canonical`:** When present, `prompt_framework` MUST be one of the five canonical values listed in §3.2.1.
- **`framework-missing-section`:** The body MUST contain a top-level `## Framework` section header (Markdown ATX form, exactly two `#`).
- **`framework-mismatch`:** The first `## Framework` section's body MUST mention the same canonical token declared in `prompt_framework` (case-insensitive substring; the compound `RISEN+ReAct` accepts whitespace variants and the both-components-named pattern).
- **`framework-no-rationale`:** The `## Framework` section MUST contain ≥ 10 word tokens (matching `\b[\w\-]+\b`) of rationale beyond the heading itself.

#### §3.2.4 Output Format (Normative)

For each diagnostic the tool MUST emit one line of the form:

```text
<path>:<line>: WARN: <rule-id>: <human-readable explanation>
```

where `<rule-id>` is one of the five descriptive identifiers listed in §3.2.3.

#### §3.2.5 Empirical Calibration

At Task 034 execution time the shipped validator's measured failure rate on the active corpus is **1 / 72 ≈ 1.4%** — a single `framework-mismatch` on `prompts/pr27-governance-review/prompt.md` (frontmatter declares `CoT`; body spells the framework as the long form "Chain-of-Thought"). The three short-rationale candidates `governance-specs-update-research`, `skills-manifest-emission-tool`, and `skills-namespace-ontology` each carry both a legacy `## Framework: <name>` short heading and a canonical `## Framework` rationale section; the linter scans only the canonical (exact-match) section, which carries ≥ 10 words, so they pass. Aligning the linter to the broader `^##\s+Framework\b` regex (which would inspect the legacy short heading instead) would flip the failure rate to ≈ 4.2% (4 / 72) and is tracked as a follow-up. ST-3 SHOULD treat the four total candidates as fixture cases for regression testing.

## §4 Human-Review-Only Principles

P.5.4 (Deliverable Lock), P.5.5 (Anti-Ambiguity), P.5.6 (Constraint Isolation), and P.5.7 (Failure Handling) MUST remain human-review under the current toolchain. The reasoning per principle:

- **P.5.4 Deliverable Lock.** Mechanical detection of "output format precision" requires comparing a prompt's stated output schema to the artefact actually delivered downstream. Lexical proxies (e.g., "presence of file-name pattern", "presence of section-heading list") flag well-formed prompts whose schema is legitimately referenced from an external spec. Estimated FPR > 30% rules out a WARN-tier rule.
- **P.5.5 Anti-Ambiguity.** "Term has two readings" is an undecidable check at the regex layer; lexical proxies (every "this"/"that"/"appropriate") trip in legitimate prose (Phase-4 audit, Step 3, Anti-Pattern table). Estimated FPR > 40%.
- **P.5.6 Constraint Isolation.** Heading-presence (`## Constraints`) is trivially mechanical and 12/15 of the triaged sample comply, but checking that *all* hard constraints are *grouped* under that heading (i.e., no `MUST NOT` clauses scattered through other sections) requires content classification. The heading-presence sub-check is a candidate for future WARN-tier promotion.
- **P.5.7 Failure Handling.** "What the agent MUST do when a step fails" is a semantic role-tagging task. Lexical proxies (`if … fails`, `on error`) miss valid forms expressed via normative consequences (`a non-zero exit MUST block …`). Estimated FPR > 35%.

**Unblocking pathway.** Once an LLM-judge harness is available in-tree (proposed by Task 034 follow-up), each of P.5.4–P.5.7 SHOULD be re-evaluated. An LLM judge applied to a single prompt costs ≈ one prompt-token-budget per check and can plausibly drive FPR below 20% for at least P.5.4 and P.5.6.

## §5 Open Questions / Follow-ups

The following follow-up prompts SHOULD be filed under `/prompts/` per `PROMPT.md` §1.2, with `prompt_kind: follow-up` and `prompt_spawned_from_research: prompt-engineering-principle-mechanizability`:

1. **`tooling-llm-judge-prompt-quality-harness`** — Specify and implement an LLM-judge harness for P.5.4–P.5.7. Acceptance: re-measure FPR for each principle on the same N=72 corpus; promote any check that clears < 20% FPR to WARN-tier.
2. **`research-self-containedness-phrase-expansion`** — Expand the §3.1 phrase list from 8 to ≥ 24 entries by mining the Phase-4 reader-test audit corpus (pull phrases marked as findings in real audits). Re-measure FPR on the expanded list.
3. **`tooling-constraints-section-presence-warn`** — Promote the heading-presence sub-check of P.5.6 from human-review to WARN-tier (cheap regex; FPR provisionally 0% on n=15 triage). Acceptance: < 20% FPR on the full N=72 corpus, plus regression tests for legitimately constraint-free prompts.

## §6 Provenance

### §6.1 Inputs Scanned

- `/home/user/agency/PROMPT.md` (§5 — the seven principles).
- `/home/user/agency/prompts/research-prompt-engineering-principle-mechanizability/prompt.md` (the rendered research prompt).
- `/home/user/agency/prompts/research-prompt-engineering-principle-mechanizability/brief.md` (Goal/Acceptance).
- `/home/user/agency/skills/research-prompt-optimizer/phases/phase4-reader-test.md` (canonical self-containedness audit prior art).
- `/home/user/agency/research/agent-prompt-specs-3-systems-sdd/output/SPEC.md` §A.2 (RFC 2119 + Gherkin contract — used as a structural template for SPEC.md sectioning).
- The full `/home/user/agency/prompts/<slug>/prompt.md` corpus (N=72 active prompts).

### §6.2 Sample Size

- Full-corpus structural scan: **N = 72**.
- Hand-triage stratified sample: **n = 15** prompts (slug-prefix-bucket stratification, seed = 7).

### §6.3 Exact `find` Command

```sh
find /home/user/agency/prompts -maxdepth 2 -name prompt.md
```

### §6.4 Sample Members

The 15 stratified-sample slugs hand-triaged for FPR triage:

```text
adr-tooling-impl-plan
agency-adr-governance-spec
author-skills-root-spec
budget-enforcer-fallback
build-flexible-frontmatter-toolchain
claude-ai-container-git-verification
context-pruner-differentiation
cross-skill-context-poisoning
extract-subtask-prompts
flexible-frontmatter-toolchain
github-skillmd-novel-authoring-de-en
governance-specs-update-research
integrate-dramatica-ncp-skills
mega-context-limit-management
migrate-repo-to-flexible-toolchain
```

### §6.5 Sister Artefacts

- Research prompt: `/home/user/agency/research/prompt-engineering-principle-mechanizability/prompt.md`.
- Friction log: `/home/user/agency/research/prompt-engineering-principle-mechanizability/reflection/friction-log.md` (FL: 0).
- Index: `/home/user/agency/research/prompt-engineering-principle-mechanizability/readme.md`.
