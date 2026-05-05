#!/usr/bin/env python3
"""fm-fix — tier-tagged auto-repair driver atop fm-validate / fm-edit.

Spec anchors: F.5.1, F.7.2, F.12.4 (closed-set repair recipes).
Maintenance ladder: see /MAINTENANCE.md §1.

Surface
-------

    python3 tools/fm/fix.py [PATH ...] [--dry-run | --apply] [--code F.X.Y[,...]]

Default mode is ``--dry-run`` (no writes). ``--apply`` writes via
``fm.edit.apply_edit`` under an OS-level FileLock. Anything outside the
closed-set recipe table is deferred to a draft Task stub in
``tasks/<NNN>-fix-<slug>/task.md``.

Recipe table (closed set)
-------------------------

* F.3.1 missing L1 ``updated``                  → T1, ``--bump-updated``
* F.3.1 missing L1 ``created``                  → T1, ``--set created=<today-utc>``
* F.3.1 missing L1 ``type`` (path unambiguous)  → T2, ``--set type=<expected>``
* F.3.1 missing L1 ``status`` (path unambiguous) → T2, ``--set status=draft``
* F.3.1 missing L1 ``slug`` (derivable)         → T1, ``--set slug=<derived>``
* F.3.2 missing L2 list-typed key               → T2, ``--append-list <key>`` (empty)
* F.3.3 type/path disagreement, alt_types open  → T2, ``--set type=<expected>``
* F.3.4 did-you-mean                            → REFUSED (warning printed)
* F.4.2 missing required heading                → REFUSED (warning printed)
* anything else                                 → T3 stub

Exit codes
----------

* 0 on success (no errors, even if items were deferred).
* 1 if any file still has unfixed errors after the run (apply mode).
* 4 when the user passes a ``--code`` value that is not in the recipe table
  AND it is not a known F.* code we recognise as "deferred-only" (T3).
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# Allow running as `python3 tools/fm/fix.py` (script mode).
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _core  # type: ignore
    import edit as _edit  # type: ignore
    import validate as _validate  # type: ignore
else:
    from . import _core, edit as _edit, validate as _validate  # type: ignore

EXIT_OK = 0
EXIT_HAS_ERRORS = 1
EXIT_USAGE = 2
EXIT_UNKNOWN_CODE = 4

# All F.* codes the validator can emit. Anything outside this set passed via
# --code triggers EXIT_UNKNOWN_CODE.
KNOWN_CODES = frozenset({
    "F.3.1", "F.3.2", "F.3.3", "F.3.4",
    "F.4.1", "F.4.2", "F.4.3",
    "F.B.1", "F.B.2", "F.B.3", "F.B.4", "F.B.5", "F.B.6", "F.B.7",
})

# L2 keys we are willing to default to an empty list. Naming convention:
# tail tokens like "_paths", "_prompts", "_research", "_blocked_by",
# "_supersedes", "_superseded_by" are list-typed by ontology contract.
_LIST_KEY_HINTS = (
    "_uses_prompts", "_spawns_research", "_spawns_prompts",
    "_affects_paths", "_blocked_by", "_supersedes", "_superseded_by",
    "_target_agents",
)

SLUG_DERIVE_RE = re.compile(r"^[0-9]{3}-(.+)$")


# ---- Diagnostic parsing -----------------------------------------------------

L1_KEY_LIST_RE = re.compile(r"missing L1 keys \[([^\]]+)\]")
L2_KEY_LIST_RE = re.compile(r"missing L2 keys \[([^\]]+)\] \(type=([^)]+)\)")
TYPE_DISAGREE_RE = re.compile(r"type '([^']+)' disagrees with path-expected type")
DID_YOU_MEAN_RE = re.compile(r"did you mean '([^']+)'")
HEADING_RE = re.compile(r"missing required heading '## (.+)'")


def _parse_keys(s: str) -> list[str]:
    return [tok.strip().strip("'").strip('"') for tok in s.split(",") if tok.strip()]


# ---- Repair plan model ------------------------------------------------------

@dataclass
class Repair:
    """One mutation to apply via fm-edit's apply_edit()."""
    tier: str               # "T1" or "T2"
    code: str               # F.* code that triggered the repair
    action: str             # apply_edit action: "set"/"append-list"/"bump-updated"
    args: tuple[str, ...] = ()
    explain: str = ""       # human-readable summary, used in dry-run output


@dataclass
class Refusal:
    code: str
    message: str
    explain: str


@dataclass
class Defer:
    code: str
    message: str
    explain: str


@dataclass
class FilePlan:
    path: Path
    rel: str
    repairs: list[Repair] = field(default_factory=list)
    refusals: list[Refusal] = field(default_factory=list)
    defers: list[Defer] = field(default_factory=list)
    unrecognised: list[tuple[str, str]] = field(default_factory=list)


# ---- Recipe planner ---------------------------------------------------------

def _today_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def _is_list_typed(key: str) -> bool:
    return any(key.endswith(h) for h in _LIST_KEY_HINTS) or key == "task_uses_prompts"


def _derive_slug_from_path(path: Path) -> str | None:
    """Return a slug derived from the parent folder for tasks/NNN-foo/task.md
    or skills/foo/SKILL.md style paths. None if no clean derivation exists."""
    parent = path.parent.name
    m = SLUG_DERIVE_RE.match(parent)
    if m:
        return m.group(1)
    if parent and re.match(r"^[a-z0-9-]+$", parent):
        return parent
    return None


def plan_for_diag(
    diag: _core.Diagnostic,
    classification: _core.Classification,
    path: Path,
) -> tuple[list[Repair], list[Refusal], list[Defer]]:
    """Translate one diagnostic into 0+ Repairs (auto-apply) or a Refusal/Defer.

    Returns (repairs, refusals, defers). Exactly one of the three lists is
    typically non-empty per diagnostic.
    """
    repairs: list[Repair] = []
    refusals: list[Refusal] = []
    defers: list[Defer] = []
    code = diag.code
    msg = diag.message
    expected = classification.expected_type

    # ---- F.3.1: missing L1 keys ----
    if code == "F.3.1":
        m = L1_KEY_LIST_RE.search(msg)
        if not m:
            defers.append(Defer(code, msg, "F.3.1 with unparseable key list"))
            return repairs, refusals, defers
        keys = _parse_keys(m.group(1))
        for key in keys:
            if key == "updated":
                repairs.append(Repair(
                    "T1", code, "bump-updated", (),
                    "set updated to today (UTC)",
                ))
            elif key == "created":
                repairs.append(Repair(
                    "T1", code, "set", (f"created={_today_utc()}",),
                    f"set created={_today_utc()}",
                ))
            elif key == "type":
                if expected:
                    repairs.append(Repair(
                        "T2", code, "set", (f"type={expected}",),
                        f"set type={expected} (from path classification)",
                    ))
                else:
                    defers.append(Defer(
                        code, msg,
                        "missing 'type' but path classification is ambiguous",
                    ))
            elif key == "status":
                # 'draft' is the universally safe default for newborn files
                # (per status_values). T2: additive, no semantic change.
                repairs.append(Repair(
                    "T2", code, "set", ("status=draft",),
                    "set status=draft (safe default)",
                ))
            elif key == "slug":
                derived = _derive_slug_from_path(path)
                if derived:
                    repairs.append(Repair(
                        "T1", code, "set", (f"slug={derived}",),
                        f"set slug={derived} (derived from folder name)",
                    ))
                else:
                    defers.append(Defer(
                        code, msg,
                        "missing 'slug' and no derivation from folder name",
                    ))
            elif key == "summary":
                # Authoring required — never auto-fillable.
                defers.append(Defer(
                    code, msg,
                    "missing 'summary' requires human authoring",
                ))
            else:
                defers.append(Defer(
                    code, msg,
                    f"missing L1 key {key!r} has no mechanical recipe",
                ))
        return repairs, refusals, defers

    # ---- F.3.2: missing L2 keys ----
    if code == "F.3.2":
        m = L2_KEY_LIST_RE.search(msg)
        if not m:
            defers.append(Defer(code, msg, "F.3.2 with unparseable key list"))
            return repairs, refusals, defers
        keys = _parse_keys(m.group(1))
        for key in keys:
            if _is_list_typed(key):
                # apply_edit's append-list creates an empty list when the key
                # is absent, but we want `key: []`. Use a sentinel pattern:
                # apply --set key=[]? No — _do_set marks it scalar. Instead,
                # a fresh empty list is the natural state of a list key the
                # planner inserts. Use action "ensure-empty-list".
                repairs.append(Repair(
                    "T2", code, "ensure-empty-list", (key,),
                    f"insert empty list {key}: []",
                ))
            else:
                # Scalar L2 keys (e.g. prompt_kind, research_phase) carry
                # semantics — defer to a Task stub.
                defers.append(Defer(
                    code, msg,
                    f"missing L2 key {key!r} is scalar (semantic) — needs author",
                ))
        return repairs, refusals, defers

    # ---- F.3.3: type/path disagreement ----
    if code == "F.3.3":
        m = TYPE_DISAGREE_RE.search(msg)
        if m and expected and classification.alt_types:
            # Path declares alt_types — the path is flexible, so flipping the
            # declared type to the canonical primary is mechanical.
            repairs.append(Repair(
                "T2", code, "set", (f"type={expected}",),
                f"set type={expected} (path's primary, alt_types={list(classification.alt_types)})",
            ))
        else:
            defers.append(Defer(
                code, msg,
                "F.3.3 outside the alt-permitted recipe — needs review",
            ))
        return repairs, refusals, defers

    # ---- F.3.4: did-you-mean — REFUSED ----
    if code == "F.3.4":
        refusals.append(Refusal(
            code, msg,
            "did-you-mean is never auto-applied (renaming a key may lose data)",
        ))
        return repairs, refusals, defers

    # ---- F.4.2: missing required heading — REFUSED ----
    if code == "F.4.2":
        m = HEADING_RE.search(msg)
        what = m.group(1) if m else "<heading>"
        refusals.append(Refusal(
            code, msg,
            f"adding heading '## {what}' requires body authoring (T3)",
        ))
        return repairs, refusals, defers

    # ---- anything else: T3 stub ----
    defers.append(Defer(code, msg, f"no recipe for {code}"))
    return repairs, refusals, defers


# ---- Mutation surface bridge ------------------------------------------------

def _ensure_empty_list_apply(text: str, key: str) -> str:
    """Insert ``key: []`` if absent, idempotently. Mirrors apply_edit's
    invariants (preserves body bytes). Used because apply_edit's
    ``append-list`` requires a value and ``set key=[]`` would be quoted as a
    scalar string."""
    open_fence, fm_body, rest = _edit._split(text)
    if not open_fence:
        return text
    entries = _edit._parse_lines(fm_body)
    if _edit._find(entries, key) is not None:
        return text
    entries.append({"kind": "list", "key": key, "value": [], "raw": []})
    new_fm = _edit._render(entries)
    return open_fence + new_fm + rest


def apply_repairs_to_text(text: str, repairs: Iterable[Repair]) -> str:
    """Apply a list of Repairs to ``text`` in order. Pure function (no I/O)."""
    cur = text
    for r in repairs:
        if r.action == "ensure-empty-list":
            cur = _ensure_empty_list_apply(cur, r.args[0])
            continue
        new_text, rc = _edit.apply_edit(cur, r.action, *r.args)
        if rc != _edit.EXIT_OK:
            raise RuntimeError(
                f"fm-fix: apply_edit({r.action}, {r.args}) returned rc={rc}; "
                f"the recipe table generated a mutation fm-edit refused."
            )
        cur = new_text
    return cur


# ---- Task stub generator ----------------------------------------------------

_SLUGIFY_RE = re.compile(r"[^a-z0-9-]+")


def _slugify(s: str) -> str:
    s = s.lower().replace(" ", "-").replace("/", "-").replace(".", "-")
    s = _SLUGIFY_RE.sub("-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "fix"


def _next_task_id(repo_root: Path) -> str:
    """Return the smallest free 3-digit task id by scanning ``tasks/``."""
    used: set[int] = set()
    tasks = repo_root / "tasks"
    if tasks.exists():
        for child in tasks.iterdir():
            if not child.is_dir():
                continue
            m = re.match(r"^([0-9]{3})-", child.name)
            if m:
                used.add(int(m.group(1)))
    n = 1
    while n in used:
        n += 1
    return f"{n:03d}"


def _stub_text(
    *,
    task_id: str,
    slug: str,
    rel_path: str,
    diag_line: str,
    explain: str,
    today: str,
) -> str:
    summary = (
        f"Auto-generated by fm-fix: defer T3 repair for {rel_path} "
        f"({diag_line.split(':')[3] if diag_line.count(':') >= 3 else 'F.?.?'})"
    )
    body = (
        f"---\n"
        f"type: task\n"
        f"status: draft\n"
        f"slug: {slug}\n"
        f"summary: \"{summary}\"\n"
        f"created: {today}\n"
        f"updated: {today}\n"
        f"task_id: \"{task_id}\"\n"
        f"task_status: draft\n"
        f"task_owner: \"unassigned\"\n"
        f"task_priority: P3\n"
        f"task_uses_prompts: []\n"
        f"task_spawns_research: []\n"
        f"task_spawns_prompts: []\n"
        f"task_affects_paths:\n"
        f"  - {rel_path}\n"
        f"---\n"
        f"\n"
        f"# Task {task_id} - fm-fix deferred repair\n"
        f"\n"
        f"## Goal\n"
        f"\n"
        f"Resolve the following fm-validate diagnostic that fm-fix could not "
        f"safely auto-repair: `{diag_line}`. Reason: {explain}.\n"
        f"\n"
        f"## Plan\n"
        f"\n"
        f"1. Inspect `{rel_path}`, decide the correct repair, and apply it via "
        f"fm-edit (T1/T2) or by editing the body (T3).\n"
        f"\n"
        f"## Todo\n"
        f"\n"
        f"- [ ] 1. Apply the repair and re-run fm-validate to confirm zero "
        f"diagnostics for this file.\n"
        f"\n"
        f"## Links\n"
        f"\n"
        f"- Affected file: [`/{rel_path}`](../../{rel_path})\n"
        f"- Governing spec: [`/MAINTENANCE.md`](../../MAINTENANCE.md)\n"
    )
    return body


def write_stub(
    repo_root: Path,
    plan: FilePlan,
    defer: Defer,
    *,
    write: bool,
    today: str | None = None,
    task_id: str | None = None,
) -> Path:
    """Materialise (or simulate) one T3 stub and return its (planned) path."""
    today = today or _today_utc()
    task_id = task_id or _next_task_id(repo_root)
    base_slug = Path(plan.rel).stem
    slug = _slugify(f"fix-{base_slug}-{defer.code.lower()}")[:60].rstrip("-") or "fix"
    folder = repo_root / "tasks" / f"{task_id}-{slug}"
    target = folder / "task.md"
    diag_line = f"{plan.rel}::ERROR:{defer.code}:{defer.message}"
    text = _stub_text(
        task_id=task_id,
        slug=slug,
        rel_path=plan.rel,
        diag_line=diag_line,
        explain=defer.explain,
        today=today,
    )
    if write:
        folder.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    return target


# ---- File-level driver ------------------------------------------------------

def build_plan(
    diags: list[_core.Diagnostic],
    repo_root: Path,
    ontology: dict,
    *,
    code_filter: set[str] | None,
) -> dict[Path, FilePlan]:
    """Group diagnostics by absolute path and translate them into FilePlans.

    Diagnostics with codes not in code_filter (when given) are dropped.
    """
    plans: dict[Path, FilePlan] = {}
    for d in diags:
        if code_filter and d.code not in code_filter:
            continue
        rel = d.path
        abs_path = (repo_root / rel).resolve()
        if abs_path not in plans:
            plans[abs_path] = FilePlan(path=abs_path, rel=rel)
        plan = plans[abs_path]
        cls = _core.classify_path(abs_path, repo_root, ontology)
        repairs, refusals, defers = plan_for_diag(d, cls, abs_path)
        plan.repairs.extend(repairs)
        plan.refusals.extend(refusals)
        plan.defers.extend(defers)
    return plans


def execute_plan(
    plan: FilePlan,
    repo_root: Path,
    *,
    apply: bool,
    today: str | None,
    next_id_fn,
    out,
) -> tuple[int, int, int, int]:
    """Apply (or simulate) all repairs and emit stubs for one file.

    Returns (t1_count, t2_count, deferred_count, refused_count).
    """
    t1 = sum(1 for r in plan.repairs if r.tier == "T1")
    t2 = sum(1 for r in plan.repairs if r.tier == "T2")
    deferred = len(plan.defers)
    refused = len(plan.refusals)

    if plan.repairs:
        if apply:
            with _core.FileLock(plan.path):
                text = plan.path.read_text(encoding="utf-8")
                new_text = apply_repairs_to_text(text, plan.repairs)
                if new_text != text:
                    plan.path.write_text(new_text, encoding="utf-8")
        for r in plan.repairs:
            verb = "APPLY" if apply else "DRYRUN"
            print(f"[{verb}] {plan.rel} :: {r.tier} {r.code} -> {r.explain}",
                  file=out)

    for refusal in plan.refusals:
        print(f"[REFUSE] {plan.rel} :: {refusal.code}: {refusal.explain}",
              file=out)

    for defer in plan.defers:
        target = write_stub(
            repo_root, plan, defer,
            write=apply,
            today=today,
            task_id=next_id_fn(),
        )
        verb = "STUB" if apply else "DRY-STUB"
        rel_target = target.relative_to(repo_root) if target.is_absolute() else target
        print(f"[{verb}] {plan.rel} :: {defer.code}: would create {rel_target}",
              file=out)

    return t1, t2, deferred, refused


# ---- CLI --------------------------------------------------------------------

def _gather_diagnostics(
    targets: list[Path],
    repo_root: Path,
    ontology: dict,
) -> list[_core.Diagnostic]:
    diags: list[_core.Diagnostic] = []
    for path in _validate._iter_targets([str(p) for p in targets], repo_root, None):
        cls = _core.classify_path(path, repo_root, ontology)
        if cls.expected_type is None:
            continue
        diags.extend(_validate.check_file(path, repo_root, ontology, classification=cls))
    return diags


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fm-fix", add_help=True)
    p.add_argument("paths", nargs="*",
                   help="Files or directories to scan; default = all operational roots")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", default=True,
                   help="(default) print the plan, do not write")
    g.add_argument("--apply", action="store_true",
                   help="actually write repairs and stubs")
    p.add_argument("--code", default=None,
                   help="comma-separated list of F.* codes to act on; default = all")
    p.add_argument("--format", choices=("text", "json"), default="text")
    args = p.parse_args(argv)

    apply_mode = bool(args.apply)
    repo_root = _core.repo_root_from_cwd()
    ontology = _core.load_ontology(repo_root)

    code_filter: set[str] | None = None
    if args.code:
        code_filter = {c.strip() for c in args.code.split(",") if c.strip()}
        bad = [c for c in code_filter if c not in KNOWN_CODES]
        if bad:
            print(f"fm-fix: unknown code(s): {sorted(bad)}", file=sys.stderr)
            return EXIT_UNKNOWN_CODE

    target_paths = [Path(p) for p in args.paths] if args.paths else []

    diags = _gather_diagnostics(target_paths, repo_root, ontology)
    plans = build_plan(diags, repo_root, ontology, code_filter=code_filter)

    # Allocate task ids for stubs as we go, so dry-run and apply both produce
    # deterministic, non-clashing ids.
    used: set[int] = set()
    tasks_dir = repo_root / "tasks"
    if tasks_dir.exists():
        for child in tasks_dir.iterdir():
            if not child.is_dir():
                continue
            m = re.match(r"^([0-9]{3})-", child.name)
            if m:
                used.add(int(m.group(1)))

    counter = {"n": 1}

    def _next_id() -> str:
        while counter["n"] in used:
            counter["n"] += 1
        nid = counter["n"]
        used.add(nid)
        counter["n"] += 1
        return f"{nid:03d}"

    today = _today_utc()
    fixed_t1 = fixed_t2 = deferred_total = refused_total = 0
    out_stream = sys.stdout

    json_records: list[dict] = []
    for path in sorted(plans.keys()):
        plan = plans[path]
        t1, t2, dd, rr = execute_plan(
            plan, repo_root,
            apply=apply_mode,
            today=today,
            next_id_fn=_next_id,
            out=out_stream,
        )
        fixed_t1 += t1
        fixed_t2 += t2
        deferred_total += dd
        refused_total += rr
        if args.format == "json":
            json_records.append({
                "path": plan.rel,
                "repairs": [
                    {"tier": r.tier, "code": r.code, "action": r.action,
                     "args": list(r.args), "explain": r.explain}
                    for r in plan.repairs
                ],
                "refusals": [
                    {"code": r.code, "message": r.message, "explain": r.explain}
                    for r in plan.refusals
                ],
                "defers": [
                    {"code": d.code, "message": d.message, "explain": d.explain}
                    for d in plan.defers
                ],
            })

    if args.format == "json":
        print(json.dumps({
            "apply": apply_mode,
            "files": json_records,
            "summary": {
                "fixed": fixed_t1 + fixed_t2,
                "t1": fixed_t1,
                "t2": fixed_t2,
                "deferred": deferred_total,
                "refused": refused_total,
            },
        }, indent=2))
    else:
        total_fixed = fixed_t1 + fixed_t2
        print(f"Fixed {total_fixed} (T1={fixed_t1}, T2={fixed_t2}); "
              f"deferred to Tasks: {deferred_total}; refused: {refused_total}.")

    # Report a non-zero exit if --apply left any errors uncovered (i.e. there
    # were defers/refusals): the caller may want to gate on that.
    if apply_mode and (deferred_total + refused_total) > 0:
        return EXIT_HAS_ERRORS
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
