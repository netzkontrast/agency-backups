# Method: Philosophy-as-Engine

> **Category:** Conflict Engine
> **Load when:** `intent.philosophy_integration_level: engine` (oder `frame`)
> **Pattern aus:** Dual-Kernel (Korrespondenz-Kohärenz-Konflikt)

## §0 Konzept

Philosophie ist **nicht Dekoration** — sie ist die *Konflikt-Engine*. Statt
philosophische Themen anzudeuten, werden zwei (oder mehr) philosophische
Positionen als treibende Kräfte des Plots installiert. Charaktere repräsentieren
Positionen; der Plot ist deren Auseinandersetzung.

Geeignet für:
- Hard-SF mit philosophischem Anspruch (Kohärenz Protokoll, Greg Egan, Ted Chiang)
- Literary Fiction mit ideen-getriebenen Plots
- Romane, in denen Charaktere *für* ihre Überzeugungen Konflikte erleiden

## §1 Pattern

```
1. Wähle 2-3 philosophische Positionen, die ein zentrales Problem unterschiedlich beantworten
2. Verkörpere jede Position in einem Charakter (typisch: MC eine Position, IC andere)
3. Plot-Beats sind Tests der jeweiligen Position
4. Klimax = Konfrontation der Positionen
5. Resolution = Synthese / Triumph einer Position / parakonsistente Aufrechterhaltung
```

## §2 Beispiele-Achsen

| Achse | Position A | Position B |
|-------|-----------|-----------|
| Wahrheitstheorie | Korrespondenz (extern) | Kohärenz (intern) |
| Bewusstsein | Funktionalismus | Phänomenologie |
| Identität | Substanzialismus (Kern-Selbst) | Bundle-Theorie (Strom) |
| Ethik | Konsequentialismus | Deontologie |
| Realität | Realismus | Konstruktivismus |
| Erkenntnis | Empirismus | Rationalismus |
| Sein | Monismus | Dualismus |
| Logik | Klassisch | Parakonsistent (Dialetheismus) |

## §3 Slot-Schema (in canon-meta.md)

```yaml
philosophy_engine:
  central_question: "Ist Bewusstsein simulierbar?"
  positions:
    - position_id: pos_a
      label: "Funktionalismus"
      character_carrier: char_001  # MC
      core_claim: "Mind ist Software, Substrat irrelevant"
    - position_id: pos_b
      label: "Phänomenologie"
      character_carrier: char_002  # IC
      core_claim: "Erleben kann nicht simuliert werden"
  conflict_dynamic:
    type: dialectic | parakonsistent | synthesis
    resolution_target: <synthesis | A_wins | B_wins | unresolved (Dialetheismus)>
```

## §4 Integration mit Dramatica

- Positionen ↔ Throughlines: MC trägt eine, IC andere
- Konflikt-Beats ↔ Storypoints (Goal, Cost, Requirements)
- Klimax = Crucial Element confrontation
- MC Resolve = Change (zur anderen Position) oder Steadfast (behält Position)

## §5 Hard Rules

- **Positionen müssen ernsthaft sein** — keine Strohmänner
- **Charaktere verkörpern Positionen, sind aber MEHR** als nur Sprachrohre
- **Plot-Beats müssen die Positionen TESTEN** — abstraktes Geplapper ist nicht Engine
- **Resolution ist *nicht* Patt** — auch parakonsistente Aufrechterhaltung ist Entscheidung

## §6 Anti-Patterns

- „Charaktere diskutieren über Philosophie" ohne Plot-Konsequenz = Frame, nicht Engine
- Philosophische Konzepte als Welt-Lore ohne Charakter-Verkörperung = Decoration
- Strohmann-Antagonist mit unhaltbarer Position = unfair, schwacher Roman

## §7 Reference

Dual-Kernel-Beispiele:
- `Dual-Kernel/Markdown-docs/ErkenntnistheorieFurNarrativesRomanprojekt.md`
- `Dual-Kernel/Markdown-docs/DialetheismusImKoharenzProtokoll.md`
- `Dual-Kernel/Markdown-docs/BridgingNarrativeTheoryAndAiAuthorship.md`
