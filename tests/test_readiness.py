"""Behavior and rejection tests for the investigation controls and evidence gates."""
import copy
import hashlib
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from scripts.evidence import (ROOT, digest, loads, read_json, validate_event, validate_graph,
                              validate_manifest, validate_schema, validate_trajectory, write_json)
from scripts.simulations import child_authorized, run, standalone
from scripts.convert_events import to_ocsf, to_otel, restore, unix_ns
from scripts.validate_extended import check_records


class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.event = read_json(ROOT / "schemas/examples/v02/tool-executed.valid.json")

    def test_declared_conformance_examples(self):
        for fixture in read_json(ROOT / "schemas/conformance.json"):
            with self.subTest(path=fixture["path"]):
                if fixture["valid"]:
                    validate_event(read_json(ROOT / fixture["path"]))
                else:
                    with self.assertRaises(ValueError):
                        validate_event(read_json(ROOT / fixture["path"]))

    def test_duplicate_keys_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            loads('{"approved": false, "approved": true}')

    def test_nonfinite_json_rejected(self):
        for value in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                loads('{"confidence":' + value + '}')

    def test_external_schema_references_rejected(self):
        with self.assertRaisesRegex(ValueError, "external"):
            validate_schema({"$ref": "https://example.invalid/injected-schema.json"}, {})

    def test_validation_event_requires_scoped_result(self):
        self.event["event_type"] = "ai.state.validated"
        with self.assertRaisesRegex(ValueError, "validation"):
            validate_event(self.event)

    def test_approval_requires_what_reviewer_saw(self):
        self.event["event_type"] = "ai.approval.granted"
        with self.assertRaisesRegex(ValueError, "oversight"):
            validate_event(self.event)

    def test_memory_event_requires_lineage(self):
        self.event["event_type"] = "ai.memory.read"
        with self.assertRaisesRegex(ValueError, "memory"):
            validate_event(self.event)

    def test_unknown_schema_rejected(self):
        self.event["schema_version"] = "9.9.9"
        with self.assertRaisesRegex(ValueError, "unsupported"):
            validate_event(self.event)

    def test_hash_algorithm_requires_matching_digest(self):
        self.event["integrity"].update(hash_algorithm="sha256", hash="claimed-hash")
        with self.assertRaisesRegex(ValueError, "hash"):
            validate_event(self.event)

    def test_executed_event_cannot_only_be_authorized(self):
        self.event["action"]["outcome"] = "authorized"
        with self.assertRaisesRegex(ValueError, "outcome"):
            validate_event(self.event)

    def test_granted_approval_cannot_record_denial(self):
        self.event["event_type"] = "ai.approval.granted"
        self.event["oversight"] = {"reviewer_id": "test-reviewer", "decided_at": "2026-09-08T12:00:00Z",
                                   "presented_evidence_refs": ["synthetic://test-display"], "available_actions": ["deny"],
                                   "independence": "independent", "decision": "deny"}
        with self.assertRaisesRegex(ValueError, "decision"):
            validate_event(self.event)


class ExperimentTests(unittest.TestCase):
    def compare(self, case):
        return run(case)["conclusion"], run(case, True)["conclusion"]

    def test_untrusted_context_cannot_grant_export(self):
        bad, good = self.compare(1)
        self.assertTrue(bad["unauthorized_export"])
        self.assertFalse(good["unauthorized_export"])
        self.assertFalse(bad["retrospective_resolved"])

    def test_source_removal_does_not_remove_memory(self):
        bad, good = self.compare(2)
        self.assertTrue(bad["delayed_influence"])
        self.assertFalse(good["delayed_influence"])

    def test_child_identity_is_distinct_in_both_conditions(self):
        bad, good = self.compare(3)
        self.assertTrue(bad["distinct_child_identity"] and good["distinct_child_identity"])
        self.assertTrue(bad["child_allowed_after_parent_revocation"])
        self.assertFalse(good["child_allowed_after_parent_revocation"])
        self.assertFalse(bad["lease_expired"])

    def test_revocation_and_derivative_disposition_are_separate(self):
        bad, good = self.compare(4)
        self.assertTrue(bad["prospective_revoked"] and good["prospective_revoked"])
        self.assertEqual(bad["residual_operational_derivatives"], ["summary", "embedding", "cache"])
        self.assertEqual(good["residual_operational_derivatives"], [])
        self.assertEqual(good["external_copies"], "unknown")

    def test_tool_selection_is_not_execution_authority(self):
        bad, good = self.compare(5)
        self.assertEqual(bad["selected_operation"], good["selected_operation"])
        self.assertTrue(bad["export_executed"])
        self.assertFalse(good["export_executed"])

    def test_approval_can_exist_for_misrepresented_action(self):
        bad, good = self.compare(6)
        self.assertTrue(bad["approved"] and bad["unintended_deletion"])
        self.assertFalse(bad["display_matches_action"])
        self.assertTrue(good["display_matches_action"])
        self.assertFalse(good["approved"] or good["unintended_deletion"])

    def test_tenant_filter_blocks_cross_boundary_read(self):
        bad, good = self.compare(7)
        self.assertTrue(bad["cross_tenant_exposure"])
        self.assertFalse(good["cross_tenant_exposure"])
        self.assertIsNone(good["affected_decision"])

    def test_drift_is_visible_without_asserting_model_causation(self):
        bad, good = self.compare(8)
        self.assertTrue(bad["configuration_drift"] and good["configuration_drift"])
        self.assertTrue(bad["unevaluated_action_executed"])
        self.assertFalse(good["unevaluated_action_executed"])
        self.assertIn("not tested", good["model_causation"])

    def test_correction_does_not_reverse_publication(self):
        bad, good = self.compare(9)
        self.assertTrue(bad["published"] and bad["external_copy_remains"])
        self.assertFalse(bad["correction_is_reversal"])
        self.assertFalse(good["published"])

    def test_missing_context_does_not_negate_downstream_receipt(self):
        bad, good = self.compare(10)
        self.assertTrue(bad["execution_confirmed_in_simulation"] and good["execution_confirmed_in_simulation"])
        self.assertEqual(bad["influence_confidence"], "unknown")
        self.assertEqual(good["internal_reasoning"], "unknown")

    def test_all_conditions_deterministic_and_schema_valid(self):
        for case in range(1, 11):
            for control in (False, True):
                with self.subTest(case=case, control=control):
                    self.assertEqual(run(case, control), run(case, control))
                    validate_trajectory(run(case, control)["events"])

    def test_standalone_results_have_resolvable_evidence(self):
        for case in range(1, 11):
            comparison = standalone(case)
            for condition in ("failure", "control"):
                for event in comparison[condition]["events"]:
                    validate_event(event)
                    ref = event["evidence_refs"][0]
                    self.assertTrue(ref.startswith("#/"))
                    resolved = comparison
                    for part in ref[2:].split("/"):
                        resolved = resolved[int(part)] if isinstance(resolved, list) else resolved[part]
                    self.assertEqual(event["integrity"]["hash"], digest(resolved))


class GrantTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 9, 8, tzinfo=timezone.utc)
        self.options = dict(now=self.now, expires_at=self.now + timedelta(minutes=10),
                            parent_active=True, parent_expires_at=self.now + timedelta(minutes=5), bound=True)

    def test_valid_bound_child_allowed(self):
        self.assertTrue(child_authorized(**self.options))

    def test_child_expiry_boundary_is_denied(self):
        self.options["expires_at"] = self.now
        self.assertFalse(child_authorized(**self.options))

    def test_parent_expiry_bounds_child_even_before_child_expiry(self):
        self.options["parent_expires_at"] = self.now
        self.assertFalse(child_authorized(**self.options))

    def test_parent_revocation_blocks_bound_child(self):
        self.options["parent_active"] = False
        self.assertFalse(child_authorized(**self.options))

    def test_independent_child_still_checks_own_revocation(self):
        self.options.update(bound=False, parent_active=False, revoked=True)
        self.assertFalse(child_authorized(**self.options))

    def test_wrong_scope_and_audience_denied(self):
        for key, value in (("scope", "storage:delete"), ("audience", "synthetic://other-tenant")):
            with self.subTest(key=key):
                self.assertFalse(child_authorized(**self.options, **{key: value}))


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name) / "case-999-test"
        self.artifact = self.folder / "evidence/receipt.json"
        write_json(self.artifact, {"performed": False})
        self.manifest = {"case_id": "case-999", "generated_at": "2026-09-08T12:00:00Z", "synthetic_data": True,
                         "artifacts": [{"path": "evidence/receipt.json", "media_type": "application/json",
                                        "sha256": hashlib.sha256(self.artifact.read_bytes()).hexdigest(), "source": "test",
                                        "collection_time": "2026-09-08T12:00:00Z"}]}
        self.save()

    def save(self):
        write_json(self.folder / "manifest.json", self.manifest)

    def test_valid_manifest(self):
        self.assertEqual(validate_manifest(self.folder), 1)

    def test_tampered_content_rejected(self):
        write_json(self.artifact, {"performed": True})
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            validate_manifest(self.folder)

    def test_unmanifested_evidence_rejected(self):
        write_json(self.folder / "evidence/hidden.json", {})
        with self.assertRaisesRegex(ValueError, "coverage"):
            validate_manifest(self.folder)

    def test_duplicate_manifest_path_rejected(self):
        self.manifest["artifacts"] *= 2
        self.save()
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate_manifest(self.folder)

    def test_manifest_traversal_rejected(self):
        self.manifest["artifacts"][0]["path"] = "../outside.json"
        self.save()
        with self.assertRaisesRegex(ValueError, "unsafe"):
            validate_manifest(self.folder)

    def test_manifest_symlink_rejected(self):
        outside = Path(self.temp.name) / "outside.json"
        outside.write_bytes(self.artifact.read_bytes())
        self.artifact.unlink()
        self.artifact.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "symlink"):
            validate_manifest(self.folder)

    def test_manifest_schema_enforces_timestamp(self):
        self.manifest["generated_at"] = "yesterday"
        self.save()
        with self.assertRaises(ValueError):
            validate_manifest(self.folder)

    def test_duplicate_and_forward_parents_rejected(self):
        events = run(4)["events"]
        events[0]["correlation"]["parent_event_id"] = events[-1]["event_id"]
        with self.assertRaisesRegex(ValueError, "parent"):
            validate_trajectory(events)
        events = run(4)["events"]
        events[1]["event_id"] = events[0]["event_id"]
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate_trajectory(events)

    def test_raw_to_normalized_tamper_rejected(self):
        result = run(4)
        folder = next((ROOT / "cases").glob("case-004-*"))
        result["events"][0]["integrity"]["hash"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "digest"):
            check_records(result["events"], result["records"], folder)

    def test_confirmed_graph_requires_resolvable_evidence(self):
        from scripts.build_cases import graph_for
        result = run(4)
        graph = graph_for(result)
        graph["edges"][0]["record_ids"] = ["invented-record"]
        with self.assertRaisesRegex(ValueError, "missing evidence"):
            validate_graph(graph, result["events"], result["records"])


class MappingTests(unittest.TestCase):
    def setUp(self):
        self.event = read_json(ROOT / "schemas/examples/v02/tool-executed.valid.json")

    def test_does_not_invent_w3c_trace_identity(self):
        mapped = to_otel(self.event)
        self.assertNotIn("TraceId", mapped)
        self.assertEqual(mapped["Attributes"]["afr.trace_id"], self.event["correlation"]["trace_id"])

    def test_valid_trace_and_span_pass_through(self):
        self.event["correlation"].update(trace_id="a" * 32, span_id="b" * 16)
        mapped = to_otel(self.event)
        self.assertEqual(mapped["TraceId"], "a" * 32)
        self.assertEqual(mapped["SpanId"], "b" * 16)

    def test_all_zero_trace_rejected_as_correlation_context(self):
        self.event["correlation"]["trace_id"] = "0" * 32
        self.assertNotIn("TraceId", to_otel(self.event))

    def test_nanoseconds_without_float_rounding(self):
        self.assertEqual(unix_ns("1970-01-01T00:00:00.123456789Z"), 123456789)
        self.assertEqual(unix_ns("1970-01-01T01:00:00.123456789+01:00"), 123456789)

    def test_excess_precision_not_silently_truncated(self):
        with self.assertRaisesRegex(ValueError, "precision"):
            unix_ns("2026-09-08T12:00:00.1234567891Z")

    def test_ocsf_requires_source_endpoint_for_api_classification(self):
        self.assertEqual(to_ocsf(self.event)["class_uid"], 0)
        api = to_ocsf(self.event, "synthetic-observed-endpoint")
        self.assertEqual(api["class_uid"], 6003)
        self.assertEqual(api["activity_id"], 2)
        self.assertEqual(api["type_uid"], 600302)

    def test_authorization_is_not_completed_api_activity(self):
        self.event["event_type"] = "ai.tool.authorized"
        self.event["action"]["outcome"] = "authorized"
        mapped = to_ocsf(self.event, "synthetic-endpoint")
        self.assertEqual(mapped["class_uid"], 0)
        self.assertNotIn("status_id", mapped)

    def test_full_envelope_preserved_in_both_targets(self):
        for name, convert in (("ocsf", to_ocsf), ("otel", to_otel)):
            with self.subTest(target=name):
                self.assertEqual(restore(convert(self.event), name), self.event)


if __name__ == "__main__":
    unittest.main()
