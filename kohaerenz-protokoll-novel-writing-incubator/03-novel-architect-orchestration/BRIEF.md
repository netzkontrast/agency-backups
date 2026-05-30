# Jules Brief — Slice 3: Novel-Architect Orchestration

- **alias:** `kp-incubator-orchestration`
- **repo:** `netzkontrast/agency-backups`
- **starting branch:** `claude/dreamy-galileo-06exy`
- **write only here:** `kohaerenz-protokoll-novel-writing-incubator/03-novel-architect-orchestration/`

## Dispatch prompt

```
Self-contained task. Do NOT clone any repo. Work language: English; never
translate German prose. Full autonomy — finish and open a PR.

STEP 1 — read the plugin model (one file only):
  kohaerenz-protokoll-novel-writing-incubator/PLUGIN-CONCEPTS.md

STEP 2 — read the orchestration source material in THIS repo (read-only):
  skills/novel-architect/**          (8-phase orchestrator: Bootstrap, Intent,
                                      Narrative Architecture, Characters, World &
                                      Research, Scene Matrix, Drafting, Iteration;
                                      hard exit gates; AskUserQuestion loops)
  skills/novel-architect/commands/** (the /novel-* command surface)
  skills/novel-architect-legacy/**   (frozen original KP skill — for contrast)

STEP 3 — write ONLY into
  kohaerenz-protokoll-novel-writing-incubator/03-novel-architect-orchestration/ :
    CONCEPTS.md   — the orchestration as a state machine mapped onto the plugin's
                    Lifecycle + Intent + gate primitives: the phases, the hard
                    gates, where human input is elicited, what state each phase
                    reads/writes.
    COHERENCE.md  — coherence check: do novel-architect's phases/gates map cleanly
                    onto plugin Lifecycle + gate (PASSED / BLOCKED_ON +
                    input-required)? Where does the skill model (progressive
                    disclosure) fit, and where does it fight?
    PROPOSAL.md   — how orchestration becomes a gated agency skill, the command
                    surface, and a `scaffold` verb that initialises a new novel
                    (the novels/{author}/works/{genre}/{slug}/ layout).

Concise, evidence-cited. Open a PR into claude/dreamy-galileo-06exy. Touch nothing
outside your slice dir.
```
