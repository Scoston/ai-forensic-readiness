# Safe reproduction and validation

## Safety properties

This package is designed for offline review. It contains no executable prompt injection, live credential, personal information, production ticket, or routable destination. Do not replace `.invalid` URLs or `synthetic://` identifiers with real services.

## Prerequisites

- Python 3.10 or later
- A clean checkout of the repository
- No third-party Python packages

## Validate the committed bundle

From the repository root:

```powershell
python .\scripts\validate.py
```

Validation must confirm:

- JSON and JSONL syntax;
- normalized event structure, order, trace/session pairs, and parent references;
- required case files;
- manifest path safety, completeness, and SHA-256 values;
- source, memory, vector, read, and injected-context digest consistency;
- source removal before delayed execution;
- complete known-consumer containment evidence; and
- a controlled comparison in which active-memory availability is the only modeled difference.

## Conduct a blind investigation

1. Copy the case directory to a clean analysis workspace.
2. Give the investigator `analyst-guide.md`, `manifest.json`, and `evidence/`.
3. Withhold `scenario.md`, `airg.md`, `findings.md`, and the replay interpretation until the investigator submits a narrative.
4. Ask for a cross-session timeline, memory-lineage graph, consumer inventory, action reconstruction, containment assessment, and residual-risk statement.
5. Compare the result with the edge register and findings.
6. Record missed lineage pivots, incorrect certainty claims, and proposed evidence changes.

## Deterministic state replay

1. Begin with `raw/state-before.json`.
2. Apply the source retrieval, memory write, index creation, and cache insertion in timestamp order.
3. Apply the source-removal event without changing memory or derivative state.
4. Apply the later memory read, policy decision, tool execution, and ticket audit.
5. Confirm the after-action snapshot reports the ticket closed and all memory derivatives active.
6. Apply the containment actions and confirm the after-containment snapshot.

## Controlled comparison

Inspect `raw/replay-results.json`. Confirm both conditions use the same instruction digest, agent/model versions, system prompt, policy baseline, ticket snapshot, and replay seed. Confirm the only changed variable is `active_memory_availability`.

The expected outcomes are:

- **Poisoned condition:** `memory-0002` is retrieved and `close_ticket` is requested.
- **Quarantined condition:** no poisoned memory is retrieved and no close operation is requested.

Treat the result as support for influence, not access to private model reasoning.

## Tamper test

1. Work only in a disposable copy.
2. Change one byte in any file under `evidence/`.
3. Run `python .\scripts\validate.py`.
4. Confirm the validator reports a Case 002 SHA-256 mismatch.
5. Delete the disposable copy; do not commit modified evidence.

## Evidence-quality exercise

Repeat the blind investigation after removing `raw/memory-audit.jsonl` or `raw/replay-results.json`. The investigator must lower confidence in lineage or influence rather than preserving the original conclusion without support.
