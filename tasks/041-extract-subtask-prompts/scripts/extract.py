#!/usr/bin/env python3
"""
Task 041 — Extract subtask Execution Briefs to /prompts/<slug>/.

Reads the 35 subtask files under tasks/03[2-9]*/subtasks/[0-9]*.md, generates
one /prompts/<slug>/{brief.md, prompt.md, readme.md} scaffold per subtask,
replaces each subtask body with a thin pointer to the prompt, and appends the
prompt slug to the parent task's task_uses_prompts list.

Idempotent: re-running on an already-extracted subtask is a no-op (or a
re-scaffold, controlled by --force).

Driven by tasks/041-extract-subtask-prompts/slug-manifest.md (informational —
the actual mapping is reconstructed from filenames).
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
PROMPTS_ROOT = REPO_ROOT / "prompts"
TASKS_ROOT = REPO_ROOT / "tasks"

PARENT_TASK_DIRS = [
    "032-agents-spec-integration",
    "033-task-spec-integration",
    "034-prompt-spec-integration",
    "035-research-spec-integration",
    "036-folders-spec-integration",
    "037-pre-commit-spec-integration",
    "038-frustrated-spec-integration",
    "039-maintenance-spec-integration",
]


# ---------- frontmatter helpers (minimal, stdlib-only) ----------

FM_FENCE = "---"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (fm_dict, body). Tolerates list values via simple YAML subset."""
    if not text.startswith(FM_FENCE + "\n"):
        return {}, text
    end = text.find("\n" + FM_FENCE + "\n", len(FM_FENCE) + 1)
    if end == -1:
        return {}, text
    fm_block = text[len(FM_FENCE) + 1 : end]
    body = text[end + len(FM_FENCE) + 2 :]
    fm: dict = {}
    cur_list_key: str | None = None
    for raw in fm_block.splitlines():
        if not raw.strip():
            continue
        if raw.startswith("  - "):
            if cur_list_key is None:
                continue
            fm[cur_list_key].append(raw[4:].strip())
            continue
        cur_list_key = None
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$", raw)
        if not m:
            continue
        k, v = m.group(1), m.group(2).rstrip()
        if v == "":
            cur_list_key = k
            fm[k] = []
            continue
        if v == "[]":
            fm[k] = []
            continue
        # strip outer quotes
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            v = v[1:-1]
        fm[k] = v
    return fm, body


def serialise_frontmatter(fm: dict) -> str:
    """Round-trip serialisation matching the repo's prevailing style."""
    out = [FM_FENCE]
    for k, v in fm.items():
        if isinstance(v, list):
            if not v:
                out.append(f"{k}: []")
            else:
                out.append(f"{k}:")
                for item in v:
                    out.append(f"  - {item}")
        else:
            out.append(f"{k}: {v}")
    out.append(FM_FENCE)
    return "\n".join(out) + "\n"


# ---------- body section extraction ----------

def split_sections(body: str) -> dict[str, str]:
    """Split body into {h2_heading_text: section_body}. Heading text returned
    verbatim (with surrounding whitespace stripped); section body excludes the
    heading line. Order is preserved via insertion order."""
    sections: dict[str, str] = {}
    cur_heading: str | None = None
    cur_lines: list[str] = []
    in_fence = False
    fence_marker: str | None = None
    for line in body.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif fence_marker == marker:
                in_fence = False
                fence_marker = None
            cur_lines.append(line)
            continue
        if not in_fence and line.startswith("## "):
            if cur_heading is not None:
                sections[cur_heading] = "\n".join(cur_lines).strip("\n")
            cur_heading = line[3:].strip()
            cur_lines = []
            continue
        cur_lines.append(line)
    if cur_heading is not None:
        sections[cur_heading] = "\n".join(cur_lines).strip("\n")
    return sections


def get_section(sections: dict[str, str], *names: str) -> str | None:
    """Return the body of the first matching section name (case-insensitive,
    trailing-punctuation-tolerant)."""
    norm = {k.casefold().rstrip(": —–-"): v for k, v in sections.items()}
    for name in names:
        v = norm.get(name.casefold().rstrip(": —–-"))
        if v is not None:
            return v
    return None


def extract_lead_metadata(body: str) -> tuple[dict[str, str], str]:
    """Strip leading **Key:** lines (Executor / Parallelism / Insertion point) from
    the body before the first ## section. Returns (metadata_dict, remaining_body).
    The remaining_body still contains the title H1 and the rest of the file."""
    md: dict[str, str] = {}
    lines = body.splitlines()
    i = 0
    # skip past the H1 line and any blank lines
    seen_h1 = False
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("# ") and not seen_h1:
            seen_h1 = True
            i += 1
            continue
        if not seen_h1:
            i += 1
            continue
        if not ln.strip():
            i += 1
            continue
        m = re.match(r"^\*\*([A-Za-z][A-Za-z\- ]*?):\*\*\s*(.*)$", ln)
        if m:
            md[m.group(1).strip()] = m.group(2).strip()
            i += 1
            continue
        if ln.startswith("## "):
            break
        # any other content terminates the metadata block
        break
    return md, body


def fenced_to_text(s: str) -> str:
    """Strip a single ```text ... ``` (or ```...```) fence wrapper if present."""
    s = s.strip()
    m = re.match(r"^```[a-zA-Z0-9_-]*\n(.*)\n```$", s, flags=re.DOTALL)
    if m:
        return m.group(1).rstrip()
    return s


# ---------- ensure ordered list ≥ N items ----------

def lines_starting_with_dash(s: str) -> list[str]:
    out = []
    for ln in s.splitlines():
        m = re.match(r"^\s*[-*]\s+(.*)$", ln)
        if m:
            out.append(m.group(1).rstrip())
    return out


def numbered_items(s: str) -> list[str]:
    """Extract numbered list items, preserving multi-line continuations.
    A continuation line is any indented (≥2-space) non-numbered line, or any
    further line of the current item before the next `<n>. ` marker."""
    out: list[str] = []
    cur: list[str] | None = None
    for ln in s.splitlines():
        m = re.match(r"^\s*\d+\.\s+(.*)$", ln)
        if m:
            if cur is not None:
                out.append(" ".join(cur).strip())
            cur = [m.group(1).rstrip()]
            continue
        if cur is not None:
            stripped = ln.strip()
            if not stripped:
                # blank line ends the item only if followed by a non-continuation
                continue
            if re.match(r"^\s+\S", ln):  # indented continuation
                cur.append(stripped)
                continue
            # non-indented non-numbered line ends the list
            out.append(" ".join(cur).strip())
            cur = None
    if cur is not None:
        out.append(" ".join(cur).strip())
    return out


_RFC2119_RE = re.compile(r"\b(MUST(?:\s+NOT)?|SHOULD(?:\s+NOT)?|MAY|REQUIRED|SHALL(?:\s+NOT)?)\b")


_VERB_LOWERCASEABLE = {
    "Author", "Build", "Check", "Commit", "Confirm", "Create", "Define",
    "Delete", "Document", "Edit", "Emit", "Enforce", "Ensure", "Execute",
    "File", "Fix", "Generate", "Implement", "Insert", "Land", "Migrate",
    "Open", "Patch", "Produce", "Push", "Read", "Remove", "Rename", "Render",
    "Replace", "Run", "Scaffold", "Select", "Set", "Ship", "Skip", "Stage",
    "Submit", "Sync", "Update", "Use", "Validate", "Verify", "Write",
}


def ensure_rfc2119(item: str) -> str:
    """Return the item verbatim if it already carries an RFC-2119 keyword,
    otherwise prepend `The agent MUST ` (or convert leading negative
    imperatives to `MUST NOT`). Preserves the item's substantive content
    without lossy case normalisation of proper-noun labels."""
    cleaned = item.strip()
    cleaned = re.sub(r"^[Ss]atisfy\s+acceptance\s+criterion:\s*", "", cleaned)
    cleaned = re.sub(r"^[Tt]he\s+agent\s+", "", cleaned)
    if not cleaned:
        return "The agent MUST execute the parent subtask's instructions verbatim."
    if _RFC2119_RE.search(cleaned):
        return cleaned

    # Negative imperatives: "Do NOT X" / "DO NOT X" / "Don't X" → "MUST NOT X".
    m = re.match(r"^(?:do\s+not|don'?t)\s+(.*)$", cleaned, flags=re.IGNORECASE)
    if m:
        return f"The agent MUST NOT {m.group(1).rstrip('.').strip()}."

    # Leading common imperative verb in title case → lowercase first letter.
    first_word_match = re.match(r"^(\w+)(\b.*)$", cleaned, flags=re.S)
    if first_word_match and first_word_match.group(1) in _VERB_LOWERCASEABLE:
        verb = first_word_match.group(1).lower()
        rest = first_word_match.group(2)
        return f"The agent MUST {verb}{rest}"

    # Otherwise: prefix with "MUST execute the following instruction:" so the
    # original (often a label like 'Phase 2: …') reads as the object of MUST.
    return f"The agent MUST execute the following instruction: {cleaned}"


def to_unordered_list(items: list[str]) -> str:
    if not items:
        return "- (no items)"
    return "\n".join(f"- {it}" for it in items)


def to_ordered_list(items: list[str]) -> str:
    if not items:
        return "1. (no items)"
    return "\n".join(f"{i+1}. {it}" for i, it in enumerate(items))


# ---------- core build per-subtask ----------

def parent_task_slug(parent_dir: Path) -> str:
    fm, _ = parse_frontmatter((parent_dir / "task.md").read_text())
    return str(fm.get("slug") or "")


def parent_task_id(parent_dir: Path) -> str:
    fm, _ = parse_frontmatter((parent_dir / "task.md").read_text())
    return str(fm.get("task_id") or "")


def subtask_label(filename: str) -> str:
    """Derive ST-N from filename '01-...' → 'ST-1' (no zero-pad)."""
    m = re.match(r"^(\d+)-", filename)
    if not m:
        return "ST-?"
    return f"ST-{int(m.group(1))}"


def prompt_slug_from_subtask(filename: str) -> str:
    return re.sub(r"^\d+-", "", filename[:-3] if filename.endswith(".md") else filename)


def derive_summary(sections: dict[str, str], h1: str, prompt_slug: str) -> str:
    """One-line summary, 200 chars max."""
    goal = get_section(sections, "Goal") or ""
    first_para = goal.strip().split("\n\n")[0].strip()
    first_para = re.sub(r"\s+", " ", first_para)
    if not first_para:
        first_para = h1
    if len(first_para) > 240:
        first_para = first_para[:237] + "..."
    # Escape double-quotes for YAML.
    first_para = first_para.replace('"', "'")
    return first_para


def build_brief_md(
    *,
    prompt_slug: str,
    parent_dir_name: str,
    parent_slug: str,
    subtask_filename: str,
    st_label: str,
    h1_title: str,
    sections: dict[str, str],
    lead_meta: dict[str, str],
    today: str,
) -> str:
    fm = {
        "type": "note",
        "status": "active",
        "slug": f"{prompt_slug}-brief",
        "summary": f'"Brief for prompt {prompt_slug} — extracted from tasks/{parent_dir_name}/subtasks/{subtask_filename} per Task 041 (PR #70 review C.3 audit-graph repair)."',
        "created": today,
        "updated": today,
    }
    fm_text = serialise_frontmatter(fm)

    goal = get_section(sections, "Goal") or "(no Goal section in source)"
    falsif = get_section(sections, "Falsification") or "(none stated)"
    inputs = get_section(sections, "Inputs") or "(none listed)"
    accept = get_section(sections, "Acceptance Criteria", "Acceptance") or "(none stated)"
    deps = get_section(sections, "Dependencies") or "(none stated)"
    effort = get_section(sections, "Estimated Effort", "Effort") or "(unspecified)"

    parallelism = lead_meta.get("Parallelism", "(unspecified)")
    executor = lead_meta.get("Executor", "main-agent")
    insertion = lead_meta.get("Insertion point", "")

    body_lines: list[str] = [
        "",
        f"# Brief — {h1_title}",
        "",
        "## Raw User Request",
        "",
        f"> Extract the inlined Execution Brief from `tasks/{parent_dir_name}/subtasks/{subtask_filename}` ({st_label}) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).",
        "",
        "## Target Audience",
        "",
        f"The dispatched executor for [Task {parent_dir_name.split('-', 1)[0]} `{parent_slug}`](../../tasks/{parent_dir_name}/task.md), specifically subtask {st_label} ({subtask_filename}). Default executor: **{executor}**.",
        "",
        "## Intended Model / Agent",
        "",
        "Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).",
        "",
        "## Use-Case Context",
        "",
        f"This prompt drives subtask {st_label} of [Task {parent_slug}](../../tasks/{parent_dir_name}/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.",
        "",
        f"**Parallelism:** {parallelism}",
    ]
    if insertion:
        body_lines.append("")
        body_lines.append(f"**Insertion point:** {insertion}")
    body_lines.extend([
        "",
        "## Goal (from subtask)",
        "",
        goal,
        "",
        "## Falsification (from subtask)",
        "",
        falsif,
        "",
        "## Inputs (from subtask)",
        "",
        inputs,
        "",
        "## Acceptance Criteria (from subtask)",
        "",
        accept,
        "",
        "## Dependencies (from subtask)",
        "",
        deps,
        "",
        "## Estimated Effort (from subtask)",
        "",
        effort,
        "",
    ])
    return fm_text + "\n".join(body_lines).rstrip() + "\n"


def build_prompt_md(
    *,
    prompt_slug: str,
    parent_slug: str,
    parent_dir_name: str,
    subtask_filename: str,
    st_label: str,
    h1_title: str,
    sections: dict[str, str],
    lead_meta: dict[str, str],
    today: str,
) -> str:
    summary = derive_summary(sections, h1_title, prompt_slug)
    fm = {
        "type": "prompt",
        "status": "active",
        "slug": prompt_slug,
        "summary": f'"{summary}"',
        "created": today,
        "updated": today,
        "prompt_kind": "task-spec",
        "prompt_framework": "RISEN+ReAct",
        "prompt_target_agent": '"Claude Code"',
        "prompt_relates_to_task": parent_slug,
    }
    fm_text = serialise_frontmatter(fm)

    goal = (get_section(sections, "Goal") or "").strip()
    inputs_section = (get_section(sections, "Inputs") or "").strip()
    accept = (get_section(sections, "Acceptance Criteria", "Acceptance") or "").strip()
    deps = (get_section(sections, "Dependencies") or "").strip()
    falsif = (get_section(sections, "Falsification") or "").strip()
    eb = (get_section(sections, "Execution Brief") or "").strip()
    eb_text = fenced_to_text(eb) if eb else ""

    # Inputs: ensure unordered list with ≥1 item.
    input_items = lines_starting_with_dash(inputs_section)
    if not input_items:
        input_items = [f"`tasks/{parent_dir_name}/subtasks/{subtask_filename}` — the parent subtask file (lifted verbatim into this prompt's `brief.md`)."]
    input_items.append(f"`tasks/{parent_dir_name}/task.md` — parent task chain-level context.")

    # Steps: RISEN-native ordered list. Each step carries an RFC-2119 keyword and
    # a discrete deliverable; per PROMPT.md §5 (Self-Containedness, RFC 2119
    # Normativity, Deliverable Lock, Failure Handling). Two phases:
    #   (a) Implementation steps — derived from the Execution Brief's own
    #       numbered items (if present) or from Acceptance Criteria when there
    #       is no explicit brief. Multi-line continuations are preserved.
    #   (b) Verification + closure steps — uniform across every prompt, citing
    #       the Acceptance Criteria authoritatively from `brief.md`.
    impl_steps: list[str] = []
    if eb_text:
        eb_items = numbered_items(eb_text)
        # Pull a leading prose preamble (if any) before the first numbered item.
        first_marker = re.search(r"^\s*\d+\.\s+", eb_text, flags=re.M)
        preamble = ""
        if first_marker:
            preamble = eb_text[: first_marker.start()].strip()
        elif eb_text.strip():
            preamble = eb_text.strip()
        if preamble:
            impl_steps.append(
                "The agent MUST treat the following preamble as authoritative orientation before executing any subsequent step: "
                + re.sub(r"\s+", " ", preamble).strip()
            )
        for it in eb_items:
            impl_steps.append(ensure_rfc2119(it))
    if not impl_steps:
        ac_items_for_impl = numbered_items(accept) or lines_starting_with_dash(accept)
        for it in ac_items_for_impl:
            impl_steps.append(
                "The agent MUST produce the artefact required by acceptance criterion: " + it
            )

    verification_steps: list[str] = [
        f"The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.",
        f"The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.",
        f"The agent SHOULD author or update `tasks/{parent_dir_name}/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.",
        f"The agent MUST commit with a message that names `Task {parent_dir_name.split('-', 1)[0]} {st_label}` in its trailer; the agent MUST NOT push (the maintainer pushes after review).",
    ]

    steps = impl_steps + verification_steps
    if len(steps) < 3:
        steps.append(
            "The agent MUST confirm the parent task's `task_uses_prompts` list still names this prompt's slug after commit (reciprocity invariant)."
        )

    # Expectations: unordered list of acceptance items + commit/lint expectations.
    exp_items = numbered_items(accept) or lines_starting_with_dash(accept)
    if not exp_items:
        exp_items = ["All Acceptance Criteria from the parent subtask brief are satisfied."]
    exp_items.append("`tools/check-governance.sh` exits 0 on the produced commit.")
    exp_items.append(f"Commit message follows the parent task's convention; the commit cites `Task {parent_dir_name.split('-', 1)[0]} {st_label}` in its trailer.")

    # Constraints: unordered list of MUST/SHOULD items derived from Falsification + Dependencies + repo invariants.
    constraint_items: list[str] = []
    if deps:
        for ln in deps.splitlines():
            lns = ln.strip()
            if lns:
                constraint_items.append(f"Dependency: {lns}")
    if falsif:
        # Falsification is usually a paragraph; convert to a single MUST NOT.
        falsif_one_line = re.sub(r"\s+", " ", falsif).strip()
        constraint_items.append(f"MUST NOT trigger the subtask's Falsification clause: {falsif_one_line}")
    constraint_items.extend([
        "MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.",
        "MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.",
        "SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.",
    ])

    parallelism = lead_meta.get("Parallelism", "(unspecified)")
    executor = lead_meta.get("Executor", "main-agent")

    role_line = (
        f"You are the **{executor}** dispatched to execute subtask "
        f"{st_label} of [Task {parent_slug}](../../tasks/{parent_dir_name}/task.md). "
        f"Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); "
        f"you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`."
    )

    body: list[str] = [
        "",
        f"# {h1_title} — Task-Spec Prompt",
        "",
        "## Framework",
        "",
        f"RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.",
        "",
        "## R — Role",
        "",
        role_line,
        "",
        f"**Parallelism:** {parallelism}.",
        "",
        "## I — Input",
        "",
        to_unordered_list(input_items),
        "",
        "## S — Steps",
        "",
        to_ordered_list(steps),
        "",
        "## E — Expectations",
        "",
        to_unordered_list(exp_items),
        "",
        "## Constraints",
        "",
        to_unordered_list(constraint_items),
        "",
    ]
    return fm_text + "\n".join(body).rstrip() + "\n"


def build_readme_md(
    *,
    prompt_slug: str,
    parent_slug: str,
    parent_dir_name: str,
    st_label: str,
    h1_title: str,
    today: str,
) -> str:
    fm = {
        "type": "index",
        "status": "active",
        "slug": f"{prompt_slug}-prompt-readme",
        "summary": f'"Index for prompt {prompt_slug} — task-spec prompt that drives subtask {st_label} of Task {parent_slug}. Extracted by Task 041 from the inlined subtask brief."',
        "created": today,
        "updated": today,
    }
    fm_text = serialise_frontmatter(fm)
    body = (
        f"\n# Prompt — {prompt_slug}\n"
        f"\n- [`brief.md`](./brief.md) — Subtask orientation: Goal, Falsification, Inputs, Acceptance, Dependencies, Effort.\n"
        f"- [`prompt.md`](./prompt.md) — The executable RISEN+ReAct task-spec prompt.\n"
        f"\n## Usage\n"
        f"\nExecute via subtask {st_label} of [Task `{parent_slug}`](../../tasks/{parent_dir_name}/task.md). The prompt's `prompt_relates_to_task` reciprocity binds it to the parent task's `task_uses_prompts` list.\n"
        f"\n## Source\n"
        f"\nExtracted by [Task 041](../../tasks/041-extract-subtask-prompts/task.md) from the inlined subtask brief. The original subtask file is now a thin pointer to this prompt; its body content has migrated to [`brief.md`](./brief.md) and [`prompt.md`](./prompt.md).\n"
    )
    return fm_text + body


def build_subtask_pointer(
    *,
    original_text: str,
    h1_title: str,
    prompt_slug: str,
    parent_dir_name: str,
    st_label: str,
    lead_meta: dict[str, str],
    today: str,
) -> str:
    """Build the new subtask body — a thin pointer that retains only:
    - L1 frontmatter (preserved verbatim from original; updated date bumped)
    - H1 title
    - Executor / Parallelism / Insertion point metadata lines
    - One-line Prompt cross-reference link
    """
    # Line-based frontmatter rewrite preserving original quoting.
    if original_text.startswith(FM_FENCE + "\n"):
        end = original_text.find("\n" + FM_FENCE + "\n", len(FM_FENCE) + 1)
    else:
        end = -1
    if end == -1:
        fm_text = ""
    else:
        fm_block = original_text[len(FM_FENCE) + 1 : end]
        out_lines: list[str] = []
        saw_updated = False
        for raw in fm_block.splitlines():
            if raw.startswith("updated:"):
                out_lines.append(f"updated: {today}")
                saw_updated = True
                continue
            out_lines.append(raw)
        if not saw_updated:
            out_lines.append(f"updated: {today}")
        fm_text = FM_FENCE + "\n" + "\n".join(out_lines) + "\n" + FM_FENCE + "\n"

    parts = [
        "",
        f"# {h1_title}",
        "",
    ]
    if "Executor" in lead_meta:
        parts.append(f"**Executor:** {lead_meta['Executor']}")
    if "Insertion point" in lead_meta:
        parts.append(f"**Insertion point:** {lead_meta['Insertion point']}")
    if "Parallelism" in lead_meta:
        parts.append("")
        parts.append(f"**Parallelism:** {lead_meta['Parallelism']}")
    parts.extend([
        "",
        f"**Prompt:** [`/prompts/{prompt_slug}/prompt.md`](../../../prompts/{prompt_slug}/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/{prompt_slug}/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).",
        "",
    ])
    return fm_text + "\n".join(parts).rstrip() + "\n"


def update_parent_task_uses_prompts(parent_dir: Path, prompt_slugs: list[str], today: str) -> None:
    """Line-based frontmatter edit that preserves original key formatting and
    quoting; only mutates `task_uses_prompts` and `updated`."""
    task_md = parent_dir / "task.md"
    text = task_md.read_text()
    if not text.startswith(FM_FENCE + "\n"):
        return
    end = text.find("\n" + FM_FENCE + "\n", len(FM_FENCE) + 1)
    if end == -1:
        return
    fm_block = text[len(FM_FENCE) + 1 : end]
    body = text[end + len(FM_FENCE) + 2 :]

    # Read existing task_uses_prompts entries (so we don't duplicate).
    existing: list[str] = []
    in_tup = False
    for raw in fm_block.splitlines():
        if raw.startswith("task_uses_prompts:"):
            in_tup = True
            tail = raw.split(":", 1)[1].strip()
            if tail and tail != "[]":
                # inline list (rare in this corpus); skip — we'll let the rewrite
                # below decide.
                pass
            continue
        if in_tup:
            if raw.startswith("  - "):
                existing.append(raw[4:].strip())
                continue
            in_tup = False
    new_list = list(existing)
    changed = False
    for s in prompt_slugs:
        if s not in new_list:
            new_list.append(s)
            changed = True
    if not changed:
        return

    # Rewrite the frontmatter block line-by-line, preserving everything except
    # task_uses_prompts (replaced with new list) and updated (bumped to today).
    out_lines: list[str] = []
    skip_until_non_dash = False
    saw_updated = False
    for raw in fm_block.splitlines():
        if skip_until_non_dash:
            if raw.startswith("  - "):
                continue
            skip_until_non_dash = False
        if raw.startswith("task_uses_prompts:"):
            out_lines.append("task_uses_prompts:")
            for item in new_list:
                out_lines.append(f"  - {item}")
            skip_until_non_dash = True
            continue
        if raw.startswith("updated:"):
            out_lines.append(f"updated: {today}")
            saw_updated = True
            continue
        out_lines.append(raw)
    if not saw_updated:
        out_lines.append(f"updated: {today}")

    new_text = FM_FENCE + "\n" + "\n".join(out_lines) + "\n" + FM_FENCE + "\n" + body
    task_md.write_text(new_text)


# ---------- main ----------

def process_subtask(subtask_path: Path, today: str, *, force: bool, dry_run: bool) -> tuple[str, str]:
    """Returns (parent_slug, prompt_slug)."""
    parent_dir = subtask_path.parent.parent
    parent_dir_name = parent_dir.name
    parent_slug = parent_task_slug(parent_dir)
    subtask_filename = subtask_path.name
    st_label = subtask_label(subtask_filename)
    prompt_slug = prompt_slug_from_subtask(subtask_filename)

    text = subtask_path.read_text()
    original_fm, body = parse_frontmatter(text)

    # H1 title.
    h1_match = re.search(r"^#\s+(.+)$", body, flags=re.M)
    h1_title = h1_match.group(1).strip() if h1_match else f"{st_label} — {prompt_slug}"

    # Lead metadata.
    lead_meta, _ = extract_lead_metadata(body)

    # Sections.
    sections = split_sections(body)

    prompt_dir = PROMPTS_ROOT / prompt_slug
    if prompt_dir.exists() and not force:
        print(f"  [skip-existing-prompt] {prompt_slug}")
    else:
        if not dry_run:
            prompt_dir.mkdir(parents=True, exist_ok=True)
            (prompt_dir / "brief.md").write_text(build_brief_md(
                prompt_slug=prompt_slug,
                parent_dir_name=parent_dir_name,
                parent_slug=parent_slug,
                subtask_filename=subtask_filename,
                st_label=st_label,
                h1_title=h1_title,
                sections=sections,
                lead_meta=lead_meta,
                today=today,
            ))
            (prompt_dir / "prompt.md").write_text(build_prompt_md(
                prompt_slug=prompt_slug,
                parent_slug=parent_slug,
                parent_dir_name=parent_dir_name,
                subtask_filename=subtask_filename,
                st_label=st_label,
                h1_title=h1_title,
                sections=sections,
                lead_meta=lead_meta,
                today=today,
            ))
            (prompt_dir / "readme.md").write_text(build_readme_md(
                prompt_slug=prompt_slug,
                parent_slug=parent_slug,
                parent_dir_name=parent_dir_name,
                st_label=st_label,
                h1_title=h1_title,
                today=today,
            ))

    # Rewrite subtask file as thin pointer (idempotent: skip if already a pointer).
    is_already_pointer = "**Prompt:**" in body and ("`/prompts/" in body or "/prompts/" in body)
    if is_already_pointer and not force:
        print(f"  [skip-already-pointer] {subtask_path.relative_to(REPO_ROOT)}")
    else:
        if not dry_run:
            subtask_path.write_text(build_subtask_pointer(
                original_text=text,
                h1_title=h1_title,
                prompt_slug=prompt_slug,
                parent_dir_name=parent_dir_name,
                st_label=st_label,
                lead_meta=lead_meta,
                today=today,
            ))

    return parent_slug, prompt_slug


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="Re-scaffold prompt folders and re-write subtask pointers even if already extracted.")
    ap.add_argument("--today", default=date.today().isoformat())
    args = ap.parse_args()

    today = args.today
    parent_to_prompts: dict[str, list[str]] = {}
    parent_dirs_by_slug: dict[str, Path] = {}

    for ptd in PARENT_TASK_DIRS:
        parent_dir = TASKS_ROOT / ptd
        if not parent_dir.is_dir():
            print(f"WARN: parent task dir missing: {parent_dir}")
            continue
        slug = parent_task_slug(parent_dir)
        parent_dirs_by_slug[slug] = parent_dir
        for st in sorted((parent_dir / "subtasks").glob("[0-9]*.md")):
            print(f"processing {st.relative_to(REPO_ROOT)}")
            parent_slug, prompt_slug = process_subtask(
                st, today, force=args.force, dry_run=args.dry_run,
            )
            parent_to_prompts.setdefault(parent_slug, []).append(prompt_slug)

    if args.dry_run:
        print("[dry-run] skipping parent task_uses_prompts updates")
        return 0

    for parent_slug, slugs in parent_to_prompts.items():
        parent_dir = parent_dirs_by_slug[parent_slug]
        update_parent_task_uses_prompts(parent_dir, slugs, today)
        print(f"updated task_uses_prompts on {parent_dir.relative_to(REPO_ROOT)}/task.md ({len(slugs)} entries)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
