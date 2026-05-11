# Method: Science-as-Engine

> **Category:** Conflict Engine
> **Load when:** `intent.science_integration_level: engine` (oder `frame`)

## §0 Konzept

Analog zu `philosophy-as-engine`, aber mit wissenschaftlichen Theorien als
Konflikt-Treiber. Geeignet für:
- Hard-SF (Greg Egan, Cixin Liu, Andy Weir)
- Cli-Fi (Climate Fiction mit echter Klimawissenschaft)
- Medical/Bio-Thriller
- Romane, in denen *Theorie-Konsequenzen* den Plot vorantreiben

## §1 Pattern

```
1. Wähle 1-3 wissenschaftliche Theorien, die das zentrale Problem unterschiedlich modellieren
2. Verkörpere jede Theorie in einem Charakter ODER einer Setting-Komponente
3. Plot-Beats sind Tests der Theorie-Vorhersagen
4. Klimax = Theorie A scheitert, B siegt — oder beide werden modifiziert
5. Resolution = neues theoretisches Verständnis
```

## §2 Beispiele-Achsen

| Achse | Theorie A | Theorie B |
|-------|-----------|-----------|
| Bewusstsein (Cog Sci) | Globaler Arbeitsraum (GWT) | Integrated Information Theory (IIT) |
| Quantenphysik | Kopenhagen-Deutung | Many-Worlds |
| Evolution | Strict Darwinismus | Punctuated Equilibrium |
| Kosmologie | Big Bang einmalig | Zyklisches Universum |
| KI | Symbolic AI | Connectionism |
| Klima | Anthropogen | Solar-zyklisch |
| Bio | Neo-Darwinismus | Symbiogenese |

## §3 Slot-Schema (in canon-meta.md)

```yaml
science_engine:
  central_phenomenon: "Bewusstsein in KI"
  theories:
    - theory_id: th_a
      label: "GWT"
      character_or_artifact: char_001  # Forscherin
      predictions: ["KI X wird selbstreferentiell sein", "Latenz erkennbar"]
    - theory_id: th_b
      label: "IIT"
      character_or_artifact: artifact_aegis  # KI selbst
      predictions: ["Phi-Wert messbar", "Kein klares Threshold"]
  experimental_setup:
    - in_world: "AEGIS-Test in Kapitel 18"
    - falsifies: th_a
    - confirms: th_b (partially)
```

## §4 Hard Rules

- **Wissenschaft muss WAHR sein** (im Roman-Universum konsistent). Bei realer Wissenschaft: aktueller Stand recherchieren (→ Phase 4)
- **Theorien müssen falsifizierbar sein** (zumindest im Roman-Setting)
- **Charaktere können sich irren** — Theorie A kann verlieren, das ist OK
- **„Pseudo-Wissenschaft" ist OK in Fantasy**, aber muss intern konsistent sein

## §5 Anti-Patterns

- Theorien ohne Plot-Konsequenz = Decoration
- Theorien, die zu spezifisch sind für Leser-Verständnis ohne Glossar
- „Wissenschaft erklärt alles" — schadet narrativer Spannung
