# GE19 Repair30 Repair01 local runner — lock

## Status

The local Repair30 runner has been rebound to the locked Repair01 implementation after the first pre-science KeyError failure.

This remains the same Repair30 science contract.

## Runner

File:

`ge19/run_local_repair30_reduced_h2_z11_reclosure.sh`.

Repair01 runner blob:

`d7b140ab459e9c91efe439405431f7f475d7926a`.

Repair01 runner commit:

`65255c61464e8325ed6e4684de81d68b9acb0aa4`.

Static audit:

- run:
  `35749772381`;
- job:
  `106820567336`;
- conclusion:
  `success`.

## Bound implementation

Repair01 science implementation:

- blob:
  `a014dd3a56914858cb6ca7e0f5bdd45afdf573db`;
- commit:
  `37d8b6f1e2e5980f1f423c014b6a6b60157f78bd`.

Repair01 dedicated prelock:

- blob:
  `4cad3fee8bc4574cbf0aec8dcbd31944b877c5d5`;
- run:
  `35749669679`;
- conclusion:
  `success`.

Implementation-failure freeze:

- blob:
  `4e803520f73c97272a3f35ff62b017021908dc1d`;
- commit:
  `0939742f9c518818091bed8a84465b2148c73153`.

Repair01 implementation lock:

- blob:
  `6d41cbda64d0524217d342d8d45f728d4bba7948`;
- commit:
  `c19ff6dd3ccc859ec54c66edaa05048391f70a3c`.

## Science integrity

Unchanged from original Repair30 preregistration:

- equation:
  `L_total Z11=-M1[Z10,q10]`;
- B10:
  `X10-weighted_z10`;
- reduced dictionary;
- full-history inherited boundary;
- primary/control grids;
- C envelope;
- all thresholds;
- no H4/Z21 solve;
- no finite eta;
- no observational input.

The only Repair01 change is reading `rho_dark,p_dark` from the already-returned GE15 per-mode state dictionaries rather than from the background dictionary.

## Stop rule

No valid Repair30 science JSON has yet been generated.

Therefore the next local invocation remains the first valid Repair30 science execution.

A valid JSON with exit 0 or 2 must be frozen and not rerun under the same contract.
