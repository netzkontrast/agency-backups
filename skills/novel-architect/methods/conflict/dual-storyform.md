# Method: Dual Storyform (5D Interference)

> **Category:** Conflict Engine
> **Load when:** `intent.dramatica_storyform_count: dual` ODER
> `intent.methods_preference.conflict` enthält `dual-storyform`
> **Pattern aus:** Dual-Kernel (Kohärenz Protokoll Storyform A + B)

## §0 Konzept

Zwei Dramatica-Storyforms parallel encodiert, die als **5D-Interferenz**
wirken. Anders als zwei separate Plots: die Storyforms beziehen sich
aufeinander, ihre Throughlines durchdringen sich. Resultat: dichteres,
mehrdeutiges narratives Feld.

Geeignet für:
- Hard-SF mit metaphysischer Anspruchstiefe
- Romane mit Multi-POV und Realitäts-Layer-Konflikt
- Storys, die *zwei zentrale Fragen* gleichzeitig beantworten

**WARN:** Sehr advanced. Verdoppelt Aufwand in Phase 2, 3, 5. Für ersten Roman nicht empfohlen.

## §1 Pattern

```
1. Identifiziere zwei zentrale Fragen, die beide den Roman tragen können
2. Erstelle Storyform A für Frage 1, Storyform B für Frage 2
3. NICHT: A in Akt I-II, B in III-IV (sequenziell)
4. SONDERN: A + B parallel pro Kapitel, beide aktiv
5. Charaktere können unterschiedliche Throughline-Assignments in A vs. B haben
6. Klimax: 5D-Interferenz = beide Storyforms gleichzeitig konvergieren
```

## §2 Konkretes Beispiel (Kohärenz Protokoll)

- **Storyform A:** Kael's Weg zur funktionalen Multiplizität (innerer Konflikt)
  - MC: Kael (Host)
  - IC: Lex (analytische Persona)
  - OS: Trauma-Reintegration
- **Storyform B:** Decodierung der AEGIS-Matrix (äußerer Konflikt)
  - MC: Kael (im Konflikt mit AEGIS)
  - IC: AEGIS (als System)
  - OS: Wahrheits-vs-Stabilitäts-Direktive

Bei dual: Kael ist MC in beiden, aber in A geht es um Innenwelt, in B um Außenwelt. Die 5D-Interferenz: Innen- und Außenwelt sind nicht-trennbar, jeder Beat in A hat Echo in B.

## §3 NCP-Pattern

```yaml
narratives:
  - id: storyform_a
    label: "Innere Multiplizität"
    throughlines: { ... }
    dynamics: { ... }
    subtext: { players, storypoints, storybeats, dynamics }
  - id: storyform_b
    label: "Äußere Matrix-Dekodierung"
    throughlines: { ... }
    dynamics: { ... }
    subtext: { players, storypoints, storybeats, dynamics }
```

Pro Kapitel: ein storybeat in jedem narrative, parallel orchestriert.

## §4 Charakter-Spiegelung

Ein Charakter kann unterschiedliche Rollen haben:
- Kael in A: MC, Change, Doer
- Kael in B: MC, Change, Doer (gleich)
- Lex in A: IC
- Lex in B: Sidekick (oder Skeptic, je nach narrative)

In NCP: gleiche `id` für Player, unterschiedliche `perspectives` per narrative.

## §5 Hard Rules

- **Beide Storyforms parallel, niemals sequenziell**
- **Throughline-für-Throughline durch BEIDE simultan encodieren**
- **5D-Interferenz muss thematisch begründet sein** — nicht bloß zwei Plots übereinander
- **Pro Kapitel: Storybeat in beiden narratives** — sonst zerfällt die Interferenz

## §6 Anti-Patterns

- **Zwei Storyforms = zwei Romane in einem** — nein, das ist additive Längung
- **Storyform B ist Sub-Plot** — nein, dann reicht single Storyform mit B-Story
- **Storyforms erst in Phase 5 koppeln** — zu spät; Konflikt-Verknüpfung muss in Phase 2

## §7 Reference

- `Dual-Kernel/Markdown-docs/KoharenzProtokoll39KapitelMatrix.md`
- `Dual-Kernel/Markdown-docs/DramaturgicalPrecisionDeconstructingTheIrreversibleConflictInKoharenzProtokoll.md`
