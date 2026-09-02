#!/usr/bin/env python3
"""Dependency-free repository checks for the v0.1 discussion draft."""

from __future__ import annotations

import json
import hashlib
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_001 = ROOT / "cases" / "case-001-prompt-injection-tool-abuse"


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")


def load_jsonl(path: Path) -> list[dict]:
    records = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except Exception as exc:
            fail(f"{path.relative_to(ROOT)}:{number}: invalid JSONL: {exc}")
        if not isinstance(record, dict):
            fail(f"{path.relative_to(ROOT)}:{number}: JSONL record must be an object")
        records.append(record)
    if not records:
        fail(f"{path.relative_to(ROOT)}: JSONL file is empty")
    return records


def validate_event(schema: dict, event: dict) -> None:
    if not isinstance(event, dict):
        fail("event example: event must be an object")
    allowed = set(schema["properties"])
    extra = set(event) - allowed
    if extra:
        fail(f"event example: unexpected properties: {sorted(extra)}")
    missing = set(schema["required"]) - set(event)
    if missing:
        fail(f"event example: missing properties: {sorted(missing)}")
    if event["schema_version"] != schema["properties"]["schema_version"]["const"]:
        fail("event example: schema_version does not match schema")
    permitted = set(schema["properties"]["event_type"]["enum"])
    if event["event_type"] not in permitted:
        fail("event example: event_type is not permitted")
    for key in ("timestamp", "observed_at"):
        if key in event:
            datetime.fromisoformat(event[key].replace("Z", "+00:00"))
    for group, value in event.items():
        definition = schema["properties"][group]
        if definition.get("type") != "object":
            continue
        if not isinstance(value, dict):
            fail(f"event example: {group} must be an object")
        missing_nested = set(definition.get("required", [])) - set(value)
        if missing_nested:
            fail(f"event example: {group} missing {sorted(missing_nested)}")
        extra_nested = set(value) - set(definition["properties"])
        if extra_nested:
            fail(f"event example: {group} has unexpected {sorted(extra_nested)}")
        for key, nested_value in value.items():
            permitted_values = definition["properties"][key].get("enum")
            if permitted_values and nested_value not in permitted_values:
                fail(f"event example: {group}.{key} is not permitted")


def validate_case_001(schema: dict) -> int:
    required_files = {
        "README.md",
        "scenario.md",
        "analyst-guide.md",
        "airg.md",
        "findings.md",
        "reproduce.md",
        "manifest.json",
        "evidence/README.md",
        "evidence/normalized/events.json",
    }
    missing_files = sorted(path for path in required_files if not (CASE_001 / path).is_file())
    if missing_files:
        fail(f"Case 001: missing required files: {missing_files}")

    events = load_json(CASE_001 / "evidence" / "normalized" / "events.json")
    if not isinstance(events, list) or not events:
        fail("Case 001: normalized events must be a non-empty array")

    seen_ids: set[str] = set()
    seen_sequences: set[int] = set()
    previous_time = None
    expected_trace = "trace-case-001"
    expected_session = "session-synthetic-001"

    for event in events:
        validate_event(schema, event)
        event_id = event["event_id"]
        sequence = event.get("sequence")
        if event_id in seen_ids:
            fail(f"Case 001: duplicate event_id {event_id}")
        if sequence in seen_sequences:
            fail(f"Case 001: duplicate sequence {sequence}")
        parent = event["correlation"].get("parent_event_id")
        if parent and parent not in seen_ids:
            fail(f"Case 001: {event_id} references unknown or later parent {parent}")
        if event["correlation"]["trace_id"] != expected_trace:
            fail(f"Case 001: {event_id} has an unexpected trace_id")
        if event["correlation"]["session_id"] != expected_session:
            fail(f"Case 001: {event_id} has an unexpected session_id")
        event_time = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
        if previous_time and event_time < previous_time:
            fail(f"Case 001: {event_id} is out of timestamp order")
        previous_time = event_time
        seen_ids.add(event_id)
        seen_sequences.add(sequence)

    if sorted(seen_sequences) != list(range(1, len(events) + 1)):
        fail("Case 001: sequence values must be contiguous and start at 1")

    required_types = {
        "ai.instruction.received",
        "ai.context.retrieved",
        "ai.plan.created",
        "ai.policy.evaluated",
        "ai.tool.requested",
        "ai.tool.authorized",
        "ai.tool.executed",
        "ai.delegation.created",
        "ai.delegation.revoked",
        "ai.state.changed",
        "ai.state.validated",
        "ai.evidence.exported",
        "ai.evidence.sealed",
    }
    observed_types = {event["event_type"] for event in events}
    missing_types = sorted(required_types - observed_types)
    if missing_types:
        fail(f"Case 001: missing required event types: {missing_types}")
    return len(events)


def validate_case_001_manifest() -> int:
    manifest = load_json(CASE_001 / "manifest.json")
    required = {"case_id", "generated_at", "synthetic_data", "artifacts"}
    missing = required - set(manifest)
    if missing:
        fail(f"Case 001 manifest: missing fields {sorted(missing)}")
    if manifest["case_id"] != "case-001" or manifest["synthetic_data"] is not True:
        fail("Case 001 manifest: invalid case identity or synthetic_data flag")
    datetime.fromisoformat(manifest["generated_at"].replace("Z", "+00:00"))

    artifacts = manifest["artifacts"]
    if not isinstance(artifacts, list) or not artifacts:
        fail("Case 001 manifest: artifacts must be a non-empty array")

    manifested_paths: set[str] = set()
    for artifact in artifacts:
        required_artifact = {"path", "media_type", "sha256", "source", "collection_time"}
        missing_artifact = required_artifact - set(artifact)
        if missing_artifact:
            fail(f"Case 001 manifest: artifact missing {sorted(missing_artifact)}")
        relative_path = artifact["path"]
        if relative_path in manifested_paths:
            fail(f"Case 001 manifest: duplicate path {relative_path}")
        candidate = (CASE_001 / relative_path).resolve()
        if CASE_001.resolve() not in candidate.parents or not candidate.is_file():
            fail(f"Case 001 manifest: unsafe or missing path {relative_path}")
        expected_hash = artifact["sha256"].lower()
        if not re.fullmatch(r"[a-f0-9]{64}", expected_hash):
            fail(f"Case 001 manifest: invalid SHA-256 for {relative_path}")
        actual_hash = hashlib.sha256(candidate.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            fail(f"Case 001 manifest: SHA-256 mismatch for {relative_path}")
        datetime.fromisoformat(artifact["collection_time"].replace("Z", "+00:00"))
        manifested_paths.add(relative_path)

    evidence_paths = {
        path.relative_to(CASE_001).as_posix()
        for path in (CASE_001 / "evidence").rglob("*")
        if path.is_file()
    }
    if manifested_paths != evidence_paths:
        missing_from_manifest = sorted(evidence_paths - manifested_paths)
        absent_from_disk = sorted(manifested_paths - evidence_paths)
        fail(
            "Case 001 manifest coverage mismatch: "
            f"unmanifested={missing_from_manifest}, missing={absent_from_disk}"
        )
    return len(artifacts)


def validate_case_001_consistency() -> None:
    raw = CASE_001 / "evidence" / "raw"
    user_record = load_json(raw / "user-instruction.json")
    retrieval_record = load_json(raw / "retrieved-content.json")
    deployment = load_json(raw / "deployment-manifest.json")
    state_before = load_json(raw / "state-before.json")
    state_after = load_json(raw / "state-after.json")
    containment = load_json(raw / "containment-validation.json")
    tool_records = load_jsonl(raw / "tool-gateway.jsonl")
    downstream_records = load_jsonl(raw / "downstream-audit.jsonl")
    egress_records = load_jsonl(raw / "network-egress.jsonl")

    instruction_hash = hashlib.sha256(user_record["instruction"].encode("utf-8")).hexdigest()
    if instruction_hash != user_record["instruction_sha256"]:
        fail("Case 001: user-instruction content digest mismatch")
    retrieval_hash = hashlib.sha256(retrieval_record["content"].encode("utf-8")).hexdigest()
    if retrieval_hash != retrieval_record["content_sha256"]:
        fail("Case 001: retrieved-content digest mismatch")

    document_hash = state_before["restricted_document"]["content_sha256"]
    observed_payload_hashes = {
        record[key]
        for record in tool_records + downstream_records + egress_records
        for key in ("content_sha256", "result_sha256", "payload_sha256")
        if key in record
    }
    if observed_payload_hashes != {document_hash}:
        fail("Case 001: cross-source document/payload digests do not agree")

    after_action = state_after["after_action"]
    after_containment = state_after["after_containment"]
    if after_action["external_copies"][0]["payload_sha256"] != document_hash:
        fail("Case 001: after-action external copy digest mismatch")
    if after_containment["external_copies"][0]["payload_sha256"] != document_hash:
        fail("Case 001: post-containment external copy digest mismatch")
    if after_containment["external_copies"][0]["disposition"] != "unknown":
        fail("Case 001: retrospective external-copy disposition must remain unknown")

    scopes = set(deployment["delegated_identity"]["eligible_scopes"])
    if scopes != {"documents:read", "webhook:send"}:
        fail("Case 001: delegated scope fixture is inconsistent")
    if containment["prospective_revocation"] != "confirmed":
        fail("Case 001: prospective revocation is not confirmed")
    if containment["retrospective_disposition"] != "unresolved":
        fail("Case 001: retrospective disposition must remain unresolved")
    denied_replay = any(
        result.get("validation_id") == "validate-0001"
        and result.get("expected") == "deny"
        and result.get("observed") == "deny"
        for result in containment["validation"]
    )
    if not denied_replay:
        fail("Case 001: independent denied-replay validation is missing")

    case_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in CASE_001.rglob("*")
        if path.is_file()
    )
    non_lab_urls = [
        url
        for url in re.findall(r"https://[^\s\"'`)]+", case_text)
        if not url.startswith(("https://research.example.invalid/", "https://collector.invalid/"))
    ]
    if non_lab_urls:
        fail(f"Case 001: unexpected network destination(s): {sorted(set(non_lab_urls))}")


def validate_markdown_links() -> None:
    link_pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    failures = []
    for path in ROOT.rglob("*.md"):
        for target in link_pattern.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0]
            if clean and not (path.parent / clean).resolve().exists():
                failures.append(f"{path.relative_to(ROOT)} -> {target}")
    if failures:
        fail("broken local links:\n" + "\n".join(failures))


def main() -> int:
    for path in ROOT.rglob("*.json"):
        load_json(path)
    jsonl_records = 0
    for path in ROOT.rglob("*.jsonl"):
        jsonl_records += len(load_jsonl(path))
    schema = load_json(ROOT / "schemas" / "ai-investigation-event.schema.json")
    event = load_json(ROOT / "schemas" / "examples" / "tool-executed.valid.json")
    validate_event(schema, event)
    case_event_count = validate_case_001(schema)
    manifested_artifact_count = validate_case_001_manifest()
    validate_case_001_consistency()
    validate_markdown_links()
    print("JSON syntax: OK")
    print(f"JSONL syntax: OK ({jsonl_records} records)")
    print("AI event example: structurally valid for v0.1")
    print(f"Case 001 normalized events: OK ({case_event_count} events)")
    print(f"Case 001 evidence manifest: OK ({manifested_artifact_count} artifacts)")
    print("Case 001 cross-source consistency: OK")
    print("Local Markdown links: OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
