---
type: note
status: active
slug: adr-spec-research-synthesis-m13
summary: "M13 Adversarial Query Expansion across adjacent / opposing / abstraction / orthogonal axes; also hosts the five mandatory CB0 reflection checkpoints."
created: 2026-05-05
updated: 2026-05-05
---

# [M13] Adversarial Query Expansion

Run across all four axes per the originating Gemini research prompt. Each axis MUST surface ≥ 1 finding that modifies or hardens the conclusion.

## Axis 1 — Adjacent

**Query:** "What governance patterns in similar multi-agent / ADR-aware repos contradict the current model?"

**Sample probes:**
- `adr-tools` (Pryce) — sequential numbering, `docs/decisions/` default, no DAG, no synthesis pipeline.
- `log4brains` (Thomvaill) — static-site rendering, frontmatter-driven, supports supersession via `supersedes` field, no AGENTS.md synthesis.
- MADR (Kopp et al.) — template definition only; no enforcement tooling.
- `structurizr-adr` — diagrams-first, ADRs are second-class.
- `AGENTS.md` ecosystem — convention emerging; competes with `llms.txt` at the web-root level.

**Findings:**
- Sequential numbering is universal in adr-tools / log4brains. Repo-native spec adopts `ADR-NNNN` (B7). **Hardens** §4.1 ADR.A.2.2.
- Static-site rendering is OUT of scope here; the repo has no website. **No change** to spec.
- log4brains' supersession-via-frontmatter is the same model adopted here (`adr_supersedes`). **Confirms** §6.1 ADR.A.4.2.
- MADR's lack of enforcement is exactly the gap this spec fills via `agency-adr validate`. **Hardens** §7.1.

**Modified conclusion?** Yes — the spec gained explicit alignment with `adr_id: ADR-NNNN` formatting (matches log4brains conventions, eases tooling reuse).

## Axis 2 — Opposing

**Query:** "What would cause this ADR governance model to *fail* in this repo?"

**Sample probes:**
- Agents simply never author ADRs (the corpus stays empty; AGENTS.md guarded section stays empty).
- Synthesis pipeline silently produces wrong AGENTS.md (a fidelity-check regression goes unnoticed).
- The guarded-section markers get edited by hand and never restored.
- Two parallel branches each create `ADR-0042` and merge non-deterministically (analogous to the duplicate `task_id` problem already documented in `MAINTENANCE.md §3.5`).
- The `decisions/` folder is renamed by an unaware refactor.

**Findings:**
- **Empty corpus:** explicitly handled — `agency-adr validate` exits 0 if `decisions/` is absent or empty. **Documented** in `analysis.md §E`.
- **Silent fidelity regression:** mitigated by the ≥ 0.95 floor + exit-1 on miss. But the *measurement algorithm* itself is `[OPEN]`. **Surfaced** in §8 as the highest-priority unblock for Task 029.
- **Manual edit of guarded section:** the next synthesis run overwrites it; humans can't reliably preserve their edits. **Mitigation:** the `<!-- AGENT-WRITTEN. DO NOT EDIT BY HAND. -->` notice MUST be the first line inside the markers. **Hardens** §2.3.
- **Duplicate `ADR-NNNN`:** inherits the duplicate-`task_id` failure mode. The spec MUST cite `MAINTENANCE.md §3.5` as the precedent, but cycle detection alone does not catch ID collisions. **New normative statement added:** §7.1 ADR.A.5.6 — "`agency-adr validate` MUST emit ERROR `ADR.A.5.6` on duplicate `adr_id` across the corpus."
- **Folder rename:** `tools/check-governance.sh` will continue to pass (validator exits 0 on absence). **Mitigation:** the validator's behaviour MUST also flag any reference to a now-orphaned ADR via `adr_supersedes` as ERROR `ADR.A.5.7`. **New normative added:** §7.1.

**Modified conclusion?** Yes — added two new normative statements to §7 (ADR.A.5.6 duplicate-id detection; ADR.A.5.7 orphan-reference detection) that the original Gemini draft did not surface.

## Axis 3 — Abstraction

**Query:** "What higher-level principle is the entire spec resting on? Is it honoured by this repo's culture?"

**Principle identified:** *Normative governance can be both human-narrative and machine-extractable, simultaneously, without sacrificing fidelity.*

**Repo evidence:**
- Every existing root spec is RFC 2119 + Gherkin (machine-extractable) wrapped in lowercase rationale prose (human-narrative). **Confirms** the principle.
- `header-ontology.json` is the binding source for tooling, but `TASK.md §3` is the human-narrative mirror — the principle is *operationalised* in this very codebase. **Confirms.**
- The synthesis pipeline (proposed here) is the same pattern at one level up: ADRs are human-narrative; the guarded section in `AGENTS.md` is machine-extractable. **Consistent.**

**Modified conclusion?** No, but the rationale prose in `output/SPEC.md §2.3` and §5.3 cites this principle explicitly so future maintainers can challenge it directly.

## Axis 4 — Orthogonal (MDL / Token Budget)

**Query:** "Apply the MDL lens. Given current `AGENTS.md` ≈ N tokens and a 2,000-token guarded-section budget, what is the maximum ADR corpus that fits?"

**Estimation:**
- Current `AGENTS.md`: `wc -w` ≈ 3,600 words → ≈ 4,800 tokens by 1.33× heuristic.
- Guarded-section target: 2,000 tokens.
- Per-ADR average MDL contribution (one BCP-14 normative line + one footer cite): ≈ 35–45 tokens after extraction-and-deduplication.
- **Budget arithmetic:** 2,000 ÷ 40 ≈ **50 ADRs** in the synthesised section.
- 50 ADRs is comfortable for a typical 5–10-year-old repo; this repo currently has zero formal ADRs and ~14 implicit ones.

**Findings:**
- The 2,000-token limit is *not* a binding constraint at current corpus size; it is a future-proofing rail.
- The empirical floor on `AGENTS.md` non-guarded content (≈ 4,800 tokens) makes the *total* file ≈ 6,800 tokens after synthesis. This is well within Claude's optimal-attention window but is itself a candidate for a future `[OPEN]` reduction Task.

**Modified conclusion?** Yes — added §5.3 rationale paragraph noting the 50-ADR practical capacity at the 2,000-token limit, and the `[OPEN]` item in §8 about empirical token-counting against the actual `AGENTS.md`.

## Reflection Regime (CB0 — Five Mandatory Checkpoints)

| Checkpoint | Belief & Confidence | Strongest Counter-Evidence | Weakest Assumption | De-Anchoring Strategy | Next Action |
|---|---|---|---|---|---|
| Kickoff | The Gemini draft is a sound theoretical scaffold; the work is to ground it. (high) | Several Gemini claims (C1, C3, C4) are repo-violating. | I assume "ground it" is achievable without a full rewrite. | Treat the §0–§9 schema as the structural frame; re-derive every block. | Read all root specs and tooling listed in the prompt. |
| Mid-run | The five integration questions can each be `[RESOLVED]` or honestly labelled `[OPEN]`. (medium) | Some questions (Q5 migration cardinality) genuinely need human judgement. | I assume my brainstorm is exhaustive. | Explicitly enumerate alternates per question; reject only with stated rationale. | Produce `workspace/brainstorm.md` with labelled conclusions. |
| Post-M13 | The four axes hardened the spec rather than overturning it. (high) | The opposing axis surfaced two new normatives (ADR.A.5.6 / ADR.A.5.7) that were missing. | I assumed the Gemini draft was complete on Aspect 5. | Add ADR.A.5.6 and ADR.A.5.7 to §7.1 of `output/SPEC.md`. | Draft §7 with the additions. |
| Pre-synthesis | The §0–§9 spec is comprehensive and deployable. (high) | The fidelity-metric algorithm is genuinely undefined; this is a real `[OPEN]`. | I may be undercounting the empirical token cost of synthesis pipeline runtime. | Surface the fidelity algorithm and the token-count empirics as `[OPEN]` in §8 with explicit owners. | Draft `output/SPEC.md`. |
| Post-synthesis | The spec is repo-native, deployable, and honours every existing convention. (high) | The guarded-section convention is new to the repo; future agents may not know about it. | I assume the marker placement question is safely deferable to Task 028. | Document marker semantics in §2.3 with the strongest possible language; cite `[DEFERRED to Task 028]` for placement only. | Run `tools/check-governance.sh`; close Task 027. |
