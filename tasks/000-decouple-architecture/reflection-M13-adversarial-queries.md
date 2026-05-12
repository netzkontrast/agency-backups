# M13 — Adversarial Query Expansion

Method: For the chosen architecture, generate four adversarial reframings (Adjacent, Opposing, Abstraction, Orthogonal axes), state what each reframing would suggest, and decide whether to modify the design.

## Adjacent — "How does Linear / Jira model Tasks vs Prompts?"

Linear has **Issues** (Tasks) and **Templates** (recurring instruction sets). It does *not* separate "follow-up question" from "issue"; everything is an Issue with parent/child links. This suggests collapsing `/prompts/` follow-ups into `/tasks/` as a `task_kind: follow-up`. **Decision:** Reject. Linear's flat issue model works because issues are short-lived and context-light. Our prompts are long, executable instruction sets that get reused across multiple Tasks (e.g., a research-prompt-optimizer skill). Forcing reuse-bearing artifacts under `/tasks/` would couple instruction lifetime to coordination lifetime.

## Opposing — "What if Tasks were Git issues / external GitHub Issues, not files?"

Strongest counter-argument: GitHub Issues already exist, support assignment, status, labels, and threaded comments. Why duplicate that in markdown? **Decision:** Reject for this repo, but document the trade-off. The repo is intentionally a *single source of truth* readable offline by an agent in a sandbox without GitHub API access. File-based Tasks are queryable by `grep` and `python3 tools/validate-frontmatter.py`. GitHub Issues are an integration target, not a substitute. **Modification:** Note in `TASK.md` §8 that an external issue tracker MAY mirror Tasks but the markdown is canonical.

## Abstraction — "What is the most general data structure here?"

A Task is a *node* with edges to Prompts and to Research. This is graph database territory. The most general abstraction is: **every operational file is a node; every frontmatter relational key is an edge**. The directory structure (`/tasks/`, `/prompts/`, `/research/`) is a *labeled partition* of the node set. **Decision:** Adopt as the mental model. Documented in `FOLDERS.md` §6: "the frontmatter is the source of truth for any future CLI/graph tooling." This frames the Obsidian Graph View, future CLI, and any RAG indexer as consumers of the same edge set.

## Orthogonal — "What does game asset metadata or media-pipeline metadata teach us?"

Game engines store *sidecar* `.meta` files alongside every asset because the asset itself (texture, mesh) is binary and unannotatable. Markdown is annotatable, so we put L1/L2 *inside* the file via frontmatter. But L3 (vectors, embeddings) is binary-ish and frontmatter-hostile — exactly where the sidecar pattern earns its keep. **Decision:** Adopted in `TASK.md` §3.4: L3 lives in `/.agent_cache/<file>.meta.json`. Direct cross-pollination from game-engine practice.

## Net Modifications Made From This Pass

1. Documented the "frontmatter is source of truth for tooling" framing in `FOLDERS.md` §6 (Abstraction axis).
2. Reserved L3 sidecar convention in `TASK.md` §3.4 (Orthogonal axis).
3. Added §8 Edge Cases including "Tasks That Spawn Tasks" (sibling, not nested) (Adjacent axis).
4. Did **not** adopt: external issue tracker as substitute for `/tasks/` (Opposing axis), or follow-up-as-task collapse (Adjacent axis).
