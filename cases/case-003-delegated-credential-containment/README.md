# Case 003 — Delegated credential containment failure

## Status

Design scaffold; evidence bundle not yet generated.

## Scenario

Agent A delegates a task to Agent B. Agent B uses a synthetic service identity to modify a downstream application. Agent A is isolated, but the child task and delegated session remain active.

## Questions tested

1. Can investigators reconstruct the human → Agent A → Agent B → delegated identity → target chain?
2. Which tokens, queues, sessions, and tools survive isolation of Agent A?
3. Can capability dependencies be enumerated before containment is declared complete?
4. What independent tests prove that inherited authority is no longer usable?
5. Which changes require rollback, compensation, or residual-risk acceptance?

## Success criterion

Containment is not considered complete until the child task, delegated authority, scheduled work, and downstream state are discovered, addressed, and independently validated.

