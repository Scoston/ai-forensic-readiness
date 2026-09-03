# Case 002 — Persistent memory poisoning

## Status

Complete synthetic reference investigation for the v0.1 public-review cycle.

## Purpose

This case tests whether an investigator can reconstruct malicious influence that crosses session boundaries through persistent memory and determine whether containment addressed the source, the stored assertion, its indexed derivative, known consumers, and the downstream state change.

A synthetic knowledge agent retrieves an untrusted runbook containing an instruction to store a false emergency-approval rule. The agent writes a derived assertion to shared memory. The source is removed, but two days later a separate operations session retrieves the stored assertion and closes a synthetic incident ticket contrary to the user's instruction. Responders preserve the poisoned record in forensic quarantine, remove it from active memory, rebuild the index, invalidate the cache, reopen the ticket, and run a controlled comparison.

No real model, credential, personal information, external service, or production system is used. All identities and records are fictional, and all domains use the reserved `.invalid` top-level domain.

## Primary claim tested

Removing an original malicious source does not contain durable derived influence. Source-to-memory lineage, cross-session retrieval, consequential execution, downstream state, and remediation can be reconstructed without claiming access to private model reasoning.

## Investigation questions

1. Can the source be linked to the memory write and the later read?
2. Which transformations occurred between retrieved content, derived assertion, index entry, and injected context?
3. Which agents, sessions, workflows, and caches could retrieve the poisoned state?
4. Did source removal occur before the later consequential action?
5. Can tool execution and ticket state be corroborated independently of the agent record?
6. Does controlled replay support the influence finding while preserving uncertainty about private reasoning?
7. Did containment remove active retrieval paths while preserving evidence?

## Bundle contents

| Artifact | Purpose |
| --- | --- |
| [`scenario.md`](scenario.md) | System, threat, boundaries, ground truth, and cross-session trajectory |
| [`analyst-guide.md`](analyst-guide.md) | Investigation questions and suggested pivots without the answer key |
| [`evidence/`](evidence/README.md) | Synthetic raw evidence and normalized AI investigation events |
| [`manifest.json`](manifest.json) | SHA-256 hashes, sources, and collection metadata |
| [`airg.md`](airg.md) | Evidence-backed AI Incident Reconstruction Graph and edge register |
| [`findings.md`](findings.md) | Findings, confidence, gaps, containment, recovery, and measurements |
| [`reproduce.md`](reproduce.md) | Safe validation and controlled-replay procedure |

## Success criterion

A second investigator can:

- link the untrusted source to the derived memory and indexed representation;
- identify the later session that retrieved the poisoned assertion;
- reconstruct the policy and tool path that closed the ticket;
- prove that source removal preceded, but did not prevent, the later action;
- distinguish evidence preservation from active-memory removal;
- validate the reopened ticket and absence of the poisoned record from known active retrieval paths; and
- explain why the controlled comparison supports influence without exposing private reasoning.

## Expected result

The cross-session trajectory is reconstructable. Source removal alone failed because the derived assertion and index entry remained active. The ticket closure is R1 and was directly reversed. Known active retrieval paths were remediated and independently validated, while unobserved historical consumption remains an explicit evidence gap.
