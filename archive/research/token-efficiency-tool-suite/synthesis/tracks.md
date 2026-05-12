# Tracks

- **Track A: Mandatory tool calling.** Investigated `licitra-sentry` and `agentic_mp_dualrag`. Found that structural enforcement (allowlisting tools or using a mediation layer) successfully prevents direct free-form output.
- **Track B: Token budget enforcement.** Investigated `Token-Budgeted-Multi-Agentic-System`, `openclaw-revenium`, and `tokencap`. Highlighted the need for pre-invocation budget checks and hard limits to prevent silent token drain.
- **Track C: Structured output coercion.** Investigated `structured-output`. Found that Pydantic validation combined with JSON-mode enforces strict schemas, trimming verbose natural language.
- **Track D: Context window management.** Investigated `Context-Engine` and `ContextGate`. Found that middleware hooks can dynamically prune and compress RAG/history data before LLM invocation.
- **Track M13: Expansions.** Uncovered that failure modes often occur when tools return uncompressed data. Identified the "query planner" abstraction from orthogonal domains as a missing piece.
