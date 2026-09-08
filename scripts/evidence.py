"""Offline schema, manifest and reconstruction checks. No evidence is executed."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from functools import lru_cache


ROOT = Path(__file__).resolve().parents[1]


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value):
    raise ValueError(f"non-finite JSON number: {value}")


def loads(text):
    return json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)


def read_json(path):
    return loads(Path(path).read_text(encoding="utf-8"))


def digest(value):
    """Digest our deterministic fixture encoding; this is not RFC 8785 JCS."""
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


@lru_cache(maxsize=32)
def validator(schema_text):
    from jsonschema import Draft202012Validator, FormatChecker
    schema = loads(schema_text)
    Draft202012Validator.check_schema(schema)
    # Only bundled, self-contained schemas are accepted. A schema must not cause
    # network retrieval or dereference investigator-controlled external paths.
    def inspect(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in ("$ref", "$dynamicRef") and not item.startswith("#"):
                    raise ValueError("external schema references are not supported")
                inspect(item)
        elif isinstance(value, list):
            for item in value:
                inspect(item)
    inspect(schema)
    checker = FormatChecker()
    if "date-time" not in checker.checkers:
        raise RuntimeError("date-time validation unavailable; install requirements.txt")
    return Draft202012Validator(schema, format_checker=checker)


def validate_schema(schema, value, label="record"):
    check = validator(json.dumps(schema, sort_keys=True))
    errors = sorted(check.iter_errors(value), key=lambda e: str(list(e.absolute_path)))
    if errors:
        error = errors[0]
        location = ".".join(map(str, error.absolute_path)) or "$"
        raise ValueError(f"{label} at {location}: {error.message}")


def event_schema(version):
    names = {"0.1.0-draft": "ai-investigation-event.schema.json",
             "0.2.0-draft": "ai-investigation-event-v0.2.schema.json"}
    if version not in names:
        raise ValueError(f"unsupported schema version: {version}")
    return read_json(ROOT / "schemas" / names[version])


def validate_event(event):
    if not isinstance(event, dict):
        raise ValueError("event must be an object")
    validate_schema(event_schema(event.get("schema_version")), event, "event")


def safe_path(root, relative):
    if not isinstance(relative, str) or "\\" in relative or ":" in relative:
        raise ValueError(f"unsafe evidence path: {relative!r}")
    parts = PurePosixPath(relative)
    if parts.is_absolute() or ".." in parts.parts or not parts.parts:
        raise ValueError(f"unsafe evidence path: {relative!r}")
    candidate = Path(root).joinpath(*parts.parts)
    # Reject even internal symlinks: the manifest must describe the file itself.
    for parent in (candidate, *candidate.parents):
        if parent == Path(root):
            break
        if parent.is_symlink():
            raise ValueError(f"symlink in evidence path: {relative}")
    if Path(root).resolve() not in candidate.resolve().parents or not candidate.is_file():
        raise ValueError(f"missing or escaped evidence path: {relative}")
    return candidate


def validate_manifest(case_dir):
    case_dir = Path(case_dir)
    manifest = read_json(case_dir / "manifest.json")
    validate_schema(read_json(ROOT / "schemas/evidence-manifest.schema.json"), manifest, "manifest")
    if manifest["case_id"] != case_dir.name[:8]:
        raise ValueError("manifest case identity does not match directory")
    if not manifest["artifacts"]:
        raise ValueError("empty evidence manifest")
    paths = set()
    for artifact in manifest["artifacts"]:
        relative = artifact["path"]
        if relative in paths:
            raise ValueError(f"duplicate manifest path: {relative}")
        paths.add(relative)
        actual = hashlib.sha256(safe_path(case_dir, relative).read_bytes()).hexdigest()
        if actual != artifact["sha256"].lower():
            raise ValueError(f"SHA-256 mismatch: {relative}")
    actual_paths = {p.relative_to(case_dir).as_posix()
                    for p in (case_dir / "evidence").rglob("*") if p.is_file() or p.is_symlink()}
    if paths != actual_paths:
        raise ValueError(f"manifest coverage mismatch: {sorted(paths ^ actual_paths)}")
    return len(paths)


def validate_trajectory(events):
    if not isinstance(events, list) or not events:
        raise ValueError("trajectory must be a non-empty array")
    seen = set()
    from datetime import datetime
    previous = None
    for index, event in enumerate(events, 1):
        validate_event(event)
        if event["event_id"] in seen:
            raise ValueError("duplicate event identifier")
        if type(event.get("sequence")) is not int or event["sequence"] != index:
            raise ValueError("trajectory sequence is not contiguous")
        parent = event["correlation"].get("parent_event_id")
        if parent and parent not in seen:
            raise ValueError("parent event is missing or not earlier in the trajectory")
        time = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
        if previous is not None and time < previous:
            raise ValueError("fixture timestamp order is inconsistent")
        previous = time
        seen.add(event["event_id"])
    return seen


def validate_graph(graph, events, records):
    validate_schema(read_json(ROOT / "schemas/airg.schema.json"), graph, "AIRG")
    nodes = {n["id"] for n in graph["nodes"]}
    if len(nodes) != len(graph["nodes"]):
        raise ValueError("duplicate AIRG node")
    event_ids = {e["event_id"] for e in events}
    record_ids = {r["record_id"] for r in records}
    edge_ids = set()
    for edge in graph["edges"]:
        if edge["id"] in edge_ids or not {edge["source"], edge["target"]} <= nodes:
            raise ValueError("duplicate edge or missing AIRG endpoint")
        edge_ids.add(edge["id"])
        if not set(edge["event_ids"]) <= event_ids or not set(edge["record_ids"]) <= record_ids:
            raise ValueError("AIRG cites missing evidence")
        if edge["confidence"] == "confirmed" and not edge["record_ids"]:
            raise ValueError("confirmed AIRG edge has no supporting record")
        if edge["confidence"] in ("unknown", "inferred") and not edge.get("limitation"):
            raise ValueError("uncertain AIRG edge requires a limitation")
