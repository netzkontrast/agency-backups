#!/usr/bin/env python3
"""check-hard-rules — validate Dramatica Hard Rules H1-H12 against architecture.yaml.

Spec anchor:
    skills/novel-architect-structure/methods/validation/hard-rules.md §1 (Task 073)
    skills/dramatica-theory/references/00-storyform-validation.md (canonical numbering)

Target: `architecture.yaml` files produced by novel-architect Phase 2.

Implementation tier:
  Fully mechanical (this linter):  H1, H2, H3, H4, H9, H10, H11, H12.
  Deferred to follow-up:           H5, H6, H7, H8 — require Type/Quad/Element/
                                    Dynamic-Pair ontology lookups via
                                    tools/dramatica-nav/nav.py. The linter
                                    emits an INFO diagnostic noting the gap;
                                    full coverage lands when Task 085 promotes
                                    this linter to ERROR-tier.

Exit codes:
    0 — clean (no H-rule violations)
    1 — usage error
    2 — at least one WARN diagnostic surfaced

Initial landing: **WARN-tier** (advisory). Task 085 promotes to ERROR after
one validation cycle on real corpus.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, Any

import yaml  # type: ignore


THROUGHLINE_KEYS = ("os", "mc", "ic", "ss")
ALL_CLASSES = {"Universe", "Physics", "Mind", "Psychology"}
COMPLEMENT_PAIRS = {
    "Universe": "Mind", "Mind": "Universe",
    "Physics": "Psychology", "Psychology": "Physics",
}
ENUM_RESOLVE = {"Change", "Steadfast"}
ENUM_GROWTH = {"Start", "Stop"}
ENUM_APPROACH = {"Doer", "Beer", "Do-er", "Be-er"}
ENUM_MENTAL_SEX = {"Linear", "Holistic"}
ENUM_DRIVER = {"Action", "Decision"}
ENUM_LIMIT = {"Timelock", "Optionlock"}
ENUM_OUTCOME = {"Success", "Failure"}
ENUM_JUDGMENT = {"Good", "Bad"}
PLACEHOLDER = "<PLACEHOLDER>"


def _diag(path: Path, code: str, msg: str, tier: str = "WARN") -> str:
    return f"{path}::{tier}:{code}:{msg}"


# ───────── H1-H4 (Throughline structure + Class pairing) ─────────────────────


def _check_h1(path: Path, narrative: dict[str, Any], idx: int) -> list[str]:
    tl = narrative.get("throughlines")
    if not isinstance(tl, dict):
        return [_diag(path, "H1.THROUGHLINE_COUNT",
                     f"narrative[{idx}].throughlines missing or not a mapping")]
    if len(tl) != 4:
        return [_diag(path, "H1.THROUGHLINE_COUNT",
                     f"narrative[{idx}] has {len(tl)} throughlines, expected 4")]
    missing = set(THROUGHLINE_KEYS) - set(tl.keys())
    if missing:
        return [_diag(path, "H1.THROUGHLINE_COUNT",
                     f"narrative[{idx}] missing throughlines: {sorted(missing)}")]
    return []


def _classes_of(narrative: dict[str, Any]) -> dict[str, str]:
    tl = narrative.get("throughlines", {})
    return {slot: (entry.get("class") if isinstance(entry, dict) else None)
            for slot, entry in tl.items() if isinstance(entry, dict)}


def _check_h2(path: Path, narrative: dict[str, Any], idx: int) -> list[str]:
    classes = [c for c in _classes_of(narrative).values()
               if isinstance(c, str) and c != PLACEHOLDER]
    if not classes:
        return []  # WIP
    seen = set(classes)
    if len(seen) != len(classes):
        # Some class duplicated.
        dups = sorted(c for c in seen if classes.count(c) > 1)
        return [_diag(path, "H2.CLASS_UNIQUENESS",
                     f"narrative[{idx}] has duplicate Class assignment(s): {dups}")]
    # If all 4 are assigned, they must cover the full set.
    if len(classes) == 4 and seen != ALL_CLASSES:
        unexpected = sorted(seen - ALL_CLASSES)
        missing = sorted(ALL_CLASSES - seen)
        return [_diag(path, "H2.CLASS_UNIQUENESS",
                     f"narrative[{idx}] does not use all 4 canonical Classes: "
                     f"missing={missing}, unexpected={unexpected}")]
    return []


def _check_h3(path: Path, narrative: dict[str, Any], idx: int) -> list[str]:
    classes = _classes_of(narrative)
    mc, ic = classes.get("mc"), classes.get("ic")
    if (isinstance(mc, str) and isinstance(ic, str)
            and mc != PLACEHOLDER and ic != PLACEHOLDER):
        if COMPLEMENT_PAIRS.get(mc) != ic:
            return [_diag(path, "H3.MC_IC_COMPLEMENT",
                         f"narrative[{idx}] MC/IC Classes not complementary: "
                         f"mc={mc}, ic={ic} "
                         f"(complement of {mc} is {COMPLEMENT_PAIRS.get(mc, '?')})")]
    return []


def _check_h4(path: Path, narrative: dict[str, Any], idx: int) -> list[str]:
    classes = _classes_of(narrative)
    os_cls, ss_cls = classes.get("os"), classes.get("ss")
    if (isinstance(os_cls, str) and isinstance(ss_cls, str)
            and os_cls != PLACEHOLDER and ss_cls != PLACEHOLDER):
        if COMPLEMENT_PAIRS.get(os_cls) != ss_cls:
            return [_diag(path, "H4.OS_SS_COMPLEMENT",
                         f"narrative[{idx}] OS/SS Classes not complementary: "
                         f"os={os_cls}, ss={ss_cls} "
                         f"(complement of {os_cls} is {COMPLEMENT_PAIRS.get(os_cls, '?')})")]
    return []


# ───────── H5-H8 — deferred (require dramatica-nav ontology) ─────────────────


def _deferred_info(path: Path, idx: int) -> list[str]:
    return [_diag(path, "H5-H8.DEFERRED",
                 f"narrative[{idx}] H5/H6/H7/H8 (Concern/Quad/Dynamic-Pair) "
                 f"validation requires tools/dramatica-nav/nav.py integration; "
                 f"deferred to Task 085 ERROR-promotion follow-up",
                 tier="INFO")]


# ───────── H9-H12 (Dynamic enum checks) ──────────────────────────────────────


def _check_enum(path: Path, value: Any, code: str, valid: set[str],
                label: str, idx: int) -> list[str]:
    if value is None or value == PLACEHOLDER:
        return []  # WIP
    if value not in valid:
        return [_diag(path, code,
                     f"narrative[{idx}].dynamics.{label}={value!r} "
                     f"not in {sorted(valid)}")]
    return []


def _check_h9(path: Path, narrative: dict[str, Any], idx: int) -> list[str]:
    dyn = narrative.get("dynamics", {})
    if not isinstance(dyn, dict):
        return []
    return _check_enum(path, dyn.get("plot_driver"),
                       "H9.DRIVER_ENUM", ENUM_DRIVER, "plot_driver", idx)


def _check_h10(path: Path, narrative: dict[str, Any], idx: int) -> list[str]:
    dyn = narrative.get("dynamics", {})
    if not isinstance(dyn, dict):
        return []
    return _check_enum(path, dyn.get("plot_limit"),
                       "H10.LIMIT_ENUM", ENUM_LIMIT, "plot_limit", idx)


def _check_h11(path: Path, narrative: dict[str, Any], idx: int) -> list[str]:
    dyn = narrative.get("dynamics", {})
    if not isinstance(dyn, dict):
        return []
    return (
        _check_enum(path, dyn.get("outcome"),
                    "H11.OUTCOME_ENUM", ENUM_OUTCOME, "outcome", idx)
        + _check_enum(path, dyn.get("judgment"),
                      "H11.JUDGMENT_ENUM", ENUM_JUDGMENT, "judgment", idx)
    )


def _check_h12(path: Path, narrative: dict[str, Any], idx: int) -> list[str]:
    dyn = narrative.get("dynamics", {})
    if not isinstance(dyn, dict):
        return []
    return (
        _check_enum(path, dyn.get("mc_approach"),
                    "H12.APPROACH_ENUM", ENUM_APPROACH, "mc_approach", idx)
        + _check_enum(path, dyn.get("mc_mental_sex"),
                      "H12.MENTAL_SEX_ENUM", ENUM_MENTAL_SEX, "mc_mental_sex", idx)
    )


# ───────── Driver / orchestration ────────────────────────────────────────────


def diagnostics_for(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{path}::WARN:HARD_RULES.READ:cannot read file ({exc})"]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return [f"{path}::WARN:HARD_RULES.YAML:parse error ({exc})"]
    if not isinstance(data, dict):
        return []
    arch = data.get("architecture")
    if not isinstance(arch, dict):
        return []
    narratives = arch.get("narratives")
    if not isinstance(narratives, list):
        return []

    diags: list[str] = []
    for idx, narrative in enumerate(narratives):
        if not isinstance(narrative, dict):
            continue
        diags.extend(_check_h1(path, narrative, idx))
        diags.extend(_check_h2(path, narrative, idx))
        diags.extend(_check_h3(path, narrative, idx))
        diags.extend(_check_h4(path, narrative, idx))
        diags.extend(_deferred_info(path, idx))
        diags.extend(_check_h9(path, narrative, idx))
        diags.extend(_check_h10(path, narrative, idx))
        diags.extend(_check_h11(path, narrative, idx))
        diags.extend(_check_h12(path, narrative, idx))
    return diags


def _iter_architecture_files(target: Path) -> Iterable[Path]:
    if target.is_file():
        yield target
        return
    if target.is_dir():
        for pattern in ("architecture.yaml", "*-architecture.yaml",
                        "example-architecture.yaml"):
            for p in sorted(target.rglob(pattern)):
                yield p


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="check-hard-rules",
        description=(
            "Advisory linter for Dramatica Hard Rules H1-H12 against "
            "architecture.yaml (skills/novel-architect-structure/methods/"
            "validation/hard-rules.md). H1-H4 + H9-H12 fully mechanical; "
            "H5-H8 deferred (ontology-dependent)."
        ),
    )
    parser.add_argument("paths", nargs="*", help="architecture.yaml files or dirs")
    args = parser.parse_args(argv)

    targets = [Path(p) for p in args.paths]
    diags: list[str] = []
    seen: set[Path] = set()
    for t in targets:
        if not t.exists():
            print(
                f"check-hard-rules: warning: path does not exist: {t}",
                file=sys.stderr,
            )
            continue
        for f in _iter_architecture_files(t):
            if f in seen:
                continue
            seen.add(f)
            diags.extend(diagnostics_for(f))

    for d in diags:
        print(d)

    # WARN-tier counts toward the non-zero exit; INFO-tier (deferred) does not.
    warn_count = sum(1 for d in diags if "::WARN:" in d)
    info_count = sum(1 for d in diags if "::INFO:" in d)
    print(
        f"check-hard-rules: {warn_count} WARN + {info_count} INFO diagnostic(s) "
        f"across {len(seen)} architecture file(s).",
        file=sys.stderr,
    )
    return 2 if warn_count else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
