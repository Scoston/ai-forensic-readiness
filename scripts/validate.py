#!/usr/bin/env python3
"""Dependency-free repository checks for the v0.1 discussion draft."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")


def validate_event(schema: dict, event: dict) -> None:
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
    for group in ("correlation", "principal", "integrity"):
        definition = schema["properties"][group]
        missing_nested = set(definition.get("required", [])) - set(event[group])
        if missing_nested:
            fail(f"event example: {group} missing {sorted(missing_nested)}")
        extra_nested = set(event[group]) - set(definition["properties"])
        if extra_nested:
            fail(f"event example: {group} has unexpected {sorted(extra_nested)}")


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
    schema = load_json(ROOT / "schemas" / "ai-investigation-event.schema.json")
    event = load_json(ROOT / "schemas" / "examples" / "tool-executed.valid.json")
    validate_event(schema, event)
    validate_markdown_links()
    print("JSON syntax: OK")
    print("AI event example: structurally valid for v0.1")
    print("Local Markdown links: OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

