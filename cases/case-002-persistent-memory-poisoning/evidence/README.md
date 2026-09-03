# Evidence package

All records in this directory are synthetic. They contain no secrets, personal information, customer data, proprietary prompts, live credentials, or routable endpoints.

## Raw sources

| File | Simulated source | Evidentiary purpose |
| --- | --- | --- |
| `raw/user-instructions.jsonl` | Agent application | Preserves bounded seed, trigger, and replay instructions |
| `raw/retrieved-content.json` | Retrieval gateway | Preserves the untrusted source, embedded directive, trust label, and digest |
| `raw/deployment-manifest.json` | Configuration registry | Pins agent, model, prompt, policy, memory service, tools, and consumer inventory |
| `raw/agent-runtime.jsonl` | Protected agent telemetry | Records sessions, transformations, memory context, plans, and tool requests |
| `raw/memory-audit.jsonl` | Shared-memory control plane | Records write, indexing, reads, quarantine, active removal, rebuild, and cache invalidation |
| `raw/source-control.jsonl` | Content moderation service | Records source removal and later retrieval denial |
| `raw/authorization.jsonl` | Policy service | Records the defective allow decision and post-containment denial |
| `raw/tool-gateway.jsonl` | Ticket tool gateway | Records ticket closure and compensating reopen operation |
| `raw/downstream-audit.jsonl` | Ticket service | Independently corroborates closed and restored ticket state |
| `raw/replay-results.json` | Independent replay harness | Compares poisoned and quarantined memory conditions |
| `raw/state-before.json` | State collector | Records source, memory, derivatives, and ticket before the incident |
| `raw/state-after.json` | State collector | Records state after the action and after containment |
| `raw/containment-validation.json` | Independent response controller | Records controls, known-consumer queries, policy replay, and restoration validation |

## Normalized evidence

`normalized/events.json` contains the cross-source trajectory expressed with the v0.1 AI investigation event schema. It is an analyst convenience layer, not a replacement for raw evidence.

## Time and correlation

- All timestamps are UTC.
- Seed trace/session: `trace-case-002-seed` / `session-memory-seed-002`
- Source-removal trace/session: `trace-case-002-source-removal` / `session-source-removal-002`
- Trigger trace/session: `trace-case-002-trigger` / `session-memory-trigger-002`
- Response trace/session: `trace-case-002-response` / `session-memory-response-002`
- Replay trace/session: `trace-case-002-replay` / `session-memory-replay-002`
- Workflow: `workflow-case-002`
- Maximum modeled clock skew: 100 milliseconds

## Integrity and handling

[`../manifest.json`](../manifest.json) contains SHA-256 hashes over the committed bytes. The validator fails if an artifact is missing or its hash differs. The poisoned memory record remains in synthetic forensic quarantine while being unavailable to the active runtime; preservation and operational removal are intentionally represented as separate facts.
