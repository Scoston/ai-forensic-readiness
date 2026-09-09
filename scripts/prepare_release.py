#!/usr/bin/env python3
"""Verify the existing Zenodo archive and optionally prepare a GitHub draft release.

Default: local preparation only. --apply creates a draft and uploads verified assets;
it never publishes a release, edits a published release, moves a tag or archives to Zenodo.
"""
from __future__ import annotations

import argparse
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import tempfile
import urllib.parse
import urllib.request
import zipfile

try:
    from .publication import (ROOT, REPOSITORY, GitHub, PublicationError, check_assets,
                              check_release, check_tag, find_release, load_config,
                              run, sha256, source_file, verify_bytes)
except ImportError:
    from publication import (ROOT, REPOSITORY, GitHub, PublicationError, check_assets,
                             check_release, check_tag, find_release, load_config,
                             run, sha256, source_file, verify_bytes)


def fetch_public(url, maximum):
    request = urllib.request.Request(url, headers={"User-Agent": "ai-forensic-readiness-release"})
    with urllib.request.urlopen(request, timeout=45) as response:
        data = response.read(maximum + 1)
    if len(data) > maximum:
        raise PublicationError("Download exceeds its declared limit")
    return data


def verify_record(config, record):
    metadata = record["metadata"]
    if (record.get("doi") != config["doi"] or metadata["version"] != config["version"]
            or metadata["title"] != config["title"] or metadata["access_right"] != "open"):
        raise PublicationError("Zenodo identity, version, title or visibility mismatch")
    files = {item["key"]: item for item in record["files"]}
    if len(files) != len(record["files"]):
        raise PublicationError("Duplicate Zenodo filenames")
    for asset in config["assets"]:
        if asset["zenodo_name"] not in files or files[asset["zenodo_name"]]["size"] != asset["size"]:
            raise PublicationError("Zenodo file inventory does not match the publication manifest")


def verify_source_zip(data, commit):
    expected = set(run(["git", "ls-tree", "-r", "--name-only", commit]).decode().splitlines())
    with zipfile.ZipFile(BytesIO(data)) as archive:
        files = [item for item in archive.infolist() if not item.is_dir()]
        if not files or len({item.filename for item in files}) != len(files):
            raise PublicationError("Empty source ZIP or duplicate entries")
        prefix = files[0].filename.split("/", 1)[0] + "/"
        actual = {}
        for item in files:
            path = PurePosixPath(item.filename)
            if not item.filename.startswith(prefix) or path.is_absolute() or ".." in path.parts:
                raise PublicationError("Unsafe source ZIP entry")
            actual[item.filename[len(prefix):]] = item
        if set(actual) != expected:
            raise PublicationError("Source ZIP file list differs from the archived commit")
        for path, item in actual.items():
            if archive.read(item) != source_file(commit, path):
                raise PublicationError(f"Source ZIP differs from the archived commit: {path}")
    return len(expected)


def prepare_files(config, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    record_url = f"https://zenodo.org/api/records/{config['zenodo_record']}"
    record = json.loads(fetch_public(record_url, 2_000_000))
    verify_record(config, record)
    assets = []
    compared = None
    for asset in config["assets"]:
        name = urllib.parse.quote(asset["zenodo_name"], safe="")
        data = fetch_public(f"{record_url}/files/{name}/content", asset["size"])
        verify_bytes(asset, data)
        if asset["name"].endswith(".pdf"):
            if data != source_file(config["source_commit"], "release/" + asset["name"]):
                raise PublicationError("PDF differs from the archived source commit")
        elif asset["name"].endswith(".zip"):
            compared = verify_source_zip(data, config["source_commit"])
        path = output / asset["name"]
        if path.exists() and path.read_bytes() != data:
            raise PublicationError(f"Local output already contains different data: {path.name}")
        path.write_bytes(data)
        assets.append(path)
    checksums = output / "SHA256SUMS.txt"
    sums = "".join(f"{sha256(path.read_bytes())}  {path.name}\n" for path in assets).encode()
    if checksums.exists() and checksums.read_bytes() != sums:
        raise PublicationError("Existing checksum output differs")
    checksums.write_bytes(sums)
    assets.append(checksums)
    return assets, {"doi": config["doi"], "source_commit": config["source_commit"],
                    "source_files_compared": compared, "assets": [path.name for path in assets]}


def prepare_draft(api, config, assets):
    tag_exists = check_tag(api, config)
    release = find_release(api, config)
    if release:
        check_release(release, config)
        if not release["draft"] and not tag_exists:
            raise PublicationError("Published release has no source tag; owner investigation required")
    # Check existing artifacts before creating a tag or changing any remote data.
    with tempfile.TemporaryDirectory() as temporary:
        missing = check_assets(api, release or {"assets": []}, config, assets,
                               directory=temporary, allow_missing=not release or release["draft"])
    if release and not release["draft"]:
        return {"state": "already-published", "url": release["html_url"]}
    if not tag_exists:
        api.api(f"repos/{REPOSITORY}/git/refs", "POST",
                {"ref": "refs/tags/" + config["tag"], "sha": config["source_commit"]})
    if not release:
        release = api.api(f"repos/{REPOSITORY}/releases", "POST", {
            "tag_name": config["tag"], "target_commitish": config["source_commit"],
            "name": config["title"], "body": (ROOT / config["notes"]).read_text(encoding="utf-8"),
            "draft": True, "prerelease": True, "make_latest": "false"})
    for path in missing:
        api.upload(config["tag"], path)
    current = api.api(f"repos/{REPOSITORY}/releases/{release['id']}")
    check_release(current, config)
    with tempfile.TemporaryDirectory() as temporary:
        check_assets(api, current, config, assets, directory=temporary)
    return {"state": "draft-ready", "url": current["html_url"], "release_id": current["id"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/v0.2-publication")
    parser.add_argument("--apply", action="store_true", help="Create a GitHub draft and upload verified assets")
    args = parser.parse_args()
    config = load_config()
    assets, result = prepare_files(config, args.output)
    if args.apply:
        result.update(prepare_draft(GitHub(), config, assets))
    else:
        result["state"] = "local-files-verified"
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (PublicationError, OSError, ValueError) as exc:
        raise SystemExit(str(exc))
