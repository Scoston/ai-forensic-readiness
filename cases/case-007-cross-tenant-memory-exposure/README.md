# Case 007: Cross-tenant memory exposure

**Status:** Complete deterministic simulation bundle for the v0.2 discussion draft.

A shared memory namespace contains a summary written from tenant A. A tenant B workflow retrieves it and uses the returned chunk in a plan. The control checks source and requesting tenant at the memory gateway before the read.

**Investigation question:** Can the source boundary, consumer boundary, returned chunk and resulting plan be linked?

- [Scenario and ground truth](scenario.md)
- [Evidence and source limits](evidence/README.md)
- [AIRG and evidence register](airg.md)
- [Analyst guide](analyst-guide.md)
- [Findings and recovery limits](findings.md)
- [Reproduce both conditions](reproduce.md)

The package contains 6 failure-condition events and 4
control-condition events. No external model, credential, system or person is used.
