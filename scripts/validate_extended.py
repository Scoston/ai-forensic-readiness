"""Conformance, manifest, evidence-link and simulation gates for the review build."""
from __future__ import annotations

try:
    from .evidence import ROOT, read_json, loads, validate_schema, validate_event, validate_trajectory, validate_manifest, validate_graph, safe_path, digest
    from .simulations import run
    from .convert_events import to_ocsf, to_otel, restore
except ImportError:
    from evidence import ROOT, read_json, loads, validate_schema, validate_event, validate_trajectory, validate_manifest, validate_graph, safe_path, digest
    from simulations import run
    from convert_events import to_ocsf, to_otel, restore


def check_records(events, records, case_dir):
    by_id = {r["record_id"]: r for r in records}
    if len(by_id) != len(records):
        raise ValueError("duplicate raw record ID")
    if len(events) != len(records):
        raise ValueError("normalized/raw record coverage mismatch")
    for event in events:
        path, rid = event["evidence_refs"][0].split("#", 1)
        referenced_file = safe_path(case_dir, path)
        if rid not in by_id:
            raise ValueError("event references unknown raw record")
        record = by_id[rid]
        referenced_records = [loads(line) for line in referenced_file.read_text().splitlines() if line.strip()]
        if [r for r in referenced_records if r.get("record_id") == rid] != [record]:
            raise ValueError("evidence reference does not resolve to the cited raw record")
        if event["integrity"]["hash"] != digest(record):
            raise ValueError("normalized record digest mismatch")
        for field in ("event_id", "event_type", "timestamp"):
            if event[field] != record[field]:
                raise ValueError(f"raw/normalized {field} mismatch")
        if event["integrity"]["collector"] != record["source"]:
            raise ValueError("raw/normalized source mismatch")
        if event["correlation"].get("parent_event_id") != record["parent_event_id"]:
            raise ValueError("raw/normalized parent mismatch")
        for group, value in record["normalized_groups"].items():
            if event.get(group) != value:
                raise ValueError(f"raw/normalized {group} mismatch")


def validate_all():
    examples = read_json(ROOT / "schemas/conformance.json")
    for example in examples:
        event = read_json(ROOT / example["path"])
        try:
            validate_event(event)
            accepted = True
        except ValueError:
            accepted = False
        if accepted != example["valid"]:
            raise ValueError(f"conformance expectation failed: {example['path']}")
    total_events, total_artifacts = 0, 0
    for folder in sorted((ROOT / "cases").glob("case-*")):
        total_artifacts += validate_manifest(folder)
        number = int(folder.name[5:8])
        failure_events = read_json(folder / "evidence/normalized/events.json")
        validate_trajectory(failure_events)
        total_events += len(failure_events)
        if number < 4:
            continue
        for control in (False, True):
            record_file = "records-control" if control else "records"
            event_file = "control-events" if control else "events"
            records = [loads(line) for line in (folder / f"evidence/raw/{record_file}.jsonl").read_text().splitlines()]
            events = read_json(folder / f"evidence/normalized/{event_file}.json")
            validate_trajectory(events)
            check_records(events, records, folder)
            result = run(number, control)
            if result["records"] != records or result["events"] != events:
                raise ValueError(f"case {number}: recorded experiment differs from execution")
            if control:
                total_events += len(events)
        graph = read_json(folder / "evidence/airg.json")
        records = run(number)["records"]
        validate_graph(graph, failure_events, records)
        by_record = {r["record_id"]: r for r in records}
        for edge in graph["edges"]:
            if edge["relationship"] == "recorded_parent":
                if not any(by_record[r]["event_id"] == edge["target"] and by_record[r]["parent_event_id"] == edge["source"] for r in edge["record_ids"]):
                    raise ValueError("AIRG parent edge cites unrelated evidence")
    for number in range(1, 11):
        for control in (False, True):
            for event in run(number, control)["events"]:
                for target, convert in (("ocsf", to_ocsf), ("otel", to_otel)):
                    projected = convert(event)
                    shape = "ocsf-projection" if target == "ocsf" else "otel-log-projection"
                    validate_schema(read_json(ROOT / f"mappings/{shape}.schema.json"), projected, target)
                    if restore(projected, target) != event:
                        raise ValueError(f"{target}: source envelope was not preserved")
    for name, target in (("ocsf-base", "ocsf"), ("ocsf-api", "ocsf"), ("otel-log", "otel")):
        projected = read_json(ROOT / f"mappings/examples/{name}.json")
        shape = "ocsf-projection" if target == "ocsf" else "otel-log-projection"
        validate_schema(read_json(ROOT / f"mappings/{shape}.schema.json"), projected)
        if target == "ocsf" and projected["type_uid"] != projected["class_uid"] * 100 + projected["activity_id"]:
            raise ValueError("OCSF type identifier mismatch")
    import hashlib
    for asset in read_json(ROOT / "release/pdf-manifest.json")["assets"]:
        for key in ("source", "pdf"):
            if hashlib.sha256(safe_path(ROOT, asset[key]).read_bytes()).hexdigest() != asset[f"{key}_sha256"]:
                raise ValueError("PDF or source changed without rebuilding its manifest")
    print(f"JSON Schema conformance: OK ({len(examples)} positive/negative fixtures)")
    print(f"All ten case manifests: OK ({total_artifacts} artifacts)")
    print(f"All case trajectories: OK ({total_events} committed events)")
    print("Simulation results, raw/normalized links and AIRG evidence: OK")
    print("OCSF and OTel source-envelope round trips: OK (20 scenario conditions)")


if __name__ == "__main__":
    validate_all()
