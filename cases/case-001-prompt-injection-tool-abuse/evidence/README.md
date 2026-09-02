# Evidence package

All records in this directory are synthetic. They contain no secrets, personal information, customer data, proprietary prompts, live credentials, or routable endpoints.

## Raw sources

| File | Simulated source | Evidentiary purpose |
| --- | --- | --- |
| `raw/user-instruction.json` | Agent application | Establishes the human's bounded objective |
| `raw/retrieved-content.json` | Retrieval gateway | Preserves the untrusted source, directive, trust label, and digest |
| `raw/deployment-manifest.json` | Configuration registry | Pins agent, model, prompt, policy, tool, identity, and scopes |
| `raw/agent-runtime.jsonl` | Protected agent telemetry | Records instruction, retrieval, plan, and tool requests |
| `raw/authorization.jsonl` | IAM/policy control plane | Records policy decisions, delegation, revocation, and denied replay |
| `raw/tool-gateway.jsonl` | Tool gateway | Records authorized and executed operations |
| `raw/downstream-audit.jsonl` | Document store and webhook service | Corroborates the read and accepted submission |
| `raw/network-egress.jsonl` | Customer-controlled egress gateway | Independently corroborates outbound transmission |
| `raw/state-before.json` | State collector | Records the pre-incident state |
| `raw/state-after.json` | State collector | Records the post-incident and post-containment state |
| `raw/containment-validation.json` | Independent response controller | Records controls applied and validation results |

## Normalized evidence

`normalized/events.json` contains the cross-source trajectory expressed with the v0.1 AI investigation event schema. It is an analyst convenience layer, not a replacement for the raw records.

## Time and correlation

- All timestamps are UTC.
- Primary trace: `trace-case-001`
- Session: `session-synthetic-001`
- Task: `task-summarize-public-report`
- Workflow: `workflow-case-001`
- Maximum modeled clock skew: 100 milliseconds

## Integrity and handling

[`../manifest.json`](../manifest.json) contains SHA-256 hashes calculated over the committed bytes. The case validator fails if an artifact is missing or its hash differs. Event-level cryptographic signatures are deliberately absent; the manifest provides file-level fixity, and the findings record the absence of signed source events as an evidence-quality limitation.

