# Technical review and independent exercise kit

**Review window:** through October 17, 2026. Use [issue 1](https://github.com/Scoston/ai-forensic-readiness/issues/1)
for general feedback and [issue 12](https://github.com/Scoston/ai-forensic-readiness/issues/12)
for v0.2 changes. Existing case review threads remain open.

The repository contains synthetic cases and deterministic tests. This kit is ready
for external reviewers; it does not record invitations sent or independent reviews completed.

## Download and submit

- [Download the ten-case reviewer package](https://github.com/Scoston/ai-forensic-readiness/raw/refs/heads/main/release/reviewer-packs-v0.2.zip)
- [Package SHA-256](../release/reviewer-packs-v0.2.sha256)
- [Investigator instructions](reviewer-instructions.md)
- [Submit an actual review or reproduction result](https://github.com/Scoston/ai-forensic-readiness/issues/new?template=review-result.yml)

The package contains 78 raw artifacts copied byte for byte from archived commit
`2db88053c8579e4db7aa6a5a45ea4c325a787ec9`, plus derived manifests and empty response
forms. It is a later review aid, outside the original Zenodo deposit. Each derived
manifest preserves the included artifacts' original SHA-256 hashes and identifies
the intentionally withheld files. These packaging omissions are not incident
telemetry gaps. The original manifests and complete source remain in the
[Zenodo archive](https://zenodo.org/records/22677119).

To reproduce and check the package from a full Git checkout:

```bash
python scripts/build_review_packs.py --output release/reviewer-packs-v0.2.zip --check
```

## Review assignments

| Expertise | Review question | Starting material |
| --- | --- | --- |
| DFIR / incident response | Can another investigator reach the conclusion with these artifacts and no private developer explanation? | Case evidence and analyst guides |
| IAM / cloud | Are parent grants, independent grants and cascading revocation distinguished correctly? | Case 003 response and grant tests |
| AI platform / retrieval | Can content transformations and derivative consumers be reconstructed? | Cases 002, 004, 007 |
| Human factors / governance | Does approval evidence support only the claims it can establish? | Case 006 and v0.2 section 6 |
| Privacy / records | Is content minimized and operational deletion distinguished from protected retention? | v0.2 sections 5 and 8 |
| OCSF / observability | Are types and identity/time semantics mapped without unsupported claims? | Mapping table, converter and tests |

Select named reviewers and confirm the contact route before sending invitations.
No private employer information or confidential incident evidence is needed.

## Evidence reconstruction procedure

1. Record the exact Git commit, case, participant role and start time.
2. Give the investigator `instructions.md` and one `case-NNN/` directory from the
   reviewer package. Verify the included artifact hashes before starting. Do not
   provide the original evidence folder or analyst guide: those contain author
   interpretations, graphs or replay answers.
3. Ask for the six-question reconstruction, an evidence-linked graph and the
   completed `response.md`. Record prior familiarity and any assistance.
4. Require a separate list of unknowns, alternative explanations and missing logs.
5. Save the initial response, then reveal the full scenario, findings, analyst
   guide, normalized events, graph and replay results from the archived source.
   Record disagreements before discussion.
6. Have a different person validate containment/recovery against the artifacts.
7. Record elapsed time and supported/unsupported graph edges without treating
   assisted answers or repeated runs by the same author as independent replication.

This is an evidence-first exercise, not a claim of formal blinding. The source is
public, and raw records may themselves contain system claims or descriptive
identifiers. Record those limitations when interpreting reviewer performance.

## Result form

| Field | Reviewer entry |
| --- | --- |
| Commit and case | |
| Reviewer role; relevant experience | |
| Relationship or potential conflict | |
| Materials provided; assistance used | |
| Start/end time and interruptions | |
| Reconstructed authority path | |
| Supported material nodes/edges; denominator | |
| Incorrect or disputed conclusions and supporting records | |
| Missing sources and effect on confidence | |
| Containment inventory and independently verified paths | |
| Reversal, compensation and residual disposition | |
| Suggested requirement/schema change | |
| Consent to public attribution | |

Only publish results and attribution with the contributor's permission. A public
review should distinguish operational experience, live controlled experiments,
this deterministic laboratory, standards analysis and opinion.

## Invitation draft

I am seeking technical criticism of the AI Forensic Readiness discussion draft.
The repository includes ten synthetic investigation cases, explicit evidence gaps,
scoped containment results and reproducible checks. Could you review the part
closest to your work and identify unsupported conclusions, missing evidence or
incompatible field mappings? The current review period closes October 17, 2026.
Please cite the case, artifact or proposed requirement when possible.

Project: https://github.com/Scoston/ai-forensic-readiness
