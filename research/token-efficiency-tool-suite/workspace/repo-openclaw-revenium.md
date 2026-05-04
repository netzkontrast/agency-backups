# Repo: revenium/openclaw-revenium
- Axis: Token budget enforcement
- Mechanism: Pre-invocation budget guardrails and token metering skill. It enforces budgets at the invocation layer, preventing the agent from silently blowing through tokens.
- Reusable patterns: "Configurable budget guardrail decorator/hook" to check token spend before allowing a prompt or tool call.
