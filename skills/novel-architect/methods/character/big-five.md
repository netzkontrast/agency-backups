# Method: Big Five (OCEAN)

> **Category:** Character Architecture
> **Load when:** `intent.methods_preference.character` enthält `big-five`

## §0 Wofür dieses Modell?

Wissenschaftlich am breitesten validiertes Persönlichkeits-Modell (Costa &
McCrae 1992). Geeignet für:
- Realistische Hauptfiguren (Literary Fiction, Thriller, Drama)
- Charaktere, deren Verhalten konsistent psychologisch motiviert sein muss
- Romane, in denen *psychologische Plausibilität* mehr zählt als mythische Tiefe

## §1 Slot-Schema

```yaml
psycho_model:
  primary: big-five
psycho_config:
  openness: 75            # 0-100, hoch = kreativ, neugierig, abstrakt
  conscientiousness: 60   # 0-100, hoch = organisiert, diszipliniert
  extraversion: 30        # 0-100, hoch = energisch, sozial
  agreeableness: 55       # 0-100, hoch = kooperativ, vertrauend
  neuroticism: 70         # 0-100, hoch = ängstlich, instabil
  facets:                 # optional, pro Trait Subfacetten
    openness:
      - imagination: high
      - artistic_interest: medium
```

## §2 Encoding-Patterns

- Hoch-Neuroticism → emotionale Reaktivität in Szenen sichtbar machen
- Niedrig-Extraversion → Innere Monologe wichtiger als Dialog
- Hoch-Openness → Charakter fragt „was wäre wenn" — geeignet für Hard-SF MC

## §3 Dramatica-Mapping

OCEAN ergänzt Dramatica nicht 1:1, sondern *kalibriert*:
- MC Approach: Doer (extraversion + conscientiousness hoch) vs. Beer (introvertiert, reflektiv)
- MC Mental Sex: Linear (low openness) vs. Holistic (high openness)

## §4 Hard Rules

- **Werte sind 0-100, nicht binär** — Persönlichkeit ist Spektrum
- **Konsistenz im Draft prüfen** — neurotischer Charakter darf nicht plötzlich gelassen sein
- **Trait-Veränderung über Arc = thematisch** — Big Five sagt Traits sind über Lebenszeit stabil; im Roman: Arc kann Traits *verschieben*, aber zentrale Werte bleiben

## §5 NCP-Mapping

Ein Big-Five-Charakter wird als ein `player` im NCP angelegt. Die OCEAN-Werte
gehören NICHT direkt ins NCP-Schema — NCP modelliert Dramatica-Slots (archetype,
perspectives, motivations), nicht Persönlichkeits-Traits. Speichere OCEAN-Werte
in `character-architecture.yaml` (Schema 3) und referenziere den Player über
`character_id` für Cross-Lookup. Optional: `custom_psycho_traits` Custom Field
im NCP (Namespace `custom_*` per AGENTS.md NO.2).
