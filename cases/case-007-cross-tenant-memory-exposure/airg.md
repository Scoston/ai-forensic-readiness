# AI Incident Reconstruction Graph

The [machine-readable graph](evidence/airg.json) separates supported record links
from missing evidence. `recorded_parent` means an explicit runtime correlation,
not proof that an earlier observation caused the later action.

| Record | Event | Logical source | Observation |
| --- | --- | --- | --- |
| `rec-007-001` | `evt-007-001` | sim-instruction-vault | ai.instruction.received |
| `rec-007-002` | `evt-007-002` | sim-memory-writer | ai.memory.written |
| `rec-007-003` | `evt-007-003` | sim-memory-gateway | ai.policy.evaluated |
| `rec-007-004` | `evt-007-004` | sim-retrieval-audit | ai.memory.read |
| `rec-007-005` | `evt-007-005` | sim-runtime | ai.plan.created |
| `rec-007-006` | `evt-007-006` | sim-validation-controller | ai.state.validated |

Every confirmed edge cites a raw record. Case 010 also includes an explicitly
unknown context edge without invented source evidence. Source independence in
these bundles is simulated only.
