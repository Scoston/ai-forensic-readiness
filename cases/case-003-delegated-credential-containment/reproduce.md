# Reproduction and validation

## Safety

This case is a static synthetic fixture. Do not replace `.invalid` endpoints or fictional identities with production systems. No model invocation, token issuance, storage API, or network connection is required.

## Prerequisites

- Python 3.12 or a compatible Python 3 release
- Git
- A local checkout of this repository

## Validate the repository

From the repository root:

```powershell
python .\scripts\validate.py
```

Expected Case 003 results:

```text
Case 003 normalized events: OK (32 events)
Case 003 evidence manifest: OK (15 artifacts)
Case 003 delegation and containment consistency: OK
```

## Manual reconstruction

1. Read `evidence/raw/user-instruction.json` and record the prohibition on changes.
2. Link the retrieved directive to the parent plan in `agent-runtime.jsonl`.
3. Follow `delegation-003` through `delegation-audit.jsonl`, `task-queue.jsonl`, and `token-broker.jsonl`.
4. Record the parent isolation and revocation time from `containment-validation.json`.
5. Compare the parent and child probe results in `authorization.jsonl`.
6. Follow the child request through authorization, tool execution, and `downstream-audit.jsonl`.
7. Compare `state-before.json` and both sections of `state-after.json`.
8. Confirm every deployment-declared authority artifact has a terminal disposition and validation result.
9. Compare the result with the AIRG edge register and findings.

## Integrity check

Every file under `evidence/` is listed in `manifest.json` with a SHA-256 digest. The validator rejects missing, additional, duplicated, unsafe, or modified evidence artifacts.

To inspect one file manually:

```powershell
(Get-FileHash .\cases\case-003-delegated-credential-containment\evidence\raw\token-broker.jsonl -Algorithm SHA256).Hash
```

Compare the result with the matching manifest entry.

## Containment test logic

The fixture requires two phases:

### Parent-only containment

- parent runtime: deny
- parent session: revoked
- child task: still queued
- child lease: allow
- service principal: enabled

This phase must be classified incomplete.

### Expanded containment

- parent runtime: deny
- child runtime: deny
- child task: canceled and absent from queue
- child lease: revoked and denied
- service principal workflow binding: disabled
- target object: restored to the pre-action state

This phase may be classified confirmed only for the deployment-declared inventory.

## Tamper test

In a disposable copy, alter one byte in any Case 003 evidence file and rerun the validator. Expected behavior:

```text
ERROR: Case 003 manifest: SHA-256 mismatch for ...
```

Restore the repository copy after the test. Do not modify the authoritative evidence bundle.
