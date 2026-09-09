"""Shared, standard-library release checks. Credentials stay inside GitHub CLI."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "Scoston/ai-forensic-readiness"


class PublicationError(RuntimeError):
    pass


class NotFound(PublicationError):
    pass


def run(command, *, cwd=ROOT, stdin=None):
    try:
        result = subprocess.run(command, cwd=cwd, input=stdin, capture_output=True,
                                timeout=180, check=False)
    except FileNotFoundError as exc:
        raise PublicationError(f"Install {command[0]} and run this command again.") from exc
    except subprocess.TimeoutExpired as exc:
        raise PublicationError(f"{command[0]} timed out; check the operation's state before rerunning.") from exc
    if result.returncode:
        # Report the operation, not captured output that might contain service data.
        if b"HTTP 404" in result.stderr:
            raise NotFound("GitHub resource not found")
        status = re.search(rb"HTTP (\d{3})", result.stderr)
        detail = f", HTTP {status[1].decode()}" if status else ""
        raise PublicationError(f"{command[0]} {command[1]} failed (exit {result.returncode}{detail}). "
                               "Check authentication and permissions; no alternate credentials are used.")
    return result.stdout


class GitHub:
    def api(self, path, method="GET", payload=None):
        if not path.startswith(f"repos/{REPOSITORY}/") and path != f"repos/{REPOSITORY}":
            raise PublicationError("Operation is outside the authorized repository")
        args = ["gh", "api", "--method", method, path]
        data = None
        if payload is not None:
            args += ["--input", "-"]
            data = json.dumps(payload).encode()
        output = run(args, stdin=data)
        return json.loads(output) if output.strip() else None

    def pages(self, path):
        for page in range(1, 101):
            rows = self.api(f"{path}?per_page=100&page={page}")
            if not isinstance(rows, list):
                raise PublicationError("Unexpected paginated GitHub response")
            yield from rows
            if len(rows) < 100:
                return
        raise PublicationError("Too many pages; stopped without guessing")

    def upload(self, tag, path):
        run(["gh", "release", "upload", tag, str(path), "--repo", REPOSITORY])

    def download(self, tag, name, directory):
        with tempfile.TemporaryDirectory(dir=directory) as temporary:
            run(["gh", "release", "download", tag, "--repo", REPOSITORY,
                 "--pattern", name, "--dir", temporary])
            return (Path(temporary) / name).read_bytes()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def load_config():
    config = json.loads((ROOT / "release/v0.2-publication.json").read_text(encoding="utf-8"))
    if config["repository"] != REPOSITORY or config["tag"] != "v" + config["version"]:
        raise PublicationError("Repository or version mismatch")
    if not re.fullmatch(r"\d+\.\d+\.\d+-draft", config["version"]):
        raise PublicationError("This workflow only prepares discussion-draft versions")
    if type(config["zenodo_record"]) is not int or config["zenodo_record"] <= 0:
        raise PublicationError("Invalid Zenodo record ID")
    if not re.fullmatch(r"[0-9a-f]{40}", config["source_commit"]):
        raise PublicationError("An exact source commit is required")
    if config["doi"] != f"10.5281/zenodo.{config['zenodo_record']}":
        raise PublicationError("Zenodo record and DOI mismatch")
    if config["notes"] != "release/v0.2-github-release.md":
        raise PublicationError("Unexpected release-notes path")
    if len(config["assets"]) != 3:
        raise PublicationError("The archive must include the two PDFs and source ZIP")
    names = set()
    for asset in config["assets"]:
        for key in ("name", "zenodo_name"):
            if not re.fullmatch(r"[A-Za-z0-9_. ()-]+", asset[key]) or asset[key] in (".", ".."):
                raise PublicationError("Unsafe asset name")
        if asset["name"] in names or not re.fullmatch(r"[0-9a-f]{64}", asset["sha256"]):
            raise PublicationError("Duplicate asset or invalid hash")
        if type(asset["size"]) is not int or not 0 < asset["size"] < 10_000_000:
            raise PublicationError("Invalid asset size")
        names.add(asset["name"])
    return config


def source_file(commit, path):
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise PublicationError("Invalid source commit")
    return run(["git", "show", f"{commit}:{path}"])


def verify_bytes(asset, data):
    if len(data) != asset["size"] or sha256(data) != asset["sha256"]:
        raise PublicationError(f"Archive content mismatch: {asset['name']}")


def check_tag(api, config):
    try:
        obj = api.api(f"repos/{REPOSITORY}/git/ref/tags/{config['tag']}")["object"]
    except NotFound:
        return False
    visited = set()
    while obj["type"] == "tag":
        if obj["sha"] in visited or len(visited) >= 8:
            raise PublicationError("Cyclic or excessive annotated tags")
        visited.add(obj["sha"])
        obj = api.api(f"repos/{REPOSITORY}/git/tags/{obj['sha']}")["object"]
    if obj["type"] != "commit" or obj["sha"] != config["source_commit"]:
        raise PublicationError("The release tag points to a different commit; it will not be moved")
    return True


def find_release(api, config):
    return next((item for item in api.pages(f"repos/{REPOSITORY}/releases")
                 if item["tag_name"] == config["tag"]), None)


def check_release(release, config):
    if release["tag_name"] != config["tag"] or not release["prerelease"]:
        raise PublicationError("The existing release is not the intended discussion draft")
    if config["doi"] not in (release.get("body") or ""):
        raise PublicationError("The existing release does not cite the verified Zenodo DOI")
    if release.get("draft") and release.get("target_commitish") != config["source_commit"]:
        raise PublicationError("The draft release does not target the archived commit")


def check_assets(api, release, config, assets, *, directory, allow_missing=False):
    """Never clobber an uploaded artifact, including an altered draft asset."""
    existing = {item["name"]: item for item in release.get("assets", [])}
    if len(existing) != len(release.get("assets", [])):
        raise PublicationError("Duplicate release asset names")
    if set(existing) - {path.name for path in assets}:
        raise PublicationError("Release contains assets outside the verified publication manifest")
    missing = []
    for path in assets:
        item = existing.get(path.name)
        if item is None:
            missing.append(path)
            continue
        digest = sha256(path.read_bytes())
        if item["size"] != path.stat().st_size:
            raise PublicationError(f"Existing release asset differs: {path.name}")
        if item.get("digest"):
            if item["digest"] != "sha256:" + digest:
                raise PublicationError(f"Existing release asset differs: {path.name}")
        elif sha256(api.download(config["tag"], path.name, directory)) != digest:
            raise PublicationError(f"Existing release asset differs: {path.name}")
    if missing and not allow_missing:
        raise PublicationError("Release is missing verified assets")
    return missing
