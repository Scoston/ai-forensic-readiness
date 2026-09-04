# Case 003 — Delegated credential containment failure

## Status

Complete synthetic reference investigation for the v0.1 public-review cycle.

## Purpose

This case tests whether investigators can reconstruct authority that survives beyond the parent agent that created it and determine whether containment actually removed every usable descendant path.

A synthetic orchestration agent retrieves an untrusted response guide and delegates a storage-quarantine task to a child agent. The delegation service persists the task and a token broker issues the child an independent credential lease. Responders isolate the parent agent and revoke its session, but they do not cancel the queued child task or revoke the child lease. Two minutes later, the child agent uses the synthetic service principal to move a case-export object. Expanded containment cancels the task, revokes the lease, disables the principal, reverses the object move, and independently tests every known authority path.

No real model, credential, personal information, external service, or production system is used. All identities and records are fictional, and all domains use the reserved `.invalid` top-level domain.

## Primary claim tested

Isolating a parent agent does not automatically contain already-issued child tasks, credential leases, or delegated service authority. Containment is complete only when descendant authority and downstream state are enumerated, revoked or recovered, and independently validated.

## Investigation questions

1. Can the human → parent agent → child task → credential lease → service principal → target chain be reconstructed?
2. Which authority artifacts remain usable after parent isolation?
3. Did the child action occur after the parent session was revoked?
4. Can authorization and object-state change be corroborated independently of agent telemetry?
5. Which dependency inventory should define the containment boundary?
6. Can expanded containment prove that each known execution path is unusable?
7. Was the downstream change reversed to the authoritative pre-action state?

## Bundle contents

| Artifact | Purpose |
| --- | --- |
| [`scenario.md`](scenario.md) | System, threat, boundaries, ground truth, and event trajectory |
| [`analyst-guide.md`](analyst-guide.md) | Investigation questions and suggested pivots without the answer key |
| [`evidence/`](evidence/README.md) | Synthetic raw evidence and normalized AI investigation events |
| [`manifest.json`](manifest.json) | SHA-256 hashes, sources, and collection metadata |
| [`airg.md`](airg.md) | Evidence-backed authority and containment graph |
| [`findings.md`](findings.md) | Findings, confidence, gaps, containment, recovery, and measurements |
| [`reproduce.md`](reproduce.md) | Safe validation and containment-test procedure |

## Success criterion

A second investigator can:

- identify the parent instruction and untrusted influence;
- link the parent delegation to the persisted child task and independent credential lease;
- prove that parent isolation preceded the child action;
- show why parent-only containment failed;
- enumerate and revoke the child task, lease, and service-principal path;
- validate that both parent and child authorization paths are denied; and
- prove that the object was restored without claiming that undocumented authority paths cannot exist.

## Expected result

The authority chain is reconstructable. Parent isolation was prospectively effective for the parent but incomplete for already-issued descendant authority. The child object move is R1 and was directly reversed. All deployment-declared authority paths were independently denied after expanded containment; undocumented external delegation remains an explicit inventory limitation.
