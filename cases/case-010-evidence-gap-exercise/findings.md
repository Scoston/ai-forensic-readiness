# Findings

## Supported result

The object move is recorded in both conditions. In the failure, missing provider context leaves influence unknown. In the control, retrieved context is observable, but private reasoning and internal cognitive causation remain unknown.

This result is confirmed within the deterministic model. Supporting records are
listed in [the AIRG register](airg.md); exact comparisons are in
[the replay result](evidence/raw/replay-results.json).

## Containment procedure

Preserve unsampled gateway and downstream evidence, stop the affected workflow and record the missing-source interval before repairing collection.

## Recovery assessment

Collection repair improves future visibility; it cannot reconstruct the historical context that was never captured. The simulator does not reverse the object move.

## Evidence limitations and alternatives

A single deliberate drop models evidence loss. Real sampling policies, clock skew, outages and adversarial suppression require deployment testing.

No incident frequency, model behavior, human decision quality, latency or complete
enterprise inventory is measured. A real system may implement different delegation,
storage or review semantics. Validate the proposed control at the actual enforcement
boundary before claiming equivalent behavior.

## Proposed v0.2 requirement

Record capture quality and missing sources; an absent log is not evidence that no action occurred.
