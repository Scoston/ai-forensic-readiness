#!/usr/bin/env python3
"""Generate or verify documented simulation artifacts without changing Cases 001-003."""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

try:
    from .evidence import ROOT, write_json
    from .simulations import CASES, run, standalone
except ImportError:
    from evidence import ROOT, write_json
    from simulations import CASES, run, standalone

DETAILS = {
    4: {
        "scenario": "A mail connector creates a summary, vector entry and retrieval cache. Revoking the mail grant stops new reads, but the three operational derivatives survive. The control condition applies a source-to-derivative inventory and removes the operational copies while leaving protected case evidence separately retained.",
        "change": "Invalidate each declared operational derivative after mail-grant revocation.",
        "question": "Which receipts prove access termination, and which prove derivative disposition?",
        "finding": "Mail access is denied in both conditions. The failure retains three operational derivatives; the control removes all three named derivatives. Neither condition proves the disposition of undocumented external copies.",
        "sources": "Mail-gateway denial, derivative-registry writes/deletions, scoped validation probes and before/after inventory.",
        "containment": "Revoke the mail grant; enumerate summary, vector and cache; remove operational copies; retain evidence under separate access; probe each known consumer.",
        "recovery": "No claim of global erasure. Operational deletion is established only for the three declared derivatives. Protected evidence retention is not a surviving operational access path.",
        "limit": "No real email service, vector store, backup, embedding inversion or deletion attestation is tested.",
        "lesson": "Require separate prospective and retrospective results, derivative lineage and explicit inventory scope.",
    },
    5: {
        "scenario": "The approved report-reader description permits an internal read. A substituted description keeps the tool name but changes operation and audience to export. A deterministic selector follows the served description. The control checks its approved digest and operation allowlist at the gateway.",
        "change": "Enforce the approved capability-description digest and explicit operation allowlist.",
        "question": "Which description did selection use, and did the authorization boundary verify that exact version?",
        "finding": "The served and approved descriptions have different digests in both conditions. The failure executes export_report. The control selects the same proposed operation but denies execution, exposing the distinction between selection and authority.",
        "sources": "Versioned registry descriptions and hashes, runtime selection request, gateway evaluation and synthetic egress receipt.",
        "containment": "Disable the altered capability, pin the approved registry version, invalidate cached descriptions and review downstream export receipts.",
        "recovery": "Denying subsequent exports cannot undo the failure-condition disclosure. Restoring the description repairs the control surface; recipient copy disposition remains outside this laboratory.",
        "limit": "The selector is explicit Python logic. This does not measure prompt-injection susceptibility of any real model or MCP implementation.",
        "lesson": "Record the tool-description digest used for selection and recheck allowed operations at the resource boundary.",
    },
    6: {
        "scenario": "An object-deletion request is presented as a harmless test preview. A scripted reviewer approves previews and denies production deletion. The control presents the actual target and consequence from the request rather than the manipulated display. The approval evidence retains what was displayed and the available rejection path.",
        "change": "Bind the review display to the exact target and consequence of the requested action.",
        "question": "What did the reviewer see, and was that the operation that actually executed?",
        "finding": "A recorded approval exists in the failure condition despite a mismatch between the displayed test preview and actual production deletion. In the control the same scripted reviewer can see the actual deletion and rejects it.",
        "sources": "Tool request, exact review display, approval-store decision and downstream object state.",
        "containment": "Suspend the approval path; compare the displayed action against actual request digests; preserve reviewer choices and presentation history; require an independently populated display.",
        "recovery": "The simulator proves prevention in the control condition. It does not restore the deleted failure-condition object or claim a tested rollback.",
        "limit": "This is a scripted reviewer, not a human-subject experiment. Review time, competence, coercion and real human judgment are unmeasured.",
        "lesson": "Approval is evidence of a decision only within the recorded presentation and authority context.",
    },
    7: {
        "scenario": "A shared memory namespace contains a summary written from tenant A. A tenant B workflow retrieves it and uses the returned chunk in a plan. The control checks source and requesting tenant at the memory gateway before the read.",
        "change": "Enforce tenant-bound retrieval at the memory gateway.",
        "question": "Can the source boundary, consumer boundary, returned chunk and resulting plan be linked?",
        "finding": "The failure exposes tenant A's named chunk to tenant B and records its use in the simulated plan. The control denies the read and emits no downstream memory-read or plan event.",
        "sources": "Memory write, tenant policy evaluation, retrieval receipt with chunk ID and source tenant, consumer plan.",
        "containment": "Disable the shared retrieval route, quarantine the entry, enumerate tenant B consumers and caches, then test both permitted and prohibited boundaries.",
        "recovery": "The control proves denial for the two named tenants. Deletion of every prior consumer copy is unknown; subsequent isolation does not undo an already-observed disclosure.",
        "limit": "One memory record and two synthetic tenants are modeled. Vector-index filtering, distributed cache timing and alternate workflows are not exercised.",
        "lesson": "Tenant and workflow provenance must survive transformations and be checked before retrieval returns content.",
    },
    8: {
        "scenario": "An evaluated baseline uses a synthetic-v1 model and read-only policy. Deployment changes the model label and policy to allow-delete without a matching evaluation baseline. The control pins deployment admission to the evaluated configuration digest.",
        "change": "Require deployed configuration to match the evaluated baseline before execution.",
        "question": "Can the action be pinned to model, prompt, policy, tool and evaluation versions?",
        "finding": "Both conditions contain the same drift. The failure admits a delete under the changed policy; the control blocks the unevaluated configuration. The recorded model-label change alone does not establish model causation.",
        "sources": "Baseline and deployed manifests with hashes, evaluation reference, admission decision and downstream state.",
        "containment": "Block the unevaluated deployment, restore a pinned version, rerun consequence-specific evaluations and retain both manifests for reconstruction.",
        "recovery": "Prevention is demonstrated. No failure-condition restoration, canary reliability or model rollback fidelity is claimed.",
        "limit": "The model names are labels. The explicit policy branch causes the simulated action; no real model behavior is evaluated.",
        "lesson": "Preserve immutable deployment and evaluation references; do not infer causation from version correlation alone.",
    },
    9: {
        "scenario": "A publication request has an R3 confidentiality consequence. The failure permits publication without the independent approval required by the control. A simulated recipient retains a copy. Local deletion and a correction follow, but the recipient copy remains.",
        "change": "Deny high-consequence R3 publication when independent approval is absent.",
        "question": "Was irreversibility considered before authority was granted, and can compensation restore confidentiality?",
        "finding": "The failure publishes and then issues a correction, while its simulated recipient copy remains. The control denies the publication before any receipt. A correction is compensation and does not reverse disclosure.",
        "sources": "Publication request, consequence and reversibility classification, policy evaluation, recipient receipt, compensating-action record and residual-state probe.",
        "containment": "Disable further publication, inventory recipients and propagation, preserve the release receipt and obtain scoped disposition evidence where available.",
        "recovery": "R3 disclosure is irreversible in this exercise. Correction and local removal reduce further harm but cannot support a recovered-confidentiality claim.",
        "limit": "No message is actually sent or published. A synthetic receiver models retained data; real downstream propagation is unmeasured.",
        "lesson": "Evaluate consequence and reversibility at authorization time and keep compensation separate from reversal.",
    },
    10: {
        "scenario": "A provider-context record is deliberately absent while tool-gateway and storage-audit records remain. The control enables context capture. Both conditions execute the same object move, permitting the investigator to separate confirmed execution from an unavailable influence path.",
        "change": "Change provider-context capture from absent to present while preserving the downstream operation.",
        "question": "Which conclusions survive a missing provider record, and which must remain unknown?",
        "finding": "The object move is recorded in both conditions. In the failure, missing provider context leaves influence unknown. In the control, retrieved context is observable, but private reasoning and internal cognitive causation remain unknown.",
        "sources": "Collector-health record, gateway request ID, storage receipt, before/after state and, only in the control, provider context.",
        "containment": "Preserve unsampled gateway and downstream evidence, stop the affected workflow and record the missing-source interval before repairing collection.",
        "recovery": "Collection repair improves future visibility; it cannot reconstruct the historical context that was never captured. The simulator does not reverse the object move.",
        "limit": "A single deliberate drop models evidence loss. Real sampling policies, clock skew, outages and adversarial suppression require deployment testing.",
        "lesson": "Record capture quality and missing sources; an absent log is not evidence that no action occurred.",
    },
}


def graph_for(result):
    nodes = [{"id": e["event_id"], "label": e["event_type"].removeprefix("ai."), "kind": "observation"} for e in result["events"]]
    records = {r["event_id"]: r for r in result["records"]}
    edges = []
    for event in result["events"]:
        parent = event["correlation"].get("parent_event_id")
        if parent:
            edges.append({"id": f"edge-{len(edges)+1}", "source": parent, "target": event["event_id"],
                          "relationship": "recorded_parent", "confidence": "confirmed",
                          "event_ids": [parent, event["event_id"]], "record_ids": [records[event["event_id"]]["record_id"]],
                          "limitation": "Recorded simulator linkage; not independent evidence of cognitive causation."})
    if result["case_id"] == "case-010":
        nodes.append({"id": "unobserved-context", "label": "Missing provider context", "kind": "evidence_gap"})
        target = next(e["event_id"] for e in result["events"] if e["event_type"] == "ai.tool.requested")
        edges.append({"id": "edge-missing", "source": "unobserved-context", "target": target,
                      "relationship": "possible_influence", "confidence": "unknown", "event_ids": [target], "record_ids": [],
                      "limitation": "Provider context was not captured. Do not fill this gap from the simulator's private state."})
    return {"case_id": result["case_id"], "nodes": nodes, "edges": edges}


def materialize_case(root, number):
    slug, title = CASES[number]
    folder = root / "cases" / f"case-{number:03}-{slug}"
    details = DETAILS[number]
    failure, control = run(number), run(number, True)
    for result, prefix, record_name, event_name in [(failure, "", "records", "events"), (control, "control-", "records-control", "control-events")]:
        write_json(folder / f"evidence/raw/{prefix}state-before.json", result["state_before"])
        write_json(folder / f"evidence/raw/{prefix}state-after.json", result["state_after"])
        path = folder / f"evidence/raw/{record_name}.jsonl"
        path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in result["records"]), encoding="utf-8", newline="\n")
        write_json(folder / f"evidence/normalized/{event_name}.json", result["events"])
    experiment = {"case_id": failure["case_id"], "synthetic_data": True,
                  "method": "deterministic-state-machine", "changed_variable": details["change"],
                  "controlled_variables": ["scenario inputs", "scripted decision rules except named control", "logical source set except Case 010 capture", "synthetic clock"],
                  "failure": failure["conclusion"], "control": control["conclusion"],
                  "limitations": [details["limit"], "All sources are generated by one program; no independent production corroboration."]}
    write_json(folder / "evidence/raw/replay-results.json", experiment)
    graph = graph_for(failure)
    write_json(folder / "evidence/airg.json", graph)
    (folder / "evidence/README.md").write_text(f"""# Evidence for Case {number:03}

{details['sources']}

The files use synthetic data only. `records.jsonl` is the failure condition;
`records-control.jsonl` is the control. Each raw record has a stable record ID,
source, payload and declared parent. The normalized envelopes reference those
records and hash their deterministic JSON encoding. The manifest hashes exact
file bytes. These are consistency checks, not signatures or proof of authenticity.

The two conditions share one simulator and clock. Source names show where an
enterprise would collect evidence, not independent trust in this experiment.
`replay-results.json` states controlled and changed variables. The graph records
observed links and explicit unknowns; it does not infer hidden reasoning.
""", encoding="utf-8", newline="\n")
    (folder / "README.md").write_text(f"""# Case {number:03}: {title}

**Status:** Complete deterministic simulation bundle for the v0.2 discussion draft.

{details['scenario']}

**Investigation question:** {details['question']}

- [Scenario and ground truth](scenario.md)
- [Evidence and source limits](evidence/README.md)
- [AIRG and evidence register](airg.md)
- [Analyst guide](analyst-guide.md)
- [Findings and recovery limits](findings.md)
- [Reproduce both conditions](reproduce.md)

The package contains {len(failure['events'])} failure-condition events and {len(control['events'])}
control-condition events. No external model, credential, system or person is used.
""", encoding="utf-8", newline="\n")
    (folder / "scenario.md").write_text(f"""# Scenario and ground truth

{details['scenario']}

## Experiment design

The executable scenario is `scripts/simulations.py`, case {number}. Both conditions
run deterministic Python state transitions. The changed control is:

{details['change']}

Raw source payloads, state snapshots, normalized records and probe results are
generated by execution. The case tests the modeled relationship, not prevalence,
model accuracy, real-world exploitation success, or production containment.

## Trust boundaries and required logs

{details['sources']}

In a real deployment, collect each source under its owning system's authority,
preserve request IDs and content hashes, and export evidence outside agent control.
Here every source is simulated by the same process. {details['limit']}

## Ground-truth boundary

The before/after snapshots describe only the named simulation inventory. A missing
resource or consumer is not proven absent outside that inventory. Failure and
control traces are separate experiments; the control does not erase the failure.
""", encoding="utf-8", newline="\n")
    register = "\n".join(f"| `{r['record_id']}` | `{r['event_id']}` | {r['source']} | {r['event_type']} |" for r in failure["records"])
    (folder / "airg.md").write_text(f"""# AI Incident Reconstruction Graph

The [machine-readable graph](evidence/airg.json) separates supported record links
from missing evidence. `recorded_parent` means an explicit runtime correlation,
not proof that an earlier observation caused the later action.

| Record | Event | Logical source | Observation |
| --- | --- | --- | --- |
{register}

Every confirmed edge cites a raw record. Case 010 also includes an explicitly
unknown context edge without invented source evidence. Source independence in
these bundles is simulated only.
""", encoding="utf-8", newline="\n")
    (folder / "analyst-guide.md").write_text(f"""# Analyst guide

Begin with the evidence files; reserve findings and state-machine code for the
facilitator until the initial reconstruction is complete.

1. {details['question']}
2. Identify the requester, runtime and authority boundary. Where is attribution incomplete?
3. Join raw record IDs to normalized events and check the manifest before using content.
4. Separate requested, permitted and completed actions. Which source proves each?
5. Compare the two conditions. What changed, and what was actually held constant?
6. Identify known persistent effects and write a scoped containment result.
7. Which missing source would change the conclusion? Which claim remains unmeasured?

Record the time spent, disagreements and evidence gaps using the
[blind exercise form](../../research/review-kit.md). Do not infer an empirical
success rate from deterministic replay.
""", encoding="utf-8", newline="\n")
    (folder / "findings.md").write_text(f"""# Findings

## Supported result

{details['finding']}

This result is confirmed within the deterministic model. Supporting records are
listed in [the AIRG register](airg.md); exact comparisons are in
[the replay result](evidence/raw/replay-results.json).

## Containment procedure

{details['containment']}

## Recovery assessment

{details['recovery']}

## Evidence limitations and alternatives

{details['limit']}

No incident frequency, model behavior, human decision quality, latency or complete
enterprise inventory is measured. A real system may implement different delegation,
storage or review semantics. Validate the proposed control at the actual enforcement
boundary before claiming equivalent behavior.

## Proposed v0.2 requirement

{details['lesson']}
""", encoding="utf-8", newline="\n")
    (folder / "reproduce.md").write_text(f"""# Reproduction

From a clean checkout, install validation dependencies once:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# PowerShell: .\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python scripts/build_cases.py --check
python scripts/run_case.py --case {number} --output dist/case-{number:03}-comparison.json
python scripts/validate.py
python -m unittest discover -s tests -v
```

`run_case.py` executes both conditions and writes their complete results to the
chosen local output. `build_cases.py --check` regenerates committed simulation
artifacts in a temporary directory and compares exact bytes, without modifying
evidence. `--write` is for deliberately rebuilding synthetic reference fixtures;
never use it to reseal collected production evidence.

No network access is needed after dependency installation. All timestamps and
identities are synthetic. Repetition is deterministic and is not an independent
experiment or external reproduction.
""", encoding="utf-8", newline="\n")
    artifacts = []
    for path in sorted((folder / "evidence").rglob("*")):
        if path.is_file():
            artifacts.append({"path": path.relative_to(folder).as_posix(), "media_type": "application/x-ndjson" if path.suffix == ".jsonl" else "text/markdown" if path.suffix == ".md" else "application/json",
                              "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "source": "deterministic-laboratory-simulator",
                              "collection_time": "2026-09-08T12:01:00Z", "notes": "Synthetic; no independent evidence collection."})
    write_json(folder / "manifest.json", {"case_id": f"case-{number:03}", "generated_at": "2026-09-08T12:01:00Z", "synthetic_data": True,
                                         "tooling": ["Python standard library", "scripts/simulations.py"], "artifacts": artifacts})


def generate(root):
    for number in range(4, 11):
        materialize_case(root, number)
    for number in range(1, 4):
        # These new comparisons support, but do not replace or regenerate,
        # the original three authored reference investigations.
        write_json(root / f"research/simulations/case-{number:03}-comparison.json", standalone(number))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        generate(ROOT)
        print("Generated Cases 004-010 and supplemental comparisons for 001-003")
    else:
        with tempfile.TemporaryDirectory() as temp:
            generated = Path(temp)
            generate(generated)
            changed = [p.relative_to(generated).as_posix() for p in generated.rglob("*")
                       if p.is_file() and (not (ROOT / p.relative_to(generated)).is_file()
                                          or p.read_bytes() != (ROOT / p.relative_to(generated)).read_bytes())]
            if changed:
                raise ValueError(f"simulation artifacts differ: {changed}")
        print("Deterministic fixture regeneration: OK (all ten scenarios)")


if __name__ == "__main__":
    main()
