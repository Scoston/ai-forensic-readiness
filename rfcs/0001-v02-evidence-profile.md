# RFC 0001: v0.2 evidence profile and reproducible case coverage

**Status:** Implemented as a versioned discussion draft, open to technical review.
**Proposal:** [issue 12](https://github.com/Scoston/ai-forensic-readiness/issues/12)
**Date:** September 8, 2026

## Problem

The first three cases identify material evidence that v0.1 represents only in
free text or references. The repository also promises concrete mappings, schema
conformance checks and ten research cases. Its original validator checked selected
properties but accepted, for example, a string in `decision.approval_required`.
That undermines a claimed validation result even though the existing fixtures pass.

## Evidence and proposed disposition

| Proposal | Investigation need | Supporting case | Disposition |
| --- | --- | --- | --- |
| Consequence and reversibility at authorization | Was the effect considered before permission? | 001, 009 | Implement in v0.2 decision group |
| Source trust and chunk identity | What material was used, from which boundary? | 001, 007 | Implement context chunks with trust, digest and source |
| Rule and evaluated inputs | Why was an action permitted? | 001, 005 | Add explicit policy decision support |
| Memory and derivative lineage | What survives source removal? | 002, 004 | Add memory source/derived trust and disposition |
| Scoped validation | What inventory and test support containment? | 001-004 | Require scope, observed/expected result and validator |
| Parent/child authority lifecycle | Why did a child remain authorized? | 003; issue 10 | Model grants and revocation mechanism separately from identity |
| Approval presentation | Did the reviewer see the executed action? | 006 | Preserve displayed evidence and available actions |
| Configuration/evaluation baseline | Which deployment was in use? | 005, 008 | Add immutable references and description digest |
| Missing-source and capture quality | Which conclusions remain unknown? | 010 | Require explicit quality and limitations |
| Machine-readable AIRG | Are reconstruction edges evidence-backed? | 004-010 | Add graph schema and source-reference checks |
| Full JSON Schema checks | Will malformed records actually fail? | Validator defect reproduced during audit | Enforce Draft 2020-12 and date-time checks; add rejection fixtures |
| Hidden model reasoning | Is internal chain of thought necessary? | 001-003 | Exclude from minimum profile; retain observable evidence instead |

The case-derived requirements are implemented for evaluation under the maintainer's
request to complete the repository. This disposition does not assert external
consensus. Public objections can change the candidate without altering the archived v0.1.

## Compatibility decision

The existing event schema retains `0.1.0-draft`. Only its placeholder `$id` becomes
the real repository address. A new schema uses `0.2.0-draft`; additional evidence
groups are not silently imposed on legacy events. The manifest's existing structure
is unchanged, with declared constraints now fully enforced. Consumers must select
the schema by version and reject unknown versions.

The validator now has pinned JSON Schema dependencies. A missing date-time checker
fails explicitly instead of silently bypassing format validation. This ends the
earlier dependency-free validation claim. The simulated state machines themselves
use the standard library and make no network requests.

Original Cases 001-003 and their manifested evidence are preserved byte-for-byte.
New supplemental comparisons are separate artifacts and do not pretend to have
been collected at the original investigation times.

## Privacy, retention and source authority

Each new field exists to answer a case-backed investigation question. References,
chunk IDs and digests support selective capture; they do not justify indiscriminate
retention. Review-display snapshots and tenant provenance may be sensitive in a
real deployment. Limit access, document retention and protect referenced content
outside agent control. No real tokens, prompts, customer data or personal data are
included in the synthetic cases.

The converter preserves the whole input envelope for restoration. This duplicates
metadata into a new output file; use it only with destinations authorized for that
data. A future production exporter should apply an approved minimization policy
and document any lossy mapping rather than silently dropping evidence.

## Existing-standard overlap

OCSF already provides base/API events, metadata, actor, API and resource fields.
OpenTelemetry provides log timestamps, resource attributes and trace correlation.
The reference converter reuses those fields only when semantics match and retains
unmapped AI detail explicitly. Local logical identifiers are not converted into
invented W3C trace IDs. See the versioned source links and field table in
[mappings](../mappings/README.md).

No OCSF extension is registered. No reliance on changing GenAI attribute names is
required for the initial converter. Span links and actual model/tool instrumentation
need deployment-specific testing beyond these offline projections.

## Validation and falsification

Reject malformed booleans, arrays, duplicate references, timestamps and nested
properties; reject evidence tampering, missing artifacts, traversal, symlinks,
duplicate events, dangling graph references and fabricated raw-to-normalized hashes.
Run each failure and control condition. Test parent expiry/revocation boundaries,
scope and audience separately. Preserve every source field across projection round trips.

Falsify operational claims with independent replay against real enforcement
boundaries, blinded reconstruction and alternative interpretations. The deterministic
simulator validates only its explicit state machine. It cannot establish model
causation, human oversight effectiveness, unknown dependency completeness or
production reliability. Those limitations remain in the specification and review kit.

## Deferred external evidence

The 45-day review, real-system integrations and independent reproductions still
require external evidence. The candidate and review materials are complete
without representing those milestones as done.

The v0.2 draft is now [archived on Zenodo](https://doi.org/10.5281/zenodo.22677119).
Its DOI and file contents were verified on September 9, 2026; this establishes
archival provenance, not independent validation of the proposed requirements.
See [publication status](../PUBLISHING.md) for verification details and remaining
owner metadata corrections.
