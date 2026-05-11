# Method: Jung Archetypes & Individuation

> **Category:** Character Architecture
> **Load when:** `intent.methods_preference.character` enthält `jung-archetypes`

## §0 Wofür dieses Modell?

Tiefenpsychologische Architektur nach C.G. Jung. Geeignet für:
- Mythische / Archetypische Romane (Fantasy, Magical Realism, Literary)
- Romane mit starkem Unbewusstem-Element
- Coming-of-Age-Plots mit Individuation als zentralem Arc

## §1 Kern-Archetypen

| Archetyp | Funktion | Roman-Rolle |
|----------|----------|-------------|
| **Self** | Zentrum der Psyche, Ganzheit | Endpunkt der Individuation |
| **Ego** | Bewusstes Selbstbild | MC-Perspektive |
| **Persona** | Soziale Maske | Außenwelt-Selbst |
| **Shadow** | Verdrängte Anteile | Antagonist oder IC |
| **Anima/Animus** | Inneres weibliches/männliches | IC oft im RS-Throughline |
| **Wise Old Man/Woman** | Weisheit | Guardian-Archetyp |
| **Trickster** | Chaos, Transformation | Contagonist |
| **Mother** | Nährend / verschlingend | Archetyp im OS |
| **Hero** | Mut, Aufbruch | Protagonist |

## §2 Slot-Schema

```yaml
psycho_model:
  primary: jung-archetypes
psycho_config:
  primary_archetype: Hero
  shadow_content:
    - "Verdrängte Wut"
    - "Selbstzweifel"
  anima_animus_projection:
    target_character: char_002
    quality: "Inkonsistenz, Intuition"
  individuation_stage: "Confrontation with Shadow"  # Steps: Persona → Shadow → Anima/Animus → Self
  symbolic_motifs:
    - "Wasser"
    - "Spiegel"
    - "Schwellen"
```

## §3 Individuations-Arc als narrativer Bogen

Klassische Individuation:
1. **Persona-Identifikation** (junger Charakter, Image-zentriert)
2. **Shadow-Confrontation** (Antagonist als Schatten-Projektion)
3. **Anima/Animus-Integration** (Beziehung als Spiegel)
4. **Self-Realisation** (Ganzheit, transzendent)

→ Mappt direkt auf Dramatica MC Resolve = Change

## §4 Dramatica-Mapping

- Shadow → IC oder Antagonist (challenger of MC's worldview)
- Wise Old Man/Woman → Guardian (Dramatica Archetyp)
- Self → Ziel des MC Arcs (Change)

## §5 Hard Rules

- **Archetypen sind nicht Personen** — sie sind Psyche-Funktionen. Mehrere Charaktere können denselben Archetyp tragen
- **Individuation ist nichtlinear** — Rückfälle sind Teil des Prozesses
- **Symbolische Motive müssen konsistent sein** — Wasser kann nicht zugleich „Tod" und „Geburt" sein, ohne dass das thematisiert wird
