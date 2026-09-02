# Case 002 — Persistent memory poisoning

## Status

Design scaffold; evidence bundle not yet generated.

## Scenario

An agent encounters a synthetic malicious assertion, stores a derived memory, and ends the original session. Days later, a different workflow retrieves that memory and acts on it after the original source has been removed.

## Questions tested

1. Can the original source be linked to the memory write and later read?
2. Which transformations occurred between source, summary, embedding, memory, and downstream action?
3. Which workflows or agents could retrieve the poisoned state?
4. Does source removal leave actionable derived state behind?
5. Can investigators quarantine, delete, rebuild, and independently validate the affected stores?

## Success criterion

The case identifies all known memory reads, writes, derivatives, and consumers; demonstrates why deleting the original source is insufficient; and validates remediation of persistent influence.

