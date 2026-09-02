# Interoperability mappings

These notes are hypotheses for implementation testing, not claims of official compatibility or endorsement.

## OCSF direction

OCSF should be the first candidate for normalized security-event representation because it is implementation-agnostic and already models security events, identities, resources, API activity, and findings. The initial work should:

1. Reuse existing OCSF objects and fields where semantics match.
2. Model AI-specific influence, memory, delegation, and approval relationships as an extension only when no equivalent exists.
3. Preserve trace, session, task, and parent-event correlation.
4. Document any lossy conversion between the AI event envelope and OCSF classes.

Do not publish an OCSF extension proposal until the first three reference cases identify the minimum fields that are repeatedly necessary.

## OpenTelemetry direction

OpenTelemetry trace context may provide cross-service correlation among agent runtimes, model gateways, retrieval services, tools, and downstream applications. Initial testing should evaluate:

- Trace and span identifiers as AIRG correlation anchors.
- GenAI semantic conventions for model and operation metadata.
- Span links for delegation and asynchronous child tasks.
- Events for approvals, memory access, and policy decisions where spans alone are insufficient.
- Sampling behavior and its effect on forensic completeness.

Telemetry optimized for performance monitoring may be sampled, mutable, or retained too briefly for evidence purposes. Observability records should therefore be treated as evidence inputs, not automatically as a protected evidentiary system.

