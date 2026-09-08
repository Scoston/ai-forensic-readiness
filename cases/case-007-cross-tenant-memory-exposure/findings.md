# Findings

## Supported result

The failure exposes tenant A's named chunk to tenant B and records its use in the simulated plan. The control denies the read and emits no downstream memory-read or plan event.

This result is confirmed within the deterministic model. Supporting records are
listed in [the AIRG register](airg.md); exact comparisons are in
[the replay result](evidence/raw/replay-results.json).

## Containment procedure

Disable the shared retrieval route, quarantine the entry, enumerate tenant B consumers and caches, then test both permitted and prohibited boundaries.

## Recovery assessment

The control proves denial for the two named tenants. Deletion of every prior consumer copy is unknown; subsequent isolation does not undo an already-observed disclosure.

## Evidence limitations and alternatives

One memory record and two synthetic tenants are modeled. Vector-index filtering, distributed cache timing and alternate workflows are not exercised.

No incident frequency, model behavior, human decision quality, latency or complete
enterprise inventory is measured. A real system may implement different delegation,
storage or review semantics. Validate the proposed control at the actual enforcement
boundary before claiming equivalent behavior.

## Proposed v0.2 requirement

Tenant and workflow provenance must survive transformations and be checked before retrieval returns content.
