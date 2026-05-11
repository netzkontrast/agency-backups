# Method: Research Domain Mapping

> **Category:** Research
> **Load when:** Phase 4 startet, Domain-Identifikation

## §0 Konzept

Strukturierte Identifikation von Forschungs-Domänen aus `intent.yaml`. Statt
ad-hoc Recherche: systematisches Mapping Genre → Domain → Tiefe.

## §1 Genre-zu-Domain-Mapping (heuristisch)

| Genre | Default Domains | Optional |
|-------|----------------|----------|
| Hard-SF | Physik, Cog Sci, KI, Math, Informationstheorie | Philosophie (bei `philosophy_integration_level`) |
| Literary | Sozialwissenschaft, Psychologie, lokale Kultur | Geschichte, Anthropologie |
| Horror | Psychologie (Trauma, Phobien), Folklore | Forensik, Pathologie |
| Fantasy | Mythologie, mittelalterliche Geschichte | Linguistik (für Sprach-Erfindung) |
| Thriller | Forensik, Recht, Geopolitik | Cybersecurity, Finance |
| Cli-Fi | Klimawissenschaft, Ökologie | Politikwissenschaft |
| Mystery | Forensik, Kriminologie | Psychologie |
| Historical | Spezifische Epoche, Sozial-, Wirtschaftsgeschichte | Mode, Kulinarik |

## §2 Tiefe-Heuristik

| Integration-Level | Recherche-Tiefe | Outputs nötig |
|-------------------|-----------------|---------------|
| `decoration` | surface (Wikipedia + 1-2 Übersichtsartikel) | ~500-1000 Wörter Notes |
| `frame` | standard (5-10 Sekundärquellen + 1-2 Primär) | ~2000-5000 Wörter |
| `engine` | exhaustive (Primärquellen, aktueller Forschungsstand, Konflikte zwischen Theorien) | ~5000-15000 Wörter |

## §3 Domain-Priorisierung

```
1. Engine-Level Domains zuerst (Pflicht für Plot-Engine)
2. Frame-Level Domains zweitens (Welt-Bibel-Anchor)
3. Decoration-Level Domains zuletzt (oder skippen wenn Zeit knapp)
```

## §4 Slot-Schema (in research/domains.yaml)

```yaml
domains:
  - id: dom_001
    name: "Kognitive Neurowissenschaft"
    integration_level: engine
    priority: core
    sub_topics:
      - "Global Workspace Theory"
      - "Integrated Information Theory"
      - "Default Mode Network"
    expected_brief: research/briefs/cog-neuro.md
    expected_findings: research/findings/cog-neuro.md
    status: pending  # pending / researching / complete
```

## §5 Hard Rules

- **Engine-Domains müssen tief recherchiert sein** — sonst zerfällt der Roman bei kundigen Lesern
- **Domain ≠ Konzept** — eine Domain umfasst mehrere Sub-Topics
- **Recherche ist iterativ** — neue Domains tauchen beim Drafting auf (Phase 6 → zurück zu Phase 4)
