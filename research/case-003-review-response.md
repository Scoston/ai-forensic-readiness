# Case 003: identity, lease expiry and parent-bound revocation

This technical response addresses the [question in issue 10](https://github.com/Scoston/ai-forensic-readiness/issues/10#issuecomment-5552512712).
It is recorded in the repository as part of the v0.2 review work.

The observed failure is a missing authority-lifecycle dependency. The distinct
child identity is useful for attribution and is not itself the defect. It can
remain distinct while its grant is bounded by the parent grant and its own expiry.

The original lease was issued at `11:00:07Z` with expiry `11:30:07Z`. Parent
revocation occurred at `11:03:00Z`; the child action occurred at `11:05:03Z`.
Therefore the child lease was **not expired** at execution. It remained usable
because `parent_dependency_enforced_at_use` was false and the parent revocation
did not revoke the independent child lease.

| Proposition | Original record | What it supports |
| --- | --- | --- |
| Child lease had its own subject, scope and audience | `token3-0002` | A distinct credential with a recorded parent session |
| Parent was revoked before child execution | `token3-0003` | Parent lifecycle transition |
| Child remained usable after that revocation | `token3-0004`, `authz3-0003` | Surviving authority despite parent isolation |
| Resource authorization allowed the child | `authz3-0004` | An at-use decision before the storage action |
| Expanded response revoked the child lease | `token3-0005`, `token3-0006` | Explicit child revocation and subsequent denial |

Sources: [token broker](../cases/case-003-delegated-credential-containment/evidence/raw/token-broker.jsonl),
[authorization](../cases/case-003-delegated-credential-containment/evidence/raw/authorization.jsonl),
and [findings](../cases/case-003-delegated-credential-containment/findings.md).

The v0.2 fields distinguish `parent_grant_id`, `grant_id`, `lease_id`, credential
subject, scopes, audiences, parent/child expiry, parent dependency enforcement and
revocation mechanism. A production trace should additionally preserve resource-server
decision time, cache behavior, revocation propagation and descendant-denial receipts.

The [supplemental comparison](simulations/case-003-comparison.json) keeps the child
identity distinct in both conditions. With independent authority it acts after
parent revocation. With parent-bound authorization it is denied. Additional tests
cover parent expiry, child expiry, own revocation, scope and audience.

This comparison is a local state machine. It does not inspect cryptographic token
claims or test a live identity provider. The original Case 003 still lacks a full
external delegation inventory; no broader containment claim is added.
