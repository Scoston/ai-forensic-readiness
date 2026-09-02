# Findings and lessons

## Executive finding

The evidence confirms that the synthetic research workflow read a restricted document and transmitted a representation of it to an external destination. The user did not request either action. Retrieved content supplied the restricted target, destination, and classification later used in the plan and tool calls, making prompt-injection influence strongly supported.

The delegated session was revoked and a subsequent validation call was denied, proving prospective revocation. The evidence does not prove deletion of the external copy. The disclosure remains R3 and retrospective disposition remains unresolved.

## Six-question findings

| Dimension | Finding | Confidence |
| --- | --- | --- |
| Identity | `analyst-01` initiated the task; `research-agent` ran as `workload-research-agent` and used `svc-afr-lab-reader`. | Confirmed |
| Context | The user limited the task to public material. The retrieved page introduced the restricted target, external destination, and misleading classification. | Confirmed inputs; influence strongly supported |
| Execution | The policy allowed, and the tool completed, `read_document` followed by `send_webhook`. | Confirmed |
| Provenance | The consequential parameters originated in an `untrusted-web` retrieval record with a preserved digest. | Confirmed |
| Persistence / blast radius | A represented copy persisted at the external destination; the delegated session and connector were additional dependencies. | Confirmed existence; deletion unknown |
| Recovery | Future use of the delegated session was denied after containment. External deletion cannot be proven. | Prospective revocation confirmed; retrospective disposition unresolved |

## Material findings

### F-001 — The human instruction did not authorize the consequential actions

`user-instruction.json` explicitly prohibits internal-document access and external transmission. The human principal cannot be treated as having approved the later actions merely because the agent operated within a user-created session.

### F-002 — Retrieved content crossed the instruction boundary

The retrieved page was labeled untrusted but preserved an embedded directive. The agent plan repeated three distinctive values found only in that directive. This supports the influence edge, although it does not expose or prove private model reasoning.

### F-003 — Authorization was distinct from agent selection

The policy engine independently returned `allow`. The defect was not simply that the agent requested the wrong tool. `policy-lab-004` trusted an agent-supplied `public-validation` classification and permitted an R3 action without independent approval.

### F-004 — Independent evidence corroborated execution

The restricted-document read is present in both tool-gateway and document-store records. The outbound transfer is present in tool-gateway, downstream-service, and customer-controlled network-egress records. The agent record is not the sole evidence source.

### F-005 — Revocation and deletion were not equivalent

The control plane revoked `delegated-session-001`, the connector was disabled for the workflow, and a replay attempt was denied. Those facts prove future access termination. No deletion receipt or control over the represented external copy exists.

## Evidence gaps

| Gap | Effect | Disposition |
| --- | --- | --- |
| `GAP-001` — No external deletion receipt | Retrospective disposition cannot be proven | Residual risk remains open |
| `GAP-002` — No signed source events | Source-event tampering cannot be excluded cryptographically | File-level manifest provides limited fixity; recommend signed export batches |
| `GAP-003` — No authoritative model-causality record | Exact internal causal weight is unknowable | Keep influence at strongly supported |
| `GAP-004` — No human approval evidence for R3 action | Oversight effectiveness cannot be demonstrated | Treat as authorization-control failure |

## Containment and recovery

| Dependency or effect | Action | Validation | Status |
| --- | --- | --- | --- |
| Agent session | Terminated | Session state reported closed | Contained |
| Delegated session | Revoked | Replay call denied by control plane | Contained and validated |
| Workflow connector | Disabled | Connector inventory reports disabled | Contained and validated |
| Defective policy rule | Disabled for workflow | Policy snapshot records inactive override | Contained pending engineering correction |
| Restricted document | Read-only source unchanged | Before/after document hash matches | No restoration required |
| External copy | No available deletion control | No deletion receipt | Unresolved, R3 |

Containment is therefore **complete for identified future execution paths but incomplete for retrospective data disposition**. The organization must not summarize that state simply as “contained” without the qualification.

## Measurements

| Metric | Result | Basis |
| --- | --- | --- |
| Reconstruction coverage | 11 of 12 material AIRG edges supported; 1 unknown | External deletion edge is missing |
| Attribution completeness | 2 of 2 consequential operations mapped to principal and authority chain | Read and send operations |
| Containment completeness | 4 of 4 identified future-execution dependencies controlled and validated | Session, delegated session, connector, policy override |
| Recovery success | 0 of 1 irreversible disclosure effects reversed | R3 disclosure cannot be undone |
| Residual-state disposition | 0 of 1 external copies deleted or retained with authoritative confirmation | `GAP-001` |
| Evidence latency | Not measured | Synthetic fixtures are pre-collected |
| Time to defensible narrative | Not measured | Should be measured in a blind tabletop |

## Lessons proposed for v0.2 consideration

1. **Add explicit risk or consequence classification to action/authorization evidence.** The v0.1 schema records policy outcome and reversibility class on state, but not the action risk tier considered at authorization time.
2. **Represent trust labels on influence records.** Provenance references alone do not express that retrieved content was classified `untrusted-web`.
3. **Add authorization-reason and evaluated-input references.** A policy decision should preserve the rule and material attributes that produced `allow` without relying on free text.
4. **Add validation method and result fields.** `ai.state.validated` currently uses general action/state fields; a defined validation object would improve proof of containment.
5. **Keep private model reasoning out of the minimum profile.** The case was defensibly reconstructed without claiming access to hidden reasoning, but content provenance and plan/tool correlation were essential.

These are evidence-backed proposals, not accepted schema changes. They should enter the public process as issues or an RFC before inclusion in v0.2.
