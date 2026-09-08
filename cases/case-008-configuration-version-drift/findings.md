# Findings

## Supported result

Both conditions contain the same drift. The failure admits a delete under the changed policy; the control blocks the unevaluated configuration. The recorded model-label change alone does not establish model causation.

This result is confirmed within the deterministic model. Supporting records are
listed in [the AIRG register](airg.md); exact comparisons are in
[the replay result](evidence/raw/replay-results.json).

## Containment procedure

Block the unevaluated deployment, restore a pinned version, rerun consequence-specific evaluations and retain both manifests for reconstruction.

## Recovery assessment

Prevention is demonstrated. No failure-condition restoration, canary reliability or model rollback fidelity is claimed.

## Evidence limitations and alternatives

The model names are labels. The explicit policy branch causes the simulated action; no real model behavior is evaluated.

No incident frequency, model behavior, human decision quality, latency or complete
enterprise inventory is measured. A real system may implement different delegation,
storage or review semantics. Validate the proposed control at the actual enforcement
boundary before claiming equivalent behavior.

## Proposed v0.2 requirement

Preserve immutable deployment and evaluation references; do not infer causation from version correlation alone.
