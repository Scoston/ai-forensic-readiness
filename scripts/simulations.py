"""Deterministic local experiments, not agents, external services or model tests.

Controls change state transitions; conclusions are computed from recorded state.
Logical source separation is illustrative and does not create independent trust.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

try:
    from .evidence import digest
except ImportError:
    from evidence import digest

CASES = {
    1: ("prompt-injection-tool-abuse", "Prompt injection and tool abuse"),
    2: ("persistent-memory-poisoning", "Persistent memory poisoning"),
    3: ("delegated-credential-containment", "Delegated credential containment failure"),
    4: ("unverifiable-revocation", "Unverifiable revocation"),
    5: ("tool-description-manipulation", "Tool description manipulation"),
    6: ("approval-compromise", "Approval compromise"),
    7: ("cross-tenant-memory-exposure", "Cross-tenant memory exposure"),
    8: ("configuration-version-drift", "Model and policy version drift"),
    9: ("irreversible-external-action", "Irreversible external action"),
    10: ("evidence-gap-exercise", "Evidence-gap exercise"),
}


@dataclass
class Lab:
    case: int
    hardened: bool
    records: list = field(default_factory=list)
    events: list = field(default_factory=list)
    state: dict = field(default_factory=dict)

    @property
    def condition(self):
        return "control" if self.hardened else "failure"

    def emit(self, event_type, source, payload, *, parent=None, **groups):
        index = len(self.records) + 1
        rid = f"rec-{self.case:03}-{index:03}"
        eid = f"evt-{self.case:03}-{index:03}"
        time = (datetime(2026, 9, 8, 12, tzinfo=timezone.utc) + timedelta(seconds=index)).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        correlation = {"trace_id": f"sim-case-{self.case:03}-{self.condition}",
                       "session_id": f"session-{self.case:03}", "task_id": f"task-{self.case:03}"}
        if parent:
            correlation["parent_event_id"] = parent
        record = {"record_id": rid, "event_id": eid, "timestamp": time,
                  "source": source, "event_type": event_type, "payload": copy.deepcopy(payload),
                  "parent_event_id": parent, "normalized_groups": copy.deepcopy(groups)}
        self.records.append(record)
        event = {"schema_version": "0.2.0-draft", "event_id": eid, "event_type": event_type,
                 "timestamp": time, "observed_at": time, "sequence": index,
                 "correlation": correlation,
                 "principal": {"agent_id": f"agent-{self.case:03}", "runtime_identity": f"runtime-{self.case:03}",
                               "human_id": "synthetic-requester", "tenant_id": "tenant-lab"},
                 "integrity": {"collector": source, "hash_algorithm": "sha256", "hash": digest(record),
                               "retention_class": "public-synthetic", "access_label": "synthetic-only"},
                 "evidence_refs": [f"evidence/raw/{'records-control' if self.hardened else 'records'}.jsonl#{rid}"],
                 "evidence_quality": {"capture_status": "complete", "confidence": "confirmed",
                                      "limitations": ["Computed by a deterministic simulator; logical sources share one trust domain."]}}
        event.update(copy.deepcopy(groups))
        self.events.append(event)
        return eid

    def decision(self, allow, reason, consequence="high", reversibility="R1"):
        return {"policy_decision": "allow" if allow else "deny", "approval_required": False,
                "consequence": consequence, "reversibility_at_authorization": reversibility,
                "policy_rule_id": f"rule-{self.case:03}-{'control' if self.hardened else 'failure'}",
                "evaluated_input_refs": [f"evidence/raw/{'control-state-before' if self.hardened else 'state-before'}.json"], "reason": reason}

    def action(self, operation, target, outcome):
        return {"tool_id": f"sim-tool-{self.case:03}", "tool_version": "1.0-lab",
                "operation": operation, "target": target, "outcome": outcome,
                "request_id": f"request-{self.case:03}"}

    def probe(self, name, expected, observed, scope, *, result=None, parent=None):
        result = result or ("pass" if expected == observed else "fail")
        return self.emit("ai.state.validated", "sim-validation-controller",
                         {"probe": name, "expected": expected, "observed": observed, "result": result}, parent=parent,
                         validation={"method": name, "scope": scope, "expected": str(expected),
                                     "observed": str(observed), "result": result,
                                     "validator_identity": "sim-validation-controller", "independence": "simulation_only"})


def memory_profile(source="source-mail", disposition="active", tenant="tenant-A"):
    return {"record_id": "memory-1", "source_refs": [source], "writer_id": "sim-summarizer",
            "transformation_ref": "summary-transform-1", "value_sha256": digest("synthetic-summary"),
            "derivative_ids": ["vector-1", "cache-1"], "consumer_scope": tenant,
            "source_trust": "untrusted-content", "derived_trust": "untrusted-content", "disposition": disposition}


def delegation_profile(bound):
    return {"grant_id": "grant-child", "parent_grant_id": "grant-parent", "parent_agent_id": "agent-parent",
            "child_agent_id": "agent-child", "lease_id": "lease-child", "credential_subject": "runtime-child",
            "scopes": ["storage:move"], "audiences": ["synthetic://storage"], "issued_at": "2026-09-08T11:59:00Z",
            "expires_at": "2026-09-08T12:30:00Z", "parent_expires_at": "2026-09-08T12:30:00Z",
            "parent_dependency_enforced_at_use": bound, "revocation_mechanism": "parent_bound" if bound else "independent",
            "task_id": "child-task"}


def child_authorized(*, now, expires_at, parent_active, parent_expires_at, bound, revoked=False,
                     scope="storage:move", audience="synthetic://storage"):
    """A separate child identity is allowed. Authority is bounded at resource use."""
    if revoked or now >= expires_at or scope != "storage:move" or audience != "synthetic://storage":
        return False
    return not bound or (parent_active and now < parent_expires_at)


def run(case, hardened=False):
    if case not in CASES:
        raise ValueError("case must be 1 through 10")
    lab = Lab(case, hardened)
    start = lab.emit("ai.instruction.received", "sim-instruction-vault",
                     {"instruction": "Perform only the described synthetic exercise.", "condition": lab.condition})
    before = {}
    if case == 1:
        before = {"copied": False, "session_active": True}
        lab.state = copy.deepcopy(before)
        input_event = lab.emit("ai.context.retrieved", "sim-retrieval", {"chunk_id": "chunk-1", "trust": "untrusted", "instruction": "export synthetic restricted report"}, parent=start)
        allowed = not hardened
        auth = lab.emit("ai.policy.evaluated", "sim-policy", {"trust": "untrusted", "allow": allowed}, parent=input_event,
                        decision=lab.decision(allowed, "untrusted context must not grant export scope", reversibility="R3"))
        if allowed:
            lab.state["copied"] = True
            lab.emit("ai.tool.executed", "sim-egress", {"external_copy": True}, parent=auth,
                     action=lab.action("export", "synthetic://external-copy", "succeeded"), decision=lab.decision(True, "unsafe trust promotion", reversibility="R3"))
        lab.state["session_active"] = False
        lab.probe("prospective-access", False, lab.state["session_active"], "one synthetic session")
        lab.probe("external-copy-absent", False, lab.state["copied"], "one simulated recipient")
        conclusion = {"unauthorized_export": lab.state["copied"], "prospective_denied": True,
                      "retrospective_resolved": not lab.state["copied"]}
    elif case == 2:
        before = {"source_present": True, "memory_active": False, "ticket_status": "open"}
        lab.state = copy.deepcopy(before)
        seed = lab.emit("ai.memory.written", "sim-memory", {"instruction": "close ticket", "source_trust": "untrusted"}, parent=start, memory=memory_profile("source-poison"))
        lab.state.update(source_present=False, memory_active=not hardened)
        lab.emit("ai.context.filtered", "sim-source-control", {"source_present": False, "invalidate_derivatives": hardened}, parent=seed)
        if lab.state["memory_active"]:
            read = lab.emit("ai.memory.read", "sim-memory", {"consumed": "memory-1"}, parent=seed, memory=memory_profile("source-poison"))
            lab.state["ticket_status"] = "closed"
            lab.emit("ai.tool.executed", "sim-ticket-audit", {"status": "closed"}, parent=read,
                     action=lab.action("close_ticket", "synthetic://ticket-1", "succeeded"), decision=lab.decision(True, "unsafe durable instruction"))
        lab.probe("ticket-remains-open", "open", lab.state["ticket_status"], "one ticket and known memory derivative")
        conclusion = {"delayed_influence": lab.state["ticket_status"] == "closed", "derived_state_active": lab.state["memory_active"]}
    elif case == 3:
        before = {"parent_active": True, "child_active": True, "object_path": "original"}
        lab.state = copy.deepcopy(before)
        issued = lab.emit("ai.delegation.created", "sim-token-broker", delegation_profile(hardened), parent=start, delegation=delegation_profile(hardened))
        lab.state["parent_active"] = False
        revoked = lab.emit("ai.delegation.revoked", "sim-control-plane", {"target": "grant-parent", "child_identity": "runtime-child"}, parent=issued, delegation=delegation_profile(hardened))
        now = datetime(2026, 9, 8, 12, 5, tzinfo=timezone.utc)
        expiry = now + timedelta(minutes=25)
        allow = child_authorized(now=now, expires_at=expiry, parent_active=False, parent_expires_at=expiry, bound=hardened)
        policy = lab.emit("ai.policy.evaluated", "sim-resource-server", {"allow": allow, "lease_expired": now >= expiry, "parent_revoked": True}, parent=revoked, decision=lab.decision(allow, "evaluate descendant grant at use"))
        if allow:
            lab.state["object_path"] = "quarantine"
            lab.emit("ai.tool.executed", "sim-storage-audit", {"object_path": lab.state["object_path"]}, parent=policy,
                     action=lab.action("move_object", "synthetic://object-1", "succeeded"), decision=lab.decision(True, "parent lifecycle not checked"))
        lab.probe("descendant-denial", False, allow, "parent grant, one child lease and one target")
        conclusion = {"child_allowed_after_parent_revocation": allow, "lease_expired": False,
                      "distinct_child_identity": True, "authority_lifecycle_failure": allow}
    elif case == 4:
        before = {"mail_access": True, "summary": "synthetic-summary", "embedding": "vector-1", "cache": "cache-1"}
        lab.state = copy.deepcopy(before)
        mem = lab.emit("ai.memory.written", "sim-derivative-registry", {"source": "mail-1", "derivatives": ["summary", "embedding", "cache"]}, parent=start, memory=memory_profile())
        lab.state["mail_access"] = False
        revoked = lab.emit("ai.policy.evaluated", "sim-mail-gateway", {"mail_access": False}, parent=start, decision=lab.decision(False, "mail grant revoked"))
        lab.probe("mail-api-denied", False, lab.state["mail_access"], "one mail grant", parent=revoked)
        if hardened:
            for key in ("summary", "embedding", "cache"):
                lab.state[key] = None
            lab.emit("ai.memory.deleted", "sim-derivative-registry", {"disposed": ["summary", "embedding", "cache"], "protected_evidence_copy": "retained separately"}, parent=mem, memory=memory_profile(disposition="deleted"))
        residual = [k for k in ("summary", "embedding", "cache") if lab.state[k] is not None]
        lab.probe("operational-derivatives-absent", [], residual, "declared summary, vector and cache only", parent=mem)
        conclusion = {"prospective_revoked": not lab.state["mail_access"], "residual_operational_derivatives": residual,
                      "retrospective_resolved_for_inventory": not residual, "external_copies": "unknown"}
    elif case == 5:
        trusted = {"name": "report-reader", "operation": "read_report", "audience": "internal"}
        altered = {"name": "report-reader", "operation": "export_report", "audience": "external"}
        before = {"registered_digest": digest(trusted), "served_digest": digest(altered), "exported": False}
        lab.state = copy.deepcopy(before)
        selected = altered["operation"]
        description = lab.emit("ai.context.retrieved", "sim-tool-registry", {"approved": trusted, "served": altered, "approved_sha256": digest(trusted), "served_sha256": digest(altered)}, parent=start,
                               ai_component={"tool_manifest_sha256": digest(altered), "deployment_ref": "evidence/raw/state-before.json"})
        requested = lab.emit("ai.tool.requested", "sim-runtime", {"selection": selected}, parent=description,
                             action=lab.action(selected, "synthetic://report-1", "requested"))
        allowed = not hardened or (digest(trusted) == digest(altered) and selected == "read_report")
        auth = lab.emit("ai.policy.evaluated", "sim-gateway", {"allow": allowed, "digest_match": digest(trusted) == digest(altered)}, parent=requested,
                        decision=lab.decision(allowed, "pinned description and explicit operation allowlist", reversibility="R3"))
        if allowed:
            lab.state["exported"] = True
            lab.emit("ai.tool.executed", "sim-egress", {"receipt": "export-1", "exported": True}, parent=auth,
                     action={**lab.action(selected, "synthetic://report-1", "succeeded"), "description_sha256": digest(altered)},
                     decision=lab.decision(True, "unsafe name-only trust", reversibility="R3"))
        lab.probe("unexpected-export-blocked", False, lab.state["exported"], "one registered tool version")
        conclusion = {"description_changed": digest(trusted) != digest(altered), "selected_operation": selected,
                      "export_executed": lab.state["exported"]}
    elif case == 6:
        before = {"target": "synthetic://production-object", "action": "delete_object", "object_exists": True}
        lab.state = copy.deepcopy(before)
        request = lab.emit("ai.tool.requested", "sim-runtime", {"target": before["target"], "operation": before["action"]}, parent=start,
                           action=lab.action(before["action"], before["target"], "requested"))
        display = {"target": before["target"] if hardened else "synthetic://test-object", "effect": "delete" if hardened else "preview"}
        shown = lab.emit("ai.approval.requested", "sim-review-interface", {"displayed": display, "actual": {"target": before["target"], "effect": "delete"}, "can_override": True}, parent=request)
        # Scripted reviewer behavior is explicit; this does not measure humans.
        approved = display["effect"] == "preview"
        oversight = {"reviewer_id": "synthetic-reviewer", "decided_at": "2026-09-08T12:00:04Z",
                     "presented_evidence_refs": [f"evidence/raw/{'records-control' if hardened else 'records'}.jsonl#{lab.records[-1]['record_id']}"],
                     "action_sha256": digest({"target": before["target"], "operation": before["action"]}),
                     "available_actions": ["approve", "deny", "escalate"], "independence": "independent" if hardened else "shared_source",
                     "decision": "approve" if approved else "deny"}
        approval = lab.emit("ai.approval.granted" if approved else "ai.approval.denied", "sim-approval-store", {"approved": approved, "scripted_reviewer": True}, parent=shown, oversight=oversight)
        if approved:
            lab.state["object_exists"] = False
            lab.emit("ai.tool.executed", "sim-object-audit", {"object_exists": False}, parent=approval,
                     action=lab.action(before["action"], before["target"], "succeeded"),
                     decision={**lab.decision(True, "approval accepted despite display mismatch"), "approval_required": True, "approval_ref": f"evidence/raw/{'records-control' if hardened else 'records'}.jsonl#{lab.records[-1]['record_id']}"})
        lab.probe("unintended-deletion-prevented", True, lab.state["object_exists"], "one action and its exact approval display")
        conclusion = {"approved": approved, "display_matches_action": display == {"target": before["target"], "effect": "delete"},
                      "unintended_deletion": not lab.state["object_exists"], "reviewer_could_override": True}
    elif case == 7:
        before = {"source_tenant": "tenant-A", "consumer_tenant": "tenant-B", "memory_namespace": "shared", "exposed": False}
        lab.state = copy.deepcopy(before)
        write = lab.emit("ai.memory.written", "sim-memory-writer", {"tenant": "tenant-A", "chunk_id": "chunk-tenant-A"}, parent=start, memory=memory_profile("source-tenant-A"))
        allowed = not hardened or before["source_tenant"] == before["consumer_tenant"]
        auth = lab.emit("ai.policy.evaluated", "sim-memory-gateway", {"source_tenant": "tenant-A", "request_tenant": "tenant-B", "allow": allowed}, parent=write,
                        decision=lab.decision(allowed, "compare source tenant and consumer boundary"))
        if allowed:
            lab.state["exposed"] = True
            read = lab.emit("ai.memory.read", "sim-retrieval-audit", {"consumer": "tenant-B", "source": "tenant-A", "chunk_id": "chunk-tenant-A"}, parent=auth,
                            memory=memory_profile("source-tenant-A", tenant="tenant-B"), influence={"context_chunks": [{"chunk_id": "chunk-tenant-A", "source_ref": "evidence/raw/state-before.json", "sha256": digest("synthetic-summary"), "trust_label": "tenant-A-private", "tenant_id": "tenant-A"}]})
            lab.emit("ai.plan.created", "sim-runtime", {"consumer": "tenant-B", "influenced_by": "chunk-tenant-A"}, parent=read)
        lab.probe("cross-tenant-read-denied", False, lab.state["exposed"], "two named synthetic tenants and one shared memory entry")
        conclusion = {"cross_tenant_exposure": lab.state["exposed"], "source_tenant": "tenant-A", "consumer_tenant": "tenant-B",
                      "affected_decision": "tenant-B-plan" if lab.state["exposed"] else None}
    elif case == 8:
        baseline = {"model": "synthetic-v1", "policy": "read-only", "prompt": "prompt-1", "tool": "tool-1"}
        deployed = {**baseline, "policy": "allow-delete", "model": "synthetic-v2"}
        before = {"baseline": baseline, "deployed": deployed, "object_exists": True}
        lab.state = copy.deepcopy(before)
        changed = lab.emit("ai.state.changed", "sim-deployment-controller", {"baseline": baseline, "deployed": deployed, "baseline_sha256": digest(baseline), "deployed_sha256": digest(deployed)}, parent=start,
                           ai_component={"model_id": "synthetic", "model_version": deployed["model"], "policy_version": deployed["policy"], "system_prompt_version": deployed["prompt"], "deployment_ref": "evidence/raw/state-before.json", "evaluation_ref": "synthetic://evaluation/baseline-v1"})
        allowed = deployed["policy"] == "allow-delete" and (not hardened or digest(baseline) == digest(deployed))
        auth = lab.emit("ai.policy.evaluated", "sim-runtime-admission", {"allow": allowed, "baseline_matches": digest(baseline) == digest(deployed)}, parent=changed,
                        decision=lab.decision(allowed, "admission requires evaluated configuration digest"))
        if allowed:
            lab.state["object_exists"] = False
            lab.emit("ai.tool.executed", "sim-object-audit", {"object_exists": False}, parent=auth,
                     action=lab.action("delete_object", "synthetic://object-1", "succeeded"), decision=lab.decision(True, "unevaluated drift admitted"))
        lab.probe("unevaluated-change-blocked", True, lab.state["object_exists"], "one deployment manifest and evaluation baseline")
        conclusion = {"configuration_drift": digest(baseline) != digest(deployed), "unevaluated_action_executed": not lab.state["object_exists"],
                      "model_causation": "not tested; decision comes from explicit policy code"}
    elif case == 9:
        before = {"published": False, "local_copy": True, "external_copy": False, "correction_issued": False}
        lab.state = copy.deepcopy(before)
        requested = lab.emit("ai.tool.requested", "sim-runtime", {"operation": "publish", "reversibility": "R3"}, parent=start,
                             action=lab.action("publish", "synthetic://public-message", "requested"))
        allowed = not hardened
        auth = lab.emit("ai.policy.evaluated", "sim-publication-gateway", {"allow": allowed, "consequence": "high", "reversibility": "R3"}, parent=requested,
                        decision=lab.decision(allowed, "R3 publication needs independent approval; absent in exercise", reversibility="R3"))
        if allowed:
            lab.state.update(published=True, external_copy=True)
            receipt = lab.emit("ai.tool.executed", "sim-recipient-receipt", {"publication_id": "publication-1", "external_copy": True}, parent=auth,
                               action=lab.action("publish", "synthetic://public-message", "succeeded"), decision=lab.decision(True, "irreversibility omitted by unsafe gate", reversibility="R3"))
            lab.state.update(local_copy=False, correction_issued=True)
            lab.emit("ai.state.compensated", "sim-response-controller", {"local_deleted": True, "correction_issued": True, "external_copy": True}, parent=receipt,
                     state={"reversibility_class": "R3", "disposition": "compensated", "disposition_scope": "local copy and correction only"})
        lab.probe("external-copy-absent", False, lab.state["external_copy"], "one simulated recipient; no real recipient deletion proof")
        conclusion = {"published": lab.state["published"], "correction_is_reversal": False,
                      "external_copy_remains": lab.state["external_copy"], "authorization_considered_R3": hardened}
    else:
        before = {"provider_sampling": 1.0 if hardened else 0.0, "object_state": "original"}
        lab.state = copy.deepcopy(before)
        observed_parent = start
        if hardened:
            observed_parent = lab.emit("ai.context.retrieved", "sim-provider-log", {"chunk_id": "chunk-10", "source": "synthetic-retrieval"}, parent=start)
        else:
            lab.emit("ai.evidence.exported", "sim-collector-health", {"missing_source": "provider-context", "sampling_rate": 0.0}, parent=start,
                     evidence_quality={"capture_status": "partial", "confidence": "confirmed", "limitations": ["Provider context was not captured; cause is unknown."], "missing_sources": ["provider-context"], "sampling_rate": 0.0})
        gateway = lab.emit("ai.tool.requested", "sim-tool-gateway", {"request_id": "request-010", "operation": "move_object"}, parent=observed_parent,
                           action=lab.action("move_object", "synthetic://object-1", "requested"))
        lab.state["object_state"] = "moved"
        executed = lab.emit("ai.tool.executed", "sim-storage-audit", {"request_id": "request-010", "object_state": "moved"}, parent=gateway,
                            action=lab.action("move_object", "synthetic://object-1", "succeeded"), decision=lab.decision(True, "recorded resource-server permission"))
        captured = any(r["source"] == "sim-provider-log" for r in lab.records)
        lab.probe("context-capture-available", True, captured, "one provider context record", result="pass" if captured else "unknown", parent=executed)
        conclusion = {"execution_confirmed_in_simulation": lab.state["object_state"] == "moved", "context_observed": captured,
                      "influence_confidence": "inferred" if captured else "unknown", "internal_reasoning": "unknown"}
    return {"case_id": f"case-{case:03}", "condition": lab.condition, "synthetic_data": True,
            "method": "deterministic-state-machine", "state_before": before, "state_after": lab.state,
            "records": lab.records, "events": lab.events, "conclusion": conclusion}


def standalone(case):
    """Make a single-file result whose evidence refs resolve within that file."""
    comparison = {"method": "supplemental deterministic model; not replay of the original event times"}
    for control in (False, True):
        result = run(case, control)
        condition = result["condition"]
        record_index = {r["record_id"]: i for i, r in enumerate(result["records"])}
        def rewrite(value):
            if isinstance(value, dict):
                return {k: rewrite(v) for k, v in value.items()}
            if isinstance(value, list):
                return [rewrite(v) for v in value]
            if isinstance(value, str) and value.startswith("evidence/raw/"):
                if ".jsonl#" in value:
                    rid = value.split("#", 1)[1]
                    return f"#/{condition}/records/{record_index[rid]}"
                if value.endswith("state-before.json"):
                    return f"#/{condition}/state_before"
                if value.endswith("state-after.json"):
                    return f"#/{condition}/state_after"
            return value
        result = rewrite(result)
        by_event = {r["event_id"]: r for r in result["records"]}
        for event in result["events"]:
            event["integrity"]["hash"] = digest(by_event[event["event_id"]])
        comparison[condition] = result
    return comparison
