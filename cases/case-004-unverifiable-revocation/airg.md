# AI Incident Reconstruction Graph

The [machine-readable graph](evidence/airg.json) separates supported record links
from missing evidence. `recorded_parent` means an explicit runtime correlation,
not proof that an earlier observation caused the later action.

| Record | Event | Logical source | Observation |
| --- | --- | --- | --- |
| `rec-004-001` | `evt-004-001` | sim-instruction-vault | ai.instruction.received |
| `rec-004-002` | `evt-004-002` | sim-derivative-registry | ai.memory.written |
| `rec-004-003` | `evt-004-003` | sim-mail-gateway | ai.policy.evaluated |
| `rec-004-004` | `evt-004-004` | sim-validation-controller | ai.state.validated |
| `rec-004-005` | `evt-004-005` | sim-validation-controller | ai.state.validated |

Every confirmed edge cites a raw record. Case 010 also includes an explicitly
unknown context edge without invented source evidence. Source independence in
these bundles is simulated only.
