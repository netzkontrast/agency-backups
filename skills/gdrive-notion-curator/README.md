# gdrive-notion-curator (v0.4.0)

MCP-driven Drive-zu-Notion Curator. Drive ist passiver Bucket, Notion ist Strukturebene.

## In 30 Sekunden

```
1. setup        — One-time: 3 Notion-DBs anlegen + komplettes Source-Listing + alle Files verarbeiten
2. routine      — Daily: filter createdTime > newest_in_last_run, cap 50 ASC, Status-Report
3. review-inbox — On-demand: Inbox durchgehen mit askuser
4. repair       — On-demand: Drive /curated/ vs Notion Konsistenz checken (komplett-Listing)
```

Siehe `SKILL.md` für Trigger-Phrasen.

## Was sich gegenüber v0.3.0 geändert hat

| Bereich | v0.3.0 | v0.4.0 |
|---|---|---|
| Operations | setup / sweep / review / repair | setup / routine / review-inbox / repair |
| Setup | nur DBs anlegen (Phase 0) | DBs anlegen + komplett-Listing + alle Files verarbeiten (Phase 0+A kombiniert) |
| Sweep | Phase A unbegrenzt + Phase B cap 30 | nur routine, cap 50 |
| Routine-Filter | `createdTime >= oldest_in_last_run` (defensiv) | `createdTime > newest_in_last_run` (klarer) |
| Sortierung | "ASC by createdTime" — implizit | client-side ASC explizit dokumentiert (Drive-MCP hat kein orderBy) |
| Backlog-Handling | unklar, askuser-Pause nach 20 | Status-Report mit Anzahl übriger Files, User triggert nochmal |
| Resume-Logic | komplex (>= oldest + Skip-Filter) | einfach (> newest, File-by-File-Writes garantieren Crash-Safety) |

## Voraussetzungen

| Tool | Wo | Was |
|---|---|---|
| Drive-MCP | in der Claude-Sitzung | für Drive-Zugriff |
| Notion-MCP | in der Claude-Sitzung | für DB-Verwaltung |
| Notion Page | im User-Workspace | als Parent für die 3 DBs |
| Drive-Folder | im Drive-Account | `/Claude/` Root + Source-Folder ("Inbox") |

## Architektur

```
DRIVE                                   NOTION
─────                                   ──────
/Claude/                                📁 Claude Drive Files (DB 1)
├── (Source-Folder)                        ├── Pro File ein Eintrag
│                                          ├── Original Drive ID + Curated Drive ID
└── curated/                               ├── Sprache, Topic, Status, Run-ID
    ├── slug-filename-1.md             📚 Claude Topics (DB 2)
    ├── slug-filename-2.md                ├── Eine Page pro Topic
    └── ...                                ├── Sub-Pages = File-Inhalte (Auszug)
        flach, einmal kopiert.         📥 Claude Topic Inbox (DB 3)
        slug-filename mit              ├── Eine Page pro Topic-Vorschlag
        Topic-Keywords drin.           └── Awaits askuser-Approve
```

## Operating-Prinzipien

1. **Drive ist write-once-additive** — copy + create_folder, nichts sonst
2. **Notion ist State-Source** — Skill-Start zieht aktuellen State aus Notion
3. **DRINGEND keinen Müll erzeugen** — Files NIE doppelt nach /curated/
4. **Flat-Search** im Source — kein Directory-Traversal
5. **Sensitive Topics werden NICHT inhaltlich gelesen** (trauma-dis-material default)
6. **setup ist idempotent** — re-triggern bei Crash filtert via Skip-Regel
7. **routine ist klein und schnell** — cap 50, Status-Report bei Backlog

## Was dieser Skill NICHT macht

- KEINE Topic-Subfolder im Drive
- KEIN /curated/_pending/ Folder
- KEIN yaml-State im Drive
- KEINE Folder-Anlage für neue Topics ohne explizites User-Approve via Inbox
- KEIN Trashen/Löschen/Renamen von Drive-Files (Tool-Limitation)
- KEIN Directory-Traversal im Source
- KEIN Auto-Repair bei Drift (askuser-First)
- KEINE Inhalts-Reads für sensitive Topics
- KEINE Server-Side-Sortierung im Drive (`search_files` hat kein `orderBy` — alle Sortierung client-side)

## Token-Budget

| Operation | Cost |
|---|---|
| setup, leer (DBs anlegen, 0 Source-Files) | ~10k |
| setup, 100 Files Source | ~150-300k |
| setup, 500 Files Source | ~750k-1.5M (mehrfache Trigger empfohlen) |
| routine, 0 neue Files | ~5-10k |
| routine, 50 Files | ~80-150k |
| review-inbox, 10 Einträge | ~5-10k |
| repair, 100 Files curated, ~5 Findings | ~30-50k |

## Wichtige Limitationen

- **Multi-Session Race**: zwei parallele Skill-Sessions können kollidieren (Notion-Lookup vs Notion-Create). Nur eine Session gleichzeitig triggern.
- **Sensitive-Detection nur via Title**: wenn Titel harmlos aber Inhalt sensitive — wird als non-sensitive verarbeitet. User kann nachträglich `Sensitive=__YES__` setzen.
- **Google Docs haben kein md5**: Duplikat-Heuristik nutzt Title+Size für Google-native Files.
- **Drive-MCP `search_files` hat kein orderBy**: ASC-Sortierung in routine passiert client-side nach komplettem paginated-Listing.
- **`/tmp/`-State ist nicht persistent**: bei Container-Restart muss User Setup-IDs erneut bestätigen. v0.5.0-Plan: `_meta`-Page in Notion als Single-Source-of-Truth.

## Files

| Pfad | Zweck |
|---|---|
| `SKILL.md` | Trigger + Workflow-Übersicht (4 Operations) |
| `references/workflow-phases.md` | setup / routine / review-inbox / repair im Detail |
| `references/notion-schema.md` | DB-Schemas + Setup-Sequenz |
| `references/duplicate-handling.md` | 5-stufige Duplikat-Erkennung |
| `references/resume-logic.md` | State aus Notion ziehen + Crash-Resume |
| `references/repair-consistency.md` | Drive vs Notion Diff |
| `references/slug-rules.md` | Slug-Algorithmus |
| `references/sensitive-handling.md` | Trauma-Topic-Sonderbehandlung |
| `references/classification-rules.md` | Title+Content-Match + Sprache |
| `references/topics-initial.md` | Topics-DB Initial-Befüllung |
| `scripts/slug.py` | CLI-Tool für Slug-Generation |
| `scripts/classify.py` | CLI-Tool für Klassifikation |
| `scripts/language_detect.py` | CLI-Tool für Sprach-Erkennung |
| `scripts/duplicate_check.py` | CLI-Tool für Duplikat-Heuristiken |
| `assets/topics-config.yaml` | 11 initiale Topics |
| `assets/ddl-statements.sql` | DDL für notion-create-database |

## Roadmap

- v0.4.1: Pre-Read-Sample-Check für Sensitive-Detection (lese erste 200 Tokens)
- v0.5.0: Setup-IDs in Notion `_meta`-Page (kein /tmp/-State mehr)
- v0.5.0: Per-File-Lookup für Duplicate-Check bei großer DB (>5000 Files)
- v0.6: Topics-DB als RELATION zu Files-DB (bidirektional)
- v0.7: LLM-Fallback-Klassifikation bei keinem Title+Content-Match
- v0.8: Time-Series-Analytics (Run-Logs in Notion-Page mit Charts)
