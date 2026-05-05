# Sample runtime files (optional)

`agents.jsonl` — one JSON object per line, appended live by your runtime:

```json
{"id":"claude-code-01","handle":"claude-code","model":"claude-sonnet-4.5","status":"running","currentTask":"012","currentAction":"reviewing PR #29","tokensUsed":184320,"tokenBudget":240000,"costUSD":2.41,"uptime":"1h 42m","color":"#00FF9F","role":"implementer"}
{"id":"claude-code-01","status":"idle","currentAction":"awaiting next task"}
```

The server upserts on `id`, so subsequent lines patch the same agent.

`chat.jsonl` — one message per line, with a `channel` field:

```json
{"channel":"general","id":"m1","ts":"08:14","author":"claude-code","role":"agent","text":"Coherence run 2026-05-05 partial — 7 issues, 12 deferred."}
{"channel":"tasks","id":"t1","ts":"08:30","author":"claude-code","role":"agent","text":"Task 012 at hunk 14/22."}
```
