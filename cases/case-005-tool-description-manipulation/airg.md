# AI Incident Reconstruction Graph

The [machine-readable graph](evidence/airg.json) separates supported record links
from missing evidence. `recorded_parent` means an explicit runtime correlation,
not proof that an earlier observation caused the later action.

| Record | Event | Logical source | Observation |
| --- | --- | --- | --- |
| `rec-005-001` | `evt-005-001` | sim-instruction-vault | ai.instruction.received |
| `rec-005-002` | `evt-005-002` | sim-tool-registry | ai.context.retrieved |
| `rec-005-003` | `evt-005-003` | sim-runtime | ai.tool.requested |
| `rec-005-004` | `evt-005-004` | sim-gateway | ai.policy.evaluated |
| `rec-005-005` | `evt-005-005` | sim-egress | ai.tool.executed |
| `rec-005-006` | `evt-005-006` | sim-validation-controller | ai.state.validated |

Every confirmed edge cites a raw record. Case 010 also includes an explicitly
unknown context edge without invented source evidence. Source independence in
these bundles is simulated only.
