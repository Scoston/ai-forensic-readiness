# Findings

## Supported result

The failure publishes and then issues a correction, while its simulated recipient copy remains. The control denies the publication before any receipt. A correction is compensation and does not reverse disclosure.

This result is confirmed within the deterministic model. Supporting records are
listed in [the AIRG register](airg.md); exact comparisons are in
[the replay result](evidence/raw/replay-results.json).

## Containment procedure

Disable further publication, inventory recipients and propagation, preserve the release receipt and obtain scoped disposition evidence where available.

## Recovery assessment

R3 disclosure is irreversible in this exercise. Correction and local removal reduce further harm but cannot support a recovered-confidentiality claim.

## Evidence limitations and alternatives

No message is actually sent or published. A synthetic receiver models retained data; real downstream propagation is unmeasured.

No incident frequency, model behavior, human decision quality, latency or complete
enterprise inventory is measured. A real system may implement different delegation,
storage or review semantics. Validate the proposed control at the actual enforcement
boundary before claiming equivalent behavior.

## Proposed v0.2 requirement

Evaluate consequence and reversibility at authorization time and keep compensation separate from reversal.
