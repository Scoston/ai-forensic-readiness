# Contributing

AI Forensic Readiness is currently a discussion draft. Contributions should make the model more testable, interoperable, proportionate, or operationally useful.

## Before proposing a change

Search existing issues and RFCs. For a new field, requirement, maturity criterion, or event type, explain:

1. The investigation question it answers.
2. The incident or exercise demonstrating the need.
3. The authoritative evidence source.
4. Privacy, privilege, retention, and access implications.
5. Whether an equivalent construct already exists in OCSF, OpenTelemetry, an identity standard, or another maintained specification.
6. How the proposal can be tested.

## Contribution routes

- **Clarification or typo:** Open a pull request.
- **Material specification change:** Open a proposal issue, then add an RFC after initial discussion.
- **New reference case:** Use the case template and include reproducible evidence-generation steps.
- **Schema change:** Include valid and invalid examples plus compatibility notes.
- **Security concern:** Follow [SECURITY.md](SECURITY.md); do not disclose sensitive vulnerabilities in a public issue.

## Evidence language

Reference cases must distinguish:

- **Confirmed:** Directly supported by authoritative evidence.
- **Strongly supported:** Multiple reliable sources converge.
- **Inferred:** Plausible analytical conclusion with stated assumptions.
- **Disputed:** Credible evidence conflicts.
- **Unknown:** Required evidence is absent or unavailable.

Do not present an AI-generated narrative as independent corroboration.

## Pull-request expectations

- Keep the proposal focused.
- Update the changelog when behavior or meaning changes.
- Validate JSON files against their schemas.
- Lint Mermaid source.
- Preserve neutral, vendor-independent language.
- Identify backward-incompatible changes.
- Confirm that examples contain no secrets, personal information, customer data, or proprietary prompts.

By contributing, you agree that specification prose and diagrams are licensed under CC BY 4.0 and code-like artifacts are licensed under Apache-2.0.

