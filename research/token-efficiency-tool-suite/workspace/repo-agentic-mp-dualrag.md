# Repo: chkao831/agentic_mp_dualrag
- Axis: Mandatory tool calling
- Mechanism: Allowlisted tools only. The agent's generation is structurally constrained to tool calls via FastAPI backend constraints.
- Reusable patterns: Strict "allowlisted tool execution" validation; if the output is not a tool call, it fails parsing and is rejected.
