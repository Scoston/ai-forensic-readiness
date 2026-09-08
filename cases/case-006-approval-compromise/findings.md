# Findings

## Supported result

A recorded approval exists in the failure condition despite a mismatch between the displayed test preview and actual production deletion. In the control the same scripted reviewer can see the actual deletion and rejects it.

This result is confirmed within the deterministic model. Supporting records are
listed in [the AIRG register](airg.md); exact comparisons are in
[the replay result](evidence/raw/replay-results.json).

## Containment procedure

Suspend the approval path; compare the displayed action against actual request digests; preserve reviewer choices and presentation history; require an independently populated display.

## Recovery assessment

The simulator proves prevention in the control condition. It does not restore the deleted failure-condition object or claim a tested rollback.

## Evidence limitations and alternatives

This is a scripted reviewer, not a human-subject experiment. Review time, competence, coercion and real human judgment are unmeasured.

No incident frequency, model behavior, human decision quality, latency or complete
enterprise inventory is measured. A real system may implement different delegation,
storage or review semantics. Validate the proposed control at the actual enforcement
boundary before claiming equivalent behavior.

## Proposed v0.2 requirement

Approval is evidence of a decision only within the recorded presentation and authority context.
