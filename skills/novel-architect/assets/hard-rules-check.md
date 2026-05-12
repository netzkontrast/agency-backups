# Hard-Rules Check (Storyform Validation)

> Checkliste-Schablone für Phase 2 Gate 2 / Gate 3. Pro Storyform einmal
> ausfüllen; gefüllte Schablone landet in `<workspace>/hard-rules-check.md`
> (per `render/io_helpers.py`, file-first).
>
> Vollständige Hard-Rules-Logik siehe
> [`skills/novel-architect-structure/methods/validation/hard-rules.md`](../../novel-architect-structure/methods/validation/hard-rules.md).

## Project Metadata

- **Slug:** `<project-slug>`
- **Storyform Count:** `single` | `dual`
- **Generated:** `<utc-iso>`
- **Validated by:** novel-architect-structure v1.1.0
- **Gate:** Gate-2 / Gate-3

## Hard-Rule Results

| Rule | Statement | Result | Diagnostic (if FAIL) |
|------|-----------|--------|-----------------------|
| H1 | Exactly 4 Throughlines (OS, MC, IC, SS) | [ ] PASS / [ ] FAIL | |
| H2 | Each Class used exactly once | [ ] PASS / [ ] FAIL | |
| H3 | MC Class ↔ IC Class complementary | [ ] PASS / [ ] FAIL | |
| H4 | OS Class ↔ SS Class complementary | [ ] PASS / [ ] FAIL | |
| H5 | Concern ∈ Class's open Type set | [ ] PASS / [ ] FAIL | |
| H6 | Issue/Problem/Solution same Quad in Class | [ ] PASS / [ ] FAIL | |
| H7 | Problem ↔ Solution dynamic-pair partners | [ ] PASS / [ ] FAIL | |
| H8 | Symptom ↔ Response dynamic-pair partners (same Quad) | [ ] PASS / [ ] FAIL | |
| H9 | Driver ∈ {Action, Decision} (story-wide) | [ ] PASS / [ ] FAIL | |
| H10 | Limit ∈ {Optionlock, Timelock} (story-wide) | [ ] PASS / [ ] FAIL | |
| H11 | Outcome ∈ {Success, Failure}, Judgment ∈ {Good, Bad} | [ ] PASS / [ ] FAIL | |
| H12 | MC Approach ∈ {Do-er, Be-er}, Mental Sex ∈ {Linear, Holistic} | [ ] PASS / [ ] FAIL | |

## Gate Decision

- [ ] **PASS** — All Hard Rules satisfied. Gate may proceed.
- [ ] **FAIL** — At least one Hard Rule violated. Worksheet-Loop MUST re-ask the offending slot before re-validation.

## Soft-Rule Warnings (Informational)

Soft Rules werden separat (Linter WARN-tier) erfasst und blockieren das
Gate **nicht**. Hier nur als Kontext für den User-Approval-Schritt
auflisten:

| Soft Rule | Warning |
|-----------|---------|
| S1 | Premise is articulable in one sentence |
| S2 | IC's challenge to MC is concrete |
| S3 | SS has its own arc (not just MC+IC scenes) |
| S4 | Each thematic story point is concrete enough to write |
| S5 | Goal, Consequences, Forewarnings, Requirements form one coherent arc |
| S6 | Costs and Dividends are visible (not just structural) |
| S7 | At least one full Signposts-and-Journeys progression picked |
| S8 | Author's Intent isn't ironic relative to the storyform |

> Provenance: `skills/dramatica-theory/references/00-storyform-validation.md` §"Soft checks" (S1–S8).
