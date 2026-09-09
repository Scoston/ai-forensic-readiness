# AI Forensic Readiness
[![v0.2 DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22677119.svg)](https://doi.org/10.5281/zenodo.22677119)
> A working model for reconstructing, attributing, containing, validating, and recovering from consequential actions performed or influenced by autonomous AI systems.

**Status:** v0.2 discussion draft archived on Zenodo and open for review
**Author:** Dr. Stephen Coston
**Public review:** Open through October 17, 2026 - [Submit feedback](https://github.com/Scoston/ai-forensic-readiness/issues/1)

AI systems increasingly act through tools, delegated identities, persistent memory, retrieval systems, cloud services, and other agents. Existing telemetry may prove that an API call or state change occurred while failing to preserve the instructions, context, authority, delegation, or persistent influence that caused it.

This project proposes a forensic-readiness model for closing that investigation and recovery gap.

## Start here

- [Read the v0.2 discussion draft](spec/AI-Forensic-Readiness-v0.2.md)
- [Download the archived v0.2 report, briefing and repository bundle](https://zenodo.org/records/22677119)
- [Practitioner briefing](research/practitioner-briefing.md)
- [Cross-case findings and limits](research/cross-case-findings.md)
- [Read the v0.1 specification](spec/AI-Forensic-Readiness-v0.1.md)
- [Review the reference architecture](architecture/README.md)
- [Inspect the event schema](schemas/ai-investigation-event.schema.json)
- [Run the maturity assessment](assessments/maturity-assessment.md)
- [Explore the reference investigations](cases/README.md)
- [Download reviewer packs and submit a technical review](research/review-kit.md)
- [Finish the GitHub release and repository settings](release/OWNER-STEPS.md)
- [Comment or contribute](CONTRIBUTING.md)

## Implemented investigation coverage

All ten scenarios in the original research backlog now have investigation bundles.
Cases 001-003 preserve their original evidence; Cases 004-010 add deterministic
failure/control simulations. Supplemental control models cover 001-003. The
committed bundles contain **158 normalized events and 120 manifested artifacts**.
The simulator runs **20 conditions** across all ten scenarios.

The new work includes versioned evidence profiles, content-chunk identity, memory
lineage, grant lifecycle, approval presentation, scoped validation, evidence gaps,
an evidence-linked graph format and local OCSF/OTel reference converters.

These are synthetic investigations and deterministic software experiments. They
do not establish production readiness, real-model behavior, effective human
oversight or independent external validation. See [publication status](PUBLISHING.md)
and [RFC 0001](rfcs/0001-v02-evidence-profile.md) for disposition and remaining external steps.

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
| `mappings/` | Concrete OCSF/OTel projections, examples and loss disclosures |
| `scripts/` | Validation, offline simulations and local converters |
| `tests/` | Control, conformance, integrity and mapping regression tests |
| `research/` | Cross-case synthesis, practitioner briefing and technical review kit |
| `rfcs/` | Proposed changes and design decisions |
| `.github/` | Review, issue, and pull-request workflows |

## Local validation

Use Python 3.12 or 3.13. Install the pinned validation dependencies, then run:

```bash
python -m pip install -r requirements.txt
python scripts/validate.py
python scripts/build_cases.py --check
python -m unittest discover -s tests -v
```

Run a case without external systems or model calls:

```bash
python scripts/run_case.py --case 3 --output dist/case-003-comparison.json
```

The output contains both conditions. Choose a fresh output path for each saved
run. [PowerShell and Linux setup](cases/case-004-unverifiable-revocation/reproduce.md)
and [converter usage](mappings/README.md) are included.

The canonical Mermaid document is statically linted with the Mermaid diagram tooling during release preparation. Host rendering should also be reviewed after publication because GitHub's Mermaid version may differ from local validation profiles.

## Release posture

Version 0.2 is an archived discussion draft. Public review remains open through October 17, 2026. Proposed requirements should be validated through controlled investigations before being presented as mature practice. Every proposed field or control should answer a documented investigation question and include privacy, retention, and existing-standard considerations.

## Licensing

- Specification, explanatory text, and diagrams: [CC BY 4.0](LICENSE-SPECIFICATION.md)
- Schemas, examples, and code: [Apache License 2.0](LICENSE-CODE)

## Cite this work

Coston Jr., Stephen. (2026). *AI Forensic Readiness v0.2 — Discussion Draft*
(Version 0.2.0-draft). Zenodo. [10.5281/zenodo.22677119](https://doi.org/10.5281/zenodo.22677119).

The version DOI and `CITATION.cff` identify the archive of commit
`2db88053c8579e4db7aa6a5a45ea4c325a787ec9`. Cite an exact Git commit for later
repository changes. The archived PDFs and specification retain their original
pre-publication wording; use this citation for the subsequently assigned DOI.

The [v0.1 archive](https://doi.org/10.5281/zenodo.22255979) remains available for
citations to that version. The [concept DOI](https://doi.org/10.5281/zenodo.22255978)
identifies the version family; use the v0.2 DOI above when citing this draft.
