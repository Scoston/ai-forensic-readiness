# Cross-case findings and v0.2 changes

Cases 001-003 contain the original detailed synthetic evidence bundles; Cases
004-010 contain new executable failure/control simulations. Supplemental models
for 001-003 test their control relationships without replacing the original records.

## Findings and implementation traceability

| Case | Evidence-backed lesson | v0.2 implementation | Unresolved operational question |
| --- | --- | --- | --- |
| 001 | Untrusted context reached authorized export; later denial did not restore confidentiality | Consequence, policy inputs, context trust and scoped validation | How will a deployment establish external copy disposition? |
| 002 | Source removal left durable memory, vector and cache influence | Memory lineage, source/derived trust and consumer scope | Can every historical consumer be enumerated? |
| 003 | Child authority survived parent isolation before lease expiry | Grant lineage and explicit revocation mechanism; boundary tests | How quickly do distributed enforcement points converge? |
| 004 | Mail denial and derivative deletion require different proof | Separate operational and protected-evidence disposition | What survives in backups or unknown recipients? |
| 005 | The same tool name concealed a changed description and operation | Description digest, registry baseline and gateway allowlist | Which cached descriptions must be invalidated? |
| 006 | Approval existed for a misleading presentation | Presented evidence, reviewer options and action binding | How does real workload affect review quality? |
| 007 | Shared retrieval exposed one tenant's context to another | Source tenant, chunk identity and boundary check | Do distributed indexes enforce the same boundary? |
| 008 | Changed deployment lacked a matching evaluation baseline | Deployment/evaluation references and admission comparison | Which component caused a real behavior change? |
| 009 | Correction and local deletion left a recipient copy | R3 at authorization; separate compensation and reversal | Can recipients independently attest disposition? |
| 010 | Execution was visible while provider context was missing | Capture status, missing sources and explicit unknown edge | Which independent sources can narrow the gap? |

## What the evidence establishes

Failure and control conditions produce different outcomes where a modeled control
changes authority, persistence, presentation, isolation or admission. Case 010 keeps
the downstream action constant while changing capture, distinguishing execution
from influence confidence.

These deterministic software experiments support specific relationships in the
model. They do not measure model susceptibility, independent analyst accuracy,
human attention, incident prevalence or production reliability. Cases 006 and 008
do not turn scripted review or a model-version label into a behavioral claim.

## Evidence quality defects fixed

The original checker accepted a string value for approval_required. Full Draft
2020-12 checks now reject that and the other invalid examples. Date-time support
is explicit and fails closed if unavailable. All manifests receive full schema
and path checks; the original consistency checks remain in place.

The new graph format checks endpoints and record/event references. A confirmed
recorded-parent edge must cite its actual linkage. The evidence-gap case preserves
an unknown context edge instead of generating a plausible explanation.

## Review question disposition

The only public technical comment found in the audit was on Case 003. The
[repository response](case-003-review-response.md) distinguishes credential identity
from authority lifecycle and corrects the possible expired-lease interpretation.
Existing public-review threads remain open.

Use the [review kit](review-kit.md) for blind reconstruction, separate validation
and explicit disagreement. Pin the commit and record the supported-edge denominator,
known inventory, missing sources and assistance used. Real-system reproductions
and public comments should determine whether these candidate requirements survive
review. No external reviewer results are fabricated here.
