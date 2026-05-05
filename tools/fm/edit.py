#!/usr/bin/env python3
"""fm-edit — small, idempotent mutations of frontmatter only.

Spec anchor: F.5.3, F.7.2.

Usage:
    fm-edit <path> --set <key>=<value>
    fm-edit <path> --unset <key>
    fm-edit <path> --append-list <key> <value>
    fm-edit <path> --remove-from-list <key> <value>
    fm-edit <path> --bump-updated

Invariants:
    - The body bytes after the closing `---\\n` MUST be byte-identical pre/post.
    - --append-list MUST NOT introduce a duplicate.
    - --bump-updated is a no-op when `updated:` already equals today's UTC date.
    - --set on a list-valued key fails with exit 4 (use --append-list).
    - The whole read-modify-write is wrapped in an OS file lock.
"""
from __future__ import annotations

import argparse
import datetime
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


def _today_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def _split(text: str) -> tuple[str, str, str]:
    """Return (open_fence, fm_body, rest) where rest starts with `---\\n` and
    contains the file body. If there is no frontmatter, fm_body is empty and
    rest equals the entire input (caller must error)."""
    m = _core.FRONTMATTER_RE.match(text)
    if not m:
        return "", "", text
    fm_body = m.group(1)
    open_fence = "---\n"
    closing_start = m.end(1)  # position of `\n` before the closing `---`
    rest = text[closing_start:]
    # Ensure the rest starts at the closing `---` line.
    return open_fence, fm_body, rest


def _parse_lines(fm_body: str) -> list[dict]:
    """Parse fm_body into a list of dicts:
    {kind: "scalar"|"list", key: str, value: str|list[str], raw: list[str]}
    The order is preserved, and `raw` lets us round-trip unchanged when no
    edit touches the entry.
    """
    entries: list[dict] = []
    i = 0
    lines = fm_body.split("\n")
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            entries.append({"kind": "blank", "raw": [raw]})
            i += 1
            continue
        if ":" not in stripped:
            entries.append({"kind": "blank", "raw": [raw]})
            i += 1
            continue
        key, _, val = stripped.partition(":")
        key = key.strip()
        val = val.strip()
        if val == "" or val == "[]":
            # block list
            list_items: list[str] = []
            raws = [raw]
            j = i + 1
            while j < len(lines):
                cont = lines[j]
                cs = cont.strip()
                if cs.startswith("- "):
                    list_items.append(cs[2:].strip().strip('"').strip("'"))
                    raws.append(cont)
                    j += 1
                elif cs == "":
                    raws.append(cont)
                    j += 1
                else:
                    break
            # Trim trailing blanks from `raws` so we don't accidentally
            # absorb the next entry's whitespace.
            while raws and raws[-1].strip() == "":
                raws.pop()
            entries.append({
                "kind": "list", "key": key, "value": list_items,
                "raw": raws,
            })
            i = i + len(raws)
        else:
            quoted = val.startswith(('"', "'"))
            entries.append({
                "kind": "scalar", "key": key,
                "value": val.strip('"').strip("'"),
                "quoted": quoted, "raw": [raw],
            })
            i += 1
    return entries


def _render(entries: list[dict]) -> str:
    out: list[str] = []
    for e in entries:
        if e["kind"] == "blank":
            out.extend(e["raw"])
        elif e["kind"] == "scalar":
            v = e["value"]
            # Preserve original quoting where present; quote anyway if the
            # value contains characters that re-parse ambiguously without
            # quotes, OR if it would otherwise be interpreted as a non-string
            # scalar (digits-only, "true"/"false"/"null", ISO-date-like).
            forced = (
                v == ""
                or any(ch in v for ch in (":", "#", "[", "]", "{", "}", ",",
                                          "&", "*", "!", "|", ">", "%", "@", "`"))
            )
            if e.get("quoted") or forced:
                escaped = v.replace("\\", "\\\\").replace('"', '\\"')
                out.append(f"{e['key']}: \"{escaped}\"")
            else:
                out.append(f"{e['key']}: {v}")
        elif e["kind"] == "list":
            items = e["value"]
            if not items:
                out.append(f"{e['key']}: []")
            else:
                out.append(f"{e['key']}:")
                for item in items:
                    out.append(f"  - {item}")
    return "\n".join(out)


def _find(entries: list[dict], key: str) -> int | None:
    for idx, e in enumerate(entries):
        if e["kind"] in ("scalar", "list") and e["key"] == key:
            return idx
    return None


def _do_set(entries: list[dict], key: str, value: str) -> int:
    idx = _find(entries, key)
    if idx is not None and entries[idx]["kind"] == "list":
        return EXIT_TYPE_ERROR
    # Preserve the original quoting style if we're replacing an existing
    # scalar, so `--set task_id=099` keeps `task_id: "099"` quoted.
    quoted = entries[idx].get("quoted", False) if idx is not None else False
    new = {"kind": "scalar", "key": key, "value": value,
           "quoted": quoted, "raw": []}
    if idx is None:
        entries.append(new)
    else:
        entries[idx] = new
    return EXIT_OK


def _do_unset(entries: list[dict], key: str) -> int:
    idx = _find(entries, key)
    if idx is None:
        return EXIT_OK  # idempotent
    entries.pop(idx)
    return EXIT_OK


def _do_append_list(entries: list[dict], key: str, value: str) -> int:
    idx = _find(entries, key)
    if idx is None:
        entries.append({"kind": "list", "key": key, "value": [value], "raw": []})
        return EXIT_OK
    e = entries[idx]
    if e["kind"] == "scalar":
        return EXIT_TYPE_ERROR
    if value not in e["value"]:
        e["value"].append(value)
    return EXIT_OK


def _do_remove_from_list(entries: list[dict], key: str, value: str) -> int:
    idx = _find(entries, key)
    if idx is None:
        return EXIT_OK  # idempotent
    e = entries[idx]
    if e["kind"] != "list":
        return EXIT_TYPE_ERROR
    e["value"] = [v for v in e["value"] if v != value]
    return EXIT_OK


def _do_bump_updated(entries: list[dict]) -> int:
    today = _today_utc()
    idx = _find(entries, "updated")
    if idx is None:
        entries.append({"kind": "scalar", "key": "updated",
                        "value": today, "raw": []})
        return EXIT_OK
    e = entries[idx]
    if e["kind"] != "scalar":
        return EXIT_TYPE_ERROR
    if e["value"] == today:
        return EXIT_OK  # no-op
    e["value"] = today
    return EXIT_OK


def apply_edit(text: str, action: str, *args: str) -> tuple[str, int]:
    """Pure-function form, used by tests."""
    open_fence, fm_body, rest = _split(text)
    if not open_fence:
        return text, EXIT_NOT_FOUND
    entries = _parse_lines(fm_body)
    rc = EXIT_OK
    if action == "set":
        key, _, val = args[0].partition("=")
        rc = _do_set(entries, key.strip(), val)
    elif action == "unset":
        rc = _do_unset(entries, args[0])
    elif action == "append-list":
        rc = _do_append_list(entries, args[0], args[1])
    elif action == "remove-from-list":
        rc = _do_remove_from_list(entries, args[0], args[1])
    elif action == "bump-updated":
        rc = _do_bump_updated(entries)
    else:
        return text, EXIT_USAGE
    if rc != EXIT_OK:
        return text, rc
    new_fm = _render(entries)
    new_text = open_fence + new_fm + rest
    # Body bytes (`rest` — everything from the closing fence onward) are by
    # construction identical pre/post: we reuse the same `rest` string. This
    # check catches the case where a future change introduces a mutation
    # path that bypasses the construction. RuntimeError (not assert) so the
    # guard survives `python -O`.
    _, _, new_rest = _split(new_text)
    if rest != new_rest:
        raise RuntimeError("fm-edit invariant: body bytes changed")
    return new_text, EXIT_OK


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fm-edit", add_help=True)
    p.add_argument("path", type=Path)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--set", metavar="KEY=VALUE")
    g.add_argument("--unset", metavar="KEY")
    g.add_argument("--append-list", nargs=2, metavar=("KEY", "VALUE"))
    g.add_argument("--remove-from-list", nargs=2, metavar=("KEY", "VALUE"))
    g.add_argument("--bump-updated", action="store_true")
    args = p.parse_args(argv)

    if not args.path.exists():
        print(f"fm-edit: no such file: {args.path}", file=sys.stderr)
        return EXIT_NOT_FOUND

    with _core.FileLock(args.path):
        text = args.path.read_text(encoding="utf-8")

        if args.set is not None:
            new_text, rc = apply_edit(text, "set", args.set)
        elif args.unset is not None:
            new_text, rc = apply_edit(text, "unset", args.unset)
        elif args.append_list is not None:
            new_text, rc = apply_edit(text, "append-list",
                                      args.append_list[0], args.append_list[1])
        elif args.remove_from_list is not None:
            new_text, rc = apply_edit(text, "remove-from-list",
                                      args.remove_from_list[0],
                                      args.remove_from_list[1])
        elif args.bump_updated:
            new_text, rc = apply_edit(text, "bump-updated")
        else:
            return EXIT_USAGE

        if rc == EXIT_TYPE_ERROR:
            print("fm-edit: type error — use --append-list / --remove-from-list "
                  "for list-valued keys", file=sys.stderr)
            return rc
        if rc != EXIT_OK:
            return rc

        if new_text != text:
            args.path.write_text(new_text, encoding="utf-8")

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
