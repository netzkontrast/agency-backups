# Method: Dramatica Quad (Fractal Recursion)

> **Category:** Structure
> **Load when:** `intent.methods_preference.structure` enthält `dramatica-quad`
> **Detail:** Volle Theorie in `skills/dramatica-theory/`

## §0 Konzept

Story Mind = ein Verstand, der ein Problem löst, betrachtet durch 4 Klassen
(Quad-Struktur). **Fraktale Rekursion:** Akt = Kapitel = Szene = Quad.

## §1 Die Quad-Struktur

```
        Universe (Situation)
              │
   Mind ─────┼───── Physics
              │
        Psychology (Manipulation)
```

- **Universe** + **Mind** = State Pair (external/internal state)
- **Physics** + **Psychology** = Process Pair (external/internal process)

## §2 Akt-Quad-Mapping

| Akt | Throughline-Fokus | Class-Aktivierung |
|-----|-------------------|-------------------|
| I — Setup | OS (Universe-State) | äußere Situation klar |
| II — Rising Action | MC (innerer Konflikt) | innerer State + Process |
| III — Reversal | IC (Process-Wandel) | äußerer Process gegen MC |
| IV — Resolution | SS (Relationship synthesis) | Process + State zusammen |

## §3 Pro-Kapitel Quad

Jedes Kapitel kann selbst ein Mini-Quad sein:
- Anfang (Setup) — eine Klasse aktiv
- Mitte (Conflict) — andere Klasse betreten
- Ende (Resolution) — beide Klassen interagieren

## §4 Pro-Szene Quad

Sogar einzelne Szenen:
- Knowing (Universe-State): Was wissen wir?
- Thinking (Mind-State): Was glauben wir?
- Doing (Physics-Process): Was tun wir?
- Being (Psychology-Process): Was sind wir?

→ Eine vollständige Szene berührt alle vier.

## §5 Anwendung in Phase 5

```
Pro Kapitel-Slot in scene-matrix.md:
  - chapter_class: <Universe|Physics|Mind|Psychology>
  - subQuad: 
      knowing: <storypoint>
      thinking: <storypoint>
      doing: <storypoint>
      being: <storypoint>
```

## §6 Kombination mit anderen Strukturen

- **40-Chapter-Matrix + Dramatica-Quad** = 40 Kapitel, jedes ein Mini-Quad
- **Hero's Journey + Dramatica-Quad** = 12 Stufen, jede ein Quad
- **Save-the-Cat + Dramatica-Quad** = 15 Beats, jeder ein Quad

## §7 Hard Rules

- **Quad-Klassen sind exklusiv pro Throughline** — OS+SS sharen Pair, MC+IC sharen Pair
- **Fraktale Rekursion ist optional** — minimal: Akt-Level Quad
- **Klasse-Zuordnung muss konsistent mit architecture.yaml sein**

## §8 Reference

Vollständige Theorie + worked examples in `skills/dramatica-theory/references/`
(insb. `01-foundations.md`, `06-storyforming.md`, `13-worked-storyforms.md`).
