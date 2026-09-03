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
CASE_002 = ROOT / "cases" / "case-002-persistent-memory-poisoning"


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


def validate_case_002(schema: dict) -> int:
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
    missing_files = sorted(path for path in required_files if not (CASE_002 / path).is_file())
    if missing_files:
        fail(f"Case 002: missing required files: {missing_files}")

    events = load_json(CASE_002 / "evidence" / "normalized" / "events.json")
    if not isinstance(events, list) or not events:
        fail("Case 002: normalized events must be a non-empty array")

    valid_trace_sessions = {
        "trace-case-002-seed": "session-memory-seed-002",
        "trace-case-002-source-removal": "session-source-removal-002",
        "trace-case-002-trigger": "session-memory-trigger-002",
        "trace-case-002-response": "session-memory-response-002",
        "trace-case-002-replay": "session-memory-replay-002",
    }
    seen_ids: set[str] = set()
    seen_sequences: set[int] = set()
    previous_time = None

    for event in events:
        validate_event(schema, event)
        event_id = event["event_id"]
        sequence = event.get("sequence")
        if not event_id.startswith("evt2-"):
            fail(f"Case 002: unexpected event_id format {event_id}")
        if event_id in seen_ids:
            fail(f"Case 002: duplicate event_id {event_id}")
        if sequence in seen_sequences:
            fail(f"Case 002: duplicate sequence {sequence}")
        parent = event["correlation"].get("parent_event_id")
        if parent and parent not in seen_ids:
            fail(f"Case 002: {event_id} references unknown or later parent {parent}")
        trace_id = event["correlation"]["trace_id"]
        session_id = event["correlation"]["session_id"]
        if valid_trace_sessions.get(trace_id) != session_id:
            fail(f"Case 002: {event_id} has an unexpected trace/session pair")
        event_time = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
        if previous_time and event_time < previous_time:
            fail(f"Case 002: {event_id} is out of timestamp order")
        previous_time = event_time
        seen_ids.add(event_id)
        seen_sequences.add(sequence)

    if sorted(seen_sequences) != list(range(1, len(events) + 1)):
        fail("Case 002: sequence values must be contiguous and start at 1")
    observed_traces = {event["correlation"]["trace_id"] for event in events}
    if observed_traces != set(valid_trace_sessions):
        fail("Case 002: normalized events do not cover all expected traces")

    required_types = {
        "ai.session.started",
        "ai.session.ended",
        "ai.instruction.received",
        "ai.instruction.transformed",
        "ai.context.retrieved",
        "ai.context.filtered",
        "ai.memory.read",
        "ai.memory.written",
        "ai.memory.deleted",
        "ai.plan.created",
        "ai.plan.revised",
        "ai.policy.evaluated",
        "ai.tool.requested",
        "ai.tool.authorized",
        "ai.tool.executed",
        "ai.state.changed",
        "ai.state.compensated",
        "ai.state.validated",
        "ai.evidence.exported",
        "ai.evidence.sealed",
    }
    observed_types = {event["event_type"] for event in events}
    missing_types = sorted(required_types - observed_types)
    if missing_types:
        fail(f"Case 002: missing required event types: {missing_types}")
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


def validate_case_002_manifest() -> int:
    manifest = load_json(CASE_002 / "manifest.json")
    required = {"case_id", "generated_at", "synthetic_data", "artifacts"}
    missing = required - set(manifest)
    if missing:
        fail(f"Case 002 manifest: missing fields {sorted(missing)}")
    if manifest["case_id"] != "case-002" or manifest["synthetic_data"] is not True:
        fail("Case 002 manifest: invalid case identity or synthetic_data flag")
    datetime.fromisoformat(manifest["generated_at"].replace("Z", "+00:00"))

    artifacts = manifest["artifacts"]
    if not isinstance(artifacts, list) or not artifacts:
        fail("Case 002 manifest: artifacts must be a non-empty array")

    manifested_paths: set[str] = set()
    for artifact in artifacts:
        required_artifact = {"path", "media_type", "sha256", "source", "collection_time"}
        missing_artifact = required_artifact - set(artifact)
        if missing_artifact:
            fail(f"Case 002 manifest: artifact missing {sorted(missing_artifact)}")
        relative_path = artifact["path"]
        if relative_path in manifested_paths:
            fail(f"Case 002 manifest: duplicate path {relative_path}")
        candidate = (CASE_002 / relative_path).resolve()
        if CASE_002.resolve() not in candidate.parents or not candidate.is_file():
            fail(f"Case 002 manifest: unsafe or missing path {relative_path}")
        expected_hash = artifact["sha256"].lower()
        if not re.fullmatch(r"[a-f0-9]{64}", expected_hash):
            fail(f"Case 002 manifest: invalid SHA-256 for {relative_path}")
        actual_hash = hashlib.sha256(candidate.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            fail(f"Case 002 manifest: SHA-256 mismatch for {relative_path}")
        datetime.fromisoformat(artifact["collection_time"].replace("Z", "+00:00"))
        manifested_paths.add(relative_path)

    evidence_paths = {
        path.relative_to(CASE_002).as_posix()
        for path in (CASE_002 / "evidence").rglob("*")
        if path.is_file()
    }
    if manifested_paths != evidence_paths:
        missing_from_manifest = sorted(evidence_paths - manifested_paths)
        absent_from_disk = sorted(manifested_paths - evidence_paths)
        fail(
            "Case 002 manifest coverage mismatch: "
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


def validate_case_002_consistency() -> None:
    raw = CASE_002 / "evidence" / "raw"
    instructions = load_jsonl(raw / "user-instructions.jsonl")
    retrieval = load_json(raw / "retrieved-content.json")
    deployment = load_json(raw / "deployment-manifest.json")
    state_before = load_json(raw / "state-before.json")
    state_after = load_json(raw / "state-after.json")
    replay = load_json(raw / "replay-results.json")
    containment = load_json(raw / "containment-validation.json")
    agent_records = load_jsonl(raw / "agent-runtime.jsonl")
    memory_records = load_jsonl(raw / "memory-audit.jsonl")
    source_records = load_jsonl(raw / "source-control.jsonl")
    authorization_records = load_jsonl(raw / "authorization.jsonl")
    tool_records = load_jsonl(raw / "tool-gateway.jsonl")
    downstream_records = load_jsonl(raw / "downstream-audit.jsonl")
    normalized_events = load_json(CASE_002 / "evidence" / "normalized" / "events.json")

    for record in instructions:
        instruction_hash = hashlib.sha256(record["instruction"].encode("utf-8")).hexdigest()
        if instruction_hash != record["instruction_sha256"]:
            fail(f"Case 002: instruction digest mismatch for {record['record_id']}")
    instruction_by_id = {record["record_id"]: record for record in instructions}
    if instruction_by_id["instr-trigger-0002"]["instruction_sha256"] != instruction_by_id["instr-replay-0002"]["instruction_sha256"]:
        fail("Case 002: trigger and replay instructions differ")

    retrieval_hash = hashlib.sha256(retrieval["content"].encode("utf-8")).hexdigest()
    if retrieval_hash != retrieval["content_sha256"]:
        fail("Case 002: retrieved-content digest mismatch")
    derived_value = retrieval["embedded_directive"]["derived_value"]
    value_hash = hashlib.sha256(derived_value.encode("utf-8")).hexdigest()

    writes = [record for record in memory_records if record["record_type"] == "memory_write"]
    reads = [record for record in memory_records if record["record_type"] == "memory_read"]
    indexes = [record for record in memory_records if record["record_type"] == "memory_index"]
    if len(writes) != 1 or len(reads) != 1 or len(indexes) != 1:
        fail("Case 002: expected one authoritative memory write, index, and incident read")
    write, read, index = writes[0], reads[0], indexes[0]
    if write["source_content_sha256"] != retrieval["content_sha256"]:
        fail("Case 002: source-to-memory content digest mismatch")
    if {write["value_sha256"], read["value_sha256"], index["value_sha256"]} != {value_hash}:
        fail("Case 002: memory value digests do not agree")
    if write["source_trust_label"] != "untrusted-web" or write["assigned_trust_label"] != "trusted-shared":
        fail("Case 002: trust-boundary fixture is inconsistent")

    source_removal = next(
        record for record in source_records
        if record.get("action") == "remove-and-block" and record.get("outcome") == "removed"
    )
    removal_time = datetime.fromisoformat(source_removal["timestamp"].replace("Z", "+00:00"))
    read_time = datetime.fromisoformat(read["timestamp"].replace("Z", "+00:00"))
    if removal_time >= read_time:
        fail("Case 002: source removal must precede the delayed memory read")

    agent_context = next(
        record for record in agent_records if record.get("event") == "memory_context_injected"
    )
    if agent_context["value_sha256"] != value_hash or agent_context["memory_id"] != "memory-0002":
        fail("Case 002: agent memory-context record does not match the stored assertion")

    close_tool = next(record for record in tool_records if record["operation"] == "close_ticket")
    reopen_tool = next(record for record in tool_records if record["operation"] == "reopen_ticket")
    close_request = next(
        record for record in agent_records
        if record.get("event") == "tool_requested" and record.get("operation") == "close_ticket"
    )
    close_arguments = {
        "classification": close_request["classification"],
        "operation": close_request["operation"],
        "target": close_request["target"],
    }
    close_arguments_digest = "sha256:" + hashlib.sha256(
        json.dumps(close_arguments, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    reopen_arguments = {"operation": "reopen_ticket", "target": reopen_tool["target"]}
    reopen_arguments_digest = "sha256:" + hashlib.sha256(
        json.dumps(reopen_arguments, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    normalized_close_digests = {
        event["action"]["arguments_digest"]
        for event in normalized_events
        if event.get("action", {}).get("operation") == "close_ticket"
    }
    normalized_reopen_digests = {
        event["action"]["arguments_digest"]
        for event in normalized_events
        if event.get("action", {}).get("operation") == "reopen_ticket"
    }
    if normalized_close_digests != {close_arguments_digest}:
        fail("Case 002: normalized close-ticket argument digests are inconsistent")
    if normalized_reopen_digests != {reopen_arguments_digest}:
        fail("Case 002: normalized reopen-ticket argument digest is inconsistent")
    close_audit = next(record for record in downstream_records if record.get("operation") == "close")
    reopen_audit = next(record for record in downstream_records if record.get("operation") == "reopen")
    before_ticket = state_before["before_trigger"]["ticket"]
    action_ticket = state_after["after_action"]["ticket"]
    restored_ticket = state_after["after_containment"]["ticket"]
    if close_tool["result_sha256"] != close_audit["state_sha256"] or close_audit["state_sha256"] != action_ticket["state_sha256"]:
        fail("Case 002: ticket-close state digests do not agree")
    if reopen_tool["result_sha256"] != reopen_audit["state_sha256"] or reopen_audit["state_sha256"] != restored_ticket["state_sha256"]:
        fail("Case 002: ticket-reopen state digests do not agree")
    if before_ticket["state_sha256"] != restored_ticket["state_sha256"]:
        fail("Case 002: restored ticket does not match the authoritative pre-action state")
    if action_ticket["state"] != "closed" or restored_ticket["state"] != "open":
        fail("Case 002: ticket state transition or restoration is inconsistent")

    policy_allow = next(record for record in authorization_records if record.get("decision") == "allow")
    if policy_allow["evaluated_attributes"]["classification"]["source"] != "memory-0002":
        fail("Case 002: policy allow decision is not tied to the poisoned memory")
    policy_validation = next(record for record in authorization_records if record["record_type"] == "policy_validation")
    if policy_validation["expected"] != "deny" or policy_validation["observed"] != "deny":
        fail("Case 002: post-containment policy denial is not validated")

    if replay["changed_variable"] != "active_memory_availability":
        fail("Case 002: controlled replay changes an unexpected variable")
    if replay["controlled_variables"]["instruction_sha256"] != instruction_by_id["instr-trigger-0002"]["instruction_sha256"]:
        fail("Case 002: controlled replay instruction does not match the trigger")
    conditions = {condition["condition"]: condition for condition in replay["conditions"]}
    if set(conditions) != {"poisoned", "quarantined"}:
        fail("Case 002: controlled replay must contain poisoned and quarantined conditions")
    poisoned = conditions["poisoned"]
    quarantined = conditions["quarantined"]
    if poisoned["retrieved_memory_ids"] != ["memory-0002"] or poisoned["plan_operation"] != "close_ticket" or poisoned["tool_call_generated"] is not True:
        fail("Case 002: poisoned replay condition is inconsistent")
    if quarantined["retrieved_memory_ids"] or quarantined["plan_operation"] != "report_status" or quarantined["tool_call_generated"] is not False:
        fail("Case 002: quarantined replay condition is inconsistent")
    if poisoned["tool_executed"] is not False or quarantined["tool_executed"] is not False:
        fail("Case 002: controlled replay must not execute a consequential tool")

    expected_consumers = set(deployment["memory"]["known_consumers"])
    inventory = set(containment["known_consumer_inventory"]["consumers"])
    if inventory != expected_consumers:
        fail("Case 002: containment consumer inventory does not match deployment")
    consumer_validations = {
        record["consumer"]: (record["expected"], record["observed"])
        for record in memory_records
        if record["record_type"] == "consumer_validation"
    }
    if set(consumer_validations) != expected_consumers:
        fail("Case 002: one or more known consumers lack independent validation")
    if any(expected != observed for expected, observed in consumer_validations.values()):
        fail("Case 002: known-consumer validation did not match expectations")

    after_containment = state_after["after_containment"]
    if after_containment["active_memory_ids"] or after_containment["vector_entry_ids"] or after_containment["cache_entry_ids"]:
        fail("Case 002: active memory derivatives remain after containment")
    if after_containment["forensic_quarantine_ids"] != ["quarantine-memory-0002"]:
        fail("Case 002: poisoned evidence was not preserved in forensic quarantine")
    if containment["active_retrieval_paths"] != "confirmed-removed-for-known-consumers":
        fail("Case 002: known active retrieval paths are not confirmed removed")
    if containment["historical_undocumented_consumption"] != "unresolved":
        fail("Case 002: undocumented historical consumption must remain unresolved")

    case_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in CASE_002.rglob("*")
        if path.is_file()
    )
    if "TO_FILL" in case_text:
        fail("Case 002: unresolved placeholder detected")
    non_lab_urls = [
        url
        for url in re.findall(r"https://[^\s\"'`)]+", case_text)
        if not url.startswith("https://knowledge.example.invalid/")
    ]
    if non_lab_urls:
        fail(f"Case 002: unexpected network destination(s): {sorted(set(non_lab_urls))}")


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
    case_001_event_count = validate_case_001(schema)
    case_001_manifested_artifact_count = validate_case_001_manifest()
    validate_case_001_consistency()
    case_002_event_count = validate_case_002(schema)
    case_002_manifested_artifact_count = validate_case_002_manifest()
    validate_case_002_consistency()
    validate_markdown_links()
    print("JSON syntax: OK")
    print(f"JSONL syntax: OK ({jsonl_records} records)")
    print("AI event example: structurally valid for v0.1")
    print(f"Case 001 normalized events: OK ({case_001_event_count} events)")
    print(f"Case 001 evidence manifest: OK ({case_001_manifested_artifact_count} artifacts)")
    print("Case 001 cross-source consistency: OK")
    print(f"Case 002 normalized events: OK ({case_002_event_count} events)")
    print(f"Case 002 evidence manifest: OK ({case_002_manifested_artifact_count} artifacts)")
    print("Case 002 cross-source and replay consistency: OK")
    print("Local Markdown links: OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
