#!/usr/bin/env python3
"""Owner command: inspect publication/settings, or apply them with --apply.

Uses the owner's existing gh authentication. It does not change webhooks, relax
existing branch protection, move tags, contact reviewers or create Zenodo records.
"""
from __future__ import annotations

import argparse
import json
import tempfile
from urllib.parse import urlparse

try:
    from .publication import (ROOT, REPOSITORY, GitHub, NotFound, PublicationError,
                              check_assets, check_release, check_tag, find_release, load_config)
    from .prepare_release import prepare_files, prepare_draft
except ImportError:
    from publication import (ROOT, REPOSITORY, GitHub, NotFound, PublicationError,
                             check_assets, check_release, check_tag, find_release, load_config)
    from prepare_release import prepare_files, prepare_draft

REQUIRED_CHECKS = {"validate (3.12)", "validate (3.13)"}


def enabled(value):
    return value.get("enabled", False) if isinstance(value, dict) else value is True


def protection_satisfies(protection):
    checks = protection.get("required_status_checks") or {}
    contexts = set(checks.get("contexts", [])) | {
        item["context"] for item in checks.get("checks", [])}
    return (REQUIRED_CHECKS <= contexts and checks.get("strict") is True
            and enabled(protection.get("enforce_admins"))
            and isinstance(protection.get("required_pull_request_reviews"), dict)
            and protection["required_pull_request_reviews"].get("dismiss_stale_reviews") is True
            and enabled(protection.get("required_conversation_resolution"))
            and not enabled(protection.get("allow_force_pushes"))
            and not enabled(protection.get("allow_deletions")))


def zenodo_release_hooks(hooks):
    # Only IDs are returned. Webhook URLs can contain credentials and are never printed.
    result = []
    for hook in hooks:
        host = (urlparse(hook.get("config", {}).get("url", "")).hostname or "").lower()
        if (hook.get("active") and (host == "zenodo.org" or host.endswith(".zenodo.org"))
                and set(hook.get("events", [])) & {"release", "*"}):
            result.append(hook["id"])
    return result


def check_ci(api):
    main = api.api(f"repos/{REPOSITORY}/branches/main")["commit"]["sha"]
    runs = api.api(f"repos/{REPOSITORY}/actions/runs?head_sha={main}&per_page=100")["workflow_runs"]
    passing = [run for run in runs if run["name"] == "Validate repository"
               and run["head_sha"] == main and run["conclusion"] == "success"]
    if not passing:
        raise PublicationError("Wait for Validate repository to pass on current main, then rerun")
    jobs = api.api(f"repos/{REPOSITORY}/actions/runs/{passing[0]['id']}/jobs?per_page=100")["jobs"]
    if not REQUIRED_CHECKS <= {job["name"] for job in jobs if job["conclusion"] == "success"}:
        raise PublicationError("The expected Python validation jobs have not passed")


def finish(api, config, assets, *, apply=False):
    repo = api.api(f"repos/{REPOSITORY}")
    if repo.get("full_name", "").lower() != REPOSITORY.lower() or not repo.get("permissions", {}).get("admin"):
        raise PublicationError("This owner command requires repository administration access in gh")
    check_ci(api)
    tag_exists = check_tag(api, config)
    try:
        protection = api.api(f"repos/{REPOSITORY}/branches/main/protection")
    except NotFound:
        protection = None
    if protection and not protection_satisfies(protection):
        raise PublicationError("Existing branch protection differs from the baseline. Review it in GitHub settings; "
                               "this command will not overwrite existing policy.")
    reporting = api.api(f"repos/{REPOSITORY}/private-vulnerability-reporting")
    hooks = zenodo_release_hooks(api.pages(f"repos/{REPOSITORY}/hooks"))
    release = find_release(api, config)
    if release:
        check_release(release, config)
        if not release["draft"] and not tag_exists:
            raise PublicationError("Published release has no source tag; owner investigation required")
        with tempfile.TemporaryDirectory() as directory:
            check_assets(api, release, config, assets, directory=directory,
                         allow_missing=release["draft"])
    result = {"repository": REPOSITORY, "doi": config["doi"], "apply": apply,
              "branch_protection": "already-configured" if protection else "to-enable",
              "private_vulnerability_reporting": "enabled" if reporting["enabled"] else "to-enable",
              "release": "published" if release and not release["draft"] else "draft-to-publish",
              "active_zenodo_release_hook_ids": hooks}
    if not apply:
        return result
    if not protection:
        baseline = json.loads((ROOT / "release/branch-protection.json").read_text(encoding="utf-8"))
        api.api(f"repos/{REPOSITORY}/branches/main/protection", "PUT", baseline)
    if not reporting["enabled"]:
        api.api(f"repos/{REPOSITORY}/private-vulnerability-reporting", "PUT")
    if not protection_satisfies(api.api(f"repos/{REPOSITORY}/branches/main/protection")):
        raise PublicationError("Branch protection did not verify after applying it")
    if not api.api(f"repos/{REPOSITORY}/private-vulnerability-reporting")["enabled"]:
        raise PublicationError("Private vulnerability reporting did not verify")
    result.update(branch_protection="verified", private_vulnerability_reporting="verified")
    if release and not release["draft"]:
        result["release_url"] = release["html_url"]
        return result
    if hooks:
        result["release"] = "blocked-by-zenodo-auto-archiving"
        result["next_action"] = ("In Zenodo's GitHub settings, disable automatic archiving for this repository, "
                                 "then rerun this command. v0.2 already has its DOI. No webhook was changed.")
        return result
    # The same verified preparation also recovers a missing or partially uploaded draft.
    prepare_draft(api, config, assets)
    release = find_release(api, config)
    if not check_tag(api, config):
        raise PublicationError("Source tag is missing")
    check_release(release, config)
    with tempfile.TemporaryDirectory() as directory:
        check_assets(api, release, config, assets, directory=directory)
    published = api.api(f"repos/{REPOSITORY}/releases/{release['id']}", "PATCH",
                        {"draft": False, "prerelease": True, "make_latest": "false"})
    if published["draft"] or not published["prerelease"] or not check_tag(api, config):
        raise PublicationError("Published release did not verify")
    result.update(release="published", release_url=published["html_url"])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Apply verified settings and publish the prepared prerelease")
    args = parser.parse_args()
    config = load_config()
    with tempfile.TemporaryDirectory() as directory:
        assets, _ = prepare_files(config, directory)
        result = finish(GitHub(), config, assets, apply=args.apply)
    print(json.dumps(result, indent=2))
    if result["release"] == "blocked-by-zenodo-auto-archiving":
        raise SystemExit(2)


if __name__ == "__main__":
    try:
        main()
    except (PublicationError, OSError, ValueError) as exc:
        raise SystemExit(str(exc))
