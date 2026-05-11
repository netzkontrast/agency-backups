# Method: TSDP + IFS (Tertiary Structural Dissociation + Internal Family Systems)

> **Category:** Character Architecture
> **Load when:** `intent.methods_preference.character` enthält `tsdp-ifs`,
> oder Phase 3 spezifiziert TSDP/IFS für einen Charakter

## §0 Wofür dieses Modell?

Modelliert **fragmentierte Identität** wissenschaftlich fundiert auf
trauma-informierter Psychologie. Geeignet für:
- Protagonisten mit komplexer Trauma-Vorgeschichte (z.B. Kael in Kohärenz-Protokoll)
- Romane, in denen Multiplizität *Feature* statt Pathologie ist
- Charaktere, die nicht als kohärent-individualistisches Selbst dargestellt werden

**NICHT geeignet für:**
- Klassisch-integrierte Hauptfiguren
- Romance/Coming-of-Age mit linearer Identitäts-Findung (Big Five passt besser)

## §1 Theoretische Grundlage

**TSDP** (Tertiäre Strukturelle Dissoziation, van der Hart et al.):
- **ANP** (Apparently Normal Personality): Host, rational/funktional
- **EP** (Emotional Personality): trauma-fixiert, oft kindlich oder protektiv
- **Sub-EPs**: spezialisierte Trauma-Antworten

**IFS** (Internal Family Systems, Schwartz):
- **Self** (zentrale Bewusstseinsinstanz, „True Self")
- **Parts**: Manager (protektiv), Firefighter (impulsiv), Exiles (verletzt)

## §2 Slot-Schema für `character-architecture.yaml`

```yaml
- id: char_001
  name: "Kael"
  psycho_model:
    primary: tsdp-ifs
  psycho_config:
    host:
      name: "Kael"
      role: ANP
      function: "Analytisch, sucht Wahrheit"
      stability: "präsent in 70% der Szenen"
    alters:
      - name: "Lex"
        role: EP
        function: "Hyper-analytisch, dissoziiert in Krisen"
        somatic: "Stirnrunzeln, Atem flach"
        triggers: ["technischer Konflikt", "AEGIS-Direktive"]
        relationship_to_host: "Kooperativ, aber dominant in Crisis"
      - name: "Kiko"
        role: EP-child
        function: "Emotional, traumatisch fixiert"
        somatic: "Frösteln, Augen weiten"
        triggers: ["Verlassen", "Lärm"]
        relationship_to_host: "Protektiv, aber chaotisch"
    self_state:
      access_level: "intermittierend"
      target: "Funktionale Multiplizität (NICHT Fusion)"
```

## §3 Encoding-Patterns (für Drafting)

### §3.1 Persona-Wechsel sichtbar machen

- POV-Shift im Text (ohne kursiv/Fußnote — nur strukturell)
- Somatic-Marker am Anfang einer Szene
- Sprache wechselt (Lex = lange Sätze, Kiko = fragmentiert)

### §3.2 Conflict zwischen Personas als interner Plot

- Personas haben *Ziele*, nicht nur Modi
- Konflikt zwischen Lex und Kiko = Sub-Plot

### §3.3 Self-Integration als Arc, nicht Endpunkt

- Klassischer Roman: Persönlichkeit „heilt" → integriert
- TSDP-Roman: „Heilung" = funktionale Kooperation, nicht Verschmelzung
- Endpunkt: Self moderiert Persona-Rat, nicht löscht sie

## §4 Dramatica-Mapping

Pro Persona kann eine Dramatica-Rolle in Storyform A oder B haben:
- Host (Kael) = MC
- Lex = IC (challenger of MC's worldview)
- Kiko = Influence Character im OS

**Bei dual storyform:** Persona-Konstellation kann variieren (Kael ist MC in A, IC in B).

## §5 Hard Rules

- **Personas haben Namen, Rollen, Funktionen** — niemals abstrakte „Stimmen"
- **Somatic-Marker müssen konsistent sein** — niemals flexible „Schaudern" für alle
- **Trigger-Conditions müssen plot-kompatibel sein** — sonst zerfällt der Plot
- **Self ist NICHT eine weitere Persona** — Self ist die *meta*-Position

## §6 Anti-Patterns

- **„DID als Plot-Twist"** — pathologisierend, klischeehaft
- **Personas mit identischem Vokabular** — sie sind Teil-Selbste, nicht Synonyme
- **Self-Integration als „Auflösung"** — verletzt das IFS-Modell

## §7 References

- Van der Hart, O., Nijenhuis, E., & Steele, K. (2006). *The Haunted Self.* — TSDP-Quelle
- Schwartz, R. (1995). *Internal Family Systems Therapy* — IFS-Quelle
- Im Dual-Kernel-Repo: `Markdown-docs/KaelsDissociativeArchitectureAnalysis.md` (worked example)

## §8 NCP-Mapping

Jede Persona kann als separater `player` im NCP angelegt werden (mit derselben
`character_name` aber unterschiedlicher `id`). Alternativ: ein Player mit
`subpersonalities[]` Custom Field (NCP `custom_*` Namespace).

Bevorzugt: separate Players → Storybeats können explizit auf Personas-Wechsel
referenzieren.
