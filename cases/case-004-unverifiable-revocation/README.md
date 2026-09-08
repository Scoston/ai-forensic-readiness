# Case 004: Unverifiable revocation

**Status:** Complete deterministic simulation bundle for the v0.2 discussion draft.

A mail connector creates a summary, vector entry and retrieval cache. Revoking the mail grant stops new reads, but the three operational derivatives survive. The control condition applies a source-to-derivative inventory and removes the operational copies while leaving protected case evidence separately retained.

**Investigation question:** Which receipts prove access termination, and which prove derivative disposition?

- [Scenario and ground truth](scenario.md)
- [Evidence and source limits](evidence/README.md)
- [AIRG and evidence register](airg.md)
- [Analyst guide](analyst-guide.md)
- [Findings and recovery limits](findings.md)
- [Reproduce both conditions](reproduce.md)

The package contains 5 failure-condition events and 6
control-condition events. No external model, credential, system or person is used.
