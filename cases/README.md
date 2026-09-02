# Reference investigations

Reference cases are controlled, reproducible investigations used to validate or falsify the specification. They should produce synthetic evidence bundles that another investigator can analyze without privileged developer knowledge.

## Initial case sequence

| Case | Status | Focus | Primary claim tested |
| --- | --- | --- | --- |
| [001](case-001-prompt-injection-tool-abuse/README.md) | Complete synthetic bundle | Prompt injection → tool abuse | Influence, authorization, tool execution, state change, and containment can be reconstructed without overstating data disposition. |
| [002](case-002-persistent-memory-poisoning/README.md) | Design scaffold | Persistent memory poisoning | Removing the original source does not contain durable derived influence. |
| [003](case-003-delegated-credential-containment/README.md) | Design scaffold | Delegated credential containment failure | Isolating the parent agent does not contain inherited authority or child workflows. |

## Standard evidence bundle

Each completed case should contain:

- `scenario.md` — system, threat, actions, and ground truth
- `evidence/` — synthetic raw and normalized evidence
- `manifest.json` — hashes, sources, collection times, and tools
- `airg.md` — evidence-backed reconstruction graph
- `analyst-guide.md` — questions and expected pivots, without giving away answers prematurely
- `findings.md` — confirmed facts, inferences, gaps, containment, recovery, and lessons
- `reproduce.md` — safe laboratory procedure
