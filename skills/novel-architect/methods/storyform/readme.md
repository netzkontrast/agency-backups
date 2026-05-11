---
type: index
status: active
slug: novel-architect-methods-storyform
summary: "Dramatica Storyform Worksheet methods for Phase 2 — operational 8-step build-loop for OS/MC/IC/SS, Classes, Dynamics, Story Points, Crucial Element, Signposts."
created: 2026-05-12
updated: 2026-05-12
---

# Methods: Storyform (Phase 2 build-loop)

Operationale Methoden-Files für das Aufbauen eines Dramatica-Storyform.
Phase 2 (Narrative Architecture) lädt das `worksheet-workflow.md` als
Default-Methode für `intent.methods_preference.structure` Auswahlen, die
`dramatica-quad` enthalten (oder leerer Default).

## Files

| File | Lädt wann | Zweck |
|---|---|---|
| [`worksheet-workflow.md`](./worksheet-workflow.md) | Phase 2.1 selects methods + `dramatica-quad`-default | Operationaler 8-Step-Loop: per-step askuser shape, decision heuristic, recovery path, NCP slot map |

## Relation zu anderen Verzeichnissen

- **`phases/phase2-narrative-architecture.md`** — gate-binding contract
  (what gets asked, at which gate, what's the file output). References
  `worksheet-workflow.md` for operational detail.
- **`methods/structure/dramatica-quad.md`** — fractal Akt = Kapitel = Szene
  Quad-rekursion. Sister method; `worksheet-workflow.md` is *building*
  the storyform, `dramatica-quad.md` is *applying* it in Phases 2 + 5.
- **`methods/conflict/dual-storyform.md`** — 5D-Interferenz-Regeln when
  `intent.dramatica_storyform_count: dual`. The worksheet-loop runs
  through BOTH narratives simultaneously per HR.P2.6.
- **`assets/decision-heuristic-quick-ref.md`** — inline-quotable
  heuristics; the worksheet-loop's HR.M2.3 mandates embedding an excerpt
  in every Step 2–7 askuser.
- **`assets/architecture-template.yaml`** — Schema 2; the worksheet-loop's
  per-step outputs land in this schema's named blocks (Step 1 →
  `throughlines.*.name`, Step 6 → `crucial_element`, etc.).

## Source Specs (external)

- [`dramatica-theory/references/00-storyform-worksheet.md`](../../../dramatica-theory/references/00-storyform-worksheet.md) — the worksheet itself (theory SSoT).
- [`dramatica-theory/references/10-decision-heuristics.md`](../../../dramatica-theory/references/10-decision-heuristics.md) — full heuristics (the quick-ref is a condensation).
- [`dramatica-theory/references/00-storyform-validation.md`](../../../dramatica-theory/references/00-storyform-validation.md) — the 5 hard checks Phase 2.11 runs.
- [`dramatica-theory/references/11-anti-patterns.md`](../../../dramatica-theory/references/11-anti-patterns.md) — anti-patterns surfaced mid-loop.

## Forward-compat note (Task 071 sub-skill split)

When Task 071 lands (`novel-architect-structure/` sub-skill refactor),
this whole directory will `git mv` to
`skills/novel-architect-structure/methods/storyform/` unchanged. All
relative links in `worksheet-workflow.md` are designed to survive the
move (they reach `dramatica-theory` through `../../../` and `decision-
heuristic-quick-ref.md` through `../../assets/`).

## Assumptions Log

- (none)
