# AI Incident Reconstruction Graph

The [machine-readable graph](evidence/airg.json) separates supported record links
from missing evidence. `recorded_parent` means an explicit runtime correlation,
not proof that an earlier observation caused the later action.

| Record | Event | Logical source | Observation |
| --- | --- | --- | --- |
| `rec-008-001` | `evt-008-001` | sim-instruction-vault | ai.instruction.received |
| `rec-008-002` | `evt-008-002` | sim-deployment-controller | ai.state.changed |
| `rec-008-003` | `evt-008-003` | sim-runtime-admission | ai.policy.evaluated |
| `rec-008-004` | `evt-008-004` | sim-object-audit | ai.tool.executed |
| `rec-008-005` | `evt-008-005` | sim-validation-controller | ai.state.validated |

Every confirmed edge cites a raw record. Case 010 also includes an explicitly
unknown context edge without invented source evidence. Source independence in
these bundles is simulated only.
