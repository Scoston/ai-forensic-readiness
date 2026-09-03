# Analyst guide

Use this guide before reading [`findings.md`](findings.md). The evidence package is intended to support an independent cross-session reconstruction.

## Objective

Determine how a removed source continued to influence a later session, which persistent derivatives and consumers carried that influence, what action occurred, and whether response actions remediated known active paths without destroying evidence.

## Starting points

1. Validate [`manifest.json`](manifest.json) before interpreting evidence.
2. Establish the five trace/session pairs in `evidence/normalized/events.json`.
3. Compare both human instructions with the retrieved source and derived memory value.
4. Trace `source-synthetic-web-0002` through `memory-0002`, `vector-0002`, and the later memory read.
5. Establish when source removal occurred relative to the delayed action.
6. Separate memory retrieval, plan creation, policy decision, tool request, authorization, execution, and downstream state.
7. Compare the poisoned and quarantined replay conditions.
8. Evaluate evidence preservation and active-memory removal as different objectives.

## Questions to answer

### Identity and authority

- Who initiated the seed and trigger sessions?
- Which agent and runtime wrote and later read the memory?
- Which policy input converted the stored assertion into an authorized operation?
- Did either human authorize ticket closure?

### Memory lineage and provenance

- Which source supplied the false approval rule and ticket identifier?
- What transformation produced the stored assertion?
- Which digest links the write, index, read, and injected-context records?
- Where was the original source trust label lost or overwritten?

### Execution and state

- Which operation was requested, authorized, and executed?
- Which independent source confirms the ticket state change?
- Is the closure reversible, and was restoration validated?

### Containment

- Did removing the source affect existing memory or derivatives?
- Which known consumers could retrieve `memory-0002`?
- Were the active record, vector entry, cache, and policy path addressed?
- Was the evidence preserved before active removal?
- What residual uncertainty remains after validation?

## Expected output

Produce:

- a UTC timeline spanning both days;
- a source-to-memory-to-action lineage;
- an AIRG with confidence and evidence references per edge;
- an inventory of persistent derivatives and consumers;
- a distinction between confirmed facts, strong support, inference, and unknowns;
- a containment, restoration, and residual-risk statement; and
- proposed instrumentation or schema changes supported by the case.

## Rules

- Do not treat source removal as memory deletion.
- Do not treat the agent plan as independent corroboration.
- Do not infer causality solely from semantic similarity when lineage and replay evidence are available.
- Do not call the memory erased when it remains in forensic quarantine.
- Do not generalize validation of known consumers into proof that no undocumented consumer exists.
- Do not use [`scenario.md`](scenario.md) or [`findings.md`](findings.md) as evidence during a blind exercise.
