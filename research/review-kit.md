# Technical review and independent exercise kit

**Review window:** through October 17, 2026. Use [issue 1](https://github.com/Scoston/ai-forensic-readiness/issues/1)
for general feedback and [issue 12](https://github.com/Scoston/ai-forensic-readiness/issues/12)
for v0.2 changes. Existing case review threads remain open.

The repository contains synthetic cases and deterministic tests. This kit is ready
for external reviewers; it does not record invitations sent or independent reviews completed.

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

## Blind exercise procedure

1. Record the exact Git commit, case, participant role and start time.
2. Give the investigator only `evidence/`, `manifest.json` and `analyst-guide.md`.
   Do not supply findings, ground truth or simulator code initially.
3. Ask for the six-question reconstruction and an evidence-linked graph.
4. Require a separate list of unknowns, alternative explanations and missing logs.
5. Reveal the scenario and findings. Record disagreements before discussion.
6. Have a different person validate containment/recovery against the artifacts.
7. Record elapsed time and supported/unsupported graph edges without treating
   assisted answers or repeated runs by the same author as independent replication.

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
