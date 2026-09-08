#!/usr/bin/env python3
"""Offline reference projections to OCSF 1.6.0 and the OTel Logs Data Model.

No events are transmitted. The original envelope remains in an explicit extension
so projection losses do not silently remove investigation evidence.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    from .evidence import read_json, validate_event, write_json
except ImportError:
    from evidence import read_json, validate_event, write_json


def unix_ns(value):
    """Parse RFC 3339 without floating point or invented time precision."""
    match = re.fullmatch(r"(\d{4}-\d\d-\d\d)[Tt](\d\d:\d\d:\d\d)(?:\.(\d+))?([Zz]|[+-]\d\d:\d\d)", value)
    if not match:
        raise ValueError("timestamp must include a numeric offset or Z")
    day, clock, fraction, zone = match.groups()
    fraction = fraction or ""
    if len(fraction) > 9:
        raise ValueError("timestamp precision exceeds nanoseconds; refusing truncation")
    # Leap seconds require an explicit provider time policy. Do not silently
    # normalize them into a different second.
    point = datetime.fromisoformat(day + "T" + clock + ("+00:00" if zone.lower() == "z" else zone))
    delta = point - datetime(1970, 1, 1, tzinfo=timezone.utc)
    ns = (delta.days * 86400 + delta.seconds) * 1_000_000_000 + int(fraction.ljust(9, "0") or "0")
    if ns < 0:
        raise ValueError("this export profile requires a nonnegative UNIX timestamp")
    return ns


def to_ocsf(event, source_endpoint_uid=None):
    validate_event(event)
    action = event.get("action", {})
    is_api = event["event_type"] in {"ai.tool.executed", "ai.tool.failed"} and bool(source_endpoint_uid)
    operation = action.get("operation")
    activities = {"read_document": 2, "read_report": 2, "delete_object": 4,
                  "move_object": 3, "close_ticket": 3, "reopen_ticket": 3}
    activity = activities.get(operation, 99) if is_api else 99
    class_uid = 6003 if is_api else 0
    losses = ["AI authority, influence, approval and validation fields remain in unmapped.ai_forensic_readiness."]
    if not is_api:
        losses.append("Base Event used: no API classification is asserted without an observed source endpoint and tool-execution event.")
    ns = unix_ns(event["timestamp"])
    if ns % 1_000_000:
        losses.append("OCSF time is truncated to milliseconds; the full source timestamp is preserved in the original envelope.")
    out = {"category_uid": 6 if is_api else 0, "class_uid": class_uid, "activity_id": activity,
           "type_uid": class_uid * 100 + activity, "severity_id": 0,
           "time": ns // 1_000_000, "message": event["event_type"],
           "metadata": {"version": "1.6.0", "uid": event["event_id"],
                        "product": {"name": "AI Forensic Readiness reference converter", "vendor_name": "AI Forensic Readiness", "version": "0.2.0-draft"},
                        "correlation_uid": event["correlation"]["trace_id"],
                        "original_time": event["timestamp"]},
           "unmapped": {"ai_forensic_readiness": copy.deepcopy(event), "mapping_notes": losses}}
    if is_api:
        if not operation:
            raise ValueError("API projection requires a recorded operation")
        principal = event["principal"]
        out.update({"actor": {"user": {"uid": principal.get("delegated_identity") or principal["runtime_identity"]}},
                    "api": {"operation": operation}, "src_endpoint": {"uid": source_endpoint_uid},
                    "status_id": {"succeeded": 1, "failed": 2, "denied": 2}.get(action.get("outcome"), 0)})
        if action.get("target"):
            out["resources"] = [{"uid": action["target"]}]
    return out


def to_otel(event):
    validate_event(event)
    attrs = {"afr.event_id": event["event_id"], "afr.schema_version": event["schema_version"],
             "afr.trace_id": event["correlation"]["trace_id"], "afr.session_id": event["correlation"]["session_id"],
             "afr.mapping_notes": ["Logical Logs Data Model JSON; not an OTLP wire payload.",
                                   "No sampling or span ancestry is invented; the original envelope remains in Body."]}
    out = {"Timestamp": str(unix_ns(event["timestamp"])), "EventName": event["event_type"],
           "Resource": {"service.name": event["principal"]["runtime_identity"]},
           "InstrumentationScope": {"name": "ai-forensic-readiness", "version": "0.2.0-draft"},
           "Attributes": attrs, "Body": {"ai_forensic_readiness": copy.deepcopy(event)}}
    if event.get("observed_at"):
        out["ObservedTimestamp"] = str(unix_ns(event["observed_at"]))
    trace_id = event["correlation"]["trace_id"]
    # The existing fixture's identifiers such as trace-case-001 are correlation
    # keys, not W3C TraceIds. Hashing them would falsely invent trace provenance.
    if re.fullmatch(r"[a-f0-9]{32}", trace_id) and int(trace_id, 16):
        out["TraceId"] = trace_id
        span_id = event["correlation"].get("span_id")
        if span_id and re.fullmatch(r"[a-f0-9]{16}", span_id) and int(span_id, 16):
            out["SpanId"] = span_id
    else:
        attrs["afr.mapping_notes"].append("Source trace ID is not a valid W3C TraceId; retained only as afr.trace_id.")
    return out


def restore(projected, target):
    if target == "ocsf":
        event = projected["unmapped"]["ai_forensic_readiness"]
    elif target == "otel":
        event = projected["Body"]["ai_forensic_readiness"]
    else:
        raise ValueError("target must be ocsf or otel")
    validate_event(event)
    return copy.deepcopy(event)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--format", choices=["ocsf", "otel"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-endpoint-uid", help="OCSF API projection only; must identify an independently observed source endpoint")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists; choose a new path")
    events = read_json(args.input)
    if not isinstance(events, list):
        events = [events]
    result = [to_ocsf(e, args.source_endpoint_uid) if args.format == "ocsf" else to_otel(e) for e in events]
    write_json(args.output, result)
    print(f"Wrote {len(result)} reference projections to {args.output}; no telemetry was sent")


if __name__ == "__main__":
    main()
