# Case 001 — Prompt injection to delegated tool abuse

## Status

Complete synthetic reference investigation for the v0.1 public-review cycle.

## Purpose

This case tests whether an investigator can reconstruct a consequential agent trajectory without relying on the agent's retrospective explanation or hidden developer knowledge.

A synthetic research agent is asked to summarize a public report. Retrieved content contains an untrusted instruction directing the agent to read a restricted document and transmit it to an external validation endpoint. A policy defect permits both operations through a delegated identity. The case then tests prospective revocation, containment validation, and retrospective data disposition.

No real model, credential, confidential information, external service, or network destination is used. All identities and records are fictional, and all domains use the reserved `.invalid` top-level domain.

## Primary claim tested

Influence, policy evaluation, delegated authority, tool execution, downstream data access, outbound transfer, and containment can be reconstructed from correlated evidence while uncertainty about internal model causality and external data disposition remains explicit.

## Investigation questions

1. Which retrieved content materially influenced the action?
2. Were instruction receipt, retrieval, planning, policy evaluation, delegation, tool request, authorization, and execution recorded as distinguishable events?
3. Which human, agent, runtime, and delegated identities formed the authority chain?
4. Can agent, IAM, tool, data-store, and network evidence corroborate the consequential actions?
5. What durable state changed, and which effects are reversible?
6. Can responders prove prospective revocation without overstating retrospective deletion?

## Bundle contents

| Artifact | Purpose |
| --- | --- |
| [`scenario.md`](scenario.md) | System, threat, boundaries, ground truth, and expected trajectory |
| [`analyst-guide.md`](analyst-guide.md) | Investigation questions and suggested pivots without the answer key |
| [`evidence/`](evidence/README.md) | Synthetic raw evidence and normalized AI investigation events |
| [`manifest.json`](manifest.json) | SHA-256 hashes, sources, and collection metadata |
| [`airg.md`](airg.md) | Evidence-backed AI Incident Reconstruction Graph and edge register |
| [`findings.md`](findings.md) | Findings, confidence, gaps, containment, recovery, and measurements |
| [`reproduce.md`](reproduce.md) | Safe procedure for validating and replaying the case |

## Success criterion

A second investigator can:

- identify the initiating principal and complete authority chain;
- distinguish the user instruction from the retrieved prompt injection;
- reconstruct the requested, authorized, and executed operations;
- corroborate the restricted-document read and outbound transfer with independent records;
- classify the disclosure as R3 rather than claiming it was reversed;
- prove that the delegated identity cannot make another authorized call; and
- state that deletion of the external copy is unresolved.

## Expected result

The material trajectory is reconstructable, but the exact internal causal weight assigned by the model is not directly observable. Prospective revocation is independently validated. Retrospective disposition of the transmitted copy remains unresolved by design.
