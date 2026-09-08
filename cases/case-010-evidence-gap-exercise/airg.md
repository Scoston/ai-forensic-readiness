# AI Incident Reconstruction Graph

The [machine-readable graph](evidence/airg.json) separates supported record links
from missing evidence. `recorded_parent` means an explicit runtime correlation,
not proof that an earlier observation caused the later action.

| Record | Event | Logical source | Observation |
| --- | --- | --- | --- |
| `rec-010-001` | `evt-010-001` | sim-instruction-vault | ai.instruction.received |
| `rec-010-002` | `evt-010-002` | sim-collector-health | ai.evidence.exported |
| `rec-010-003` | `evt-010-003` | sim-tool-gateway | ai.tool.requested |
| `rec-010-004` | `evt-010-004` | sim-storage-audit | ai.tool.executed |
| `rec-010-005` | `evt-010-005` | sim-validation-controller | ai.state.validated |

Every confirmed edge cites a raw record. Case 010 also includes an explicitly
unknown context edge without invented source evidence. Source independence in
these bundles is simulated only.
