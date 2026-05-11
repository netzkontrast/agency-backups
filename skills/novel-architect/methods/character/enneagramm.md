# Method: Enneagramm

> **Category:** Character Architecture
> **Load when:** `intent.methods_preference.character` enthält `enneagramm`

## §0 Wofür dieses Modell?

9-Typen-Modell mit Stress/Integration-Pfaden. Wissenschaftlich weniger
validiert als Big Five, aber **stark für narrative Motivation**. Geeignet für:
- Charaktere mit klarer Motivations-Struktur
- Romance, Drama, Coming-of-Age
- Ensembles (verschiedene Typen geben verschiedene Konflikt-Vektoren)

## §1 Die 9 Typen (Kurzform)

1. **Der Reformer** — Perfektionist, prinzipientreu
2. **Der Helfer** — Beziehungs-orientiert, gibt sich auf
3. **Der Erfolgreiche** — Image-bewusst, ambitioniert
4. **Der Individualist** — emotional, einzigartig
5. **Der Forscher** — wissensorientiert, distanziert
6. **Der Loyale** — sicherheitsorientiert, ängstlich oder rebellisch
7. **Der Enthusiast** — vielseitig, flüchtet vor Schmerz
8. **Der Herausforderer** — kontrollierend, schützt Schwächere
9. **Der Friedliebende** — harmoniebedürftig, vermeidet Konflikt

## §2 Slot-Schema

```yaml
psycho_model:
  primary: enneagramm
psycho_config:
  type: 5                  # Hauptyp 1-9
  wing: 4                  # Flügel (benachbart), z.B. 5w4 = Forscher mit Individualisten-Flügel
  integration_path: 8      # Bei psychischer Gesundheit Bewegung zu Typ 8
  disintegration_path: 7   # Bei Stress Bewegung zu Typ 7
  level_of_health: 4       # 1-9 (1 = gesund, 9 = pathologisch)
  core_fear: "Hilflos zu sein"
  core_desire: "Kompetent und fähig zu sein"
```

## §3 Encoding-Patterns

- Stress-Szene → Charakter zeigt Disintegration-Typ-Verhalten
- Heilende Szene → Charakter zeigt Integration-Typ-Verhalten
- Core Fear/Desire steuern Motivations-Konflikte

## §4 Dramatica-Mapping

- Typ → Archetyp-Tendenz (z.B. Typ 1 → Protagonist mit „rechtem Weg" Storypoint, Typ 8 → Contagonist oder Antagonist)
- Integration/Disintegration = Dramatica Arc (Change/Steadfast)

## §5 Hard Rules

- **Wing ist 4 oder 6** (benachbart), niemals andere
- **Integration/Disintegration sind FIX pro Typ** (siehe Standard-Tabelle), nicht frei wählbar
- **Level of Health beeinflusst alle Darstellungen** — Typ 5 Level 2 ≠ Typ 5 Level 7
