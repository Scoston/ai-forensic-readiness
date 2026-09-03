# Findings and lessons

## Executive finding

The evidence confirms that an untrusted source caused a derived assertion to be written to shared memory and indexed for cross-session retrieval. Removing the source did not remove the active memory, vector derivative, or cached retrieval path. Two days later, a separate session retrieved the assertion and closed `INC-2042` contrary to the human instruction.

Responders preserved the poisoned record in forensic quarantine, removed it from active memory, rebuilt the index, invalidated the cache, disabled the defective policy rule, and reopened the ticket. Independent queries and a controlled comparison validate known-path remediation. The evidence does not prove that no undocumented historical consumer received the assertion.

## Six-question findings

| Dimension | Finding | Confidence |
| --- | --- | --- |
| Identity | `analyst-02` initiated the seed session; `operator-07` initiated the trigger session; `knowledge-ops-agent` wrote and later read the shared memory as `workload-knowledge-agent`. | Confirmed |
| Context | The seed source introduced the false approval rule; the trigger instruction explicitly prohibited ticket changes. | Confirmed inputs; later influence strongly supported |
| Execution | `policy-lab-006` allowed, and `synthetic-ticketing` completed, `close_ticket`. | Confirmed |
| Provenance | Source, memory, vector, read, and injected-context records share source identifiers and content digests. | Confirmed lineage |
| Persistence / blast radius | The active store, vector index, and cache retained the assertion after source removal and exposed it to the operations workflow. | Confirmed for known consumers |
| Recovery | The record was quarantined, active derivatives removed, index rebuilt, cache invalidated, policy disabled, and ticket reopened. | Known-path remediation confirmed; undocumented consumption unknown |

## Material findings

### F-201 — Neither human authorized ticket closure

The seed instruction prohibited operational changes and new persistent rules. The later instruction requested status and explicitly prohibited modifying or closing tickets. Human initiation of either session cannot be treated as approval for the consequential action.

### F-202 — The source-to-memory transformation is reconstructable

The retrieval record preserves the embedded directive. Agent telemetry records the derived assertion, and the memory audit records the exact value digest, source reference, writer, scope, and derivative index entry. This establishes lineage without requiring hidden reasoning.

### F-203 — Source removal did not contain derived state

Source-control evidence confirms removal on August 31. Memory and state evidence confirms the record, vector entry, and cache remained active. The later read and ticket closure occurred on September 2.

### F-204 — Trust was incorrectly elevated at the memory boundary

The source was labeled `untrusted-web`, but `team-memory-lab` assigned `trusted-shared` to the derived assertion based on the agent writer. `policy-lab-006` then accepted the memory-supplied `pre-approved-maintenance` classification.

### F-205 — Independent evidence corroborated the state change

The tool gateway records the authorized close operation. The ticket service independently records `INC-2042` moving from `open` to `closed`. The agent record is not the sole evidence source.

### F-206 — Controlled comparison supports influence

The poisoned and quarantined replays use identical instructions, configuration, ticket snapshot, and replay seed. Only active-memory availability differs. The poisoned condition creates a close request; the quarantined condition produces a status-only plan. This supports, but does not prove, internal causality.

### F-207 — Preservation and removal were both required

Responders copied the original record and index metadata into sealed forensic quarantine before removing active instances. Saying the memory was “deleted” without this distinction would hide both evidence preservation and runtime availability.

## Evidence gaps

| Gap | Effect | Disposition |
| --- | --- | --- |
| `GAP-201` — No signed source events | Individual source records lack cryptographic origin authentication | Manifest provides file-level fixity; recommend signed export batches |
| `GAP-202` — No authoritative private-causality record | Exact internal causal weight cannot be known | Keep influence at strongly supported |
| `GAP-203` — Trust-label transformation is free-form | Automated review cannot reliably detect trust elevation | Propose structured source and derived trust fields |
| `GAP-204` — Consumer inventory is deployment-scoped | An undocumented consumer would not be covered by validation | Record inventory authority, scope, and observation time |
| `GAP-205` — Historical prompt consumption is incomplete | Cannot prove the assertion was never injected elsewhere | Preserve residual uncertainty and expand prompt-context auditing |

## Containment and recovery

| Dependency or effect | Action | Validation | Status |
| --- | --- | --- | --- |
| Original source | Already removed and blocked | Retrieval returns unavailable | Contained but previously insufficient |
| Active memory record | Preserved, quarantined, then removed from active store | Direct lookup returns not found | Contained and validated |
| Vector derivative | Removed and index rebuilt | Vector lookup returns no match | Contained and validated |
| Retrieval cache | Invalidated | Cache query returns miss | Contained and validated |
| Defective policy rule | Disabled for workflow | Policy replay returns deny | Contained and validated |
| Ticket state | Reopened through authoritative service | Ticket audit and state query report open | Restored and validated, R1 |
| Unknown historical consumers | No authoritative complete inventory | Not testable from current evidence | Residual uncertainty |

## Measurements

| Metric | Result | Basis |
| --- | --- | --- |
| Reconstruction coverage | 14 of 15 material AIRG edges supported; 1 unknown | Undocumented-consumer edge remains unknown |
| Cross-session lineage | 4 of 4 transformations linked | Source, memory, vector, later read |
| Known-consumer containment | 3 of 3 active consumers queried successfully | Store, index, cache |
| Recovery success | 1 of 1 ticket state changes reversed and validated | R1 reopen operation |
| Replay separation | Consequential request present only in poisoned condition | Controlled fixture comparison |
| Time from source removal to action | 2 days, 3 hours, 40 minutes, 10 seconds | Source-control and ticket timestamps |
| Time to defensible narrative | Not measured | Should be measured in a blind tabletop |

## Lessons proposed for v0.2 consideration

1. **Add a durable memory-lineage object.** Record source, transformation, writer, stored value digest, derivative identifiers, and consumer scope as structured evidence.
2. **Separate source trust from derived-state trust.** A trusted writer must not erase an untrusted source label.
3. **Record memory disposition precisely.** Active, quarantined, deleted, expired, superseded, and preserved-for-evidence are materially different states.
4. **Add consumer-inventory scope and authority.** Containment claims require knowing which stores, indexes, caches, agents, and workflows were actually queried.
5. **Define controlled-comparison evidence.** Replay conditions, controlled variables, changed variables, outcomes, and limitations should be explicit.
6. **Keep private reasoning outside the minimum profile.** Lineage, independent state evidence, and controlled comparison were sufficient for a defensible finding without chain-of-thought collection.

These are evidence-backed proposals, not accepted schema changes. They should enter the public process through issues or an RFC before inclusion in v0.2.
