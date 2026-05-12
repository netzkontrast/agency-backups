# Friction Log — Task 003 (Analyze SKILL.md Novel-Authoring Research)

Highest Friction Level: FL1

## Summary

The task delivered its primary artifact (`output/RECOMMENDATIONS.md`) and filed
three follow-up prompts (`mega-context-limit-management`,
`cross-skill-context-poisoning`, `subjective-quality-evaluation`) without
significant blocker during execution.

Friction surfaced **after** closure during a subsequent governance audit:

1. **Frontmatter semantics drift.** The task originally listed the three
   follow-up prompt slugs in `task_spawns_research`, but those follow-ups are
   *prompts awaiting execution*, not research workspaces. The linker
   (`tools/lint-linkage.py`) correctly rejected them as unresolved research
   slugs. Resolved by emptying `task_spawns_research` — the spawn artifact is
   the prompt set, captured naturally via each prompt's
   `prompt_spawned_from_research` back-link.
2. **`prompt_relates_to_task` overloaded.** Each follow-up prompt declared
   `prompt_relates_to_task: analyze-skillmd-novel-authoring`, but the linker
   interprets that field as "task that *uses* this prompt" with reciprocity
   required. Follow-up prompts have no using task yet. Resolved by removing
   the field from all three; the spawn relationship survives via
   `prompt_spawned_from_research`.
3. **Provider-subfolder research not resolvable.** The follow-up prompts
   declared `prompt_spawned_from_research: github-skillmd-novel-authoring-de-en`,
   which lives at `research/gemini/github-skillmd-novel-authoring-de-en/`
   (a provider subfolder per RESEARCH.md §6). The linker only walked
   top-level `/research/<slug>/`. Resolved by extending the linker to also
   accept provider subfolders.

## Recommendation (Governance)

These three frictions are governance-level signals, not session-level
annoyances. They are flagged for governance review per FRUSTRATED.md FL2
"Special Triggers" (administrative overhead caused by spec ambiguity), even
though the per-step friction during execution was FL0–FL1.

Concrete spec follow-ups (already applied in the same coherence pass):

- TASK.md §2 should mark `friction-log.md` MANDATORY for `task_status: done`,
  matching enforcement in `lint-linkage.py:133` and `check-trust.py`.
- PROMPT.md §6.5 should explicitly state that
  `prompt_spawned_from_research` resolves under provider subfolders too.
- PROMPT.md §6.6 should explicitly state that `prompt_relates_to_task`
  encodes a *uses* relationship requiring reciprocity, not a "spawned-from"
  relationship.

## Provenance

Authored 2026-05-04 during the governance-coherence pass that detected the
above linkage failures. Reconstructed in retrospect from artifact evidence
(task.md, prompt frontmatter, linker output). Original session by
`claude-code` did not produce a friction log.
