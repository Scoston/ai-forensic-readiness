# Interoperability mappings

These are implemented reference projections for local evaluation. They do not
register an OCSF extension or claim certified compatibility with a collector.
The [converter](../scripts/convert_events.py) validates the source, writes a local
file and preserves the original envelope. It never transmits telemetry.

## OCSF 1.6.0 profile

The initial profile pins OCSF **1.6.0** rather than silently following upstream changes.
[API Activity](https://github.com/ocsf/ocsf-schema/blob/v1.6.0/events/application/api_activity.json)
and [Base Event](https://github.com/ocsf/ocsf-schema/blob/v1.6.0/events/base_event.json)
are the relevant classes. [Metadata](https://github.com/ocsf/ocsf-schema/blob/v1.6.0/objects/metadata.json)
and the [dictionary](https://github.com/ocsf/ocsf-schema/blob/v1.6.0/dictionary.json)
define reused correlation and time fields. Sources reviewed September 8, 2026.

| Source | OCSF target | Rule and limit |
| --- | --- | --- |
| Event ID | metadata.uid | Preserve original identifier |
| Timestamp | time, metadata.original_time | Integer milliseconds plus original string; disclose discarded submillisecond precision |
| Trace identifier | metadata.correlation_uid | Correlation identifier, without inventing W3C context |
| Tool completion/failure plus observed network source | class_uid 6003, category_uid 6 | API Activity only when required source semantics exist |
| Other events, including authorization-only | class_uid 0, category_uid 0 | Base Event with activity Other; no completed API claim |
| Known CRUD operation | activity_id, type_uid | Explicit operation table; otherwise Other; type is class times 100 plus activity |
| Executing delegated or runtime identity | actor.user.uid | API projection; human requester remains in original envelope |
| Operation | api.operation | Preserve operation name |
| Observed network source supplied by caller | src_endpoint.uid | Never infer an IP or endpoint from an agent name |
| Target | resources[].uid | Preserve observed target |
| Execution outcome | status_id | Success 1; failure/denial 2; otherwise unknown 0 |
| No source severity | severity_id 0 | Unknown; do not infer severity from execution |
| All AI fields | unmapped.ai_forensic_readiness | Original envelope; not an official AI extension |

Examples: [Base Event](examples/ocsf-base.json),
[API projection with a synthetic observed endpoint](examples/ocsf-api.json).

```bash
python scripts/convert_events.py schemas/examples/v02/tool-executed.valid.json --format ocsf --output dist/ocsf.json
```

Supply `--source-endpoint-uid` only when an authoritative source identifies that
network endpoint. The example's endpoint is synthetic and is not inferred from
the source event. Destination, HTTP and cloud details are absent from that fixture.

## OpenTelemetry Logs Data Model profile

This profile uses the stable [Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/)
reviewed September 8, 2026. The JSON is a readable representation of that logical
model, **not an OTLP JSON or Protobuf wire payload**. An SDK/collector adapter must
perform transport encoding and destination integration.

| Source | Logical target | Rule and limit |
| --- | --- | --- |
| Timestamp | Timestamp | Exact nonnegative UNIX nanoseconds encoded as a decimal string |
| Observed time | ObservedTimestamp | Set only when present |
| Event type | EventName | Preserve event identity |
| Runtime identity | Resource.service.name | Logical source workload |
| Valid, nonzero W3C trace ID | TraceId | Pass through 32 lowercase hexadecimal characters |
| Valid span ID with valid trace ID | SpanId | Pass through 16 lowercase hexadecimal characters |
| Human-readable trace/session IDs | Attributes.afr.trace_id, afr.session_id | Project attributes; never hash them into invented trace IDs |
| Original event | Body.ai_forensic_readiness | Preserve all evidence fields |

Example: [OTel logical log record](examples/otel-log.json).

```bash
python scripts/convert_events.py schemas/examples/v02/tool-executed.valid.json --format otel --output dist/otel.json
```

No trace flags, sampling decisions, parent spans or span links are synthesized.
Asynchronous delegation needs real instrumentation and observed span links. GenAI
semantic conventions are evolving; this initial projection uses project-namespaced
attributes rather than claiming a current GenAI agent-span implementation.

## Loss and validation boundary

Dropping the original envelope loses AI-specific semantics. Keeping it permits
exact restoration, but that only verifies source preservation; it does not prove
a SIEM indexes those fields, an OTLP endpoint accepts the logical JSON, or
independent systems corroborate the evidence.

Tests check timestamps without floating-point rounding, rejected excess precision,
trace-ID handling, operation/classification semantics and round trips. Project-owned
projection schemas validate the supported local shapes; they do not substitute
for full upstream schemas or live integration tests.

Content handling and retention apply to exports as well as originals. Only send
production-derived exports to destinations authorized for their metadata and
references. No production data is present in these examples.
