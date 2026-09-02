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

## Status

Public review is open through **October 17, 2026**. [Submit feedback](https://github.com/Scoston/ai-forensic-readiness/issues/1). This remains a working practitioner draft, not a formal standard.

Dr. Stephen Coston · September 2026
