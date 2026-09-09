#!/usr/bin/env python3
"""Build deterministic review packs from the exact archived source commit.

Raw evidence is copied byte for byte. Author answers and normalized conclusions
are withheld, and a derived manifest makes those omissions explicit.
"""
from __future__ import annotations

import argparse
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import re
import zipfile

try:
    from .publication import ROOT, PublicationError, load_config, run, sha256, source_file
except ImportError:
    from publication import ROOT, PublicationError, load_config, run, sha256, source_file


def include_artifact(path):
    parts = PurePosixPath(path)
    if parts.is_absolute() or ".." in parts.parts or "\\" in path:
        raise PublicationError("Unsafe artifact path")
    return parts.parts[:2] == ("evidence", "raw") and parts.name != "replay-results.json"


def response_form(case, commit):
    return f"""# Review response: {case}

Source commit: `{commit}`

| Field | Reviewer response |
| --- | --- |
| Review date and relevant experience | |
| Relationship to author; potential conflicts | |
| Prior familiarity with this case | |
| Assistance, tools and AI used | |
| Start/end time and interruptions | |
| Authority and execution path | |
| Context and provenance | |
| Persistent effects and scope limits | |
| Containment/recovery conclusions | |
| Supporting file and record identifiers | |
| Alternative explanations and conflicting evidence | |
| Unknowns and additional sources needed | |
| Disagreements after the facilitator reveals findings | |
| Suggested requirement or schema changes | |
| Consent to public attribution | |

Leave results blank until an actual investigator completes the exercise.
""".encode()


def build_entries(config):
    commit = config["source_commit"]
    directories = run(["git", "ls-tree", "-d", "--name-only", f"{commit}:cases"]).decode().splitlines()
    cases = [name for name in directories if re.fullmatch(r"case-\d{3}-[a-z0-9-]+", name)]
    if len(cases) != 10:
        raise PublicationError("Expected the ten archived cases")
    entries = {"instructions.md": (ROOT / "research/reviewer-instructions.md").read_bytes()}
    included_count = 0
    for directory in sorted(cases):
        case = directory[:8]
        base = "cases/" + directory
        original = source_file(commit, base + "/manifest.json")
        source = json.loads(original)
        if source["case_id"] != case or source["synthetic_data"] is not True:
            raise PublicationError("Unexpected source case identity")
        included, withheld = [], []
        seen = set()
        for artifact in source["artifacts"]:
            path = artifact["path"]
            if path in seen:
                raise PublicationError("Duplicate source manifest path")
            seen.add(path)
            if include_artifact(path):
                data = source_file(commit, base + "/" + path)
                if sha256(data) != artifact["sha256"]:
                    raise PublicationError(f"Source artifact hash mismatch: {base}/{path}")
                entries[f"{case}/{path}"] = data
                included.append(artifact)
                included_count += 1
            else:
                withheld.append({"path": path, "reason": "Author interpretation or review answer; withheld by pack design"})
        if not included:
            raise PublicationError("Case has no raw evidence")
        manifest = {"profile": "raw-evidence-review-v1", "case_id": case, "synthetic_data": True,
                    "source_commit": commit, "source_case": base,
                    "source_manifest_sha256": sha256(original), "artifacts": included,
                    "intentionally_withheld": withheld}
        entries[f"{case}/manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
        entries[f"{case}/response.md"] = response_form(case, commit)
    return entries, included_count


def zip_bytes(entries):
    stream = BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, data in sorted(entries.items()):
            info = zipfile.ZipInfo(path, date_time=(2000, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, data, compresslevel=9)
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/reviewer-packs-v0.2.zip")
    parser.add_argument("--check", action="store_true", help="Verify existing bytes without changing files")
    args = parser.parse_args()
    entries, count = build_entries(load_config())
    data = zip_bytes(entries)
    if args.check:
        if not args.output.is_file() or args.output.read_bytes() != data:
            raise SystemExit("Review pack differs from deterministic regeneration")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(data)
    print(json.dumps({"path": str(args.output), "cases": 10, "raw_artifacts": count,
                      "sha256": sha256(data), "bytes": len(data)}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (PublicationError, OSError, ValueError) as exc:
        raise SystemExit(str(exc))
