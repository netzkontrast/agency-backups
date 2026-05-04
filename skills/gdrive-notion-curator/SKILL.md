---
name: gdrive-notion-curator
description: >-
  MCP-driven Drive-zu-Notion Curator. Vier Operations: setup (komplett-Listing
  Source-Folder paginated, alle Files verarbeiten, DBs initial anlegen),
  routine (incremental, filter createdTime gt newest_in_last_run, cap 50
  ASC, Status-Report bei Backlog), review-inbox (askuser-driven, on-demand),
  repair (komplett-Listing /curated/ paginated, diff gegen Notion).
  Kopiert Drive-Files EINMAL nach /Claude/curated/ flach, klassifiziert via
  Title plus Content gegen Topics-DB, indexiert klassifizierte Files als
  Sub-Pages mit Auszug, schickt unklare Klassifikationen in Inbox-DB.
  Notion ist State-Source. Sensitive Topics werden NICHT inhaltlich gelesen.
  Trigger bei drive aufräumen, drive sortieren, drive curate, kuratiere
  meine docs, neue docs einsortieren, drive cleanup, repair drive notion,
  drive scan, drive routine, drive sweep, files in topic einsortieren auch
  ohne explizites skill-Wort. v0.4.0 nutzt Drive-MCP plus Notion-MCP.
---

# gdrive-notion-curator (v0.4.0)

MCP-only Skill. Drive ist passiver Bucket — Notion macht die Strukturarbeit.

## Architektur in einem Bild

```
DRIVE (passiver Bucket)              NOTION (Strukturebene)
───────                              ──────
/Claude/                             📁 Claude Drive Files
├── (Source-Folder)                     Eine Page pro Drive-File.
│   └── (User-Inbox)                    Drive-IDs, Sprache, Status,
└── curated/                             Topic-Relation, Page-Link.
    ├── kohaerenz-protokoll-x.md
    ├── trauma-dis-doc-y.md          📚 Claude Topics
    ├── english-notes-z.md              Eine Page pro Topic.
    └── ...                             Sub-Pages = File-Inhalte (Auszug).
        flach.
        einmal kopiert.              📥 Claude Topic Inbox
        slug-filename.                  Eine Page pro Vorschlag für
                                        neuen Topic. Awaits askuser.
```

## Operating-Prinzipien (kritisch)

1. **Drive ist write-once-additive.** copy + create_folder, nichts sonst. KEIN Trash, KEIN Move, KEIN Rename via MCP.
2. **DRINGEND keinen Müll erzeugen.** Files werden EINMAL nach /curated/ kopiert. Nie zweimal. Doppel-Check via Notion-DB-Lookup vor jedem Copy.
3. **Notion ist State-Source.** Skill-Start zieht aktuellen State aus Notion (kein lokaler State ausser den statischen Setup-IDs).
4. **Flat-Search im Source-Folder.** KEIN Directory-Traversal. Nur direkt im Source-Folder mit `parentId = '<id>'`.
5. **Sensitive Topics werden NICHT inhaltlich gelesen.** Nur Title-basierte Klassifikation, keine Sub-Page mit Inhalt.
6. **Setup ist idempotent.** Skip-Regel via `Original Drive ID` filtert schon-verarbeitete Files. User kann Setup re-triggern bei Crash.
7. **Routine ist klein und schnell.** Cap 50 Files. Wenn mehr da, Status-Report → User triggert nochmal.

## Quick Reference — Skill-Operations

| Operation | Trigger | Drive-Listing | File-Cap |
|---|---|---|---|
| `setup` | One-time bei Skill-Erst-Nutzung. DBs anlegen + initial-sweep. | Komplett, paginated, alle Files im Source | unbegrenzt |
| `routine` | Routine. Findet neue Files seit letztem Run. | Filter `createdTime > newest_in_last_run`, paginated | 50 (ASC by createdTime) |
| `review-inbox` | On-demand. Geht Topic-Inbox durch mit askuser. | — (nur Notion) | unbegrenzt (Inbox-DB-Größe) |
| `repair` | On-demand. Drift zwischen Drive `/curated/` und Notion. | Komplett /curated/, paginated | unbegrenzt |

### Wahl der Operation

- **Beim ersten Skill-Run im Workspace:** `setup`. Falls Setup mid-run abbricht: `setup` nochmal triggern — Skip-Regel filtert schon-verarbeitete Files, Skill macht weiter.
- **Daily/regulär:** `routine`. Bei Backlog >50 mehrfach triggern bis Status-Report sagt "0 Files übrig".
- **Wenn Inbox-Einträge anstehen:** `review-inbox`. Kann nach jeder routine getriggert werden, ist aber separat.
- **Bei Verdacht auf Drift** (manuelle Drive-Edits, Crash mit unklaren Folgen, oder routinemäßig 1x/Monat): `repair`.

## Workflow-Detail

Alle Operations spezifiziert in `references/workflow-phases.md`. Hier die Kurzform:

### setup

1. askuser nach Notion-Parent-Page-ID, Drive-Source-Folder-ID, Drive-Claude-Root-ID
2. `/Claude/curated/`-Folder anlegen (idempotent)
3. 3 Notion-DBs anlegen (Files, Topics, Inbox) + Views
4. Topics-DB initial befüllen aus `assets/topics-config.yaml` (11 Topics)
5. Setup-IDs in `/tmp/gdrive-curator-state.json` speichern
6. **Komplett-Listing** Source-Folder, paginated bis nextPageToken leer
7. Pro File: Skip-Checks → Slug → Copy → Files-DB-Entry → Sensitive-Check → Content-Read → Classify → Routing (siehe `workflow-phases.md` § "setup")
8. Run-Übersicht an User

→ Detail: `references/workflow-phases.md` § "setup"

### routine

1. State aus Notion: `last_run_id`, `newest_in_last_run`, Duplicate-Sets (siehe `references/resume-logic.md`)
2. Drive-Listing flat: `query: parentId='<source>' and trashed=false and createdTime > '<newest_in_last_run>'`
3. Paginated holen, **client-side ASC by createdTime** sortieren
4. **Cap 50** Files (ältester der neuen zuerst — FIFO bei Backlog)
5. Pro File: gleicher Verarbeitungs-Loop wie setup
6. **Status-Report:**
   - "X Files verarbeitet, Y unverändert (skip), Z Files NOCH ÜBRIG — bitte routine nochmal triggern" (wenn paginated-Total > Cap)
   - Sonst: "X Files verarbeitet, alle neuen Files seit letztem Run sind durch."

→ Detail: `references/workflow-phases.md` § "routine"

### review-inbox

1. Notion-Query Inbox-DB: alle Pages mit `Status=pending-review`
2. Pro Eintrag mit `ask_user_input_v0`:
   - Optionen: `Approve neuer Topic` / `Merge in <existing-slug>` / `Reject` / `Skip`
3. Bei Approve: Topics-DB neue Page + Topic-Select erweitern + Sample-Files re-indexieren
4. Bei Merge: Sample-Files in Existing-Topic einsortieren

→ Detail: `references/workflow-phases.md` § "review-inbox"

### repair

1. Drive-Listing `/curated/` flat, paginated bis komplett
2. Notion-Query Files-DB mit `Curated Drive ID` gesetzt, paginated
3. Diffs berechnen (orphan in Drive, ghost in Notion, optional source-gone, status-inconsistent)
4. Pro Diff: askuser mit Repair-Optionen, kein automatisches Reparieren

→ Detail: `references/repair-consistency.md`

## Reference-Files

| File | Wann lesen |
|---|---|
| `references/workflow-phases.md` | Vor jeder Operation die zugehörige Sektion |
| `references/notion-schema.md` | Bei Setup und bei Schema-Migrationen |
| `references/duplicate-handling.md` | In setup und routine vor jedem Copy |
| `references/resume-logic.md` | Bei jedem Skill-Start (setup, routine, repair) |
| `references/repair-consistency.md` | Bei `repair` |
| `references/slug-rules.md` | Vor jedem Filename-Slug |
| `references/sensitive-handling.md` | Bei jedem File mit potentiell sensitiven Keywords |
| `references/classification-rules.md` | In setup und routine für Title+Content-Match |
| `references/topics-initial.md` | Bei Setup zur Topics-DB-Befüllung |

## Scripts

| Script | CLI-Nutzung |
|---|---|
| `scripts/slug.py` | `python3 scripts/slug.py "<title>"` → slug-filename |
| `scripts/classify.py` | `python3 scripts/classify.py --title "<t>" --content "<c>" --topics-yaml topics.yaml` → JSON |
| `scripts/language_detect.py` | `python3 scripts/language_detect.py "<text>"` → de/en/mixed/unknown |
| `scripts/duplicate_check.py` | `python3 scripts/duplicate_check.py "<title>" --md5 "<md5>" --size <bytes>` → JSON |

## Assets

| Asset | Inhalt |
|---|---|
| `assets/ddl-statements.sql` | SQL DDL für die 3 Notion-DBs (Files, Topics, Inbox) |
| `assets/topics-config.yaml` | Initial Topics-Set (11 Topics inkl. sensitive-Flag) |

## Token-Budget (geschätzt)

| Operation | Cost |
|---|---|
| setup, leer | ~10k (DBs anlegen, keine Files) |
| setup, 100 Files Source | ~150-300k (mit Content-Reads + Notion-Writes) |
| setup, 500 Files Source | ~750k-1.5M — User sollte vorher mehrfache Trigger einplanen |
| routine, 0 neue Files | ~5-10k (nur State-Holen + leeres Listing) |
| routine, 50 Files | ~80-150k |
| review-inbox, 10 Einträge | ~5-10k (askuser-driven) |
| repair, 100 Files curated | ~30-60k abhängig von Findings |

## Was dieser Skill NICHT macht

- KEINE Topic-Subfolder im Drive
- KEIN /curated/_pending/ Folder
- KEIN yaml-State im Drive
- KEINE Folder-Anlage für neue Topics ohne explizites User-Approve via Inbox
- KEIN Trashen/Löschen/Renamen von Drive-Files (Tool-Limitation)
- KEIN Directory-Traversal im Source
- KEIN Auto-Repair bei Drift (askuser-First)
- KEINE Inhalts-Reads für sensitive Topics
- KEINE Sortierung server-side im Drive (`search_files` hat kein `orderBy` — alle Sortierung client-side nach Listing)
