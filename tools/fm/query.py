#!/usr/bin/env python3
"""fm-query — stateless filesystem query over frontmatter.

Spec anchor: F.5.4.

Usage:
    fm-query <selector>[,<selector>...] [--scope=…] [--limit=N] \\
             [--format=text|json|paths]

Selectors:
    type=<value>           : files whose frontmatter type matches
    status=<value>         : files whose status matches
    slug=<value>           : exact slug match
    has-key=<key>          : files where key is present in frontmatter
    missing-key=<key>      : files where key is required + absent
    refers-to=<slug>       : files whose any *_<list> includes slug
    referenced-by=<slug>   : reverse — files referenced from slug's lists
    stale-since=<N>d       : files whose `updated:` is older than N days

Statelessness invariants:
    - The tool MUST NOT read or write any cache file.
    - Default scope is the operational roots (SPEC §5.4).
    - Default output cap is 1024 bytes (per CONSTRAINTS in the prompt).
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _core  # type: ignore
else:
    from . import _core  # type: ignore

OUTPUT_CAP_BYTES = 1024
STALE_RE = re.compile(r"^(\d+)d$")


def _parse_selectors(raw: str) -> list[tuple[str, str]]:
    parts: list[tuple[str, str]] = []
    for chunk in raw.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            raise SystemExit(f"fm-query: malformed selector {chunk!r}")
        k, _, v = chunk.partition("=")
        parts.append((k.strip(), v.strip()))
    return parts


def _stale_cutoff(spec: str) -> datetime.date:
    m = STALE_RE.match(spec)
    if not m:
        raise SystemExit(f"fm-query: stale-since requires <N>d format, got {spec!r}")
    days = int(m.group(1))
    return datetime.date.today() - datetime.timedelta(days=days)


def _matches(
    fm: dict,
    classification: _core.Classification,
    ontology: dict,
    selectors: list[tuple[str, str]],
    *,
    referenced_index: dict[str, set[str]] | None = None,
    file_slug: str = "",
    stale_cutoffs: dict[str, datetime.date],
) -> bool:
    for k, v in selectors:
        if k == "type":
            if _core.str_val(fm, "type") != v:
                return False
        elif k == "status":
            if _core.str_val(fm, "status") != v:
                return False
        elif k == "slug":
            if _core.str_val(fm, "slug") != v:
                return False
        elif k == "has-key":
            if v not in fm:
                return False
        elif k == "missing-key":
            type_for_keys = _core.str_val(fm, "type") or classification.expected_type
            required = ontology["types"].get(type_for_keys or "", {}).get("required_keys", [])
            if v not in required:
                # Not a required key for this type — never "missing-required".
                return False
            if v in fm:
                return False
        elif k == "refers-to":
            # SPEC §5.4: "files whose any *_<list> includes slug".
            # Any list-valued frontmatter key counts; non-list values are
            # ignored. Selector matches when at least one list contains v.
            if not any(isinstance(val, list) and v in val
                       for val in fm.values()):
                return False
        elif k == "referenced-by":
            # `referenced-by=<slug>` means: this file's slug appears in any list
            # of the file with slug=<v>. The caller pre-built referenced_index.
            if referenced_index is None:
                return False
            if file_slug not in referenced_index.get(v, set()):
                return False
        elif k == "stale-since":
            cutoff = stale_cutoffs[v]
            try:
                d = datetime.date.fromisoformat(_core.str_val(fm, "updated"))
            except ValueError:
                return False
            if d > cutoff:
                return False
        else:
            raise SystemExit(f"fm-query: unknown selector {k!r}")
    return True


def _build_referenced_index(
    repo_root: Path, scope: list[str] | None
) -> dict[str, set[str]]:
    """For every file with slug=S, collect the set of slugs in its frontmatter
    lists. Returns {S: set_of_referenced_slugs}."""
    out: dict[str, set[str]] = {}
    for path in _core.iter_operational_files(repo_root, scope=scope):
        fm = _core.read_fm(path, strict=False)
        slug = _core.str_val(fm, "slug")
        if not slug:
            continue
        refs: set[str] = set()
        for key, val in fm.items():
            if isinstance(val, list):
                refs.update(s for s in val if isinstance(s, str))
        out[slug] = refs
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fm-query", add_help=True)
    p.add_argument("selector",
                   help="comma-joined selectors, e.g., 'type=task,status=active'")
    p.add_argument("--scope", default=None,
                   help="comma-separated subset of operational roots")
    p.add_argument("--limit", type=int, default=0,
                   help="cap the result count (0 = unlimited)")
    p.add_argument("--format", choices=("text", "json", "paths"), default="paths")
    args = p.parse_args(argv)

    if args.limit < 0:
        raise SystemExit(f"fm-query: --limit must be ≥ 0, got {args.limit}")

    repo_root = _core.repo_root_from_cwd()
    ontology = _core.load_ontology(repo_root)
    selectors = _parse_selectors(args.selector)

    scope: list[str] | None = (
        [s.strip() for s in args.scope.split(",") if s.strip()]
        if args.scope else None
    )

    # Pre-compute stale cutoffs once (no per-file recomputation).
    stale_cutoffs: dict[str, datetime.date] = {}
    for k, v in selectors:
        if k == "stale-since":
            stale_cutoffs[v] = _stale_cutoff(v)

    referenced_index: dict[str, set[str]] | None = None
    if any(k == "referenced-by" for k, _ in selectors):
        referenced_index = _build_referenced_index(repo_root, scope)

    # path-classification is only consulted by the `missing-key` selector
    # (to derive the expected type when frontmatter omits it). Skip the
    # fnmatch sweep entirely when no selector needs it.
    needs_classification = any(k == "missing-key" for k, _ in selectors)
    empty_classification = _core.Classification(None)

    matches: list[str] = []
    for path in _core.iter_operational_files(repo_root, scope=scope):
        cls = (_core.classify_path(path, repo_root, ontology)
               if needs_classification else empty_classification)
        # fm-query MAY consider files outside path classification, but we
        # still respect operational scope. Read frontmatter leniently.
        fm = _core.read_fm(path, strict=False)
        slug = _core.str_val(fm, "slug")
        if _matches(fm, cls, ontology, selectors,
                    referenced_index=referenced_index,
                    file_slug=slug, stale_cutoffs=stale_cutoffs):
            try:
                rel = path.resolve().relative_to(repo_root.resolve())
            except ValueError:
                rel = path
            matches.append(str(rel))

    matches.sort()
    if args.limit > 0:
        matches = matches[: args.limit]

    if args.format == "json":
        out = json.dumps({"matches": matches}, indent=2)
    elif args.format == "text":
        out = "\n".join(matches) + ("\n" if matches else "")
    else:  # paths
        out = "\n".join(matches) + ("\n" if matches else "")

    raw = out.encode("utf-8")
    if len(raw) > OUTPUT_CAP_BYTES:
        truncated = raw[:OUTPUT_CAP_BYTES].decode("utf-8", errors="ignore")
        # Snip back to the last newline for a clean cut, then append a
        # truncation marker line.
        if "\n" in truncated:
            truncated = truncated[: truncated.rfind("\n") + 1]
        sys.stdout.write(truncated)
        sys.stdout.write(f"… [truncated; {len(matches)} total matches]\n")
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
