# Repo: narendrakumarnutalapati/licitra-sentry
- Axis: Mandatory tool calling
- Mechanism: Cryptographic execution binding and mandatory tool mediation. The agent is forced to use tools via a secure mediation layer; generating direct context responses bypasses the tamper-evident audit and is likely blocked structurally.
- Reusable patterns: "Mandatory tool mediation layer", preventing direct agent outputs and enforcing execution through a predefined hook/proxy.

- Readme Lektüre: Die Dokumentation zeigt, dass der Agent an eine strikte Sandbox gebunden ist. Jeder Output muss über ein definiertes Interface laufen, andernfalls wird er abgewiesen.
