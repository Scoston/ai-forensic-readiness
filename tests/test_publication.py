"""Release guards and review packaging; no account, network or remote writes."""
import copy
from io import BytesIO
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from scripts import build_review_packs as packs
from scripts import finish_publication as owner
from scripts import prepare_release as prepare
from scripts import publication as pub


class FakeGitHub:
    def __init__(self, config, assets, *, draft=True, tag_exists=True):
        self.config = config
        self.tag_exists = tag_exists
        self.tag_sha = config["source_commit"]
        self.protection = None
        self.reporting = False
        self.hooks = []
        self.writes = []
        self.admin = True
        self.release = {"id": 321, "tag_name": config["tag"], "target_commitish": self.tag_sha,
                        "draft": draft, "prerelease": True, "body": config["doi"],
                        "html_url": "https://github.com/Scoston/ai-forensic-readiness/releases/tag/" + config["tag"],
                        "assets": [{"name": p.name, "size": p.stat().st_size,
                                    "digest": "sha256:" + pub.sha256(p.read_bytes())} for p in assets]}

    def pages(self, path):
        if path.endswith("/hooks"):
            return iter(self.hooks)
        if path.endswith("/releases"):
            return iter([self.release] if self.release else [])
        raise AssertionError(path)

    def api(self, path, method="GET", payload=None):
        prefix = "repos/" + pub.REPOSITORY
        if method != "GET":
            self.writes.append((method, path, copy.deepcopy(payload)))
            if path.endswith("/protection"):
                self.protection = copy.deepcopy(payload)
                return self.protection
            if path.endswith("/private-vulnerability-reporting"):
                self.reporting = True
                return None
            if path.endswith("/git/refs"):
                self.tag_exists = True
                self.tag_sha = payload["sha"]
                return {}
            if path.endswith("/releases"):
                self.release = dict(payload, id=321, assets=[], html_url="https://github.com/draft")
                return self.release
            if path.endswith("/releases/321"):
                self.release.update(payload)
                return self.release
            raise AssertionError((method, path))
        if path == prefix:
            return {"full_name": pub.REPOSITORY, "permissions": {"admin": self.admin}}
        if path.endswith("/branches/main"):
            return {"commit": {"sha": "a" * 40}}
        if "/actions/runs?" in path:
            return {"workflow_runs": [{"id": 42, "name": "Validate repository", "head_sha": "a" * 40,
                                      "conclusion": "success"}]}
        if "/actions/runs/42/jobs?" in path:
            return {"jobs": [{"name": name, "conclusion": "success"} for name in owner.REQUIRED_CHECKS]}
        if path.endswith("/protection"):
            if self.protection is None:
                raise pub.NotFound()
            return self.protection
        if path.endswith("/private-vulnerability-reporting"):
            return {"enabled": self.reporting}
        if "/git/ref/tags/" in path:
            if not self.tag_exists:
                raise pub.NotFound()
            return {"object": {"type": "commit", "sha": self.tag_sha}}
        if path.endswith("/releases/321"):
            return self.release
        raise AssertionError((method, path))

    def upload(self, tag, path):
        self.writes.append(("UPLOAD", path.name, None))
        self.release["assets"].append({"name": path.name, "size": path.stat().st_size,
                                       "digest": "sha256:" + pub.sha256(path.read_bytes())})


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.config = pub.load_config()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.asset = Path(self.temp.name) / "asset.pdf"
        self.asset.write_bytes(b"known archive bytes")
        self.assets = [self.asset]

    def test_changed_zenodo_bytes_rejected(self):
        spec = {"name": "asset.pdf", "size": 3, "sha256": pub.sha256(b"abc")}
        with self.assertRaises(pub.PublicationError):
            pub.verify_bytes(spec, b"abd")

    def test_wrong_zenodo_version_rejected(self):
        record = {"doi": self.config["doi"], "metadata": {"version": "0.1.0-draft"}}
        with self.assertRaises(pub.PublicationError):
            prepare.verify_record(self.config, record)

    def test_wrong_tag_stops_before_any_write(self):
        api = FakeGitHub(self.config, self.assets)
        api.tag_sha = "b" * 40
        with self.assertRaises(pub.PublicationError):
            prepare.prepare_draft(api, self.config, self.assets)
        self.assertEqual(api.writes, [])

    def test_altered_existing_asset_stops_before_tag_creation(self):
        api = FakeGitHub(self.config, self.assets, tag_exists=False)
        api.release["assets"][0]["digest"] = "sha256:" + "0" * 64
        with self.assertRaises(pub.PublicationError):
            prepare.prepare_draft(api, self.config, self.assets)
        self.assertEqual(api.writes, [])

    def test_prepare_creates_only_a_draft_and_is_idempotent(self):
        api = FakeGitHub(self.config, [], tag_exists=False)
        api.release = None
        result = prepare.prepare_draft(api, self.config, self.assets)
        self.assertEqual(result["state"], "draft-ready")
        self.assertTrue(api.release["draft"])
        self.assertTrue(api.release["prerelease"])
        self.assertEqual(api.tag_sha, self.config["source_commit"])
        writes = len(api.writes)
        prepare.prepare_draft(api, self.config, self.assets)
        self.assertEqual(len(api.writes), writes)

    def test_published_release_is_never_edited_by_preparation(self):
        api = FakeGitHub(self.config, self.assets, draft=False)
        result = prepare.prepare_draft(api, self.config, self.assets)
        self.assertEqual(result["state"], "already-published")
        self.assertEqual(api.writes, [])

    def test_missing_asset_in_published_release_is_not_silently_repaired(self):
        api = FakeGitHub(self.config, [], draft=False)
        with self.assertRaises(pub.PublicationError):
            prepare.prepare_draft(api, self.config, self.assets)
        self.assertEqual(api.writes, [])

    def test_owner_plan_makes_no_writes(self):
        api = FakeGitHub(self.config, self.assets)
        result = owner.finish(api, self.config, self.assets)
        self.assertFalse(result["apply"])
        self.assertEqual(api.writes, [])

    def test_unverified_extra_asset_blocks_publication(self):
        api = FakeGitHub(self.config, self.assets)
        api.release["assets"].append({"name": "unexpected.zip", "size": 1})
        with self.assertRaises(pub.PublicationError):
            owner.finish(api, self.config, self.assets, apply=True)
        self.assertEqual(api.writes, [])

    def test_published_release_without_tag_requires_investigation(self):
        api = FakeGitHub(self.config, self.assets, draft=False, tag_exists=False)
        with self.assertRaises(pub.PublicationError):
            owner.finish(api, self.config, self.assets, apply=True)
        self.assertEqual(api.writes, [])

    def test_admin_access_is_required_before_settings_or_release_writes(self):
        api = FakeGitHub(self.config, self.assets)
        api.admin = False
        with self.assertRaises(pub.PublicationError):
            owner.finish(api, self.config, self.assets, apply=True)
        self.assertEqual(api.writes, [])

    def test_unknown_existing_protection_is_not_overwritten(self):
        api = FakeGitHub(self.config, self.assets)
        api.protection = {"required_pull_request_reviews": {"required_approving_review_count": 2}}
        with self.assertRaises(pub.PublicationError):
            owner.finish(api, self.config, self.assets, apply=True)
        self.assertEqual(api.writes, [])

    def test_stronger_existing_protection_is_preserved(self):
        api = FakeGitHub(self.config, self.assets)
        api.protection = json.loads((pub.ROOT / "release/branch-protection.json").read_text())
        api.protection["required_pull_request_reviews"]["required_approving_review_count"] = 2
        owner.finish(api, self.config, self.assets, apply=True)
        self.assertEqual(api.protection["required_pull_request_reviews"]["required_approving_review_count"], 2)
        self.assertFalse(any(path.endswith("/protection") for _, path, _ in api.writes))

    def test_active_zenodo_hook_blocks_publication_but_settings_are_verified(self):
        api = FakeGitHub(self.config, self.assets)
        api.hooks = [{"id": 5, "active": True, "events": ["release"],
                      "config": {"url": "https://zenodo.org/api/hooks?token=do-not-print"}}]
        result = owner.finish(api, self.config, self.assets, apply=True)
        self.assertEqual(result["release"], "blocked-by-zenodo-auto-archiving")
        self.assertTrue(api.release["draft"])
        self.assertTrue(owner.protection_satisfies(api.protection))
        self.assertTrue(api.reporting)
        self.assertNotIn("do-not-print", json.dumps(result))
        self.assertFalse(any("/hooks" in path for _, path, _ in api.writes))

    def test_owner_publishes_only_after_settings_checks(self):
        api = FakeGitHub(self.config, self.assets)
        result = owner.finish(api, self.config, self.assets, apply=True)
        self.assertEqual(result["release"], "published")
        self.assertFalse(api.release["draft"])
        self.assertTrue(api.release["prerelease"])
        self.assertEqual(api.writes[-1][0], "PATCH")
        count = len(api.writes)
        owner.finish(api, self.config, self.assets, apply=True)
        self.assertEqual(len(api.writes), count)

    def test_zenodo_hook_host_and_event_matching(self):
        hooks = [{"id": 1, "active": True, "events": ["release"], "config": {"url": "https://zenodo.org.evil.example/x"}},
                 {"id": 2, "active": False, "events": ["release"], "config": {"url": "https://zenodo.org/x"}},
                 {"id": 3, "active": True, "events": ["push"], "config": {"url": "https://zenodo.org/x"}}]
        self.assertEqual(owner.zenodo_release_hooks(hooks), [])


class ReviewPackTests(unittest.TestCase):
    def setUp(self):
        self.config = pub.load_config()
        directories = sorted(path.name for path in (pub.ROOT / "cases").iterdir() if path.is_dir())
        self.command = patch.object(packs, "run", return_value="\n".join(directories).encode())
        self.command.start()
        self.addCleanup(self.command.stop)

    def source(self, commit, path):
        self.assertEqual(commit, self.config["source_commit"])
        return (pub.ROOT / path).read_bytes()

    def test_pack_contains_raw_evidence_and_explicit_omissions(self):
        with patch.object(packs, "source_file", side_effect=self.source):
            entries, count = packs.build_entries(self.config)
        manifests = [path for path in entries if path.endswith("/manifest.json")]
        self.assertEqual(len(manifests), 10)
        self.assertGreater(count, 0)
        for path, data in entries.items():
            self.assertNotIn("/normalized/", path)
            self.assertNotIn("replay-results.json", path)
            self.assertFalse(path.endswith("airg.json"))
            self.assertFalse(path.endswith("findings.md"))
            if path in manifests:
                manifest = json.loads(data)
                self.assertTrue(manifest["intentionally_withheld"])
                case = path.split("/")[0]
                for artifact in manifest["artifacts"]:
                    self.assertEqual(pub.sha256(entries[case + "/" + artifact["path"]]), artifact["sha256"])
        self.assertEqual(packs.zip_bytes(entries), packs.zip_bytes(dict(reversed(list(entries.items())))))

    def test_committed_pack_matches_expected_evidence_and_forms(self):
        with patch.object(packs, "source_file", side_effect=self.source):
            expected, _ = packs.build_entries(self.config)
        with zipfile.ZipFile(pub.ROOT / "release/reviewer-packs-v0.2.zip") as archive:
            self.assertEqual(len(archive.namelist()), len(set(archive.namelist())))
            self.assertEqual({name: archive.read(name) for name in archive.namelist()}, expected)

    def test_tampered_raw_artifact_is_rejected(self):
        def tampered(commit, path):
            data = self.source(commit, path)
            return data + b"tampered" if "/raw/" in path else data
        with patch.object(packs, "source_file", side_effect=tampered):
            with self.assertRaises(pub.PublicationError):
                packs.build_entries(self.config)

    def test_traversal_is_rejected(self):
        for path in ("evidence/raw/../../answers", "/evidence/raw/a", "evidence\\raw\\a"):
            with self.assertRaises(pub.PublicationError):
                packs.include_artifact(path)

    def test_zip_content_must_match_the_pinned_commit(self):
        stream = BytesIO()
        with zipfile.ZipFile(stream, "w") as archive:
            archive.writestr("repo/a.txt", b"altered")
        with patch.object(prepare, "run", return_value=b"a.txt\n"), \
                patch.object(prepare, "source_file", return_value=b"original"):
            with self.assertRaises(pub.PublicationError):
                prepare.verify_source_zip(stream.getvalue(), self.config["source_commit"])


if __name__ == "__main__":
    unittest.main()
