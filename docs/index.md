---
layout: default
title: AI Forensic Readiness
description: An open working model for investigating and recovering from consequential AI actions.
---
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22255979.svg)](https://doi.org/10.5281/zenodo.22255979)
# AI Forensic Readiness

When an AI system takes a consequential action, an organization may see fragments of what happened without being able to reconstruct the full chain of instruction, context, delegated authority, execution, persistent state, and recovery.

**AI Forensic Readiness** is a working model for closing that gap.

> The organizational and technical ability to reconstruct, attribute, contain, validate, and recover from consequential actions performed or influenced by AI systems.

## Discussion Draft v0.1

The first draft proposes:

- A six-question investigation model
- A minimum viable AI evidence profile
- The AI Incident Reconstruction Graph
- Dependency-aware containment
- Verifiable revocation
- Reversibility as an authorization property
- A six-level maturity model

[Read the specification](https://github.com/Scoston/ai-forensic-readiness/blob/main/spec/AI-Forensic-Readiness-v0.1.md) · [Run the assessment](https://github.com/Scoston/ai-forensic-readiness/blob/main/assessments/maturity-assessment.md) · [Review the cases](https://github.com/Scoston/ai-forensic-readiness/tree/main/cases) · [Contribute](https://github.com/Scoston/ai-forensic-readiness/blob/main/CONTRIBUTING.md)

## Reference Case 001

### Prompt Injection → Tool Abuse

Case 001 presents a complete synthetic investigation of an AI agent influenced by untrusted retrieved content. The resulting trajectory includes delegated identity use, restricted-data access, an outbound transfer, prospective revocation, and unresolved retrospective data disposition.

The package contains **19 normalized events**, **13 integrity-verified evidence artifacts**, an AI Incident Reconstruction Graph, analyst guidance, findings, containment validation, and reproduction instructions.

[Examine Case 001](https://github.com/Scoston/ai-forensic-readiness/tree/main/cases/case-001-prompt-injection-tool-abuse) · [Review the AIRG](https://github.com/Scoston/ai-forensic-readiness/blob/main/cases/case-001-prompt-injection-tool-abuse/airg.md) · [Submit Case 001 feedback](https://github.com/Scoston/ai-forensic-readiness/issues/4)

## Reference Case 002

### Persistent Memory Poisoning → Delayed Tool Abuse

Case 002 traces untrusted retrieved content into persistent agent memory, a vector derivative, and a cache. Although the original source is removed, the derived state survives and influences a later workflow that closes a synthetic incident ticket without user authorization.

The package contains **35 normalized events**, **15 integrity-verified evidence artifacts**, a controlled replay, an AI Incident Reconstruction Graph, dependency-aware containment, reversal validation, and documentation of unresolved historical consumption.

[Examine Case 002](https://github.com/Scoston/ai-forensic-readiness/tree/main/cases/case-002-persistent-memory-poisoning) · [Review the AIRG](https://github.com/Scoston/ai-forensic-readiness/blob/main/cases/case-002-persistent-memory-poisoning/airg.md) · [Submit Case 002 feedback](https://github.com/Scoston/ai-forensic-readiness/issues/7)

## Reference Case 003

### Delegated Credential Containment Failure

Case 003 demonstrates why isolating a parent agent may not contain authority it has already delegated. A persisted child task and independently issued credential lease remain usable, allowing the child agent to move a synthetic storage object **123 seconds after the parent session was revoked**.

The package contains **32 normalized events**, **15 integrity-verified evidence artifacts**, an authority-focused AI Incident Reconstruction Graph, independent authorization probes, parent-only and expanded containment validation, downstream recovery, and explicit limits on inventory-completeness claims.

[Examine Case 003](https://github.com/Scoston/ai-forensic-readiness/tree/main/cases/case-003-delegated-credential-containment) · [Review the AIRG](https://github.com/Scoston/ai-forensic-readiness/blob/main/cases/case-003-delegated-credential-containment/airg.md) · [Submit Case 003 feedback](https://github.com/Scoston/ai-forensic-readiness/issues/10)

## Status

Public review is open through **October 17, 2026**. [Submit feedback](https://github.com/Scoston/ai-forensic-readiness/issues/1). This remains a working practitioner draft, not a formal standard.

Dr. Stephen Coston · September 2026
