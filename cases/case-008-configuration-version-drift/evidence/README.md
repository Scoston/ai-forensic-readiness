# Evidence for Case 008

Baseline and deployed manifests with hashes, evaluation reference, admission decision and downstream state.

The files use synthetic data only. `records.jsonl` is the failure condition;
`records-control.jsonl` is the control. Each raw record has a stable record ID,
source, payload and declared parent. The normalized envelopes reference those
records and hash their deterministic JSON encoding. The manifest hashes exact
file bytes. These are consistency checks, not signatures or proof of authenticity.

The two conditions share one simulator and clock. Source names show where an
enterprise would collect evidence, not independent trust in this experiment.
`replay-results.json` states controlled and changed variables. The graph records
observed links and explicit unknowns; it does not infer hidden reasoning.
