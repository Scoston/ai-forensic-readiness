# AI Forensic Readiness: practitioner briefing

**Dr. Stephen Coston | September 8, 2026 | v0.2 discussion draft**

## The operational problem

An enterprise may know that a credential changed a system while being unable to
reconstruct the AI workflow behind that change. Missing evidence can include the
source content, delegated grant, approval presentation, persistent memory and
downstream effects. Those gaps affect investigation and containment.

AI Forensic Readiness provides a working specification, event schemas, reference
investigations and assessment materials for designing that evidence before an
incident. It asks six questions: who acted, what influenced the action, what was
requested and completed, where the inputs originated, what persisted, and what
can be contained or recovered.

## What the repository now provides

Ten cases cover prompt injection, durable memory poisoning, delegation, revocation,
tool descriptions, approvals, tenant isolation, configuration drift, irreversible
actions and missing telemetry. The first three retain their original evidence
bundles. The remaining seven include executable failure and control conditions,
raw records, normalized events, hashes, reconstruction graphs, findings and
reproduction instructions. Supplemental control models cover the first three.

The v0.2 schema adds evidence references and quality, consequence at authorization,
content-chunk identity, memory lineage, grant lifecycle, approval presentation and
scoped validation. Local converters show how to preserve this evidence in OCSF and
OpenTelemetry-oriented representations. Tests check malformed inputs, tampering,
references, grant boundaries, deterministic results and conversion losses.

## Three decisions this changes

**Treat parent isolation as the start of descendant investigation.** In original
Case 003, a child acted 123 seconds after its parent session was revoked. Its lease
had not expired. The failure was a missing authority dependency. A distinct child
identity can remain useful while its authority is bounded by its parent grant.

**Separate access termination from residual data disposition.** Denying a mail API
call does not establish that summaries, vectors, caches or recipient copies are
gone. The cases record prospective denial and retrospective disposition as different
results, with a named inventory and explicit unknowns.

**Preserve what the reviewer actually saw.** An approval record can exist even when
the displayed summary misrepresents the action. Evidence should bind the presentation
to the operation, target, consequence and available rejection path. The approval
case uses a scripted reviewer; it does not measure real human judgment.

## How an enterprise can use it

Choose one consequential AI workflow. Name its business and technical owners and
list the actions it can take. Map the authority chain, persistent stores, queues,
tools and downstream systems. Assign an authoritative source to each investigation
question and preserve the identifiers connecting those records.

Run an exercise using the actual enforcement boundaries. Ask a second investigator
to reconstruct the action from collected evidence. Independently test credential
denial, descendant containment and state recovery. Record unresolved effects and
the person accepting that residual risk.

The maturity assessment is bounded by the weakest capability required for the
selected consequence. Strong logging elsewhere cannot compensate for an untraceable
high-impact agent or an untested containment path.

## What the results support

The repository is a discussion draft with synthetic data and deterministic local
experiments. It provides reviewable models and runnable checks. It does not prove
production readiness, live-provider interoperability, model attack success rates,
complete dependency discovery or effective human oversight.

Hashes detect differences relative to a trusted manifest. They do not authenticate
an author who can rewrite both records and hashes. Production evidence still needs
separate authority, appropriate retention and independent validation.

## Review request

Public review remains open through October 17, 2026. Useful feedback identifies
an unsupported conclusion, a missing authoritative source, an excessive collection
requirement, or a mapping that loses investigative meaning. The review kit includes
focused assignments and a blind-exercise form.

Repository: https://github.com/Scoston/ai-forensic-readiness

Working specification: https://github.com/Scoston/ai-forensic-readiness/blob/main/spec/AI-Forensic-Readiness-v0.2.md

Public review: https://github.com/Scoston/ai-forensic-readiness/issues/1
