# Findings

## Supported result

The served and approved descriptions have different digests in both conditions. The failure executes export_report. The control selects the same proposed operation but denies execution, exposing the distinction between selection and authority.

This result is confirmed within the deterministic model. Supporting records are
listed in [the AIRG register](airg.md); exact comparisons are in
[the replay result](evidence/raw/replay-results.json).

## Containment procedure

Disable the altered capability, pin the approved registry version, invalidate cached descriptions and review downstream export receipts.

## Recovery assessment

Denying subsequent exports cannot undo the failure-condition disclosure. Restoring the description repairs the control surface; recipient copy disposition remains outside this laboratory.

## Evidence limitations and alternatives

The selector is explicit Python logic. This does not measure prompt-injection susceptibility of any real model or MCP implementation.

No incident frequency, model behavior, human decision quality, latency or complete
enterprise inventory is measured. A real system may implement different delegation,
storage or review semantics. Validate the proposed control at the actual enforcement
boundary before claiming equivalent behavior.

## Proposed v0.2 requirement

Record the tool-description digest used for selection and recheck allowed operations at the resource boundary.
