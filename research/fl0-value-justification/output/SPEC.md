---
type: spec
status: active
slug: fl0-value-justification
summary: "Empirical justification for the FL0-mandatory rule (FRUSTRATED.md §FL.0). Population: 60 friction logs across closed Tasks (40) and research runs (20). Distribution: 23 FL0 (38%) / 30 FL1 (50%) / 6 FL2 (10%) / 1 FL3 (2%). Verdict: MANDATE FL0, with clarified rationale. The FL0 line provides a falsifiable null-baseline signal that lets the nightly maintenance run distinguish 'no friction' from 'no log'."
created: 2026-05-07
updated: 2026-05-07
---

# SPEC — FL0 Value Justification (Task 038 ST-1)

## §1. Population & Method

**Population.** Every `friction-log.md` file in the repo at 2026-05-07. Enumerated via `find tasks research -name friction-log.md`. Total: **60 logs** (40 task closures + 20 research-reflection runs).

**Method.** For each log, extract the first occurrence of `FL[0-3]`. No interpretation; the surface-form variant (canonical or otherwise) was treated as authoritative. Logs that bury the FL marker below the first occurrence are still counted by their first match — this is a deliberate concession to the variant-form set documented in §2.

**Coverage statement.** This study covers ≥15 closed tasks (the threshold set by [`prompts/research-fl0-value-justification/prompt.md`](../../../prompts/research-fl0-value-justification/prompt.md) §E). The 60-log population exceeds the threshold by 4×.

## §2. FL Distribution and Variant-Form Set

### §2.1 FL distribution (full population)

| Level | Count | Percentage |
|-------|-------|------------|
| FL0   | 23    | 38%        |
| FL1   | 30    | 50%        |
| FL2   | 6     | 10%        |
| FL3   | 1     | 2%         |
| **Total** | **60** | **100%** |

**Reading.** FL0 is the modal "no-friction" case but is *not* the majority. Half of all closed work surfaces FL1 friction. If FL0 logging were optional, the agent could not distinguish the FL0 majority case from a missed log; the distribution would collapse.

### §2.2 Variant forms in corpus (input to ST-2 linter)

The canonical line per [FRUSTRATED.md §31](../../../FRUSTRATED.md#when-and-how-to-log-mandatory) is:

> `Highest Frustration Level: FL[0-3]`

In practice the corpus exhibits the following variant declarations. The ST-2 linter (`tools/check-fl-declaration.py`) MUST accept this bounded set:

1. `Highest Frustration Level: FL0` — canonical (research/agent-prompt-specs-3-systems-sdd, others).
2. `**Highest Frustration Level: FL0**` — bold-canonical (research/spec-staleness-decision-formalization).
3. `**Highest friction level experienced: FL0**` — phrasing variant (research/skills-namespace-ontology).
4. `**Highest FL experienced: FL0**` — abbreviated phrasing (research/research-cross-spec-contradiction-baseline).
5. `**FL0** — <prose>` — bold-bare-prose (tasks/011, tasks/010, tasks/004).
6. `- **Friction Level:** FL0 (...)` — list-form (tasks/009).
7. `**FL0**` — bold-bare (tasks/052, tasks/051; the prose follows on the next line).
8. `FL0 - <prose>` — bare-with-em-dash (tasks/012, tasks/006).
9. `FL0` (line of its own) — bare (tasks/008, research/governance-specs-update-research).
10. Frontmatter-only `summary: FL0` (tasks/008) — not a body declaration; SHOULD trigger a WARN, not an ERROR.

### §2.3 Quoted FL0 entries (≥10 distinct samples)

> **`tasks/004-create-missing-prompts/friction-log.md`** — "**FL0** — plan obsolesced cleanly. The two prompts the Task asked for now exist on disk; the original Goal is satisfied by drift via subsequent commits. The Task is closed as `updated` (not `done`) because the *next* concern was never in scope of the original Plan."

> **`tasks/006-skills-navigation-bootstrap/friction-log.md`** — "FL0 - Task was already done, just applying a mechanical frontmatter fix locally found by the Repo Coherence routine."

> **`tasks/009-author-skills-root-spec/friction-log.md`** — "**Friction Level:** FL0 (No unexpected blockers, context was clear and specs were readily available). **Notes:** The task was clear and well-scoped. All necessary schemas and sections were clearly laid out."

> **`tasks/010-skills-frontmatter-index-suite/friction-log.md`** — "**FL0** — plan obsolesced cleanly. The original persistent-index strategy is explicitly superseded by the stateless toolchain shipped under Task 016."

> **`tasks/011-skills-frontmatter-schema-files/friction-log.md`** — "**FL0** — plan obsolesced cleanly. Task 016 consolidated what Task 011 had decomposed into five separate JSON Schema files into a single canonical `maintenance/schemas/header-ontology.json`."

> **`tasks/012-review-pr-29/friction-log.md`** — "FL0 - Execution went flawlessly. The task successfully ran a Repo Coherence check following the git delta logic and updated missing task frontmatter attributes mechanically before successfully validating through the governance bash scripts."

> **`tasks/014-improve-maintenance-spec-from-session/friction-log.md`** — "**FL0** — plan obsolesced cleanly. Three of the seven captured findings have been resolved by sibling Tasks since 014 was filed, so the original 'treat F1–F7 as a single batch' plan no longer reflects the work that remains."

> **`tasks/047-cross-spec-contradiction-baseline/friction-log.md`** — "**FL0** — No friction encountered. The research executed cleanly: methodology validated against the known CONTR-001 anchor on first pass; 15 additional contradictions identified without ambiguity; governance checks passed after fixing sub-readme `type: index` and installing `jsonschema`."

> **`tasks/052-deepwiki-integration-artifact/friction-log.md`** — "FL0 — the M·A·S map was already self-consistent in task.md; the .devin/wiki.json schema admits no ambiguity; the only minor friction (FL1 candidate) was the /Agency-System/ isomorphism call, resolved by treating the row as a deliberate boundary marker."

> **`research/agent-prompt-specs-3-systems-sdd/reflection/friction-log.md`** — "Highest Frustration Level: FL0. The task proceeded exactly as expected. Instructions were clear, tools worked flawlessly, and no backtracking was required."

> **`research/agentic-session-continuity-spec/reflection/friction-log.md`** — "Highest Frustration Level: FL0. The instructions were clear and detailed. The requirement to manually track and script the pre-synthesis states using python was straightforward given the provided file schemas and clear structural prompts."

> **`research/prompt-engineering-principle-mechanizability/reflection/friction-log.md`** — "**FL0** — No friction encountered during research execution."

## §3. Upstream Consumers of FL0 (the value-justification core)

The orphaned-research panel (Task 014) and the Nightly Maintenance Run (MAINTENANCE.md §3.2) consume the friction-log corpus. FL0 entries provide the following measurable upstream signal that absence-of-log does not:

### §3.1 Falsifiable null baseline (the primary value)

When the maintenance run scans for friction patterns ([MAINTENANCE.md §3.2](../../../MAINTENANCE.md)), it computes ratios like "FL2 frequency in spec-amendment tasks vs spec-research tasks". Without an explicit FL0 declaration, the denominator is undefined: was there really no friction, or did the agent simply forget to log? The FL0 line is the **null hypothesis declaration**: "I executed this run and observed no friction-class events". Absence-of-log is unfalsifiable; an FL0 line is a positive claim that can be inspected.

**Concrete consumer.** `tools/check-trust.py` already enforces friction-log presence at task closure. Without a parsed FL value, it cannot flag the pathological case "log exists but no FL declared" — which is the exact failure mode the FL0-mandatory rule prevents.

### §3.2 Distribution-shift detection (the longitudinal value)

The 38% / 50% / 10% / 2% distribution across 60 logs is itself a corpus invariant. A maintenance run that observes a sudden drop in FL0 frequency (say, 15% in the next quarter's logs) can ask: did the work get harder, or did agents stop logging FL0? Without FL0 entries in the population, this question has no answer.

### §3.3 Pattern-recognition input (the semantic value)

Six of the 23 FL0 entries explicitly describe the "plan obsolesced cleanly" supersession pattern (tasks 004, 010, 011, 014, and two others). This is an *informative* FL0 signal — it tells the maintenance run that the Task's original plan was overtaken by sibling work, which is itself a friction-class observation about the *planning surface*, not the *execution surface*. An optional FL0 rule would lose this signal.

## §4. Verdict

**MANDATE FL0** — keep the rule, with the rationale clarified.

The FL0-mandatory rule is not bureaucracy. It is a falsifiable null-hypothesis declaration whose absence breaks three concrete upstream consumers (§3.1–§3.3). The legitimate friction the rule causes for agents — "I did nothing wrong, why must I log?" — is addressed by the rationale in §5 below.

The §FL.0 paragraph in FRUSTRATED.md MUST cite the empirical evidence (§3.1 in particular). The ST-2 linter MUST accept the variant forms enumerated in §2.2; pedantic format rejection would punish the agents who already log honestly.

## §5. Drop-in §FL.0 Paragraph for FRUSTRATED.md

The following paragraph is normative and MUST land in FRUSTRATED.md after the FL0 definition (§9–§11 in the current numbering), with no edits beyond fitting the surrounding heading style:

> **Why FL0 is mandatory.** An FL0 entry is a *falsifiable null-baseline declaration* — "I executed this run and observed no friction". Absent that declaration, the maintenance run cannot distinguish "no friction occurred" from "the agent forgot to log", which destroys the denominator for every friction-frequency metric. Empirical evidence: 38% of the 60 friction logs in the repo at 2026-05-07 are FL0; if FL0 were optional, half the population would silently disappear from longitudinal analysis. FL0 entries also carry semantic content (e.g. the "plan obsolesced cleanly" supersession pattern observed in 6 of 23 FL0 entries). Logging FL0 is *cheap* — one line — and it is the cheapness that makes the discipline sustainable. The friction the rule causes for agents is acknowledged; the friction the rule prevents (silent corpus drift) is larger.

(See `research/fl0-value-justification/output/SPEC.md` §3 for the full upstream-consumer enumeration.)
