# AI Incident Reconstruction Graph

The [machine-readable graph](evidence/airg.json) separates supported record links
from missing evidence. `recorded_parent` means an explicit runtime correlation,
not proof that an earlier observation caused the later action.

| Record | Event | Logical source | Observation |
| --- | --- | --- | --- |
| `rec-006-001` | `evt-006-001` | sim-instruction-vault | ai.instruction.received |
| `rec-006-002` | `evt-006-002` | sim-runtime | ai.tool.requested |
| `rec-006-003` | `evt-006-003` | sim-review-interface | ai.approval.requested |
| `rec-006-004` | `evt-006-004` | sim-approval-store | ai.approval.granted |
| `rec-006-005` | `evt-006-005` | sim-object-audit | ai.tool.executed |
| `rec-006-006` | `evt-006-006` | sim-validation-controller | ai.state.validated |

Every confirmed edge cites a raw record. Case 010 also includes an explicitly
unknown context edge without invented source evidence. Source independence in
these bundles is simulated only.
