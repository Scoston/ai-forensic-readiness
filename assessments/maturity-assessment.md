# AI forensic-readiness maturity assessment

Assess one consequential AI use case at a time. Record the evidence supporting each answer; policy assertions without tested evidence do not qualify.

## Use-case profile

- System / agent:
- Business owner:
- Technical owner:
- Assessor and date:
- Consequential actions:
- Sensitive data or regulated decisions:
- Maximum plausible impact:
- Current deployment stage:

## Dimension scoring

Score each dimension from 0 to 5.

| Score | Meaning |
| --- | --- |
| 0 | Invisible: activity cannot be reliably reconstructed. |
| 1 | Observable: basic interaction and API records exist. |
| 2 | Attributable: actions map to principals, agents, models, tools, and authority. |
| 3 | Reconstructable: material context, delegation, execution, and state paths can be rebuilt. |
| 4 | Containable: dependencies and persistent effects can be scoped and isolated. |
| 5 | Reversible and verifiable: recovery, revocation, and containment are tested and independently proven. |

| Dimension | Score | Evidence | Gap / action | Owner | Due date |
| --- | ---: | --- | --- | --- | --- |
| Identity and authority |  |  |  |  |  |
| Context and provenance |  |  |  |  |  |
| Execution evidence |  |  |  |  |  |
| Persistent-state visibility |  |  |  |  |  |
| Reconstruction capability |  |  |  |  |  |
| Dependency-aware containment |  |  |  |  |  |
| Prospective revocation |  |  |  |  |  |
| Retrospective data disposition |  |  |  |  |  |
| Reversibility / compensation |  |  |  |  |  |
| Meaningful human oversight |  |  |  |  |  |
| Evidence integrity and export |  |  |  |  |  |
| Privacy and retention controls |  |  |  |  |  |

## Readiness rule

The overall level should not exceed the lowest capability required to investigate and recover from the use case’s plausible high-impact incident. Do not average away a critical weakness.

## Exercise record

- Reference scenario executed:
- Date and participants:
- Reconstruction coverage:
- Attribution completeness:
- Time to defensible narrative:
- Containment completeness:
- Recovery success:
- Unresolved evidence gaps:
- Residual risk owner and decision:

## v0.2 evidence gate

Complete this gate for the selected consequence before assigning a readiness level.
Unknown means insufficient evidence, not a passing control.

| Requirement | Evidence to retain | Pass / fail / unknown |
| --- | --- | --- |
| Supported v0.1/v0.2 schema and complete manifest | Validator output, trusted manifest and protected originals | |
| Authority lifecycle | Parent/child grants, scope, audience, expiry and at-use denial probes | |
| Material context provenance | Protected content/chunk references, digests, trust and boundary | |
| Operational derivative disposition | Store/index/cache inventory, consumers, deletion or retention receipts | |
| Meaningful approval evidence | Actual presentation, operation/target binding, decision and available alternatives | |
| Configuration/evaluation alignment | Pinned deployed/evaluated manifests and changes | |
| Scoped recovery claim | Expected/observed state, independent validator and residual effects | |
| Capture quality and uncertainty | Missing-source interval, sampling and clock limits | |
| Independent reconstruction | Completed blind-exercise record identifying assistance and disagreements | |

The repository tests and synthetic cases do not themselves satisfy an enterprise's
deployment gate. Use the [review kit](../research/review-kit.md) to collect actual
exercise evidence. An R3 consequence may remain irreversible even when access
revocation is effective; record that residual limit explicitly.
