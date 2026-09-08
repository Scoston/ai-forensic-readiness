# Reference investigations

Reference cases are controlled, reproducible investigations used to validate or falsify the specification. They should produce synthetic evidence bundles that another investigator can analyze without privileged developer knowledge.

## Initial case sequence

| Case | Status | Focus | Primary claim tested |
| --- | --- | --- | --- |
| [001](case-001-prompt-injection-tool-abuse/README.md) | Complete synthetic bundle | Prompt injection → tool abuse | Influence, authorization, tool execution, state change, and containment can be reconstructed without overstating data disposition. |
| [002](case-002-persistent-memory-poisoning/README.md) | Complete synthetic bundle | Persistent memory poisoning | Source removal does not contain durable derived influence; memory lineage and remediation can be reconstructed and validated. |
| [003](case-003-delegated-credential-containment/README.md) | Complete synthetic bundle | Delegated credential containment failure | Isolating the parent agent does not contain already-issued descendant authority or child workflows. |
| [004](case-004-unverifiable-revocation/README.md) | Complete simulation bundle | Unverifiable revocation | Prospective denial and operational derivative disposition require separate proof. |
| [005](case-005-tool-description-manipulation/README.md) | Complete simulation bundle | Tool description manipulation | Description provenance and gateway enforcement separate selection from permitted execution. |
| [006](case-006-approval-compromise/README.md) | Complete simulation bundle | Approval compromise | Approval evidence must preserve what the reviewer saw and could reject. |
| [007](case-007-cross-tenant-memory-exposure/README.md) | Complete simulation bundle | Cross-tenant memory exposure | Chunk provenance and enforcement identify and prevent boundary crossing. |
| [008](case-008-configuration-version-drift/README.md) | Complete simulation bundle | Model/policy version drift | Deployed configuration must be compared with the evaluated baseline. |
| [009](case-009-irreversible-external-action/README.md) | Complete simulation bundle | Irreversible external action | A correction does not restore confidentiality after publication. |
| [010](case-010-evidence-gap-exercise/README.md) | Complete simulation bundle | Evidence-gap exercise | Downstream execution can be established while missing influence remains unknown. |

Cases 004-010 contain separate failure and control traces. These state machines
test explicit control relationships, not real models or production services.
[Supplemental comparisons](../research/simulations) cover Cases 001-003 without
altering their original manifested evidence. See [cross-case findings](../research/cross-case-findings.md).

## Standard evidence bundle

Each completed case should contain:

- `scenario.md` — system, threat, actions, and ground truth
- `evidence/` — synthetic raw and normalized evidence
- `manifest.json` — hashes, sources, collection times, and tools
- `airg.md` — evidence-backed reconstruction graph
- `analyst-guide.md` — questions and expected pivots, without giving away answers prematurely
- `findings.md` — confirmed facts, inferences, gaps, containment, recovery, and lessons
- `reproduce.md` — safe laboratory procedure
