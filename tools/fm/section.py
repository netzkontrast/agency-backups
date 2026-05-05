#!/usr/bin/env python3
"""fm-section — single-section body editor (SPEC §13).

Companion to fm-edit (which mutates frontmatter). Every invocation
mutates exactly one section; bytes outside the addressed
`## heading-through-next-## -or-EOF` span are preserved byte-for-byte,
and the YAML frontmatter is preserved through its closing fence.

Operations (per SPEC §13.1):
    --replace <name> --from-stdin
    --append-to <name> --text <str>
    --append-list-item <name> <item>
    --check-task <name> <item-substring>
    --insert-after <name> --new-heading <h> --from-stdin
    --insert-before <name> --new-heading <h> --from-stdin
    --delete <name>
    --rename <old> <new>

Addressing (SPEC §13.3):
    default      first match
    --nth N      1-indexed
    --anchor ID  match by `<!-- anchor: ID -->` comment above the heading

Exit codes:
    0  success
    2  usage error
    3  file not found
    4  schema/type error (mutation would violate §12 body_schema)
    5  ambiguous address (multiple matches without --nth/--anchor)
    6  tier guard refusal (T3 mutation rejected — file a Task)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _core  # type: ignore
else:
    from . import _core  # type: ignore

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_NOT_FOUND = 3
EXIT_TYPE_ERROR = 4
EXIT_AMBIGUOUS = 5
EXIT_TIER = 6


def _err(msg: str, code: int) -> int:
    print(msg, file=sys.stderr)
    return code


def _split(text: str) -> tuple[str, str]:
    """Return (frontmatter_with_fences_or_empty, body_text). Body starts at
    the first byte after the closing `---\\n` (or the file start if no FM).
    """
    m = _core.FRONTMATTER_RE.match(text)
    if not m:
        return "", text
    end = m.end()
    return text[:end], text[end:]


def _select(spans: list[_core.SectionSpan], nth: int | None, anchor: str | None) -> _core.SectionSpan | int:
    if anchor is not None:
        matches = [s for s in spans if s.anchor_id == anchor]
        if not matches:
            return EXIT_NOT_FOUND
        if len(matches) > 1:
            return EXIT_AMBIGUOUS
        return matches[0]
    if not spans:
        return EXIT_NOT_FOUND
    if len(spans) == 1:
        return spans[0]
    if nth is None:
        return EXIT_AMBIGUOUS
    if nth < 1 or nth > len(spans):
        return EXIT_NOT_FOUND
    return spans[nth - 1]


def _ontology() -> dict:
    return _core.load_ontology()


def _classify(path: Path, repo_root: Path, ont: dict) -> str | None:
    cls = _core.classify_path(path, repo_root, ont)
    if cls.expected_type is None:
        return None
    fm_text = path.read_text(encoding="utf-8")
    fm = _core.read_fm(path, strict=False)
    declared = _core.str_val(fm, "type")
    permitted = {cls.expected_type, *cls.alt_types}
    if declared and declared in permitted:
        return declared
    return cls.expected_type


def _body_schema_for(type_name: str | None, heading_norm: str, ont: dict) -> dict | None:
    if not type_name:
        return None
    body_schema = ont["types"].get(type_name, {}).get("body_schema", {})
    for raw_key, schema in body_schema.items():
        if raw_key.startswith("_"):
            continue
        if _core.normalise_heading(raw_key) == heading_norm:
            return schema
    return None


def _verify_schema(new_body: str, schema: dict | None) -> int | None:
    if not schema:
        return None
    diags = _core.validate_section_body(new_body, schema)
    errors = [d for d in diags if d[0] == "ERROR"]
    if errors:
        msg = "; ".join(f"{code}: {m}" for _, code, m in errors)
        print(f"fm-section: schema violation — {msg}", file=sys.stderr)
        return EXIT_TYPE_ERROR
    return None


def _verify_unchanged_outside(
    orig: str,
    new: str,
    *,
    fm_block: str,
    change_start: int,
    change_end: int,
) -> bool:
    """Body-relative byte-for-byte invariant.

    Bytes before body line `change_start` and from line `change_end`
    onwards MUST be identical. Frontmatter MUST be byte-identical.
    """
    orig_body = orig[len(fm_block):]
    orig_lines = orig_body.splitlines(keepends=True)
    head = fm_block + "".join(orig_lines[: change_start])
    tail = "".join(orig_lines[change_end:])
    if not new.startswith(fm_block):
        return False
    if not new.startswith(head):
        return False
    if not new.endswith(tail):
        return False
    return True


_LIST_PREFIX_RE = re.compile(r"^(\s*)([-*]\s+\[[ xX]\]\s+|\d+\.\s+|[-*]\s+)")


def _detect_list_marker(body: str) -> str:
    """Pick a list marker that matches the existing list-style of `body`.
    Default to `- ` if none."""
    for line in body.splitlines():
        m = _LIST_PREFIX_RE.match(line)
        if m:
            return m.group(2)
    return "- "


# ---- Operations --------------------------------------------------------------


def op_replace(body_lines: list[str], span: _core.SectionSpan, payload: str) -> list[str]:
    payload = payload if payload.endswith("\n") else payload + "\n"
    return body_lines[: span.body_start] + [payload] + body_lines[span.body_end:]


def op_append_to(body_lines: list[str], span: _core.SectionSpan, text: str) -> list[str]:
    body = "".join(body_lines[span.body_start: span.body_end])
    if body and not body.endswith("\n"):
        body += "\n"
    if body and not body.endswith("\n\n"):
        body += "\n"
    text = text if text.endswith("\n") else text + "\n"
    new_body = body + text
    return body_lines[: span.body_start] + [new_body] + body_lines[span.body_end:]


def op_append_list_item(body_lines: list[str], span: _core.SectionSpan, item: str) -> list[str]:
    body = "".join(body_lines[span.body_start: span.body_end])
    marker = _detect_list_marker(body)
    if marker[:1].isdigit() or marker[:1] in "0123456789":
        existing = [l for l in body.splitlines() if re.match(r"^\d+\.\s+", l)]
        n = len(existing) + 1
        line = f"{n}. {item}\n"
    else:
        line = f"{marker}{item}\n"
    if body and not body.endswith("\n"):
        body += "\n"
    new_body = body + line
    return body_lines[: span.body_start] + [new_body] + body_lines[span.body_end:]


def op_check_task(body_lines: list[str], span: _core.SectionSpan, needle: str) -> tuple[list[str], int]:
    out = list(body_lines)
    matched = 0
    for i in range(span.body_start, span.body_end):
        line = out[i]
        m = re.match(r"^(\s*)([-*])\s+\[\s\]\s+(.*)$", line.rstrip("\n"))
        if m and needle in m.group(3):
            indent, marker, rest = m.groups()
            out[i] = f"{indent}{marker} [x] {rest}\n"
            matched += 1
    return out, matched


def op_insert(body_lines: list[str], span: _core.SectionSpan, *, before: bool, heading: str, payload: str) -> list[str]:
    payload = payload if payload.endswith("\n") else payload + "\n"
    block = [f"## {heading}\n", "\n", payload]
    if not block[-1].endswith("\n\n"):
        block[-1] = block[-1].rstrip("\n") + "\n\n"
    insertion = "".join(block)
    if before:
        return body_lines[: span.heading_line] + [insertion] + body_lines[span.heading_line:]
    return body_lines[: span.body_end] + [insertion] + body_lines[span.body_end:]


def op_delete(body_lines: list[str], span: _core.SectionSpan) -> list[str]:
    start = span.heading_line
    if span.anchor_line is not None and span.anchor_line == span.heading_line - 1:
        start = span.anchor_line
    return body_lines[: start] + body_lines[span.body_end:]


def op_rename(body_lines: list[str], span: _core.SectionSpan, new_heading: str) -> list[str]:
    out = list(body_lines)
    line = out[span.heading_line]
    leading_ws = line[: len(line) - len(line.lstrip())]
    out[span.heading_line] = f"{leading_ws}## {new_heading}\n"
    return out


# ---- Tier guard for --rename -------------------------------------------------


def _scan_cross_refs(repo_root: Path, target_path: Path, old_heading: str) -> list[Path]:
    """Find other operational files that reference `target_path#old-heading`.

    Markdown anchor convention: lower-cased heading with non-alphanumerics
    collapsed to `-`. Returns a list of files whose body contains a Markdown
    link with a fragment matching the old heading.
    """
    try:
        target_rel = target_path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        # Target lives outside the repo (e.g., a unit-test scratch file).
        # No cross-references possible.
        return []
    target_basename = target_path.name
    anchor = re.sub(r"[^a-z0-9]+", "-", old_heading.lower()).strip("-")
    if not anchor:
        return []
    refs: list[Path] = []
    pattern = re.compile(
        r"\(([^)]*?)#" + re.escape(anchor) + r"[^)\s]*\)",
        re.IGNORECASE,
    )
    for f in _core.iter_operational_files(repo_root):
        if f.resolve() == target_path.resolve():
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in pattern.finditer(text):
            link_target = m.group(1).strip()
            if not link_target:
                continue
            if link_target.endswith(target_basename) or target_rel in link_target:
                refs.append(f)
                break
    return refs


# ---- Main --------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fm-section")
    p.add_argument("path")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--replace", metavar="NAME")
    g.add_argument("--append-to", metavar="NAME")
    g.add_argument("--append-list-item", nargs=2, metavar=("NAME", "ITEM"))
    g.add_argument("--check-task", nargs=2, metavar=("NAME", "ITEM_SUBSTRING"))
    g.add_argument("--insert-after", metavar="NAME")
    g.add_argument("--insert-before", metavar="NAME")
    g.add_argument("--delete", metavar="NAME")
    g.add_argument("--rename", nargs=2, metavar=("OLD", "NEW"))
    p.add_argument("--from-stdin", action="store_true")
    p.add_argument("--text", metavar="STR")
    p.add_argument("--new-heading", metavar="HEADING")
    p.add_argument("--nth", type=int)
    p.add_argument("--anchor")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    path = Path(args.path)
    if not path.is_file():
        return _err(f"fm-section: not a file: {path}", EXIT_NOT_FOUND)

    repo_root = Path.cwd()
    ont = _ontology()
    ttype = _classify(path, repo_root, ont)

    text = path.read_text(encoding="utf-8")
    fm_block, body = _split(text)
    body_lines = body.splitlines(keepends=True)

    target_name = (
        args.replace or args.append_to
        or (args.append_list_item[0] if args.append_list_item else None)
        or (args.check_task[0] if args.check_task else None)
        or args.insert_after or args.insert_before or args.delete
        or (args.rename[0] if args.rename else None)
    )
    if target_name is None:
        return _err("fm-section: no operation supplied", EXIT_USAGE)

    spans = _core.find_section_spans(text, target_name)
    selected = _select(spans, args.nth, args.anchor)
    if isinstance(selected, int):
        if selected == EXIT_AMBIGUOUS:
            return _err(
                f"fm-section: ambiguous address — {len(spans)} matches for '{target_name}'; "
                "use --nth N or --anchor ID",
                EXIT_AMBIGUOUS,
            )
        return _err(f"fm-section: heading not found: '{target_name}'", EXIT_NOT_FOUND)

    new_lines = body_lines
    schema_check_heading: str | None = None

    if args.replace is not None:
        if not args.from_stdin:
            return _err("fm-section: --replace requires --from-stdin", EXIT_USAGE)
        payload = sys.stdin.read()
        new_lines = op_replace(body_lines, selected, payload)
        schema_check_heading = selected.heading_text
    elif args.append_to is not None:
        if args.text is None:
            return _err("fm-section: --append-to requires --text", EXIT_USAGE)
        new_lines = op_append_to(body_lines, selected, args.text)
        schema_check_heading = selected.heading_text
    elif args.append_list_item is not None:
        _, item = args.append_list_item
        new_lines = op_append_list_item(body_lines, selected, item)
        schema_check_heading = selected.heading_text
    elif args.check_task is not None:
        _, needle = args.check_task
        new_lines, matched = op_check_task(body_lines, selected, needle)
        if matched == 0:
            return _err(
                f"fm-section: --check-task found no unchecked item matching '{needle}'",
                EXIT_NOT_FOUND,
            )
        schema_check_heading = selected.heading_text
    elif args.insert_after is not None or args.insert_before is not None:
        if not args.new_heading or not args.from_stdin:
            return _err(
                "fm-section: --insert-* requires both --new-heading and --from-stdin",
                EXIT_USAGE,
            )
        payload = sys.stdin.read()
        new_lines = op_insert(
            body_lines, selected,
            before=args.insert_before is not None,
            heading=args.new_heading,
            payload=payload,
        )
        schema_check_heading = args.new_heading
    elif args.delete is not None:
        new_lines = op_delete(body_lines, selected)
    elif args.rename is not None:
        old, new = args.rename
        cross = _scan_cross_refs(repo_root, path, old)
        if cross:
            cross_paths = ", ".join(sorted({c.resolve().relative_to(repo_root.resolve()).as_posix() for c in cross}))
            return _err(
                f"fm-section: --rename '{old}' is referenced by: {cross_paths}. "
                "This is a T3 change — file a Task per MAINTENANCE.md §1.",
                EXIT_TIER,
            )
        new_lines = op_rename(body_lines, selected, new)
        schema_check_heading = new

    if schema_check_heading is not None:
        post_text = fm_block + "".join(new_lines)
        new_spans = _core.find_section_spans(post_text, schema_check_heading)
        idx = 0 if (args.insert_after or args.insert_before) else (args.nth or 1) - 1
        if 0 <= idx < len(new_spans):
            post_body_lines = "".join(new_lines).splitlines(keepends=True)
            sp = new_spans[idx]
            new_body = "".join(post_body_lines[sp.body_start: sp.body_end])
            schema = _body_schema_for(ttype, _core.normalise_heading(schema_check_heading), ont)
            err = _verify_schema(new_body, schema)
            if err:
                return err

    new_text = fm_block + "".join(new_lines)

    # Compute the change span in body-relative line indices.
    if args.insert_before is not None:
        change_start = selected.heading_line
        change_end = selected.heading_line
    elif args.insert_after is not None:
        change_start = selected.body_end
        change_end = selected.body_end
    elif args.delete is not None:
        change_start = (
            selected.anchor_line
            if (selected.anchor_line is not None
                and selected.anchor_line == selected.heading_line - 1)
            else selected.heading_line
        )
        change_end = selected.body_end
    elif args.rename is not None:
        change_start = selected.heading_line
        change_end = selected.heading_line + 1
    else:
        # replace / append-to / append-list-item / check-task: only body changes.
        change_start = selected.body_start
        change_end = selected.body_end

    if not _verify_unchanged_outside(
        text, new_text,
        fm_block=fm_block,
        change_start=change_start,
        change_end=change_end,
    ):
        return _err(
            "fm-section: internal invariant violated (bytes outside section changed); refusing to write",
            EXIT_TYPE_ERROR,
        )

    with _core.FileLock(path):
        path.write_text(new_text, encoding="utf-8")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
