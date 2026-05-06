#!/usr/bin/env python3
"""term.py — per-term editor for the dramatica narrative ontology.

Mechanises the create / edit / move / deprecate workflows that previously
required hand-editing markdown + YAML + ontology.json. Delegates frontmatter-
field edits to ``tools/fm/edit.py`` (which is the canonical fm editor); this
module only owns the *term-spanning* mutations:

  - ``create``      mint a ``## <Label>`` heading + nav-ontology YAML block in
                    a vocab reference + a matching entry in ontology.json.
  - ``edit``        alias / scenario manipulation; ``--refresh <id>`` re-
                    projects the per-term YAML into ontology.json (idempotent
                    no-op when block + ontology already agree).
  - ``move``        physically move a heading + body + YAML block between
                    files and rewrite ``term_file``.
  - ``deprecate``   either alias-fold the term onto a successor (preferred
                    lifecycle) or surface the schema-bump-required friction.

Importable side-effect free: every subcommand's logic is exposed as a Python
function returning an exit code, and ``main()`` dispatches an argparse
namespace. The helpers reuse:

  - ``tools.fm._core``                 — frontmatter parser + heading walker.
  - ``tools.dramatica-nav.lib.ontology``  — ontology load + index.
  - ``tools.dramatica-nav.lib.frontmatter`` — per-term YAML extractor + slugify.

Exit codes:
    0  success
    2  usage / I/O error
    3  not found (id missing for edit/move/deprecate; target file missing)
    4  refusal (would overwrite without --force; duplicate id; no clean break)
    5  schema-bump required without alias-on fallback path
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

# --- import bootstrap --------------------------------------------------------
_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parents[1]

# tools/dramatica-nav on path so `from lib import ontology` works.
sys.path.insert(0, str(_HERE))
# tools/ on path so we can `import fm._core` (fm is a package).
sys.path.insert(0, str(_REPO_ROOT / "tools"))

from fm import _core as _fm_core  # noqa: E402
from lib import frontmatter as _frontmatter_lib  # noqa: E402
from lib import ontology as _ontology_lib  # noqa: E402
from lib import LookupNotFoundError, OntologyError  # noqa: E402


# --- constants ---------------------------------------------------------------

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_NOT_FOUND = 3
EXIT_REFUSED = 4
EXIT_SCHEMA_BUMP = 5

VOCAB_BASE_REL = Path("skills/dramatica-vocabulary/references")

# Default landing file per kind (only used when --file is not supplied).
KIND_DEFAULT_FILE: dict[str, str] = {
    "element": "elements.md",
    "variation": "variations.md",
    "type": "types.md",
    "class": "classes.md",
    "archetype": "archetypes.md",
    "character-dynamic": "character-dynamics.md",
    "plot-dynamic": "plot-dynamics.md",
    "throughline": "main-vs-impact-character.md",
    "concept": "dramatica-fundamentals.md",
    "storypoint": "storyform-mechanics.md",
    "dynamic-pair": "dynamic-pairs-index.md",
    "quad": "element-quads.md",
    "signpost-slot": "storyform-mechanics.md",
}

YAML_BLOCK_RE = re.compile(
    r"<!-- nav-ontology[^>]*-->\n```yaml\n(.+?)\n```",
    re.DOTALL,
)
NAV_MARKER = "<!-- nav-ontology (auto-managed; see maintenance/schemas/narrative-ontology/) -->"


# --- low-level YAML emit -----------------------------------------------------

def _emit_block_yaml(fields: dict) -> str:
    """Emit a deterministic YAML body matching ontology-build.py's expectations.

    Order: id, kind, canonical_label, provenance, then the rest sorted.
    Lists rendered as block lists; scalars as ``key: value``.
    """
    head_keys = ["id", "kind", "canonical_label", "provenance"]
    lines: list[str] = []
    for k in head_keys:
        if k in fields:
            lines.append(f"{k}: {fields[k]}")
    for k in sorted(fields.keys()):
        if k in head_keys:
            continue
        v = fields[k]
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"- {item}")
        elif isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        else:
            lines.append(f"{k}: {v}")
    return "\n".join(lines)


def _wrap_block(yaml_body: str) -> str:
    return f"{NAV_MARKER}\n```yaml\n{yaml_body}\n```\n"


# --- ontology helpers --------------------------------------------------------

def _load_ontology(ontology_path: Path) -> dict:
    return json.loads(ontology_path.read_text(encoding="utf-8"))


def _save_ontology(doc: dict, ontology_path: Path) -> None:
    text = json.dumps(doc, indent=2, ensure_ascii=False)
    ontology_path.write_text(text, encoding="utf-8")


def _entry_index(doc: dict) -> dict[str, int]:
    return {e["id"]: i for i, e in enumerate(doc.get("entries", [])) if "id" in e}


def _sort_entries(entries: list[dict]) -> list[dict]:
    return sorted(entries, key=lambda e: (e.get("kind", ""), e.get("id", "")))


# --- markdown surgery --------------------------------------------------------

def _split_sections(text: str) -> list[tuple[str, str]]:
    """Split ``text`` into [(heading_or_empty, section_text), ...] tuples.

    The first element is always the pre-heading prologue; subsequent elements
    each begin with a ``## `` heading line. ``section_text`` includes the
    heading line itself plus everything up to (but not including) the next
    ``## `` heading. Headings inside fenced code blocks are ignored.
    """
    lines = text.splitlines(keepends=True)
    out: list[tuple[str, str]] = []
    in_fence = False
    fence_marker: Optional[str] = None
    starts: list[int] = []
    for i, line in enumerate(lines):
        s = line.lstrip()
        if s.startswith("```") or s.startswith("~~~"):
            marker = s[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif fence_marker == marker:
                in_fence = False
                fence_marker = None
            continue
        if in_fence:
            continue
        m = re.match(r"^## (.+?)\s*$", line.rstrip("\n"))
        if m:
            starts.append(i)
    starts.append(len(lines))
    if not starts or starts[0] != 0:
        prologue = "".join(lines[: starts[0] if starts else len(lines)])
        out.append(("", prologue))
    for k in range(len(starts) - 1):
        chunk = "".join(lines[starts[k]: starts[k + 1]])
        m = re.match(r"^## (.+?)\s*$", chunk.splitlines()[0])
        head = m.group(1) if m else ""
        out.append((head, chunk))
    return out


def _find_section(text: str, heading: str) -> Optional[tuple[int, int, str]]:
    """Locate a ``## heading`` section. Returns (start_byte, end_byte, raw)."""
    norm = _fm_core.normalise_heading(heading)
    cursor = 0
    in_fence = False
    fence_marker: Optional[str] = None
    line_starts: list[int] = []
    for i, ch in enumerate(text):
        if i == 0 or text[i - 1] == "\n":
            line_starts.append(i)
    line_starts.append(len(text))
    sections: list[tuple[int, str]] = []
    for k in range(len(line_starts) - 1):
        s = line_starts[k]
        e = line_starts[k + 1]
        line = text[s:e]
        ls = line.lstrip()
        if ls.startswith("```") or ls.startswith("~~~"):
            marker = ls[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif fence_marker == marker:
                in_fence = False
                fence_marker = None
            continue
        if in_fence:
            continue
        m = re.match(r"^## (.+?)\s*$", line.rstrip("\n"))
        if m:
            sections.append((s, m.group(1)))
    sections.append((len(text), ""))
    for idx in range(len(sections) - 1):
        s, head = sections[idx]
        if _fm_core.normalise_heading(head) == norm:
            e = sections[idx + 1][0]
            return s, e, text[s:e]
    return None


def _read_term_block_from_section(section_text: str) -> Optional[dict]:
    m = YAML_BLOCK_RE.search(section_text)
    if not m:
        return None
    import yaml  # local import — yaml is already pulled in by ontology-build
    data = yaml.safe_load(m.group(1))
    return data if isinstance(data, dict) else None


# --- repo + run helpers ------------------------------------------------------

def _ontology_path(repo_root: Path) -> Path:
    return repo_root / "maintenance/schemas/narrative-ontology/ontology.json"


def _run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return res.returncode, res.stdout, res.stderr


def _post_mutation_gate(repo_root: Path) -> tuple[int, list[str]]:
    """Re-run ontology-build --check then validate.py. Surface diagnostics.

    Returns (exit_code, messages). ``exit_code`` is 0 when both pass; the
    caller uses this to advise the user (does not abort, since the mutation
    has already been applied to disk).
    """
    msgs: list[str] = []
    rc1, out1, err1 = _run(
        ["python3", "tools/dramatica-nav/ontology-build.py", "--check-only"],
        cwd=repo_root,
    )
    if rc1 != 0:
        msgs.append(f"ontology-build --check-only: rc={rc1}")
        if err1.strip():
            msgs.append(err1.strip())
    rc2, out2, err2 = _run(
        ["python3", "tools/dramatica-nav/validate.py"],
        cwd=repo_root,
    )
    if rc2 != 0:
        msgs.append(f"validate.py: rc={rc2}")
        if err2.strip():
            msgs.append(err2.strip())
    return (rc1 or rc2), msgs


def _maybe_commit(repo_root: Path, msg: Optional[str], paths: list[Path]) -> None:
    if not msg:
        return
    rels = [str(p.relative_to(repo_root)) for p in paths if p.exists()]
    if not rels:
        return
    _run(["git", "add", *rels], cwd=repo_root)
    _run(["git", "commit", "-m", msg], cwd=repo_root)


# --- subcommand: create ------------------------------------------------------

def cmd_create(
    *,
    oid: str,
    kind: str,
    label: str,
    file: Optional[str],
    scenarios: Optional[list[str]],
    repo_root: Path,
    force: bool = False,
    commit: Optional[str] = None,
    ontology_path: Optional[Path] = None,
) -> int:
    """Create a new term: heading + nav-ontology YAML + ontology entry."""
    onto_path = ontology_path or _ontology_path(repo_root)

    if not onto_path.exists():
        print(f"term.py create: ontology not found at {onto_path}", file=sys.stderr)
        return EXIT_USAGE

    doc = _load_ontology(onto_path)
    idx = _entry_index(doc)
    if oid in idx and not force:
        print(
            f"term.py create: id {oid!r} already exists; pass --force to overwrite",
            file=sys.stderr,
        )
        return EXIT_REFUSED

    # Resolve target file.
    if file:
        target = Path(file)
        if not target.is_absolute():
            target = (repo_root / target).resolve()
            # If the user passed a bare filename, also try the default vocab dir.
            if not target.exists():
                alt = repo_root / VOCAB_BASE_REL / Path(file).name
                if alt.exists():
                    target = alt.resolve()
    else:
        default = KIND_DEFAULT_FILE.get(kind)
        if not default:
            print(
                f"term.py create: no default file for kind={kind!r}; pass --file",
                file=sys.stderr,
            )
            return EXIT_USAGE
        target = (repo_root / VOCAB_BASE_REL / default).resolve()

    if not target.exists():
        print(f"term.py create: target file not found: {target}", file=sys.stderr)
        return EXIT_NOT_FOUND

    # Refuse if heading already exists.
    text = target.read_text(encoding="utf-8")
    existing = _find_section(text, label)
    if existing and not force:
        print(
            f"term.py create: heading '## {label}' already in {target.name}; "
            "pass --force to overwrite",
            file=sys.stderr,
        )
        return EXIT_REFUSED

    # Build the YAML block.
    fields: dict = {
        "id": oid,
        "kind": kind,
        "canonical_label": label,
        "provenance": "extension-derived",
    }
    if scenarios:
        fields["scenarios"] = list(scenarios)

    yaml_body = _emit_block_yaml(fields)
    block = _wrap_block(yaml_body)

    new_section = (
        f"## {label}\n"
        f"{block}\n"
    )
    # Append at end-of-file. Ensure there is a trailing newline before the
    # heading (and after, if missing).
    if existing and force:
        # Replace the existing section in place.
        s, e, _raw = existing
        new_text = text[:s] + new_section + text[e:]
    else:
        sep = "" if text.endswith("\n") else "\n"
        new_text = text + sep + new_section

    target.write_text(new_text, encoding="utf-8")

    # Project into ontology.json. Compute a repo-relative term_file when the
    # target sits inside the repo; fall back to the bare filename otherwise
    # (callers using /tmp/ for smoke tests get a useful but non-canonical
    # pointer rather than a crash).
    slug = _frontmatter_lib.slugify(label)
    try:
        rel_md = target.resolve().relative_to(repo_root.resolve())
        term_file = f"{rel_md.as_posix()}#{slug}"
    except ValueError:
        term_file = f"{target.name}#{slug}"
    entry = dict(fields)
    entry["term_file"] = term_file

    entries = list(doc.get("entries", []))
    if oid in idx:
        entries[idx[oid]] = entry
    else:
        entries.append(entry)
    doc["entries"] = _sort_entries(entries)
    _save_ontology(doc, onto_path)

    # Post-mutation gate.
    rc, msgs = _post_mutation_gate(repo_root)
    for m in msgs:
        print(f"term.py create: {m}", file=sys.stderr)

    _maybe_commit(repo_root, commit, [target, onto_path])
    return EXIT_OK


# --- subcommand: edit --------------------------------------------------------

def _find_term_file(repo_root: Path, oid: str) -> Optional[tuple[Path, str]]:
    """Locate the source file + heading for an ontology id by scanning blocks.

    Returns (path, heading) or None.
    """
    base = repo_root / VOCAB_BASE_REL
    for path in sorted(base.glob("*.md")):
        if path.name in _frontmatter_lib.VOCAB_SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        # Walk sections; for each section with a nav-ontology block whose id
        # matches, return.
        for head, section in _split_sections(text):
            if not head:
                continue
            data = _read_term_block_from_section(section)
            if data and data.get("id") == oid:
                return path, head
    return None


def _refresh_ontology_from_blocks(repo_root: Path, oid: str) -> int:
    """Re-project a single block into ontology.json idempotently.

    Reads the per-term YAML for ``oid`` from the source file and overlays it
    onto the matching ontology entry, preserving ``term_file`` if unset.
    """
    onto_path = _ontology_path(repo_root)
    doc = _load_ontology(onto_path)
    idx = _entry_index(doc)
    if oid not in idx:
        print(f"term.py edit: id {oid!r} not in ontology", file=sys.stderr)
        return EXIT_NOT_FOUND
    located = _find_term_file(repo_root, oid)
    if located is None:
        print(f"term.py edit: no source heading for {oid!r}", file=sys.stderr)
        return EXIT_NOT_FOUND
    path, heading = located
    text = path.read_text(encoding="utf-8")
    section = _find_section(text, heading)
    if section is None:
        print(
            f"term.py edit: heading {heading!r} vanished in {path.name}",
            file=sys.stderr,
        )
        return EXIT_NOT_FOUND
    data = _read_term_block_from_section(section[2])
    if data is None:
        print(f"term.py edit: no nav-ontology block under {heading!r}", file=sys.stderr)
        return EXIT_NOT_FOUND

    slug = _frontmatter_lib.slugify(heading)
    try:
        rel_md = path.resolve().relative_to(repo_root.resolve())
        target_term_file = f"{rel_md.as_posix()}#{slug}"
    except ValueError:
        target_term_file = f"{path.name}#{slug}"

    entries = list(doc["entries"])
    existing = dict(entries[idx[oid]])
    seeded = dict(existing)
    seeded.update(data)
    if "term_file" not in seeded:
        seeded["term_file"] = existing.get("term_file") or target_term_file
    entries[idx[oid]] = seeded
    doc["entries"] = _sort_entries(entries)
    _save_ontology(doc, onto_path)
    return EXIT_OK


def cmd_edit(
    *,
    oid: str,
    add_alias: list[str],
    remove_alias: list[str],
    set_scenario: Optional[list[str]],
    refresh: bool,
    repo_root: Path,
    commit: Optional[str] = None,
) -> int:
    """alias / scenario manipulation. ``--refresh`` re-syncs ontology only."""
    located = _find_term_file(repo_root, oid)
    if located is None:
        print(f"term.py edit: id {oid!r} not found in any source file", file=sys.stderr)
        return EXIT_NOT_FOUND
    path, heading = located

    # Read the per-term block, mutate alias/scenario fields in-place, write back.
    text = path.read_text(encoding="utf-8")
    sec = _find_section(text, heading)
    if sec is None:
        print(f"term.py edit: heading vanished in {path}", file=sys.stderr)
        return EXIT_NOT_FOUND
    s, e, raw = sec
    block_match = YAML_BLOCK_RE.search(raw)
    if block_match is None:
        print(f"term.py edit: no nav-ontology block under {heading!r}", file=sys.stderr)
        return EXIT_NOT_FOUND

    import yaml as _yaml
    fields: dict = _yaml.safe_load(block_match.group(1)) or {}

    # Apply alias mutations.
    for spec in add_alias:
        if ":" not in spec:
            print(
                f"term.py edit: --add-alias expects locale:value (got {spec!r})",
                file=sys.stderr,
            )
            return EXIT_USAGE
        loc, _, val = spec.partition(":")
        key = f"aliases_{loc.strip()}"
        bucket = list(fields.get(key, []))
        if val not in bucket:
            bucket.append(val)
        fields[key] = bucket

    for spec in remove_alias:
        if ":" not in spec:
            print(
                f"term.py edit: --remove-alias expects locale:value (got {spec!r})",
                file=sys.stderr,
            )
            return EXIT_USAGE
        loc, _, val = spec.partition(":")
        key = f"aliases_{loc.strip()}"
        bucket = [a for a in fields.get(key, []) if a != val]
        if bucket:
            fields[key] = bucket
        elif key in fields:
            del fields[key]

    if set_scenario is not None:
        if set_scenario:
            fields["scenarios"] = list(set_scenario)
        elif "scenarios" in fields:
            del fields["scenarios"]

    # Re-emit block.
    new_yaml = _emit_block_yaml(fields)
    new_block = _wrap_block(new_yaml).rstrip("\n")
    new_section = raw[: block_match.start()] + new_block + raw[block_match.end():]
    new_text = text[:s] + new_section + text[e:]
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")

    # Re-sync ontology.
    rc = _refresh_ontology_from_blocks(repo_root, oid)
    if rc != EXIT_OK and not refresh:
        return rc

    rc_gate, msgs = _post_mutation_gate(repo_root)
    for m in msgs:
        print(f"term.py edit: {m}", file=sys.stderr)

    _maybe_commit(repo_root, commit, [path, _ontology_path(repo_root)])
    return EXIT_OK


# --- subcommand: move --------------------------------------------------------

def cmd_move(
    *,
    oid: str,
    to_file: str,
    rename_anchor: Optional[str],
    repo_root: Path,
    force: bool = False,
    commit: Optional[str] = None,
) -> int:
    """Move heading + body + YAML between vocab files; rewrite term_file."""
    located = _find_term_file(repo_root, oid)
    if located is None:
        print(f"term.py move: id {oid!r} not found", file=sys.stderr)
        return EXIT_NOT_FOUND
    src_path, heading = located

    target = Path(to_file)
    if not target.is_absolute():
        target = (repo_root / target).resolve()
        if not target.exists():
            alt = repo_root / VOCAB_BASE_REL / Path(to_file).name
            if alt.exists():
                target = alt.resolve()
    if not target.exists():
        print(f"term.py move: target file not found: {target}", file=sys.stderr)
        return EXIT_NOT_FOUND
    if target.resolve() == src_path.resolve():
        # Same-file rename-anchor only.
        if not rename_anchor:
            print("term.py move: target file equals source file (no-op)", file=sys.stderr)
            return EXIT_USAGE

    src_text = src_path.read_text(encoding="utf-8")
    sec = _find_section(src_text, heading)
    if sec is None:
        print(f"term.py move: heading vanished in {src_path}", file=sys.stderr)
        return EXIT_NOT_FOUND
    s, e, raw = sec

    # Determine new heading (rename) and slug.
    new_heading = heading
    if rename_anchor:
        # Re-derive a label from the slug-style anchor (Title Case).
        new_heading = " ".join(p.capitalize() for p in rename_anchor.split("-"))

    # Patch block id/canonical_label only if we renamed.
    block_match = YAML_BLOCK_RE.search(raw)
    if block_match is None:
        print(f"term.py move: no nav-ontology block under {heading!r}", file=sys.stderr)
        return EXIT_NOT_FOUND

    if rename_anchor:
        import yaml as _yaml
        fields = _yaml.safe_load(block_match.group(1)) or {}
        fields["canonical_label"] = new_heading
        new_yaml = _emit_block_yaml(fields)
        new_block = _wrap_block(new_yaml).rstrip("\n")
        # Replace the heading line + block in the moved section text.
        # raw begins with `## <heading>\n`; rewrite its first line.
        first_nl = raw.find("\n")
        replaced_first = f"## {new_heading}" + raw[first_nl:]
        moved = (
            replaced_first[: block_match.start()]
            + new_block
            + replaced_first[block_match.end():]
        )
    else:
        moved = raw

    # Verify clean break in target: target must end with newline OR contain at
    # least one ## heading already. If neither, refuse with hint.
    tgt_text = target.read_text(encoding="utf-8")
    has_h2 = bool(re.search(r"^## ", tgt_text, flags=re.MULTILINE))
    ends_clean = tgt_text == "" or tgt_text.endswith("\n")
    if not (has_h2 or ends_clean) and not force:
        print(
            "term.py move: target lacks a clean section break; "
            "re-run with --force or --position end-of-file (not yet implemented)",
            file=sys.stderr,
        )
        return EXIT_REFUSED

    # Refuse if heading already in target (collision).
    collision = _find_section(tgt_text, new_heading)
    if collision and not force:
        print(
            f"term.py move: heading '## {new_heading}' already in {target.name}; "
            "pass --force to overwrite",
            file=sys.stderr,
        )
        return EXIT_REFUSED

    # Write.
    if src_path.resolve() != target.resolve():
        # Excise source.
        src_new = src_text[:s] + src_text[e:]
        src_path.write_text(src_new, encoding="utf-8")
        # Append to target.
        sep = "" if tgt_text.endswith("\n") or tgt_text == "" else "\n"
        target.write_text(tgt_text + sep + moved, encoding="utf-8")
    else:
        # Same-file rewrite (rename-anchor branch only).
        new_text = src_text[:s] + moved + src_text[e:]
        src_path.write_text(new_text, encoding="utf-8")

    # Update ontology term_file.
    onto_path = _ontology_path(repo_root)
    doc = _load_ontology(onto_path)
    idx = _entry_index(doc)
    if oid in idx:
        entry = dict(doc["entries"][idx[oid]])
        slug = _frontmatter_lib.slugify(new_heading)
        try:
            rel = target.resolve().relative_to(repo_root.resolve()).as_posix()
            entry["term_file"] = f"{rel}#{slug}"
        except ValueError:
            entry["term_file"] = f"{target.name}#{slug}"
        if rename_anchor:
            entry["canonical_label"] = new_heading
        entries = list(doc["entries"])
        entries[idx[oid]] = entry
        doc["entries"] = _sort_entries(entries)
        _save_ontology(doc, onto_path)

    rc, msgs = _post_mutation_gate(repo_root)
    for m in msgs:
        print(f"term.py move: {m}", file=sys.stderr)

    _maybe_commit(repo_root, commit, [src_path, target, onto_path])
    return EXIT_OK


# --- subcommand: deprecate ---------------------------------------------------

def cmd_deprecate(
    *,
    oid: str,
    reason: str,
    alias_on: Optional[str],
    repo_root: Path,
    force: bool = False,
    commit: Optional[str] = None,
) -> int:
    """Deprecate a term. Two lifecycles per ST-5 brief."""
    located = _find_term_file(repo_root, oid)
    if located is None:
        print(f"term.py deprecate: id {oid!r} not found", file=sys.stderr)
        return EXIT_NOT_FOUND
    src_path, heading = located

    if alias_on is None:
        # Schema-bump-required path.
        agency_adr = shutil.which("agency-adr")
        if agency_adr:
            # Best-effort ADR file; deliberately non-blocking.
            _run(
                [
                    agency_adr,
                    "draft",
                    "--title",
                    f"term-level deprecation lifecycle (triggered by {oid})",
                    "--body",
                    f"reason: {reason}",
                ],
                cwd=repo_root,
            )
        else:
            print(
                "# TODO(after-028): agency-adr CLI not on PATH; "
                "schema bump for term-level `status: deprecated` not filed.",
                file=sys.stderr,
            )
        # Fall back: if no successor, refuse with friction message.
        print(
            f"term.py deprecate: schema bump required for {oid!r} without --alias-on; "
            "no successor identifiable. Re-run with --alias-on <successor-id>.",
            file=sys.stderr,
        )
        return EXIT_SCHEMA_BUMP

    # alias-on path: delete heading from source, fold label onto successor.
    onto_path = _ontology_path(repo_root)
    doc = _load_ontology(onto_path)
    idx = _entry_index(doc)
    if oid not in idx:
        print(f"term.py deprecate: id {oid!r} not in ontology", file=sys.stderr)
        return EXIT_NOT_FOUND
    if alias_on not in idx:
        print(
            f"term.py deprecate: successor {alias_on!r} not in ontology",
            file=sys.stderr,
        )
        return EXIT_NOT_FOUND

    src_entry = doc["entries"][idx[oid]]
    label = src_entry.get("canonical_label", heading)

    # Delete heading section from source file.
    text = src_path.read_text(encoding="utf-8")
    sec = _find_section(text, heading)
    if sec is None:
        print(f"term.py deprecate: heading vanished in {src_path}", file=sys.stderr)
        return EXIT_NOT_FOUND
    s, e, _ = sec
    src_path.write_text(text[:s] + text[e:], encoding="utf-8")

    # Update successor ontology entry: append deprecated_aliases_en.
    successor = dict(doc["entries"][idx[alias_on]])
    bucket = list(successor.get("deprecated_aliases_en", []))
    if label not in bucket:
        bucket.append(label)
    successor["deprecated_aliases_en"] = bucket
    entries = list(doc["entries"])
    entries[idx[alias_on]] = successor

    # Update successor's per-term YAML block likewise so projection stays clean.
    succ_loc = _find_term_file(repo_root, alias_on)
    if succ_loc is not None:
        spath, sheading = succ_loc
        stext = spath.read_text(encoding="utf-8")
        ssec = _find_section(stext, sheading)
        if ssec is not None:
            ss, se, sraw = ssec
            block_match = YAML_BLOCK_RE.search(sraw)
            if block_match is not None:
                import yaml as _yaml
                sf = _yaml.safe_load(block_match.group(1)) or {}
                sb = list(sf.get("deprecated_aliases_en", []))
                if label not in sb:
                    sb.append(label)
                sf["deprecated_aliases_en"] = sb
                new_yaml = _emit_block_yaml(sf)
                new_block = _wrap_block(new_yaml).rstrip("\n")
                new_section = (
                    sraw[: block_match.start()] + new_block + sraw[block_match.end():]
                )
                spath.write_text(stext[:ss] + new_section + stext[se:], encoding="utf-8")

    # Drop the deprecated entry.
    entries = [e for e in entries if e.get("id") != oid]
    doc["entries"] = _sort_entries(entries)
    _save_ontology(doc, onto_path)

    rc, msgs = _post_mutation_gate(repo_root)
    for m in msgs:
        print(f"term.py deprecate: {m}", file=sys.stderr)

    paths = [src_path, onto_path]
    if succ_loc is not None:
        paths.append(succ_loc[0])
    _maybe_commit(repo_root, commit, paths)
    return EXIT_OK


# --- argparse + main ---------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="term.py",
        description=(
            "Per-term editor for the Dramatica narrative ontology. "
            "Coordinates markdown heading + nav-ontology YAML + ontology.json."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (default: auto-detect from this script's location).",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    pc = sub.add_parser("create", help="Mint a new term entry.")
    pc.add_argument("--id", dest="oid", required=True)
    pc.add_argument("--kind", required=True)
    pc.add_argument("--label", required=True)
    pc.add_argument("--file", default=None)
    pc.add_argument("--scenarios", default=None,
                    help="Comma-separated scenario ids.")
    pc.add_argument("--force", action="store_true")
    pc.add_argument("--commit", default=None)

    pe = sub.add_parser("edit", help="Alias/scenario manipulation; --refresh re-syncs ontology.")
    pe.add_argument("--id", dest="oid", required=True)
    pe.add_argument("--add-alias", action="append", default=[],
                    help="Locale:value (repeatable).")
    pe.add_argument("--remove-alias", action="append", default=[],
                    help="Locale:value (repeatable).")
    pe.add_argument("--set-scenario", default=None,
                    help="Comma-separated scenario ids (replaces existing list).")
    pe.add_argument("--refresh", action="store_true",
                    help="Re-project the per-term block into ontology.json (idempotent).")
    pe.add_argument("--commit", default=None)

    pm = sub.add_parser("move", help="Move a term between source files.")
    pm.add_argument("--id", dest="oid", required=True)
    pm.add_argument("--to-file", required=True)
    pm.add_argument("--rename-anchor", default=None)
    pm.add_argument("--force", action="store_true")
    pm.add_argument("--commit", default=None)

    pd = sub.add_parser("deprecate", help="Deprecate a term (alias-on preferred).")
    pd.add_argument("--id", dest="oid", required=True)
    pd.add_argument("--reason", required=True)
    pd.add_argument("--alias-on", default=None)
    pd.add_argument("--force", action="store_true")
    pd.add_argument("--commit", default=None)

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    repo_root = args.repo_root or _REPO_ROOT
    repo_root = Path(repo_root).resolve()

    if args.cmd == "create":
        scenarios = (
            [s.strip() for s in args.scenarios.split(",") if s.strip()]
            if args.scenarios
            else None
        )
        return cmd_create(
            oid=args.oid,
            kind=args.kind,
            label=args.label,
            file=args.file,
            scenarios=scenarios,
            repo_root=repo_root,
            force=args.force,
            commit=args.commit,
        )
    if args.cmd == "edit":
        set_scenario = (
            [s.strip() for s in args.set_scenario.split(",") if s.strip()]
            if args.set_scenario is not None
            else None
        )
        return cmd_edit(
            oid=args.oid,
            add_alias=list(args.add_alias),
            remove_alias=list(args.remove_alias),
            set_scenario=set_scenario,
            refresh=args.refresh,
            repo_root=repo_root,
            commit=args.commit,
        )
    if args.cmd == "move":
        return cmd_move(
            oid=args.oid,
            to_file=args.to_file,
            rename_anchor=args.rename_anchor,
            repo_root=repo_root,
            force=args.force,
            commit=args.commit,
        )
    if args.cmd == "deprecate":
        return cmd_deprecate(
            oid=args.oid,
            reason=args.reason,
            alias_on=args.alias_on,
            repo_root=repo_root,
            force=args.force,
            commit=args.commit,
        )
    parser.error(f"unknown subcommand {args.cmd!r}")
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
