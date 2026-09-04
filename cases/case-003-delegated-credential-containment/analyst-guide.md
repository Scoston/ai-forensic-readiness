# Analyst guide

## Objective

Determine whether isolation of the parent agent contained the incident, identify any surviving authority, reconstruct consequential activity after isolation, and evaluate recovery claims.

Do not assume that revoking a parent session recursively revokes a child task or its credential.

## Suggested pivots

### 1. Establish the authorized objective

- Read `evidence/raw/user-instruction.json`.
- Compare the prohibition on changes with the parent plan and delegation record.
- Preserve the instruction digest as the starting provenance value.

### 2. Reconstruct delegation lineage

- Pivot from `delegation-003` to `child-task-003`.
- Identify the child runtime and token-broker issuance record.
- Determine whether the child lease depends on the parent session at use time.

### 3. Build the authority graph

- Human instruction
- Parent session and runtime
- Delegation record
- Queue message and child task
- Child runtime
- Credential lease
- Service principal
- Tool gateway and storage target

Treat each node as a possible containment target, not merely as supporting context.

### 4. Test the initial containment claim

- Find the exact time of parent isolation and session revocation.
- Compare it with the child tool request, authorization, and execution times.
- Review the independent parent and child authorization probes.

### 5. Corroborate the downstream action

- Compare agent telemetry, authorization, tool-gateway, storage-audit, and state snapshots.
- Verify that the moved-object digest and state hash agree across sources.
- Do not infer an object move solely from the agent's claimed result.

### 6. Evaluate expanded containment

- Compare the deployment authority inventory with the response inventory.
- Require a disposition and validation result for every known authority artifact.
- Confirm queue removal, lease revocation, principal disablement, session termination, and policy denial.

### 7. Evaluate recovery

- Compare the authoritative pre-action object state with the restored state.
- Confirm the recovery action used an independent identity.
- Identify any residual uncertainty that cannot be resolved by the available logs.

## Questions for the investigator

1. When did the parent lose authority?
2. Which descendant authority remained usable at that moment?
3. What evidence proves that the child action occurred later?
4. Was the child lease inherited, copied, or independently issued?
5. Which control made parent-only containment incomplete?
6. What tests are necessary before declaring expanded containment complete?
7. What cannot be proven from the declared inventory?

## Expected discipline

Separate confirmed facts, strongly supported influence, and unknown inventory coverage. The case demonstrates a known surviving path; it does not justify a universal claim that all possible delegated authority has been discovered.
