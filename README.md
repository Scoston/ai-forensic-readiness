# AI Forensic Readiness

> A working model for reconstructing, attributing, containing, validating, and recovering from consequential actions performed or influenced by autonomous AI systems.

**Status:** Discussion Draft v0.1  
**Author:** Dr. Stephen Coston  
**Public review:** Open through October 17, 2026 - [Submit feedback](https://github.com/Scoston/ai-forensic-readiness/issues/1)

AI systems increasingly act through tools, delegated identities, persistent memory, retrieval systems, cloud services, and other agents. Existing telemetry may prove that an API call or state change occurred while failing to preserve the instructions, context, authority, delegation, or persistent influence that caused it.

This project proposes a forensic-readiness model for closing that investigation and recovery gap.

## Start here

- [Read the v0.1 specification](spec/AI-Forensic-Readiness-v0.1.md)
- [Review the reference architecture](architecture/README.md)
- [Inspect the event schema](schemas/ai-investigation-event.schema.json)
- [Run the maturity assessment](assessments/maturity-assessment.md)
- [Explore the reference investigations](cases/README.md)
- [Comment or contribute](CONTRIBUTING.md)

## Core contributions proposed for testing

1. A six-question investigation model covering identity, context, execution, provenance, persistence/blast radius, and recovery.
2. A minimum viable evidence profile for consequential AI actions.
3. The AI Incident Reconstruction Graph (AIRG), combining identity, authority, influence, causality, state, and time.
4. Dependency-aware containment across credentials, tools, memory, queues, child agents, and downstream systems.
5. Verifiable revocation, separating future-access termination from disposition of previously acquired or derived data.
6. Reversibility classes that treat safe recovery as an authorization property.
7. A six-level AI forensic-readiness maturity model.

## Project boundaries

This is not a formal standard, a universal security control catalog, or a replacement for incident response, governance, legal discovery, safety assessment, or model evaluation. It is an open practitioner model intended to complement established work such as NIST AI RMF, OCSF, OpenTelemetry, and OWASP agentic-security guidance.

## Repository map

| Path | Purpose |
| --- | --- |
| `spec/` | Normative and explanatory specification drafts |
| `schemas/` | Vendor-neutral JSON Schema and example events |
| `architecture/` | Portable Mermaid diagrams and architecture notes |
| `cases/` | Controlled reference investigations and evidence manifests |
| `assessments/` | Maturity assessment and readiness gate |
| `mappings/` | Initial standards-interoperability notes |
| `rfcs/` | Proposed changes and design decisions |
| `.github/` | Review, issue, and pull-request workflows |

## Local validation

Run the dependency-free repository checks with:

```bash
python scripts/validate.py
```

The canonical Mermaid document is statically linted with the Mermaid diagram tooling during release preparation. Host rendering should also be reviewed after publication because GitHub's Mermaid version may differ from local validation profiles.

## Release posture

Version 0.1 is a discussion draft. Proposed requirements should be validated through controlled investigations before being presented as mature practice. Every proposed field or control should answer a documented investigation question and include privacy, retention, and existing-standard considerations.

## Licensing

- Specification, explanatory text, and diagrams: [CC BY 4.0](LICENSE-SPECIFICATION.md)
- Schemas, examples, and code: [Apache License 2.0](LICENSE-CODE)

## Citation

See [CITATION.cff](CITATION.cff). A DOI should be added after the first public GitHub release is archived through Zenodo.
