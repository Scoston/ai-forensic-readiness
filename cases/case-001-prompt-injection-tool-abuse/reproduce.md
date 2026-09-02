# Safe reproduction and validation

## Safety properties

This package is designed for offline review. It contains no executable prompt injection, live credential, customer data, or routable destination. Do not replace `.invalid` URLs with real services or add real restricted information.

## Prerequisites

- Python 3.10 or later
- A clean checkout of the repository
- No third-party Python packages

## Validate the committed bundle

From the repository root:

```powershell
python .\scripts\validate.py
```

The validation must confirm:

- JSON and JSONL syntax;
- normalized event structure;
- event order and parent references;
- required case files;
- manifest path safety and completeness; and
- SHA-256 hashes for every manifested evidence artifact.

## Conduct a blind investigation

1. Copy the case directory to a clean analysis workspace.
2. Give the investigator `analyst-guide.md`, `manifest.json`, and `evidence/`.
3. Withhold `scenario.md`, `airg.md`, and `findings.md` until the investigator submits a narrative.
4. Ask the investigator to build a timeline, authority chain, AIRG, containment inventory, and residual-risk statement.
5. Compare the result with the edge register and findings.
6. Record time to defensible narrative, incorrect certainty claims, missing pivots, and proposed evidence changes.

## Deterministic replay model

The fixtures represent this state transition without invoking an agent:

1. Start with `raw/state-before.json`.
2. Apply the read and transmission records in timestamp order.
3. Confirm `raw/state-after.json` represents the accepted external copy and active delegated session immediately after the action.
4. Apply the controls in `raw/containment-validation.json`.
5. Confirm the delegated session and connector are disabled while external-copy disposition remains `unknown`.

## Tamper test

To confirm that manifest verification detects modification:

1. Work only in a disposable copy of the case.
2. Change one byte in any file under `evidence/`.
3. Run `python .\scripts\validate.py`.
4. Confirm the validator reports a SHA-256 mismatch.
5. Delete the disposable copy; do not commit the modified evidence.

## Evidence-quality exercise

Run a second tabletop after removing one corroborating source, such as `network-egress.jsonl`. The investigator must lower confidence or explicitly record the new gap rather than preserving the original conclusion without support.

