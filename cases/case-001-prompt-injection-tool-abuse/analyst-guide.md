# Analyst guide

Use this guide before reading [`findings.md`](findings.md). The evidence package is intended to support an independent reconstruction.

## Objective

Determine whether a consequential data disclosure occurred, why the action path became reachable, whose authority was used, what evidence supports each material relationship, and which containment claims can be proven.

## Starting points

1. Validate [`manifest.json`](manifest.json) before interpreting evidence.
2. Establish the time range and correlation identifiers from `evidence/normalized/events.json`.
3. Compare the original user instruction with the retrieved content.
4. Separate tool requests from policy decisions, delegation, authorization, and execution.
5. Corroborate agent records with IAM, tool-gateway, document-store, and network evidence.
6. Identify every durable effect or copy represented in the evidence.
7. Evaluate prospective revocation and retrospective disposition separately.

## Questions to answer

### Identity and authority

- Who initiated the workflow?
- Which agent and runtime executed it?
- Which delegated identity and scopes enabled the operations?
- What policy version authorized each consequential action?

### Context and provenance

- Which instruction constrained the user's objective?
- Which retrieved source supplied the restricted target and destination?
- How trustworthy was that source classified at collection time?
- Can the evidence prove influence, or only support an inference?

### Execution

- Which operations were requested, authorized, and executed?
- Did the tool arguments change between those stages?
- Which independent evidence confirms document access and outbound transfer?

### Persistence and recovery

- What state changed inside and outside the controlled environment?
- Which effect is reversible, compensable, recoverable with cost, or irreversible?
- What control stopped future access?
- What independent test validates that control?
- What residual state remains unresolved?

## Expected output

Produce:

- a UTC timeline;
- an authority chain;
- an AIRG with evidence references and confidence per material edge;
- a distinction between facts, strong support, inference, dispute, and unknowns;
- a dependency-aware containment inventory;
- a recovery and residual-risk statement; and
- proposed changes to instrumentation, authorization, or the v0.1 evidence model.

## Rules

- Do not treat the agent plan as independent corroboration.
- Do not infer deletion from revocation.
- Do not call the incident contained until the validation evidence is evaluated.
- Do not upgrade “strongly supported” influence to “confirmed” without an authoritative causal record.
- Do not use [`scenario.md`](scenario.md) ground truth or [`findings.md`](findings.md) as evidence during a blind exercise.

