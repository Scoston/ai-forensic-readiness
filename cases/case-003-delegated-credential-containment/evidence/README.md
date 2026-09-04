# Evidence inventory

All evidence is synthetic and safe for offline analysis. Timestamps use UTC. JSONL files contain one JSON object per line.

## Normalized evidence

| Artifact | Description |
| --- | --- |
| `normalized/events.json` | Ordered v0.1 AI investigation events spanning parent activity, initial response, child execution, expanded containment, recovery, and sealing |

## Raw evidence

| Artifact | Source represented |
| --- | --- |
| `user-instruction.json` | Protected human instruction and digest |
| `retrieved-content.json` | Untrusted guide and embedded delegation directive |
| `agent-runtime.jsonl` | Parent, child, and recovery-controller telemetry |
| `delegation-audit.jsonl` | Delegation creation, acceptance, and revocation |
| `token-broker.jsonl` | Parent session and child lease lifecycle |
| `task-queue.jsonl` | Persisted child task lifecycle |
| `authorization.jsonl` | Policy decisions and independent authorization probes |
| `tool-gateway.jsonl` | Storage move and restoration operations |
| `downstream-audit.jsonl` | Authoritative synthetic storage audit |
| `deployment-manifest.json` | Declared authority graph and containment inventory |
| `state-before.json` | Authoritative pre-action object and authority state |
| `state-after.json` | Post-action and post-recovery state |
| `containment-validation.json` | Initial and expanded containment results |

## Evidence handling

- Preserve LF line endings for byte-stable manifest verification.
- Treat the manifest as an integrity index, not a cryptographic signature.
- Corroborate agent records with delegation, token, authorization, queue, tool, and storage sources.
- Limit completeness claims to the declared deployment inventory.

## Synthetic identifiers

Token and session values such as `lease-child-003` are identifiers, not usable secrets. Storage targets use the `synthetic://` scheme, and the only HTTPS source uses `.invalid`.
