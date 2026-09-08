# Case 008: Model and policy version drift

**Status:** Complete deterministic simulation bundle for the v0.2 discussion draft.

An evaluated baseline uses a synthetic-v1 model and read-only policy. Deployment changes the model label and policy to allow-delete without a matching evaluation baseline. The control pins deployment admission to the evaluated configuration digest.

**Investigation question:** Can the action be pinned to model, prompt, policy, tool and evaluation versions?

- [Scenario and ground truth](scenario.md)
- [Evidence and source limits](evidence/README.md)
- [AIRG and evidence register](airg.md)
- [Analyst guide](analyst-guide.md)
- [Findings and recovery limits](findings.md)
- [Reproduce both conditions](reproduce.md)

The package contains 5 failure-condition events and 4
control-condition events. No external model, credential, system or person is used.
