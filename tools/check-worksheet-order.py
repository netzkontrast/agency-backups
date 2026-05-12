#!/usr/bin/env python3
"""check-worksheet-order — validate Phase 2 storyform worksheet order in architecture.yaml.

Spec anchor:
    skills/novel-architect-structure/methods/storyform/worksheet-loop.md §1–§3 (Task 072)

Target: `architecture.yaml` files produced by novel-architect Phase 2.

Checks (all WARN-tier — advisory; gates remain in the orchestrator):
  WORKSHEET.THROUGHLINE_COUNT  — narratives[].throughlines lists exactly 4
                                  entries (os, mc, ic, ss).
  WORKSHEET.THROUGHLINE_KEYS    — the 4 keys are exactly {os, mc, ic, ss}.
  WORKSHEET.NAME_EMPTY          — each throughline.name is non-empty
                                  (PLACEHOLDER is allowed during work-in-progress).
  WORKSHEET.AUDIT_INCOMPLETE    — worksheet_audit step_0..step_7 / validation_pass
                                  must all be true for an `approved: true` architecture
                                  (step_8 may be false — Step 8 is optional).
  WORKSHEET.AUDIT_GAP           — if step_N is true, step_(N-1) MUST also be true
                                  (worksheet enforces sequential completion).
  WORKSHEET.CLASS_PAIR          — MC/IC and OS/SS Class pairs are complementary
                                  (Universe↔Mind, Physics↔Psychology).

Exit codes:
    0 — clean
    1 — usage error
    2 — at least one WARN diagnostic
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, Any

import yaml  # type: ignore


THROUGHLINE_KEYS = {"os", "mc", "ic", "ss"}
# Class complementary pairs per Dramatica's Mind/Universe ↔ Physics/Psychology
# axis (00-storyform-validation.md H3/H4).
COMPLEMENT_PAIRS = {
    "Universe": "Mind",
    "Mind": "Universe",
    "Physics": "Psychology",
    "Psychology": "Physics",
}
AUDIT_REQUIRED = [
    "step_0_intent_loaded",
    "step_1_throughlines_named",
    "step_2_classes_assigned",
    "step_3_character_dynamics_set",
    "step_4_plot_dynamics_set",
    "step_5_story_points_set",
    "step_6_crucial_element_set",
    "step_7_signposts_set",
    "validation_pass",
]


def _diag(path: Path, code: str, msg: str) -> str:
    return f"{path}::WARN:WORKSHEET.{code}:{msg}"


def _check_throughlines(path: Path, narrative: dict[str, Any], idx: int) -> list[str]:
    diags: list[str] = []
    tl = narrative.get("throughlines")
    if not isinstance(tl, dict):
        diags.append(_diag(path, "THROUGHLINE_COUNT",
                          f"narrative[{idx}].throughlines missing or not a dict"))
        return diags
    keys = set(tl.keys())
    if keys != THROUGHLINE_KEYS:
        diags.append(_diag(path, "THROUGHLINE_KEYS",
                          f"narrative[{idx}].throughlines keys {sorted(keys)} != "
                          f"{sorted(THROUGHLINE_KEYS)}"))
        return diags
    if len(tl) != 4:
        diags.append(_diag(path, "THROUGHLINE_COUNT",
                          f"narrative[{idx}].throughlines has {len(tl)} entries, expected 4"))
    for slot, entry in tl.items():
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name.strip():
            diags.append(_diag(path, "NAME_EMPTY",
                              f"narrative[{idx}].throughlines.{slot}.name is empty"))
    return diags


def _check_class_pairs(path: Path, narrative: dict[str, Any], idx: int) -> list[str]:
    diags: list[str] = []
    tl = narrative.get("throughlines")
    if not isinstance(tl, dict):
        return diags
    classes = {slot: (entry.get("class") if isinstance(entry, dict) else None)
               for slot, entry in tl.items()}
    # MC/IC pair
    mc_cls, ic_cls = classes.get("mc"), classes.get("ic")
    if isinstance(mc_cls, str) and isinstance(ic_cls, str):
        # PLACEHOLDER values are allowed during work-in-progress.
        if (mc_cls != "<PLACEHOLDER>" and ic_cls != "<PLACEHOLDER>"
                and COMPLEMENT_PAIRS.get(mc_cls) != ic_cls):
            diags.append(_diag(path, "CLASS_PAIR",
                              f"narrative[{idx}] MC/IC Classes not complementary: "
                              f"mc={mc_cls}, ic={ic_cls} "
                              f"(expected complement of mc: {COMPLEMENT_PAIRS.get(mc_cls, '?')})"))
    # OS/SS pair
    os_cls, ss_cls = classes.get("os"), classes.get("ss")
    if isinstance(os_cls, str) and isinstance(ss_cls, str):
        if (os_cls != "<PLACEHOLDER>" and ss_cls != "<PLACEHOLDER>"
                and COMPLEMENT_PAIRS.get(os_cls) != ss_cls):
            diags.append(_diag(path, "CLASS_PAIR",
                              f"narrative[{idx}] OS/SS Classes not complementary: "
                              f"os={os_cls}, ss={ss_cls} "
                              f"(expected complement of os: {COMPLEMENT_PAIRS.get(os_cls, '?')})"))
    return diags


def _check_worksheet_audit(path: Path, data: dict[str, Any]) -> list[str]:
    diags: list[str] = []
    audit = data.get("worksheet_audit")
    if not isinstance(audit, dict):
        return diags  # Audit is optional in WIP; presence not required pre-approval.

    if data.get("approved") is True:
        # Approved architectures MUST have all required steps satisfied.
        for step in AUDIT_REQUIRED:
            if audit.get(step) is not True:
                diags.append(_diag(path, "AUDIT_INCOMPLETE",
                                  f"worksheet_audit.{step} is not true on an "
                                  f"approved architecture (worksheet steps 0–7 + "
                                  f"validation MUST be true; step 8 optional)"))

    # Sequential gap check — if step_N is true, all earlier required steps must
    # also be true. This catches authors who set step_7=true while step_3=false.
    for i, step in enumerate(AUDIT_REQUIRED):
        if audit.get(step) is True:
            for earlier in AUDIT_REQUIRED[:i]:
                if audit.get(earlier) is not True:
                    diags.append(_diag(path, "AUDIT_GAP",
                                      f"worksheet_audit.{step} is true but earlier "
                                      f"step {earlier!r} is not — worksheet enforces "
                                      f"sequential completion"))
                    break  # One gap per step is enough
    return diags


def diagnostics_for(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{path}::WARN:WORKSHEET.READ:cannot read file ({exc})"]

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return [f"{path}::WARN:WORKSHEET.YAML:parse error ({exc})"]

    if not isinstance(data, dict):
        return [f"{path}::WARN:WORKSHEET.YAML:top-level is not a mapping"]

    diags: list[str] = []
    arch = data.get("architecture")
    if not isinstance(arch, dict):
        return diags  # Not a Phase 2 architecture.yaml — quietly skip.

    narratives = arch.get("narratives")
    if not isinstance(narratives, list):
        diags.append(_diag(path, "STRUCTURE",
                          "architecture.narratives is missing or not a list"))
        return diags

    for idx, narrative in enumerate(narratives):
        if not isinstance(narrative, dict):
            continue
        diags.extend(_check_throughlines(path, narrative, idx))
        diags.extend(_check_class_pairs(path, narrative, idx))

    diags.extend(_check_worksheet_audit(path, data))
    return diags


def _iter_architecture_files(target: Path) -> Iterable[Path]:
    if target.is_file():
        yield target
        return
    if target.is_dir():
        # Match common naming variants used by novel-architect Phase 2.
        for pattern in ("architecture.yaml", "*-architecture.yaml",
                        "example-architecture.yaml"):
            for p in sorted(target.rglob(pattern)):
                yield p


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="check-worksheet-order",
        description=(
            "Advisory linter for Phase 2 storyform worksheet order in "
            "architecture.yaml (skills/novel-architect-structure/methods/"
            "storyform/worksheet-loop.md)."
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
                f"check-worksheet-order: warning: path does not exist: {t}",
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
    print(
        f"check-worksheet-order: {len(diags)} WARN diagnostic(s) "
        f"across {len(seen)} architecture file(s).",
        file=sys.stderr,
    )
    return 2 if diags else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
