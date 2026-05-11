---
type: index
status: active
slug: novel-architect-structure
summary: "Directory index for novel-architect-structure sub-skill (Phase 2/5 plot-structure templates: 40-chapter-matrix, hero's-journey, save-the-cat, dramatica-quad)."
created: 2026-05-11
updated: 2026-05-11
---

# novel-architect-structure

**What:** Plot-Struktur Sub-Skill von [`novel-architect`](../novel-architect/).
Stellt Strukturschablonen bereit für Phase 2 (Narrative Architecture) und
Phase 5 (Scene Matrix) — 40-Kapitel-Matrix, Hero's Journey, Save the Cat,
Dramatica Quad.

**Why here:** Pro [`SKILLS.md §2`](../../SKILLS.md), jede Capability lebt in
einem eigenen `/skills/<slug>/`-Verzeichnis. Der Sub-Skill ist als Teil der
v1.1.0 Sub-Module Refaktorisierung (Task 071) aus dem monolithischen
`novel-architect` extrahiert worden. Strukturschablonen sind Phase-2/Phase-5-
spezifisch und benötigen keine Bootstrap-, Intent-, oder Drafting-Logik —
ideal für die Sub-Skill-Trennung.

## Navigation

- [SKILL.md](./SKILL.md) — Skill-Spec: Scope, Methoden-Tabelle, Delegation Contract.
- [methods/](./methods/) — 4 Struktur-Methoden.
  - [methods/readme.md](./methods/readme.md) — Methods Library Index.
  - [methods/40-chapter-matrix.md](./methods/40-chapter-matrix.md)
  - [methods/heroes-journey.md](./methods/heroes-journey.md)
  - [methods/save-the-cat.md](./methods/save-the-cat.md)
  - [methods/dramatica-quad.md](./methods/dramatica-quad.md)

## Assumptions Log

- (none)
