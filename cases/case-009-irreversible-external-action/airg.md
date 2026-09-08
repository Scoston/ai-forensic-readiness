# AI Incident Reconstruction Graph

The [machine-readable graph](evidence/airg.json) separates supported record links
from missing evidence. `recorded_parent` means an explicit runtime correlation,
not proof that an earlier observation caused the later action.

| Record | Event | Logical source | Observation |
| --- | --- | --- | --- |
| `rec-009-001` | `evt-009-001` | sim-instruction-vault | ai.instruction.received |
| `rec-009-002` | `evt-009-002` | sim-runtime | ai.tool.requested |
| `rec-009-003` | `evt-009-003` | sim-publication-gateway | ai.policy.evaluated |
| `rec-009-004` | `evt-009-004` | sim-recipient-receipt | ai.tool.executed |
| `rec-009-005` | `evt-009-005` | sim-response-controller | ai.state.compensated |
| `rec-009-006` | `evt-009-006` | sim-validation-controller | ai.state.validated |

Every confirmed edge cites a raw record. Case 010 also includes an explicitly
unknown context edge without invented source evidence. Source independence in
these bundles is simulated only.
